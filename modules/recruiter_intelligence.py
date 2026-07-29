import re


class RecruiterIntelligence:

    """
    Recruiter & Company Contact Intelligence

    Enriches executive jobs with:

    • Company Website
    • Careers Page
    • HR Email
    • Recruiter Email (if known)
    • LinkedIn Company Page
    • Contact Confidence
    """

    def __init__(self):

        self.company_database = {

            "Microsoft": {
                "website": "https://www.microsoft.com",
                "careers": "https://careers.microsoft.com",
                "linkedin": "https://www.linkedin.com/company/microsoft",
                "hr_email": "askhr@microsoft.com"
            },

            "Google": {
                "website": "https://about.google",
                "careers": "https://careers.google.com",
                "linkedin": "https://www.linkedin.com/company/google",
                "hr_email": ""
            },

            "Amazon": {
                "website": "https://www.amazon.jobs",
                "careers": "https://www.amazon.jobs",
                "linkedin": "https://www.linkedin.com/company/amazon",
                "hr_email": ""
            },

            "Siemens": {
                "website": "https://www.siemens.com",
                "careers": "https://jobs.siemens.com",
                "linkedin": "https://www.linkedin.com/company/siemens",
                "hr_email": ""
            },

            "ABB": {
                "website": "https://global.abb",
                "careers": "https://careers.abb",
                "linkedin": "https://www.linkedin.com/company/abb",
                "hr_email": ""
            },

            "Schneider Electric": {
                "website": "https://www.se.com",
                "careers": "https://careers.se.com",
                "linkedin": "https://www.linkedin.com/company/schneider-electric",
                "hr_email": ""
            },

            "Honeywell": {
                "website": "https://www.honeywell.com",
                "careers": "https://careers.honeywell.com",
                "linkedin": "https://www.linkedin.com/company/honeywell",
                "hr_email": ""
            },

            "Cisco": {
                "website": "https://www.cisco.com",
                "careers": "https://jobs.cisco.com",
                "linkedin": "https://www.linkedin.com/company/cisco",
                "hr_email": ""
            },

            "Oracle": {
                "website": "https://www.oracle.com",
                "careers": "https://careers.oracle.com",
                "linkedin": "https://www.linkedin.com/company/oracle",
                "hr_email": ""
            },

            "SAP": {
                "website": "https://www.sap.com",
                "careers": "https://jobs.sap.com",
                "linkedin": "https://www.linkedin.com/company/sap",
                "hr_email": ""
            }

        }

    def _clean_company(self, company):

        company = company.strip()

        company = re.sub(r"\s+", " ", company)

        return company

    def enrich_jobs(self, jobs):

        enriched = []

        for job in jobs:

            company = self._clean_company(
                job.get("company", "")
            )

            info = self.company_database.get(company)

            if info:

                job["company_website"] = info["website"]

                job["careers_page"] = info["careers"]

                job["linkedin_company"] = info["linkedin"]

                job["hr_email"] = info["hr_email"]

                job["recruiter_name"] = ""

                job["recruiter_title"] = "Talent Acquisition"

                job["recruiter_email"] = ""

                job["contact_confidence"] = "High"

            else:

                job["company_website"] = ""

                job["careers_page"] = ""

                job["linkedin_company"] = ""

                job["hr_email"] = ""

                job["recruiter_name"] = ""

                job["recruiter_title"] = ""

                job["recruiter_email"] = ""

                job["contact_confidence"] = "Low"

            enriched.append(job)

        return enriched