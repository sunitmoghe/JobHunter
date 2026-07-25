import streamlit as st
import pandas as pd
import plotly.express as px

from modules.resume_parser import ResumeParser
from modules.ats_matcher import ATSMatcher
from modules.profile_pipeline import process_resume

st.set_page_config(
    page_title="Global Executive Job Hunter",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Executive Job Hunter")

jobs = pd.DataFrame([
    ["Head of Sales","Google","Singapore","35 min ago"],
    ["Country Manager","Microsoft","Germany","20 min ago"],
    ["VP Sales","Oracle","UAE","50 min ago"],
    ["Director Sales","SAP","Poland","15 min ago"],
    ["Business Development Director","Amazon","UK","45 min ago"],
    ["Chief Revenue Officer","Siemens","Saudi Arabia","30 min ago"],
])

jobs.columns = ["Role","Company","Country","Posted"]

# ---------- KPIs ----------
c1, c2, c3 = st.columns(3)

c1.metric("Total Jobs", len(jobs))
c2.metric("Countries", jobs["Country"].nunique())
c3.metric("Companies", jobs["Company"].nunique())

st.divider()

# ---------- Filters ----------
role = st.selectbox(
    "Select Role",
    ["All"] + sorted(jobs["Role"].unique().tolist())
)

if role != "All":
    jobs = jobs[jobs["Role"] == role]

st.dataframe(jobs, use_container_width=True)

st.divider()

country_count = jobs.groupby("Country").size().reset_index(name="Jobs")

fig = px.bar(
    country_count,
    x="Country",
    y="Jobs",
    title="Jobs by Country"
)

st.plotly_chart(fig, use_container_width=True)

st.header("📄 ATS Resume Matcher")

uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

if uploaded_resume:

    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_resume.getbuffer())


    # Build Executive Profile
    profile = process_resume(
        "temp_resume.pdf"
    )


    st.success(
        "✅ Executive Profile Created and Stored"
    )

    st.info(
        "🗄️ Profile saved in JobHunter database"
    )

    st.divider()

    st.header("👤 Executive Profile")

    col1, col2 = st.columns(2)


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


    st.subheader("🛠 Skills Detected")

    for skill in profile["skills"]:
        st.success(skill)


st.divider()


job_description = st.text_area(
    "Paste Job Description",
    height=250
)

if uploaded_resume and job_description:

    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_resume.getbuffer())

    parser = ResumeParser("temp_resume.pdf")

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

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matched Skills")

        if result["matched"]:
            for item in result["matched"]:
                st.success(f"{item['category']} → {item['skill']}")
        else:
            st.info("No matching skills found.")

    with col2:
        st.subheader("❌ Missing Skills")

        if result["missing"]:
            for item in result["missing"]:
                st.error(f"{item['category']} → {item['skill']}")
        else:
            st.success("No missing skills.")