import streamlit as st

from modules.executive_ai_agent import ExecutiveAIAgent
from modules.profile_manager import ProfileManager
from modules.executive_performance_engine import ExecutivePerformanceEngine

st.set_page_config(
    page_title="Executive Performance",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Executive Performance Dashboard")

profile_manager = ProfileManager()
agent = ExecutiveAIAgent()
engine = ExecutivePerformanceEngine()

# -----------------------------

# Profile

# -----------------------------

if profile_manager.profile_exists():

    profile = profile_manager.load_profile()

else:

    profile = {
        "experience": 23
    }

# -----------------------------

# Cached Jobs

# -----------------------------

if "cached_jobs" not in st.session_state:

    with st.spinner("Loading Executive Jobs..."):

        st.session_state["cached_jobs"] = agent.search_all_roles(
            max_roles=10
        )

jobs = st.session_state["cached_jobs"]

# -----------------------------

# Performance

# -----------------------------

performance = engine.calculate(
    profile,
    jobs
)

# -----------------------------

# KPIs

# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Executive Score",
        f"{performance['Executive Score']}%"
    )

    st.metric(
        "ATS Readiness",
        f"{performance['ATS Readiness']}%"
    )

with col2:

    st.metric(
        "Interview Readiness",
        f"{performance['Interview Readiness']}%"
    )

    st.metric(
        "Recruiter Reach",
        f"{performance['Recruiter Reach']}%"
    )

with col3:

    st.metric(
        "Global Market",
        f"{performance['Global Market']}%"
    )

    st.metric(
        "Overall Readiness",
        f"{performance['Overall Readiness']}%"
    )

# -----------------------------

st.divider()

st.subheader("📋 Executive Career Summary")

st.success(
    f"""
Executive Readiness : **{performance['Overall Readiness']}%**

Executive Score : **{performance['Executive Score']}%**

ATS Ready : **{performance['ATS Readiness']}%**

Interview Ready : **{performance['Interview Readiness']}%**

Recruiter Reach : **{performance['Recruiter Reach']}%**

Global Market : **{performance['Global Market']}%**
"""
)

st.divider()

st.subheader("🎯 Next Executive Actions")

tasks = [

    "Apply to Top Executive Roles",

    "Reach out to Senior Recruiters",

    "Tailor Resume",

    "Prepare Executive Interviews",

    "Expand Global Network"

]

for task in tasks:

    st.checkbox(task)

st.success("Executive Performance Ready")