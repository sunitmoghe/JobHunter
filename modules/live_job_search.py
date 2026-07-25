import requests


class LiveJobSearch:

    def __init__(self):
        self.jobs = []

    def search(self, role, country):

        # Sample live-search framework (replace with API later)
        self.jobs = [
            {
                "role": "Head of Sales",
                "company": "Google",
                "country": "Singapore",
                "location": "Singapore",
                "salary": "Negotiable",
                "link": "https://careers.google.com"
            },
            {
                "role": "Country Manager",
                "company": "Microsoft",
                "country": "Germany",
                "location": "Berlin",
                "salary": "Negotiable",
                "link": "https://careers.microsoft.com"
            },
            {
                "role": "Director Sales",
                "company": "SAP",
                "country": "Poland",
                "location": "Warsaw",
                "salary": "Negotiable",
                "link": "https://jobs.sap.com"
            }
        ]

        results = []

        for job in self.jobs:

            if role.lower() in job["role"].lower():

                if country.lower() in job["country"].lower():

                    results.append(job)

        return results


if __name__ == "__main__":

    engine = LiveJobSearch()

    jobs = engine.search(
        "Head",
        "Singapore"
    )

    print(jobs)