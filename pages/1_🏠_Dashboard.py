import streamlit as st
import pandas as pd

from modules.application_analytics import ApplicationAnalytics
from modules.recruiter_manager import RecruiterManager
from modules.executive_ai_agent import ExecutiveAIAgent

from modules.ui_components import (
    page_header,
    metric_row,
    section_header,
    divider,
    empty_state,
)

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="🏠",
    layout="wide",
)

page_header(
    "🏠 Executive Career Dashboard",
    "Your executive command overview."
)

analytics = ApplicationAnalytics()
summary = analytics.get_summary()

agent = ExecutiveAIAgent()
jobs = agent.search_all_roles(max_roles=2)

recruiters = RecruiterManager().get_recruiters()

metric_row(
    [
        ("Live Jobs", len(jobs)),
        ("Applications", summary["total"]),
        ("Recruiters", len(recruiters)),
        (
            "Interviews",
            summary["statuses"].get(
                "Interview",
                0,
            ),
        ),
    ]
)

divider()

section_header("🔥 Latest Executive Jobs")

df = pd.DataFrame(jobs)

if not df.empty:

    columns = [
        c
        for c in [
            "role",
            "company",
            "country",
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