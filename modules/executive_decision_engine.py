"""
Executive Decision Engine
Phase 2D - Executive Job Intelligence & Decision Engine

Purpose:
Convert a ranked JobHunter opportunity into an actionable decision.

Possible decisions:
    APPLY NOW
    PRIORITIZE
    APPLY
    CONSIDER
    LOW PRIORITY
    SKIP
"""


class ExecutiveDecisionEngine:

    def __init__(self):

        self.preferred_countries = {
            "Singapore",
            "UAE",
            "Germany",
            "United Kingdom",
            "United States",
            "Australia",
            "Netherlands",
            "India",
            "Poland",
            "New Zealand",
            "Norway",
            "Finland",
            "Malaysia",
            "Canada",
        }

        self.executive_titles = [
            "chief",
            "ceo",
            "coo",
            "cro",
            "cto",
            "cfo",
            "president",
            "vice president",
            "vp",
            "head of",
            "director",
            "regional director",
            "country director",
            "country manager",
            "general manager",
        ]

        self.target_role_keywords = [
            "sales",
            "business development",
            "commercial",
            "revenue",
            "customer success",
            "customer service",
            "operations",
            "key account",
            "strategic account",
            "partnership",
        ]

        self.profile_keywords = [
            "saas",
            "ai",
            "artificial intelligence",
            "iot",
            "iiot",
            "cloud",
            "erp",
            "crm",
            "technology",
            "automation",
            "telecom",
            "solar",
            "renewable",
            "industrial",
        ]

        self.business_keywords = [
            "p&l",
            "profit and loss",
            "revenue growth",
            "revenue",
            "arr",
            "growth",
            "profitability",
            "margin",
            "business transformation",
            "transformation",
            "go-to-market",
            "go to market",
            "market expansion",
            "customer acquisition",
            "customer retention",
            "forecasting",
            "leadership",
            "team management",
        ]

    # --------------------------------------------------
    # TEXT HELPERS
    # --------------------------------------------------

    @staticmethod
    def clean_text(value):

        if value is None:
            return ""

        if isinstance(
            value,
            (list, tuple, set),
        ):

            return " ".join(
                str(item)
                for item in value
            ).strip()

        return str(value).strip()

    def job_text(self, job):

        fields = [
            "title",
            "role",
            "description",
            "summary",
            "requirements",
            "responsibilities",
            "skills",
            "company",
            "location",
            "country",
        ]

        return " ".join(
            self.clean_text(
                job.get(
                    field,
                    "",
                )
            )
            for field in fields
        ).lower()

    # --------------------------------------------------
    # BASIC CHECKS
    # --------------------------------------------------

    @staticmethod
    def get_score(
        job,
        *keys,
        default=0,
    ):

        for key in keys:

            try:

                value = float(
                    job.get(
                        key,
                        default,
                    )
                )

                return value

            except (
                TypeError,
                ValueError,
            ):

                continue

        return default

    @staticmethod
    def is_true(value):

        if isinstance(
            value,
            bool,
        ):

            return value

        return str(
            value or ""
        ).strip().lower() in {
            "true",
            "yes",
            "available",
            "sponsored",
            "sponsorship",
            "1",
        }

    @staticmethod
    def has_application_link(job):

        for key in (
            "apply_link",
            "url",
            "redirect_url",
        ):

            value = str(
                job.get(
                    key,
                    "",
                )
                or ""
            ).strip()

            if value.startswith(
                (
                    "http://",
                    "https://",
                )
            ):

                return True

        return False

    # --------------------------------------------------
    # SENIORITY
    # --------------------------------------------------

    def calculate_seniority_fit(
        self,
        job,
    ):

        text = self.job_text(
            job
        )

        for keyword in (
            self.executive_titles
        ):

            if keyword in text:

                return 100

        return 60

    # --------------------------------------------------
    # ROLE FIT
    # --------------------------------------------------

    def calculate_role_fit(
        self,
        job,
    ):

        text = self.job_text(
            job
        )

        matches = sum(
            1
            for keyword in (
                self.target_role_keywords
            )
            if keyword in text
        )

        if matches >= 4:

            return 100

        if matches >= 3:

            return 90

        if matches >= 2:

            return 80

        if matches >= 1:

            return 70

        return 50

    # --------------------------------------------------
    # PROFILE FIT
    # --------------------------------------------------

    def calculate_profile_fit(
        self,
        job,
    ):

        text = self.job_text(
            job
        )

        matches = sum(
            1
            for keyword in (
                self.profile_keywords
            )
            if keyword in text
        )

        if matches >= 5:

            return 100

        if matches >= 4:

            return 90

        if matches >= 3:

            return 80

        if matches >= 2:

            return 70

        if matches >= 1:

            return 60

        return 45

    # --------------------------------------------------
    # BUSINESS FIT
    # --------------------------------------------------

    def calculate_business_fit(
        self,
        job,
    ):

        text = self.job_text(
            job
        )

        matches = sum(
            1
            for keyword in (
                self.business_keywords
            )
            if keyword in text
        )

        if matches >= 7:

            return 100

        if matches >= 5:

            return 90

        if matches >= 3:

            return 80

        if matches >= 2:

            return 70

        if matches >= 1:

            return 60

        return 45

    # --------------------------------------------------
    # MARKET FIT
    # --------------------------------------------------

    def calculate_market_fit(
        self,
        job,
    ):

        country = self.clean_text(
            job.get(
                "country",
                "",
            )
        )

        if country in self.preferred_countries:

            return 100

        if not country:

            return 60

        return 70

    # --------------------------------------------------
    # VISA FIT
    # --------------------------------------------------

    def calculate_visa_fit(
        self,
        job,
    ):

        country = self.clean_text(
            job.get(
                "country",
                "",
            )
        )

        visa = self.is_true(
            job.get(
                "visa_sponsorship",
                False,
            )
        )

        if visa:

            return 100

        if country in {
            "India",
        }:

            return 90

        if country in self.preferred_countries:

            return 55

        return 50

    # --------------------------------------------------
    # APPLICATION ACCESS
    # --------------------------------------------------

    def calculate_application_access(
        self,
        job,
    ):

        if self.has_application_link(
            job
        ):

            return 100

        return 40

    # --------------------------------------------------
    # CAREER VALUE
    # --------------------------------------------------

    def calculate_career_value(
        self,
        job,
    ):

        text = self.job_text(
            job
        )

        score = 50

        executive_match = any(
            keyword in text
            for keyword in (
                self.executive_titles
            )
        )

        if executive_match:

            score += 20

        if any(
            keyword in text
            for keyword in [
                "regional",
                "global",
                "international",
                "asia",
                "apac",
                "emea",
                "middle east",
                "europe",
            ]
        ):

            score += 15

        if any(
            keyword in text
            for keyword in [
                "revenue",
                "p&l",
                "profitability",
                "transformation",
                "market expansion",
            ]
        ):

            score += 15

        return min(
            score,
            100,
        )

    # --------------------------------------------------
    # RISK ANALYSIS
    # --------------------------------------------------

    def calculate_risk(
        self,
        job,
    ):

        risks = []

        country = self.clean_text(
            job.get(
                "country",
                "",
            )
        )

        if (
            country
            and country not in self.preferred_countries
        ):

            risks.append(
                "Country is outside preferred markets."
            )

        if (
            country
            and country in self.preferred_countries
            and not self.is_true(
                job.get(
                    "visa_sponsorship",
                    False,
                )
            )
            and country != "India"
        ):

            risks.append(
                "Visa sponsorship is not confirmed."
            )

        if not self.has_application_link(
            job
        ):

            risks.append(
                "Application link is unavailable."
            )

        score = self.get_score(
            job,
            "ranking_score",
            "executive_score",
            default=0,
        )

        if score < 70:

            risks.append(
                "Overall opportunity score is below the preferred threshold."
            )

        if not risks:

            risks.append(
                "No major decision risk detected."
            )

        return risks

    # --------------------------------------------------
    # DECISION SCORE
    # --------------------------------------------------

    def calculate_decision_score(
        self,
        job,
    ):

        ranking_score = self.get_score(
            job,
            "ranking_score",
            "executive_score",
            default=0,
        )

        seniority = (
            self.calculate_seniority_fit(
                job
            )
        )

        role_fit = (
            self.calculate_role_fit(
                job
            )
        )

        profile_fit = (
            self.calculate_profile_fit(
                job
            )
        )

        business_fit = (
            self.calculate_business_fit(
                job
            )
        )

        market_fit = (
            self.calculate_market_fit(
                job
            )
        )

        visa_fit = (
            self.calculate_visa_fit(
                job
            )
        )

        application_access = (
            self.calculate_application_access(
                job
            )
        )

        career_value = (
            self.calculate_career_value(
                job
            )
        )

        decision_score = (

            ranking_score * 0.35

            + seniority * 0.10

            + role_fit * 0.10

            + profile_fit * 0.10

            + business_fit * 0.10

            + market_fit * 0.08

            + visa_fit * 0.07

            + application_access * 0.05

            + career_value * 0.05

        )

        return round(
            min(
                decision_score,
                100,
            ),
            2,
        )

    # --------------------------------------------------
    # DECISION
    # --------------------------------------------------

    @staticmethod
    def get_decision(
        score,
    ):

        if score >= 90:

            return "APPLY NOW"

        if score >= 82:

            return "PRIORITIZE"

        if score >= 74:

            return "APPLY"

        if score >= 65:

            return "CONSIDER"

        if score >= 55:

            return "LOW PRIORITY"

        return "SKIP"

    # --------------------------------------------------
    # RECOMMENDATION
    # --------------------------------------------------

    @staticmethod
    def get_recommendation(
        decision,
    ):

        recommendations = {

            "APPLY NOW":
                "Exceptional strategic fit. Apply immediately.",

            "PRIORITIZE":
                "Strong opportunity. Move this application ahead of lower-ranked jobs.",

            "APPLY":
                "Good opportunity. Tailor the executive CV before applying.",

            "CONSIDER":
                "Potentially useful opportunity. Review the job description carefully.",

            "LOW PRIORITY":
                "Limited strategic fit. Apply only if the opportunity has additional value.",

            "SKIP":
                "Low strategic value compared with stronger opportunities.",

        }

        return recommendations.get(
            decision,
            "Review opportunity manually.",
        )

    # --------------------------------------------------
    # REASONS
    # --------------------------------------------------

    def generate_reasons(
        self,
        job,
        decision,
    ):

        reasons = []

        ranking_score = self.get_score(
            job,
            "ranking_score",
            "executive_score",
            default=0,
        )

        country = self.clean_text(
            job.get(
                "country",
                "",
            )
        )

        if ranking_score >= 85:

            reasons.append(
                "Strong overall executive ranking."
            )

        elif ranking_score >= 75:

            reasons.append(
                "Good overall executive ranking."
            )

        elif ranking_score >= 65:

            reasons.append(
                "Moderate executive ranking."
            )

        seniority = (
            self.calculate_seniority_fit(
                job
            )
        )

        if seniority >= 90:

            reasons.append(
                "Role has strong executive seniority alignment."
            )

        role_fit = (
            self.calculate_role_fit(
                job
            )
        )

        if role_fit >= 80:

            reasons.append(
                "Strong sales/business leadership alignment."
            )

        profile_fit = (
            self.calculate_profile_fit(
                job
            )
        )

        if profile_fit >= 80:

            reasons.append(
                "Good alignment with technology and executive profile."
            )

        business_fit = (
            self.calculate_business_fit(
                job
            )
        )

        if business_fit >= 80:

            reasons.append(
                "Strong revenue, P&L, growth or transformation alignment."
            )

        if country in self.preferred_countries:

            reasons.append(
                f"{country} is a preferred JobHunter market."
            )

        if self.is_true(
            job.get(
                "visa_sponsorship",
                False,
            )
        ):

            reasons.append(
                "Visa sponsorship is indicated."
            )

        if self.has_application_link(
            job
        ):

            reasons.append(
                "Direct application route is available."
            )

        if not reasons:

            reasons.append(
                "Limited positive signals detected."
            )

        return reasons[:6]

    # --------------------------------------------------
    # COMPLETE ANALYSIS
    # --------------------------------------------------

    def analyze_job(
        self,
        job,
    ):

        item = dict(
            job
        )

        decision_score = (
            self.calculate_decision_score(
                item
            )
        )

        decision = (
            self.get_decision(
                decision_score
            )
        )

        item[
            "decision_score"
        ] = decision_score

        item[
            "decision"
        ] = decision

        item[
            "decision_recommendation"
        ] = (
            self.get_recommendation(
                decision
            )
        )

        item[
            "decision_reasons"
        ] = (
            self.generate_reasons(
                item,
                decision,
            )
        )

        item[
            "decision_risks"
        ] = (
            self.calculate_risk(
                item
            )
        )

        item[
            "seniority_fit"
        ] = (
            self.calculate_seniority_fit(
                item
            )
        )

        item[
            "role_fit"
        ] = (
            self.calculate_role_fit(
                item
            )
        )

        item[
            "profile_fit"
        ] = (
            self.calculate_profile_fit(
                item
            )
        )

        item[
            "business_fit"
        ] = (
            self.calculate_business_fit(
                item
            )
        )

        item[
            "market_fit"
        ] = (
            self.calculate_market_fit(
                item
            )
        )

        item[
            "visa_fit"
        ] = (
            self.calculate_visa_fit(
                item
            )
        )

        item[
            "career_value"
        ] = (
            self.calculate_career_value(
                item
            )
        )

        return item

    # --------------------------------------------------
    # MULTIPLE JOBS
    # --------------------------------------------------

    def analyze_jobs(
        self,
        jobs,
    ):

        analyzed = [
            self.analyze_job(
                job
            )
            for job in (
                jobs or []
            )
        ]

        analyzed.sort(
            key=lambda job: (
                float(
                    job.get(
                        "decision_score",
                        0,
                    )
                ),
                float(
                    job.get(
                        "ranking_score",
                        0,
                    )
                ),
            ),
            reverse=True,
        )

        for position, job in enumerate(
            analyzed,
            start=1,
        ):

            job[
                "decision_position"
            ] = position

        return analyzed


# ------------------------------------------------------
# DIRECT TEST
# ------------------------------------------------------

if __name__ == "__main__":

    from modules.executive_ai_agent import (
        ExecutiveAIAgent,
    )

    agent = ExecutiveAIAgent()

    jobs = agent.search_jobs(
        role="Head of Sales"
    )

    engine = (
        ExecutiveDecisionEngine()
    )

    analyzed = (
        engine.analyze_jobs(
            jobs
        )
    )

    print(
        "ANALYZED JOBS:",
        len(analyzed)
    )

    print(
        "TOP 10 DECISIONS:"
    )

    for job in analyzed[:10]:

        print(
            job.get(
                "decision_position"
            ),
            "|",
            job.get(
                "title",
                job.get(
                    "role",
                    ""
                )
            ),
            "|",
            job.get(
                "company",
                ""
            ),
            "|",
            job.get(
                "country",
                ""
            ),
            "| Rank:",
            job.get(
                "ranking_score",
                0
            ),
            "| Decision:",
            job.get(
                "decision",
                ""
            ),
            "| Decision Score:",
            job.get(
                "decision_score",
                0
            ),
        )

        print(
            "   Reasons:",
            "; ".join(
                job.get(
                    "decision_reasons",
                    [],
                )
            )
        )

        print(
            "   Risks:",
            "; ".join(
                job.get(
                    "decision_risks",
                    [],
                )
            )
        )