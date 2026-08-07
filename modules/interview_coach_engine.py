class InterviewCoachEngine:

    def generate_questions(self, profile, job):

        role = job.get(
            "role",
            job.get("title", "Executive")
        )

        company = job.get(
            "company",
            "the company"
        )

        return [
            f"Tell us about your leadership experience relevant to the {role} role.",
            "Describe a major business transformation you successfully led.",
            "How have you managed P&L responsibility?",
            "Tell us about your biggest revenue growth achievement.",
            "Describe a difficult stakeholder management situation.",
            f"Why do you want to join {company}?",
            "How would your previous team describe your leadership style?",
            "What would your 90-day plan be if selected?",
            "Describe a crisis you handled successfully.",
            "Why should we hire you over other executive candidates?"
        ]