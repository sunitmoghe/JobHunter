import streamlit as st

from modules.profile_pipeline import process_resume
from modules.ai_resume_intelligence import AIResumeIntelligence
from modules.profile_manager import ProfileManager


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Resume Intelligence",
    page_icon="📄",
    layout="wide"
)


# --------------------------------------------------
# RESUME INTELLIGENCE
# --------------------------------------------------

st.title(
    "📄 Resume Intelligence Engine"
)

st.write(
    "Upload your resume and generate your Executive Profile."
)

uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)


if uploaded_resume:

    with open(
        "temp_resume.pdf",
        "wb"
    ) as f:

        f.write(
            uploaded_resume.getbuffer()
        )

    with st.spinner(
        "Analysing resume and creating executive profile..."
    ):

        profile = process_resume(
            "temp_resume.pdf"
        )

        # --------------------------------------------
        # SAVE PROFILE FOR ENTIRE APPLICATION
        # --------------------------------------------

        profile_manager = ProfileManager()

        profile_manager.save_profile(
            profile
        )

    st.success(
        "✅ Executive Profile Created Successfully"
    )

    st.info(
        "💾 Executive profile saved successfully for all JobHunter modules."
    )

    st.divider()

    # --------------------------------------------------
    # EXECUTIVE PROFILE
    # --------------------------------------------------

    st.subheader(
        "👤 Executive Profile"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "**Name:**",
            profile.get(
                "name",
                "Not Available"
            )
        )

        st.write(
            "**Email:**",
            profile.get(
                "email",
                "Not Available"
            )
        )

        st.write(
            "**Phone:**",
            profile.get(
                "phone",
                "Not Available"
            )
        )

        st.write(
            "**Experience:**",
            profile.get(
                "experience",
                "Not Available"
            )
        )

    with col2:

        st.write(
            "**LinkedIn:**",
            profile.get(
                "linkedin",
                "Not Available"
            )
        )

        st.write(
            "**Location:**",
            profile.get(
                "location",
                "Not Available"
            )
        )

        st.write(
            "**Current Role:**",
            profile.get(
                "current_role",
                "Not Available"
            )
        )

        st.write(
            "**Industry:**",
            profile.get(
                "industry",
                "Not Available"
            )
        )

    st.divider()

    # --------------------------------------------------
    # SKILLS
    # --------------------------------------------------

    st.subheader(
        "🛠 Skills Detected"
    )

    skills = profile.get(
        "skills",
        []
    )

    if skills:

        for skill in skills:

            st.success(
                skill
            )

    else:

        st.info(
            "No skills detected"
        )

    st.divider()

    # --------------------------------------------------
    # AI RESUME INTELLIGENCE
    # --------------------------------------------------

    st.subheader(
        "🧠 AI Executive Intelligence"
    )

    ai_engine = AIResumeIntelligence()

    ai_analysis = ai_engine.analyze_profile(
        profile
    )

    st.metric(
        "🎯 Executive Positioning Score",
        f"{ai_analysis['positioning_score']}%"
    )

    st.divider()

    st.subheader(
        "📝 Executive Summary"
    )

    st.info(
        ai_analysis["executive_summary"]
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "💪 Leadership Strengths"
        )

        for item in ai_analysis["leadership_strengths"]:

            st.success(
                item
            )

    with col2:

        st.subheader(
            "🚀 Recommended Executive Roles"
        )

        for role in ai_analysis["recommended_roles"]:

            st.write(
                "🔥",
                role
            )

    st.divider()

    st.subheader(
        "⚠ Keyword Improvement Areas"
    )

    for keyword in ai_analysis["keyword_gaps"]:

        st.warning(
            keyword
        )

    st.divider()

    st.subheader(
        "📊 Complete Profile Data"
    )

    st.json(
        profile
    )

else:

    st.info(
        "Please upload a PDF resume to begin analysis."
    )