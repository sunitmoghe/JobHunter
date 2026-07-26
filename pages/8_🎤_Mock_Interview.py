import streamlit as st

from modules.mock_interview_ai import MockInterviewAI


st.set_page_config(
    page_title="Mock Interview Simulator",
    page_icon="🎤",
    layout="wide"
)


st.title(
    "🎤 AI Executive Mock Interview Simulator"
)

st.caption(
    "Practice executive interviews and receive AI-powered feedback."
)


coach = MockInterviewAI()


# --------------------------------------------------
# RESET
# --------------------------------------------------

if st.button(
    "🔄 New Interview"
):

    st.session_state.clear()

    st.rerun()



st.divider()


# --------------------------------------------------
# INTERVIEW SETUP
# --------------------------------------------------

st.subheader(
    "💼 Interview Setup"
)


role = st.text_input(
    "Target Role",
    "Chief Revenue Officer"
)


company = st.text_input(
    "Company",
    "Target Company"
)



if st.button(
    "🚀 Start Mock Interview",
    type="primary"
):

    st.session_state["interview"] = coach.start_interview(
        role,
        company
    )

    st.session_state["question_number"] = 1

    st.session_state.pop(
        "evaluation",
        None
    )

    st.success(
        "✅ Executive interview started"
    )



# --------------------------------------------------
# INTERVIEW SESSION
# --------------------------------------------------

if "interview" in st.session_state:


    session = st.session_state["interview"]


    number = st.session_state.get(
        "question_number",
        1
    )


    question = coach.get_question(
        session,
        number
    )


    st.divider()


    if question:


        st.subheader(
            f"Question {number}"
        )


        st.info(
            question
        )


        answer = st.text_area(
            "Your Executive Answer",
            height=250
        )


        col1, col2 = st.columns(2)


        with col1:


            if st.button(
                "📊 Evaluate Answer"
            ):


                if answer.strip():


                    evaluation = coach.evaluate_response(
                        answer
                    )


                    st.session_state["evaluation"] = evaluation


                else:

                    st.warning(
                        "Please enter your answer."
                    )



        with col2:


            if st.button(
                "➡ Next Question"
            ):


                st.session_state["question_number"] = number + 1

                st.session_state.pop(
                    "evaluation",
                    None
                )

                st.rerun()



    else:


        st.success(
            """
🎉 Interview completed.

Review your feedback and continue practising executive responses.
"""
        )



# --------------------------------------------------
# FEEDBACK
# --------------------------------------------------

if "evaluation" in st.session_state:


    evaluation = st.session_state["evaluation"]


    st.divider()


    st.subheader(
        "🤖 AI Interview Assessment"
    )


    st.metric(
        "Executive Readiness Score",
        f"{evaluation.get('overall_score',0)}%"
    )


    col1, col2 = st.columns(2)


    with col1:


        st.write(
            "### 📊 Performance Metrics"
        )


        for key, value in evaluation.get(
            "metrics",
            {}
        ).items():


            st.progress(

                value / 100,

                text=f"{key.replace('_',' ').title()}: {value}%"

            )



    with col2:


        st.write(
            "### 💪 Strengths"
        )


        for item in evaluation.get(
            "strengths",
            []
        ):

            st.success(
                item
            )


        st.write(
            "### ⚠ Improvement Areas"
        )


        for item in evaluation.get(
            "improvements",
            []
        ):

            st.warning(
                item
            )



st.divider()


st.success(
    "✅ AI Executive Mock Interview Simulator operational."
)


st.caption(
    "JobHunter AI • Executive Interview Coach Suite"
)