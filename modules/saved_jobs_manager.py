import json
import os
from datetime import datetime


class SavedJobsManager:

    def __init__(
        self,
        file_path="data/saved_jobs.json",
    ):

        self.file_path = file_path

        directory = os.path.dirname(
            self.file_path
        )

        if directory:
            os.makedirs(
                directory,
                exist_ok=True,
            )

        if not os.path.exists(
            self.file_path
        ):

            with open(
                self.file_path,
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    [],
                    file,
                    indent=4,
                )

    def load_jobs(self):

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8",
            ) as file:

                jobs = json.load(file)

                if isinstance(
                    jobs,
                    list,
                ):

                    return jobs

        except Exception:

            pass

        return []

    def save_job(
        self,
        job,
    ):

        jobs = self.load_jobs()

        job_id = self.get_job_id(
            job
        )

        for existing in jobs:

            if (
                self.get_job_id(existing)
                == job_id
            ):

                return False

        saved_job = dict(job)

        saved_job[
            "saved_on"
        ] = datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        )

        jobs.append(
            saved_job
        )

        self._write_jobs(
            jobs
        )

        return True

    def remove_job(
        self,
        job,
    ):

        jobs = self.load_jobs()

        job_id = self.get_job_id(
            job
        )

        updated = [

            item

            for item in jobs

            if self.get_job_id(item)
            != job_id

        ]

        if len(updated) == len(jobs):

            return False

        self._write_jobs(
            updated
        )

        return True

    def get_job_id(
        self,
        job,
    ):

        return "|".join(
            [
                str(
                    job.get(
                        "title",
                        job.get(
                            "role",
                            "",
                        ),
                    )
                ),
                str(
                    job.get(
                        "company",
                        "",
                    )
                ),
                str(
                    job.get(
                        "location",
                        "",
                    )
                ),
                str(
                    job.get(
                        "apply_link",
                        "",
                    )
                ),
            ]
        )

    def _write_jobs(
        self,
        jobs,
    ):

        with open(
            self.file_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                jobs,
                file,
                indent=4,
                ensure_ascii=False,
            )