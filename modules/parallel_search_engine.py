from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback

from modules.job_validator import JobValidator
from modules.job_deduplicator import JobDeduplicator
from modules.search_scheduler import SearchScheduler


class ParallelSearchEngine:

    def __init__(self, engine, max_workers=6):

        self.engine = engine
        self.max_workers = max_workers
        self.scheduler = SearchScheduler()

    # --------------------------------------------------

    def search_role(
        self,
        role,
        selected_countries=None
    ):

        try:

            jobs = self.engine.search_jobs(
                role=role,
                selected_countries=selected_countries
            )

            jobs = JobValidator.validate_jobs(jobs)
            jobs = JobDeduplicator.remove_empty(jobs)
            jobs = JobDeduplicator.deduplicate(jobs)

            for job in jobs:

                job["executive_role"] = role

            return jobs

        except Exception as e:

            print(f"\nSearch Error ({role})")
            print(e)
            traceback.print_exc()

            return []

    # --------------------------------------------------

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

                role = futures[future]

                try:

                    jobs = future.result()

                    if jobs:

                        all_jobs.extend(jobs)

                        print(
                            f"✓ {role}: {len(jobs)} jobs"
                        )

                except Exception as e:

                    print(f"{role} failed : {e}")

        all_jobs = JobDeduplicator.remove_empty(all_jobs)
        all_jobs = JobDeduplicator.deduplicate(all_jobs)

        return all_jobs

    # --------------------------------------------------

    def search_single_country(
        self,
        roles,
        country
    ):

        jobs = []

        for role in roles:

            try:

                result = self.engine.search_jobs(
                    role=role,
                    selected_countries=[country]
                )

                result = JobValidator.validate_jobs(result)

                for job in result:

                    job["executive_role"] = role

                jobs.extend(result)

            except Exception:

                pass

        jobs = JobDeduplicator.remove_empty(jobs)
        jobs = JobDeduplicator.deduplicate(jobs)

        return jobs

    # --------------------------------------------------

    def search_multiple_countries(
        self,
        roles,
        countries
    ):

        all_jobs = []

        with ThreadPoolExecutor(
            max_workers=min(
                len(countries),
                self.max_workers
            )
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

                country = futures[future]

                try:

                    jobs = future.result()

                    all_jobs.extend(jobs)

                    print(
                        f"✓ {country}: {len(jobs)} jobs"
                    )

                except Exception as e:

                    print(
                        f"{country} failed : {e}"
                    )

        all_jobs = JobDeduplicator.remove_empty(all_jobs)
        all_jobs = JobDeduplicator.deduplicate(all_jobs)

        return all_jobs

    # --------------------------------------------------

if __name__ == "__main__":

    from modules.unified_job_engine import UnifiedJobEngine

    engine = UnifiedJobEngine()

    parallel = ParallelSearchEngine(
        engine=engine,
        max_workers=3
    )

    roles = [

        "Head of Sales",
        "Regional Sales Director"

    ]

    countries = [

        "Singapore",
        "Germany"

    ]

    jobs = parallel.search_multiple_countries(

        roles,
        countries

    )

    print()

    print("=" * 60)

    print("TOTAL UNIQUE JOBS :", len(jobs))

    print("=" * 60)

    for job in jobs[:10]:

        print(

            f"{job.get('role')} | "
            f"{job.get('company')} | "
            f"{job.get('country')} | "
            f"{job.get('source')}"

        )