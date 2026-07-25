import json
import os
from datetime import datetime


class ApplicationTracker:

    def __init__(self):

        self.database_dir = "database"

        self.file = os.path.join(
            self.database_dir,
            "application_tracker.json"
        )

        self.ensure_database()

    def ensure_database(self):

        os.makedirs(
            self.database_dir,
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

    def load_applications(self):

        self.ensure_database()

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

                if isinstance(data, list):

                    return data

                return []

        except (json.JSONDecodeError, FileNotFoundError):

            self.save_applications([])

            return []

    def save_applications(
        self,
        applications
    ):

        self.ensure_database()

        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                applications,
                f,
                indent=4,
                ensure_ascii=False
            )

    def add_application(
        self,
        job,
        score,
        interview_probability
    ):

        applications = self.load_applications()

        application = {

            "company": job.get(
                "company",
                ""
            ),

            "role": job.get(
                "role",
                ""
            ),

            "country": job.get(
                "country",
                ""
            ),

            "status": "Applied",

            "priority_score": score,

            "interview_probability": interview_probability,

            "application_date": str(
                datetime.now().date()
            ),

            "recruiter": "",

            "notes": ""

        }

        applications.append(application)

        self.save_applications(applications)

        return application

    def update_status(
        self,
        index,
        status
    ):

        applications = self.load_applications()

        if 0 <= index < len(applications):

            applications[index]["status"] = status

            self.save_applications(applications)

    def get_applications(self):

        return self.load_applications()