class CompanyIntelligence:

    def __init__(self):

        self.company_database = {

            "microsoft": {
                "rating": 5,
                "visa_sponsorship": True,
                "remote": True,
                "fortune500": True,
                "hiring": "High"
            },

            "google": {
                "rating": 5,
                "visa_sponsorship": True,
                "remote": True,
                "fortune500": True,
                "hiring": "High"
            },

            "amazon": {
                "rating": 5,
                "visa_sponsorship": True,
                "remote": True,
                "fortune500": True,
                "hiring": "High"
            },

            "oracle": {
                "rating": 5,
                "visa_sponsorship": True,
                "remote": True,
                "fortune500": True,
                "hiring": "Medium"
            },

            "siemens": {
                "rating": 5,
                "visa_sponsorship": True,
                "remote": True,
                "fortune500": True,
                "hiring": "High"
            }

        }

    def enrich(self, job):

        company = str(

            job.get(
                "company",
                ""
            )

        ).lower()

        info = self.company_database.get(

            company,

            {

                "rating": 3,

                "visa_sponsorship": False,

                "remote": False,

                "fortune500": False,

                "hiring": "Unknown"

            }

        )

        job["company_rating"] = info["rating"]

        job["visa_sponsorship"] = info["visa_sponsorship"]

        job["remote_friendly"] = info["remote"]

        job["fortune500"] = info["fortune500"]

        job["hiring_trend"] = info["hiring"]

        return job

    def enrich_jobs(

        self,

        jobs

    ):

        return [

            self.enrich(job)

            for job in jobs

        ]


if __name__ == "__main__":

    engine = CompanyIntelligence()

    sample = [

        {

            "company": "Microsoft",

            "role": "Sales Director"

        },

        {

            "company": "Unknown Company",

            "role": "VP Sales"

        }

    ]

    jobs = engine.enrich_jobs(

        sample

    )

    for job in jobs:

        print(job)