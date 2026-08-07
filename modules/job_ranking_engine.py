class JobRankingEngine:

    def __init__(self):

        self.source_weight = {

            "Adzuna": 100,
            "Greenhouse": 95,
            "Lever": 92,
            "Ashby": 90,
            "TheMuse": 88,
            "Remotive": 85,
            "RemoteOK": 82

        }

    # --------------------------------------------------

    def calculate_score(
        self,
        job
    ):

        score = 0

        score += job.get(
            "executive_score",
            0
        ) * 0.55

        score += job.get(
            "company_score",
            0
        ) * 0.10

        if job.get(
            "visa_sponsorship",
            False
        ):
            score += 8

        if job.get(
            "remote_friendly",
            False
        ):
            score += 5

        if job.get(
            "recruiter_found",
            False
        ):
            score += 5

        if job.get(
            "salary"
        ):
            score += 4

        score += (

            self.source_weight.get(

                job.get(
                    "source",
                    ""
                ),

                70

            )

            / 10

        )

        return round(
            min(score, 100),
            2
        )

    # --------------------------------------------------

    def rank_jobs(
        self,
        jobs
    ):

        for job in jobs:

            score = self.calculate_score(job)

            job["jobhunter_score"] = score

            job["priority_score"] = score

        jobs.sort(

            key=lambda x: (

                x.get(
                    "priority_score",
                    0
                ),

                x.get(
                    "executive_score",
                    0
                )

            ),

            reverse=True

        )

        return jobs