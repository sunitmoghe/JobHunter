class OpportunityScoreEngine:

    def calculate(self, job):

        score = 0

        # --------------------------------------------------
        # Executive Score (40)
        # --------------------------------------------------

        score += (
            job.get(
                "executive_score",
                0
            ) * 0.40
        )

        # --------------------------------------------------
        # JobHunter Score (20)
        # --------------------------------------------------

        score += (
            job.get(
                "jobhunter_score",
                0
            ) * 0.20
        )

        # --------------------------------------------------
        # Company Rating (10)
        # --------------------------------------------------

        score += (
            job.get(
                "company_rating",
                3
            ) * 2
        )

        # --------------------------------------------------
        # Company Growth
        # --------------------------------------------------

        score += (
            job.get(
                "growth_score",
                50
            ) * 0.10
        )

        # --------------------------------------------------
        # Fortune 500
        # --------------------------------------------------

        if job.get(
            "fortune500",
            False
        ):
            score += 5

        # --------------------------------------------------
        # Verified Employer
        # --------------------------------------------------

        if job.get(
            "verified_company",
            False
        ):
            score += 3

        # --------------------------------------------------
        # Visa Sponsorship
        # --------------------------------------------------

        if job.get(
            "visa_sponsorship",
            False
        ):
            score += 8

        # --------------------------------------------------
        # Remote Friendly
        # --------------------------------------------------

        if job.get(
            "remote_friendly",
            False
        ):
            score += 5

        # --------------------------------------------------
        # Recruiter Available
        # --------------------------------------------------

        if job.get(
            "recruiter_found",
            False
        ):
            score += 5

        # --------------------------------------------------
        # Hiring Trend
        # --------------------------------------------------

        trend = str(
            job.get(
                "hiring_trend",
                ""
            )
        ).lower()

        if "growing" in trend:
            score += 5

        elif "stable" in trend:
            score += 3

        # --------------------------------------------------
        # Layoff Risk
        # --------------------------------------------------

        layoff = str(
            job.get(
                "layoff_risk",
                ""
            )
        ).lower()

        if layoff == "low":
            score += 3

        elif layoff == "medium":
            score += 1

        elif layoff == "high":
            score -= 5

        # --------------------------------------------------
        # Final Score
        # --------------------------------------------------

        final_score = max(
            0,
            min(
                int(score),
                100
            )
        )

        if final_score >= 95:

            rating = "★★★★★ Elite Opportunity"

        elif final_score >= 85:

            rating = "★★★★ Excellent Opportunity"

        elif final_score >= 75:

            rating = "★★★ Strong Opportunity"

        elif final_score >= 65:

            rating = "★★ Good Opportunity"

        else:

            rating = "★ Low Priority"

        return {

            "score": final_score,

            "rating": rating

        }


if __name__ == "__main__":

    engine = OpportunityScoreEngine()

    sample = {

        "executive_score": 92,
        "jobhunter_score": 90,
        "company_rating": 5,
        "growth_score": 96,
        "fortune500": True,
        "verified_company": True,
        "visa_sponsorship": True,
        "remote_friendly": True,
        "recruiter_found": True,
        "hiring_trend": "Growing",
        "layoff_risk": "Low"

    }

    print(engine.calculate(sample))