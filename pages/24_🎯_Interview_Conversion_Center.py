import streamlit as st

from modules.application_tracker import ApplicationTracker
from modules.interview_conversion_engine import (
    InterviewConversionEngine,
)
from modules.profile_manager import ProfileManager


st.set_page_config(
    page_title="Interview & Conversion Center",
    page_icon="🎯",
    layout="wide",
)


st.title("🎯 Interview & Conversion Center")

st.caption(
    "Manage executive interviews, preparation, outcomes and application conversion."
)


tracker = ApplicationTracker()
engine = InterviewConversionEngine()
profile_manager = ProfileManager()


# ==========================================================
# PROFILE
# ==========================================================

if profile_manager.profile_exists():

    profile = profile_manager.load_profile()

else:

    profile = {
        "experience": 23,
        "skills": [],
    }


# ==========================================================
# CONVERSION DASHBOARD
# ==========================================================

summary = engine.conversion_summary()


st.subheader(
    "📊 Executive Conversion Funnel"
)


c1, c2, c3, c4, c5 = st.columns(5)


with c1:

    st.metric(
        "Applications",
        summary["total"],
    )


with c2:

    st.metric(
        "Interviews",
        summary["interview"],
    )


with c3:

    st.metric(
        "Next Round",
        summary["next_round"],
    )


with c4:

    st.metric(
        "Offers",
        summary["offer"],
    )


with c5:

    st.metric(
        "Interview Rate",
        f"{summary['interview_rate']}%",
    )


st.divider()


# ==========================================================
# EXISTING APPLICATIONS
# ==========================================================

applications = tracker.get_applications()


if not applications:

    st.info(
        "No applications are available yet."
    )

    st.stop()


st.subheader(
    "📋 Application Pipeline"
)


application_labels = []

for application in applications:

    role = application.get(
        "role",
        "Executive Position",
    )

    company = application.get(
        "company",
        "Company",
    )

    status = application.get(
        "status",
        "Applied",
    )

    application_id = application.get(
        "application_id",
        "",
    )

    application_labels.append(
        (
            application_id,
            f"{role} • {company} • {status}",
        )
    )


selected_id = st.selectbox(
    "Select Application",
    range(
        len(application_labels)
    ),
    format_func=lambda x:
        application_labels[x][1],
)


selected_application_id = (
    application_labels[
        selected_id
    ][0]
)


application = engine.get_application(
    selected_application_id
)


if not application:

    st.error(
        "Selected application could not be loaded."
    )

    st.stop()


# ==========================================================
# APPLICATION SUMMARY
# ==========================================================

role = application.get(
    "role",
    "Executive Position",
)

company = application.get(
    "company",
    "Company",
)

country = application.get(
    "country",
    "",
)

status = application.get(
    "status",
    "Applied",
)


st.markdown(
    f"### {role}"
)

st.write(
    f"**Company:** {company}"
)

if country:

    st.write(
        f"**Country:** {country}"
    )

st.write(
    f"**Current Status:** {status}"
)


# ==========================================================
# INTERVIEW SCHEDULING
# ==========================================================

st.divider()

st.subheader(
    "📅 Interview Management"
)


date_col, stage_col = st.columns(2)


with date_col:

    interview_date = st.text_input(
        "Interview Date / Time",
        value=application.get(
            "interview_date",
            "",
        ),
        placeholder="YYYY-MM-DD HH:MM",
    )


with stage_col:

    interview_stage = st.selectbox(
        "Interview Stage",
        [
            "First Round",
            "Hiring Manager",
            "Panel",
            "Technical",
            "Commercial",
            "Final Round",
        ],
    )


if st.button(
    "📅 Schedule / Update Interview",
    use_container_width=True,
):

    if not interview_date.strip():

        st.warning(
            "Enter an interview date/time."
        )

    else:

        success = engine.schedule_interview(
            selected_application_id,
            interview_date.strip(),
            interview_stage,
        )

        if success:

            st.success(
                "Interview scheduled successfully."
            )

            st.rerun()

        else:

            st.error(
                "Unable to schedule interview."
            )


# ==========================================================
# INTERVIEW PREPARATION
# ==========================================================

st.divider()

st.subheader(
    "🧠 Interview Preparation"
)


if st.button(
    "🎯 Generate Executive Interview Questions",
    type="primary",
    use_container_width=True,
):

    preparation = engine.prepare_interview(
        profile,
        application,
    )

    st.session_state[
        "interview_preparation"
    ] = preparation


preparation = st.session_state.get(
    "interview_preparation",
    None,
)


if preparation:

    questions = preparation.get(
        "questions",
        [],
    )


    for index, question in enumerate(
        questions,
        start=1,
    ):

        with st.expander(
            f"Q{index}. {question}"
        ):

            if st.button(
                "✨ Generate STAR Answer",
                key=f"star_{index}",
            ):

                answer = engine.generate_star_answer(
                    question,
                    profile,
                )

                st.session_state[
                    f"star_answer_{index}"
                ] = answer


            answer = st.session_state.get(
                f"star_answer_{index}",
                "",
            )


            if answer:

                st.text_area(
                    "Suggested STAR Answer",
                    value=answer,
                    height=250,
                    key=f"star_text_{index}",
                )


# ==========================================================
# INTERVIEW RESULT
# ==========================================================

st.divider()

st.subheader(
    "📝 Interview Result"
)


result_col1, result_col2 = st.columns(2)


with result_col1:

    interview_outcome = st.selectbox(
        "Outcome",
        [
            "Scheduled",
            "Completed",
            "Next Round",
            "Offer",
            "Rejected",
            "Withdrawn",
        ],
    )


with result_col2:

    interview_score = st.number_input(
        "Interview Score",
        min_value=0,
        max_value=100,
        value=75,
        step=1,
    )


feedback = st.text_area(
    "Interview Feedback / Notes",
    height=180,
)


if st.button(
    "💾 Record Interview Result",
    use_container_width=True,
):

    success = engine.record_interview_result(
        selected_application_id,
        interview_outcome,
        interview_score,
        feedback,
    )

    if success:

        st.success(
            f"Interview result recorded: {interview_outcome}"
        )

        st.rerun()

    else:

        st.error(
            "Unable to record interview result."
        )


# ==========================================================
# CURRENT INTERVIEW FEEDBACK
# ==========================================================

if application.get(
    "interview_score"
) is not None:

    st.divider()

    st.subheader(
        "📈 Current Interview Assessment"
    )

    st.metric(
        "Interview Score",
        f"{application.get('interview_score', 0)}%",
    )

    stored_feedback = application.get(
        "interview_feedback",
        "",
    )

    if stored_feedback:

        st.info(
            stored_feedback
        )


# ==========================================================
# CONVERSION METRICS
# ==========================================================

st.divider()

st.subheader(
    "📈 Conversion Analytics"
)


a1, a2, a3 = st.columns(3)


with a1:

    st.metric(
        "Application → Interview",
        f"{summary['interview_rate']}%",
    )


with a2:

    st.metric(
        "Application → Offer",
        f"{summary['offer_rate']}%",
    )


with a3:

    st.metric(
        "Interview → Offer",
        f"{summary['interview_to_offer']}%",
    )


# ==========================================================
# FUNNEL
# ==========================================================

st.subheader(
    "🔻 Application Funnel"
)


funnel = engine.funnel()


for stage in funnel:

    st.write(
        f"**{stage['stage']}** — "
        f"{stage['count']}"
    )


st.divider()

st.success(
    "🎯 Interview & Conversion Center operational."
)

st.caption(
    "JobHunter AI • Executive Interview & Conversion Intelligence"
)