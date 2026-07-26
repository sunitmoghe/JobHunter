import streamlit as st

from modules.profile_pipeline import process_resume
from modules.ai_resume_intelligence import AIResumeIntelligence
from modules.profile_manager import ProfileManager

from modules.ui_components import (
    page_header,
    section_header,
    success_box,
    info_box,
    warning_box,
    metric_row,
    divider,
    empty_state,
)

st.set_page_config(
    page_title="Resume Intelligence",
    page_icon="📄",
    layout="wide",
)

page_header(
    "📄 Resume Intelligence Engine",
    "Upload your resume to generate your Executive Profile."
)

uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"],
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

        profile_manager = ProfileManager()

        profile_manager.save_profile(
            profile
        )

    success_box(
        "✅ Executive Profile Created Successfully"
    )

    info_box(
        "💾 Executive profile saved successfully for all JobHunter modules."
    )

    divider()

    section_header(
        "👤 Executive Profile"
    )

    left, right = st.columns(2)

    with left:

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

    with right:

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

    divider()

    section_header(
        "🛠 Skills Detected"
    )

    skills = profile.get(
        "skills",
        []
    )

    if skills:

        cols = st.columns(3)

        for index, skill in enumerate(skills):

            with cols[index % 3]:

                success_box(skill)

    else:

        empty_state(
            "No skills detected."
        )

    divider()

    section_header(
        "🧠 AI Executive Intelligence"
    )

    ai_engine = AIResumeIntelligence()

    ai_analysis = ai_engine.analyze_profile(
        profile
    )

    metric_row(
        [
            (
                "Executive Positioning",
                f"{ai_analysis['positioning_score']}%"
            )
        ]
    )

    divider()

    section_header(
        "📝 Executive Summary"
    )

    info_box(
        ai_analysis["executive_summary"]
    )

    left, right = st.columns(2)

    with left:

        section_header(
            "💪 Leadership Strengths"
        )

        for item in ai_analysis[
            "leadership_strengths"
        ]:

            success_box(item)

    with right:

        section_header(
            "🚀 Recommended Executive Roles"
        )

        for role in ai_analysis[
            "recommended_roles"
        ]:

            st.write(
                "🔥",
                role
            )

    divider()

    section_header(
        "⚠ Keyword Improvement Areas"
    )

    for keyword in ai_analysis[
        "keyword_gaps"
    ]:

        warning_box(keyword)

    divider()

    with st.expander(
        "📊 Complete Executive Profile"
    ):

        st.json(
            profile
        )

else:

    empty_state(
        "Please upload a PDF resume to begin analysis."
    )