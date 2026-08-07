import streamlit as st

from modules.dashboard_engine import DashboardEngine


st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Executive Dashboard")

engine = DashboardEngine()

stats = engine.get_dashboard_stats()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🎯 Total Jobs",
        stats["total_jobs"],
    )

with col2:
    st.metric(
        "💾 Saved Jobs",
        stats["saved_jobs"],
    )

with col3:
    st.metric(
        "📤 Applied Jobs",
        stats["applied_jobs"],
    )

with col4:
    st.metric(
        "🌍 Countries",
        stats["countries"],
    )

st.divider()

col5, col6, col7 = st.columns(3)

with col5:
    st.metric(
        "🏢 Companies",
        stats["companies"],
    )

with col6:
    st.metric(
        "⭐ Avg JobHunter Score",
        stats["avg_score"],
    )

with col7:
    st.metric(
        "🏆 Avg Opportunity Score",
        stats["avg_opportunity"],
    )

st.divider()

st.subheader("🚀 Executive Quick Actions")

a, b, c, d = st.columns(4)

with a:
    st.page_link(
        "pages/4_🔥_AI_Executive_Jobs.py",
        label="🔥 AI Executive Jobs",
    )

with b:
    st.page_link(
        "pages/2_📄_Resume_Intelligence.py",
        label="📄 Resume Intelligence",
    )

with c:
    st.page_link(
        "pages/3_🎯_ATS_Matcher.py",
        label="🎯 ATS Matcher",
    )

with d:
    st.page_link(
        "pages/5_👥_Recruiter_CRM.py",
        label="👥 Recruiter CRM",
    )

st.divider()

st.info(
    "Executive Analytics charts will be added in the next phase."
)