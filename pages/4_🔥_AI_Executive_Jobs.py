import streamlit as st

from modules.executive_ai_agent import ExecutiveAIAgent
from modules.saved_jobs_manager import SavedJobsManager
from modules.application_manager import ApplicationManager


st.set_page_config(
    page_title="AI Executive Jobs",
    page_icon="🔥",
    layout="wide",
)


st.title("🔥 AI Executive Jobs")

st.caption(
    "AI-powered executive job discovery and scoring."
)


agent = ExecutiveAIAgent()
saved_manager = SavedJobsManager()
application_manager = ApplicationManager()


st.subheader("🎯 Search Executive Jobs")


role = st.text_input(
    "Executive Role",
    value="Head of Sales",
)


if st.button(
    "🔎 Search Executive Jobs",
    type="primary",
    use_container_width=True,
):

    with st.spinner(
        "Searching executive opportunities..."
    ):

        try:

            jobs = agent.search_jobs(
                role=role.strip()
            )

            st.session_state[
                "executive_jobs"
            ] = jobs

        except Exception as error:

            st.error(
                "Job search failed."
            )

            st.exception(error)


jobs = st.session_state.get(
    "executive_jobs",
    [],
)


st.divider()

st.subheader(
    f"📊 Results: {len(jobs)}"
)


if not jobs:

    st.info(
        "No jobs loaded yet."
    )

else:

    for index, job in enumerate(
        jobs,
        start=1,
    ):

        title = job.get(
            "title",
            job.get(
                "role",
                "Executive Position"
            )
        )

        company = job.get(
            "company",
            "Company"
        )

        location = job.get(
            "location",
            ""
        )

        score = job.get(
            "executive_score",
            0
        )

        apply_link = job.get(
            "apply_link",
            ""
        )

        if not apply_link:

            apply_link = job.get(
                "url",
                ""
            )

        if not apply_link:

            apply_link = job.get(
                "redirect_url",
                ""
            )


        with st.container(
            border=True
        ):

            st.markdown(
                f"### {index}. {title}"
            )

            st.write(
                f"**Company:** {company}"
            )

            if location:

                st.write(
                    f"**Location:** {location}"
                )

            st.metric(
                "Executive Fit",
                f"{score}%"
            )

            st.divider()


            col1, col2, col3 = st.columns(3)


            with col1:

                if apply_link:

                    if st.button(
                        "🚀 APPLY NOW",
                        key=f"apply_{index}",
                        use_container_width=True,
                    ):

                        application_manager.add_application(
                            job
                        )

                        st.success(
                            "Application recorded."
                        )

                        st.markdown(
                            f"[Open Job Application ↗]({apply_link})"
                        )

                else:

                    st.error(
                        "No application URL available."
                    )


            with col2:

                if st.button(
                    "💾 SAVE JOB",
                    key=f"save_{index}",
                    use_container_width=True,
                ):

                    saved = (
                        saved_manager.save_job(
                            job
                        )
                    )

                    if saved:

                        st.success(
                            "Job saved."
                        )

                    else:

                        st.info(
                            "Job already saved."
                        )


            with col3:

                if apply_link:

                    st.link_button(
                        "🔗 OPEN JOB",
                        apply_link,
                        use_container_width=True,
                    )


            description = job.get(
                "description",
                ""
            )

            if description:

                with st.expander(
                    "📄 Job Description"
                ):

                    st.write(
                        description
                    )