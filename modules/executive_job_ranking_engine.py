"""
Executive Job Ranking Engine
Phase 2C - Final Score Calibration
"""

from datetime import datetime


class ExecutiveJobRankingEngine:

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

        self.seniority_keywords = {
            "chief executive officer": 18,
            "chief operating officer": 18,
            "chief revenue officer": 18,
            "chief commercial officer": 18,
            "chief business officer": 18,
            "chief sales officer": 18,
            "vice president": 16,
            "vp ": 16,
            "head of": 13,
            "regional director": 12,
            "sales director": 12,
            "business development director": 12,
            "commercial director": 12,
            "country director": 11,
            "country manager": 9,
            "general manager": 8,
            "senior manager": 5,
            "manager": 2,
        }

        self.role_keywords = {
            "sales": 8,
            "business development": 8,
            "commercial": 7,
            "revenue": 7,
            "sales strategy": 6,
            "enterprise sales": 7,
            "key account": 5,
            "strategic account": 5,
            "partnership": 5,
            "customer success": 3,
            "customer service": 3,
            "operations": 4,
        }

        self.profile_keywords = {
            "saas": 5,
            "ai": 4,
            "artificial intelligence": 4,
            "iot": 5,
            "iiot": 5,
            "cloud": 4,
            "erp": 3,
            "crm": 3,
            "technology": 3,
            "automation": 4,
            "telecom": 3,
            "renewable": 3,
            "solar": 3,
            "industrial automation": 4,
        }

        self.business_keywords = {
            "p&l": 6,
            "profit and loss": 6,
            "revenue growth": 6,
            "revenue": 4,
            "arr": 5,
            "growth": 4,
            "business transformation": 5,
            "transformation": 4,
            "customer acquisition": 4,
            "customer retention": 4,
            "market expansion": 4,
            "go-to-market": 5,
            "go to market": 5,
            "forecast": 3,
            "forecasting": 3,
            "profitability": 4,
            "margin": 3,
            "team management": 4,
            "leadership": 4,
        }

    @staticmethod
    def _text(job):

        parts = []

        for key in (
            "title",
            "role",
            "description",
            "summary",
            "company",
            "location",
            "country",
            "skills",
            "requirements",
            "responsibilities",
        ):

            value = job.get(key, "")

            if isinstance(value, (list, tuple, set)):
                value = " ".join(
                    str(x)
                    for x in value
                )

            parts.append(
                str(value or "")
            )

        return " ".join(parts).lower()

    @staticmethod
    def _country(job):

        return str(
            job.get(
                "country",
                ""
            ) or ""
        ).strip()

    @staticmethod
    def _bool(value):

        if isinstance(value, bool):
            return value

        return str(
            value or ""
        ).strip().lower() in {
            "true",
            "yes",
            "y",
            "1",
            "available",
            "sponsored",
            "sponsorship",
        }

    @staticmethod
    def _has_link(job):

        for key in (
            "apply_link",
            "url",
            "redirect_url",
        ):

            value = str(
                job.get(
                    key,
                    ""
                ) or ""
            ).strip()

            if value.startswith(
                (
                    "http://",
                    "https://",
                )
            ):

                return True

        return False

    @staticmethod
    def _freshness_score(job):

        value = (
            job.get("posted_date")
            or job.get("published_date")
            or job.get("date")
            or ""
        )

        if not value:
            return 0

        text = str(
            value
        ).strip()

        try:

            if len(text) >= 10:

                posted = datetime.fromisoformat(
                    text[:10]
                )

                days = max(
                    (
                        datetime.now()
                        - posted
                    ).days,
                    0,
                )

                if days <= 3:
                    return 4

                if days <= 7:
                    return 3

                if days <= 14:
                    return 2

                if days <= 30:
                    return 1

        except (
            ValueError,
            TypeError,
        ):

            pass

        return 0

    def _seniority_score(self, text):

        score = 0

        for keyword, points in (
            self.seniority_keywords.items()
        ):

            if keyword in text:

                score = max(
                    score,
                    points,
                )

        return score

    @staticmethod
    def _keyword_score(
        text,
        keywords,
        maximum,
    ):

        score = sum(
            points
            for keyword, points
            in keywords.items()
            if keyword in text
        )

        return min(
            score,
            maximum,
        )

    def calculate_ranking_score(
        self,
        job,
    ):

        text = self._text(
            job
        )

        country = self._country(
            job
        )

        try:

            executive_score = float(
                job.get(
                    "executive_score",
                    job.get(
                        "jobhunter_score",
                        0,
                    ),
                ) or 0
            )

        except (
            TypeError,
            ValueError,
        ):

            executive_score = 0

        executive_score = max(
            0,
            min(
                executive_score,
                100,
            ),
        )

        # Existing JobHunter score.
        base = (
            executive_score
            * 0.45
        )

        seniority = (
            self._seniority_score(
                text
            )
        )

        role_fit = (
            self._keyword_score(
                text,
                self.role_keywords,
                18,
            )
        )

        profile_fit = (
            self._keyword_score(
                text,
                self.profile_keywords,
                10,
            )
        )

        business_fit = (
            self._keyword_score(
                text,
                self.business_keywords,
                12,
            )
        )

        country_fit = (
            6
            if country
            in self.preferred_countries
            else 2
        )

        visa_fit = (
            5
            if self._bool(
                job.get(
                    "visa_sponsorship",
                    False,
                )
            )
            else 0
        )

        application_fit = (
            4
            if self._has_link(
                job
            )
            else 0
        )

        remote_fit = (
            1
            if self._bool(
                job.get(
                    "remote_friendly",
                    job.get(
                        "remote",
                        False,
                    ),
                )
            )
            else 0
        )

        freshness = (
            self._freshness_score(
                job
            )
        )

        raw_score = (
            base
            + seniority
            + role_fit
            + profile_fit
            + business_fit
            + country_fit
            + visa_fit
            + application_fit
            + remote_fit
            + freshness
        )

        # Keep the ranking realistic.
        score = min(
            round(
                raw_score,
                2,
            ),
            95,
        )

        return {
            "ranking_score": score,
            "executive_score": round(
                executive_score,
                2,
            ),
            "seniority_score": seniority,
            "role_fit_score": role_fit,
            "profile_fit_score": profile_fit,
            "business_fit_score": business_fit,
            "country_fit_score": country_fit,
            "visa_fit_score": visa_fit,
            "application_fit_score": application_fit,
            "remote_fit_score": remote_fit,
            "freshness_score": freshness,
        }

    @staticmethod
    def get_priority(score):

        if score >= 90:
            return "Critical"

        if score >= 80:
            return "High"

        if score >= 70:
            return "Medium"

        if score >= 60:
            return "Low"

        return "Very Low"

    @staticmethod
    def get_recommendation(score):

        if score >= 90:

            return (
                "Exceptional executive opportunity. "
                "Apply immediately."
            )

        if score >= 80:

            return (
                "Strong executive opportunity. "
                "Prioritize application."
            )

        if score >= 70:

            return (
                "Good opportunity. "
                "Tailor CV before applying."
            )

        if score >= 60:

            return (
                "Moderate fit. "
                "Apply selectively."
            )

        return "Low strategic fit."

    def rank_job(
        self,
        job,
    ):

        item = dict(
            job
        )

        details = (
            self.calculate_ranking_score(
                item
            )
        )

        item.update(
            details
        )

        item["ranking_priority"] = (
            self.get_priority(
                details[
                    "ranking_score"
                ]
            )
        )

        item["ranking_recommendation"] = (
            self.get_recommendation(
                details[
                    "ranking_score"
                ]
            )
        )

        return item

    def rank_jobs(
        self,
        jobs,
    ):

        ranked = [
            self.rank_job(job)
            for job in (
                jobs or []
            )
        ]

        ranked.sort(
            key=lambda job: (
                float(
                    job.get(
                        "ranking_score",
                        0,
                    )
                ),
                float(
                    job.get(
                        "executive_score",
                        0,
                    )
                ),
            ),
            reverse=True,
        )

        for position, job in enumerate(
            ranked,
            start=1,
        ):

            job[
                "ranking_position"
            ] = position

        return ranked


if __name__ == "__main__":

    engine = (
        ExecutiveJobRankingEngine()
    )

    sample_jobs = [

        {
            "title": "Head of Sales",
            "company": "Singapore SaaS",
            "country": "Singapore",
            "executive_score": 92,
            "visa_sponsorship": True,
            "apply_link": (
                "https://example.com/apply"
            ),
            "description": (
                "Lead enterprise sales, "
                "revenue growth, P&L, "
                "SaaS, IoT, AI and "
                "strategic partnerships."
            ),
        },

        {
            "title": "Sales Manager",
            "company": "Example Company",
            "country": "India",
            "executive_score": 70,
            "description": (
                "Manage sales team "
                "and customer acquisition."
            ),
        },

    ]

    ranked = (
        engine.rank_jobs(
            sample_jobs
        )
    )

    for job in ranked:

        print(
            job[
                "ranking_position"
            ],
            job["title"],
            job["ranking_score"],
            job["ranking_priority"],
        )