import streamlit as st
import pandas as pd

from modules.executive_dashboard_engine import ExecutiveDashboardEngine
from modules.executive_ai_agent import ExecutiveAIAgent
from modules.executive_report_engine import ExecutiveReportEngine
from modules.job_recommendation import JobRecommendationEngine

from modules.ui_components import (
    page_header,
    metric_row,
    section_header,
    divider,
    empty_state,
    success_box,
)

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="🏠",
    layout="wide",
)

page_header(
    "🏠 Executive Career Dashboard",
    "AI Powered Executive Career Command Center"
)

dashboard = ExecutiveDashboardEngine()

dashboard_data = dashboard.get_dashboard()

agent = ExecutiveAIAgent()

jobs = agent.search_all_roles(max_roles=2)

report = ExecutiveReportEngine().generate(jobs)

recommended_jobs = JobRecommendationEngine().top_recommendations(
    jobs,
    limit=10
)

metric_row(
    [
        ("Executive Score", f"{dashboard_data['executive_score']}%"),
        ("Live Jobs", report["total_jobs"]),
        ("Applications", dashboard_data["application_count"]),
        ("Recruiters", dashboard_data["recruiter_count"]),
    ]
)

st.markdown("### 📈 Executive Career Snapshot")

c1, c2, c3 = st.columns(3)

with c1:
    st.info(f"🌍 Best Market\n\n{dashboard_data['best_market']}")

with c2:
    st.success(f"🎯 High Priority Jobs\n\n{report['high_priority_jobs']}")

with c3:
    st.warning(f"⭐ Average Executive Score\n\n{report['average_score']}%")

divider()

success_box(
    f"""
🌍 Best Executive Market

**{dashboard_data['best_market']}**

High Priority Jobs: **{report['high_priority_jobs']}**

Average Executive Score: **{report['average_score']}%**
"""
)

divider()

section_header("🔥 Recommended Executive Jobs")

df = pd.DataFrame(recommended_jobs)

if not df.empty:

    columns = [
        c for c in [
            "role",
            "company",
            "country",
            "executive_score",
            "priority",
        ]
        if c in df.columns
    ]

    st.dataframe(
        df[columns],
        use_container_width=True,
        hide_index=True,
    )

else:

    empty_state(
        "No executive jobs found."
    )

divider()

st.caption(
    "JobHunter AI • Executive Career Platform"
)