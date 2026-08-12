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

    def get_all_applications(self):

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

        application["role"] = role or ""

        application["country"] = (
            country or ""
        )

        application["location"] = (
            location or ""
        )

        application["status"] = "Applied"

        application["applied_on"] = (
            datetime.now().strftime(
                "%d-%m-%Y"
            )
        )

        applications.append(
            application
        )

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

        return True