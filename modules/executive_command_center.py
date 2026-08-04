import streamlit as st


def render_command_center(

    jobs,

    saved_jobs,

    applied_jobs,

    ats_scores,

):

    st.header("🧠 Executive Command Center")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Jobs Found", len(jobs))

    with col2:
        st.metric("Saved Jobs", saved_jobs)

    with col3:
        st.metric("Applications", applied_jobs)

    with col4:

        if ats_scores:

            avg = round(sum(ats_scores) / len(ats_scores), 1)

        else:

            avg = 0

        st.metric("Average ATS", f"{avg}%")