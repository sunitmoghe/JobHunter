import streamlit as st

from modules.resume_parser import ResumeParser
from modules.ats_matcher import ATSMatcher


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI ATS Matcher",
    page_icon="🎯",
    layout="wide"
)


# --------------------------------------------------
# ATS MATCHER PAGE
# --------------------------------------------------

st.title(
    "🎯 AI ATS Resume Matcher"
)


st.write(
    "Upload your resume and compare it with any job description."
)


# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------

uploaded_resume = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)


# --------------------------------------------------
# JOB DESCRIPTION
# --------------------------------------------------

job_description = st.text_area(
    "Paste Job Description",
    height=300
)



# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

if uploaded_resume and job_description:


    with open(
        "temp_ats_resume.pdf",
        "wb"
    ) as f:

        f.write(
            uploaded_resume.getbuffer()
        )


    parser = ResumeParser(
        "temp_ats_resume.pdf"
    )


    resume_text = parser.read_resume()



    matcher = ATSMatcher(
        resume_text,
        job_description
    )


    result = matcher.calculate_match()



    st.divider()


    # --------------------------------------------------
    # ATS SCORE
    # --------------------------------------------------

    st.header(
        "🎯 ATS Compatibility Analysis"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "ATS Match Score",
            f"{result['score']}%"
        )


    with col2:

        st.metric(
            "🔥 Interview Probability",
            f"{result.get('interview_probability',0)}%"
        )


    with col3:

        readiness = (

            "High"

            if result.get(
                "interview_probability",
                0
            ) >= 80

            else "Medium"

        )


        st.metric(
            "🤖 AI Readiness",
            readiness
        )



    st.divider()



    # --------------------------------------------------
    # MATCHED SKILLS
    # --------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "✅ Matched Skills"
        )


        if result["matched"]:

            for item in result["matched"]:

                st.success(
                    f"{item['category']} → {item['skill']}"
                )

        else:

            st.info(
                "No matching skills found"
            )



    # --------------------------------------------------
    # MISSING SKILLS
    # --------------------------------------------------

    with col2:

        st.subheader(
            "⚠ Missing Keywords"
        )


        if result["missing"]:

            for item in result["missing"]:

                st.error(
                    f"{item['category']} → {item['skill']}"
                )

        else:

            st.success(
                "No major keyword gaps found"
            )



    st.divider()



    # --------------------------------------------------
    # AI RECOMMENDATIONS
    # --------------------------------------------------

    st.header(
        "📝 AI Resume Improvement Recommendations"
    )


    recommendations = result.get(
        "recommendations",
        []
    )


    if recommendations:


        for item in recommendations:

            st.warning(
                item
            )


    else:

        st.success(
            "Your resume already aligns strongly with this role."
        )



    st.divider()



    # --------------------------------------------------
    # RAW ANALYSIS
    # --------------------------------------------------

    with st.expander(
        "View Complete ATS Analysis"
    ):

        st.json(
            result
        )



else:


    st.info(
        "Please upload resume PDF and paste job description to start ATS analysis."
    )