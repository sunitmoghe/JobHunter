import streamlit as st

from modules.career_strategy_ai import CareerStrategyAI
from modules.profile_manager import ProfileManager


st.set_page_config(
    page_title="AI Career Strategy Advisor",
    page_icon="🧠",
    layout="wide"
)


st.title(
    "🧠 AI Executive Career Strategy Advisor"
)

st.caption(
    "AI-powered career recommendations based on executive profile, skills, markets and experience."
)


st.divider()


profile_manager = ProfileManager()

career_ai = CareerStrategyAI()


if profile_manager.profile_exists():

    profile = profile_manager.load_profile()

    st.success(
        "✅ Executive profile loaded"
    )

else:

    profile = {

        "experience": 23,

        "skills": [

            "Sales Leadership",
            "P&L Management",
            "SaaS",
            "IoT",
            "Digital Transformation"

        ]

    }

    st.warning(
        "Using default executive profile data."
    )


if st.button(
    "🚀 Generate Career Strategy",
    type="primary"
):

    strategy = career_ai.career_recommendation(
        profile
    )

    st.session_state["strategy"] = strategy



if "strategy" in st.session_state:


    strategy = st.session_state["strategy"]


    st.divider()


    st.subheader(
        "🎯 Executive Readiness Score"
    )


    score = strategy["executive_score"]


    st.metric(
        "Overall Executive Match",
        f"{score['overall_score']}%"
    )


    breakdown = score["breakdown"]


    cols = st.columns(len(breakdown))


    for index, item in enumerate(breakdown):

        with cols[index]:

            st.metric(
                item.replace(
                    "_",
                    " "
                ).title(),

                f"{breakdown[item]}%"
            )


    st.divider()


    st.subheader(
        "🌍 Executive Relocation Intelligence"
    )


    for market in strategy["best_markets"]:

        st.success(

            f"""
🌍 {market['country']}

Relocation Score:
{market['score']}%
"""

        )


        details = market.get(
            "details",
            {}
        )


        cols = st.columns(5)


        metrics = [

            (
                "Career Fit",
                details.get("career_fit",0)
            ),

            (
                "Salary Fit",
                details.get("salary_fit",0)
            ),

            (
                "Visa Fit",
                details.get("visa_fit",0)
            ),

            (
                "Family Fit",
                details.get("family_fit",0)
            ),

            (
                "Market Demand",
                details.get("market_demand",0)
            )

        ]


        for index, data in enumerate(metrics):

            with cols[index]:

                st.metric(
                    data[0],
                    f"{data[1]}%"
                )


        st.divider()



    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "💪 Executive Strengths"
        )

        for strength in strategy["strengths"]:

            st.success(
                strength
            )


    with col2:

        st.subheader(
            "⚠ Career Improvement Areas"
        )

        for gap in strategy["gaps"]:

            st.warning(
                gap
            )


    st.divider()


    st.subheader(
        "📅 90-Day Executive Career Action Plan"
    )


    plan = strategy["action_plan"]


    tab1, tab2, tab3 = st.tabs(

        [
            "Month 1",
            "Month 2",
            "Month 3"
        ]

    )


    with tab1:

        for item in plan["Month 1"]:

            st.info(item)



    with tab2:

        for item in plan["Month 2"]:

            st.info(item)



    with tab3:

        for item in plan["Month 3"]:

            st.info(item)



else:

    st.info(
        "Click 🚀 Generate Career Strategy to create your executive career roadmap."
    )


st.divider()


st.success(
    "✅ AI Career Strategy Advisor operational."
)


st.caption(
    "JobHunter AI • Executive Career Strategy Suite"
)