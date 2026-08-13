import streamlit as st

from modules.executive_ai_agent import ExecutiveAIAgent
from modules.saved_jobs_manager import SavedJobsManager
from modules.application_manager import ApplicationManager


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Executive Jobs",
    page_icon="🔥",
    layout="wide",
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🔥 AI Executive Jobs")

st.caption(
    "Live AI-powered executive job discovery, scoring, filtering and application tracking."
)


# ============================================================
# MANAGERS
# ============================================================

agent = ExecutiveAIAgent()

saved_manager = SavedJobsManager()

application_manager = ApplicationManager()


# ============================================================
# SESSION STATE
# ============================================================

if "executive_jobs" not in st.session_state:

    st.session_state[
        "executive_jobs"
    ] = []


# ============================================================
# SEARCH SECTION
# ============================================================

st.subheader(
    "🎯 Search Executive Jobs"
)


role = st.text_input(
    "Executive Role",
    value="Head of Sales",
    help="Enter the executive position you want to search for.",
)


search_col1, search_col2 = st.columns(
    [4, 1]
)


with search_col1:

    search_button = st.button(
        "🔎 SEARCH LIVE EXECUTIVE JOBS",
        type="primary",
        use_container_width=True,
    )


with search_col2:

    clear_button = st.button(
        "🗑️ CLEAR",
        use_container_width=True,
    )


if clear_button:

    st.session_state[
        "executive_jobs"
    ] = []

    st.rerun()


if search_button:

    if not role.strip():

        st.warning(
            "Please enter an executive role."
        )

    else:

        with st.spinner(
            "Searching live executive opportunities..."
        ):

            try:

                jobs = agent.search_jobs(
                    role=role.strip()
                )

                st.session_state[
                    "executive_jobs"
                ] = jobs

                st.success(
                    f"Search completed. {len(jobs)} opportunities found."
                )

            except Exception as error:

                st.error(
                    "Job search failed."
                )

                st.exception(
                    error
                )


# ============================================================
# LOAD JOBS
# ============================================================

jobs = st.session_state.get(
    "executive_jobs",
    [],
)


# ============================================================
# INTELLIGENCE SUMMARY
# ============================================================

if jobs:

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
        or job.get(
            "apply_link",
            ""
        )
        or job.get(
            "url",
            ""
        )
        or job.get(
            "redirect_url",
            ""
        )
    )


    visa_jobs = sum(
        1
        for job in jobs
        if job.get(
            "has_visa",
            False
        )
        or job.get(
            "visa_sponsorship",
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


    scores = []

    for job in jobs:

        try:

            scores.append(
                float(
                    job.get(
                        "intelligence_score",
                        job.get(
                            "executive_score",
                            0
                        )
                    )
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            pass


    average_score = (
        sum(scores) / len(scores)
        if scores
        else 0
    )


    st.divider()

    st.subheader(
        "🧠 Job Intelligence"
    )


    metric1, metric2, metric3, metric4, metric5 = st.columns(
        5
    )


    with metric1:

        st.metric(
            "Total Jobs",
            total_jobs,
        )


    with metric2:

        st.metric(
            "Apply Ready",
            apply_jobs,
        )


    with metric3:

        st.metric(
            "Visa Jobs",
            visa_jobs,
        )


    with metric4:

        st.metric(
            "Remote Jobs",
            remote_jobs,
        )


    with metric5:

        st.metric(
            "Avg Intelligence",
            f"{average_score:.1f}",
        )


# ============================================================
# FILTERS
# ============================================================

st.divider()

st.subheader(
    "🎛️ Job Intelligence Filters"
)


countries = sorted(
    {
        str(
            job.get(
                "country",
                ""
            )
        ).strip()
        for job in jobs
        if str(
            job.get(
                "country",
                ""
            )
        ).strip()
    }
)


filter1, filter2, filter3 = st.columns(
    3
)


with filter1:

    selected_country = st.selectbox(
        "🌍 Country",
        ["All"] + countries,
    )


with filter2:

    minimum_score = st.slider(
        "🎯 Minimum Intelligence Score",
        min_value=0,
        max_value=100,
        value=0,
        step=5,
    )


with filter3:

    sort_by = st.selectbox(
        "📊 Sort By",
        [
            "Best Match",
            "Executive Score",
            "Newest",
            "Company",
        ],
    )


filter4, filter5, filter6 = st.columns(
    3
)


with filter4:

    remote_only = st.checkbox(
        "🏠 Remote Only"
    )


with filter5:

    visa_only = st.checkbox(
        "🛂 Visa Sponsorship Only"
    )


with filter6:

    apply_only = st.checkbox(
        "🔗 Apply Link Available Only"
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_jobs = []


for job in jobs:

    # --------------------------------------------------------
    # COUNTRY
    # --------------------------------------------------------

    job_country = str(
        job.get(
            "country",
            ""
        )
    ).strip()


    if (
        selected_country != "All"
        and job_country != selected_country
    ):

        continue


    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    try:

        intelligence_score = float(
            job.get(
                "intelligence_score",
                job.get(
                    "executive_score",
                    0
                )
            )
        )

    except (
        TypeError,
        ValueError,
    ):

        intelligence_score = 0


    if intelligence_score < minimum_score:

        continue


    # --------------------------------------------------------
    # REMOTE
    # --------------------------------------------------------

    is_remote = job.get(
        "is_remote",
        False
    )


    if remote_only and not is_remote:

        continue


    # --------------------------------------------------------
    # VISA
    # --------------------------------------------------------

    has_visa = job.get(
        "has_visa",
        False
    )


    if not has_visa:

        visa_value = job.get(
            "visa_sponsorship",
            False
        )

        if isinstance(
            visa_value,
            str
        ):

            has_visa = (
                visa_value.lower()
                in [
                    "true",
                    "yes",
                    "available",
                    "sponsored",
                    "sponsorship",
                ]
            )

        else:

            has_visa = bool(
                visa_value
            )


    if visa_only and not has_visa:

        continue


    # --------------------------------------------------------
    # APPLY LINK
    # --------------------------------------------------------

    apply_link = job.get(
        "apply_link",
        ""
    )


    if not apply_link:

        apply_link = job.get(
            "url",
            ""
        )


    if not apply_link:

        apply_link = job.get(
            "redirect_url",
            ""
        )


    if apply_only and not apply_link:

        continue


    # --------------------------------------------------------
    # STORE TEMPORARY FIELDS
    # --------------------------------------------------------

    display_job = dict(
        job
    )

    display_job[
        "_display_score"
    ] = intelligence_score

    display_job[
        "_apply_link"
    ] = apply_link

    display_job[
        "_has_visa"
    ] = has_visa

    filtered_jobs.append(
        display_job
    )


# ============================================================
# SORT RESULTS
# ============================================================

if sort_by == "Best Match":

    filtered_jobs.sort(
        key=lambda job:
            float(
                job.get(
                    "_display_score",
                    0
                )
            ),
        reverse=True,
    )


elif sort_by == "Executive Score":

    filtered_jobs.sort(
        key=lambda job:
            float(
                job.get(
                    "executive_score",
                    0
                )
            ),
        reverse=True,
    )


elif sort_by == "Newest":

    filtered_jobs.sort(
        key=lambda job:
            str(
                job.get(
                    "posted_date",
                    ""
                )
            ),
        reverse=True,
    )


elif sort_by == "Company":

    filtered_jobs.sort(
        key=lambda job:
            str(
                job.get(
                    "company",
                    ""
                )
            ).lower()
    )


# ============================================================
# RESULT COUNT
# ============================================================

st.divider()

st.subheader(
    f"📊 Showing {len(filtered_jobs)} of {len(jobs)} Jobs"
)


if not filtered_jobs:

    if jobs:

        st.warning(
            "No jobs match the current filters. Try lowering the score or removing a filter."
        )

    else:

        st.info(
            "No jobs loaded yet. Enter an executive role and click SEARCH LIVE EXECUTIVE JOBS."
        )


# ============================================================
# JOB CARDS
# ============================================================

for index, job in enumerate(
    filtered_jobs,
    start=1,
):

    title = job.get(
        "title",
        job.get(
            "role",
            "Executive Position"
        )
    )


    company = job.get(
        "company",
        "Company"
    )


    location = job.get(
        "location",
        ""
    )


    country = job.get(
        "country",
        ""
    )


    executive_score = job.get(
        "executive_score",
        0
    )


    intelligence_score = job.get(
        "_display_score",
        executive_score
    )


    priority = job.get(
        "priority",
        ""
    )


    recommendation = job.get(
        "recommendation",
        ""
    )


    apply_link = job.get(
        "_apply_link",
        ""
    )


    has_visa = job.get(
        "_has_visa",
        False
    )


    is_remote = job.get(
        "is_remote",
        False
    )


    description = job.get(
        "description",
        ""
    )


    # ========================================================
    # JOB CARD
    # ========================================================

    with st.container(
        border=True
    ):

        st.markdown(
            f"### {index}. {title}"
        )


        # ----------------------------------------------------
        # BASIC INFORMATION
        # ----------------------------------------------------

        info1, info2, info3 = st.columns(
            3
        )


        with info1:

            st.write(
                f"**Company:** {company}"
            )


        with info2:

            if location:

                st.write(
                    f"**Location:** {location}"
                )

            elif country:

                st.write(
                    f"**Country:** {country}"
                )


        with info3:

            if country:

                st.write(
                    f"**Market:** {country}"
                )


        # ----------------------------------------------------
        # SCORE ROW
        # ----------------------------------------------------

        score1, score2, score3, score4 = st.columns(
            4
        )


        with score1:

            st.metric(
                "Executive Fit",
                f"{executive_score}%",
            )


        with score2:

            st.metric(
                "Intelligence",
                f"{intelligence_score:.1f}",
            )


        with score3:

            if priority:

                st.metric(
                    "Priority",
                    priority,
                )


        with score4:

            if recommendation:

                st.metric(
                    "Recommendation",
                    recommendation,
                )


        # ----------------------------------------------------
        # INTELLIGENCE FLAGS
        # ----------------------------------------------------

        flags = []


        if apply_link:

            flags.append(
                "🔗 Apply Ready"
            )


        if has_visa:

            flags.append(
                "🛂 Visa"
            )


        if is_remote:

            flags.append(
                "🏠 Remote"
            )


        if flags:

            st.write(
                "  |  ".join(flags)
            )


        st.divider()


        # ----------------------------------------------------
        # ACTION BUTTONS
        # ----------------------------------------------------

        action1, action2, action3 = st.columns(
            3
        )


        with action1:

            if apply_link:

                if st.button(
                    "🚀 APPLY NOW",
                    key=f"apply_{index}",
                    use_container_width=True,
                    type="primary",
                ):

                    try:

                        application_manager.add_application(
                            job
                        )

                        st.success(
                            "Application recorded."
                        )

                        st.markdown(
                            f"[Open Job Application ↗]({apply_link})"
                        )

                    except Exception as error:

                        st.error(
                            "Application could not be recorded."
                        )

                        st.exception(
                            error
                        )

            else:

                st.warning(
                    "No application URL available."
                )


        with action2:

            if st.button(
                "💾 SAVE JOB",
                key=f"save_{index}",
                use_container_width=True,
            ):

                try:

                    saved = (
                        saved_manager.save_job(
                            job
                        )
                    )

                    if saved:

                        st.success(
                            "Job saved."
                        )

                    else:

                        st.info(
                            "Job already saved."
                        )

                except Exception as error:

                    st.error(
                        "Could not save job."
                    )

                    st.exception(
                        error
                    )


        with action3:

            if apply_link:

                st.link_button(
                    "🔗 OPEN JOB",
                    apply_link,
                    use_container_width=True,
                )


        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        if description:

            with st.expander(
                "📄 Job Description"
            ):

                st.write(
                    description
                )


        # ----------------------------------------------------
        # SCORE DETAILS
        # ----------------------------------------------------

        score_details = job.get(
            "score_details",
            {}
        )


        if score_details:

            with st.expander(
                "🧠 AI Score Details"
            ):

                st.json(
                    score_details
                )