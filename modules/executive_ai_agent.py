from modules.unified_job_engine import UnifiedJobEngine
from modules.executive_config import EXECUTIVE_ROLES
from modules.executive_scoring_engine import ExecutiveScoringEngine


class ExecutiveAIAgent:

    def __init__(self):

        self.engine = UnifiedJobEngine()
        self.scoring = ExecutiveScoringEngine()

    def search_all_roles(self, max_roles=None):

        executive_jobs = []

        if max_roles is None:
            roles = EXECUTIVE_ROLES
        else:
            roles = EXECUTIVE_ROLES[:max_roles]

        for role in roles:

            try:

                print(f"Searching Executive Role: {role}")

                jobs = self.engine.search_jobs(role)

                for job in jobs:

                    job["executive_role"] = role

                    score_data = self.scoring.calculate_score(job)

                    executive_score = score_data["executive_fit"]

                    job["executive_score"] = executive_score
                    job["score_details"] = score_data

                    job["priority"] = self.get_priority(
                        executive_score
                    )

                    job["recommendation"] = self.get_recommendation(
                        executive_score
                    )

                    executive_jobs.append(job)

            except Exception as e:

                print(f"Error searching {role}: {e}")

        executive_jobs.sort(
            key=lambda x: x.get(
                "executive_score",
                0
            ),
            reverse=True
        )

        return executive_jobs

    def get_priority(self, score):

        if score >= 90:
            return "⭐⭐⭐⭐⭐ Critical"

        elif score >= 80:
            return "⭐⭐⭐⭐ High"

        elif score >= 70:
            return "⭐⭐⭐ Good"

        elif score >= 60:
            return "⭐⭐ Moderate"

        return "⭐ Low"

    def get_recommendation(self, score):

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

    jobs = agent.search_all_roles()

    print()
    print("=" * 80)
    print(f"TOTAL EXECUTIVE JOBS FOUND : {len(jobs)}")
    print("=" * 80)

    for job in jobs[:20]:

        print()

        print("Role :", job.get("role", "Unknown"))

        print("Company :", job.get("company", "Unknown"))

        print("Location :", job.get("location", "Unknown"))

        print("Executive Score :", job.get("executive_score"))

        print("Priority :", job.get("priority"))

        print("Recommendation :", job.get("recommendation"))