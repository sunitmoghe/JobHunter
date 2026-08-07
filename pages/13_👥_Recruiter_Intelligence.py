import streamlit as st
from modules.executive_ai_agent import ExecutiveAIAgent


st.set_page_config(
    page_title="Recruiter Intelligence",
    page_icon="👥",
    layout="wide",
)

st.title("👥 Recruiter Intelligence")


agent = ExecutiveAIAgent()

jobs = st.session_state.get("cached_jobs", [])

if not jobs:
    jobs = agent.search_all_roles(max_roles=20)
    st.session_state["cached_jobs"] = jobs

if not jobs:

    st.warning("No jobs found.")

    st.stop()

for job in jobs:

    recruiter = job.get("recruiter")

    with st.expander(
        f"{job.get('role','Executive Role')} • {job.get('company','Company')}",
        expanded=False,
    ):

        if recruiter:

            st.success("👤 Recruiter Found")

            st.write(recruiter)

        else:

            st.info("Recruiter data will be available in the next version.")

        st.write("### Job Details")

        st.write(f"**Company:** {job.get('company','Unknown')}")

        st.write(f"**Country:** {job.get('country','Unknown')}")

        st.write(f"**Executive Score:** {job.get('executive_score',0)}")

        st.write(f"**Priority:** {job.get('priority','Normal')}")

        if job.get("apply_link"):

            st.link_button(
                "🌍 Apply",
                job["apply_link"]
            )

        elif job.get("url"):

            st.link_button(
                "🌍 Apply",
                job["url"]
            )