import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from pymongo import MongoClient


def build_cv_doc(user):
    user_id = str(user["_id"])
    full_name = user.get("full_name", "Avery Jordan")
    email = user.get("email", "avery.jordan@example.com")

    return {
        "user_id": user_id,
        "title": "Principal Product Designer · Full Stack",
        "template": "slate",
        "personal_info": {
            "full_name": full_name,
            "profile_image": "https://images.unsplash.com/photo-1544723795-3fb6469f5b39?auto=format&fit=crop&w=640&q=80",
            "email": email,
            "phone": "+1 (415) 555-0189",
            "location": "San Francisco, CA",
            "website": "https://portfolio.averyjordan.design",
            "social_links": [
                {"label": "LinkedIn", "url": "https://www.linkedin.com/in/averyjordan"},
                {"label": "GitHub", "url": "https://github.com/averyjordan"},
                {"label": "Behance", "url": "https://www.behance.net/averyjordan"},
            ],
            "summary": (
                "Product leader blending UX research, visual design, and full-stack engineering to ship "
                "high-impact experiences. Led cross-functional teams to launch AI-driven SaaS features, "
                "modernize design systems, and deliver measurable growth across fintech and health tech."
            ),
        },
        "education": [
            {
                "institution": "Rhode Island School of Design",
                "degree": "MFA, Digital + Experience Design",
                "start_date": "2016",
                "end_date": "2018",
                "description": "Thesis on adaptive interfaces for predictive health coaching."
            },
            {
                "institution": "University of California, Berkeley",
                "degree": "BS, Cognitive Science",
                "start_date": "2011",
                "end_date": "2015",
                "description": "Focus on human-computer interaction, cognitive systems, and data visualization."
            },
        ],
        "experience": [
            {
                "job_title": "Principal Product Designer",
                "company": "Northwind AI",
                "start_date": "2023",
                "end_date": "Present",
                "description": (
                    "Owned end-to-end design for an AI analytics suite used by 2,400+ teams. "
                    "Launched multi-tenant reporting, reducing time-to-insight by 38% and boosting ARR by $4.2M."
                ),
            },
            {
                "job_title": "Senior Product Designer",
                "company": "Kairo Health",
                "start_date": "2020",
                "end_date": "2023",
                "description": (
                    "Built a clinician workflow platform serving 180+ hospitals. "
                    "Introduced a scalable design system and cut release friction by 45%."
                ),
            },
            {
                "job_title": "Full-Stack UX Engineer",
                "company": "Vela Labs",
                "start_date": "2018",
                "end_date": "2020",
                "description": (
                    "Bridged product and engineering by shipping React + Flask tooling, "
                    "automating onboarding and lifting activation by 22%."
                ),
            },
        ],
        "skills": [
            "Product Strategy",
            "Design Systems",
            "User Research",
            "Figma",
            "Prototyping",
            "React",
            "TypeScript",
            "Flask",
            "Data Visualization",
            "A/B Testing",
            "Information Architecture",
        ],
        "certificates": [
            {
                "name": "Design Leadership Accelerator",
                "issuer": "IDEO U",
                "date": "2022",
                "description": "Advanced leadership training for scaling design teams and operational excellence."
            },
            {
                "name": "Data-Informed UX",
                "issuer": "Nielsen Norman Group",
                "date": "2021",
                "description": "Quant + qual research certification for product teams."
            },
        ],
        "custom_sections": [
            {
                "title": "Selected Launches",
                "content": (
                    "Shipped an AI forecasting dashboard for fintech executives; led a 9-week "
                    "design sprint that improved product NPS from 42 to 61."
                ),
            },
            {
                "title": "Speaking",
                "content": "Keynote speaker at Config, UXDX, and HealthTech Summit on design + AI." 
            },
        ],
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }


def main():
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/quickcv")
    client = MongoClient(mongo_uri)
    db = client.get_database()

    user = db.users.find_one()
    if not user:
        print("No users found in the database. Create a user first, then re-run.")
        return 1

    cv_doc = build_cv_doc(user)
    result = db.cvs.insert_one(cv_doc)
    print(f"Seeded CV {result.inserted_id} for user {user.get('email', user.get('_id'))}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
