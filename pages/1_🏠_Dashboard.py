import streamlit as st
import pandas as pd

from modules.application_analytics import ApplicationAnalytics
from modules.recruiter_manager import RecruiterManager
from modules.executive_ai_agent import ExecutiveAIAgent

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Executive Career Dashboard")

analytics = ApplicationAnalytics()

summary = analytics.get_summary()

agent = ExecutiveAIAgent()

jobs = agent.search_all_roles(max_roles=2)

recruiters = RecruiterManager().get_recruiters()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Live Jobs",
    len(jobs)
)

c2.metric(
    "Applications",
    summary["total"]
)

c3.metric(
    "Recruiters",
    len(recruiters)
)

c4.metric(
    "Interviews",
    summary["statuses"].get(
        "Interview",
        0
    )
)

st.divider()

st.subheader("🔥 Latest Executive Jobs")

df = pd.DataFrame(jobs)

if not df.empty:

    st.dataframe(
        df[
            [
                "role",
                "company",
                "country"
            ]
        ],
        use_container_width=True
    )

else:

    st.info("No jobs found.")