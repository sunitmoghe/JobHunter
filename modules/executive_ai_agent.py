from modules.unified_job_engine import UnifiedJobEngine
from modules.executive_config import EXECUTIVE_ROLES
from modules.executive_scoring_engine import ExecutiveScoringEngine
from modules.parallel_search_engine import ParallelSearchEngine
from modules.job_cache import JobCache


class ExecutiveAIAgent:

    def __init__(self):

        self.engine = UnifiedJobEngine()

        self.parallel_engine = ParallelSearchEngine(
            self.engine
        )

        self.scoring = ExecutiveScoringEngine()

        self.cache = JobCache()

    def search_single_role(
        self,
        role
    ):

        cached_jobs = self.cache.get_jobs(role)

        if cached_jobs:

            print(f"✓ Using cache for {role}")

            return cached_jobs

        jobs = self.engine.search_jobs(role)

        for job in jobs:

            job["executive_role"] = role

            score_data = self.scoring.calculate_score(job)

            executive_score = score_data.get(
                "executive_fit",
                0
            )

            job["executive_score"] = executive_score

            job["score_details"] = score_data

            job["priority"] = self.get_priority(
                executive_score
            )

            job["recommendation"] = self.get_recommendation(
                executive_score
            )

        self.cache.save_jobs(
            role,
            jobs
        )

        return jobs

    def search_all_roles(
        self,
        max_roles=None
    ):

        if max_roles is None:

            roles = EXECUTIVE_ROLES

        else:

            roles = EXECUTIVE_ROLES[:max_roles]

        jobs = self.parallel_engine.search_roles(
            roles
        )

        executive_jobs = []

        for job in jobs:

            score_data = self.scoring.calculate_score(job)

            executive_score = score_data.get(
                "executive_fit",
                0
            )

            job["executive_score"] = executive_score

            job["score_details"] = score_data

            job["priority"] = self.get_priority(
                executive_score
            )

            job["recommendation"] = self.get_recommendation(
                executive_score
            )

            executive_jobs.append(job)

        executive_jobs.sort(

            key=lambda x: x.get(
                "executive_score",
                0
            ),

            reverse=True

        )

        return executive_jobs

    def clear_cache(self):

        self.cache.clear_cache()

    def get_priority(
        self,
        score
    ):

        if score >= 90:
            return "⭐⭐⭐⭐⭐ Critical"

        elif score >= 80:
            return "⭐⭐⭐⭐ High"

        elif score >= 70:
            return "⭐⭐⭐ Good"

        elif score >= 60:
            return "⭐⭐ Moderate"

        return "⭐ Low"

    def get_recommendation(
        self,
        score
    ):

        if score >= 90:

            return (
                "Excellent executive opportunity. Apply immediately."
            )

        elif score >= 80:

            return (
                "Strong match. Tailor your resume and apply."
            )

        elif score >= 70:

            return (
                "Good opportunity. Improve ATS keywords before applying."
            )

        elif score >= 60:

            return (
                "Possible opportunity. Resume tailoring recommended."
            )

        return (
            "Low executive fit. Consider only if strategically relevant."
        )


if __name__ == "__main__":

    agent = ExecutiveAIAgent()

    jobs = agent.search_all_roles(max_roles=5)

    print("=" * 60)

    print(f"Jobs Found : {len(jobs)}")

    print("=" * 60)

    for job in jobs[:10]:

        print(
            job.get("role"),
            "|",
            job.get("company"),
            "|",
            job.get("executive_score")
        )