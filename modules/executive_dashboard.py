import pandas as pd


class ExecutiveDashboardEngine:

    def __init__(self):
        pass

    def calculate_kpis(
        self,
        applications=None,
        recruiters=None,
        executive_score=0
    ):

        applications = applications or []
        recruiters = recruiters or []

        app_df = pd.DataFrame(applications)

        total_applications = len(app_df)

        interview_probability = 0
        priority_score = 0

        if (
            not app_df.empty
            and "interview_probability" in app_df.columns
        ):
            interview_probability = int(
                app_df["interview_probability"].mean()
            )

        if (
            not app_df.empty
            and "priority_score" in app_df.columns
        ):
            priority_score = int(
                app_df["priority_score"].mean()
            )

        recruiter_count = len(recruiters)

        momentum = int(
            (
                executive_score
                + min(total_applications * 2, 100)
                + min(recruiter_count * 5, 100)
            ) / 3
        )

        return {
            "applications": total_applications,
            "recruiters": recruiter_count,
            "executive_score": executive_score,
            "priority_score": priority_score,
            "interview_probability": interview_probability,
            "career_momentum": momentum,
        }

    def application_status_breakdown(
        self,
        applications
    ):

        if not applications:
            return {}

        df = pd.DataFrame(applications)

        if "status" not in df.columns:
            return {}

        return (
            df.groupby("status")
            .size()
            .to_dict()
        )

    def top_countries(
        self,
        applications,
        limit=10
    ):

        if not applications:
            return pd.DataFrame()

        df = pd.DataFrame(applications)

        if "country" not in df.columns:
            return pd.DataFrame()

        return (
            df.groupby("country")
            .size()
            .reset_index(name="Applications")
            .sort_values(
                "Applications",
                ascending=False
            )
            .head(limit)
        )

    def top_companies(
        self,
        applications,
        limit=10
    ):

        if not applications:
            return pd.DataFrame()

        df = pd.DataFrame(applications)

        if "company" not in df.columns:
            return pd.DataFrame()

        return (
            df.groupby("company")
            .size()
            .reset_index(name="Applications")
            .sort_values(
                "Applications",
                ascending=False
            )
            .head(limit)
        )


if __name__ == "__main__":

    engine = ExecutiveDashboardEngine()

    print(
        engine.calculate_kpis(
            applications=[],
            recruiters=[],
            executive_score=88
        )
    )