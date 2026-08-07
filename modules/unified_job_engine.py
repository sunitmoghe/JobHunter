from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time

from modules.adzuna_api import AdzunaAPI
from modules.greenhouse_engine import GreenhouseEngine
from modules.remotive_engine import RemotiveEngine
from modules.remoteok_engine import RemoteOKEngine
from modules.themuse_engine import TheMuseEngine
from modules.lever_engine import LeverEngine
from modules.ashby_engine import AshbyEngine

from config.countries import COUNTRIES
from config.job_sources import GREENHOUSE_COMPANIES
from config.job_sources import SOURCE_PRIORITY


class UnifiedJobEngine:

    def __init__(self):

        self.countries = COUNTRIES

        self.adzuna = AdzunaAPI()
        self.greenhouse = GreenhouseEngine()
        self.remotive = RemotiveEngine()
        self.remoteok = RemoteOKEngine()
        self.themuse = TheMuseEngine()
        self.lever = LeverEngine()
        self.ashby = AshbyEngine()

        self.greenhouse_companies = GREENHOUSE_COMPANIES            

        self.lock = threading.Lock()

        self.max_workers = 8
        self.retry_count = 2
        self.retry_delay = 2

        self.source_priority = SOURCE_PRIORITY


    # --------------------------------------------------
    # SEARCH JOBS
    # --------------------------------------------------

    def search_jobs(
        self,
        role,
        selected_countries=None
    ):

        print(f"\nSearching role : {role}")

        if selected_countries is None:

            selected_countries = [
                "Singapore",
                "UAE",
                "Germany",
                "India"
            ]

        jobs = []

        # ------------------------------------------
        # ADZUNA
        # ------------------------------------------

        def search_country(country):

            code = self.countries.get(country)

            if not code:
                return []

            for _ in range(self.retry_count):

                try:

                    result = self.adzuna.search_jobs(
                        role=role,
                        country=code,
                        results=10
                    )

                    for job in result:
                        job.setdefault("source", "Adzuna")

                    return result

                except Exception:

                    time.sleep(self.retry_delay)

            return []

        with ThreadPoolExecutor(
            max_workers=min(
                len(selected_countries),
                self.max_workers
    )
) as executor:

            futures = {

                executor.submit(
                    search_country,
                    country
                ): country

                for country in selected_countries

            }

            for future in as_completed(futures):

                country = futures[future]

                try:

                    result = future.result()

                    jobs.extend(result)

                    print(
                        f"✓ {country}: {len(result)} jobs"
                    )

                except Exception as e:

                    print(
                        f"{country} failed : {e}"
                    )

        print(f"Adzuna Total : {len(jobs)}")

        # ------------------------------------------
        # GREENHOUSE
        # ------------------------------------------

        def greenhouse():

            results = []

            for company in self.greenhouse_companies:

                try:

                    postings = self.greenhouse.search_jobs(company)

                    for job in postings:

                        if role.lower() in job.get(
                            "role",
                            ""
                        ).lower():

                            job.setdefault(
                                "source",
                                "Greenhouse"
                            )

                            results.append(job)

                except Exception:

                    pass

            return results

        # ------------------------------------------
        # PARALLEL SOURCES
        # ------------------------------------------

        tasks = {

            "Greenhouse": greenhouse,

            "Remotive": lambda: self.remotive.search_jobs(role),

            "RemoteOK": lambda: self.remoteok.search_jobs(role),

            "TheMuse": lambda: self.themuse.search_jobs(role),

            "Lever": lambda: self.lever.search_jobs(role),

            "Ashby": lambda: self.ashby.search_jobs(role)

        }

        with ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:

            futures = {

                executor.submit(func): name

                for name, func in tasks.items()

            }

            for future in as_completed(futures):

                source = futures[future]

                try:

                    result = future.result()

                    if result:

                        for job in result:

                            job.setdefault(
                                "source",
                                source
                            )

                        jobs.extend(result)

                    print(
                        f"After {source}: {len(jobs)}"
                    )

                except Exception as e:

                    print(
                        f"{source} Error : {e}"
                    )

        jobs = self.remove_duplicates(jobs)

        # ------------------------------------------
        # RANK RESULTS
        # ------------------------------------------

        for job in jobs:

            priority = self.source_priority.get(
                job.get(
                    "source",
                    ""
                ),
                50
            )

            bonus = 0

            if role.lower() in job.get(
                "role",
                ""
            ).lower():

                bonus += 20

            if job.get(
                "visa_sponsorship",
                False
            ):

                bonus += 10

            job["search_rank"] = priority + bonus

        jobs.sort(
            key=lambda x: x.get(
                "search_rank",
                0
            ),
            reverse=True
        )

        print(
            f"Unique Jobs : {len(jobs)}"
        )

        return jobs

        # --------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------

    def remove_duplicates(
        self,
        jobs
    ):

        unique = {}

        for job in jobs:

            role = str(
                job.get(
                    "role",
                    job.get(
                        "title",
                        ""
                    )
                )
            ).strip().lower()

            company = str(
                job.get(
                    "company",
                    ""
                )
            ).strip().lower()

            location = str(
                job.get(
                    "location",
                    ""
                )
            ).strip().lower()

            apply_link = str(
                job.get(
                    "apply_link",
                    job.get(
                        "link",
                        ""
                    )
                )
            ).strip().lower()

            key = (
                role,
                company,
                location
            )

            if key not in unique:

                unique[key] = job

            else:

                existing = unique[key]

                current_priority = self.source_priority.get(
                    job.get(
                        "source",
                        ""
                    ),
                    0
                )

                existing_priority = self.source_priority.get(
                    existing.get(
                        "source",
                        ""
                    ),
                    0
                )

                if current_priority > existing_priority:

                    unique[key] = job

        return list(unique.values())


if __name__ == "__main__":

    engine = UnifiedJobEngine()

    jobs = engine.search_jobs(
        role="Head of Sales"
    )

    print(f"\nTOTAL JOBS : {len(jobs)}")

    for job in jobs[:10]:

        print(
            f"{job.get('role')} | "
            f"{job.get('company')} | "
            f"{job.get('source')}"
        )