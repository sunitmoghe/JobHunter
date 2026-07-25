from modules.unified_job_engine import UnifiedJobEngine
from modules.executive_config import EXECUTIVE_ROLES


class ExecutiveAIAgent:

    def __init__(self):
        self.engine = UnifiedJobEngine()

    def search_all_roles(self, max_roles=5):

        jobs = []

        for role in EXECUTIVE_ROLES[:max_roles]:

            print(f"Searching: {role}")

            results = self.engine.search_jobs(role)

            jobs.extend(results)

        return jobs


if __name__ == "__main__":

    agent = ExecutiveAIAgent()

    jobs = agent.search_all_roles()

    print()

    print("=" * 50)

    print(f"TOTAL EXECUTIVE JOBS FOUND : {len(jobs)}")