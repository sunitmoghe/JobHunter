import os
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
    "Upload Resume",
    type=["pdf", "docx", "doc"]
)

if uploaded_resume:

    extension = os.path.splitext(uploaded_resume.name)[1].lower()

    temp_file = f"temp_resume{extension}"

    with open(temp_file, "wb") as f:
        f.write(uploaded_resume.getbuffer())

    with st.spinner("Analysing resume..."):

        profile = process_resume(temp_file)

        ProfileManager().save_profile(profile)

    success_box("Executive Profile Created Successfully")

    info_box("Profile saved successfully.")

    divider()

    section_header("Executive Profile")

    left, right = st.columns(2)

    with left:
        st.write("**Name:**", profile.get("name",""))
        st.write("**Email:**", profile.get("email",""))
        st.write("**Phone:**", profile.get("phone",""))
        st.write("**Experience:**", profile.get("experience",""))

    with right:
        st.write("**LinkedIn:**", profile.get("linkedin",""))
        st.write("**Location:**", profile.get("location",""))
        st.write("**Current Role:**", profile.get("current_role",""))
        st.write("**Industry:**", profile.get("industry",""))

    divider()

    section_header("Skills")

    skills = profile.get("skills", [])

    if skills:

        cols = st.columns(3)

        for i, skill in enumerate(skills):
            with cols[i % 3]:
                success_box(skill)

    else:
        empty_state("No skills detected.")

    divider()

    ai = AIResumeIntelligence()

    result = ai.analyze_profile(profile)

    metric_row([
        ("Executive Positioning", f"{result['positioning_score']}%")
    ])

    divider()

    section_header("Executive Summary")

    info_box(result["executive_summary"])

    c1, c2 = st.columns(2)

    with c1:

        section_header("Leadership Strengths")

        for item in result["leadership_strengths"]:
            success_box(item)

    with c2:

        section_header("Recommended Roles")

        for role in result["recommended_roles"]:
            st.write("🔥", role)

    divider()

    section_header("Keyword Gaps")

    for item in result["keyword_gaps"]:
        warning_box(item)

    divider()

    with st.expander("Complete Executive Profile"):

         safe_profile = {}

    for k, v in profile.items():

        if isinstance(v, (str, int, float, bool, list, dict)) or v is None:

            safe_profile[k] = v

    st.json(safe_profile)

else:

    empty_state("Upload a PDF, DOCX or DOC resume.")