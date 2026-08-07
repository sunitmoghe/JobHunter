class MarketIntelligenceEngine:

    def analyse(self, jobs):

        countries = {}

        for job in jobs:

            country = job.get("country", "Unknown")

            countries.setdefault(
                country,
                {
                    "jobs": 0,
                    "visa": 0,
                    "executive_score": 0,
                },
            )

            countries[country]["jobs"] += 1

            if job.get("visa_sponsorship"):
                countries[country]["visa"] += 1

            countries[country]["executive_score"] += job.get(
                "executive_score",
                0,
            )

        results = []

        for country, data in countries.items():

            avg = 0

            if data["jobs"] > 0:
                avg = round(
                    data["executive_score"] / data["jobs"],
                    1,
                )

            results.append(
                {
                    "Country": country,
                    "Jobs": data["jobs"],
                    "Visa Jobs": data["visa"],
                    "Average Executive Score": avg,
                }
            )

        results.sort(
            key=lambda x: x["Jobs"],
            reverse=True,
        )

        return results