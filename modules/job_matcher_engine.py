from modules.skill_intelligence import SkillIntelligence


class JobMatcherEngine:

    def __init__(self):

        self.skill_engine = SkillIntelligence()

    # --------------------------------------------------

    def calculate_match(
        self,
        profile,
        job
    ):

        if not profile:

            raise Exception(
                "No executive profile found."
            )

        profile_skills = self.skill_engine.normalize_skills(

            profile.get(
                "skills",
                []
            )

        )

        raw_job_skills = job.get(
            "skills",
            []
        )

        if isinstance(raw_job_skills, str):

            raw_job_skills = [

                skill.strip()

                for skill in raw_job_skills.split(",")

                if skill.strip()

            ]

        job_skills = self.skill_engine.normalize_skills(
            raw_job_skills
        )

        matched = profile_skills.intersection(
            job_skills
        )

        missing = job_skills.difference(
            profile_skills
        )

        score = 0

        if job_skills:

            score = round(

                (

                    len(matched)
                    /
                    len(job_skills)

                ) * 100,

                1

            )

        return {

            "score": score,

            "matched": sorted(list(matched)),

            "missing": sorted(list(missing)),

            "matched_count": len(matched),

            "missing_count": len(missing)

        }