import sqlite3
from pathlib import Path


class RecruiterDatabase:


    def __init__(self, db_name="database/jobhunter.db"):

        Path("database").mkdir(exist_ok=True)

        self.connection = sqlite3.connect(db_name)

        self.cursor = self.connection.cursor()

        self.create_table()



    def create_table(self):

        self.cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS recruiters (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            recruiter_name TEXT,

            company TEXT,

            designation TEXT,

            linkedin TEXT,

            email TEXT,

            role TEXT,

            status TEXT,

            follow_up TEXT,

            notes TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
        )

        self.connection.commit()



    def add_recruiter(
        self,
        recruiter_name,
        company,
        designation,
        linkedin,
        email,
        role,
        status,
        follow_up,
        notes
    ):


        self.cursor.execute(
        """
        INSERT INTO recruiters

        (
        recruiter_name,
        company,
        designation,
        linkedin,
        email,
        role,
        status,
        follow_up,
        notes
        )

        VALUES (?,?,?,?,?,?,?,?,?)

        """,

        (
        recruiter_name,
        company,
        designation,
        linkedin,
        email,
        role,
        status,
        follow_up,
        notes
        )

        )

        self.connection.commit()



    def get_recruiters(self):

        self.cursor.execute(
        """
        SELECT *
        FROM recruiters
        ORDER BY id DESC
        """
        )

        return self.cursor.fetchall()