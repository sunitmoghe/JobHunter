from datetime import datetime, timedelta

from modules.recruiter_manager import RecruiterManager
from modules.recruiter_intelligence_engine import (
    RecruiterIntelligenceEngine,
)
from modules.recruiter_outreach_ai import RecruiterOutreachAI


class ExecutiveRecruiterActionCenter:

    def __init__(self):

        self.manager = RecruiterManager()

        self.intelligence = (
            RecruiterIntelligenceEngine()
        )

        self.outreach = (
            RecruiterOutreachAI()
        )

    # --------------------------------------------------
    # RECRUITER PRIORITY
    # --------------------------------------------------

    def analyze_recruiter(
        self,
        recruiter,
    ):

        summary = (
            self.intelligence
            .get_recruiter_summary(
                recruiter
            )
        )

        score = (
            self.intelligence
            .recruiter_score(
                recruiter
            )
        )

        priority = (
            self.intelligence
            .recruiter_priority(
                recruiter
            )
        )

        return {
            "recruiter_score":
                score,

            "recruiter_priority":
                priority,

            "rating":
                summary.get(
                    "rating",
                    "",
                ),

            "response_rate":
                summary.get(
                    "response_rate",
                    "",
                ),

            "recommendation":
                summary.get(
                    "recommendation",
                    "",
                ),

            "linkedin":
                summary.get(
                    "linkedin",
                    recruiter.get(
                        "linkedin",
                        "",
                    ),
                ),
        }

    # --------------------------------------------------
    # PREPARE OUTREACH
    # --------------------------------------------------

    def prepare_outreach(
        self,
        profile,
        recruiter,
    ):

        connection = (
            self.outreach
            .generate_connection_message(
                profile,
                recruiter,
            )
        )

        follow_up = (
            self.outreach
            .generate_followup_message(
                recruiter,
            )
        )

        return {
            "connection_message":
                connection,

            "follow_up_message":
                follow_up,
        }

    # --------------------------------------------------
    # PREPARE RECRUITER ACTION
    # --------------------------------------------------

    def build_action(
        self,
        profile,
        recruiter,
        job=None,
    ):

        job = job or {}

        analysis = (
            self.analyze_recruiter(
                recruiter
            )
        )

        outreach = (
            self.prepare_outreach(
                profile,
                recruiter,
            )
        )

        role = job.get(
            "role",
            job.get(
                "title",
                "",
            ),
        )

        company = job.get(
            "company",
            recruiter.get(
                "company",
                "",
            ),
        )

        return {
            "recruiter_name":
                recruiter.get(
                    "name",
                    recruiter.get(
                        "recruiter_name",
                        "",
                    ),
                ),

            "company":
                company,

            "role":
                role,

            "recruiter_score":
                analysis[
                    "recruiter_score"
                ],

            "priority":
                analysis[
                    "recruiter_priority"
                ],

            "rating":
                analysis[
                    "rating"
                ],

            "response_rate":
                analysis[
                    "response_rate"
                ],

            "recommendation":
                analysis[
                    "recommendation"
                ],

            "linkedin":
                analysis[
                    "linkedin"
                ],

            "connection_message":
                outreach[
                    "connection_message"
                ],

            "follow_up_message":
                outreach[
                    "follow_up_message"
                ],

            "follow_up_date":
                self.calculate_follow_up_date(
                    recruiter
                ),
        }

    # --------------------------------------------------
    # FOLLOW-UP DATE
    # --------------------------------------------------

    @staticmethod
    def calculate_follow_up_date(
        recruiter,
        days=3,
    ):

        existing = str(
            recruiter.get(
                "follow_up_date",
                "",
            )
            or ""
        ).strip()

        if existing:
            return existing

        return (
            datetime.now()
            + timedelta(
                days=days
            )
        ).strftime(
            "%Y-%m-%d"
        )

    # --------------------------------------------------
    # UPDATE RECRUITER FOLLOW-UP
    # --------------------------------------------------

    def schedule_follow_up(
        self,
        recruiter_index,
        follow_up_date,
        status="Follow-up Required",
    ):

        return self.manager.update_recruiter(
            recruiter_index,
            {
                "follow_up_date":
                    follow_up_date,

                "follow_up_status":
                    status,
            },
        )

    # --------------------------------------------------
    # MARK CONTACTED
    # --------------------------------------------------

    def mark_contacted(
        self,
        recruiter_index,
        follow_up_date="",
    ):

        if not follow_up_date:

            follow_up_date = (
                self.calculate_follow_up_date(
                    {}
                )
            )

        return self.manager.update_recruiter(
            recruiter_index,
            {
                "follow_up_status":
                    "Contacted",

                "follow_up_date":
                    follow_up_date,
            },
        )

    # --------------------------------------------------
    # GET RECRUITERS
    # --------------------------------------------------

    def get_recruiters(self):

        return self.manager.get_all_recruiters()

    # --------------------------------------------------
    # PRIORITIZE RECRUITERS
    # --------------------------------------------------

    def prioritize_recruiters(
        self,
        profile,
        recruiters,
        job=None,
    ):

        actions = []

        for recruiter in recruiters:

            actions.append(
                self.build_action(
                    profile,
                    recruiter,
                    job,
                )
            )

        priority_order = {
            "High": 0,
            "Medium": 1,
            "Low": 2,
        }

        actions.sort(
            key=lambda item: (
                priority_order.get(
                    item["priority"],
                    9,
                ),
                -float(
                    item.get(
                        "recruiter_score",
                        0,
                    )
                ),
            )
        )

        return actions


# ------------------------------------------------------
# DIRECT TEST
# ------------------------------------------------------

if __name__ == "__main__":

    center = (
        ExecutiveRecruiterActionCenter()
    )

    profile = {
        "name": "Sunit Moghe",
        "experience": 23,
    }

    sample_recruiters = [
        {
            "name": "Senior Recruiter",
            "company": "Example Corp",
            "linkedin": "https://linkedin.com",
            "email": "",
            "score": 92,
            "rating": "4.8/5",
            "response_rate": "72%",
        },
        {
            "name": "Recruiter",
            "company": "Example Ltd",
            "score": 76,
        },
    ]

    sample_job = {
        "role": "Head of Sales",
        "company": "Example Corp",
    }

    actions = (
        center.prioritize_recruiters(
            profile,
            sample_recruiters,
            sample_job,
        )
    )

    print(
        "RECRUITER ACTIONS:",
        len(actions),
    )

    for index, action in enumerate(
        actions,
        start=1,
    ):

        print(
            index,
            "|",
            action["recruiter_name"],
            "|",
            action["company"],
            "|",
            action["priority"],
            "| Score:",
            action["recruiter_score"],
        )