import streamlit as st


def render_cache_management(
    job_cache,
    saved_jobs_manager,
):

    st.header("⚡ Search Cache")

    saved_jobs = saved_jobs_manager.load_jobs()

    cache_col1, cache_col2 = st.columns(2)

    with cache_col1:

        if st.button("♻ Refresh Cache"):

            job_cache.clear_cache()

            st.success(
                "Search cache cleared."
            )

    with cache_col2:

        if st.button(
            "🗑 Clear Saved Jobs"
        ):

            for job in saved_jobs.copy():

                saved_jobs_manager.remove_job(

                    job.get("company", ""),

                    job.get(
                        "role",
                        job.get(
                            "title",
                            ""
                        )
                    ),

                    job.get(
                        "location",
                        ""
                    )

                )

            st.success(
                "Saved jobs removed."
            )

            st.rerun()