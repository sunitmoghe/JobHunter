import streamlit as st
import pandas as pd

from modules.profile_manager import ProfileManager
from modules.career_strategy_ai import CareerStrategyAI
from modules.application_tracker import ApplicationTracker

from modules.ui_components import (
    page_header,
    section_header,
    metric_row,
    success_box,
    warning_box,
    info_box,
    divider,
    empty_state,
)

st.set_page_config(
    page_title="Executive Command Center",
    page_icon="🚀",
    layout="wide",
)

page_header(
    "🚀 Executive Command Center",
    "Your Executive AI Career Operating System."
)

profile_manager = ProfileManager()
career_ai = CareerStrategyAI()
tracker = ApplicationTracker()


if profile_manager.profile_exists():

    profile = profile_manager.load_profile()

else:

    profile = {
        "experience": 23,
        "skills": [
            "Sales Leadership",
            "P&L",
            "SaaS",
            "IoT",
            "Digital Transformation",
        ],
    }


strategy = career_ai.career_recommendation(
    profile
)


try:

    applications = tracker.load_applications()

except Exception:

    applications = []


# --------------------------------------------------
# KPI DASHBOARD
# --------------------------------------------------

section_header(
    "📈 Executive KPI Dashboard"
)

metric_row(
    [
        (
            "Executive Score",
            f"{strategy['executive_score']['overall_score']}%"
        ),
        (
            "Applications",
            len(applications)
        ),
        (
            "Top Market",
            strategy["best_markets"][0]["country"]
        ),
        (
            "Experience",
            f"{profile.get('experience',20)} Years"
        ),
    ]
)


divider()


# --------------------------------------------------
# TOP MARKETS
# --------------------------------------------------

section_header(
    "🌍 Top Executive Markets"
)

market_cols = st.columns(3)

for index, market in enumerate(
    strategy["best_markets"]
):

    if index >= 3:
        break

    with market_cols[index]:

        success_box(
            market["country"]
        )

        st.metric(
            "Relocation Score",
            f"{market['score']}%"
        )

        details = market["details"]

        st.write(
            f"Career Fit: {details['career_fit']}%"
        )

        st.write(
            f"Salary Fit: {details['salary_fit']}%"
        )

        st.write(
            f"Visa Fit: {details['visa_fit']}%"
        )

        st.write(
            f"Family Fit: {details['family_fit']}%"
        )

        st.write(
            f"Market Demand: {details['market_demand']}%"
        )


divider()


# --------------------------------------------------
# STRENGTHS AND GAPS
# --------------------------------------------------

left, right = st.columns(2)


with left:

    section_header(
        "💪 Executive Strengths"
    )

    for strength in strategy["strengths"]:

        success_box(
            strength
        )


with right:

    section_header(
        "⚠ Career Improvement Areas"
    )

    for gap in strategy["gaps"]:

        warning_box(
            gap
        )


divider()


# --------------------------------------------------
# 90 DAY PLAN
# --------------------------------------------------

section_header(
    "📅 90-Day Executive Career Plan"
)


months = strategy["action_plan"]

month_cols = st.columns(3)


for col, month in zip(
    month_cols,
    [
        "Month 1",
        "Month 2",
        "Month 3",
    ]
):

    with col:

        info_box(
            month
        )

        for task in months.get(
            month,
            []
        ):

            st.write(
                "•",
                task
            )


divider()


# --------------------------------------------------
# APPLICATION PIPELINE
# --------------------------------------------------

section_header(
    "📄 Executive Application Pipeline"
)


if applications:

    df = pd.DataFrame(
        applications
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    metric_row(
        [
            (
                "Applications",
                len(df)
            ),
            (
                "Average Priority",
                f"{int(df['priority_score'].mean())}%"
                if "priority_score" in df.columns
                else "N/A"
            ),
            (
                "Interview Probability",
                f"{int(df['interview_probability'].mean())}%"
                if "interview_probability" in df.columns
                else "N/A"
            ),
        ]
    )

else:

    empty_state(
        "No applications have been saved yet."
    )


divider()


# --------------------------------------------------
# AI SUMMARY
# --------------------------------------------------

section_header(
    "🤖 AI Executive Summary"
)


best_country = strategy["best_markets"][0]["country"]

summary = f"""
Your Executive Readiness Score is
{strategy['executive_score']['overall_score']}%.

Your strongest international market is
{best_country}.

Focus areas:

• Senior leadership roles
• P&L ownership
• Enterprise sales
• Global expansion opportunities

Priority roles:

Director,
VP,
Chief Revenue Officer,
Chief Commercial Officer,
Country Manager.
"""


success_box(
    summary
)


divider()


# --------------------------------------------------
# ANALYTICS
# --------------------------------------------------

section_header(
    "📊 Executive Analytics"
)


analytics_col1, analytics_col2 = st.columns(2)


with analytics_col1:

    st.write(
        "### 🌍 Relocation Ranking"
    )

    ranking_df = pd.DataFrame(
        [
            {
                "Country": m["country"],
                "Score": m["score"],
            }
            for m in strategy["best_markets"]
        ]
    )

    st.dataframe(
        ranking_df,
        use_container_width=True,
        hide_index=True,
    )


with analytics_col2:

    st.write(
        "### 🎯 Executive Readiness Breakdown"
    )

    breakdown = strategy["executive_score"]["breakdown"]

    metrics_df = pd.DataFrame(
        {
            "Metric": [
                "Leadership",
                "Revenue",
                "Global",
                "Technology",
                "Market",
            ],
            "Score": [
                breakdown["leadership_score"],
                breakdown["revenue_score"],
                breakdown["global_fit_score"],
                breakdown["technology_score"],
                breakdown["market_score"],
            ],
        }
    )

    st.dataframe(
        metrics_df,
        use_container_width=True,
        hide_index=True,
    )


divider()


# --------------------------------------------------
# TODAY'S PRIORITIES
# --------------------------------------------------

section_header(
    "🚀 Today's Executive Priorities"
)


for item in [
    "Apply to 5 high-priority executive roles.",
    "Send LinkedIn messages to 3 senior recruiters.",
    "Tailor resume for highest-ranked opportunity.",
    "Prepare one executive interview success story.",
    "Review opportunities in your #1 relocation market.",
]:

    st.checkbox(
        item
    )


divider()


success_box(
    "🎯 Executive Command Center is active."
)

st.caption(
    "JobHunter AI • Executive Career Operating System"
)