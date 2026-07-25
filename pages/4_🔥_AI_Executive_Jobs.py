import streamlit as st

from modules.executive_ai_agent import ExecutiveAIAgent
from modules.priority_engine import PriorityEngine
from modules.executive_scoring_engine import ExecutiveScoringEngine


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Executive Jobs",
    page_icon="🔥",
    layout="wide"
)


# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("🔥 AI Executive Live Job Recommendations")

st.write(
    "Search global executive opportunities using the AI Executive Job Engine."
)


# --------------------------------------------------
# SEARCH
# --------------------------------------------------

if st.button("🚀 Search Global Executive Jobs"):

    with st.spinner(
        "Searching executive opportunities across multiple countries..."
    ):

        agent = ExecutiveAIAgent()

        jobs = agent.search_all_roles()

    if jobs:

        st.success(
            f"Found {len(jobs)} executive opportunities."
        )

        priority_engine = PriorityEngine()
        scoring_engine = ExecutiveScoringEngine()

        st.divider()

        for job in jobs[:50]:

            role = job.get(
                "role",
                job.get(
                    "title",
                    "Executive Role"
                )
            )

            company = job.get(
                "company",
                "Not Available"
            )

            country = job.get(
                "country",
                job.get(
                    "location",
                    "Not Available"
                )
            )

            score = scoring_engine.calculate_score(
                {
                    "role": role,
                    "country": country
                },
                ats_score=80,
                experience_years=23
            )

            priority = priority_engine.calculate_priority(
                {
                    "role": role,
                    "country": country
                },
                score["executive_fit"]
            )

            st.subheader(role)

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    "🏢 Company:",
                    company
                )

                st.write(
                    "🌍 Country:",
                    country
                )

            with col2:

                st.metric(
                    "Executive Fit",
                    f"{score['executive_fit']}%"
                )

                st.metric(
                    "Priority Score",
                    f"{priority['priority_score']}%"
                )

            st.success(
                priority["category"]
            )

            with st.expander("📊 Executive Score Breakdown"):

                st.write(
                    f"ATS Score: {score['ats_score']}%"
                )

                st.write(
                    f"Leadership Score: {score['leadership_score']}%"
                )

                st.write(
                    f"Experience Score: {score['experience_score']}%"
                )

                st.write(
                    f"Country Score: {score['country_score']}%"
                )

                st.write(
                    f"Industry Score: {score['industry_score']}%"
                )

                st.write(
                    f"Role Score: {score['role_score']}%"
                )

            with st.expander("View Job Details"):

                st.json(job)

            st.divider()

    else:

        st.warning(
            "No executive jobs found."
        )
