class ExecutivePerformanceEngine:

    def calculate(self, profile, jobs):

        experience = profile.get("experience", 23)

        if isinstance(experience, int):

            years = experience

        elif isinstance(experience, str):

            digits = "".join(c for c in experience if c.isdigit())

            years = int(digits) if digits else 23

        else:

            years = 23

        print(type(jobs))
        print(jobs)

        if isinstance(jobs, list):
            total_jobs = len(jobs)
        else:
            total_jobs = 0

        executive_score = 50 + min(years, 30)

        ats_score = min(95, 60 + years)

        interview_score = min(95, 55 + years)

        recruiter_score = min(95, 50 + total_jobs)

        market_score = min(95, 60 + (total_jobs // 2))

        readiness = round(
            (
                executive_score
                + ats_score
                + interview_score
                + recruiter_score
                + market_score
            ) / 5,
            1,
        )

        return {
            "Executive Score": executive_score,
            "ATS Readiness": ats_score,
            "Interview Readiness": interview_score,
            "Recruiter Reach": recruiter_score,
            "Global Market": market_score,
            "Overall Readiness": readiness,
        }