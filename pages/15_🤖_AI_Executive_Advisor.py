import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

from modules.profile_manager import ProfileManager
from modules.career_strategy_ai import CareerStrategyAI
from modules.application_tracker import ApplicationTracker


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Executive Advisor",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Executive Advisor")

today = datetime.now().strftime("%A, %d %B %Y")

st.caption(
    f"Executive Morning Briefing • {today}"
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
        "name": "Executive",
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
# EXECUTIVE BRIEFING
# --------------------------------------------------

st.subheader("🧠 Morning Executive Briefing")

executive_score = strategy["executive_score"]["overall_score"]

application_count = len(applications_df)

recruiter_count = len(recruiters_df)

avg_probability = 0

if (
    not applications_df.empty
    and
    "interview_probability" in applications_df.columns
):

    avg_probability = int(
        applications_df["interview_probability"].mean()
    )

best_market = strategy["best_markets"][0]["country"]

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Executive Readiness",
        f"{executive_score}%"
    )

with col2:

    st.metric(
        "Applications",
        application_count
    )

with col3:

    st.metric(
        "Recruiters",
        recruiter_count
    )

with col4:

    st.metric(
        "Interview Probability",
        f"{avg_probability}%"
    )

st.success(
    f"""
Good morning.

Your strongest executive market today is **{best_market}**.

Your executive profile is performing well. Focus on high-quality executive applications and personalised recruiter engagement.
"""
)

st.divider()

# --------------------------------------------------
# DAILY EXECUTIVE MISSION
# --------------------------------------------------

st.subheader("🎯 Today's Executive Mission")

mission = [

    f"Apply to at least {max(5, 20 - application_count)} executive opportunities.",

    "Contact 3 executive recruiters with personalised messages.",

    f"Prioritise executive positions in {best_market}.",

    "Tailor your CV for every shortlisted role.",

    "Record all recruiter interactions in the CRM."

]

for task in mission:

    st.checkbox(task)

st.divider()


# --------------------------------------------------
# MARKET FOCUS
# --------------------------------------------------

st.subheader("🌍 Executive Market Focus")

market_df = pd.DataFrame(

    [
        {
            "Country": market["country"],
            "Executive Score": market["score"]
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
# EXECUTIVE RISK MONITOR
# --------------------------------------------------

st.subheader("⚠ Executive Risk Monitor")

if application_count < 10:

    st.warning(
        "Application volume is below the recommended level."
    )

else:

    st.success(
        "Application activity is healthy."
    )

if recruiter_count < 10:

    st.warning(
        "Expand your recruiter network."
    )

else:

    st.success(
        "Recruiter network is growing well."
    )

if avg_probability < 70:

    st.warning(
        "Improve ATS alignment and CV tailoring to increase interview probability."
    )

else:

    st.success(
        "Interview probability is strong."
    )

st.divider()


# --------------------------------------------------
# CAREER MOMENTUM
# --------------------------------------------------

st.subheader("📈 Career Momentum")

momentum = int(

    (
        executive_score
        +
        min(application_count * 2, 100)
        +
        min(recruiter_count * 5, 100)
    )

    / 3

)

st.metric(
    "Career Momentum Score",
    f"{momentum}%"
)

st.divider()

# --------------------------------------------------
# AI EXECUTIVE COACH
# --------------------------------------------------

st.subheader("🤖 AI Executive Coach")

if momentum >= 85:

    coaching_message = """
You are operating at a high executive readiness level.

Continue focusing on VP, Country Manager, CRO and COO opportunities.
Your profile is competitive for international executive positions.
"""

elif momentum >= 70:

    coaching_message = """
Your executive profile is progressing well.

Increase recruiter engagement and continue tailoring your CV for each application to improve interview conversion.
"""

else:

    coaching_message = """
Your executive journey is on track, but consistency is the priority.

Increase quality applications, expand your recruiter network, and strengthen ATS alignment.
"""

st.info(coaching_message)

st.divider()


# --------------------------------------------------
# PERSONALISED RECOMMENDATIONS
# --------------------------------------------------

st.subheader("📝 Personalised Recommendations")

recommendations = [

    f"Continue prioritising opportunities in {best_market}.",

    "Focus on Director, VP, CRO, COO and Country Manager roles.",

    "Send follow-up messages to recruiters every 7–10 days.",

    "Tailor your executive CV for every shortlisted position.",

    "Track all recruiter conversations and interview outcomes.",

    "Review your Executive Performance dashboard weekly."

]

for recommendation in recommendations:

    st.success(recommendation)

st.divider()


# --------------------------------------------------
# EXECUTIVE DAILY CHECKLIST
# --------------------------------------------------

st.subheader("📅 Today's Checklist")

checklist = [

    "Apply to executive opportunities",

    "Connect with executive recruiters",

    "Send recruiter follow-ups",

    "Update application tracker",

    "Review interview preparation",

    "Improve one section of your CV"

]

for item in checklist:

    st.checkbox(item)

st.divider()


# --------------------------------------------------
# EXECUTIVE SUMMARY
# --------------------------------------------------

st.subheader("🏁 Executive Briefing Summary")

summary = pd.DataFrame({

    "Indicator": [

        "Executive Readiness",

        "Career Momentum",

        "Applications",

        "Recruiters",

        "Best Market",

        "Interview Probability"

    ],

    "Current Status": [

        f"{executive_score}%",

        f"{momentum}%",

        application_count,

        recruiter_count,

        best_market,

        f"{avg_probability}%"

    ]

})

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.success("✅ AI Executive Advisor operational.")

st.caption(
    "JobHunter AI • Executive Advisor Suite"
)