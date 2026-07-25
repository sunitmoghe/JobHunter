import streamlit as st
import pandas as pd

from modules.application_tracker import ApplicationTracker
from modules.profile_manager import ProfileManager
from modules.career_strategy_ai import CareerStrategyAI


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Executive Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Executive Analytics Dashboard")

st.caption(
    "Executive Intelligence • Analytics • Career Insights"
)

st.divider()


# --------------------------------------------------
# LOAD MODULES
# --------------------------------------------------

tracker = ApplicationTracker()
profile_manager = ProfileManager()
career_ai = CareerStrategyAI()


# --------------------------------------------------
# LOAD PROFILE
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

            "SaaS"

        ]

    }


strategy = career_ai.career_recommendation(profile)


# --------------------------------------------------
# LOAD APPLICATIONS
# --------------------------------------------------

try:

    applications = tracker.load_applications()

except Exception:

    applications = []


if len(applications) == 0:

    st.warning(
        "No applications available."
    )

    st.stop()


df = pd.DataFrame(applications)


# --------------------------------------------------
# KPI DASHBOARD
# --------------------------------------------------

st.subheader("📈 Executive KPIs")

k1, k2, k3, k4 = st.columns(4)

with k1:

    st.metric(
        "Applications",
        len(df)
    )

with k2:

    if "priority_score" in df.columns:

        st.metric(
            "Avg Priority",
            f"{int(df['priority_score'].mean())}%"
        )

    else:

        st.metric(
            "Avg Priority",
            "--"
        )

with k3:

    if "interview_probability" in df.columns:

        st.metric(
            "Interview Probability",
            f"{int(df['interview_probability'].mean())}%"
        )

    else:

        st.metric(
            "Interview Probability",
            "--"
        )

with k4:

    st.metric(
        "Executive Score",
        f"{strategy['executive_score']['overall_score']}%"
    )

st.divider()

# --------------------------------------------------
# APPLICATION ANALYTICS
# --------------------------------------------------

st.subheader("🌍 Application Analytics")

left, right = st.columns(2)

with left:

    st.write("### Applications by Country")

    if "country" in df.columns:

        country_df = (

            df.groupby("country")

            .size()

            .reset_index(name="Applications")

            .sort_values(

                "Applications",

                ascending=False

            )

        )

        st.dataframe(

            country_df,

            use_container_width=True,

            hide_index=True

        )

    else:

        st.info("Country information unavailable.")

with right:

    st.write("### Applications by Company")

    if "company" in df.columns:

        company_df = (

            df.groupby("company")

            .size()

            .reset_index(name="Applications")

            .sort_values(

                "Applications",

                ascending=False

            )

            .head(10)

        )

        st.dataframe(

            company_df,

            use_container_width=True,

            hide_index=True

        )

    else:

        st.info("Company information unavailable.")

st.divider()


# --------------------------------------------------
# HIGHEST PRIORITY OPPORTUNITIES
# --------------------------------------------------

st.subheader("⭐ Highest Priority Opportunities")

if "priority_score" in df.columns:

    top_priority = (

        df.sort_values(

            "priority_score",

            ascending=False

        )

        .head(10)

    )

    display_cols = [

        c for c in [

            "role",

            "company",

            "country",

            "priority_score",

            "interview_probability"

        ]

        if c in top_priority.columns

    ]

    st.dataframe(

        top_priority[display_cols],

        use_container_width=True,

        hide_index=True

    )

else:

    st.info("Priority score data unavailable.")

st.divider()


# --------------------------------------------------
# INTERVIEW INTELLIGENCE
# --------------------------------------------------

st.subheader("🎯 Interview Intelligence")

if "interview_probability" in df.columns:

    high = len(

        df[df["interview_probability"] >= 80]

    )

    medium = len(

        df[

            (df["interview_probability"] >= 60)

            &

            (df["interview_probability"] < 80)

        ]

    )

    low = len(

        df[df["interview_probability"] < 60]

    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.success(f"High Probability\n\n{high}")

    with c2:

        st.warning(f"Medium Probability\n\n{medium}")

    with c3:

        st.error(f"Low Probability\n\n{low}")

else:

    st.info("Interview probability data unavailable.")

st.divider()

# --------------------------------------------------
# AI EXECUTIVE INSIGHTS
# --------------------------------------------------

st.subheader("🤖 AI Executive Insights")

best_market = strategy["best_markets"][0]

st.success(
    f"""
🎯 Executive Readiness Score: {strategy['executive_score']['overall_score']}%

🌍 Best Relocation Market: {best_market['country']}

⭐ Relocation Score: {best_market['score']}%

Recommendation:
Focus your executive applications on {best_market['country']},
continue targeting Director, VP, CRO, COO and Country Manager
opportunities, and maintain a high application cadence.
"""
)

st.divider()


# --------------------------------------------------
# RECOMMENDED EXECUTIVE MARKETS
# --------------------------------------------------

st.subheader("🌍 Top Recommended Executive Markets")

market_df = pd.DataFrame(

    [
        {
            "Country": market["country"],
            "Relocation Score": market["score"],
            "Career Fit": market["details"]["career_fit"],
            "Salary Fit": market["details"]["salary_fit"],
            "Visa Fit": market["details"]["visa_fit"],
            "Family Fit": market["details"]["family_fit"],
            "Market Demand": market["details"]["market_demand"]
        }

        for market in strategy["best_markets"]

    ]

)

st.dataframe(
    market_df,
    use_container_width=True,
    hide_index=True
)

st.divider()


# --------------------------------------------------
# EXECUTIVE STRENGTH SNAPSHOT
# --------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("💪 Executive Strengths")

    for strength in strategy["strengths"]:

        st.success(strength)

with right:

    st.subheader("⚠ Executive Development Areas")

    for gap in strategy["gaps"]:

        st.warning(gap)

st.divider()


# --------------------------------------------------
# EXECUTIVE ACTION PLAN
# --------------------------------------------------

st.subheader("📅 Recommended Actions")

plan = strategy["action_plan"]

c1, c2, c3 = st.columns(3)

with c1:

    st.info("Month 1")

    for task in plan["Month 1"]:

        st.write("•", task)

with c2:

    st.info("Month 2")

    for task in plan["Month 2"]:

        st.write("•", task)

with c3:

    st.info("Month 3")

    for task in plan["Month 3"]:

        st.write("•", task)

st.divider()


# --------------------------------------------------
# DASHBOARD FOOTER
# --------------------------------------------------

st.success(
    "✅ Executive Analytics Dashboard operational."
)

st.caption(
    "JobHunter AI • Executive Analytics Suite"
)