import pandas as pd


class JobFilter:

    def __init__(self, jobs):

        self.jobs = pd.DataFrame(jobs) if jobs else pd.DataFrame()

    def by_country(self, country):

        if self.jobs.empty:
            return []

        return self.jobs[
            self.jobs["country"] == country
        ].to_dict("records")

    def by_company(self, company):

        if self.jobs.empty:
            return []

        return self.jobs[
            self.jobs["company"].str.contains(
                company,
                case=False,
                na=False
            )
        ].to_dict("records")

    def minimum_score(self, score=80):

        if self.jobs.empty:
            return []

        score_column = None

        if "executive_score" in self.jobs.columns:
            score_column = "executive_score"

        elif "priority_score" in self.jobs.columns:
            score_column = "priority_score"

        if score_column is None:
            return self.jobs.to_dict("records")

        return self.jobs[
            self.jobs[score_column] >= score
        ].to_dict("records")

    def top_jobs(self, limit=20):

        if self.jobs.empty:
            return []

        score_column = None

        if "executive_score" in self.jobs.columns:
            score_column = "executive_score"

        elif "priority_score" in self.jobs.columns:
            score_column = "priority_score"

        if score_column is None:
            return self.jobs.head(limit).to_dict("records")

        return (
            self.jobs
            .sort_values(
                score_column,
                ascending=False
            )
            .head(limit)
            .to_dict("records")
        )