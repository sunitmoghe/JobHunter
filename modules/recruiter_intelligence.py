import re


class RecruiterIntelligence:

    def __init__(self):

        self.company_database = {

            "microsoft": {
                "website": "https://www.microsoft.com",
                "careers": "https://careers.microsoft.com",
                "linkedin": "https://www.linkedin.com/company/microsoft",
                "hr_email": "askhr@microsoft.com",
                "recruiter": "Talent Acquisition Team"
            },

            "google": {
                "website": "https://about.google",
                "careers": "https://careers.google.com",
                "linkedin": "https://www.linkedin.com/company/google",
                "hr_email": "",
                "recruiter": "Google Recruiting"
            },

            "amazon": {
                "website": "https://www.amazon.jobs",
                "careers": "https://www.amazon.jobs",
                "linkedin": "https://www.linkedin.com/company/amazon",
                "hr_email": "",
                "recruiter": "Amazon Recruiting"
            },

            "oracle": {
                "website": "https://www.oracle.com",
                "careers": "https://careers.oracle.com",
                "linkedin": "https://www.linkedin.com/company/oracle",
                "hr_email": "",
                "recruiter": "Oracle Talent Acquisition"
            },

            "siemens": {
                "website": "https://www.siemens.com",
                "careers": "https://jobs.siemens.com",
                "linkedin": "https://www.linkedin.com/company/siemens",
                "hr_email": "",
                "recruiter": "Siemens Talent Acquisition"
            }

        }

    # --------------------------------------------------

    def clean_company(self, company):

        company = str(company).lower().strip()

        company = re.sub(
            r"\s+",
            " ",
            company
        )

        return company

    # --------------------------------------------------

    def find_recruiter(self, job):

        company = self.clean_company(

            job.get(
                "company",
                ""
            )

        )

        info = self.company_database.get(company)

        if info:

            return {

                "name": info["recruiter"],

                "title": "Talent Acquisition",

                "email": info["hr_email"],

                "linkedin": info["linkedin"],

                "confidence": "High"

            }

        return None

    # --------------------------------------------------

    def enrich(self, job):

        recruiter = self.find_recruiter(job)

        if recruiter:

            job["recruiter_found"] = True

            job["recruiter_name"] = recruiter["name"]

            job["recruiter_title"] = recruiter["title"]

            job["recruiter_email"] = recruiter["email"]

            job["linkedin_company"] = recruiter["linkedin"]

            job["contact_confidence"] = recruiter["confidence"]

        else:

            job["recruiter_found"] = False

            job["recruiter_name"] = ""

            job["recruiter_title"] = ""

            job["recruiter_email"] = ""

            job["linkedin_company"] = ""

            job["contact_confidence"] = "Low"

        return job

    # --------------------------------------------------

    def enrich_jobs(self, jobs):

        return [

            self.enrich(job)

            for job in jobs

        ]


if __name__ == "__main__":

    engine = RecruiterIntelligence()

    sample = {

        "company": "Microsoft",

        "role": "Head of Sales"

    }

    print(engine.enrich(sample))