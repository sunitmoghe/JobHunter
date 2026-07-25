import json
import os
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
    # DATABASE INITIALISATION
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
    # LOAD RECRUITERS SAFELY
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


                return []


        except (
            json.JSONDecodeError,
            FileNotFoundError
        ):


            self.save_recruiters([])


            return []

    # --------------------------------------------------
    # SAVE RECRUITERS SAFELY
    # --------------------------------------------------

    def save_recruiters(
        self,
        recruiters
    ):

        self.ensure_database()


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
    # ADD RECRUITER
    # --------------------------------------------------

    def add_recruiter(
        self,
        recruiter
    ):

        recruiters = self.load_recruiters()


        email = recruiter.get(
            "email",
            ""
        )


        # Duplicate check

        for existing in recruiters:

            if (
                email
                and
                existing.get("email")
                == email
            ):

                return existing



        recruiter_record = {


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


            "email": email,


            "linkedin": recruiter.get(
                "linkedin",
                ""
            ),


            "country": recruiter.get(
                "country",
                ""
            ),


            "status": "New",


            "last_contact": str(
                datetime.now().date()
            ),


            "notes": recruiter.get(
                "notes",
                ""
            )

        }



        recruiters.append(
            recruiter_record
        )


        self.save_recruiters(
            recruiters
        )


        return recruiter_record



    # --------------------------------------------------
    # UPDATE RECRUITER STATUS
    # --------------------------------------------------

    def update_status(
        self,
        index,
        status
    ):


        recruiters = self.load_recruiters()


        if 0 <= index < len(recruiters):


            recruiters[index]["status"] = status


            recruiters[index]["last_contact"] = str(
                datetime.now().date()
            )


            self.save_recruiters(
                recruiters
            )


            return True



        return False

    # --------------------------------------------------
    # GET ALL RECRUITERS
    # --------------------------------------------------

    def get_recruiters(
        self
    ):

        return self.load_recruiters()



    # --------------------------------------------------
    # SEARCH RECRUITERS
    # --------------------------------------------------

    def search_recruiters(
        self,
        keyword
    ):

        recruiters = self.load_recruiters()


        keyword = str(
            keyword
        ).lower()



        results = []


        for recruiter in recruiters:


            searchable = (

                recruiter.get(
                    "name",
                    ""
                )
                +
                recruiter.get(
                    "company",
                    ""
                )
                +
                recruiter.get(
                    "designation",
                    ""
                )
                +
                recruiter.get(
                    "country",
                    ""
                )

            ).lower()



            if keyword in searchable:

                results.append(
                    recruiter
                )



        return results



    # --------------------------------------------------
    # FILTER BY COUNTRY
    # --------------------------------------------------

    def recruiters_by_country(
        self,
        country
    ):

        recruiters = self.load_recruiters()


        return [

            recruiter

            for recruiter in recruiters

            if recruiter.get(
                "country",
                ""
            )
            ==
            country

        ]



    # --------------------------------------------------
    # DASHBOARD STATISTICS
    # --------------------------------------------------

    def get_statistics(
        self
    ):

        recruiters = self.load_recruiters()


        total = len(
            recruiters
        )


        contacted = len(

            [

                r

                for r in recruiters

                if r.get(
                    "status"
                )
                ==
                "Contacted"

            ]

        )


        responded = len(

            [

                r

                for r in recruiters

                if r.get(
                    "status"
                )
                ==
                "Responded"

            ]

        )



        return {

            "total_recruiters": total,

            "contacted": contacted,

            "responded": responded,

            "response_rate":

                round(

                    (
                        responded
                        /
                        total
                        *
                        100

                    )

                    if total > 0

                    else 0,

                    1

                )

        }

