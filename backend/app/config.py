import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback_dev_key_change_in_prod")
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/quickcv")
    WTF_CSRF_ENABLED = False  # Disabled for API — frontend handles CSRF separately
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "None"  # Allow cross-site cookies
    SESSION_COOKIE_SECURE = True       # Only send cookies over HTTPS
    REMEMBER_COOKIE_HTTPONLY = True
    # CORS origins (comma-separated)
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://127.0.0.1:5500,http://localhost:5500")

    # File storage: `local` stores under UPLOAD_DIR, `cloud` uses Cloudinary
    # Backward compatibility: FILE_STORAGE / LOCAL_UPLOAD_DIR are still respected.
    UPLOAD_STORAGE = os.environ.get("UPLOAD_STORAGE", os.environ.get("FILE_STORAGE", "cloud")).strip().lower()
    _backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    UPLOAD_DIR = os.path.abspath(
        os.environ.get(
            "UPLOAD_DIR",
            os.environ.get("LOCAL_UPLOAD_DIR", os.path.join(_backend_root, "uploads")),
        )
    )
    try:
        MAX_IMAGE_UPLOAD_BYTES = int(os.environ.get("MAX_IMAGE_UPLOAD_BYTES", "2097152"))
    except ValueError:
        MAX_IMAGE_UPLOAD_BYTES = 2097152