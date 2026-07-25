import streamlit as st

from modules.interview_coach_ai import InterviewCoachAI
from modules.profile_manager import ProfileManager


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎤",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title(
    "🎤 AI Executive Interview Coach"
)

st.write(
    "Prepare executive-level interview answers using AI."
)



coach = InterviewCoachAI()

profile_manager = ProfileManager()



if profile_manager.profile_exists():

    profile = profile_manager.load_profile()

else:

    profile = {}

    st.warning(
        "⚠ No executive profile found. Analyse your resume first."
    )



# --------------------------------------------------
# JOB INPUT
# --------------------------------------------------

st.subheader(
    "💼 Interview Preparation Setup"
)


role = st.text_input(
    "Target Role",
    "Vice President Sales"
)


company = st.text_input(
    "Company",
    "Target Company"
)


industry = st.text_input(
    "Industry",
    "Technology"
)



job = {

    "role": role,

    "company": company,

    "industry": industry

}



# --------------------------------------------------
# QUESTION GENERATOR
# --------------------------------------------------

if st.button(
    "🎯 Generate Interview Questions"
):

    questions = coach.generate_questions(
        job
    )


    st.session_state["questions"] = questions



if "questions" in st.session_state:


    st.subheader(
        "🔥 Executive Interview Questions"
    )


    for index, question in enumerate(
        st.session_state["questions"]
    ):

        with st.expander(
            f"Question {index+1}"
        ):

            st.write(
                question
            )


            if st.button(
                "Generate STAR Answer",
                key=f"star_{index}"
            ):

                answer = coach.generate_star_answer(
                    question,
                    profile
                )


                st.info(
                    answer
                )



# --------------------------------------------------
# ANSWER EVALUATOR
# --------------------------------------------------

st.divider()


st.subheader(
    "🤖 Evaluate Your Answer"
)


user_answer = st.text_area(
    "Paste your interview answer",
    height=200
)



if st.button(
    "📊 Evaluate Answer"
):

    if user_answer:


        evaluation = coach.evaluate_answer(
            user_answer
        )


        st.metric(
            "Executive Interview Score",
            f"{evaluation['score']}%"
        )


        st.success(
            evaluation["strength"]
        )


        st.warning(
            evaluation["improvement"]
        )


    else:

        st.info(
            "Please enter an answer first."
        )