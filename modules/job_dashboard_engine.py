import pandas as pd


class JobDashboardEngine:

    def dashboard_metrics(self, jobs):

        if not jobs:
            return {}

        df = pd.DataFrame(jobs)

        metrics = {

            "total_jobs": len(df),

            "countries":
                df["country"].nunique()
                if "country" in df.columns
                else 0,

            "companies":
                df["company"].nunique()
                if "company" in df.columns
                else 0,

            "average_score":
                round(
                    df["executive_score"].mean(),
                    1
                )
                if "executive_score" in df.columns
                else 0,

            "high_priority":
                len(
                    df[
                        df["executive_score"] >= 80
                    ]
                )
                if "executive_score" in df.columns
                else 0

        }

        return metrics

    def country_summary(self, jobs):

        if not jobs:
            return pd.DataFrame()

        df = pd.DataFrame(jobs)

        if "country" not in df.columns:
            return pd.DataFrame()

        return (

            df.groupby("country")

            .size()

            .reset_index(
                name="Jobs"
            )

            .sort_values(
                "Jobs",
                ascending=False
            )

        )

    def company_summary(self, jobs):

        if not jobs:
            return pd.DataFrame()

        df = pd.DataFrame(jobs)

        if "company" not in df.columns:
            return pd.DataFrame()

        return (

            df.groupby("company")

            .size()

            .reset_index(
                name="Jobs"
            )

            .sort_values(
                "Jobs",
                ascending=False
            )

        )

    def priority_jobs(self, jobs):

        if not jobs:
            return []

        return sorted(

            jobs,

            key=lambda x:
                x.get(
                    "executive_score",
                    0
                ),

            reverse=True

        )