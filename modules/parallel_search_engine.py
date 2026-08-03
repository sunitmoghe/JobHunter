from concurrent.futures import ThreadPoolExecutor, as_completed

from modules.job_validator import JobValidator
from modules.job_deduplicator import JobDeduplicator
from modules.search_scheduler import SearchScheduler


class ParallelSearchEngine:

    def __init__(self, engine, max_workers=2):

        self.engine = engine
        self.max_workers = max_workers
        self.scheduler = SearchScheduler()

    def search_role(
        self,
        role,
        selected_countries=None
    ):

        try:

            jobs = self.engine.search_jobs(
                role,
                selected_countries
            )

            jobs = JobValidator.validate_jobs(jobs)
            jobs = JobDeduplicator.remove_empty(jobs)
            jobs = JobDeduplicator.deduplicate(jobs)

            for job in jobs:
                job["executive_role"] = role

            return jobs

        except Exception as e:

            print(f"Search Error ({role}) : {e}")

            return []

    def search_roles(
        self,
        roles,
        selected_countries=None
    ):

        all_jobs = []

        with ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:

            futures = {

                executor.submit(
                    self.search_role,
                    role,
                    selected_countries
                ): role

                for role in roles

            }

            for future in as_completed(futures):

                try:

                    jobs = future.result()

                    all_jobs.extend(jobs)

                except Exception as e:

                    print(e)

        all_jobs = JobDeduplicator.deduplicate(all_jobs)

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

                result = JobValidator.validate_jobs(result)

                jobs.extend(result)

            except Exception:

                pass

        jobs = JobDeduplicator.deduplicate(jobs)

        return jobs

    def search_multiple_countries(
        self,
        roles,
        countries
    ):

        all_jobs = []

        with ThreadPoolExecutor(
            max_workers=2
        ) as executor:

            futures = {

                executor.submit(
                    self.search_single_country,
                    roles,
                    country
                ): country

                for country in countries

            }

            for future in as_completed(futures):

                try:

                    jobs = future.result()

                    all_jobs.extend(jobs)

                except Exception:

                    pass

        all_jobs = JobDeduplicator.deduplicate(all_jobs)

        return all_jobs