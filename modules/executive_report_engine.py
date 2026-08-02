from datetime import datetime


class ExecutiveReportEngine:

    def generate(self, jobs):

        total = len(jobs)

        high_priority = len(
            [
                job
                for job in jobs
                if job.get("executive_score", 0) >= 80
            ]
        )

        countries = len(
            set(
                job.get("country", "")
                for job in jobs
            )
        )

        companies = len(
            set(
                job.get("company", "")
                for job in jobs
            )
        )

        average = 0

        if total > 0:

            average = round(

                sum(

                    job.get(
                        "executive_score",
                        0
                    )

                    for job in jobs

                )

                / total,

                1

            )

        return {

            "generated_on":
                datetime.now().strftime(
                    "%d-%m-%Y %H:%M"
                ),

            "total_jobs":
                total,

            "high_priority_jobs":
                high_priority,

            "countries":
                countries,

            "companies":
                companies,

            "average_score":
                average

        }