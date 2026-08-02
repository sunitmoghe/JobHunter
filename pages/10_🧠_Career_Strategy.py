import streamlit as st

from modules.career_strategy_ai import CareerStrategyAI
from modules.profile_manager import ProfileManager


st.set_page_config(
    page_title="AI Career Strategy Advisor",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 AI Executive Career Strategy Advisor")

st.caption(
    "AI-powered career recommendations based on your executive profile, skills and experience."
)

st.divider()

profile_manager = ProfileManager()
career_ai = CareerStrategyAI()

if profile_manager.profile_exists():

    profile = profile_manager.load_profile()

    st.success("✅ Executive profile loaded")

else:

    profile = {
        "experience": 23,
        "skills": [
            "Sales Leadership",
            "P&L Management",
            "SaaS",
            "IoT",
            "Digital Transformation",
        ],
    }

    st.warning("Using default executive profile.")

if st.button(
    "🚀 Generate Career Strategy",
    type="primary",
):

    st.session_state["strategy"] = (
        career_ai.career_recommendation(profile)
    )

if "strategy" in st.session_state:

    strategy = st.session_state["strategy"]

    st.subheader("🎯 Executive Readiness Score")

    score = strategy["executive_score"]

    st.metric(
        "Overall Executive Match",
        f"{score['overall_score']}%",
    )

    cols = st.columns(len(score["breakdown"]))

    for i, item in enumerate(score["breakdown"]):

        with cols[i]:

            st.metric(
                item.replace("_", " ").title(),
                f"{score['breakdown'][item]}%",
            )

    st.divider()

    st.subheader("🌍 Best Markets")

    for market in strategy["best_markets"]:

        st.success(
            f"{market['country']} • {market['score']}%"
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("💪 Strengths")

        for item in strategy["strengths"]:

            st.success(item)

    with col2:

        st.subheader("⚠ Improvement Areas")

        for item in strategy["gaps"]:

            st.warning(item)

    st.divider()

    st.subheader("📅 90-Day Action Plan")

    tabs = st.tabs(
        [
            "Month 1",
            "Month 2",
            "Month 3",
        ]
    )

    months = [
        "Month 1",
        "Month 2",
        "Month 3",
    ]

    for tab, month in zip(tabs, months):

        with tab:

            for item in strategy["action_plan"][month]:

                st.info(item)

else:

    st.info(
        "Click 'Generate Career Strategy' to create your roadmap."
    )

st.divider()

st.success("✅ AI Career Strategy Advisor operational.")

st.caption(
    "JobHunter AI • Executive Career Strategy Suite"
)