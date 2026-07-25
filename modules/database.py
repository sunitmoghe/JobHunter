import sqlite3
from pathlib import Path


class DatabaseManager:

    def __init__(self, db_name="database/jobhunter.db"):

        Path("database").mkdir(exist_ok=True)

        self.connection = sqlite3.connect(db_name)

        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,
            email TEXT,
            phone TEXT,
            linkedin TEXT,

            experience TEXT,

            skills TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.connection.commit()

    def save_profile(self, profile):

        skills = ",".join(profile["skills"])

        self.cursor.execute("""
        INSERT INTO profiles
        (
            name,
            email,
            phone,
            linkedin,
            experience,
            skills
        )
        VALUES (?,?,?,?,?,?)
        """,
        (
            profile["name"],
            profile["email"],
            profile["phone"],
            profile["linkedin"],
            profile["experience"],
            skills
        ))

        self.connection.commit()

    def get_latest_profile(self):

        self.cursor.execute("""
        SELECT
            name,
            email,
            phone,
            linkedin,
            experience,
            skills
        FROM profiles
        ORDER BY id DESC
        LIMIT 1
        """)

        row = self.cursor.fetchone()

        if row is None:
            return None

        return {
            "name": row[0],
            "email": row[1],
            "phone": row[2],
            "linkedin": row[3],
            "experience": row[4],
            "skills": row[5].split(",") if row[5] else []
        }

    def close(self):
        self.connection.close()


if __name__ == "__main__":

    db = DatabaseManager()

    print("Database ready.")