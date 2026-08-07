from datetime import datetime


class ResumeGenerator:

    def __init__(self):

        pass

    # --------------------------------------------------

    def generate_resume(
        self,
        profile,
        job,
        tailoring,
    ):

        return {

            "executive_summary":
                self.executive_summary(
                    profile,
                    job,
                ),

            "core_skills":
                self.core_skills(
                    profile,
                    tailoring,
                ),

            "professional_experience":
                self.professional_experience(
                    profile,
                ),

            "achievements":
                self.achievements(
                    profile,
                ),

            "education":
                self.education(
                    profile,
                ),

            "ats_keywords":
                tailoring.get(
                    "recommended_keywords",
                    [],
                ),

            "generated_on":
                datetime.now().strftime(
                    "%d-%m-%Y %H:%M"
                )

        }

    # --------------------------------------------------

    def executive_summary(
        self,
        profile,
        job,
    ):

        role = job.get(
            "role",
            job.get(
                "title",
                "Executive Position"
            )
        )

        years = profile.get(
            "experience",
            "20+"
        )

        return (
            f"Executive Leader with {years} years of experience "
            f"delivering commercial growth, business transformation, "
            f"customer success, strategic partnerships and P&L ownership. "
            f"Experienced in leading high-performing teams, driving revenue "
            f"growth and operational excellence. "
            f"Target Position: {role}."
        )

    # --------------------------------------------------

    def core_skills(
        self,
        profile,
        tailoring,
    ):

        skills = list(
            profile.get(
                "skills",
                []
            )
        )

        for keyword in tailoring.get(
            "recommended_keywords",
            []
        ):

            if keyword not in skills:

                skills.append(keyword)

        return sorted(skills)
        # --------------------------------------------------

    def professional_experience(
        self,
        profile,
    ):

        experience = []

        for job in profile.get(
            "experience_details",
            []
        ):

            experience.append({

                "company":
                    job.get(
                        "company",
                        ""
                    ),

                "designation":
                    job.get(
                        "designation",
                        ""
                    ),

                "duration":
                    job.get(
                        "duration",
                        ""
                    ),

                "responsibilities":
                    job.get(
                        "responsibilities",
                        []
                    ),

            })

        return experience

    # --------------------------------------------------

    def achievements(
        self,
        profile,
    ):

        achievements = profile.get(
            "achievements",
            []
        )

        if not achievements:

            achievements = [

                "Delivered consistent revenue growth.",

                "Built strategic customer relationships.",

                "Managed executive stakeholders.",

                "Led business transformation initiatives.",

                "Improved operational excellence.",

            ]

        return achievements

    # --------------------------------------------------

    def education(
        self,
        profile,
    ):

        return profile.get(
            "education",
            []
        )

    # --------------------------------------------------

    def recruiter_resume(
        self,
        profile,
        job,
        tailoring,
    ):

        resume = self.generate_resume(

            profile,

            job,

            tailoring,

        )

        resume["version"] = "Recruiter"

        return resume

    # --------------------------------------------------

    def hiring_manager_resume(
        self,
        profile,
        job,
        tailoring,
    ):

        resume = self.generate_resume(

            profile,

            job,

            tailoring,

        )

        resume["version"] = "Hiring Manager"

        return resume
    