from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


class ParallelSearchEngine:

    def __init__(
        self,
        engine,
        max_workers=5
    ):

        self.engine = engine

        self.max_workers = max_workers

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
                    self.engine.search_jobs,
                    role
                ): role

                for role in roles

            }

            for future in as_completed(futures):

                role = futures[future]

                try:

                    jobs = future.result()

                    if jobs:

                        for job in jobs:

                            job["executive_role"] = role

                        all_jobs.extend(jobs)

                except Exception as e:

                    print(

                        f"Search failed for {role}: {e}"

                    )

        return all_jobs


if __name__ == "__main__":

    print(

        "Parallel Search Engine Ready"

    )