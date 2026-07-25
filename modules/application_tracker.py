import json
import os
from datetime import datetime


class ApplicationTracker:


    def __init__(self):

        self.file = (
            "database/application_tracker.json"
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



    def load_applications(self):

        with open(
            self.file,
            "r"
        ) as f:

            return json.load(f)



    def save_applications(
        self,
        applications
    ):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                applications,
                f,
                indent=4
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


        applications.append(
            application
        )


        self.save_applications(
            applications
        )


        return application



    def update_status(
        self,
        index,
        status
    ):

        applications = self.load_applications()


        if index < len(applications):

            applications[index]["status"] = status


        self.save_applications(
            applications
        )



    def get_applications(self):

        return self.load_applications()