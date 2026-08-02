from concurrent.futures import ThreadPoolExecutor, as_completed

from modules.adzuna_api import AdzunaAPI
from config.countries import COUNTRIES


class UnifiedJobEngine:

    def __init__(self):

        self.adzuna = AdzunaAPI()
        self.countries = COUNTRIES

    def search_jobs(
        self,
        role,
        selected_countries=None
    ):

        if selected_countries is None:

            selected_countries = [
                "Singapore",
                "UAE",
                "Germany",
                "India",
            ]

        jobs = []

        with ThreadPoolExecutor(max_workers=4) as executor:

            futures = {}

            for country in selected_countries:

                code = self.countries.get(country)

                if code:

                    futures[
                        executor.submit(
                            self.adzuna.search_jobs,
                            role=role,
                            country=code,
                            results=10
                        )
                    ] = country

            for future in as_completed(futures):

                country = futures[future]

                try:

                    jobs.extend(future.result())

                except Exception as e:

                    print(f"Error searching {country}: {e}")

        return self.remove_duplicates(jobs)

    def remove_duplicates(
        self,
        jobs
    ):

        unique = {}

        for job in jobs:

            key = (
                job["role"].lower(),
                job["company"].lower(),
            )

            if key not in unique:

                unique[key] = job

        return list(unique.values())


if __name__ == "__main__":

    engine = UnifiedJobEngine()

    jobs = engine.search_jobs(
        "Head of Sales"
    )

    print(f"TOTAL JOBS FOUND : {len(jobs)}")

    for job in jobs[:20]:

        print(
            job["role"],
            "-",
            job["company"],
            "-",
            job["country"],
        )