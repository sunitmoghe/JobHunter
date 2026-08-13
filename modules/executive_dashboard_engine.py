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

        # ==================================================
        # PROFILE
        # ==================================================

        try:

            if self.profile.profile_exists():

                profile = (
                    self.profile.load_profile()
                )

            else:

                profile = {
                    "experience": 20,
                    "skills": [],
                }

        except Exception:

            profile = {
                "experience": 20,
                "skills": [],
            }


        # ==================================================
        # CAREER STRATEGY
        # ==================================================

        try:

            strategy = (
                self.ai.career_recommendation(
                    profile
                )
            )

        except Exception:

            strategy = {
                "executive_score": {
                    "overall_score": 0,
                },
                "best_markets": [],
                "strengths": [],
                "gaps": [],
                "action_plan": {},
            }


        # ==================================================
        # APPLICATIONS
        # ==================================================

        try:

            applications = (
                self.applications
                .load_applications()
            )

        except Exception:

            applications = []


        if not isinstance(
            applications,
            list,
        ):

            applications = []


        # ==================================================
        # RECRUITERS
        # ==================================================

        try:

            recruiters = (
                self.recruiters
                .get_all_recruiters()
            )

        except Exception:

            recruiters = []


        if not isinstance(
            recruiters,
            list,
        ):

            recruiters = []


        # ==================================================
        # EXECUTIVE SCORE
        # ==================================================

        executive_score = 0

        try:

            executive_score = (
                strategy
                .get(
                    "executive_score",
                    {}
                )
                .get(
                    "overall_score",
                    0
                )
            )

        except Exception:

            executive_score = 0


        # ==================================================
        # BEST MARKET
        # ==================================================

        best_market = "Not Available"

        try:

            markets = strategy.get(
                "best_markets",
                []
            )

            if markets:

                best_market = (
                    markets[0]
                    .get(
                        "country",
                        "Not Available"
                    )
                )

        except Exception:

            best_market = "Not Available"


        # ==================================================
        # RETURN DASHBOARD DATA
        # ==================================================

        return {

            "profile": profile,

            "strategy": strategy,

            "applications": applications,

            "recruiters": recruiters,

            "executive_score":
                executive_score,

            "application_count":
                len(applications),

            "recruiter_count":
                len(recruiters),

            "best_market":
                best_market,

        }