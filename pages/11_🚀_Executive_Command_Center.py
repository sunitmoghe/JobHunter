import streamlit as st
import pandas as pd

from modules.profile_manager import ProfileManager
from modules.career_strategy_ai import CareerStrategyAI
from modules.application_tracker import ApplicationTracker


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Executive Command Center",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Executive Command Center")

st.caption(
    "Your Executive AI Career Operating System"
)

st.divider()


# --------------------------------------------------
# LOAD PROFILE
# --------------------------------------------------

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

            "Digital Transformation"

        ]

    }


strategy = career_ai.career_recommendation(
    profile
)

applications = []

try:

    applications = tracker.load_applications()

except Exception:

    applications = []


# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

st.subheader("📈 Executive KPI Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        "Executive Score",

        f"{strategy['executive_score']['overall_score']}%"

    )

with col2:

    st.metric(

        "Applications",

        len(applications)

    )

with col3:

    st.metric(

        "Top Market",

        strategy["best_markets"][0]["country"]

    )

with col4:

    st.metric(

        "Experience",

        f"{profile.get('experience',20)} Years"

    )

st.divider()


# --------------------------------------------------
# TOP MARKETS
# --------------------------------------------------

st.subheader("🌍 Top Executive Markets")

market_cols = st.columns(3)

for index, market in enumerate(strategy["best_markets"]):

    with market_cols[index]:

        st.success(
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

st.divider()

# --------------------------------------------------
# EXECUTIVE STRENGTHS & IMPROVEMENT
# --------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("💪 Executive Strengths")

    for strength in strategy["strengths"]:

        st.success(strength)

with right:

    st.subheader("⚠ Career Improvement Areas")

    for gap in strategy["gaps"]:

        st.warning(gap)

st.divider()


# --------------------------------------------------
# 90-DAY ACTION PLAN
# --------------------------------------------------

st.subheader("📅 90-Day Executive Career Plan")

months = strategy["action_plan"]

m1, m2, m3 = st.columns(3)

with m1:

    st.info("Month 1")

    for task in months["Month 1"]:

        st.write("•", task)

with m2:

    st.info("Month 2")

    for task in months["Month 2"]:

        st.write("•", task)

with m3:

    st.info("Month 3")

    for task in months["Month 3"]:

        st.write("•", task)

st.divider()


# --------------------------------------------------
# APPLICATION DASHBOARD
# --------------------------------------------------

st.subheader("📄 Executive Application Pipeline")

if len(applications) == 0:

    st.info(
        "No applications have been saved yet."
    )

else:

    df = pd.DataFrame(applications)

    st.dataframe(
        df,
        use_container_width=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Applications",
            len(df)
        )

    with col2:

        if "priority_score" in df.columns:

            st.metric(
                "Average Priority",
                f"{int(df['priority_score'].mean())}%"
            )

    with col3:

        if "interview_probability" in df.columns:

            st.metric(
                "Interview Probability",
                f"{int(df['interview_probability'].mean())}%"
            )

st.divider()


# --------------------------------------------------
# AI EXECUTIVE SUMMARY
# --------------------------------------------------

st.subheader("🤖 AI Executive Summary")

best_country = strategy["best_markets"][0]["country"]

summary = f"""
Your Executive Readiness Score is
{strategy['executive_score']['overall_score']}%.

Your strongest international market is
{best_country}.

Continue focusing on senior leadership,
P&L ownership,
enterprise sales,
and global expansion opportunities.

Priority recommendation:

Apply consistently to Director,
VP,
Chief Revenue Officer,
Chief Commercial Officer,
and Country Manager opportunities in your top relocation markets.
"""

st.success(summary)

st.divider()

# --------------------------------------------------
# EXECUTIVE ANALYTICS
# --------------------------------------------------

st.subheader("📊 Executive Analytics")

analytics_col1, analytics_col2 = st.columns(2)

with analytics_col1:

    st.write("### 🌍 Relocation Ranking")

    ranking_df = pd.DataFrame([
        {
            "Country": m["country"],
            "Score": m["score"]
        }
        for m in strategy["best_markets"]
    ])

    st.dataframe(
        ranking_df,
        use_container_width=True,
        hide_index=True
    )

with analytics_col2:

    st.write("### 🎯 Executive Readiness Breakdown")

    breakdown = strategy["executive_score"]["breakdown"]

    metrics_df = pd.DataFrame(
        {
            "Metric": [
                "Leadership",
                "Revenue",
                "Global",
                "Technology",
                "Market"
            ],
            "Score": [
                breakdown["leadership_score"],
                breakdown["revenue_score"],
                breakdown["global_fit_score"],
                breakdown["technology_score"],
                breakdown["market_score"]
            ]
        }
    )

    st.dataframe(
        metrics_df,
        use_container_width=True,
        hide_index=True
    )

st.divider()


# --------------------------------------------------
# TODAY'S AI RECOMMENDATIONS
# --------------------------------------------------

st.subheader("🚀 Today's Executive Priorities")

recommendations = [

    "Apply to 5 high-priority executive roles.",

    "Send LinkedIn messages to 3 senior recruiters.",

    "Tailor your resume for your highest-ranked opportunity.",

    "Prepare one executive interview success story.",

    "Review opportunities in your #1 relocation market."

]

for item in recommendations:

    st.checkbox(item)


st.divider()


# --------------------------------------------------
# COMMAND CENTER FOOTER
# --------------------------------------------------

st.success(
    "🎯 Executive Command Center is active."
)

st.caption(
    "JobHunter AI • Executive Career Operating System"
)