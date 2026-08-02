import pandas as pd


class JobStatistics:

    def __init__(self, jobs):
        self.jobs = pd.DataFrame(jobs) if jobs else pd.DataFrame()

    def total_jobs(self):
        return len(self.jobs)

    def countries(self):
        if self.jobs.empty or "country" not in self.jobs.columns:
            return 0
        return self.jobs["country"].nunique()

    def companies(self):
        if self.jobs.empty or "company" not in self.jobs.columns:
            return 0
        return self.jobs["company"].nunique()

    def average_score(self):
        if self.jobs.empty:
            return 0

        score_column = None

        if "executive_score" in self.jobs.columns:
            score_column = "executive_score"
        elif "priority_score" in self.jobs.columns:
            score_column = "priority_score"

        if score_column is None:
            return 0

        return round(self.jobs[score_column].mean(), 1)

    def top_countries(self, top=10):
        if self.jobs.empty or "country" not in self.jobs.columns:
            return pd.DataFrame()

        return (
            self.jobs.groupby("country")
            .size()
            .reset_index(name="Jobs")
            .sort_values("Jobs", ascending=False)
            .head(top)
        )

    def top_companies(self, top=10):
        if self.jobs.empty or "company" not in self.jobs.columns:
            return pd.DataFrame()

        return (
            self.jobs.groupby("company")
            .size()
            .reset_index(name="Jobs")
            .sort_values("Jobs", ascending=False)
            .head(top)
        )

    def executive_distribution(self):
        if self.jobs.empty or "executive_role" not in self.jobs.columns:
            return pd.DataFrame()

        return (
            self.jobs.groupby("executive_role")
            .size()
            .reset_index(name="Jobs")
            .sort_values("Jobs", ascending=False)
        )