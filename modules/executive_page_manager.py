import streamlit as st

from modules.executive_ai_agent import ExecutiveAIAgent
from modules.executive_services import ExecutiveServices


class ExecutivePageManager:

    def __init__(self):

        self.agent = ExecutiveAIAgent()

        self.services = ExecutiveServices()

    def show_dashboard(self, dashboard):

        st.subheader("📊 Executive Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Jobs Found",
                dashboard["total_jobs"]
            )

        with col2:
            st.metric(
                "Saved Jobs",
                dashboard["saved_jobs"]
            )

        with col3:
            st.metric(
                "Average Score",
                dashboard["average_score"]
            )

        with col4:
            st.metric(
                "High Priority",
                dashboard["high_priority_jobs"]
            )

    def show_jobs(self, jobs):

        st.subheader("🌍 Executive Opportunities")

        for job in jobs:

            with st.expander(

                f"{job.get('role','Unknown')} | "
                f"{job.get('company','Unknown')}"

            ):

                st.write(
                    "**Location:**",
                    job.get("location", "Unknown")
                )

                st.write(
                    "**Executive Score:**",
                    job.get(
                        "executive_score",
                        0
                    )
                )

                st.write(
                    "**Company Rating:**",
                    job.get(
                        "company_rating",
                        "-"
                    )
                )

                salary = job.get(
                    "salary_estimate",
                    {}
                )

                if salary.get("available"):

                    st.write(

                        "**Estimated Salary:**",

                        f"{salary['minimum']} - "

                        f"{salary['maximum']}"

                    )

                st.write(

                    "**Visa Sponsorship:**",

                    "✅"

                    if job.get(
                        "visa_sponsorship",
                        False
                    )

                    else "❌"

                )

                if st.button(

                    "⭐ Save Job",

                    key=f"save_{id(job)}"

                ):

                    saved = self.services.save_job(job)

                    if saved:

                        st.success(
                            "Job saved."
                        )

                    else:

                        st.info(
                            "Already saved."
                        )

    def run(self):

        st.title(
            "🌍 AI Executive Jobs"
        )

        if st.button(

            "🚀 Search Global Executive Jobs"

        ):

            with st.spinner(

                "Searching Executive Jobs..."

            ):

                jobs = self.agent.search_all_roles()

                result = self.services.enrich_jobs(
                    jobs
                )

                jobs = result["jobs"]

                dashboard = self.services.dashboard_summary(
                    jobs
                )

                self.show_dashboard(
                    dashboard
                )

                st.success(

                    f"Duplicates Removed: "

                    f"{result['duplicates_removed']}"

                )

                self.show_jobs(
                    jobs
                )


if __name__ == "__main__":

    ExecutivePageManager().run()