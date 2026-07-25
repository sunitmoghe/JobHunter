import streamlit as st

from modules.executive_ai_agent import ExecutiveAIAgent
from modules.priority_engine import PriorityEngine


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
# SEARCH BUTTON
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

            # Temporary AI score
            match_score = 80

            priority = priority_engine.calculate_priority(
                {
                    "role": role,
                    "country": country
                },
                match_score
            )

            st.subheader(
                f"{role}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write("🏢 Company:", company)
                st.write("🌍 Country:", country)

            with col2:

                st.metric(
                    "Executive Fit",
                    f"{match_score}%"
                )

                st.metric(
                    "Priority Score",
                    f"{priority['priority_score']}%"
                )

            st.success(
                priority["category"]
            )

            with st.expander("View Job Details"):

                st.json(job)

            st.divider()

    else:

        st.warning(
            "No executive jobs found."
        )