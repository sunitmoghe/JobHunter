import streamlit as st

from modules.application_manager import ApplicationManager
from modules.recruiter_manager import RecruiterManager
from modules.saved_jobs_manager import SavedJobsManager


st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)


st.title("📊 Analytics Dashboard")

st.caption(
    "Your executive job-search command center."
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:

    applications = (
        ApplicationManager()
        .get_all_applications()
    )

except Exception:

    applications = []


try:

    recruiters = (
        RecruiterManager()
        .get_all_recruiters()
    )

except Exception:

    recruiters = []


try:

    saved_manager = SavedJobsManager()

    if hasattr(
        saved_manager,
        "get_all_saved_jobs",
    ):

        saved_jobs = (
            saved_manager
            .get_all_saved_jobs()
        )

    elif hasattr(
        saved_manager,
        "get_saved_jobs",
    ):

        saved_jobs = (
            saved_manager
            .get_saved_jobs()
        )

    else:

        saved_jobs = []

except Exception:

    saved_jobs = []


jobs = st.session_state.get(
    "executive_jobs",
    [],
)


# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_jobs = len(jobs)

total_applications = len(
    applications
)

total_saved = len(
    saved_jobs
)

total_recruiters = len(
    recruiters
)


countries = sorted(
    set(
        job.get(
            "country",
            ""
        )
        for job in jobs
        if job.get("country")
    )
)


companies = sorted(
    set(
        job.get(
            "company",
            ""
        )
        for job in jobs
        if job.get("company")
    )
)


scores = []

for job in jobs:

    try:

        scores.append(
            float(
                job.get(
                    "executive_score",
                    0
                )
            )
        )

    except Exception:

        pass


average_score = (
    round(
        sum(scores) / len(scores),
        1,
    )
    if scores
    else 0
)


# --------------------------------------------------
# KPI ROW
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🔥 Jobs Found",
        total_jobs,
    )


with col2:

    st.metric(
        "🌍 Countries",
        len(countries),
    )


with col3:

    st.metric(
        "🏢 Companies",
        len(companies),
    )


with col4:

    st.metric(
        "🎯 Avg Executive Fit",
        f"{average_score}%",
    )


st.divider()


# --------------------------------------------------
# SECOND KPI ROW
# --------------------------------------------------

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "📌 Applications",
        total_applications,
    )


with col2:

    st.metric(
        "💾 Saved Jobs",
        total_saved,
    )


with col3:

    st.metric(
        "👥 Recruiters",
        total_recruiters,
    )


st.divider()


# --------------------------------------------------
# APPLICATION PIPELINE
# --------------------------------------------------

st.subheader(
    "📈 Application Pipeline"
)


statuses = [
    "Applied",
    "Interview",
    "Offer",
    "Rejected",
    "Withdrawn",
]


status_counts = {}

for status in statuses:

    status_counts[status] = sum(
        1
        for application in applications
        if application.get(
            "status",
            "Applied",
        ) == status
    )


cols = st.columns(
    len(statuses)
)


for column, status in zip(
    cols,
    statuses,
):

    with column:

        st.metric(
            status,
            status_counts[status],
        )


st.divider()


# --------------------------------------------------
# TOP JOBS
# --------------------------------------------------

st.subheader(
    "⭐ Top Executive Opportunities"
)


if not jobs:

    st.info(
        "Search for executive jobs first "
        "to populate this dashboard."
    )

else:

    top_jobs = sorted(
        jobs,
        key=lambda job: float(
            job.get(
                "executive_score",
                0
            )
            or 0
        ),
        reverse=True,
    )[:10]


    for index, job in enumerate(
        top_jobs,
        start=1,
    ):

        title = job.get(
            "title",
            job.get(
                "role",
                "Executive Position",
            ),
        )

        company = job.get(
            "company",
            "Company",
        )

        location = job.get(
            "location",
            "",
        )

        score = job.get(
            "executive_score",
            0,
        )

        apply_link = job.get(
            "apply_link",
            "",
        )

        if not apply_link:

            apply_link = job.get(
                "url",
                "",
            )


        with st.container(
            border=True
        ):

            col1, col2, col3 = st.columns(
                [5, 3, 2]
            )


            with col1:

                st.markdown(
                    f"**{index}. {title}**"
                )

                st.write(
                    f"{company}"
                )

                if location:

                    st.caption(
                        location
                    )


            with col2:

                st.metric(
                    "Executive Fit",
                    f"{score}%",
                )


            with col3:

                if apply_link:

                    st.link_button(
                        "🚀 Apply",
                        apply_link,
                        use_container_width=True,
                    )


st.divider()


# --------------------------------------------------
# COUNTRIES
# --------------------------------------------------

st.subheader(
    "🌍 Job Market Coverage"
)


if countries:

    st.write(
        ", ".join(countries)
    )

else:

    st.info(
        "No country data available yet."
    )


# --------------------------------------------------
# COMPANIES
# --------------------------------------------------

st.subheader(
    "🏢 Companies Discovered"
)


if companies:

    st.write(
        ", ".join(
            companies[:50]
        )
    )

else:

    st.info(
        "No company data available yet."
    )