class ExecutiveScoringEngine:

    def __init__(self):

        self.preferred_countries = [
            "Singapore",
            "Germany",
            "United Kingdom",
            "United States",
            "Australia",
            "Netherlands",
            "Poland",
            "New Zealand",
            "Norway",
            "Finland",
            "UAE",
            "Saudi Arabia"
        ]

        self.executive_keywords = [
            "chief",
            "ceo",
            "coo",
            "cro",
            "cto",
            "cfo",
            "vice president",
            "vp",
            "director",
            "head",
            "country manager"
        ]

    def calculate_score(
        self,
        job,
        ats_score=80,
        experience_years=20
    ):

        role = job.get(
            "role",
            ""
        ).lower()

        country = job.get(
            "country",
            ""
        )

        leadership_score = 60

        for keyword in self.executive_keywords:

            if keyword in role:

                leadership_score = 100
                break

        experience_score = min(
            100,
            50 + (experience_years * 2)
        )

        country_score = (
            100
            if country in self.preferred_countries
            else 70
        )

        industry_score = 85

        role_score = (
            100
            if leadership_score == 100
            else 70
        )

        executive_fit = round(

            (ats_score * 0.30)
            + (leadership_score * 0.25)
            + (experience_score * 0.20)
            + (country_score * 0.10)
            + (industry_score * 0.10)
            + (role_score * 0.05),

            2

        )

        return {

            "executive_fit": executive_fit,

            "ats_score": ats_score,

            "leadership_score": leadership_score,

            "experience_score": experience_score,

            "country_score": country_score,

            "industry_score": industry_score,

            "role_score": role_score

        }