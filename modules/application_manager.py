from modules.database import DatabaseManager
from datetime import datetime


class ApplicationManager:


    def add_application(
        self,
        company,
        role,
        country,
        location,
        job_link="",
        contact_person="",
        contact_email="",
        status="Applied",
        follow_up_date="",
        notes=""
    ):

        db = DatabaseManager()


        db.cursor.execute(
            """
            INSERT INTO applications
            (
                company,
                role,
                country,
                location,
                job_link,
                contact_person,
                contact_email,
                status,
                application_date,
                follow_up_date,
                notes
            )
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                company,
                role,
                country,
                location,
                job_link,
                contact_person,
                contact_email,
                status,
                datetime.now().strftime("%Y-%m-%d"),
                follow_up_date,
                notes
            )
        )


        db.connection.commit()

        db.close()


    def get_applications(self):

        db = DatabaseManager()


        db.cursor.execute(
            """
            SELECT *
            FROM applications
            ORDER BY id DESC
            """
        )


        applications = db.cursor.fetchall()

        db.close()

        return applications