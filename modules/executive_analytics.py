import streamlit as st


def render_executive_analytics(jobs):

    if not jobs:
        return

    st.header("📊 Executive Analytics")

    total_jobs = len(jobs)

    avg_score = round(
        sum(job.get("executive_score", 0) for job in jobs) / total_jobs,
        1
    )

    visa_jobs = sum(
        1 for job in jobs
        if job.get("visa_sponsorship", False)
    )

    remote_jobs = sum(
        1 for job in jobs
        if job.get("remote_friendly", False)
    )

    fortune_jobs = sum(
        1 for job in jobs
        if job.get("fortune500", False)
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Executive Jobs", total_jobs)
    col2.metric("Average Fit", f"{avg_score}%")
    col3.metric("Visa Sponsorship", visa_jobs)
    col4.metric("Remote Jobs", remote_jobs)

    st.divider()