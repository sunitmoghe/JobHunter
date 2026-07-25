from modules.database import DatabaseManager
from modules.job_matcher_engine import JobMatcherEngine
from modules.priority_engine import PriorityEngine


def get_recommendations():

    db = DatabaseManager()

    profile = db.get_latest_profile()


    if profile is None:
        return []


    db.cursor.execute(
        """
        SELECT
            role,
            company,
            country,
            skills
        FROM jobs
        """
    )


    jobs = db.cursor.fetchall()


    matcher = JobMatcherEngine()

    priority_engine = PriorityEngine()


    recommendations = []


    for job in jobs:

        job_data = {

            "role": job[0],
            "company": job[1],
            "country": job[2],
            "skills": job[3]

        }


        result = matcher.calculate_match(
            profile,
            job_data
        )


        priority = priority_engine.calculate_priority(
            job_data,
            result["score"]
        )


        recommendations.append({

            "role": job[0],

            "company": job[1],

            "country": job[2],

            "score": result["score"],

            "priority_score": priority["priority_score"],

            "priority_category": priority["category"],

            "matched": result["matched"],

            "missing": result["missing"]

        })


    recommendations.sort(
        key=lambda x: x["priority_score"],
        reverse=True
    )


    db.close()


    return recommendations