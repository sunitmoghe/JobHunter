class JobSkillMatcher:

    def __init__(self):
        pass

    def match(self, profile, job):
        """
        Simple ATS Skill Matching
        """

        profile_text = str(profile).lower()

        job_text = (
            str(job.get("description", "")) +
            " " +
            str(job.get("role", ""))
        ).lower()

        common_skills = [
            "sales",
            "leadership",
            "operations",
            "customer service",
            "business development",
            "strategy",
            "crm",
            "erp",
            "saas",
            "forecasting",
            "p&l",
            "key account",
            "negotiation",
            "executive",
            "management",
        ]

        matched = []

        missing = []

        for skill in common_skills:

            if skill in profile_text and skill in job_text:
                matched.append(skill)

            elif skill in job_text:
                missing.append(skill)

        score = 0

        if len(common_skills):

            score = round(
                len(matched) /
                len(common_skills) *
                100
            )

        return {
            "score": score,
            "matched_skills": matched,
            "missing_skills": missing,
        }