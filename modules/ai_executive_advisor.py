class AIExecutiveAdvisor:

    def generate_advice(self, profile, jobs):

        total_jobs = len(jobs)

        experience = profile.get("experience", 0)

        if total_jobs == 0:

            return {
                "summary": "No executive opportunities found today.",
                "priority": "Search more global markets.",
                "next_steps": [
                    "Update your resume.",
                    "Expand country preferences.",
                    "Increase recruiter outreach."
                ]
            }

        return {
            "summary": (
                f"You have {total_jobs} executive opportunities available. "
                f"With {experience}+ years of experience, focus on leadership and global roles."
            ),
            "priority": "Apply to the highest Executive Score jobs first.",
            "next_steps": [
                "Tailor resume for Top 5 jobs.",
                "Contact recruiters on LinkedIn.",
                "Prepare executive interview stories.",
                "Follow up within 48 hours."
            ]
        }