import streamlit as st

from modules.resume_parser import ResumeParser
from modules.ats_matcher import ATSMatcher


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="ATS Matcher",
    page_icon="🎯",
    layout="wide"
)


# --------------------------------------------------
# ATS MATCHER
# --------------------------------------------------

st.title(
    "🎯 ATS Resume Matcher"
)


st.write(
    "Compare your resume against any job description."
)


uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)


job_description = st.text_area(
    "Paste Job Description",
    height=300
)


if uploaded_resume and job_description:


    with open(
        "temp_resume.pdf",
        "wb"
    ) as f:

        f.write(
            uploaded_resume.getbuffer()
        )


    with st.spinner(
        "Calculating ATS match score..."
    ):


        parser = ResumeParser(
            "temp_resume.pdf"
        )


        resume_text = parser.read_resume()


        matcher = ATSMatcher(
            resume_text,
            job_description
        )


        result = matcher.calculate_match()


    st.success(
        "✅ ATS Analysis Completed"
    )


    st.divider()


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "ATS Match Score",
        f"{result.get('score',0)}%"
    )


    col2.metric(
        "Matched Skills",
        len(result.get("matched", []))
    )


    col3.metric(
        "Missing Skills",
        len(result.get("missing", []))
    )


    st.divider()


    left, right = st.columns(2)


    with left:

        st.subheader(
            "✅ Matching Skills"
        )


        for item in result.get(
            "matched",
            []
        ):

            if isinstance(item, dict):

                st.success(
                    f"{item.get('category')} → {item.get('skill')}"
                )

            else:

                st.success(
                    item
                )


    with right:

        st.subheader(
            "❌ Skill Gaps"
        )


        for item in result.get(
            "missing",
            []
        ):

            if isinstance(item, dict):

                st.error(
                    f"{item.get('category')} → {item.get('skill')}"
                )

            else:

                st.error(
                    item
                )


else:

    st.info(
        "Upload resume and paste job description to start ATS analysis."
    )