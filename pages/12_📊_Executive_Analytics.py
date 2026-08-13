import streamlit as st
import pandas as pd

from modules.job_intelligence import JobIntelligence


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Executive Analytics",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# HEADER
# ============================================================

st.title("📊 Executive Analytics")

st.caption(
    "Executive-level intelligence across live job opportunities."
)


# ============================================================
# LOAD JOBS
# ============================================================

jobs = st.session_state.get(
    "executive_jobs",
    [],
)


if not jobs:

    st.warning(
        "No executive jobs are loaded."
    )

    st.info(
        "Go to 🔥 AI Executive Jobs, search for an executive role, "
        "then return here."
    )

    st.stop()


# ============================================================
# ENRICH JOB DATA
# ============================================================

try:

    jobs = JobIntelligence.enrich(
        jobs
    )

except Exception as error:

    st.warning(
        "Job intelligence enrichment could not be completed. "
        "Using available job data."
    )

    st.exception(
        error
    )


# ============================================================
# DATAFRAME
# ============================================================

jobs_df = pd.DataFrame(
    jobs
)


# ============================================================
# SAFE COLUMN HELPERS
# ============================================================

def get_score(
    job,
    field,
    fallback=0,
):

    try:

        return float(
            job.get(
                field,
                fallback,
            )
        )

    except (
        TypeError,
        ValueError,
    ):

        return 0


def job_title(
    job
):

    return str(
        job.get(
            "title",
            job.get(
                "role",
                "Executive Position"
            )
        )
    ).strip()


def company_name(
    job
):

    return str(
        job.get(
            "company",
            "Unknown Company"
        )
    ).strip()


def country_name(
    job
):

    return str(
        job.get(
            "country",
            "Unknown"
        )
    ).strip()


# ============================================================
# INTELLIGENCE SUMMARY
# ============================================================

total_jobs = len(
    jobs
)


apply_jobs = sum(
    1
    for job in jobs
    if job.get(
        "has_apply_link",
        False
    )
)


visa_jobs = sum(
    1
    for job in jobs
    if job.get(
        "has_visa",
        False
    )
)


remote_jobs = sum(
    1
    for job in jobs
    if job.get(
        "is_remote",
        False
    )
)


executive_scores = [
    get_score(
        job,
        "executive_score",
    )
    for job in jobs
]


intelligence_scores = [
    get_score(
        job,
        "intelligence_score",
    )
    for job in jobs
]


avg_executive_score = (
    sum(executive_scores)
    / len(executive_scores)
    if executive_scores
    else 0
)


avg_intelligence_score = (
    sum(intelligence_scores)
    / len(intelligence_scores)
    if intelligence_scores
    else 0
)


apply_rate = (
    apply_jobs
    / total_jobs
    * 100
    if total_jobs
    else 0
)


visa_rate = (
    visa_jobs
    / total_jobs
    * 100
    if total_jobs
    else 0
)


remote_rate = (
    remote_jobs
    / total_jobs
    * 100
    if total_jobs
    else 0
)


# ============================================================
# KPI ROW
# ============================================================

st.subheader(
    "🧠 Executive Job Intelligence"
)


kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(
    6
)


with kpi1:

    st.metric(
        "Live Jobs",
        total_jobs,
    )


with kpi2:

    st.metric(
        "Apply Ready",
        apply_jobs,
    )


with kpi3:

    st.metric(
        "Visa Jobs",
        visa_jobs,
    )


with kpi4:

    st.metric(
        "Remote Jobs",
        remote_jobs,
    )


with kpi5:

    st.metric(
        "Executive Score",
        f"{avg_executive_score:.1f}",
    )


with kpi6:

    st.metric(
        "Intelligence Score",
        f"{avg_intelligence_score:.1f}",
    )


# ============================================================
# OPPORTUNITY RATES
# ============================================================

st.divider()

st.subheader(
    "📈 Opportunity Rates"
)


rate1, rate2, rate3 = st.columns(
    3
)


with rate1:

    st.metric(
        "Apply Link Coverage",
        f"{apply_rate:.1f}%",
    )


with rate2:

    st.metric(
        "Visa Opportunity Rate",
        f"{visa_rate:.1f}%",
    )


with rate3:

    st.metric(
        "Remote Opportunity Rate",
        f"{remote_rate:.1f}%",
    )


# ============================================================
# COUNTRY ANALYTICS
# ============================================================

st.divider()

st.subheader(
    "🌍 Executive Opportunity by Country"
)


country_counts = (
    jobs_df
    .assign(
        country=jobs_df.apply(
            lambda row:
                country_name(
                    row.to_dict()
                ),
            axis=1,
        )
    )
    ["country"]
    .value_counts()
)


if not country_counts.empty:

    country_col1, country_col2 = st.columns(
        2
    )


    with country_col1:

        st.bar_chart(
            country_counts
        )


    with country_col2:

        country_table = (
            country_counts
            .reset_index()
        )

        country_table.columns = [
            "Country",
            "Jobs",
        ]

        st.dataframe(
            country_table,
            use_container_width=True,
            hide_index=True,
        )

else:

    st.info(
        "Country information is not available."
    )


# ============================================================
# COUNTRY QUALITY ANALYSIS
# ============================================================

st.divider()

st.subheader(
    "🏆 Best Markets by Intelligence Score"
)


country_rows = []


for job in jobs:

    country = country_name(
        job
    )


    if not country:

        continue


    country_rows.append(
        {
            "Country": country,
            "Intelligence Score":
                get_score(
                    job,
                    "intelligence_score",
                ),
            "Executive Score":
                get_score(
                    job,
                    "executive_score",
                ),
            "Apply Ready":
                1
                if job.get(
                    "has_apply_link",
                    False
                )
                else 0,
            "Visa":
                1
                if job.get(
                    "has_visa",
                    False
                )
                else 0,
            "Remote":
                1
                if job.get(
                    "is_remote",
                    False
                )
                else 0,
        }
    )


if country_rows:

    country_quality = (
        pd.DataFrame(
            country_rows
        )
        .groupby(
            "Country"
        )
        .agg(
            Jobs=(
                "Country",
                "count",
            ),
            Avg_Intelligence=(
                "Intelligence Score",
                "mean",
            ),
            Avg_Executive_Score=(
                "Executive Score",
                "mean",
            ),
            Apply_Ready=(
                "Apply Ready",
                "sum",
            ),
            Visa_Jobs=(
                "Visa",
                "sum",
            ),
            Remote_Jobs=(
                "Remote",
                "sum",
            ),
        )
        .reset_index()
    )


    country_quality[
        "Avg_Intelligence"
    ] = country_quality[
        "Avg_Intelligence"
    ].round(
        1
    )


    country_quality[
        "Avg_Executive_Score"
    ] = country_quality[
        "Avg_Executive_Score"
    ].round(
        1
    )


    country_quality = (
        country_quality
        .sort_values(
            "Avg_Intelligence",
            ascending=False,
        )
    )


    st.dataframe(
        country_quality,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# COMPANY ANALYTICS
# ============================================================

st.divider()

st.subheader(
    "🏢 Top Companies"
)


company_counts = (
    jobs_df
    .assign(
        company=jobs_df.apply(
            lambda row:
                company_name(
                    row.to_dict()
                ),
            axis=1,
        )
    )
    ["company"]
    .value_counts()
    .head(15)
)


if not company_counts.empty:

    st.bar_chart(
        company_counts
    )


# ============================================================
# ROLE ANALYTICS
# ============================================================

st.divider()

st.subheader(
    "🎯 Executive Roles in Demand"
)


role_counts = (
    jobs_df
    .assign(
        role=jobs_df.apply(
            lambda row:
                job_title(
                    row.to_dict()
                ),
            axis=1,
        )
    )
    ["role"]
    .value_counts()
    .head(15)
)


if not role_counts.empty:

    st.bar_chart(
        role_counts
    )


# ============================================================
# SCORE DISTRIBUTION
# ============================================================

st.divider()

st.subheader(
    "📊 Intelligence Score Distribution"
)


if intelligence_scores:

    score_df = pd.DataFrame(
        {
            "Intelligence Score":
                intelligence_scores
        }
    )


    st.bar_chart(
        score_df
    )


# ============================================================
# APPLY-READY OPPORTUNITIES
# ============================================================

st.divider()

st.subheader(
    "🔗 Apply-Ready Opportunities"
)


apply_ready = [
    job
    for job in jobs
    if job.get(
        "has_apply_link",
        False
    )
]


if apply_ready:

    apply_rows = []


    for job in apply_ready:

        apply_rows.append(
            {
                "Role":
                    job_title(
                        job
                    ),

                "Company":
                    company_name(
                        job
                    ),

                "Country":
                    country_name(
                        job
                    ),

                "Executive Score":
                    get_score(
                        job,
                        "executive_score",
                    ),

                "Intelligence Score":
                    get_score(
                        job,
                        "intelligence_score",
                    ),

                "Apply Link":
                    job.get(
                        "apply_link",
                        job.get(
                            "url",
                            ""
                        )
                    ),
            }
        )


    apply_df = (
        pd.DataFrame(
            apply_rows
        )
        .sort_values(
            "Intelligence Score",
            ascending=False,
        )
    )


    st.dataframe(
        apply_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Apply Link":
                st.column_config.LinkColumn(
                    "Apply",
                    display_text="Open Job",
                )
        },
    )

else:

    st.info(
        "No apply-ready opportunities detected."
    )


# ============================================================
# VISA OPPORTUNITIES
# ============================================================

st.divider()

st.subheader(
    "🛂 Visa Sponsorship Opportunities"
)


visa_opportunities = [
    job
    for job in jobs
    if job.get(
        "has_visa",
        False
    )
]


if visa_opportunities:

    visa_rows = []


    for job in visa_opportunities:

        visa_rows.append(
            {
                "Role":
                    job_title(
                        job
                    ),

                "Company":
                    company_name(
                        job
                    ),

                "Country":
                    country_name(
                        job
                    ),

                "Executive Score":
                    get_score(
                        job,
                        "executive_score",
                    ),

                "Intelligence Score":
                    get_score(
                        job,
                        "intelligence_score",
                    ),
            }
        )


    visa_df = (
        pd.DataFrame(
            visa_rows
        )
        .sort_values(
            "Intelligence Score",
            ascending=False,
        )
    )


    st.dataframe(
        visa_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No visa sponsorship opportunities detected in the current dataset."
    )


# ============================================================
# REMOTE OPPORTUNITIES
# ============================================================

st.divider()

st.subheader(
    "🏠 Remote Opportunities"
)


remote_opportunities = [
    job
    for job in jobs
    if job.get(
        "is_remote",
        False
    )
]


if remote_opportunities:

    remote_rows = []


    for job in remote_opportunities:

        remote_rows.append(
            {
                "Role":
                    job_title(
                        job
                    ),

                "Company":
                    company_name(
                        job
                    ),

                "Country":
                    country_name(
                        job
                    ),

                "Executive Score":
                    get_score(
                        job,
                        "executive_score",
                    ),

                "Intelligence Score":
                    get_score(
                        job,
                        "intelligence_score",
                    ),
            }
        )


    remote_df = (
        pd.DataFrame(
            remote_rows
        )
        .sort_values(
            "Intelligence Score",
            ascending=False,
        )
    )


    st.dataframe(
        remote_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No remote opportunities detected in the current dataset."
    )


# ============================================================
# TOP EXECUTIVE OPPORTUNITIES
# ============================================================

st.divider()

st.subheader(
    "🏆 Top Executive Opportunities"
)


top_rows = []


for job in jobs:

    top_rows.append(
        {
            "Role":
                job_title(
                    job
                ),

            "Company":
                company_name(
                    job
                ),

            "Country":
                country_name(
                    job
                ),

            "Executive Score":
                get_score(
                    job,
                    "executive_score",
                ),

            "Intelligence Score":
                get_score(
                    job,
                    "intelligence_score",
                ),

            "Apply Ready":
                "Yes"
                if job.get(
                    "has_apply_link",
                    False
                )
                else "No",

            "Visa":
                "Yes"
                if job.get(
                    "has_visa",
                    False
                )
                else "No",

            "Remote":
                "Yes"
                if job.get(
                    "is_remote",
                    False
                )
                else "No",
        }
    )


top_df = (
    pd.DataFrame(
        top_rows
    )
    .sort_values(
        "Intelligence Score",
        ascending=False,
    )
    .head(20)
)


st.dataframe(
    top_df,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# SALARY INTELLIGENCE
# ============================================================

st.divider()

st.subheader(
    "💰 Salary Intelligence"
)


if "salary" in jobs_df.columns:

    salary_rows = []


    for job in jobs:

        salary = job.get(
            "salary",
            ""
        )


        if salary:

            salary_rows.append(
                {
                    "Role":
                        job_title(
                            job
                        ),

                    "Company":
                        company_name(
                            job
                        ),

                    "Country":
                        country_name(
                            job
                        ),

                    "Salary":
                        salary,

                    "Executive Score":
                        get_score(
                            job,
                            "executive_score",
                        ),
                }
            )


    if salary_rows:

        salary_df = pd.DataFrame(
            salary_rows
        )


        st.dataframe(
            salary_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No salary information is available in the current job dataset."
        )

else:

    st.info(
        "Salary information is not available from the current job sources."
    )


# ============================================================
# EXECUTIVE RECOMMENDATION
# ============================================================

st.divider()

st.subheader(
    "🤖 Executive Intelligence Summary"
)


if "country_quality" in locals() and not country_quality.empty:

    best_country = country_quality.iloc[0]

    st.success(
        f"🏆 Strongest current market: "
        f"{best_country['Country']} — "
        f"{int(best_country['Jobs'])} jobs, "
        f"average intelligence score "
        f"{best_country['Avg_Intelligence']:.1f}."
    )


if apply_jobs:

    st.info(
        f"🔗 {apply_jobs} opportunities currently have a usable application link."
    )


if visa_jobs:

    st.info(
        f"🛂 {visa_jobs} opportunities currently indicate visa sponsorship."
    )


if remote_jobs:

    st.info(
        f"🏠 {remote_jobs} opportunities currently appear remote-friendly."
    )


st.success(
    "Executive Analytics Ready"
)