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
            "country manager",
            "general manager",
            "regional director"
        ]

    def calculate_score(
        self,
        job,
        ats_score=80,
        experience_years=20
    ):

        role = (
            job.get("role")
            or job.get("title")
            or ""
        ).lower()

        country = job.get(
            "country",
            ""
        )

        company = job.get(
            "company",
            "Unknown"
        )

        leadership_score = self.calculate_leadership_score(role)

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
            if leadership_score >= 90
            else 75
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

            "executive_score": executive_fit,

            "priority": self.priority(executive_fit),

            "recommendation": self.recommendation(
                executive_fit
            ),

            "company": company,

            "country": country,

            "ats_score": ats_score,

            "leadership_score": leadership_score,

            "experience_score": experience_score,

            "country_score": country_score,

            "industry_score": industry_score,

            "role_score": role_score

        }

    def calculate_leadership_score(
        self,
        role
    ):

        score = 60

        for keyword in self.executive_keywords:

            if keyword in role:

                score += 10

        return min(score, 100)

    def priority(
        self,
        score
    ):

        if score >= 90:
            return "★★★★★ Critical"

        elif score >= 80:
            return "★★★★ High"

        elif score >= 70:
            return "★★★ Good"

        elif score >= 60:
            return "★★ Moderate"

        return "★ Low"

    def recommendation(
        self,
        score
    ):

        if score >= 90:

            return (
                "Excellent executive opportunity. Apply immediately."
            )

        elif score >= 80:

            return (
                "Strong match. Tailor your resume before applying."
            )

        elif score >= 70:

            return (
                "Good opportunity. Improve ATS keywords."
            )

        elif score >= 60:

            return (
                "Moderate fit. Apply selectively."
            )

        return (
            "Low strategic fit."
        )