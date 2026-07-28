import re


class DuplicateJobDetector:

    def __init__(self):

        pass

    def normalize(self, value):

        if value is None:

            return ""

        value = str(value).lower().strip()

        value = re.sub(r"\s+", " ", value)

        return value

    def generate_key(self, job):

        company = self.normalize(
            job.get("company")
        )

        role = self.normalize(
            job.get("role")
            or job.get("title")
        )

        location = self.normalize(
            job.get("location")
        )

        return f"{company}|{role}|{location}"

    def calculate_quality_score(self, job):

        score = 0

        if job.get("salary"):

            score += 10

        if job.get("description"):

            score += min(
                len(
                    job["description"]
                ) // 100,
                10
            )

        if job.get("apply_link"):

            score += 5

        if job.get("source"):

            score += 2

        if job.get("executive_score"):

            score += int(
                job.get(
                    "executive_score",
                    0
                )
            )

        return score

    def remove_duplicates(self, jobs):

        best_jobs = {}

        duplicate_count = 0

        for job in jobs:

            key = self.generate_key(job)

            score = self.calculate_quality_score(
                job
            )

            if key not in best_jobs:

                best_jobs[key] = (

                    score,
                    job

                )

            else:

                duplicate_count += 1

                existing_score = best_jobs[key][0]

                if score > existing_score:

                    best_jobs[key] = (

                        score,
                        job

                    )

        cleaned_jobs = [

            item[1]

            for item in best_jobs.values()

        ]

        cleaned_jobs.sort(

            key=lambda x: x.get(
                "executive_score",
                0
            ),

            reverse=True

        )

        return {

            "jobs": cleaned_jobs,

            "duplicates_removed": duplicate_count,

            "final_jobs": len(cleaned_jobs)

        }


if __name__ == "__main__":

    detector = DuplicateJobDetector()

    sample_jobs = [

        {

            "company": "Microsoft",

            "role": "Sales Director",

            "location": "London",

            "executive_score": 92

        },

        {

            "company": "Microsoft",

            "role": "Sales Director",

            "location": "London",

            "executive_score": 87

        },

        {

            "company": "Google",

            "role": "VP Sales",

            "location": "Singapore",

            "executive_score": 95

        }

    ]

    result = detector.remove_duplicates(
        sample_jobs
    )

    print()

    print("Duplicates Removed :",

          result["duplicates_removed"])

    print("Remaining Jobs :",

          result["final_jobs"])