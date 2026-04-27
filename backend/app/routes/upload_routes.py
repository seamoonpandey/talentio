import hashlib
import os
import time
import uuid

from flask import Blueprint, current_app, request, send_file, url_for
from flask_login import current_user
from werkzeug.utils import safe_join, secure_filename

from app.utils.decorators import login_required_api
from app.utils.response import error, success

upload_bp = Blueprint("uploads", __name__)

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def _get_storage_mode() -> str:
    mode = (current_app.config.get("UPLOAD_STORAGE") or "cloud").strip().lower()
    return mode if mode in {"local", "cloud"} else "cloud"


def _has_cloudinary_credentials() -> bool:
    return bool(
        os.environ.get("CLOUDINARY_CLOUD_NAME", "").strip()
        and os.environ.get("CLOUDINARY_API_KEY", "").strip()
        and os.environ.get("CLOUDINARY_API_SECRET", "").strip()
    )


def _ensure_local_upload_dir() -> str:
    upload_dir = current_app.config.get("UPLOAD_DIR", "").strip()
    if not upload_dir:
        upload_dir = os.path.abspath(os.path.join(current_app.root_path, "..", "uploads"))
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir


def _cloudinary_sign(params: dict, api_secret: str) -> str:
    """Create a Cloudinary signature from params.

    Cloudinary signing rules:
    - Sort params by key
    - Join as key=value with &
    - Append API secret
    - SHA1 hex digest
    """
    parts = []
    for key in sorted(params.keys()):
        value = params.get(key)
        if value is None or value == "":
            continue
        parts.append(f"{key}={value}")

    to_sign = "&".join(parts) + api_secret
    return hashlib.sha1(to_sign.encode("utf-8")).hexdigest()


@upload_bp.route("/config", methods=["GET"])
@login_required_api
def get_upload_config():
    storage = _get_storage_mode()

    if storage == "local":
        return success(
            data={
                "storage": "local",
                "upload_endpoint": "/api/uploads/profile-image",
            }
        )

    if not _has_cloudinary_credentials():
        return error("Cloud storage is enabled but Cloudinary is not fully configured.", 500)

    return success(data={"storage": "cloud"})


@upload_bp.route("/profile-image", methods=["POST"])
@login_required_api
def upload_profile_image_local():
    if _get_storage_mode() != "local":
        return error("Local file upload is disabled for current storage mode.", 400)

    file_obj = request.files.get("file")
    if not file_obj:
        return error("No file provided.")

    max_bytes = int(current_app.config.get("MAX_IMAGE_UPLOAD_BYTES", 2097152) or 2097152)
    file_obj.stream.seek(0, os.SEEK_END)
    file_size = file_obj.stream.tell()
    file_obj.stream.seek(0)
    if file_size > max_bytes:
        return error(f"Image is too large. Max allowed size is {max_bytes} bytes.", 400)

    filename = secure_filename(file_obj.filename or "")
    if not filename:
        return error("Invalid file name.")

    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return error("Unsupported image type. Use jpg, jpeg, png, webp, or gif.", 400)

    if not (file_obj.mimetype or "").startswith("image/"):
        return error("Only image uploads are allowed.", 400)

    uploads_root = _ensure_local_upload_dir()
    rel_dir = os.path.join("cv_profile_images", str(current_user.id))
    abs_dir = os.path.join(uploads_root, rel_dir)
    os.makedirs(abs_dir, exist_ok=True)

    unique_name = f"{int(time.time())}_{uuid.uuid4().hex[:12]}{ext}"
    abs_path = os.path.join(abs_dir, unique_name)
    file_obj.save(abs_path)

    rel_file_path = "/".join(["cv_profile_images", str(current_user.id), unique_name])
    file_url = url_for("uploads.get_local_upload_file", file_path=rel_file_path, _external=True)

    return success(
        data={
            "storage": "local",
            "url": file_url,
            "path": rel_file_path,
        },
        message="Image uploaded.",
    )


@upload_bp.route("/files/<path:file_path>", methods=["GET"])
def get_local_upload_file(file_path):
    uploads_root = _ensure_local_upload_dir()
    abs_path = safe_join(uploads_root, file_path)

    if not abs_path or not os.path.isfile(abs_path):
        return error("File not found.", 404)

    return send_file(abs_path)


@upload_bp.route("/cloudinary-signature", methods=["GET"])
@login_required_api
def get_cloudinary_signature():
    if _get_storage_mode() != "cloud":
        return error("Cloudinary signature is unavailable for current storage mode.", 400)

    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME", "").strip()
    api_key = os.environ.get("CLOUDINARY_API_KEY", "").strip()
    api_secret = os.environ.get("CLOUDINARY_API_SECRET", "").strip()
    folder_root = os.environ.get("CLOUDINARY_FOLDER", "quickcv").strip().strip("/")

    if not cloud_name or not api_key or not api_secret:
        return error("Cloudinary is not configured on the server.", 500)

    timestamp = int(time.time())
    folder = f"{folder_root}/cv_profile_images/{current_user.id}"

    params_to_sign = {
        "timestamp": timestamp,
        "folder": folder,
    }

    signature = _cloudinary_sign(params_to_sign, api_secret)

    return success(
        data={
            "cloud_name": cloud_name,
            "api_key": api_key,
            "timestamp": timestamp,
            "signature": signature,
            "folder": folder,
        }
    )
