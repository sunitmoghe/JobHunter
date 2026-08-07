import streamlit as st

from modules.executive_ai_agent import ExecutiveAIAgent
from modules.profile_manager import ProfileManager
from modules.interview_coach_engine import InterviewCoachEngine

st.set_page_config(
    page_title="Interview Coach",
    page_icon="🎤",
    layout="wide",
)

st.title("🎤 Executive Interview Coach")

profile_manager = ProfileManager()
agent = ExecutiveAIAgent()
coach = InterviewCoachEngine()

if profile_manager.profile_exists():

    profile = profile_manager.load_profile()

else:

    profile = {
        "experience": 23,
    }

jobs = agent.search_all_roles(max_roles=20)

if not jobs:

    st.warning("No executive jobs found.")

    st.stop()

job_names = [
    f"{j.get('role','Executive')} • {j.get('company','Company')}"
    for j in jobs
]

selected = st.selectbox(
    "Select Executive Opportunity",
    range(len(job_names)),
    format_func=lambda x: job_names[x],
)

job = jobs[selected]

questions = coach.generate_questions(
    profile,
    job,
)

st.subheader("Executive Interview Questions")

for i, q in enumerate(questions, start=1):

    st.write(f"**Q{i}.** {q}")

st.success("Interview Coach Ready")