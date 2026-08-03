import streamlit as st


def render_jobs(
    jobs,
    profile,
    job_renderer,
):
    """
    Render Executive Job Cards
    """

    if not jobs:
        st.info("No jobs found.")
        return

    display_limit = st.selectbox(
        "Number of jobs",
        [10, 25, 50],
        index=2,
    )

    st.divider()

    for index, job in enumerate(jobs[:display_limit]):

        job_renderer.render(
            job,
            index,
            profile,
        )