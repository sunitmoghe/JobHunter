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

        # Prevent duplicate applications
        db.cursor.execute(
            """
            SELECT id
            FROM applications
            WHERE company=?
            AND role=?
            AND country=?
            """,
            (
                company,
                role,
                country
            )
        )

        existing = db.cursor.fetchone()

        if existing:

            db.close()
            return False

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

        return True

    def get_applications(self):

        db = DatabaseManager()

        db.cursor.execute(
            """
            SELECT *
            FROM applications
            ORDER BY application_date DESC,id DESC
            """
        )

        applications = db.cursor.fetchall()

        db.close()

        return applications

    def delete_application(
        self,
        application_id
    ):

        db = DatabaseManager()

        db.cursor.execute(
            """
            DELETE FROM applications
            WHERE id=?
            """,
            (
                application_id,
            )
        )

        db.connection.commit()

        db.close()

    def update_status(
        self,
        application_id,
        status
    ):

        db = DatabaseManager()

        db.cursor.execute(
            """
            UPDATE applications
            SET status=?
            WHERE id=?
            """,
            (
                status,
                application_id
            )
        )

        db.connection.commit()

        db.close()