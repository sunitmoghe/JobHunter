import streamlit as st
import pandas as pd
import json
import os

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
    page_title="Recruiter Intelligence",
    page_icon="👥",
    layout="wide",
)


page_header(
    "👥 Recruiter Intelligence Dashboard",
    "Executive Recruiter Relationship Intelligence"
)


# --------------------------------------------------
# LOAD RECRUITERS
# --------------------------------------------------

RECRUITER_FILE = "database/recruiters.json"


if os.path.exists(RECRUITER_FILE):

    with open(
        RECRUITER_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        recruiters = json.load(f)

else:

    recruiters = []


if not recruiters:

    empty_state(
        "No recruiters available."
    )

    st.stop()


df = pd.DataFrame(
    recruiters
)


# --------------------------------------------------
# KPI DASHBOARD
# --------------------------------------------------

section_header(
    "📈 Recruiter KPIs"
)


metric_row(
    [
        (
            "Total Recruiters",
            len(df)
        ),

        (
            "Companies",
            df["company"].nunique()
            if "company" in df.columns
            else "--"
        ),

        (
            "Countries",
            df["country"].nunique()
            if "country" in df.columns
            else "--"
        ),

        (
            "Pipeline Size",
            len(df)
        ),
    ]
)


divider()


# --------------------------------------------------
# PIPELINE
# --------------------------------------------------

section_header(
    "📋 Recruiter Pipeline"
)


if "status" not in df.columns:

    df["status"] = "New"


pipeline = (
    df.groupby("status")
    .size()
    .reset_index(
        name="Recruiters"
    )
    .sort_values(
        "Recruiters",
        ascending=False
    )
)


st.dataframe(
    pipeline,
    use_container_width=True,
    hide_index=True,
)


divider()


# --------------------------------------------------
# ANALYTICS
# --------------------------------------------------

section_header(
    "🌍 Recruiter Network Analytics"
)


left, right = st.columns(2)


with left:

    st.write(
        "### 🌍 Recruiters by Country"
    )

    if "country" in df.columns:

        country_df = (
            df.groupby("country")
            .size()
            .reset_index(
                name="Recruiters"
            )
            .sort_values(
                "Recruiters",
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
        "### 🏢 Recruiters by Company"
    )

    if "company" in df.columns:

        company_df = (
            df.groupby("company")
            .size()
            .reset_index(
                name="Recruiters"
            )
            .sort_values(
                "Recruiters",
                ascending=False
            )
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
# DIRECTORY
# --------------------------------------------------

section_header(
    "👥 Recruiter Directory"
)


display_columns = [
    c for c in [
        "name",
        "company",
        "designation",
        "country",
        "status",
    ]
    if c in df.columns
]


st.dataframe(
    df[display_columns],
    use_container_width=True,
    hide_index=True,
)


divider()


# --------------------------------------------------
# AI INSIGHTS
# --------------------------------------------------

section_header(
    "🤖 AI Recruiter Insights"
)


country_name = "your target markets"


if (
    "country" in df.columns
    and not df.empty
):

    country_name = (
        df.groupby("country")
        .size()
        .sort_values(
            ascending=False
        )
        .index[0]
    )


success_box(
    f"""
Your recruiter network currently contains **{len(df)} recruiters**.

Strongest recruiter presence:
**{country_name}**

Recommendations:

• Contact 3 recruiters every weekday.
• Follow up after 7 days.
• Expand recruiter coverage in priority markets.
• Personalise every LinkedIn message.
"""
)


divider()


# --------------------------------------------------
# ACTIONS
# --------------------------------------------------

section_header(
    "🎯 Today's Recruiter Actions"
)


for action in [

    "Connect with 5 new executive recruiters.",

    "Send 3 personalised LinkedIn messages.",

    "Follow up with existing recruiter conversations.",

    "Update recruiter notes after every interaction.",

    "Identify recruiters in your highest-ranked market.",

]:

    st.checkbox(
        action
    )


divider()


# --------------------------------------------------
# HEALTH SCORE
# --------------------------------------------------

section_header(
    "📈 Recruiter Network Health"
)


health = min(
    100,
    50 + len(df) * 5
)


metric_row(
    [
        (
            "Recruiter Network Score",
            f"{health}%"
        )
    ]
)


if health >= 90:

    success_box(
        "Excellent recruiter coverage."
    )

elif health >= 70:

    info_box(
        "Good recruiter coverage. Continue expanding."
    )

else:

    warning_box(
        "Increase recruiter outreach to strengthen your network."
    )


divider()


success_box(
    "✅ Recruiter Intelligence Dashboard operational."
)


st.caption(
    "JobHunter AI • Recruiter Intelligence Suite"
)