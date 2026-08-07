import json
import os
from datetime import datetime
import uuid


class SavedJobsManager:

    def __init__(self):

        self.database = "database"

        self.file = os.path.join(
            self.database,
            "saved_jobs.json"
        )

        self.ensure_database()

    # --------------------------------------------------

    def ensure_database(self):

        os.makedirs(
            self.database,
            exist_ok=True
        )

        if not os.path.exists(self.file):

            with open(
                self.file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    [],
                    f,
                    indent=4
                )

    # --------------------------------------------------

    def load_jobs(self):

        self.ensure_database()

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception:

            return []

    # --------------------------------------------------

    def save_jobs(self, jobs):

        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                jobs,
                f,
                indent=4,
                ensure_ascii=False
            )

    # --------------------------------------------------

    def save_job(self, job):

        jobs = self.load_jobs()

        key = (

            str(job.get("company", "")).lower(),

            str(
                job.get(
                    "role",
                    job.get(
                        "title",
                        ""
                    )
                )
            ).lower(),

            str(
                job.get(
                    "location",
                    ""
                )
            ).lower()

        )

        for existing in jobs:

            existing_key = (

                str(existing.get("company", "")).lower(),

                str(
                    existing.get(
                        "role",
                        existing.get(
                            "title",
                            ""
                        )
                    )
                ).lower(),

                str(
                    existing.get(
                        "location",
                        ""
                    )
                ).lower()

            )

            if key == existing_key:

                return False

        job["job_id"] = str(uuid.uuid4())

        job["saved_date"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        job["last_updated"] = job["saved_date"]

        job["application_status"] = "Saved"

        job["favorite"] = False

        job["notes"] = ""

        jobs.append(job)

        self.save_jobs(jobs)

        return True

    # --------------------------------------------------

    def remove_job(
        self,
        company,
        role,
        location
    ):

        jobs = self.load_jobs()

        filtered = []

        removed = False

        for job in jobs:

            if (

                job.get(
                    "company",
                    ""
                ).lower() == company.lower()

                and

                job.get(
                    "role",
                    job.get(
                        "title",
                        ""
                    )
                ).lower() == role.lower()

                and

                job.get(
                    "location",
                    ""
                ).lower() == location.lower()

            ):

                removed = True

                continue

            filtered.append(job)

        self.save_jobs(filtered)

        return removed

    # --------------------------------------------------

    def update_status(
        self,
        job_id,
        status
    ):

        jobs = self.load_jobs()

        for job in jobs:

            if job.get("job_id") == job_id:

                job["application_status"] = status

                job["last_updated"] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

        self.save_jobs(jobs)

    # --------------------------------------------------

    def statistics(self):

        jobs = self.load_jobs()

        stats = {

            "saved_jobs": len(jobs),

            "applied": 0,

            "interview": 0,

            "offer": 0,

            "rejected": 0

        }

        for job in jobs:

            status = str(
                job.get(
                    "application_status",
                    ""
                )
            ).lower()

            if status == "applied":

                stats["applied"] += 1

            elif status == "interview":

                stats["interview"] += 1

            elif status == "offer":

                stats["offer"] += 1

            elif status == "rejected":

                stats["rejected"] += 1

        return stats


if __name__ == "__main__":

    manager = SavedJobsManager()

    sample = {

        "company": "Microsoft",

        "role": "Sales Director",

        "location": "London"

    }

    manager.save_job(sample)

    print(manager.statistics())
