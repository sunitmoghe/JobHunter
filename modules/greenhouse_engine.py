import requests


class GreenhouseEngine:

    def search_jobs(self, company):

        url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"

        try:

            response = requests.get(
                url,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            jobs = []

            for job in data.get("jobs", []):

                jobs.append({

                    "role": job.get("title"),

                    "company": company.title(),

                    "location": job.get(
                        "location",
                        {}
                    ).get(
                        "name",
                        "Unknown"
                    ),

                    "source": "Greenhouse",

                    "country": job.get(
                        "location",
                        {}
                    ).get(
                        "name",
                        "Unknown"
                    ),

                    "apply_link": job.get(
                        "absolute_url"
                    )

                })

            return jobs

        except Exception:

            return []