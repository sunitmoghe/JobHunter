import json
import os
import uuid
from datetime import datetime


class ApplicationTracker:

    def __init__(self):

        self.database_dir = "database"

        self.file = os.path.join(
            self.database_dir,
            "application_tracker.json"
        )

        self.ensure_database()

    # --------------------------------------------------

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

    # --------------------------------------------------

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

        except Exception:

            pass

        return []

    # --------------------------------------------------

    def save_applications(
        self,
        applications
    ):

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

    # --------------------------------------------------

    def mark_applied(
        self,
        job
    ):

        applications = self.load_applications()

        company = job.get(
            "company",
            ""
        ).lower()

        role = job.get(
            "role",
            job.get(
                "title",
                ""
            )
        ).lower()

        country = job.get(
            "country",
            ""
        ).lower()

        # Prevent duplicate applications

        for app in applications:

            if (

                app.get(
                    "company",
                    ""
                ).lower() == company

                and

                app.get(
                    "role",
                    ""
                ).lower() == role

                and

                app.get(
                    "country",
                    ""
                ).lower() == country

            ):

                return app

        now = datetime.now()

        application = {

            "application_id": str(uuid.uuid4()),

            "company": job.get(
                "company",
                ""
            ),

            "role": job.get(
                "role",
                job.get(
                    "title",
                    ""
                )
            ),

            "country": job.get(
                "country",
                ""
            ),

            "location": job.get(
                "location",
                ""
            ),

            "status": "Applied",

            "priority_score": job.get(
                "priority_score",
                0
            ),

            "executive_score": job.get(
                "executive_score",
                0
            ),

            "jobhunter_score": job.get(
                "jobhunter_score",
                0
            ),

            "application_date": now.strftime(
                "%Y-%m-%d"
            ),

            "last_updated": now.strftime(
                "%Y-%m-%d %H:%M"
            ),

            "interview_date": "",

            "follow_up_date": "",

            "offer_date": "",

            "recruiter": job.get(
                "recruiter_name",
                ""
            ),

            "notes": "",

            "history": [

                {

                    "date": now.strftime(
                        "%Y-%m-%d %H:%M"
                    ),

                    "status": "Applied"

                }

            ]

        }

        applications.append(application)

        self.save_applications(applications)

        return application

    # --------------------------------------------------

    def update_status(
        self,
        application_id,
        new_status
    ):

        applications = self.load_applications()

        updated = False

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )

        for application in applications:

            if application.get(
                "application_id"
            ) == application_id:

                application["status"] = new_status

                application["last_updated"] = now

                application.setdefault(
                    "history",
                    []
                ).append(

                    {

                        "date": now,

                        "status": new_status

                    }

                )

                updated = True

                break

        if updated:

            self.save_applications(applications)

        return updated

    # --------------------------------------------------

    def get_applications(self):

        applications = self.load_applications()

        applications.sort(

            key=lambda x: x.get(
                "application_date",
                ""
            ),

            reverse=True

        )

        return applications

    # --------------------------------------------------

    def statistics(self):

        applications = self.load_applications()

        stats = {

            "total": len(applications),

            "applied": 0,

            "interview": 0,

            "offer": 0,

            "rejected": 0

        }

        for app in applications:

            status = app.get(
                "status",
                ""
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

    tracker = ApplicationTracker()

    sample = {

        "company": "Microsoft",

        "role": "Head of Sales",

        "country": "Singapore",

        "priority_score": 95,

        "executive_score": 92,

        "jobhunter_score": 94,

        "recruiter_name": "Talent Acquisition"

    }

    tracker.mark_applied(sample)

    print(tracker.statistics())