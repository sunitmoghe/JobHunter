import json
import os
import uuid
from datetime import datetime


class RecruiterManager:

    def __init__(self):

        self.database_dir = "database"

        self.file = os.path.join(
            self.database_dir,
            "recruiters.json"
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

    def load_recruiters(self):

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

    def save_recruiters(
        self,
        recruiters
    ):

        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                recruiters,
                f,
                indent=4,
                ensure_ascii=False
            )

    # --------------------------------------------------

    def add_recruiter(
        self,
        recruiter
    ):

        recruiters = self.load_recruiters()

        email = str(

            recruiter.get(
                "email",
                ""
            )

        ).strip().lower()

        linkedin = str(

            recruiter.get(
                "linkedin",
                ""
            )

        ).strip().lower()

        for existing in recruiters:

            if (

                email
                and
                existing.get(
                    "email",
                    ""
                ).lower() == email

            ):

                return existing

            if (

                linkedin
                and
                existing.get(
                    "linkedin",
                    ""
                ).lower() == linkedin

            ):

                return existing

        record = {

            "recruiter_id": str(uuid.uuid4()),

            "name": recruiter.get(
                "name",
                ""
            ),

            "company": recruiter.get(
                "company",
                ""
            ),

            "designation": recruiter.get(
                "designation",
                ""
            ),

            "email": recruiter.get(
                "email",
                ""
            ),

            "phone": recruiter.get(
                "phone",
                ""
            ),

            "linkedin": recruiter.get(
                "linkedin",
                ""
            ),

            "country": recruiter.get(
                "country",
                ""
            ),

            "status": recruiter.get(
                "status",
                "New"
            ),

            "last_contact": "",

            "next_followup": "",

            "notes": recruiter.get(
                "notes",
                ""
            ),

            "created_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),

            "updated_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            )

        }

        recruiters.append(record)

        self.save_recruiters(recruiters)

        return record

    # --------------------------------------------------

    def update_status(
        self,
        recruiter_id,
        status
    ):

        recruiters = self.load_recruiters()

        for recruiter in recruiters:

            if recruiter.get(
                "recruiter_id"
            ) == recruiter_id:

                recruiter["status"] = status

                recruiter["last_contact"] = datetime.now().strftime(
                    "%Y-%m-%d"
                )

                recruiter["updated_at"] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                )

                self.save_recruiters(recruiters)

                return True

        return False

    # --------------------------------------------------

    def get_recruiters(self):

        return self.load_recruiters()

    # --------------------------------------------------

    def search_recruiters(
        self,
        keyword
    ):

        keyword = str(keyword).lower()

        results = []

        for recruiter in self.load_recruiters():

            searchable = " ".join([

                recruiter.get("name", ""),
                recruiter.get("company", ""),
                recruiter.get("designation", ""),
                recruiter.get("country", ""),
                recruiter.get("email", "")

            ]).lower()

            if keyword in searchable:

                results.append(recruiter)

        return results

    # --------------------------------------------------

    def recruiters_by_country(
        self,
        country
    ):

        return [

            recruiter

            for recruiter in self.load_recruiters()

            if recruiter.get(
                "country",
                ""
            ).lower() == country.lower()

        ]

    # --------------------------------------------------

    def get_statistics(self):

        recruiters = self.load_recruiters()

        stats = {

            "total_recruiters": len(recruiters),

            "new": 0,

            "contacted": 0,

            "responded": 0,

            "interview": 0,

            "closed": 0

        }

        for recruiter in recruiters:

            status = recruiter.get(
                "status",
                "New"
            ).lower()

            if status == "new":

                stats["new"] += 1

            elif status == "contacted":

                stats["contacted"] += 1

            elif status == "responded":

                stats["responded"] += 1

            elif status == "interview":

                stats["interview"] += 1

            elif status == "closed":

                stats["closed"] += 1

        stats["response_rate"] = round(

            (

                stats["responded"]
                /
                stats["total_recruiters"]

            ) * 100,

            1

        ) if stats["total_recruiters"] else 0

        return stats


if __name__ == "__main__":

    manager = RecruiterManager()

    manager.add_recruiter(

        {

            "name": "John Smith",

            "company": "Microsoft",

            "designation": "Talent Acquisition",

            "email": "john@microsoft.com",

            "country": "Singapore",

            "linkedin": "linkedin.com/in/johnsmith"

        }

    )

    print()

    print(manager.get_statistics())

    print()

    print(manager.get_recruiters())