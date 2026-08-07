import streamlit as st

from modules.ai_executive_advisor import AIExecutiveAdvisor
from modules.executive_ai_agent import ExecutiveAIAgent
from modules.profile_manager import ProfileManager

st.set_page_config(
    page_title="AI Executive Advisor",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Executive Advisor")

advisor = AIExecutiveAdvisor()
agent = ExecutiveAIAgent()
profile_manager = ProfileManager()

if profile_manager.profile_exists():
    profile = profile_manager.load_profile()
else:
    profile = {
        "experience": 23,
        "skills": [],
    }

jobs = agent.search_all_roles(max_roles=10)

advice = advisor.generate_advice(
    profile,
    jobs,
)

st.success(advice["summary"])

st.info(
    f"🎯 Priority: {advice['priority']}"
)

st.subheader("📋 Recommended Next Steps")

for step in advice["next_steps"]:
    st.checkbox(step)

st.success("AI Executive Advisor Ready")