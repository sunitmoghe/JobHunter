import streamlit as st

from modules.application_tracker import ApplicationTracker


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Application Tracker",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title(
    "📊 Executive Application CRM Tracker"
)

st.write(
    "Manage your executive job applications, interviews and career pipeline."
)


# --------------------------------------------------
# LOAD TRACKER
# --------------------------------------------------

tracker = ApplicationTracker()

applications = tracker.get_applications()


# --------------------------------------------------
# SUMMARY METRICS
# --------------------------------------------------

total = len(applications)

applied = len(
    [
        a for a in applications
        if a.get("status") == "Applied"
    ]
)

interview = len(
    [
        a for a in applications
        if a.get("status") == "Interview Scheduled"
    ]
)

offers = len(
    [
        a for a in applications
        if a.get("status") == "Offer"
    ]
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Applications",
        total
    )


with col2:

    st.metric(
        "Applied",
        applied
    )


with col3:

    st.metric(
        "Interviews",
        interview
    )


with col4:

    st.metric(
        "Offers",
        offers
    )


st.divider()


# --------------------------------------------------
# APPLICATION LIST
# --------------------------------------------------

st.subheader(
    "📌 Application Pipeline"
)


if applications:


    for index, application in enumerate(applications):


        with st.expander(
            f"{application.get('role')} - {application.get('company')}"
        ):


            st.write(
                "🌍 Country:",
                application.get(
                    "country",
                    ""
                )
            )


            st.write(
                "📅 Applied:",
                application.get(
                    "application_date",
                    ""
                )
            )


            st.metric(
                "Priority Score",
                f"{application.get('priority_score',0)}%"
            )


            st.metric(
                "Interview Probability",
                f"{application.get('interview_probability',0)}%"
            )


            status = st.selectbox(

                "Update Status",

                [
                    "Applied",
                    "Recruiter Contacted",
                    "Interview Scheduled",
                    "Final Round",
                    "Offer",
                    "Rejected"
                ],

                index=[
                    "Applied",
                    "Recruiter Contacted",
                    "Interview Scheduled",
                    "Final Round",
                    "Offer",
                    "Rejected"
                ].index(
                    application.get(
                        "status",
                        "Applied"
                    )
                ),

                key=f"status_{index}"

            )


            if st.button(
                "Update Status",
                key=f"update_{index}"
            ):

                tracker.update_status(
                    index,
                    status
                )

                st.success(
                    "✅ Status updated"
                )


            st.text_area(

                "Notes",

                application.get(
                    "notes",
                    ""
                ),

                key=f"notes_{index}"

            )


else:

    st.info(
        "No applications saved yet. Use 'Save Application' from AI Executive Jobs page."
    )