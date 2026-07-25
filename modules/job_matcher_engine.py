from modules.database import DatabaseManager
from modules.skill_intelligence import SkillIntelligence



class JobMatcherEngine:


    def calculate_match(self, profile, job):

        if profile is None:
            raise Exception(
                "No executive profile found."
            )


        skill_engine = SkillIntelligence()


        profile_skills = skill_engine.normalize_skills(
            profile["skills"]
        )


        job_skills = skill_engine.normalize_skills(
            job["skills"].split(",")
        )


        matched = profile_skills.intersection(
            job_skills
        )


        missing = job_skills.difference(
            profile_skills
        )


        score = 0

        if len(job_skills) > 0:

            score = int(
                (len(matched) / len(job_skills)) * 100
            )


        return {

            "score": score,

            "matched": list(matched),

            "missing": list(missing)

        }



def test_match():

    db = DatabaseManager()


    profile = db.get_latest_profile()


    db.cursor.execute(
        """
        SELECT role, company, country, skills
        FROM jobs
        LIMIT 1
        """
    )


    row = db.cursor.fetchone()


    job = {

        "role": row[0],
        "company": row[1],
        "country": row[2],
        "skills": row[3]

    }


    matcher = JobMatcherEngine()


    result = matcher.calculate_match(
        profile,
        job
    )


    print(result)



if __name__ == "__main__":

    test_match()