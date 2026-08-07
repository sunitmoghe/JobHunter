import requests


class LeverEngine:

    COMPANIES = [

        "netflix",
        "figma",
        "atlassian",
        "robinhood",
        "asana",
        "coinbase",
        "scale-ai",
        "coursera"

    ]

    def search_jobs(
        self,
        role
    ):

        jobs = []

        for company in self.COMPANIES:

            try:

                url = f"https://api.lever.co/v0/postings/{company}"

                response = requests.get(
                    url,
                    timeout=10
                )

                response.raise_for_status()

                postings = response.json()

                for post in postings:

                    title = post.get(
                        "text",
                        ""
                    )

                    if role.lower() in title.lower():

                        jobs.append({

                            "role": title,

                            "company": company.title(),

                            "location": post.get(
                                "categories",
                                {}
                            ).get(
                                "location",
                                "Unknown"
                            ),

                            "country": "Global",

                            "source": "Lever",

                            "apply_link": post.get(
                                "hostedUrl",
                                ""
                            )

                        })

            except Exception:

                pass

        return jobs