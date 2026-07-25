import streamlit as st
import pandas as pd
import plotly.express as px


from modules.resume_parser import ResumeParser
from modules.ats_matcher import ATSMatcher
from modules.profile_pipeline import process_resume

from modules.job_recommendation import get_recommendations

from modules.application_manager import ApplicationManager
from modules.application_analytics import ApplicationAnalytics


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Global Executive Job Hunter",
    page_icon="🌍",
    layout="wide"
)


st.title("🌍 Global Executive Job Hunter")


# --------------------------------------------------
# JOB DASHBOARD
# --------------------------------------------------

jobs = pd.DataFrame(
    [
        ["Head of Sales","Google","Singapore","35 min ago"],
        ["Country Manager","Microsoft","Germany","20 min ago"],
        ["VP Sales","Oracle","UAE","50 min ago"],
        ["Director Sales","SAP","Poland","15 min ago"],
        ["Business Development Director","Amazon","UK","45 min ago"],
        ["Chief Revenue Officer","Siemens","Saudi Arabia","30 min ago"],
    ],
    columns=[
        "Role",
        "Company",
        "Country",
        "Posted"
    ]
)


c1,c2,c3 = st.columns(3)

c1.metric(
    "Total Jobs",
    len(jobs)
)

c2.metric(
    "Countries",
    jobs["Country"].nunique()
)

c3.metric(
    "Companies",
    jobs["Company"].nunique()
)


st.divider()


role = st.selectbox(
    "Select Role",
    ["All"] + sorted(jobs["Role"].unique())
)


filtered_jobs = jobs.copy()


if role != "All":

    filtered_jobs = filtered_jobs[
        filtered_jobs["Role"] == role
    ]


st.dataframe(
    filtered_jobs,
    use_container_width=True
)


country_count = (
    filtered_jobs
    .groupby("Country")
    .size()
    .reset_index(name="Jobs")
)


fig = px.bar(
    country_count,
    x="Country",
    y="Jobs",
    title="Jobs by Country"
)


st.plotly_chart(
    fig,
    use_container_width=True
)



# --------------------------------------------------
# RESUME INTELLIGENCE
# --------------------------------------------------

st.divider()

st.header("📄 Resume Intelligence Engine")


uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)


profile = None


if uploaded_resume:


    with open(
        "temp_resume.pdf",
        "wb"
    ) as f:

        f.write(
            uploaded_resume.getbuffer()
        )


    profile = process_resume(
        "temp_resume.pdf"
    )


    st.success(
        "✅ Executive Profile Created and Stored"
    )


    st.info(
        "🗄️ Profile saved in JobHunter database"
    )


    st.subheader(
        "👤 Executive Profile"
    )


    col1,col2 = st.columns(2)


    with col1:

        st.write(
            "**Name:**",
            profile["name"]
        )

        st.write(
            "**Email:**",
            profile["email"]
        )

        st.write(
            "**Phone:**",
            profile["phone"]
        )


    with col2:

        st.write(
            "**Experience:**",
            profile["experience"]
        )

        st.write(
            "**LinkedIn:**",
            profile["linkedin"]
        )


    st.subheader(
        "🛠 Skills Detected"
    )


    for skill in profile["skills"]:

        st.success(skill)



# --------------------------------------------------
# ATS MATCHER
# --------------------------------------------------

st.divider()

st.header(
    "🎯 ATS Resume Matcher"
)


job_description = st.text_area(
    "Paste Job Description",
    height=250
)


if uploaded_resume and job_description:


    parser = ResumeParser(
        "temp_resume.pdf"
    )


    resume_text = parser.read_resume()


    matcher = ATSMatcher(
        resume_text,
        job_description
    )


    result = matcher.calculate_match()


    st.metric(
        "ATS Match Score",
        f"{result['score']}%"
    )


    col1,col2 = st.columns(2)


    with col1:

        st.subheader(
            "✅ Matched Skills"
        )

        for item in result["matched"]:

            st.success(
                f"{item['category']} → {item['skill']}"
            )


    with col2:

        st.subheader(
            "❌ Missing Skills"
        )

        for item in result["missing"]:

            st.error(
                f"{item['category']} → {item['skill']}"
            )



# --------------------------------------------------
# AI JOB RECOMMENDATIONS
# --------------------------------------------------

st.divider()

st.header(
    "🔥 AI Executive Job Recommendations"
)


recommendations = get_recommendations()


if recommendations:


    for job in recommendations:


        st.subheader(
            f"{job['role']} - {job['company']}"
        )


        st.write(
            f"🌍 Location: {job['country']}"
        )


        col1,col2 = st.columns(2)


        with col1:

            st.metric(
                "AI Match Score",
                f"{job['score']}%"
            )


        with col2:

            st.metric(
                "Priority Score",
                f"{job['priority_score']}%"
            )


        st.success(
            job["priority_category"]
        )


        a,b = st.columns(2)


        with a:

            st.write(
                "✅ Matching Skills"
            )

            for skill in job["matched"]:

                st.write(
                    "✓",
                    skill
                )


        with b:

            st.write(
                "⚠ Skill Gaps"
            )

            for skill in job["missing"]:

                st.write(
                    "△",
                    skill
                )


else:

    st.info(
        "No recommendations available"
    )



# --------------------------------------------------
# APPLICATION TRACKER
# --------------------------------------------------

st.divider()

st.header(
    "📌 Executive Application Tracker"
)


app_manager = ApplicationManager()


tab1,tab2 = st.tabs(
    [
        "➕ Add Application",
        "📊 View Applications"
    ]
)


with tab1:


    company = st.text_input(
        "Company"
    )

    role = st.text_input(
        "Role"
    )

    country = st.text_input(
        "Country"
    )

    location = st.text_input(
        "Location"
    )

    status = st.selectbox(
        "Status",
        [
            "Applied",
            "Recruiter Contacted",
            "Interview",
            "Offer",
            "Rejected"
        ]
    )


    if st.button(
        "Save Application"
    ):


        app_manager.add_application(
            company,
            role,
            country,
            location,
            status=status
        )


        st.success(
            "Application saved"
        )



with tab2:


    applications = (
        app_manager
        .get_applications()
    )


    if applications:


        df = pd.DataFrame(
            applications
        )


        st.dataframe(
            df,
            use_container_width=True
        )


    else:

        st.info(
            "No applications yet"
        )



# --------------------------------------------------
# ANALYTICS
# --------------------------------------------------

st.divider()

st.header(
    "📊 Application Intelligence Dashboard"
)


analytics = ApplicationAnalytics()


summary = analytics.get_summary()


c1,c2,c3,c4 = st.columns(4)


c1.metric(
    "Total",
    summary["total"]
)


c2.metric(
    "Applied",
    summary["statuses"].get(
        "Applied",
        0
    )
)


c3.metric(
    "Interview",
    summary["statuses"].get(
        "Interview",
        0
    )
)


c4.metric(
    "Offers",
    summary["statuses"].get(
        "Offer",
        0
    )
)


if summary["statuses"]:


    chart = pd.DataFrame(
        summary["statuses"].items(),
        columns=[
            "Status",
            "Count"
        ]
    )


    fig = px.bar(
        chart,
        x="Status",
        y="Count",
        title="Application Pipeline"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )