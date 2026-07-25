class ResumeTailorEngine:


    def analyze_job_fit(
        self,
        profile,
        job
    ):

        skills = profile.get(
            "skills",
            []
        )


        description = job.get(
            "description",
            ""
        ).lower()


        matched = []

        missing = []


        for skill in skills:

            if skill.lower() in description:

                matched.append(
                    skill
                )

            else:

                missing.append(
                    skill
                )


        total = len(skills)


        match_score = 0


        if total > 0:

            match_score = round(
                (len(matched) / total) * 100,
                2
            )


        return {

            "match_score": match_score,

            "matched_skills": matched,

            "missing_skills": missing

        }



    def generate_executive_summary(
        self,
        profile,
        job
    ):


        role = job.get(
            "role",
            "Executive Role"
        )


        experience = profile.get(
            "experience",
            "20+"
        )


        industry = profile.get(
            "industry",
            "Technology"
        )


        return (

            f"Results-driven executive leader with {experience} "
            f"years of experience driving revenue growth, "
            f"business transformation, and operational excellence "
            f"across {industry}. Proven ability to lead strategic "
            f"initiatives and deliver measurable outcomes for "
            f"{role} opportunities."

        )