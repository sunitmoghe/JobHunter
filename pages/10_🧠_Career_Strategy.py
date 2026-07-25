import streamlit as st

from modules.career_strategy_ai import CareerStrategyAI
from modules.profile_manager import ProfileManager


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Career Strategy Advisor",
    page_icon="🧠",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title(
    "🧠 AI Executive Career Strategy Advisor"
)

st.write(
    "Get AI-powered career recommendations based on your executive profile, skills, markets and experience."
)



# --------------------------------------------------
# LOAD PROFILE
# --------------------------------------------------

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



# --------------------------------------------------
# ANALYSIS BUTTON
# --------------------------------------------------

if st.button(
    "🚀 Generate Career Strategy"
):


    strategy = career_ai.career_recommendation(
        profile
    )


    st.session_state["strategy"] = strategy



# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

if "strategy" in st.session_state:


    strategy = st.session_state["strategy"]


    st.divider()


    # ----------------------------------------------
    # EXECUTIVE SCORE
    # ----------------------------------------------

    st.subheader(
        "🎯 Executive Readiness Score"
    )


    score = strategy["executive_score"]


    st.metric(

        "Overall Executive Match",

        f"{score['overall_score']}%"

    )


    col1, col2, col3, col4, col5 = st.columns(5)


    metrics = score["breakdown"]


    columns = [

        col1,

        col2,

        col3,

        col4,

        col5

    ]


    for index, item in enumerate(metrics):

        with columns[index]:

            st.metric(

                item.replace(
                    "_",
                    " "
                ).title(),

                f"{metrics[item]}%"

            )



    st.divider()



    # ----------------------------------------------
    # MARKET RECOMMENDATION
    # ----------------------------------------------
st.subheader(
    "🌍 Executive Relocation Intelligence"
)


for market in strategy["best_markets"]:

    st.success(

        f"""
🌍 {market['country']}

Overall Relocation Score:
{market['score']}%

"""

    )


    details = market.get(
        "details",
        {}
    )


    col1, col2, col3, col4, col5 = st.columns(5)


    with col1:
        st.metric(
            "Career Fit",
            f"{details.get('career_fit',0)}%"
        )


    with col2:
        st.metric(
            "Salary Fit",
            f"{details.get('salary_fit',0)}%"
        )


    with col3:
        st.metric(
            "Visa Fit",
            f"{details.get('visa_fit',0)}%"
        )


    with col4:
        st.metric(
            "Family Fit",
            f"{details.get('family_fit',0)}%"
        )


    with col5:
        st.metric(
            "Market Demand",
            f"{details.get('market_demand',0)}%"
        )


    st.divider()

    st.divider()



    # ----------------------------------------------
    # STRENGTHS
    # ----------------------------------------------

    st.subheader(
        "💪 Executive Strengths"
    )


    for strength in strategy["strengths"]:

        st.info(
            strength
        )



    st.divider()



    # ----------------------------------------------
    # GAPS
    # ----------------------------------------------

    st.subheader(
        "⚠ Career Improvement Areas"
    )


    for gap in strategy["gaps"]:

        st.warning(
            gap
        )



    st.divider()



    # ----------------------------------------------
    # ACTION PLAN
    # ----------------------------------------------

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

            st.success(
                item
            )



    with tab2:

        for item in plan["Month 2"]:

            st.success(
                item
            )



    with tab3:

        for item in plan["Month 3"]:

            st.success(
                item
            )