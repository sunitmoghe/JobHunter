from collections import Counter


class ExecutiveDashboard:

    def generate(self, jobs, saved_jobs=None):

        if saved_jobs is None:
            saved_jobs = []

        total_jobs = len(jobs)

        saved_count = len(saved_jobs)

        countries = Counter()

        companies = Counter()

        total_score = 0

        high_priority = 0

        for job in jobs:

            location = job.get(
                "location",
                "Unknown"
            )

            company = job.get(
                "company",
                "Unknown"
            )

            countries[location] += 1

            companies[company] += 1

            score = job.get(
                "executive_score",
                0
            )

            total_score += score

            if score >= 90:

                high_priority += 1

        average_score = 0

        if total_jobs:

            average_score = round(

                total_score / total_jobs,

                2

            )

        return {

            "total_jobs": total_jobs,

            "saved_jobs": saved_count,

            "average_score": average_score,

            "high_priority_jobs": high_priority,

            "top_countries": countries.most_common(5),

            "top_companies": companies.most_common(10)

        }


if __name__ == "__main__":

    dashboard = ExecutiveDashboard()

    jobs = [

        {

            "company": "Microsoft",

            "location": "London",

            "executive_score": 95

        },

        {

            "company": "Google",

            "location": "Singapore",

            "executive_score": 91

        },

        {

            "company": "Microsoft",

            "location": "London",

            "executive_score": 82

        }

    ]

    saved = [

        {

            "company": "Microsoft"

        }

    ]

    print(

        dashboard.generate(

            jobs,

            saved

        )