import json
import os
from datetime import datetime


class RecruiterManager:


    def __init__(self):

        self.file = (
            "database/recruiters.json"
        )

        self.ensure_database()



    def ensure_database(self):

        if not os.path.exists(
            self.file
        ):

            with open(
                self.file,
                "w"
            ) as f:

                json.dump(
                    [],
                    f
                )



    def load_recruiters(self):

        with open(
            self.file,
            "r"
        ) as f:

            return json.load(f)



    def save_recruiters(
        self,
        recruiters
    ):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                recruiters,
                f,
                indent=4
            )



    def add_recruiter(
        self,
        name,
        company,
        role="",
        linkedin="",
        email=""
    ):

        recruiters = self.load_recruiters()


        recruiter = {

            "name": name,

            "company": company,

            "role": role,

            "linkedin": linkedin,

            "email": email,

            "status": "New",

            "last_contact": str(
                datetime.now().date()
            ),

            "notes": ""

        }


        recruiters.append(
            recruiter
        )


        self.save_recruiters(
            recruiters
        )


        return recruiter



    def update_status(
        self,
        index,
        status
    ):

        recruiters = self.load_recruiters()


        if index < len(recruiters):

            recruiters[index]["status"] = status

            recruiters[index]["last_contact"] = str(
                datetime.now().date()
            )


        self.save_recruiters(
            recruiters
        )



    def update_notes(
        self,
        index,
        notes
    ):

        recruiters = self.load_recruiters()


        if index < len(recruiters):

            recruiters[index]["notes"] = notes


        self.save_recruiters(
            recruiters
        )



    def get_recruiters(self):

        return self.load_recruiters()