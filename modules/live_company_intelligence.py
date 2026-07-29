import requests


class LiveCompanyIntelligence:

    def __init__(self):
        pass

    def enrich(self, job):

        company = job.get("company", "").strip()

        if not company:
            return job

        website = self.find_company_website(company)

        job["company_website"] = website

        if website:

            website = website.rstrip("/")

            job["careers_page"] = website + "/careers"

            job["contact_page"] = website + "/contact"

            job["linkedin_company"] = (
                "https://www.linkedin.com/search/results/companies/?keywords="
                + company.replace(" ", "%20")
            )

        else:

            job["careers_page"] = ""

            job["contact_page"] = ""

            job["linkedin_company"] = ""

        return job

    def find_company_website(self, company):

        try:

            url = (
                "https://autocomplete.clearbit.com/v1/companies/suggest?query="
                + company
            )

            response = requests.get(
                url,
                timeout=8
            )

            if response.status_code == 200:

                data = response.json()

                if data:

                    domain = data[0].get("domain", "")

                    if domain:

                        return "https://" + domain

        except Exception:

            pass

        return ""