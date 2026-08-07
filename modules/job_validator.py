class JobValidator:

    REQUIRED_FIELDS = [
        "role",
        "company"
    ]

    DEFAULTS = {

        "country": "Global",
        "location": "Remote",
        "salary": "Not Disclosed",
        "source": "Unknown",
        "apply_link": "",
        "description": "",
        "executive_score": 0,
        "priority_score": 0,
        "jobhunter_score": 0,
        "visa_sponsorship": False,
        "posted_date": "",
        "employment_type": "",
        "experience_level": "",
        "remote": False

    }

    # --------------------------------------------------

    @classmethod
    def validate_jobs(
        cls,
        jobs
    ):

        validated = []

        if not jobs:

            return validated

        for job in jobs:

            if not isinstance(job, dict):

                continue

            role = str(

                job.get(
                    "role",
                    job.get(
                        "title",
                        ""
                    )
                )

            ).strip()

            company = str(

                job.get(
                    "company",
                    ""
                )

            ).strip()

            if not role or not company:

                continue

            cleaned = {}

            cleaned["role"] = role
            cleaned["company"] = company

            cleaned["country"] = str(
                job.get(
                    "country",
                    cls.DEFAULTS["country"]
                )
            ).strip()

            cleaned["location"] = str(
                job.get(
                    "location",
                    cls.DEFAULTS["location"]
                )
            ).strip()

            cleaned["salary"] = str(
                job.get(
                    "salary",
                    cls.DEFAULTS["salary"]
                )
            ).strip()

            cleaned["source"] = str(
                job.get(
                    "source",
                    cls.DEFAULTS["source"]
                )
            ).strip()

            cleaned["description"] = str(
                job.get(
                    "description",
                    cls.DEFAULTS["description"]
                )
            ).strip()

            cleaned["apply_link"] = str(

                job.get(
                    "apply_link",
                    job.get(
                        "link",
                        cls.DEFAULTS["apply_link"]
                    )
                )

            ).strip()

            cleaned["executive_score"] = float(

                job.get(
                    "executive_score",
                    cls.DEFAULTS["executive_score"]
                )

            )

            cleaned["priority_score"] = float(

                job.get(
                    "priority_score",
                    cls.DEFAULTS["priority_score"]
                )

            )

            cleaned["jobhunter_score"] = float(

                job.get(
                    "jobhunter_score",
                    cls.DEFAULTS["jobhunter_score"]
                )

            )

            cleaned["visa_sponsorship"] = bool(

                job.get(
                    "visa_sponsorship",
                    cls.DEFAULTS["visa_sponsorship"]
                )

            )

            cleaned["posted_date"] = str(
                job.get(
                    "posted_date",
                    cls.DEFAULTS["posted_date"]
                )
            ).strip()

            cleaned["employment_type"] = str(
                job.get(
                    "employment_type",
                    cls.DEFAULTS["employment_type"]
                )
            ).strip()

            cleaned["experience_level"] = str(
                job.get(
                    "experience_level",
                    cls.DEFAULTS["experience_level"]
                )
            ).strip()

            cleaned["remote"] = bool(
                job.get(
                    "remote",
                    cls.DEFAULTS["remote"]
                )
            )

            validated.append(cleaned)

        return validated


if __name__ == "__main__":

    sample_jobs = [

        {
            "role": "Head of Sales",
            "company": "Microsoft",
            "country": "Singapore"
        },

        {
            "title": "Regional Director",
            "company": "Google"
        },

        {
            "role": "",
            "company": "Invalid Company"
        }

    ]

    result = JobValidator.validate_jobs(sample_jobs)

    print(f"\nValidated Jobs : {len(result)}\n")

    for job in result:

        print(job)