import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Executive Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Executive Analytics")

jobs = st.session_state.get("executive_jobs", [])

applications = st.session_state.get("applications", [])

if not jobs:
    st.warning("Search jobs first from AI Executive Jobs.")
    st.stop()

jobs_df = pd.DataFrame(jobs)

st.subheader("Executive Job Analytics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Live Jobs",
        len(jobs_df)
    )

with col2:
    st.metric(
        "Companies",
        jobs_df["company"].nunique() if "company" in jobs_df else 0
    )

with col3:
    st.metric(
        "Countries",
        jobs_df["country"].nunique() if "country" in jobs_df else 0
    )

with col4:
    if "executive_score" in jobs_df:
        st.metric(
            "Avg Executive Score",
            round(jobs_df["executive_score"].mean(),1)
        )

st.divider()

st.subheader("Top Countries")

if "country" in jobs_df:

    st.bar_chart(
        jobs_df["country"].value_counts()
    )

st.divider()

st.subheader("Top Companies")

if "company" in jobs_df:

    st.bar_chart(
        jobs_df["company"].value_counts().head(10)
    )

st.divider()

st.subheader("Executive Score Distribution")

if "executive_score" in jobs_df:

    st.line_chart(
        jobs_df["executive_score"]
    )

st.divider()

st.subheader("Visa Sponsorship")

if "visa_sponsorship" in jobs_df:

    visa = jobs_df["visa_sponsorship"].value_counts()

    st.bar_chart(visa)

st.divider()

st.subheader("Remote Jobs")

if "remote_friendly" in jobs_df:

    remote = jobs_df["remote_friendly"].value_counts()

    st.bar_chart(remote)

st.divider()

st.subheader("Highest Executive Scores")

if "executive_score" in jobs_df:

    top = jobs_df.sort_values(
        "executive_score",
        ascending=False
    )

    cols = [
        c for c in [
            "role",
            "company",
            "country",
            "executive_score"
        ]
        if c in top.columns
    ]

    st.dataframe(
        top[cols].head(20),
        use_container_width=True,
        hide_index=True
    )

st.divider()

st.divider()

st.subheader("🌍 Executive Jobs Table")

columns = [
    c for c in [
        "role",
        "company",
        "country",
        "executive_score",
        "jobhunter_score",
        "visa_sponsorship",
        "remote_friendly"
    ]
    if c in jobs_df.columns
]

st.dataframe(
    jobs_df[columns],
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("🏆 Top 10 Executive Jobs")

if "executive_score" in jobs_df:

    top10 = jobs_df.sort_values(
        "executive_score",
        ascending=False
    ).head(10)

    st.dataframe(
        top10[columns],
        use_container_width=True,
        hide_index=True
    )

st.divider()

st.subheader("💰 Salary Intelligence")

if "salary" in jobs_df.columns:

    salary_df = jobs_df[jobs_df["salary"].notna()]

    if not salary_df.empty:

        st.dataframe(
            salary_df[
                [
                    c for c in [
                        "role",
                        "company",
                        "country",
                        "salary"
                    ]
                    if c in salary_df.columns
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info("No salary information available.")

else:

    st.info("Salary column not found.")

st.divider()

st.subheader("🏢 Executive Hiring Countries")

if "country" in jobs_df.columns:

    countries = (
        jobs_df["country"]
        .value_counts()
        .reset_index()
    )

    countries.columns = [
        "Country",
        "Jobs",
    ]

    st.dataframe(
        countries,
        use_container_width=True,
        hide_index=True,
    )

st.divider()

st.subheader("🌍 Visa Sponsorship Opportunities")

if "visa_sponsorship" in jobs_df.columns:

    visa_jobs = jobs_df[
        jobs_df["visa_sponsorship"] == True
    ]

    if not visa_jobs.empty:

        cols = [
            c for c in [
                "role",
                "company",
                "country",
                "executive_score",
            ]
            if c in visa_jobs.columns
        ]

        st.dataframe(
            visa_jobs[cols],
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info("No visa sponsorship jobs found.")

st.success("Executive Analytics Ready")