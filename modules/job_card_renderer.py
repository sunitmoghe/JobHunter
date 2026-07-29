import streamlit as st


class JobCardRenderer:

    def __init__(
        self,
        scoring_engine,
        priority_engine,
        skill_matcher,
        salary_engine,
        recruiter_engine,
        company_engine,
        resume_tailor,
        application_assistant,
        application_tracker,
        saved_jobs_manager,
    ):

        self.scoring_engine = scoring_engine
        self.priority_engine = priority_engine
        self.skill_matcher = skill_matcher
        self.salary_engine = salary_engine
        self.recruiter_engine = recruiter_engine
        self.company_engine = company_engine
        self.resume_tailor = resume_tailor
        self.application_assistant = application_assistant
        self.application_tracker = application_tracker
        self.saved_jobs_manager = saved_jobs_manager

    def render(
        self,
        job,
        index,
        profile,
    ):

        st.subheader(
            job.get(
                "role",
                job.get("title", "Executive Role")
            )
        )

        st.caption(
            f"{job.get('company','Unknown')} • "
            f"{job.get('location', job.get('country',''))}"
        )

        st.divider()

        company_col1, company_col2 = st.columns(2)

        with company_col1:

            st.write(
                f"⭐ Company Rating : {job.get('company_rating', 3)}/5"
            )

            if job.get("fortune500"):

                st.success("🏢 Fortune 500")

            else:

                st.info("🏢 Standard Company")

        with company_col2:

            if job.get("visa_sponsorship"):

                st.success("🌍 Visa Sponsorship")

            else:

                st.warning("No Visa Sponsorship")

            if job.get("remote_friendly"):

                st.success("🏠 Remote Friendly")

            st.write(
                f"📈 Hiring Trend : {job.get('hiring_trend', 'Unknown')}"
            )