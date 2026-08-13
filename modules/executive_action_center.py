from datetime import datetime

from modules.application_tracker import ApplicationTracker
from modules.application_assistant import ApplicationAssistant


class ExecutiveActionCenter:

    def __init__(self):

        self.tracker = ApplicationTracker()

        self.assistant = ApplicationAssistant()

    # --------------------------------------------------
    # ACTION DECISION
    # --------------------------------------------------

    @staticmethod
    def determine_action(job):

        decision = str(
            job.get(
                "decision",
                job.get(
                    "recommendation",
                    ""
                )
            )
        ).upper()

        decision_score = ExecutiveActionCenter._number(
    	    job.get(
        	"decision_score",
            	job.get(
            	    "ranking_score",
            	    job.get(
                	"priority_score",
            		job.get(
                	    "executive_score",
                	    0
            		)
            	    )
        	)
    	    )
	)
        ranking_score = ExecutiveActionCenter._number(
            job.get(
                "ranking_score",
                job.get(
                    "priority_score",
                    0
                )
            )
        )

        if "PRIORITIZE" in decision:

            return {
                "action": "APPLY NOW",
                "priority": "CRITICAL",
                "next_action": "Prepare application package and apply immediately.",
            }

        if "APPLY" in decision:

            return {
                "action": "APPLY",
                "priority": "HIGH",
                "next_action": "Prepare tailored application package and apply.",
            }

        if "CONSIDER" in decision:

            return {
                "action": "REVIEW",
                "priority": "MEDIUM",
                "next_action": "Review job fit, salary and location before applying.",
            }

        if decision_score >= 85 or ranking_score >= 85:

            return {
                "action": "APPLY NOW",
                "priority": "CRITICAL",
                "next_action": "Prepare application package and apply immediately.",
            }

        if decision_score >= 75 or ranking_score >= 75:

            return {
                "action": "APPLY",
                "priority": "HIGH",
                "next_action": "Prepare tailored application package and apply.",
            }

        return {
            "action": "REVIEW",
            "priority": "MEDIUM",
            "next_action": "Review opportunity before applying.",
        }

    # --------------------------------------------------
    # BUILD ACTION RECORD
    # --------------------------------------------------

    def build_action(self, job):

        decision = self.determine_action(job)

        role = job.get(
            "role",
            job.get(
                "title",
                "Executive Position"
            )
        )

        company = job.get(
            "company",
            ""
        )

        country = job.get(
            "country",
            ""
        )

        return {

            "action_id": self._action_id(
                job
            ),

            "role": role,

            "company": company,

            "country": country,

            "location": job.get(
                "location",
                ""
            ),

            "decision": job.get(
                "decision",
                ""
            ),

            "decision_score": self._number(
    		job.get(
		    "decision_score",
        	job.get(
            	    "ranking_score",
            	job.get(
                    "priority_score",
                job.get(
                    "executive_score",
                    0
                )
            )
        )
    )
),
            "ranking_score": self._number(
                job.get(
                    "ranking_score",
                    job.get(
                        "priority_score",
                        0
                    )
                )
            ),

            "executive_score": self._number(
                job.get(
                    "executive_score",
                    0
                )
            ),

            "priority": decision[
                "priority"
            ],

            "action": decision[
                "action"
            ],

            "next_action": decision[
                "next_action"
            ],

            "apply_link": job.get(
                "apply_link",
                ""
            ),

            "visa_sponsorship": job.get(
                "visa_sponsorship",
                False
            ),

            "remote_friendly": job.get(
                "remote_friendly",
                job.get(
                    "remote",
                    False
                )
            ),

            "salary": job.get(
                "salary",
                ""
            ),

            "created_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),

        }

    # --------------------------------------------------
    # PREPARE APPLICATION PACKAGE
    # --------------------------------------------------

    def prepare_application_package(
        self,
        profile,
        job
    ):

        return self.assistant.generate_apply_package(
            profile,
            job
        )

    # --------------------------------------------------
    # MARK JOB AS APPLIED
    # --------------------------------------------------

    def apply(self, job):

        return self.tracker.mark_applied(
            job
        )

    # --------------------------------------------------
    # UPDATE APPLICATION STATUS
    # --------------------------------------------------

    def update_status(
        self,
        application_id,
        status
    ):

        return self.tracker.update_status(
            application_id,
            status
        )

    # --------------------------------------------------
    # GET APPLICATIONS
    # --------------------------------------------------

    def get_applications(self):

        return self.tracker.get_applications()

    # --------------------------------------------------
    # STATISTICS
    # --------------------------------------------------

    def statistics(self):

        return self.tracker.statistics()

    # --------------------------------------------------
    # TOP ACTIONS
    # --------------------------------------------------

    def prioritize(
        self,
        jobs,
        limit=20
    ):

        actions = [

            self.build_action(job)

            for job in jobs

        ]

        priority_order = {

            "CRITICAL": 0,
            "HIGH": 1,
            "MEDIUM": 2,
            "LOW": 3,
        }

        actions.sort(

            key=lambda item: (

                priority_order.get(
                    item["priority"],
                    9
                ),

                -item["decision_score"],

                -item["ranking_score"],

            )

        )

        return actions[:limit]

    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------

    @staticmethod
    def _number(value):

        try:

            return float(value)

        except (
            TypeError,
            ValueError
        ):

            return 0.0

    # --------------------------------------------------

    @staticmethod
    def _action_id(job):

        role = str(
            job.get(
                "role",
                job.get(
                    "title",
                    ""
                )
            )
        ).strip().lower()

        company = str(
            job.get(
                "company",
                ""
            )
        ).strip().lower()

        country = str(
            job.get(
                "country",
                ""
            )
        ).strip().lower()

        return (
            f"{company}|{role}|{country}"
        )


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    engine = ExecutiveActionCenter()

    sample_jobs = [

        {
            "role": "Head of Sales",
            "company": "Example Corp",
            "country": "Singapore",
            "decision": "PRIORITIZE",
            "decision_score": 90,
            "ranking_score": 92,
            "executive_score": 88,
            "apply_link": "https://example.com/apply",
        },

        {
            "role": "Sales Manager",
            "company": "Example India",
            "country": "India",
            "decision": "CONSIDER",
            "decision_score": 70,
            "ranking_score": 72,
            "executive_score": 68,
        },

    ]

    actions = engine.prioritize(
        sample_jobs
    )

    for index, action in enumerate(
        actions,
        start=1
    ):

        print(
            index,
            action["role"],
            "|",
            action["company"],
            "|",
            action["priority"],
            "|",
            action["action"],
            "|",
            action["decision_score"],
        )