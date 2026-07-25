from modules.adzuna_api import AdzunaAPI


class UnifiedJobEngine:

    def __init__(self):

        self.adzuna = AdzunaAPI()

        self.countries = {
            "India": "in",
            "Singapore": "sg",
            "United Kingdom": "gb",
            "Germany": "de",
            "United States": "us",
            "Australia": "au",
            "Poland": "pl",
            "Netherlands": "nl",
            "New Zealand": "nz"
        }

    def search_jobs(
        self,
        role,
        selected_countries=None
    ):

        jobs = []

        if selected_countries is None:

            selected_countries = list(
                self.countries.keys()
            )

        for country in selected_countries:

            code = self.countries.get(country)

            if not code:
                continue

            try:

                result = self.adzuna.search_jobs(
                    role=role,
                    country=code,
                    results=10
                )

                jobs.extend(result)

            except Exception as e:

                print(
                    f"Error searching {country}: {e}"
                )

        jobs = self.remove_duplicates(jobs)

        return jobs

    def remove_duplicates(
        self,
        jobs
    ):

        unique = {}

        for job in jobs:

            key = (
                job["role"].lower(),
                job["company"].lower()
            )

            if key not in unique:

                unique[key] = job

        return list(
            unique.values()
        )


if __name__ == "__main__":

    engine = UnifiedJobEngine()

    jobs = engine.search_jobs(
        "Head of Sales"
    )

    print()

    print(
        f"TOTAL JOBS FOUND : {len(jobs)}"
    )

    print()

    for job in jobs[:20]:

        print(
            job["role"],
            "-",
            job["company"],
            "-",
            job["country"]
        )