class JobDeduplicator:

    SOURCE_PRIORITY = {

        "Adzuna": 100,
        "Greenhouse": 95,
        "Lever": 90,
        "Ashby": 88,
        "TheMuse": 85,
        "Remotive": 82,
        "RemoteOK": 80,
        "Unknown": 0

    }

    # --------------------------------------------------

    @classmethod
    def remove_empty(cls, jobs):

        cleaned = []

        if not jobs:

            return cleaned

        for job in jobs:

            if not isinstance(job, dict):

                continue

            role = str(

                job.get(
                    "role",
                    job.get(
                        "title",
                        ""
                    )
                )

            ).strip()

            company = str(

                job.get(
                    "company",
                    ""
                )

            ).strip()

            if not role or not company:

                continue

            job["role"] = role
            job["company"] = company

            cleaned.append(job)

        return cleaned

    # --------------------------------------------------

    @classmethod
    def deduplicate(cls, jobs):

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

            country = str(

                job.get(
                    "country",
                    ""
                )

            ).strip().lower()

            link = str(

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
                location,
                country,
                link

            )

            current_priority = cls.SOURCE_PRIORITY.get(

                job.get(
                    "source",
                    "Unknown"
                ),

                0

            )

            if key not in unique:

                unique[key] = job

                continue

            existing = unique[key]

            existing_priority = cls.SOURCE_PRIORITY.get(

                existing.get(
                    "source",
                    "Unknown"
                ),

                0

            )

            existing_score = float(

                existing.get(
                    "jobhunter_score",
                    0
                )

            )

            current_score = float(

                job.get(
                    "jobhunter_score",
                    0
                )

            )

            if current_priority > existing_priority:

                unique[key] = job

            elif (

                current_priority == existing_priority
                and
                current_score > existing_score

            ):

                unique[key] = job

        return list(unique.values())

    # --------------------------------------------------

    @classmethod
    def process(cls, jobs):

        jobs = cls.remove_empty(jobs)

        jobs = cls.deduplicate(jobs)

        return jobs


if __name__ == "__main__":

    sample = [

        {
            "role": "Head of Sales",
            "company": "Microsoft",
            "location": "Singapore",
            "country": "Singapore",
            "source": "RemoteOK",
            "jobhunter_score": 82
        },

        {
            "role": "Head of Sales",
            "company": "Microsoft",
            "location": "Singapore",
            "country": "Singapore",
            "source": "Greenhouse",
            "jobhunter_score": 75
        },

        {
            "role": "Regional Director",
            "company": "Google",
            "location": "London",
            "country": "UK",
            "source": "Adzuna"
        }

    ]

    jobs = JobDeduplicator.process(sample)

    print(f"\nUnique Jobs : {len(jobs)}\n")

    for job in jobs:

        print(

            f"{job['role']} | "
            f"{job['company']} | "
            f"{job['source']}"

        )