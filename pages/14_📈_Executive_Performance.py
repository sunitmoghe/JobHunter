import streamlit as st
import pandas as pd
import json
import os

from modules.profile_manager import ProfileManager
from modules.career_strategy_ai import CareerStrategyAI
from modules.application_tracker import ApplicationTracker


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Executive Performance",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Executive Performance Intelligence")

st.caption(
    "Track your executive career progress and growth."
)

st.divider()


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

profile_manager = ProfileManager()
career_ai = CareerStrategyAI()
tracker = ApplicationTracker()

if profile_manager.profile_exists():

    profile = profile_manager.load_profile()

else:

    profile = {
        "experience": 23,
        "skills": []
    }

strategy = career_ai.career_recommendation(profile)

try:

    applications = tracker.load_applications()

except Exception:

    applications = []

recruiters = []

recruiter_file = "database/recruiters.json"

if os.path.exists(recruiter_file):

    with open(
        recruiter_file,
        "r",
        encoding="utf-8"
    ) as f:

        recruiters = json.load(f)

applications_df = pd.DataFrame(applications)
recruiters_df = pd.DataFrame(recruiters)


# --------------------------------------------------
# PERFORMANCE KPIs
# --------------------------------------------------

st.subheader("📊 Executive Performance KPIs")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Executive Score",
        f"{strategy['executive_score']['overall_score']}%"
    )

with c2:

    st.metric(
        "Applications",
        len(applications_df)
    )

with c3:

    st.metric(
        "Recruiters",
        len(recruiters_df)
    )

with c4:

    avg_probability = 0

    if (
        not applications_df.empty
        and
        "interview_probability" in applications_df.columns
    ):

        avg_probability = int(
            applications_df["interview_probability"].mean()
        )

    st.metric(
        "Interview Probability",
        f"{avg_probability}%"
    )

st.divider()

# --------------------------------------------------
# EXECUTIVE GROWTH INDEX
# --------------------------------------------------

st.subheader("🚀 Executive Growth Index")

executive_score = strategy["executive_score"]["overall_score"]

application_score = min(
    len(applications_df) * 2,
    100
)

recruiter_score = min(
    len(recruiters_df) * 5,
    100
)

career_momentum = int(

    (
        executive_score
        +
        application_score
        +
        recruiter_score
    )

    / 3

)

g1, g2, g3 = st.columns(3)

with g1:

    st.metric(
        "Executive Readiness",
        f"{executive_score}%"
    )

with g2:

    st.metric(
        "Career Momentum",
        f"{career_momentum}%"
    )

with g3:

    st.metric(
        "Network Strength",
        f"{recruiter_score}%"
    )

st.divider()


# --------------------------------------------------
# WEEKLY PERFORMANCE REVIEW
# --------------------------------------------------

st.subheader("📅 Weekly Executive Performance")

review = pd.DataFrame(

    {

        "Metric": [

            "Applications",

            "Recruiters",

            "Executive Score",

            "Interview Probability",

            "Career Momentum"

        ],

        "Value": [

            len(applications_df),

            len(recruiters_df),

            executive_score,

            avg_probability,

            career_momentum

        ]

    }

)

st.dataframe(

    review,

    use_container_width=True,

    hide_index=True

)

st.divider()


# --------------------------------------------------
# PERFORMANCE SNAPSHOT
# --------------------------------------------------

st.subheader("📈 Executive Performance Snapshot")

snapshot_left, snapshot_right = st.columns(2)

with snapshot_left:

    st.write("### 💪 Executive Strengths")

    for strength in strategy["strengths"]:

        st.success(strength)

with snapshot_right:

    st.write("### ⚠ Areas to Improve")

    for gap in strategy["gaps"]:

        st.warning(gap)

st.divider()

# --------------------------------------------------
# AI PERFORMANCE COACH
# --------------------------------------------------

st.subheader("🤖 AI Executive Performance Coach")

if career_momentum >= 85:

    grade = "A+"
    coach_message = (
        "Outstanding progress. Maintain momentum and focus on high-value executive roles."
    )

elif career_momentum >= 70:

    grade = "A"
    coach_message = (
        "Strong progress. Increase recruiter engagement and continue targeted applications."
    )

elif career_momentum >= 55:

    grade = "B"
    coach_message = (
        "Good foundation. Increase application volume and strengthen your executive network."
    )

else:

    grade = "C"
    coach_message = (
        "Your profile has potential. Focus on consistent applications and recruiter outreach."
    )

st.success(
    f"""
Executive Performance Grade: **{grade}**

{coach_message}
"""
)

st.divider()


# --------------------------------------------------
# WEEKLY RECOMMENDATIONS
# --------------------------------------------------

st.subheader("🎯 AI Weekly Recommendations")

recommendations = [

    f"Apply to at least {max(10, 20 - len(applications_df))} additional executive opportunities this week.",

    "Continue prioritising Singapore, UAE and Germany.",

    "Reach out to at least five new executive recruiters.",

    "Follow up with recruiters contacted during the last two weeks.",

    "Tailor your CV before every executive application.",

    "Track interview outcomes and update your pipeline regularly."

]

for recommendation in recommendations:

    st.info(recommendation)

st.divider()


# --------------------------------------------------
# PERFORMANCE SUMMARY
# --------------------------------------------------

st.subheader("🏁 Executive Performance Summary")

summary = pd.DataFrame({

    "Indicator": [

        "Executive Readiness",

        "Career Momentum",

        "Applications",

        "Recruiter Network",

        "Interview Probability"

    ],

    "Current Value": [

        f"{executive_score}%",

        f"{career_momentum}%",

        len(applications_df),

        len(recruiters_df),

        f"{avg_probability}%"

    ]

})

st.dataframe(

    summary,

    use_container_width=True,

    hide_index=True

)

st.divider()

st.success("✅ Executive Performance Intelligence operational.")

st.caption(
    "JobHunter AI • Executive Performance Suite"
)