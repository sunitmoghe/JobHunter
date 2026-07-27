from concurrent.futures import ThreadPoolExecutor, as_completed


class ParallelSearchEngine:

    def __init__(self, search_engine):

        self.search_engine = search_engine

    def search_roles(

        self,

        roles,

        max_workers=5

    ):

        jobs = []

        with ThreadPoolExecutor(

            max_workers=max_workers

        ) as executor:

            futures = {

                executor.submit(

                    self.search_engine.search_jobs,

                    role

                ): role

                for role in roles

            }

            for future in as_completed(

                futures

            ):

                role = futures[future]

                try:

                    results = future.result()

                    for job in results:

                        job["executive_role"] = role

                        jobs.append(job)

                except Exception as e:

                    print(

                        f"Search failed for {role}: {e}"

                    )

        return jobs