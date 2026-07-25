from modules.database import DatabaseManager


class ApplicationAnalytics:


    def get_summary(self):

        db = DatabaseManager()


        db.cursor.execute(
            """
            SELECT COUNT(*)
            FROM applications
            """
        )

        total = db.cursor.fetchone()[0]


        db.cursor.execute(
            """
            SELECT status, COUNT(*)
            FROM applications
            GROUP BY status
            """
        )

        status_data = db.cursor.fetchall()


        db.close()


        summary = {

            "total": total,

            "statuses": dict(status_data)

        }


        return summary