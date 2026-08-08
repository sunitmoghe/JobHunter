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

profile = profile_manager.load_profile()


if not profile:
    st.error(
        "Executive Profile is empty. Please save your profile first."
    )
    st.stop()


st.success("Executive Profile Loaded")


st.subheader("🎯 Target Position")


role = st.text_input(
    "Executive Role",
    value=str(
        profile.get(
            "current_role",
            "Head of Sales"
        )
    ),
)


company = st.text_input(
    "Company",
    value="Confidential",
)


job = {
    "role": role,
    "company": company,
}


skills = profile.get(
    "skills",
    []
)


if not isinstance(skills, list):
    skills = []


tailoring = {
    "recommended_keywords": skills
}


st.divider()


col1, col2 = st.columns(2)


with col1:

    st.subheader("👥 Recruiter Resume")

    recruiter_button = st.button(
        "Generate Recruiter Resume",
        type="primary",
        use_container_width=True,
    )


with col2:

    st.subheader("🏢 Hiring Manager Resume")

    hiring_manager_button = st.button(
        "Generate Hiring Manager Resume",
        type="primary",
        use_container_width=True,
    )


if recruiter_button:

    try:

        resume = generator.recruiter_resume(
            profile,
            job,
            tailoring,
        )

        st.session_state["generated_resume"] = resume
        st.session_state["resume_type"] = "Recruiter"

        st.success(
            "Recruiter Resume Generated"
        )

    except Exception as error:

        st.error(
            "Recruiter Resume generation failed."
        )

        st.exception(error)


if hiring_manager_button:

    try:

        resume = generator.hiring_manager_resume(
            profile,
            job,
            tailoring,
        )

        st.session_state["generated_resume"] = resume
        st.session_state["resume_type"] = "Hiring Manager"

        st.success(
            "Hiring Manager Resume Generated"
        )

    except Exception as error:

        st.error(
            "Hiring Manager Resume generation failed."
        )

        st.exception(error)


if "generated_resume" in st.session_state:

    resume = st.session_state[
        "generated_resume"
    ]

    resume_type = st.session_state.get(
        "resume_type",
        "Executive"
    )


    st.divider()

    st.subheader(
        f"📋 {resume_type} Resume"
    )


    st.markdown(
        "### Executive Summary"
    )

    st.write(
        resume.get(
            "executive_summary",
            ""
        )
    )


    st.markdown(
        "### Core Skills"
    )

    core_skills = resume.get(
        "core_skills",
        []
    )

    if isinstance(core_skills, list):

        st.write(
            " • ".join(
                str(skill)
                for skill in core_skills
            )
        )

    else:

        st.write(core_skills)


    st.markdown(
        "### Education"
    )

    education = resume.get(
        "education",
        []
    )

    if isinstance(education, list):

        for item in education:

            st.write(
                f"• {item}"
            )

    else:

        st.write(education)


    st.markdown(
        "### ATS Keywords"
    )

    st.write(
        resume.get(
            "ats_keywords",
            []
        )
    )


    st.caption(
        "Generated on: "
        + str(
            resume.get(
                "generated_on",
                ""
            )
        )
    )


st.success(
    "Resume Generator Ready"
)