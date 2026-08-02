from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

from modules.job_validator import JobValidator
from modules.job_deduplicator import JobDeduplicator


class ParallelSearchEngine:

    def __init__(
        self,
        engine,
        max_workers=5
    ):

        self.engine = engine

        self.max_workers = max_workers

    def search_role(
        self,
        role
    ):

        try:

            jobs = self.engine.search_jobs(
                role
            )

            jobs = JobValidator.validate_jobs(
                jobs
            )

            jobs = JobDeduplicator.remove_empty(
                jobs
            )

            jobs = JobDeduplicator.deduplicate(
                jobs
            )

            for job in jobs:

                job["executive_role"] = role

            return jobs

        except Exception as e:

            print(
                f"Search Error ({role}) : {e}"
            )

            return []

    def search_roles(
        self,
        roles
    ):

        all_jobs = []

        with ThreadPoolExecutor(

            max_workers=self.max_workers

        ) as executor:

            futures = {

                executor.submit(

                    self.search_role,

                    role

                ): role

                for role in roles

            }

            for future in as_completed(

                futures

            ):

                try:

                    jobs = future.result()

                    all_jobs.extend(

                        jobs

                    )

                except Exception as e:

                    print(e)

        all_jobs = JobDeduplicator.deduplicate(

            all_jobs

        )

        return all_jobs

    def search_single_country(
        self,
        roles,
        country
    ):

        jobs = []

        for role in roles:

            try:

                result = self.engine.search_jobs(

                    role,

                    [country]

                )

                result = JobValidator.validate_jobs(

                    result

                )

                jobs.extend(

                    result

                )

            except Exception:

                pass

        jobs = JobDeduplicator.deduplicate(

            jobs

        )

        return jobs

    def search_multiple_countries(
        self,
        roles,
        countries
    ):

        all_jobs = []

        with ThreadPoolExecutor(

            max_workers=len(countries)

        ) as executor:

            futures = {

                executor.submit(

                    self.search_single_country,

                    roles,

                    country

                ): country

                for country in countries

            }

            for future in as_completed(

                futures

            ):

                try:

                    jobs = future.result()

                    all_jobs.extend(

                        jobs

                    )

                except Exception:

                    pass

        all_jobs = JobDeduplicator.deduplicate(

            all_jobs

        )

        return all_jobs