import streamlit as st

from modules.dashboard_engine import DashboardEngine
from modules.executive_ai_agent import ExecutiveAIAgent
from modules.executive_action_center import ExecutiveActionCenter


st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide",
)


st.title("📊 Executive Dashboard")


# ==========================================================
# DASHBOARD ENGINE
# ==========================================================

engine = DashboardEngine()

stats = engine.get_dashboard_stats()


# ==========================================================
# KPI SECTION
# ==========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🎯 Total Jobs",
        stats.get(
            "total_jobs",
            0
        ),
    )


with col2:

    st.metric(
        "💾 Saved Jobs",
        stats.get(
            "saved_jobs",
            0
        ),
    )


with col3:

    st.metric(
        "📤 Applied Jobs",
        stats.get(
            "applied_jobs",
            0
        ),
    )


with col4:

    st.metric(
        "🌍 Countries",
        stats.get(
            "countries",
            0
        ),
    )


st.divider()


col5, col6, col7 = st.columns(3)


with col5:

    st.metric(
        "🏢 Companies",
        stats.get(
            "companies",
            0
        ),
    )


with col6:

    st.metric(
        "📈 Avg Opportunity Score",
        stats.get(
            "avg_opportunity",
            0
        ),
    )


with col7:

    st.metric(
        "🔥 Action Center",
        "READY",
    )


st.divider()


# ==========================================================
# EXECUTIVE QUICK ACTIONS
# ==========================================================

st.subheader(
    "🚀 Executive Quick Actions"
)


a, b, c, d = st.columns(4)


with a:

    st.page_link(
        "pages/4_🔥_AI_Executive_Jobs.py",
        label="🔥 AI Executive Jobs",
    )


with b:

    st.page_link(
        "pages/2_📄_Resume_Intelligence.py",
        label="📄 Resume Intelligence",
    )


with c:

    st.page_link(
        "pages/3_🎯_ATS_Matcher.py",
        label="🎯 ATS Matcher",
    )


with d:

    st.page_link(
        "pages/5_👥_Recruiter_CRM.py",
        label="👥 Recruiter CRM",
    )


st.divider()


# ==========================================================
# EXECUTIVE ACTION CENTER
# ==========================================================

st.subheader(
    "🔥 Executive Action Center"
)


st.markdown(
    """
    Identify the highest-priority executive opportunities from
    the live job search and decide what action should be taken.
    """
)


# ----------------------------------------------------------
# Search controls
# ----------------------------------------------------------

search_col1, search_col2 = st.columns(
    [3, 1]
)


with search_col1:

    role = st.text_input(
        "Executive role",
        value="Head of Sales",
    )


with search_col2:

    limit = st.number_input(
        "Top jobs",
        min_value=5,
        max_value=30,
        value=10,
        step=5,
    )


refresh = st.button(
    "🔄 Search Live Executive Jobs",
    type="primary",
)


# ==========================================================
# LIVE SEARCH
# ==========================================================

if refresh:

    with st.spinner(
        f"Searching live jobs for {role}..."
    ):

        try:

            agent = ExecutiveAIAgent()

            jobs = agent.search_jobs(
                role=role
            )

            action_center = (
                ExecutiveActionCenter()
            )

            actions = (
                action_center.prioritize(
                    jobs,
                    limit=int(limit),
                )
            )

            st.session_state[
                "executive_action_jobs"
            ] = actions

            st.session_state[
                "executive_action_role"
            ] = role

            st.success(
                f"Found {len(jobs)} live jobs and generated "
                f"{len(actions)} executive actions."
            )

        except Exception as error:

            st.error(
                f"Live executive search failed: {error}"
            )


# ==========================================================
# DISPLAY ACTIONS
# ==========================================================

actions = st.session_state.get(
    "executive_action_jobs",
    []
)


if actions:

    st.caption(
        "Showing live executive opportunities ranked by the Action Center."
    )


    for index, action in enumerate(
        actions,
        start=1,
    ):

        priority = action.get(
            "priority",
            "MEDIUM",
        )


        if priority == "CRITICAL":

            badge = "🔴"

        elif priority == "HIGH":

            badge = "🟠"

        elif priority == "MEDIUM":

            badge = "🟡"

        else:

            badge = "⚪"


        role_name = action.get(
            "role",
            action.get(
                "title",
                "Executive Position",
            ),
        )


        company = action.get(
            "company",
            "Unknown Company",
        )


        country = action.get(
            "country",
            "",
        )


        ranking_score = action.get(
            "ranking_score",
            action.get(
                "priority_score",
                action.get(
                    "executive_score",
                    0,
                ),
            ),
        )


        decision_score = action.get(
            "decision_score",
            ranking_score,
        )


        recommended_action = action.get(
            "action",
            "REVIEW",
        )


        with st.container(
            border=True
        ):

            header_col1, header_col2 = st.columns(
                [5, 2]
            )


            with header_col1:

                st.markdown(
                    f"### {index}. {role_name}"
                )

                st.write(
                    f"**{company}**  |  {country}"
                )


            with header_col2:

                st.markdown(
                    f"### {badge} {priority}"
                )

                st.write(
                    f"Action: **{recommended_action}**"
                )


            score_col1, score_col2, score_col3 = st.columns(
                3
            )


            with score_col1:

                st.metric(
                    "Ranking Score",
                    f"{float(ranking_score):.2f}",
                )


            with score_col2:

                st.metric(
                    "Decision Score",
                    f"{float(decision_score):.2f}",
                )


            with score_col3:

                st.metric(
                    "Recommended Action",
                    recommended_action,
                )


            reasons = action.get(
                "reasons",
                [],
            )


            risks = action.get(
                "risks",
                [],
            )


            if reasons:

                with st.expander(
                    "Why JobHunter recommends this"
                ):

                    for reason in reasons:

                        st.write(
                            f"✅ {reason}"
                        )


            if risks:

                with st.expander(
                    "Risks / considerations"
                ):

                    for risk in risks:

                        st.write(
                            f"⚠️ {risk}"
                        )


            apply_link = action.get(
                "apply_link",
                "",
            )


            if apply_link:

                st.link_button(
                    "🚀 Open Application",
                    apply_link,
                )


else:

    st.info(
        "Click **Search Live Executive Jobs** to load the latest "
        "executive opportunities and generate recommended actions."
    )


st.divider()


# ==========================================================
# PHASE STATUS
# ==========================================================

st.subheader(
    "📌 JobHunter Executive Pipeline"
)


pipeline_col1, pipeline_col2, pipeline_col3, pipeline_col4, pipeline_col5 = (
    st.columns(5)
)


with pipeline_col1:

    st.success(
        "✓ Live Search"
    )


with pipeline_col2:

    st.success(
        "✓ Executive Scoring"
    )


with pipeline_col3:

    st.success(
        "✓ Job Ranking"
    )


with pipeline_col4:

    st.success(
        "✓ Decision Engine"
    )


with pipeline_col5:

    st.success(
        "✓ Action Center"
    )