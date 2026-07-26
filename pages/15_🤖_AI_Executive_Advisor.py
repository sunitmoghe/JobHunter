import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

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
    page_title="AI Executive Advisor",
    page_icon="🤖",
    layout="wide",
)

today = datetime.now().strftime(
    "%A, %d %B %Y"
)

page_header(
    "🤖 AI Executive Advisor",
    f"Executive Morning Briefing • {today}"
)


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
        "skills": [],
    }


strategy = career_ai.career_recommendation(
    profile
)


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


applications_df = pd.DataFrame(
    applications
)

recruiters_df = pd.DataFrame(
    recruiters
)


# --------------------------------------------------
# EXECUTIVE BRIEFING
# --------------------------------------------------

section_header(
    "🧠 Morning Executive Briefing"
)


executive_score = strategy[
    "executive_score"
]["overall_score"]

application_count = len(
    applications_df
)

recruiter_count = len(
    recruiters_df
)


avg_probability = 0

if (
    not applications_df.empty
    and
    "interview_probability" in applications_df.columns
):

    avg_probability = int(
        applications_df[
            "interview_probability"
        ].mean()
    )


best_market = strategy[
    "best_markets"
][0]["country"]


metric_row(
    [
        (
            "Executive Readiness",
            f"{executive_score}%"
        ),
        (
            "Applications",
            application_count
        ),
        (
            "Recruiters",
            recruiter_count
        ),
        (
            "Interview Probability",
            f"{avg_probability}%"
        ),
    ]
)


success_box(
    f"""
Good morning.

Your strongest executive market today is **{best_market}**.

Focus on high-quality executive applications and personalised recruiter engagement.
"""
)


divider()


# --------------------------------------------------
# DAILY MISSION
# --------------------------------------------------

section_header(
    "🎯 Today's Executive Mission"
)


for task in [

    f"Apply to at least {max(5,20-application_count)} executive opportunities.",

    "Contact 3 executive recruiters with personalised messages.",

    f"Prioritise executive positions in {best_market}.",

    "Tailor your CV for every shortlisted role.",

    "Record all recruiter interactions in CRM."

]:

    st.checkbox(task)


divider()


# --------------------------------------------------
# MARKET FOCUS
# --------------------------------------------------

section_header(
    "🌍 Executive Market Focus"
)


market_df = pd.DataFrame(
    [
        {
            "Country": market["country"],
            "Executive Score": market["score"],
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
# RISK MONITOR
# --------------------------------------------------

section_header(
    "⚠ Executive Risk Monitor"
)


if application_count < 10:

    warning_box(
        "Application volume is below recommended level."
    )

else:

    success_box(
        "Application activity is healthy."
    )


if recruiter_count < 10:

    warning_box(
        "Expand your recruiter network."
    )

else:

    success_box(
        "Recruiter network is growing well."
    )


if avg_probability < 70:

    warning_box(
        "Improve ATS alignment and CV tailoring."
    )

else:

    success_box(
        "Interview probability is strong."
    )


divider()


# --------------------------------------------------
# CAREER MOMENTUM
# --------------------------------------------------

section_header(
    "📈 Career Momentum"
)


momentum = int(
    (
        executive_score
        +
        min(application_count * 2,100)
        +
        min(recruiter_count * 5,100)
    )
    / 3
)


metric_row(
    [
        (
            "Career Momentum Score",
            f"{momentum}%"
        )
    ]
)


divider()


# --------------------------------------------------
# AI COACH
# --------------------------------------------------

section_header(
    "🤖 AI Executive Coach"
)


if momentum >= 85:

    coaching_message = """
You are operating at a high executive readiness level.

Continue targeting VP, Country Manager, CRO and COO opportunities.
"""

elif momentum >= 70:

    coaching_message = """
Your executive profile is progressing well.

Increase recruiter engagement and continue tailoring applications.
"""

else:

    coaching_message = """
Consistency is the priority.

Increase quality applications, recruiter outreach and ATS alignment.
"""


info_box(
    coaching_message
)


divider()


# --------------------------------------------------
# RECOMMENDATIONS
# --------------------------------------------------

section_header(
    "📝 Personalised Recommendations"
)


for recommendation in [

    f"Continue prioritising opportunities in {best_market}.",

    "Focus on Director, VP, CRO, COO and Country Manager roles.",

    "Send recruiter follow-ups every 7–10 days.",

    "Tailor executive CV for every shortlisted role.",

    "Track recruiter conversations and interview outcomes.",

    "Review Executive Performance dashboard weekly."

]:

    success_box(
        recommendation
    )


divider()


# --------------------------------------------------
# CHECKLIST
# --------------------------------------------------

section_header(
    "📅 Today's Checklist"
)


for item in [

    "Apply to executive opportunities",

    "Connect with executive recruiters",

    "Send recruiter follow-ups",

    "Update application tracker",

    "Review interview preparation",

    "Improve one section of CV"

]:

    st.checkbox(item)


divider()


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

section_header(
    "🏁 Executive Briefing Summary"
)


summary = pd.DataFrame(
    {
        "Indicator": [
            "Executive Readiness",
            "Career Momentum",
            "Applications",
            "Recruiters",
            "Best Market",
            "Interview Probability",
        ],

        "Current Status": [
            f"{executive_score}%",
            f"{momentum}%",
            application_count,
            recruiter_count,
            best_market,
            f"{avg_probability}%",
        ],
    }
)


st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True,
)


divider()


success_box(
    "✅ AI Executive Advisor operational."
)

st.caption(
    "JobHunter AI • Executive Advisor Suite"
)