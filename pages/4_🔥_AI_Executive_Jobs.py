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
# AI EXECUTIVE JOB ENGINE
# --------------------------------------------------

st.title(
    "🔥 AI Executive Live Job Recommendations"
)


st.write(
    "Search global executive opportunities using AI Job Engine."
)


if st.button(
    "🚀 Search Global Executive Jobs"
):


    with st.spinner(
        "AI Agent searching global executive opportunities..."
    ):


        agent = ExecutiveAIAgent()

        jobs = agent.search_all_roles()



    if jobs:


        st.success(
            f"Found {len(jobs)} executive opportunities"
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


            match_score = 80


            priority = priority_engine.calculate_priority(
                {
                    "role": role,
                    "country": country
                },
                match_score
            )


            st.subheader(
                f"{role} - {company}"
            )


            col1, col2, col3 = st.columns(3)


            col1.metric(
                "AI Match Score",
                f"{match_score}%"
            )


            col2.metric(
                "Priority Score",
                f"{priority['priority_score']}"
            )


            col3.write(
                "Category"
            )


            st.success(
                priority["category"]
            )


            st.write(
                "🌍 Location:",
                country
            )


            st.write(
                "🏢 Company:",
                company
            )


            st.write(
                "⭐ Source:",
                job.get(
                    "source",
                    "AI Search"
                )
            )


            st.divider()


    else:

        st.warning(
            "No executive jobs found"
        )