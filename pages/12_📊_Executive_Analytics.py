import streamlit as st
import pandas as pd

from modules.application_tracker import ApplicationTracker
from modules.profile_manager import ProfileManager
from modules.career_strategy_ai import CareerStrategyAI

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
    page_title="Executive Analytics",
    page_icon="📊",
    layout="wide",
)


page_header(
    "📊 Executive Analytics Dashboard",
    "Executive Intelligence • Analytics • Career Insights"
)


tracker = ApplicationTracker()
profile_manager = ProfileManager()
career_ai = CareerStrategyAI()


# --------------------------------------------------
# PROFILE
# --------------------------------------------------

if profile_manager.profile_exists():

    profile = profile_manager.load_profile()

else:

    profile = {
        "experience": 23,
        "skills": [
            "Sales",
            "Leadership",
            "P&L",
            "SaaS",
        ],
    }


strategy = career_ai.career_recommendation(
    profile
)


# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------

try:

    applications = tracker.load_applications()

except Exception:

    applications = []


if not applications:

    empty_state(
        "No applications available for analytics."
    )

    st.stop()


df = pd.DataFrame(
    applications
)


# --------------------------------------------------
# KPI DASHBOARD
# --------------------------------------------------

section_header(
    "📈 Executive KPIs"
)


metric_row(
    [
        (
            "Applications",
            len(df)
        ),

        (
            "Avg Priority",
            f"{int(df['priority_score'].mean())}%"
            if "priority_score" in df.columns
            else "--"
        ),

        (
            "Interview Probability",
            f"{int(df['interview_probability'].mean())}%"
            if "interview_probability" in df.columns
            else "--"
        ),

        (
            "Executive Score",
            f"{strategy['executive_score']['overall_score']}%"
        ),
    ]
)


divider()


# --------------------------------------------------
# APPLICATION ANALYTICS
# --------------------------------------------------

section_header(
    "🌍 Application Analytics"
)


left, right = st.columns(2)


with left:

    st.write(
        "### Applications by Country"
    )

    if "country" in df.columns:

        country_df = (
            df.groupby("country")
            .size()
            .reset_index(
                name="Applications"
            )
            .sort_values(
                "Applications",
                ascending=False
            )
        )

        st.dataframe(
            country_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        info_box(
            "Country information unavailable."
        )


with right:

    st.write(
        "### Applications by Company"
    )

    if "company" in df.columns:

        company_df = (
            df.groupby("company")
            .size()
            .reset_index(
                name="Applications"
            )
            .sort_values(
                "Applications",
                ascending=False
            )
            .head(10)
        )

        st.dataframe(
            company_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        info_box(
            "Company information unavailable."
        )


divider()


# --------------------------------------------------
# PRIORITY OPPORTUNITIES
# --------------------------------------------------

section_header(
    "⭐ Highest Priority Opportunities"
)


if "priority_score" in df.columns:

    top_priority = (
        df.sort_values(
            "priority_score",
            ascending=False
        )
        .head(10)
    )


    columns = [
        c for c in [
            "role",
            "company",
            "country",
            "priority_score",
            "interview_probability",
        ]
        if c in top_priority.columns
    ]


    st.dataframe(
        top_priority[columns],
        use_container_width=True,
        hide_index=True,
    )

else:

    info_box(
        "Priority score data unavailable."
    )


divider()


# --------------------------------------------------
# INTERVIEW INTELLIGENCE
# --------------------------------------------------

section_header(
    "🎯 Interview Intelligence"
)


if "interview_probability" in df.columns:


    high = len(
        df[
            df["interview_probability"] >= 80
        ]
    )


    medium = len(
        df[
            (
                df["interview_probability"] >= 60
            )
            &
            (
                df["interview_probability"] < 80
            )
        ]
    )


    low = len(
        df[
            df["interview_probability"] < 60
        ]
    )


    metric_row(
        [
            (
                "High Probability",
                high
            ),
            (
                "Medium Probability",
                medium
            ),
            (
                "Low Probability",
                low
            ),
        ]
    )


else:

    info_box(
        "Interview probability data unavailable."
    )


divider()


# --------------------------------------------------
# AI INSIGHTS
# --------------------------------------------------

section_header(
    "🤖 AI Executive Insights"
)


best_market = strategy[
    "best_markets"
][0]


success_box(
    f"""
Executive Readiness Score:
{strategy['executive_score']['overall_score']}%

Best Relocation Market:
{best_market['country']}

Relocation Score:
{best_market['score']}%

Recommendation:

Focus applications on {best_market['country']}.
Continue targeting Director, VP, CRO,
COO and Country Manager opportunities.
"""
)


divider()


# --------------------------------------------------
# MARKETS
# --------------------------------------------------

section_header(
    "🌍 Top Recommended Executive Markets"
)


market_df = pd.DataFrame(
    [
        {
            "Country": market["country"],
            "Relocation Score": market["score"],
            "Career Fit": market["details"]["career_fit"],
            "Salary Fit": market["details"]["salary_fit"],
            "Visa Fit": market["details"]["visa_fit"],
            "Family Fit": market["details"]["family_fit"],
            "Market Demand": market["details"]["market_demand"],
        }

        for market in strategy[
            "best_markets"
        ]
    ]
)


st.dataframe(
    market_df,
    use_container_width=True,
    hide_index=True,
)


divider()


# --------------------------------------------------
# STRENGTHS
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
        "⚠ Executive Development Areas"
    )

    for gap in strategy["gaps"]:

        warning_box(
            gap
        )


divider()


# --------------------------------------------------
# ACTION PLAN
# --------------------------------------------------

section_header(
    "📅 Recommended Actions"
)


plan = strategy["action_plan"]

cols = st.columns(3)


for col, month in zip(
    cols,
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

        for task in plan.get(
            month,
            []
        ):

            st.write(
                "•",
                task
            )


divider()


success_box(
    "✅ Executive Analytics Dashboard operational."
)


st.caption(
    "JobHunter AI • Executive Analytics Suite"
)