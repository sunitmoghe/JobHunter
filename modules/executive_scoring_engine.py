class ExecutiveScoringEngine:

    def __init__(self):

        self.preferred_countries = {

            "Singapore",
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
            "UAE",
            "Saudi Arabia",
            "Malaysia",
            "Canada"

        }

        self.executive_keywords = [

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
            "regional",
            "head",
            "general manager",
            "country manager",
            "commercial",
            "business unit"

        ]

    # --------------------------------------------------

    def calculate_score(

        self,
        job,
        ats_score=80,
        experience_years=20

    ):

        role = str(

            job.get(
                "role",
                job.get(
                    "title",
                    ""
                )
            )

        ).lower()

        country = str(

            job.get(
                "country",
                ""
            )

        )

        company = str(

            job.get(
                "company",
                "Unknown"
            )

        )

        leadership_score = self.calculate_leadership_score(role)

        experience_score = min(

            100,

            40 + (experience_years * 2)

        )

        country_score = (

            100

            if country in self.preferred_countries

            else 70

        )

        visa_score = (

            100

            if job.get(
                "visa_sponsorship",
                False
            )

            else 60

        )

        remote_score = (

            90

            if job.get(
                "remote",
                False
            )

            else 75

        )

        source_bonus = {

            "Adzuna": 10,
            "Greenhouse": 9,
            "Lever": 8,
            "Ashby": 8,
            "TheMuse": 7,
            "Remotive": 6,
            "RemoteOK": 5

        }.get(

            job.get(
                "source",
                ""
            ),

            3

        )

        executive_fit = round(

            ats_score * 0.30 +

            leadership_score * 0.22 +

            experience_score * 0.18 +

            country_score * 0.10 +

            visa_score * 0.08 +

            remote_score * 0.05 +

            source_bonus * 0.07,

            2

        )

        executive_fit = min(

            executive_fit,

            100

        )

        job["executive_score"] = executive_fit

        job["priority_score"] = executive_fit

        job["jobhunter_score"] = executive_fit

        return {

            "executive_fit": executive_fit,

            "executive_score": executive_fit,

            "priority": self.priority(executive_fit),

            "recommendation": self.recommendation(executive_fit),

            "company": company,

            "country": country,

            "ats_score": ats_score,

            "leadership_score": leadership_score,

            "experience_score": experience_score,

            "country_score": country_score,

            "visa_score": visa_score,

            "remote_score": remote_score,

            "source_bonus": source_bonus

        }

    # --------------------------------------------------

    def calculate_leadership_score(

        self,
        role

    ):

        score = 55

        for keyword in self.executive_keywords:

            if keyword in role:

                score += 7

        return min(

            score,

            100

        )

    # --------------------------------------------------

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

    # --------------------------------------------------

    def recommendation(

        self,
        score

    ):

        if score >= 90:

            return "Excellent executive opportunity. Apply immediately."

        elif score >= 80:

            return "Strong executive match. Tailor your resume and apply."

        elif score >= 70:

            return "Good opportunity. Improve ATS alignment before applying."

        elif score >= 60:

            return "Moderate fit. Apply selectively."

        return "Low strategic fit."

# --------------------------------------------------

if __name__ == "__main__":

    engine = ExecutiveScoringEngine()

    sample_job = {

        "role": "Regional Sales Director",

        "company": "Microsoft",

        "country": "Singapore",

        "source": "Greenhouse",

        "visa_sponsorship": True,

        "remote": False

    }

    result = engine.calculate_score(

        sample_job,

        ats_score=88,

        experience_years=23

    )

    print()

    print(result)