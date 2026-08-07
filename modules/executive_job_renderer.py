import streamlit as st


def render_jobs(
    jobs,
    profile,
    job_renderer,
):

    if not jobs:

        st.warning("No jobs found.")
        return

    st.success(f"Loaded {len(jobs)} jobs")

    display_limit = st.selectbox(

        "Number of jobs",

        [10, 25, 50],

        index=2,

    )

    st.divider()

    for index, job in enumerate(jobs[:display_limit]):

        try:

            job_renderer.render(

                job,

                index,

                profile,

            )

        except Exception as e:

            st.error(

                f"Error rendering job card:\n\n"
                f"{job.get('role','Unknown')} | "
                f"{job.get('company','Unknown')}\n\n"
                f"{e}"

            )