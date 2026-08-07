class RecruiterIntelligenceEngine:

    def get_recruiter_summary(self, recruiter):

        if recruiter is None:
            recruiter = {}

        return {
            "rating": recruiter.get("rating", "4.5/5"),
            "response_rate": recruiter.get("response_rate", "68%"),
            "linkedin": recruiter.get("linkedin", ""),
            "recommendation": recruiter.get(
                "recommendation",
                "Reach out within 24 hours of applying."
            )
        }

    def recruiter_score(self, recruiter):

        if recruiter is None:
            return 75

        return recruiter.get("score", 75)

    def recruiter_priority(self, recruiter):

        score = self.recruiter_score(recruiter)

        if score >= 90:
            return "High"

        elif score >= 75:
            return "Medium"

        return "Low"