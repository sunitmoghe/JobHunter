import requests


class RemotiveEngine:

    URL = "https://remotive.com/api/remote-jobs"

    def search_jobs(self, role):

        jobs = []

        try:

            response = requests.get(
                self.URL,
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            for job in data.get("jobs", []):

                title = job.get("title", "")

                if role.lower() in title.lower():

                    jobs.append({

                        "role": title,

                        "company": job.get(
                            "company_name",
                            "Unknown"
                        ),

                        "location": job.get(
                            "candidate_required_location",
                            "Remote"
                        ),

                        "country": "Global",

                        "source": "Remotive",

                        "apply_link": job.get(
                            "url"
                        )

                    })

        except Exception as e:

            print(f"Remotive Error : {e}")

        return jobs