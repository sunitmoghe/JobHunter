import streamlit as st
import pandas as pd

from modules.profile_manager import ProfileManager
from modules.career_strategy_ai import CareerStrategyAI
from modules.application_tracker import ApplicationTracker
from modules.executive_dashboard_engine import ExecutiveDashboardEngine
from modules.executive_ai_agent import ExecutiveAIAgent
from modules.executive_action_center import ExecutiveActionCenter
from modules.job_statistics import JobStatistics

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


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Executive Command Center",
    page_icon="🚀",
    layout="wide",
)


page_header(
    "🚀 Executive Command Center",
    "Your Executive AI Career Operating System.",
)


# ==========================================================
# ENGINES
# ==========================================================

profile_manager = ProfileManager()
career_ai = CareerStrategyAI()
tracker = ApplicationTracker()
dashboard = ExecutiveDashboardEngine()
agent = ExecutiveAIAgent()
action_center = ExecutiveActionCenter()


# ==========================================================
# PROFILE
# ==========================================================

if profile_manager.profile_exists():

    profile = profile_manager.load_profile()

else:

    profile = {
        "experience": 23,
        "skills": [
            "Sales Leadership",
            "P&L",
            "SaaS",
            "IoT",
            "Digital Transformation",
        ],
    }


strategy = career_ai.career_recommendation(
    profile
)


# ==========================================================
# EXISTING APPLICATIONS
# ==========================================================

try:

    applications = tracker.load_applications()

except Exception:

    applications = []


# ==========================================================
# LIVE JOBS
# ==========================================================

live_jobs = st.session_state.get(
    "executive_jobs",
    [],
)


try:

    statistics = JobStatistics(
        live_jobs
    )

except Exception:

    statistics = None


dashboard_data = dashboard.get_dashboard()


# ==========================================================
# KPI DASHBOARD
# ==========================================================

section_header(
    "📈 Executive KPI Dashboard"
)


metric_row(
    [
        (
            "Executive Score",
            f"{dashboard_data.get('executive_score', 0)}%",
        ),
        (
            "Live Jobs",
            len(live_jobs),
        ),
        (
            "Applications",
            dashboard_data.get(
                "application_count",
                len(applications),
            ),
        ),
        (
            "Recruiters",
            dashboard_data.get(
                "recruiter_count",
                0,
            ),
        ),
    ]
)


divider()


# ==========================================================
# LIVE EXECUTIVE OPPORTUNITIES
# ==========================================================

section_header(
    "🔥 Top Executive Opportunities"
)


if live_jobs:

    live_df = pd.DataFrame(
        live_jobs
    )

    columns = [
        c
        for c in [
            "ranking_position",
            "role",
            "title",
            "company",
            "country",
            "executive_score",
            "ranking_score",
            "priority",
            "ranking_priority",
        ]
        if c in live_df.columns
    ]

    if columns:

        st.dataframe(
            live_df[columns].head(20),
            use_container_width=True,
            hide_index=True,
        )

else:

    empty_state(
        "No executive opportunities found. Search for jobs from AI Executive Jobs."
    )


divider()


# ==========================================================
# PHASE 5 APPLICATION EXECUTION
# ==========================================================

section_header(
    "🚀 Executive Application Action Center"
)

st.caption(
    "Turn the highest-ranked executive opportunities into concrete application actions."
)


action_col1, action_col2 = st.columns(
    [3, 1]
)


with action_col1:

    action_role = st.text_input(
        "Search executive opportunities",
        value="Head of Sales",
        key="command_center_role",
    )


with action_col2:

    action_limit = st.number_input(
        "Top actions",
        min_value=5,
        max_value=20,
        value=10,
        step=5,
        key="command_center_limit",
    )


if st.button(
    "🔄 Refresh Executive Action Center",
    type="primary",
    use_container_width=True,
):

    with st.spinner(
        "Searching, ranking and preparing executive actions..."
    ):

        try:

            jobs = agent.search_jobs(
                role=action_role.strip()
            )

            actions = action_center.prioritize(
                jobs,
                limit=int(action_limit),
            )

            st.session_state[
                "command_center_actions"
            ] = actions

            st.session_state[
                "command_center_jobs"
            ] = jobs

            st.success(
                f"{len(jobs)} live jobs analyzed and {len(actions)} actions prepared."
            )

        except Exception as error:

            st.error(
                f"Executive action search failed: {error}"
            )

            st.exception(
                error
            )


actions = st.session_state.get(
    "command_center_actions",
    [],
)


if actions:

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
            "Company",
        )


        country = action.get(
            "country",
            "",
        )


        ranking_score = action.get(
            "ranking_score",
            action.get(
                "priority_score",
                0,
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

            title_col, priority_col = st.columns(
                [5, 2]
            )


            with title_col:

                st.markdown(
                    f"### {index}. {role_name}"
                )

                st.write(
                    f"**{company}**"
                    + (
                        f"  |  {country}"
                        if country
                        else ""
                    )
                )


            with priority_col:

                st.markdown(
                    f"### {badge} {priority}"
                )

                st.write(
                    f"Action: **{recommended_action}**"
                )


            score1, score2, score3 = st.columns(
                3
            )


            with score1:

                st.metric(
                    "Ranking Score",
                    f"{float(ranking_score):.2f}",
                )


            with score2:

                st.metric(
                    "Decision Score",
                    f"{float(decision_score):.2f}",
                )


            with score3:

                st.metric(
                    "Recommended Action",
                    recommended_action,
                )


            # --------------------------------------------------
            # REASONS
            # --------------------------------------------------

            reasons = action.get(
                "reasons",
                action.get(
                    "decision_reasons",
                    [],
                ),
            )

            if reasons:

                with st.expander(
                    "✅ Why JobHunter recommends this"
                ):

                    for reason in reasons:

                        st.write(
                            f"• {reason}"
                        )


            # --------------------------------------------------
            # RISKS
            # --------------------------------------------------

            risks = action.get(
                "risks",
                action.get(
                    "decision_risks",
                    [],
                ),
            )

            if risks:

                with st.expander(
                    "⚠️ Risks / Considerations"
                ):

                    for risk in risks:

                        st.write(
                            f"• {risk}"
                        )


            st.divider()


            action1, action2, action3 = st.columns(
                3
            )


            # --------------------------------------------------
            # OPEN APPLICATION
            # --------------------------------------------------

            apply_link = action.get(
                "apply_link",
                "",
            )


            with action1:

                if apply_link:

                    st.link_button(
                        "🚀 OPEN APPLICATION",
                        apply_link,
                        use_container_width=True,
                    )

                else:

                    st.warning(
                        "No direct application link."
                    )


            # --------------------------------------------------
            # MARK APPLIED
            # --------------------------------------------------

            with action2:

                if st.button(
                    "✅ MARK AS APPLIED",
                    key=f"mark_applied_{index}",
                    use_container_width=True,
                ):

                    try:

                        result = action_center.apply(
                            action
                        )

                        if result:

                            st.success(
                                "Application recorded in Application Tracker."
                            )

                        else:

                            st.warning(
                                "Application was not recorded."
                            )

                    except Exception as error:

                        st.error(
                            "Could not record application."
                        )

                        st.exception(
                            error
                        )


            # --------------------------------------------------
            # APPLICATION PACKAGE
            # --------------------------------------------------

            with action3:

                if st.button(
                    "📝 APPLICATION PACKAGE",
                    key=f"package_{index}",
                    use_container_width=True,
                ):

                    package = (
                        action_center.prepare_application_package(
                            profile,
                            action,
                        )
                    )

                    st.session_state[
                        f"application_package_{index}"
                    ] = package


            # --------------------------------------------------
            # PACKAGE DISPLAY
            # --------------------------------------------------

            package = st.session_state.get(
                f"application_package_{index}",
                None,
            )


            if package:

                with st.expander(
                    "📄 Application Package",
                    expanded=True,
                ):

                    tabs = st.tabs(
                        [
                            "LinkedIn",
                            "Cover Letter",
                            "Recruiter Email",
                            "HR Email",
                            "Hiring Manager",
                            "Executive Pitch",
                            "Follow-up",
                            "Thank You",
                        ]
                    )


                    package_keys = [
                        "linkedin_message",
                        "cover_letter",
                        "recruiter_email",
                        "hr_email",
                        "hiring_manager_email",
                        "executive_pitch",
                        "follow_up",
                        "thank_you",
                    ]


                    for tab, key in zip(
                        tabs,
                        package_keys,
                    ):

                        with tab:

                            st.text_area(
                                "",
                                package.get(
                                    key,
                                    "",
                                ),
                                height=260,
                                key=f"package_text_{index}_{key}",
                            )


else:

    st.info(
        "Click 'Refresh Executive Action Center' to generate your live application priorities."
    )


divider()


# ==========================================================
# TOP MARKETS
# ==========================================================

section_header(
    "🌍 Top Executive Markets"
)


market_cols = st.columns(3)


for index, market in enumerate(
    strategy.get(
        "best_markets",
        [],
    )
):

    if index >= 3:
        break


    with market_cols[index]:

        success_box(
            market["country"]
        )

        st.metric(
            "Relocation Score",
            f"{market['score']}%",
        )

        details = market["details"]

        st.write(
            f"Career Fit: {details['career_fit']}%"
        )

        st.write(
            f"Salary Fit: {details['salary_fit']}%"
        )

        st.write(
            f"Visa Fit: {details['visa_fit']}%"
        )

        st.write(
            f"Family Fit: {details['family_fit']}%"
        )

        st.write(
            f"Market Demand: {details['market_demand']}%"
        )


divider()


# ==========================================================
# STRENGTHS AND GAPS
# ==========================================================

left, right = st.columns(2)


with left:

    section_header(
        "💪 Executive Strengths"
    )

    for strength in strategy.get(
        "strengths",
        [],
    ):

        success_box(
            strength
        )


with right:

    section_header(
        "⚠️ Career Improvement Areas"
    )

    for gap in strategy.get(
        "gaps",
        [],
    ):

        warning_box(
            gap
        )


divider()


# ==========================================================
# 90 DAY PLAN
# ==========================================================

section_header(
    "📅 90-Day Executive Career Plan"
)


months = strategy.get(
    "action_plan",
    {},
)


month_cols = st.columns(3)


for col, month in zip(
    month_cols,
    [
        "Month 1",
        "Month 2",
        "Month 3",
    ],
):

    with col:

        info_box(
            month
        )

        for task in months.get(
            month,
            [],
        ):

            st.write(
                "•",
                task,
            )


divider()


# ==========================================================
# APPLICATION PIPELINE
# ==========================================================

section_header(
    "📄 Executive Application Pipeline"
)


applications = tracker.get_applications()


if applications:

    application_df = pd.DataFrame(
        applications
    )

    columns = [
        c
        for c in [
            "company",
            "role",
            "country",
            "status",
            "priority_score",
            "executive_score",
            "application_date",
            "last_updated",
        ]
        if c in application_df.columns
    ]


    st.dataframe(
        application_df[columns],
        use_container_width=True,
        hide_index=True,
    )


else:

    empty_state(
        "No applications have been recorded yet."
    )


divider()


# ==========================================================
# LIVE JOB ANALYTICS
# ==========================================================

section_header(
    "📊 Live Job Intelligence"
)


stats_col1, stats_col2, stats_col3 = st.columns(3)


with stats_col1:

    st.metric(
        "Companies",
        statistics.companies()
        if statistics
        else 0,
    )


with stats_col2:

    st.metric(
        "Countries",
        statistics.countries()
        if statistics
        else 0,
    )


with stats_col3:

    st.metric(
        "Average Executive Score",
        statistics.average_score()
        if statistics
        else 0,
    )


divider()


# ==========================================================
# TODAY'S PRIORITIES
# ==========================================================

section_header(
    "🚀 Today's Executive Priorities"
)


for item in [

    "Apply to high-priority executive roles.",

    "Prepare tailored resumes for the strongest opportunities.",

    "Send LinkedIn messages to senior recruiters.",

    "Prepare one executive interview success story.",

    "Review opportunities in your strongest relocation market.",

]:

    st.checkbox(
        item
    )


divider()


# ==========================================================
# AI SUMMARY
# ==========================================================

section_header(
    "🤖 AI Executive Summary"
)


best_country = "Global"


if strategy.get(
    "best_markets"
):

    best_country = (
        strategy[
            "best_markets"
        ][0]["country"]
    )


summary = f"""
Your Executive Readiness Score is
{strategy['executive_score']['overall_score']}%.

Your strongest international market is
{best_country}.

Focus areas:

• Senior leadership roles
• P&L ownership
• Enterprise sales
• Global expansion opportunities

Priority roles:

Director,
VP,
Chief Revenue Officer,
Chief Commercial Officer,
Country Manager.
"""


success_box(
    summary
)


divider()


success_box(
    "🎯 Executive Command Center is active."
)


st.caption(
    "JobHunter AI • Executive Career Operating System"
)