class ExecutiveDecisionCenter:

    def __init__(self):
        self.preferred_countries = {
            "Singapore",
            "Germany",
            "United Kingdom",
            "Australia",
            "New Zealand",
            "Finland",
            "Poland",
            "UAE",
            "Saudi Arabia",
            "Malaysia",
            "Canada",
            "India",
        }

    # --------------------------------------------------
    # DECISION
    # --------------------------------------------------

    def decide(self, job):

        ranking_score = self._number(
            job.get("ranking_score", 0)
        )

        executive_score = self._number(
            job.get("executive_score", 0)
        )

        country = str(
            job.get("country", "")
        ).strip()

        has_apply = self._boolean(
            job.get(
                "has_apply_link",
                job.get("apply_link", "")
            )
        )

        visa = self._boolean(
            job.get(
                "visa_sponsorship",
                job.get("has_visa", False)
            )
        )

        reasons = []
        risks = []

        # --------------------------------------------------
        # RANKING
        # --------------------------------------------------

        if ranking_score >= 85:

            reasons.append(
                "Excellent overall executive ranking."
            )

        elif ranking_score >= 75:

            reasons.append(
                "Strong overall executive ranking."
            )

        elif ranking_score >= 65:

            reasons.append(
                "Moderate overall executive ranking."
            )

        else:

            risks.append(
                "Overall ranking is below preferred threshold."
            )

        # --------------------------------------------------
        # EXECUTIVE SENIORITY
        # --------------------------------------------------

        role = str(
            job.get(
                "title",
                job.get("role", "")
            )
        ).lower()

        seniority_keywords = [
            "chief",
            "ceo",
            "coo",
            "cro",
            "cto",
            "cfo",
            "president",
            "vice president",
            "vp",
            "director",
            "head",
            "general manager",
            "country manager",
            "country head",
            "regional head",
        ]

        if any(
            keyword in role
            for keyword in seniority_keywords
        ):

            reasons.append(
                "Role has strong executive seniority alignment."
            )

        else:

            risks.append(
                "Role seniority may be below target executive level."
            )

        # --------------------------------------------------
        # SALES / BUSINESS ALIGNMENT
        # --------------------------------------------------

        leadership_keywords = [
            "sales",
            "business development",
            "commercial",
            "revenue",
            "growth",
            "partnership",
            "account",
            "customer",
        ]

        if any(
            keyword in role
            for keyword in leadership_keywords
        ):

            reasons.append(
                "Strong sales/business leadership alignment."
            )

        # --------------------------------------------------
        # STRATEGIC ALIGNMENT
        # --------------------------------------------------

        strategic_keywords = [
            "revenue",
            "p&l",
            "profit",
            "growth",
            "transformation",
            "strategy",
            "commercial",
            "business unit",
        ]

        description = str(
            job.get(
                "description",
                ""
            )
        ).lower()

        combined_text = (
            role
            + " "
            + description
        )

        if any(
            keyword in combined_text
            for keyword in strategic_keywords
        ):

            reasons.append(
                "Strong revenue, P&L, growth or transformation alignment."
            )

        # --------------------------------------------------
        # APPLICATION ROUTE
        # --------------------------------------------------

        if has_apply:

            reasons.append(
                "Direct application route is available."
            )

        else:

            risks.append(
                "No direct application link detected."
            )

        # --------------------------------------------------
        # COUNTRY
        # --------------------------------------------------

        if country:

            if country in self.preferred_countries:

                reasons.append(
                    "Location matches a preferred job market."
                )

            else:

                risks.append(
                    "Country is outside preferred markets."
                )

        else:

            risks.append(
                "Country information is unavailable."
            )

        # --------------------------------------------------
        # VISA
        # --------------------------------------------------

        if visa:

            reasons.append(
                "Visa sponsorship appears to be available."
            )

        # --------------------------------------------------
        # DECISION SCORE
        # --------------------------------------------------

        decision_score = ranking_score

        if executive_score:

            decision_score = (
                ranking_score * 0.70
                + executive_score * 0.30
            )

        if has_apply:

            decision_score += 3

        if visa:

            decision_score += 2

        if country in self.preferred_countries:

            decision_score += 3

        decision_score = round(
            min(
                decision_score,
                100
            ),
            2
        )

        # --------------------------------------------------
        # FINAL DECISION
        # --------------------------------------------------

        if decision_score >= 85:

            decision = "PRIORITIZE"

        elif decision_score >= 75:

            decision = "APPLY"

        elif decision_score >= 65:

            decision = "CONSIDER"

        else:

            decision = "LOW PRIORITY"

        return {
            "decision": decision,
            "decision_score": decision_score,
            "reasons": reasons,
            "risks": risks,
        }

    # --------------------------------------------------
    # ANALYZE JOBS
    # --------------------------------------------------

    def analyze_jobs(self, jobs):

        analyzed = []

        for job in jobs:

            item = dict(job)

            result = self.decide(item)

            item["decision"] = (
                result["decision"]
            )

            item["decision_score"] = (
                result["decision_score"]
            )

            item["decision_reasons"] = (
                result["reasons"]
            )

            item["decision_risks"] = (
                result["risks"]
            )

            analyzed.append(item)

        analyzed.sort(
            key=lambda x: self._number(
                x.get(
                    "decision_score",
                    0
                )
            ),
            reverse=True,
        )

        for position, job in enumerate(
            analyzed,
            start=1
        ):

            job["decision_position"] = position

        return analyzed

    # --------------------------------------------------
    # FILTER
    # --------------------------------------------------

    def filter_decisions(
        self,
        jobs,
        decision="ALL"
    ):

        if decision == "ALL":

            return jobs

        return [
            job
            for job in jobs
            if job.get(
                "decision",
                ""
            ) == decision
        ]

    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------

    @staticmethod
    def _number(value):

        try:

            return float(value)

        except (
            TypeError,
            ValueError,
        ):

            return 0.0

    @staticmethod
    def _boolean(value):

        if isinstance(
            value,
            bool
        ):

            return value

        if value is None:

            return False

        text = str(
            value
        ).strip().lower()

        return text in {
            "true",
            "yes",
            "1",
            "available",
            "sponsored",
            "sponsorship",
        }


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    engine = ExecutiveDecisionCenter()

    sample_jobs = [

        {
            "title": "Head of Sales",
            "company": "Test Company",
            "country": "Singapore",
            "executive_score": 88,
            "ranking_score": 91,
            "apply_link": "https://example.com",
            "visa_sponsorship": True,
        },

        {
            "title": "Sales Manager",
            "company": "Example Company",
            "country": "India",
            "executive_score": 68,
            "ranking_score": 70,
        },

    ]

    results = engine.analyze_jobs(
        sample_jobs
    )

    for job in results:

        print(
            job["decision_position"],
            job["title"],
            job["decision"],
            job["decision_score"],
        )