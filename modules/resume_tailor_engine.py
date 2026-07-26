class ResumeTailorEngine:

    def analyze_job_fit(
        self,
        profile,
        job
    ):

        skills = profile.get("skills", [])

        description = job.get(
            "description",
            ""
        ).lower()

        matched = []
        missing = []

        for skill in skills:

            if skill.lower() in description:
                matched.append(skill)
            else:
                missing.append(skill)

        total = len(skills)

        score = 0

        if total:
            score = round(
                (len(matched) / total) * 100,
                2
            )

        recommendations = []

        if missing:

            recommendations.append(
                "Add or strengthen these skills where they accurately reflect your experience: "
                + ", ".join(missing[:10])
            )

        recommendations.append(
            "Quantify achievements using revenue, growth %, savings, or team size."
        )

        recommendations.append(
            "Mirror the terminology used in the job description."
        )

        recommendations.append(
            "Strengthen your executive summary to align with the target role."
        )

        return {

            "match_score": score,

            "matched_skills": matched,

            "missing_skills": missing,

            "recommendations": recommendations
        }

    def generate_executive_summary(
        self,
        profile,
        job
    ):

        role = job.get(
            "role",
            job.get("title", "Executive Role")
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
            f"Executive leader with {experience} years of experience driving revenue growth, "
            f"business transformation, customer success and operational excellence across "
            f"{industry}. Proven record of leading strategic initiatives and delivering "
            f"measurable business outcomes, making a strong fit for {role}."
        )