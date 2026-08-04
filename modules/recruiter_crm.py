import sqlite3


class RecruiterCRM:

    def __init__(self):

        self.conn = sqlite3.connect(
            "database/jobhunter.db",
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS recruiters(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                recruiter_name TEXT,

                company TEXT,

                linkedin TEXT,

                email TEXT,

                status TEXT,

                notes TEXT
            )
        """)

        self.conn.commit()

    def add_recruiter(

        self,

        recruiter_name,

        company,

        linkedin,

        email,

        status="New",

        notes=""

    ):

        self.cursor.execute(

            """
            INSERT INTO recruiters(

                recruiter_name,

                company,

                linkedin,

                email,

                status,

                notes

            )

            VALUES(?,?,?,?,?,?)
            """,

            (

                recruiter_name,

                company,

                linkedin,

                email,

                status,

                notes

            )

        )

        self.conn.commit()

    def get_all_recruiters(self):

        self.cursor.execute(

            "SELECT * FROM recruiters ORDER BY recruiter_name"

        )

        return self.cursor.fetchall()

    def statistics(self):

        self.cursor.execute(

            "SELECT COUNT(*) FROM recruiters"

        )

        total = self.cursor.fetchone()[0]

        return {

            "total_recruiters": total

        }