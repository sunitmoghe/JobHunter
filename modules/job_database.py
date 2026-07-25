from modules.database import DatabaseManager


def add_sample_jobs():

    db = DatabaseManager()

    jobs = [

        (
            "Head of Sales",
            "Google",
            "Singapore",
            "Singapore",
            "SGD 180K-220K",
            "SaaS, Sales Strategy, CRM, Leadership",
            "https://careers.google.com",
            "Today"
        ),

        (
            "VP Sales",
            "SAP",
            "Germany",
            "Germany",
            "EUR 150K-180K",
            "ERP, Enterprise Sales, SaaS",
            "https://jobs.sap.com",
            "Today"
        ),

        (
            "Country Manager",
            "Microsoft",
            "UAE",
            "Dubai",
            "AED 900K-1.2M",
            "Cloud, Enterprise Sales, P&L",
            "https://careers.microsoft.com",
            "Today"
        )

    ]


    for job in jobs:

        db.cursor.execute(
            """
            INSERT INTO jobs
            (
                role,
                company,
                country,
                location,
                salary,
                skills,
                job_link,
                posted_date
            )
            VALUES (?,?,?,?,?,?,?,?)
            """,
            job
        )


    db.connection.commit()

    db.close()


if __name__ == "__main__":

    add_sample_jobs()

    print("Sample jobs added successfully")