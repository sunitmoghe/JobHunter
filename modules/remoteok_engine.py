import requests


class RemoteOKEngine:

    URL = "https://remoteok.com/api"

    def search_jobs(self, role):

        jobs = []

        headers = {
            "User-Agent": "JobHunterAI"
        }

        try:

            response = requests.get(
                self.URL,
                headers=headers,
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            # First record is metadata
            for job in data[1:]:

                title = job.get("position", "")

                if role.lower() in title.lower():

                    jobs.append({

                        "role": title,

                        "company": job.get(
                            "company",
                            "Unknown"
                        ),

                        "location": "Remote",

                        "country": "Global",

                        "source": "RemoteOK",

                        "apply_link": job.get(
                            "url",
                            ""
                        )

                    })

        except Exception as e:

            print(f"RemoteOK Error : {e}")

        return jobs