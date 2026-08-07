import streamlit as st

from modules.profile_manager import ProfileManager
from modules.resume_generator import ResumeGenerator

st.set_page_config(
    page_title="Resume Generator",
    page_icon="📝",
    layout="wide",
)

st.title("📝 AI Executive Resume Generator")

profile_manager = ProfileManager()
generator = ResumeGenerator()

if not profile_manager.profile_exists():

    st.warning("Please create your Executive Profile first.")

    st.stop()

profile = profile_manager.load_profile()

st.success("Executive Profile Loaded")

st.subheader("Target Position")

role = st.text_input(
    "Executive Role",
    value="Head of Sales"
)

company = st.text_input(
    "Company",
    value="Confidential"
)

job = {

    "role": role,

    "company": company

}

tailoring = {

    "recommended_keywords": [

        "Leadership",

        "Revenue Growth",

        "Strategic Sales",

        "P&L",

        "Business Development"

    ]

}

col1, col2 = st.columns(2)

with col1:

    if st.button("Generate Recruiter Resume"):

        resume = generator.recruiter_resume(
            profile,
            job,
            tailoring
        )

        st.success("Recruiter Resume Generated")

        st.json(resume)

with col2:

    if st.button("Generate Hiring Manager Resume"):

        resume = generator.hiring_manager_resume(
            profile,
            job,
            tailoring
        )

        st.success("Hiring Manager Resume Generated")

        st.json(resume)

st.success("Resume Generator Ready")