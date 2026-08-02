class JobValidator:

    REQUIRED_FIELDS = [
        "role",
        "company",
        "country",
    ]

    @classmethod
    def validate_jobs(cls, jobs):

        valid = []

        for job in jobs:

            if not isinstance(job, dict):
                continue

            ok = True

            for field in cls.REQUIRED_FIELDS:

                if not job.get(field):
                    ok = False
                    break

            if ok:
                valid.append(job)

        return valid