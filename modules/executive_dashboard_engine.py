from modules.application_tracker import ApplicationTracker
from modules.recruiter_manager import RecruiterManager
from modules.profile_manager import ProfileManager
from modules.career_strategy_ai import CareerStrategyAI


class ExecutiveDashboardEngine:

    def __init__(self):

        self.applications = ApplicationTracker()
        self.recruiters = RecruiterManager()
        self.profile = ProfileManager()
        self.ai = CareerStrategyAI()

    def get_dashboard(self):

        if self.profile.profile_exists():
            profile = self.profile.load_profile()
        else:
            profile = {
                "experience": 20,
                "skills": []
            }

        strategy = self.ai.career_recommendation(profile)

        try:
            jobs = self.applications.load_applications()
        except Exception:
            jobs = []

        recruiters = self.recruiters.get_recruiters()

        return {

            "profile": profile,

            "strategy": strategy,

            "applications": jobs,

            "recruiters": recruiters,

            "executive_score":
                strategy["executive_score"]["overall_score"],

            "application_count":
                len(jobs),

            "recruiter_count":
                len(recruiters),

            "best_market":
                strategy["best_markets"][0]["country"]

        }