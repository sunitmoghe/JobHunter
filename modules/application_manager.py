import json
import os
from datetime import datetime


class ApplicationManager:

    def __init__(
        self,
        file_path="data/applications.json",
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

            self._save([])

    # ==========================================================
    # INTERNAL STORAGE
    # ==========================================================

    def _save(
        self,
        applications,
    ):

        with open(
            self.file_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                applications,
                file,
                indent=4,
                ensure_ascii=False,
            )

    # ==========================================================
    # GET APPLICATIONS
    # ==========================================================

    def get_all_applications(
        self,
    ):

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(file)

                if isinstance(
                    data,
                    list,
                ):

                    return data

        except Exception:

            pass

        return []

    # ==========================================================
    # ADD APPLICATION
    # ==========================================================

    def add_application(
        self,
        job=None,
        role=None,
        country=None,
        location=None,
    ):

        applications = (
            self.get_all_applications()
        )

        if isinstance(
            job,
            dict,
        ):

            application = dict(job)

            role = application.get(
                "role",
                application.get(
                    "title",
                    role or "",
                ),
            )

            country = application.get(
                "country",
                country or "",
            )

            location = application.get(
                "location",
                location or "",
            )

        else:

            application = {

                "role": role or "",

                "country": country or "",

                "location": location or "",

            }

        application["job_title"] = (
            application.get(
                "title",
                application.get(
                    "role",
                    role or "Executive Position",
                ),
            )
        )

        application["role"] = (
            role or ""
        )

        application["country"] = (
            country or ""
        )

        application["location"] = (
            location or ""
        )

        application["status"] = (
            "Applied"
        )

        application["applied_on"] = (
            datetime.now().strftime(
                "%d-%m-%Y"
            )
        )

        application["last_updated"] = (
            datetime.now().strftime(
                "%d-%m-%Y %H:%M"
            )
        )

        application.setdefault(
            "history",
            [],
        )

        application["history"].append(
            {
                "date":
                    datetime.now().strftime(
                        "%d-%m-%Y %H:%M"
                    ),

                "status":
                    "Applied",
            }
        )

        applications.append(
            application
        )

        self._save(
            applications
        )

        return True

    # ==========================================================
    # UPDATE STATUS
    # ==========================================================

    def update_status(
        self,
        application_index,
        new_status,
    ):

        applications = (
            self.get_all_applications()
        )

        if not applications:

            return False

        if not isinstance(
            application_index,
            int,
        ):

            return False

        if (
            application_index < 0
            or
            application_index >= len(
                applications
            )
        ):

            return False

        valid_statuses = [

            "Applied",
            "Interview",
            "Offer",
            "Rejected",
            "Withdrawn",

        ]

        if new_status not in valid_statuses:

            return False

        application = applications[
            application_index
        ]

        now = datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        )

        application["status"] = (
            new_status
        )

        application["last_updated"] = (
            now
        )

        application.setdefault(
            "history",
            [],
        )

        application["history"].append(
            {
                "date": now,
                "status": new_status,
            }
        )

        self._save(
            applications
        )

        return True

    # ==========================================================
    # APPLICATION STATISTICS
    # ==========================================================

    def get_statistics(
        self,
    ):

        applications = (
            self.get_all_applications()
        )

        statistics = {

            "total": len(
                applications
            ),

            "applied": 0,

            "interview": 0,

            "offer": 0,

            "rejected": 0,

            "withdrawn": 0,

        }

        for application in applications:

            status = application.get(
                "status",
                "",
            ).lower()

            if status == "applied":

                statistics[
                    "applied"
                ] += 1

            elif status == "interview":

                statistics[
                    "interview"
                ] += 1

            elif status == "offer":

                statistics[
                    "offer"
                ] += 1

            elif status == "rejected":

                statistics[
                    "rejected"
                ] += 1

            elif status == "withdrawn":

                statistics[
                    "withdrawn"
                ] += 1

        return statistics


# ==========================================================
# DIRECT TEST
# ==========================================================

if __name__ == "__main__":

    manager = ApplicationManager()

    print(
        "ApplicationManager: OK"
    )

    print(
        "Applications:",
        len(
            manager.get_all_applications()
        )
    )

    print(
        "Statistics:",
        manager.get_statistics()
    )