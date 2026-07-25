import streamlit as st
import pandas as pd
import json
import os

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Recruiter Intelligence",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Recruiter Intelligence Dashboard")

st.caption(
    "Executive Recruiter Relationship Intelligence"
)

st.divider()


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


if len(recruiters) == 0:

    st.warning(
        "No recruiters available."
    )

    st.stop()


df = pd.DataFrame(recruiters)


# --------------------------------------------------
# KPI DASHBOARD
# --------------------------------------------------

st.subheader("📈 Recruiter KPIs")

k1, k2, k3, k4 = st.columns(4)

with k1:

    st.metric(
        "Total Recruiters",
        len(df)
    )

with k2:

    if "company" in df.columns:

        st.metric(
            "Companies",
            df["company"].nunique()
        )

    else:

        st.metric(
            "Companies",
            "--"
        )

with k3:

    if "country" in df.columns:

        st.metric(
            "Countries",
            df["country"].nunique()
        )

    else:

        st.metric(
            "Countries",
            "--"
        )

with k4:

    st.metric(
        "Pipeline Size",
        len(df)
    )

st.divider()

# --------------------------------------------------
# RECRUITER PIPELINE
# --------------------------------------------------

st.subheader("📋 Recruiter Pipeline")

if "status" not in df.columns:

    df["status"] = "New"

pipeline = (

    df.groupby("status")

    .size()

    .reset_index(name="Recruiters")

    .sort_values(

        "Recruiters",

        ascending=False

    )

)

st.dataframe(

    pipeline,

    use_container_width=True,

    hide_index=True

)

st.divider()


# --------------------------------------------------
# COUNTRY & COMPANY ANALYTICS
# --------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("🌍 Recruiters by Country")

    if "country" in df.columns:

        country_df = (

            df.groupby("country")

            .size()

            .reset_index(name="Recruiters")

            .sort_values(

                "Recruiters",

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

    st.subheader("🏢 Recruiters by Company")

    if "company" in df.columns:

        company_df = (

            df.groupby("company")

            .size()

            .reset_index(name="Recruiters")

            .sort_values(

                "Recruiters",

                ascending=False

            )

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
# RECRUITER DIRECTORY
# --------------------------------------------------

st.subheader("👥 Recruiter Directory")

display_columns = [

    c for c in [

        "name",

        "company",

        "designation",

        "country",

        "status"

    ]

    if c in df.columns

]

st.dataframe(

    df[display_columns],

    use_container_width=True,

    hide_index=True

)

st.divider()

# --------------------------------------------------
# AI RECRUITER INSIGHTS
# --------------------------------------------------

st.subheader("🤖 AI Recruiter Insights")

country_name = "your target markets"

if "country" in df.columns and not df.empty:

    top_country = (

        df.groupby("country")

        .size()

        .sort_values(ascending=False)

        .index[0]

    )

    country_name = top_country


st.success(
    f"""
Your recruiter network currently contains **{len(df)} recruiters**.

Your strongest recruiter presence is in **{country_name}**.

Recommendations:

• Contact 3 recruiters every weekday.
• Follow up with recruiters contacted more than 7 days ago.
• Continue expanding your recruiter network in Singapore, UAE, Germany and other priority markets.
• Personalise every LinkedIn message before sending.
"""
)

st.divider()


# --------------------------------------------------
# DAILY EXECUTIVE ACTIONS
# --------------------------------------------------

st.subheader("🎯 Today's Recruiter Actions")

actions = [

    "Connect with 5 new executive recruiters.",

    "Send 3 personalised LinkedIn messages.",

    "Follow up with existing recruiter conversations.",

    "Update recruiter notes after every interaction.",

    "Identify recruiters in your highest-ranked relocation market."

]

for action in actions:

    st.checkbox(action)


st.divider()


# --------------------------------------------------
# RECRUITER HEALTH SCORE
# --------------------------------------------------

st.subheader("📈 Recruiter Network Health")

health = min(

    100,

    50 + len(df) * 5

)

st.metric(

    "Recruiter Network Score",

    f"{health}%"

)

if health >= 90:

    st.success("Excellent recruiter coverage.")

elif health >= 70:

    st.info("Good recruiter coverage. Continue expanding.")

else:

    st.warning("Increase recruiter outreach to strengthen your network.")


st.divider()


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.success(
    "✅ Recruiter Intelligence Dashboard operational."
)

st.caption(
    "JobHunter AI • Recruiter Intelligence Suite"
)