import streamlit as st

from modules.recruiter_manager import RecruiterManager


st.set_page_config(
    page_title="Recruiter CRM",
    page_icon="👥",
    layout="wide",
)


st.title("👥 Recruiter CRM")

st.caption(
    "Manage recruiter contacts and follow-ups."
)


manager = RecruiterManager()


# --------------------------------------------------
# ADD RECRUITER
# --------------------------------------------------

st.subheader("➕ Add Recruiter")


with st.form("add_recruiter"):

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Recruiter Name"
        )

        company = st.text_input(
            "Company"
        )

        designation = st.text_input(
            "Designation"
        )

    with col2:

        email = st.text_input(
            "Email"
        )

        linkedin = st.text_input(
            "LinkedIn"
        )

        phone = st.text_input(
            "Phone"
        )

    submitted = st.form_submit_button(
        "💾 Save Recruiter",
        use_container_width=True,
    )


    if submitted:

        if not name.strip():

            st.error(
                "Recruiter name is required."
            )

        else:

            manager.add_recruiter(
                {
                    "name": name.strip(),
                    "company": company.strip(),
                    "designation": designation.strip(),
                    "email": email.strip(),
                    "linkedin": linkedin.strip(),
                    "phone": phone.strip(),
                }
            )

            st.success(
                "Recruiter saved successfully."
            )

            st.rerun()


# --------------------------------------------------
# LOAD RECRUITERS
# --------------------------------------------------

recruiters = (
    manager.get_all_recruiters()
)


st.divider()


st.subheader(
    f"📊 Recruiters: {len(recruiters)}"
)


# --------------------------------------------------
# DISPLAY
# --------------------------------------------------

if not recruiters:

    st.info(
        "No recruiters added yet."
    )

else:

    for index, recruiter in enumerate(
        recruiters,
        start=1,
    ):

        with st.container(
            border=True
        ):

            st.markdown(
                f"### {index}. "
                f"{recruiter.get('name', 'Recruiter')}"
            )

            company = recruiter.get(
                "company",
                "",
            )

            designation = recruiter.get(
                "designation",
                "",
            )

            email = recruiter.get(
                "email",
                "",
            )

            phone = recruiter.get(
                "phone",
                "",
            )

            linkedin = recruiter.get(
                "linkedin",
                "",
            )


            if company:

                st.write(
                    f"**Company:** {company}"
                )

            if designation:

                st.write(
                    f"**Designation:** {designation}"
                )

            if email:

                st.write(
                    f"**Email:** {email}"
                )

            if phone:

                st.write(
                    f"**Phone:** {phone}"
                )

            if linkedin:

                st.markdown(
                    f"[🔗 LinkedIn]({linkedin})"
                )


            st.divider()


            # --------------------------------------------------
            # FOLLOW-UP
            # --------------------------------------------------

            st.markdown(
                "#### 📅 Follow-up"
            )


            statuses = [
                "Not Contacted",
                "Contacted",
                "Follow-up Required",
                "Responded",
                "Interview",
                "Closed",
            ]


            current_status = recruiter.get(
                "follow_up_status",
                "Not Contacted",
            )


            if current_status not in statuses:

                current_status = (
                    "Not Contacted"
                )


            selected_status = st.selectbox(
                "Status",
                statuses,
                index=statuses.index(
                    current_status
                ),
                key=f"status_{index}",
            )


            follow_up_date = st.text_input(
                "Next Follow-up Date",
                value=recruiter.get(
                    "follow_up_date",
                    "",
                ),
                key=f"date_{index}",
            )


            notes = st.text_area(
                "Notes",
                value=recruiter.get(
                    "notes",
                    "",
                ),
                key=f"notes_{index}",
            )


            if st.button(
                "💾 Update Follow-up",
                key=f"update_{index}",
                use_container_width=True,
            ):

                updates = {
                    "follow_up_status":
                        selected_status,

                    "follow_up_date":
                        follow_up_date,

                    "notes":
                        notes,
                }


                success = (
                    manager.update_recruiter(
                        index - 1,
                        updates,
                    )
                )


                if success:

                    st.success(
                        "Follow-up updated successfully."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Unable to update recruiter."
                    )