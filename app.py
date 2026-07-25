import streamlit as st
import pandas as pd
import plotly.express as px


from modules.resume_parser import ResumeParser
from modules.ats_matcher import ATSMatcher
from modules.profile_pipeline import process_resume

from modules.job_recommendation import get_recommendations

from modules.executive_ai_agent import ExecutiveAIAgent
from modules.priority_engine import PriorityEngine

from modules.application_manager import ApplicationManager
from modules.application_analytics import ApplicationAnalytics


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Global Executive Job Hunter",
    page_icon="🌍",
    layout="wide"
)


st.title(
    "🌍 Global Executive Job Hunter"
)


# ==================================================
# JOB DASHBOARD
# ==================================================

st.header(
    "📊 Executive Job Dashboard"
)


jobs = pd.DataFrame(
    [
        ["Head of Sales","Google","Singapore"],
        ["Country Manager","Microsoft","Germany"],
        ["VP Sales","Oracle","UAE"],
        ["Director Sales","SAP","Poland"],
        ["Business Development Director","Amazon","UK"],
        ["Chief Revenue Officer","Siemens","Saudi Arabia"],
    ],
    columns=[
        "Role",
        "Company",
        "Country"
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


selected_role = st.selectbox(
    "Select Role",
    [
        "All"
    ]
    +
    sorted(
        jobs["Role"].unique()
    )
)


filtered_jobs = jobs.copy()


if selected_role != "All":

    filtered_jobs = filtered_jobs[
        filtered_jobs["Role"] == selected_role
    ]


st.dataframe(
    filtered_jobs,
    use_container_width=True
)


chart_data = (
    filtered_jobs
    .groupby("Country")
    .size()
    .reset_index(name="Jobs")
)


fig = px.bar(
    chart_data,
    x="Country",
    y="Jobs",
    title="Jobs by Country"
)


st.plotly_chart(
    fig,
    use_container_width=True
)



# ==================================================
# RESUME INTELLIGENCE
# ==================================================

st.divider()

st.header(
    "📄 Resume Intelligence Engine"
)


uploaded_resume = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)


if uploaded_resume:


    with open(
        "temp_resume.pdf",
        "wb"
    ) as file:

        file.write(
            uploaded_resume.getbuffer()
        )


    profile = process_resume(
        "temp_resume.pdf"
    )


    st.success(
        "✅ Executive Profile Created"
    )


    st.subheader(
        "👤 Executive Profile"
    )


    col1,col2 = st.columns(2)


    with col1:

        st.write(
            "Name:",
            profile.get(
                "name",
                ""
            )
        )

        st.write(
            "Email:",
            profile.get(
                "email",
                ""
            )
        )

        st.write(
            "Phone:",
            profile.get(
                "phone",
                ""
            )
        )


    with col2:

        st.write(
            "Experience:",
            profile.get(
                "experience",
                ""
            )
        )

        st.write(
            "LinkedIn:",
            profile.get(
                "linkedin",
                ""
            )
        )


    st.subheader(
        "🛠 Skills Detected"
    )


    for skill in profile.get(
        "skills",
        []
    ):

        st.success(
            skill
        )
# ==================================================
# ATS RESUME MATCHER
# ==================================================

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


        for item in result.get(
            "matched",
            []
        ):

            st.success(
                f"{item['category']} → {item['skill']}"
            )


    with col2:

        st.subheader(
            "❌ Missing Skills"
        )


        for item in result.get(
            "missing",
            []
        ):

            st.error(
                f"{item['category']} → {item['skill']}"
            )



# ==================================================
# AI JOB RECOMMENDATIONS
# ==================================================

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
            "🌍 Country:",
            job.get(
                "country",
                "Global"
            )
        )


        col1,col2 = st.columns(2)


        with col1:

            st.metric(
                "AI Match Score",
                f"{job.get('score',0)}%"
            )


        with col2:

            st.metric(
                "Priority Score",
                f"{job.get('priority_score',0)}%"
            )


        st.success(
            job.get(
                "priority_category",
                "Review"
            )
        )


        a,b = st.columns(2)


        with a:

            st.write(
                "✅ Matching Skills"
            )


            for skill in job.get(
                "matched",
                []
            ):

                st.write(
                    "✓",
                    skill
                )


        with b:

            st.write(
                "⚠ Skill Gaps"
            )


            for skill in job.get(
                "missing",
                []
            ):

                st.write(
                    "△",
                    skill
                )


        st.divider()


else:

    st.info(
        "No AI recommendations available"
    )



# ==================================================
# APPLICATION TRACKER
# ==================================================

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
# ==================================================
# LIVE GLOBAL EXECUTIVE JOB SEARCH
# ==================================================

st.divider()

st.header(
    "🌍 Live Global Executive Job Search"
)


if st.button(
    "🚀 Search Global Executive Jobs"
):


    with st.spinner(
        "AI Agent searching executive opportunities..."
    ):


        agent = ExecutiveAIAgent()

        executive_jobs = (
            agent.search_all_roles()
        )


    if executive_jobs:


        st.success(
            f"Found {len(executive_jobs)} executive jobs"
        )


        priority_engine = PriorityEngine()


        for job in executive_jobs[:25]:


            role = job.get(
                "role",
                job.get(
                    "title",
                    "Executive Role"
                )
            )


            company = job.get(
                "company",
                "Not Available"
            )


            country = job.get(
                "country",
                job.get(
                    "location",
                    "Global"
                )
            )


            match_score = 80


            priority = priority_engine.calculate_priority(
                {
                    "role": role,
                    "country": country
                },
                match_score
            )


            st.subheader(
                f"{role} - {company}"
            )


            col1,col2 = st.columns(2)


            with col1:


                st.metric(
                    "AI Match Score",
                    f"{match_score}%"
                )


            with col2:


                st.metric(
                    "Priority Score",
                    f"{priority['priority_score']}%"
                )


            category = priority.get(
                "category",
                "Review"
            )


            if "Apply" in category:


                st.success(
                    "🔥 Apply Immediately"
                )


            elif "High" in category:


                st.warning(
                    "🔥 High Priority"
                )


            else:


                st.info(
                    "📌 Review"
                )


            st.write(
                "🏢 Company:",
                company
            )


            st.write(
                "🌍 Location:",
                country
            )


            st.write(
                "⭐ Source:",
                job.get(
                    "source",
                    "AI Search"
                )
            )


            st.divider()



    else:


        st.warning(
            "No executive jobs found"
        )



# ==================================================
# ANALYTICS DASHBOARD
# ==================================================

st.divider()

st.header(
    "📊 Application Intelligence Dashboard"
)


analytics = ApplicationAnalytics()


summary = analytics.get_summary()


c1,c2,c3,c4 = st.columns(4)


c1.metric(
    "Total Applications",
    summary.get(
        "total",
        0
    )
)


c2.metric(
    "Applied",
    summary.get(
        "statuses",
        {}
    ).get(
        "Applied",
        0
    )
)


c3.metric(
    "Interview",
    summary.get(
        "statuses",
        {}
    ).get(
        "Interview",
        0
    )
)


c4.metric(
    "Offers",
    summary.get(
        "statuses",
        {}
    ).get(
        "Offer",
        0
    )
)



if summary.get(
    "statuses"
):


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