import streamlit as st
import pandas as pd

from modules.global_job_discovery_engine import (
    GlobalJobDiscoveryEngine,
)


st.set_page_config(
    page_title="Global Opportunity Center",
    page_icon="📊",
    layout="wide",
)


st.title("📊 Global Executive Opportunity Center")

st.caption(
    "High-volume global job discovery with freshness-first prioritization."
)


engine = GlobalJobDiscoveryEngine()


# ==========================================================
# SEARCH CONTROLS
# ==========================================================

st.subheader("🌍 Global Job Search")

col1, col2 = st.columns(2)

with col1:

    role = st.text_input(
        "Executive Role",
        value="Head of Sales",
    )

with col2:

    countries = st.multiselect(
        "Countries",
        list(
            engine.COUNTRIES.keys()
        ),
        default=[
            "India",
            "Singapore",
            "Germany",
            "Australia",
            "Austria",
            "Romania",
            "Greece",
        ],
    )


col3, col4, col5 = st.columns(3)

with col3:

    pages = st.number_input(
        "Pages per country",
        min_value=1,
        max_value=10,
        value=2,
        step=1,
    )

with col4:

    results_per_page = st.number_input(
        "Results per page",
        min_value=10,
        max_value=50,
        value=20,
        step=5,
    )

with col5:

    freshness_filter = st.selectbox(
        "Freshness",
        [
            "All Jobs",
            "Last 12 Hours",
            "Last 24 Hours",
            "Last 36 Hours",
            "Last 48 Hours",
            "Last 72 Hours",
            "Last 7 Days",
        ],
    )


search = st.button(
    "🔎 Search Global Jobs",
    type="primary",
    use_container_width=True,
)


# ==========================================================
# SEARCH
# ==========================================================

if search:

    if not role.strip():

        st.error(
            "Enter an executive role."
        )

    elif not countries:

        st.error(
            "Select at least one country."
        )

    else:

        freshness_hours = {
            "All Jobs": None,
            "Last 12 Hours": 12,
            "Last 24 Hours": 24,
            "Last 36 Hours": 36,
            "Last 48 Hours": 48,
            "Last 72 Hours": 72,
            "Last 7 Days": 168,
        }[
            freshness_filter
        ]

        with st.spinner(
            "Searching global job sources..."
        ):

            try:

                jobs = engine.search(
                    role=role.strip(),
                    countries=countries,
                    pages=int(pages),
                    results_per_page=int(
                        results_per_page
                    ),
                    freshness_hours=freshness_hours,
                )

                st.session_state[
                    "global_opportunity_jobs"
                ] = jobs

                st.session_state[
                    "global_opportunity_role"
                ] = role.strip()

            except Exception as error:

                st.error(
                    "Global search failed."
                )

                st.exception(
                    error
                )


# ==========================================================
# LOAD RESULTS
# ==========================================================

jobs = st.session_state.get(
    "global_opportunity_jobs",
    [],
)


if jobs:

    st.divider()

    # ======================================================
    # SUMMARY
    # ======================================================

    summary = engine.freshness_summary(
        jobs
    )

    st.subheader(
        "🔥 Opportunity Summary"
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric(
            "Total Jobs",
            summary["total"],
        )

    with c2:
        st.metric(
            "Last 12h",
            summary["last_12_hours"],
        )

    with c3:
        st.metric(
            "Last 24h",
            summary["last_24_hours"],
        )

    with c4:
        st.metric(
            "Last 48h",
            summary["last_48_hours"],
        )

    with c5:
        st.metric(
            "Last 7 Days",
            summary["last_7_days"],
        )


    st.divider()


    # ======================================================
    # TABLE
    # ======================================================

    st.subheader(
        f"📋 Opportunities: {len(jobs)}"
    )

    table_rows = []

    for job in jobs:

        table_rows.append(
            {
                "Urgency":
                    job.get(
                        "freshness_bucket",
                        "UNKNOWN",
                    ),

                "Role":
                    job.get(
                        "role",
                        "",
                    ),

                "Company":
                    job.get(
                        "company",
                        "",
                    ),

                "Country":
                    job.get(
                        "country",
                        "",
                    ),

                "Age (hrs)":
                    job.get(
                        "age_hours",
                        "",
                    ),

                "Salary":
                    job.get(
                        "salary",
                        "Not Disclosed",
                    ),

                "Source":
                    job.get(
                        "source",
                        "",
                    ),
            }
        )

    table_df = pd.DataFrame(
        table_rows
    )


    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True,
    )


    st.divider()


    # ======================================================
    # DETAILED JOB CARDS
    # ======================================================

    st.subheader(
        "🎯 Job Details"
    )

    for index, job in enumerate(
        jobs,
        start=1,
    ):

        urgency = job.get(
            "freshness_bucket",
            "UNKNOWN",
        )

        label = job.get(
            "freshness_label",
            "Posting age unavailable",
        )

        if urgency == "IMMEDIATE":

            badge = "🚨"

        elif urgency == "VERY HIGH":

            badge = "🔥"

        elif urgency == "HIGH":

            badge = "🟠"

        elif urgency == "PRIORITY":

            badge = "🟡"

        elif urgency == "NORMAL":

            badge = "🔵"

        else:

            badge = "⚪"


        role_name = job.get(
            "role",
            "Executive Position",
        )

        company = job.get(
            "company",
            "Unknown Company",
        )

        country = job.get(
            "country",
            "",
        )

        location = job.get(
            "location",
            "",
        )

        salary = job.get(
            "salary",
            "Not Disclosed",
        )

        source = job.get(
            "source",
            "",
        )

        apply_link = job.get(
            "apply_link",
            "",
        )

        age_hours = job.get(
            "age_hours",
            None,
        )

        with st.container(
            border=True
        ):

            title_col, urgency_col = st.columns(
                [5, 2]
            )

            with title_col:

                st.markdown(
                    f"### {index}. {role_name}"
                )

                st.write(
                    f"**{company}**"
                )

                if location or country:

                    location_text = " | ".join(
                        item
                        for item in [
                            location,
                            country,
                        ]
                        if item
                    )

                    st.write(
                        f"📍 {location_text}"
                    )

            with urgency_col:

                st.markdown(
                    f"### {badge} {urgency}"
                )

                st.caption(
                    label
                )


            info1, info2, info3 = st.columns(3)

            with info1:

                if age_hours is None:

                    st.metric(
                        "Posted Age",
                        "Unknown",
                    )

                elif job.get(
                    "future_timestamp",
                    False,
                ):

                    st.metric(
                        "Posted Age",
                        "Just posted",
                    )

                else:

                    st.metric(
                        "Posted Age",
                        f"{age_hours:.1f} hrs",
                    )

            with info2:

                st.metric(
                    "Salary",
                    salary,
                )

            with info3:

                st.metric(
                    "Source",
                    source,
                )


            action_col1, action_col2 = st.columns(
                2
            )

            with action_col1:

                if apply_link:

                    st.link_button(
                        "🚀 Open Application",
                        apply_link,
                        use_container_width=True,
                    )

                else:

                    st.info(
                        "Application URL unavailable."
                    )

            with action_col2:

                if st.button(
                    "📄 View Description",
                    key=f"description_{index}",
                    use_container_width=True,
                ):

                    st.session_state[
                        f"show_description_{index}"
                    ] = True


            if st.session_state.get(
                f"show_description_{index}",
                False,
            ):

                description = job.get(
                    "description",
                    "No description available.",
                )

                with st.expander(
                    "Job Description",
                    expanded=True,
                ):

                    st.write(
                        description
                    )


else:

    st.info(
        "Search for an executive role to load the global opportunity pool."
    )