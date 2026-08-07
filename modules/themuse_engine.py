import requests


class TheMuseEngine:

    URL = "https://www.themuse.com/api/public/jobs"

    def search_jobs(self, role):

        jobs = []

        page = 1

        try:

            while page <= 3:

                response = requests.get(
                    self.URL,
                    params={
                        "page": page
                    },
                    timeout=15
                )

                response.raise_for_status()

                data = response.json()

                for job in data.get("results", []):

                    title = job.get("name", "")

                    if role.lower() in title.lower():

                        jobs.append({

                            "role": title,

                            "company": job.get(
                                "company",
                                {}
                            ).get(
                                "name",
                                "Unknown"
                            ),

                            "location": ", ".join(
                                [
                                    loc.get("name", "")
                                    for loc in job.get(
                                        "locations",
                                        []
                                    )
                                ]
                            ),

                            "country": "Global",

                            "source": "TheMuse",

                            "apply_link": job.get(
                                "refs",
                                {}
                            ).get(
                                "landing_page",
                                ""
                            )

                        })

                page += 1

        except Exception as e:

            print(f"TheMuse Error : {e}")

        return jobs