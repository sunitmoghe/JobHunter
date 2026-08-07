import requests


class AshbyEngine:

    COMPANIES = [

        "openai",
        "notion",
        "vercel",
        "planet",
        "linear",
        "pilot",
        "checkr"

    ]

    def search_jobs(
        self,
        role
    ):

        jobs = []

        for company in self.COMPANIES:

            try:

                url = f"https://jobs.ashbyhq.com/{company}"

                response = requests.get(
                    url,
                    timeout=10
                )

                if response.status_code != 200:
                    continue

                html = response.text

                if role.lower() in html.lower():

                    jobs.append({

                        "role": role,

                        "company": company.title(),

                        "location": "Global",

                        "country": "Global",

                        "source": "Ashby",

                        "apply_link": url

                    })

            except Exception:

                pass

        return jobs