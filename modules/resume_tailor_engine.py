class ResumeTailorEngine:

    # --------------------------------------------------

    def tailor_resume(
        self,
        profile,
        job,
    ):

        fit = self.analyze_job_fit(
            profile,
            job,
        )

        summary = self.generate_executive_summary(
            profile,
            job,
        )

        keywords = fit["matched_skills"] + fit["missing_skills"]

        tailored_resume = f"""
EXECUTIVE SUMMARY

{summary}

CORE EXECUTIVE COMPETENCIES

{self._format_keywords(keywords)}

KEY ACHIEVEMENTS

• Delivered predictable revenue growth
• Managed P&L ownership
• Built high-performing leadership teams
• Led business transformation initiatives
• Improved customer success
• Developed strategic partnerships

ATS MATCH SCORE : {fit['match_score']}%

RECOMMENDATIONS

{self._format_recommendations(fit['recommendations'])}
"""

        return tailored_resume

    # --------------------------------------------------

    def analyze_job_fit(
        self,
        profile,
        job
    ):

        profile_skills = [

            str(skill).lower()

            for skill in profile.get(
                "skills",
                []
            )

        ]

        text = (

            job.get(
                "description",
                ""
            )

            + " "

            + job.get(
                "role",
                job.get(
                    "title",
                    ""
                )
            )

        ).lower()

        matched = []

        missing = []

        for skill in profile_skills:

            if skill in text:

                matched.append(skill)

            else:

                missing.append(skill)

                total = len(profile_skills)

        score = round(

            (

                len(matched)

                /

                total

            ) * 100,

            2,

        ) if total else 0

        recommendations = []

        if missing:

            recommendations.append(

                "Include these keywords where they genuinely match your experience: "

                + ", ".join(missing[:15])

            )

        recommendations.append(

            "Quantify achievements using revenue, profit, growth %, customer acquisition, project values and team size."

        )

        recommendations.append(

            "Mirror the wording used in the Job Description."

        )

        recommendations.append(

            "Rewrite your Executive Summary specifically for this role."

        )

        recommendations.append(

            "Prioritize measurable leadership achievements."

        )

        recommendations.append(

            "Place the strongest matching keywords in the first page."

        )

        return {

            "match_score": score,

            "matched_skills": sorted(matched),

            "missing_skills": sorted(missing),

            "recommended_keywords": sorted(

                list(

                    set(

                        matched + missing

                    )

                )

            ),

            "recommendations": recommendations,

        }

    # --------------------------------------------------

    def generate_executive_summary(

        self,

        profile,

        job,

    ):

        role = job.get(

            "role",

            job.get(

                "title",

                "Executive Role",

            ),

        )

        experience = profile.get(

            "experience",

            "20+",

        )

        industry = profile.get(

            "industry",

            "Technology",

        )

        return (

            f"Executive Leader with {experience} years of experience delivering "

            f"commercial growth, strategic leadership, operational excellence, "

            f"P&L ownership, customer success and business transformation across "

            f"{industry}. Strong alignment for the position of {role}."

        )
        # --------------------------------------------------

    def _format_keywords(
        self,
        keywords,
    ):

        if not keywords:

            return "No keywords identified."

        return "\n".join(

            [

                f"• {keyword.title()}"

                for keyword in keywords

            ]

        )

    # --------------------------------------------------

    def _format_recommendations(
        self,
        recommendations,
    ):

        if not recommendations:

            return "No recommendations."

        return "\n".join(

            [

                f"• {item}"

                for item in recommendations

            ]

        )

    # --------------------------------------------------

    def recruiter_resume(
        self,
        profile,
        job,
    ):

        return self.tailor_resume(

            profile,

            job,

        )

    # --------------------------------------------------

    def hiring_manager_resume(
        self,
        profile,
        job,
    ):

        return self.tailor_resume(

            profile,

            job,

        )

    # --------------------------------------------------

    def ats_resume(
        self,
        profile,
        job,
    ):

        return self.tailor_resume(

            profile,

            job,

        )

    # --------------------------------------------------

    def executive_resume(
        self,
        profile,
        job,
    ):

        return self.tailor_resume(

            profile,

            job,

        )

    # --------------------------------------------------

    def export_package(
        self,
        profile,
        job,
    ):

        resume = self.tailor_resume(

            profile,

            job,

        )

        fit = self.analyze_job_fit(

            profile,

            job,

        )

        return {

            "resume": resume,

            "ats_score": fit["match_score"],

            "matched_skills": fit["matched_skills"],

            "missing_skills": fit["missing_skills"],

            "recommended_keywords": fit["recommended_keywords"],

            "executive_summary": self.generate_executive_summary(

                profile,

                job,

            ),

        }