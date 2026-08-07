class CompanyIntelligence:

    def __init__(self):

        self.company_database = {

            "microsoft": {
                "rating": 5,
                "visa_sponsorship": True,
                "remote": True,
                "fortune500": True,
                "hiring": "Growing",
                "industry": "Technology",
                "employees": "220,000+",
                "headquarters": "Redmond, USA",
                "revenue": "$245B",
                "growth_score": 96,
                "layoff_risk": "Low",
                "verified_company": True
            },

            "google": {
                "rating": 5,
                "visa_sponsorship": True,
                "remote": True,
                "fortune500": True,
                "hiring": "Growing",
                "industry": "Technology",
                "employees": "185,000+",
                "headquarters": "California, USA",
                "revenue": "$350B",
                "growth_score": 98,
                "layoff_risk": "Low",
                "verified_company": True
            },

            "amazon": {
                "rating": 5,
                "visa_sponsorship": True,
                "remote": True,
                "fortune500": True,
                "hiring": "Growing",
                "industry": "E-Commerce / Cloud",
                "employees": "1.5M+",
                "headquarters": "Seattle, USA",
                "revenue": "$630B",
                "growth_score": 95,
                "layoff_risk": "Medium",
                "verified_company": True
            },

            "oracle": {
                "rating": 5,
                "visa_sponsorship": True,
                "remote": True,
                "fortune500": True,
                "hiring": "Stable",
                "industry": "Enterprise Software",
                "employees": "160,000+",
                "headquarters": "Texas, USA",
                "revenue": "$53B",
                "growth_score": 89,
                "layoff_risk": "Low",
                "verified_company": True
            },

            "siemens": {
                "rating": 5,
                "visa_sponsorship": True,
                "remote": True,
                "fortune500": True,
                "hiring": "Growing",
                "industry": "Industrial Automation",
                "employees": "320,000+",
                "headquarters": "Munich, Germany",
                "revenue": "$82B",
                "growth_score": 92,
                "layoff_risk": "Low",
                "verified_company": True
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
                "hiring": "Unknown",
                "industry": "Unknown",
                "employees": "Unknown",
                "headquarters": "Unknown",
                "revenue": "Unknown",
                "growth_score": 50,
                "layoff_risk": "Unknown",
                "verified_company": False
            }
        )

        job["company_rating"] = info["rating"]
        job["visa_sponsorship"] = info["visa_sponsorship"]
        job["remote_friendly"] = info["remote"]
        job["fortune500"] = info["fortune500"]
        job["hiring_trend"] = info["hiring"]

        job["industry"] = info["industry"]
        job["employee_count"] = info["employees"]
        job["headquarters"] = info["headquarters"]
        job["estimated_revenue"] = info["revenue"]
        job["growth_score"] = info["growth_score"]
        job["layoff_risk"] = info["layoff_risk"]
        job["verified_company"] = info["verified_company"]

        return job

    def enrich_jobs(self, jobs):

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

    jobs = engine.enrich_jobs(sample)

    for job in jobs:
        print(job)