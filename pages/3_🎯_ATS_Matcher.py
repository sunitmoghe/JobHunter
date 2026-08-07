import os
import streamlit as st

from modules.resume_parser import ResumeParser
from modules.ats_matcher import ATSMatcher

from modules.ui_components import (
    page_header,
    section_header,
    metric_row,
    success_box,
    warning_box,
    info_box,
    error_box,
    divider,
    empty_state,
)

st.set_page_config(
    page_title="AI ATS Matcher",
    page_icon="🎯",
    layout="wide",
)

page_header(
    "🎯 AI ATS Resume Matcher",
    "Upload your resume and compare it with any executive job description."
)

uploaded_resume = st.file_uploader(
    "Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"],
)

job_description = st.text_area(
    "Paste Job Description",
    height=300,
)

if uploaded_resume and job_description:

    extension = os.path.splitext(
        uploaded_resume.name
    )[1].lower()

    temp_resume = f"temp_ats_resume{extension}"

    with open(
        temp_resume,
        "wb"
    ) as f:

        f.write(
            uploaded_resume.getbuffer()
        )

    parser = ResumeParser(
        temp_resume
    )

    resume_text = parser.read_resume()

    matcher = ATSMatcher(
        resume_text,
        job_description
    )

    result = matcher.calculate_match()

    divider()

    section_header(
        "🎯 ATS Compatibility Analysis"
    )

    readiness = (
        "High"
        if result.get(
            "interview_probability",
            0
        ) >= 80
        else "Medium"
    )

    metric_row(
        [
            (
                "ATS Match Score",
                f"{result['score']}%"
            ),
            (
                "Interview Probability",
                f"{result.get('interview_probability',0)}%"
            ),
            (
                "AI Readiness",
                readiness
            ),
        ]
    )

    divider()

    left, right = st.columns(2)

    with left:

        section_header(
            "✅ Matched Skills"
        )

        if result.get("matched"):

            for item in result["matched"]:

                success_box(
                    f"{item['category']} → {item['skill']}"
                )

        else:

            empty_state(
                "No matching skills found."
            )

    with right:

        section_header(
            "⚠ Missing Keywords"
        )

        if result.get("missing"):

            for item in result["missing"]:

                error_box(
                    f"{item['category']} → {item['skill']}"
                )

        else:

            success_box(
                "No major keyword gaps found."
            )

    divider()

    section_header(
        "📝 AI Resume Improvement Recommendations"
    )

    recommendations = result.get(
        "recommendations",
        []
    )

    if recommendations:

        for recommendation in recommendations:

            warning_box(
                recommendation
            )

    else:

        success_box(
            "Your resume already aligns strongly with this role."
        )

    divider()

    with st.expander(
        "📊 Complete ATS Analysis"
    ):

        st.json(
            result
        )

else:

    info_box(
        "Please upload a PDF or DOCX resume and paste a job description to begin ATS analysis."
    )