class JobDeduplicator:

    @staticmethod
    def deduplicate(jobs):

        unique = {}
        cleaned = []

        for job in jobs:

            role = str(
                job.get("role", "")
            ).strip().lower()

            company = str(
                job.get("company", "")
            ).strip().lower()

            country = str(
                job.get("country", "")
            ).strip().lower()

            key = (
                role,
                company,
                country
            )

            if key not in unique:

                unique[key] = True

                cleaned.append(job)

        return cleaned

    @staticmethod
    def remove_empty(jobs):

        return [

            job

            for job in jobs

            if job.get("role")
            and job.get("company")

        ]