import streamlit as st

from modules.application_manager import ApplicationManager


st.set_page_config(
    page_title="Applications",
    page_icon="📌",
    layout="wide",
)


st.title(
    "📌 Applications Tracker"
)

st.caption(
    "Track and manage your executive job applications."
)


manager = ApplicationManager()

applications = (
    manager.get_all_applications()
)


st.subheader(
    f"📊 Applications: {len(applications)}"
)


if not applications:

    st.info(
        "No applications recorded yet."
    )

else:

    for index, application in enumerate(
        applications,
        start=1,
    ):

        title = application.get(
            "job_title",
            application.get(
                "title",
                application.get(
                    "role",
                    "Executive Position",
                ),
            ),
        )

        company = application.get(
            "company",
            "Company",
        )

        location = application.get(
            "location",
            "",
        )

        status = application.get(
            "status",
            "Applied",
        )

        applied_on = application.get(
            "applied_on",
            "",
        )

        apply_link = application.get(
            "apply_link",
            "",
        )


        with st.container(
            border=True
        ):

            st.markdown(
                f"### {index}. {title}"
            )

            st.write(
                f"**Company:** {company}"
            )

            if location:

                st.write(
                    f"**Location:** {location}"
                )


            col1, col2, col3 = st.columns(
                3
            )


            with col1:

                new_status = st.selectbox(
                    "Status",
                    [
                        "Applied",
                        "Interview",
                        "Offer",
                        "Rejected",
                        "Withdrawn",
                    ],
                    index=[
                        "Applied",
                        "Interview",
                        "Offer",
                        "Rejected",
                        "Withdrawn",
                    ].index(
                        status
                    )
                    if status
                    in [
                        "Applied",
                        "Interview",
                        "Offer",
                        "Rejected",
                        "Withdrawn",
                    ]
                    else 0,
                    key=f"status_{index}",
                )


            with col2:

                st.write(
                    "**Applied On:**"
                )

                st.write(
                    applied_on
                )


            with col3:

                if apply_link:

                    st.link_button(
                        "🔗 Open Job",
                        apply_link,
                        use_container_width=True,
                    )


            if new_status != status:

                if manager.update_status(
                    index - 1,
                    new_status,
                ):

                    st.success(
                        f"Status updated to {new_status}."
                    )

                    st.rerun()


            st.divider()