import streamlit as st

from modules.application_tracker import ApplicationTracker


st.set_page_config(
    page_title="Applications",
    page_icon="📌",
    layout="wide",
)


st.title("📌 Executive Applications Tracker")

st.caption(
    "Track, manage and monitor your executive job applications."
)


tracker = ApplicationTracker()

applications = tracker.get_applications()


# --------------------------------------------------
# HEADER METRICS
# --------------------------------------------------

stats = tracker.statistics()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total",
        stats["total"],
    )

with col2:
    st.metric(
        "Applied",
        stats["applied"],
    )

with col3:
    st.metric(
        "Interview",
        stats["interview"],
    )

with col4:
    st.metric(
        "Offer",
        stats["offer"],
    )

with col5:
    st.metric(
        "Rejected",
        stats["rejected"],
    )


st.divider()


# --------------------------------------------------
# APPLICATION LIST
# --------------------------------------------------

if not applications:

    st.info(
        "No applications recorded yet."
    )

else:

    st.subheader(
        f"📊 Applications: {len(applications)}"
    )


    for index, application in enumerate(
        applications,
        start=1,
    ):

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

        location = application.get(
            "location",
            "",
        )

        status = application.get(
            "status",
            "Applied",
        )

        application_id = application.get(
            "application_id",
            "",
        )

        application_date = application.get(
            "application_date",
            "",
        )

        last_updated = application.get(
            "last_updated",
            "",
        )

        priority_score = application.get(
            "priority_score",
            0,
        )

        executive_score = application.get(
            "executive_score",
            0,
        )

        recruiter = application.get(
            "recruiter",
            "",
        )

        notes = application.get(
            "notes",
            "",
        )


        with st.container(
            border=True
        ):

            st.markdown(
                f"### {index}. {role}"
            )

            st.write(
                f"**Company:** {company}"
            )

            location_text = " | ".join(
                value
                for value in [
                    location,
                    country,
                ]
                if value
            )

            if location_text:

                st.write(
                    f"**Location:** {location_text}"
                )


            col1, col2, col3 = st.columns(3)


            # --------------------------------------------------
            # STATUS
            # --------------------------------------------------

            with col1:

                statuses = [
                    "Applied",
                    "Interview",
                    "Offer",
                    "Rejected",
                    "Withdrawn",
                ]

                current_index = (
                    statuses.index(status)
                    if status in statuses
                    else 0
                )

                new_status = st.selectbox(
                    "Status",
                    statuses,
                    index=current_index,
                    key=f"application_status_{application_id}_{index}",
                )


            # --------------------------------------------------
            # SCORES
            # --------------------------------------------------

            with col2:

                st.write(
                    f"**Executive Score:** {executive_score}"
                )

                st.write(
                    f"**Priority Score:** {priority_score}"
                )


            # --------------------------------------------------
            # DATE
            # --------------------------------------------------

            with col3:

                st.write(
                    "**Applied:**"
                )

                st.write(
                    application_date
                )

                st.write(
                    "**Updated:**"
                )

                st.write(
                    last_updated
                )


            # --------------------------------------------------
            # STATUS UPDATE
            # --------------------------------------------------

            if new_status != status:

                if tracker.update_status(
                    application_id,
                    new_status,
                ):

                    st.success(
                        f"Application status updated to {new_status}."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Unable to update application status."
                    )


            # --------------------------------------------------
            # RECRUITER
            # --------------------------------------------------

            if recruiter:

                st.write(
                    f"**Recruiter:** {recruiter}"
                )


            # --------------------------------------------------
            # NOTES
            # --------------------------------------------------

            if notes:

                with st.expander(
                    "📝 Notes"
                ):

                    st.write(
                        notes
                    )


            # --------------------------------------------------
            # APPLICATION HISTORY
            # --------------------------------------------------

            history = application.get(
                "history",
                [],
            )

            if history:

                with st.expander(
                    "📜 Application History"
                ):

                    for event in reversed(
                        history
                    ):

                        event_date = event.get(
                            "date",
                            "",
                        )

                        event_status = event.get(
                            "status",
                            "",
                        )

                        st.write(
                            f"**{event_date}** — {event_status}"
                        )


            st.caption(
                f"Application ID: {application_id}"
            )