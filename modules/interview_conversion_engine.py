from datetime import datetime

from modules.application_tracker import ApplicationTracker
from modules.interview_coach_ai import InterviewCoachAI


class InterviewConversionEngine:

    VALID_OUTCOMES = [
        "Scheduled",
        "Completed",
        "Next Round",
        "Offer",
        "Rejected",
        "Withdrawn",
    ]

    def __init__(self):

        self.tracker = ApplicationTracker()
        self.coach = InterviewCoachAI()

    # ==========================================================
    # APPLICATION LOOKUP
    # ==========================================================

    def get_application(
        self,
        application_id,
    ):

        applications = (
            self.tracker.load_applications()
        )

        for application in applications:

            if application.get(
                "application_id"
            ) == application_id:

                return application

        return None

    # ==========================================================
    # PREPARE INTERVIEW
    # ==========================================================

    def prepare_interview(
        self,
        profile,
        application,
    ):

        job = {
            "role":
                application.get(
                    "role",
                    "",
                ),

            "company":
                application.get(
                    "company",
                    "",
                ),
        }

        questions = (
            self.coach.generate_questions(
                job
            )
        )

        return {
            "application_id":
                application.get(
                    "application_id",
                    "",
                ),

            "role":
                job["role"],

            "company":
                job["company"],

            "questions":
                questions,
        }

    # ==========================================================
    # SCHEDULE INTERVIEW
    # ==========================================================

    def schedule_interview(
        self,
        application_id,
        interview_date,
        interview_stage="First Round",
    ):

        applications = (
            self.tracker.load_applications()
        )

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )

        for application in applications:

            if application.get(
                "application_id"
            ) != application_id:

                continue

            application[
                "status"
            ] = "Interview"

            application[
                "interview_date"
            ] = interview_date

            application[
                "interview_stage"
            ] = interview_stage

            application[
                "last_updated"
            ] = now

            application.setdefault(
                "history",
                []
            ).append(
                {
                    "date":
                        now,

                    "status":
                        "Interview",

                    "stage":
                        interview_stage,
                }
            )

            self.tracker.save_applications(
                applications
            )

            return True

        return False

    # ==========================================================
    # RECORD INTERVIEW RESULT
    # ==========================================================

    def record_interview_result(
        self,
        application_id,
        outcome,
        interview_score=None,
        feedback="",
    ):

        if outcome not in self.VALID_OUTCOMES:

            return False

        applications = (
            self.tracker.load_applications()
        )

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )

        for application in applications:

            if application.get(
                "application_id"
            ) != application_id:

                continue

            application[
                "status"
            ] = outcome

            application[
                "last_updated"
            ] = now

            if interview_score is not None:

                try:

                    interview_score = float(
                        interview_score
                    )

                    interview_score = max(
                        0,
                        min(
                            100,
                            interview_score
                        )
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    interview_score = None

            if interview_score is not None:

                application[
                    "interview_score"
                ] = interview_score

            if feedback:

                application[
                    "interview_feedback"
                ] = str(
                    feedback
                ).strip()

            if outcome == "Offer":

                application[
                    "offer_date"
                ] = datetime.now().strftime(
                    "%Y-%m-%d"
                )

            application.setdefault(
                "history",
                []
            ).append(
                {
                    "date":
                        now,

                    "status":
                        outcome,

                    "interview_score":
                        interview_score,

                    "feedback":
                        feedback,
                }
            )

            self.tracker.save_applications(
                applications
            )

            return True

        return False

    # ==========================================================
    # EVALUATE INTERVIEW ANSWER
    # ==========================================================

    def evaluate_answer(
        self,
        question,
        answer,
    ):

        return self.coach.evaluate_answer(
            answer
        )

    # ==========================================================
    # GENERATE STAR ANSWER
    # ==========================================================

    def generate_star_answer(
        self,
        question,
        profile,
    ):

        return self.coach.generate_star_answer(
            question,
            profile,
        )

    # ==========================================================
    # CONVERSION SUMMARY
    # ==========================================================

    def conversion_summary(self):

        applications = (
            self.tracker.load_applications()
        )

        total = len(
            applications
        )

        applied = 0
        interview = 0
        offer = 0
        rejected = 0
        withdrawn = 0
        next_round = 0

        interview_scores = []

        for application in applications:

            status = str(
                application.get(
                    "status",
                    "",
                )
            ).lower()

            if status == "applied":
                applied += 1

            elif status == "interview":
                interview += 1

            elif status == "offer":
                offer += 1

            elif status == "rejected":
                rejected += 1

            elif status == "withdrawn":
                withdrawn += 1

            elif status == "next round":
                next_round += 1

            score = application.get(
                "interview_score"
            )

            if score is not None:

                try:

                    interview_scores.append(
                        float(score)
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    pass

        interview_rate = (
            round(
                (
                    interview
                    + next_round
                    + offer
                )
                / total
                * 100,
                2,
            )
            if total
            else 0
        )

        offer_rate = (
            round(
                offer
                / total
                * 100,
                2,
            )
            if total
            else 0
        )

        interview_to_offer = (
            round(
                offer
                / interview
                * 100,
                2,
            )
            if interview
            else 0
        )

        average_interview_score = (
            round(
                sum(
                    interview_scores
                )
                / len(
                    interview_scores
                ),
                2,
            )
            if interview_scores
            else 0
        )

        return {

            "total":
                total,

            "applied":
                applied,

            "interview":
                interview,

            "next_round":
                next_round,

            "offer":
                offer,

            "rejected":
                rejected,

            "withdrawn":
                withdrawn,

            "interview_rate":
                interview_rate,

            "offer_rate":
                offer_rate,

            "interview_to_offer":
                interview_to_offer,

            "average_interview_score":
                average_interview_score,
        }

    # ==========================================================
    # FUNNEL
    # ==========================================================

    def funnel(self):

        summary = (
            self.conversion_summary()
        )

        return [
            {
                "stage":
                    "Applications",

                "count":
                    summary["total"],
            },
            {
                "stage":
                    "Interviews",

                "count":
                    summary["interview"],
            },
            {
                "stage":
                    "Next Round",

                "count":
                    summary["next_round"],
            },
            {
                "stage":
                    "Offers",

                "count":
                    summary["offer"],
            },
        ]


# ==========================================================
# DIRECT TEST
# ==========================================================

if __name__ == "__main__":

    engine = (
        InterviewConversionEngine()
    )

    print(
        "Interview Conversion Engine: OK"
    )

    print(
        "Conversion Summary:"
    )

    print(
        engine.conversion_summary()
    )

    print()

    print(
        "Application Funnel:"
    )

    for stage in engine.funnel():

        print(
            stage["stage"],
            "|",
            stage["count"],
        )