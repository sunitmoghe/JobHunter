import json
import os
from datetime import datetime


class RecruiterManager:

    def __init__(
        self,
        file_path="data/recruiters.json",
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


    def _load(self):

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


    def _save(
        self,
        recruiters,
    ):

        with open(
            self.file_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                recruiters,
                file,
                indent=4,
                ensure_ascii=False,
            )


    def get_all_recruiters(self):

        return self._load()


    def add_recruiter(
        self,
        recruiter,
    ):

        recruiters = self._load()

        data = dict(
            recruiter
        )

        data[
            "created_on"
        ] = datetime.now().strftime(
            "%d-%m-%Y"
        )

        data[
            "follow_up_status"
        ] = "Not Contacted"

        data[
            "follow_up_date"
        ] = ""

        data[
            "notes"
        ] = ""

        recruiters.append(
            data
        )

        self._save(
            recruiters
        )

        return True


    def update_recruiter(
        self,
        index,
        updates,
    ):

        recruiters = self._load()

        if index < 0:

            return False

        if index >= len(
            recruiters
        ):

            return False

        recruiters[
            index
        ].update(
            updates
        )

        self._save(
            recruiters
        )

        return True


    def delete_recruiter(
        self,
        index,
    ):

        recruiters = self._load()

        if index < 0:

            return False

        if index >= len(
            recruiters
        ):

            return False

        recruiters.pop(
            index
        )

        self._save(
            recruiters
        )

        return True