import streamlit as st


def render_application_summary(
    saved_jobs_manager,
    job_cache,
):

    st.header("📌 Application Summary")

    saved_stats = saved_jobs_manager.statistics()

    cache_stats = job_cache.statistics()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Saved Jobs",
            saved_stats["saved_jobs"]
        )

    with col2:

        st.metric(
            "Cached Searches",
            cache_stats["cached_roles"]
        )

    with col3:

        st.metric(
            "Cache Expiry",
            f"{cache_stats['expiry_minutes']} min"
        )