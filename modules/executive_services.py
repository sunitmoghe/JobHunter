from modules.company_intelligence import CompanyIntelligence
from modules.executive_salary_engine import ExecutiveSalaryEngine
from modules.duplicate_job_detector import DuplicateJobDetector
from modules.saved_jobs_manager import SavedJobsManager
from modules.executive_dashboard import ExecutiveDashboard


class ExecutiveServices:

    def __init__(self):

        self.company = CompanyIntelligence()

        self.salary = ExecutiveSalaryEngine()

        self.duplicate = DuplicateJobDetector()

        self.saved = SavedJobsManager()

        self.dashboard = ExecutiveDashboard()

    def enrich_jobs(self, jobs):

        jobs = self.company.enrich_jobs(jobs)

        jobs = self.salary.enrich_jobs(jobs)

        duplicate_result = self.duplicate.remove_duplicates(
            jobs
        )

        jobs = duplicate_result["jobs"]

        return {

            "jobs": jobs,

            "duplicates_removed":
                duplicate_result["duplicates_removed"],

            "final_jobs":
                duplicate_result["final_jobs"]

        }

    def dashboard_summary(self, jobs):

        saved = self.saved.load_jobs()

        return self.dashboard.generate(

            jobs,

            saved

        )

    def save_job(self, job):

        return self.saved.save_job(job)

    def saved_jobs(self):

        return self.saved.load_jobs()