import streamlit as st

from modules.recruiter_manager import RecruiterManager


st.set_page_config(
    page_title="Recruiter Manager",
    page_icon="🤝",
    layout="wide",
)


st.title("🤝 Recruiter Manager")

st.caption(
    "Manage recruiter relationships, contacts and follow-ups."
)


manager = RecruiterManager()


# ==================================================
# LOAD RECRUITERS
# ==================================================

try:

    recruiters = manager.get_all_recruiters()

except Exception as error:

    st.error(
        "Unable to load recruiters."
    )

    st.exception(error)

    recruiters = []


# ==================================================
# STATISTICS
# ==================================================

total_recruiters = len(
    recruiters
)

contacted_recruiters = sum(
    1
    for recruiter in recruiters
    if recruiter.get(
        "follow_up_status",
        "",
    ) in [
        "Contacted",
        "Responded",
        "Interview",
    ]
)

follow_up_required = sum(
    1
    for recruiter in recruiters
    if recruiter.get(
        "follow_up_status",
        "",
    ) == "Follow-up Required"
)

interviews = sum(
    1
    for recruiter in recruiters
    if recruiter.get(
        "follow_up_status",
        "",
    ) == "Interview"
)


# ==================================================
# KPI CARDS
# ==================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Recruiters",
        total_recruiters,
    )


with col2:

    st.metric(
        "Contacted",
        contacted_recruiters,
    )


with col3:

    st.metric(
        "Follow-up Required",
        follow_up_required,
    )


with col4:

    st.metric(
        "Interviews",
        interviews,
    )


st.divider()


# ==================================================
# ADD RECRUITER
# ==================================================

st.subheader(
    "➕ Add Recruiter"
)


with st.form(
    "add_recruiter_form"
):

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

        phone = st.text_input(
            "Phone"
        )

        linkedin = st.text_input(
            "LinkedIn URL"
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

            try:

                manager.add_recruiter(
                    {
                        "name":
                            name.strip(),

                        "company":
                            company.strip(),

                        "designation":
                            designation.strip(),

                        "email":
                            email.strip(),

                        "phone":
                            phone.strip(),

                        "linkedin":
                            linkedin.strip(),

                        "follow_up_status":
                            "Not Contacted",

                        "follow_up_date":
                            "",

                        "notes":
                            "",
                    }
                )

                st.success(
                    "Recruiter saved successfully."
                )

                st.rerun()


            except Exception as error:

                st.error(
                    "Unable to save recruiter."
                )

                st.exception(error)


st.divider()


# ==================================================
# RECRUITER LIST
# ==================================================

st.subheader(
    f"👥 Recruiter Database ({len(recruiters)})"
)


if not recruiters:

    st.info(
        "No recruiters added yet."
    )


else:

    for index, recruiter in enumerate(
        recruiters,
        start=1,
    ):

        name = recruiter.get(
            "name",
            "Recruiter",
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

        status = recruiter.get(
            "follow_up_status",
            "Not Contacted",
        )

        follow_up_date = recruiter.get(
            "follow_up_date",
            "",
        )

        notes = recruiter.get(
            "notes",
            "",
        )


        if status not in [
            "Not Contacted",
            "Contacted",
            "Follow-up Required",
            "Responded",
            "Interview",
            "Closed",
        ]:

            status = "Not Contacted"


        # --------------------------------------------------
        # CARD
        # --------------------------------------------------

        with st.container(
            border=True
        ):

            st.markdown(
                f"### {index}. {name}"
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
                    f"[🔗 LinkedIn Profile]({linkedin})"
                )


            st.divider()


            # --------------------------------------------------
            # FOLLOW-UP
            # --------------------------------------------------

            st.markdown(
                "#### 📅 Follow-up Management"
            )


            col1, col2 = st.columns(2)


            with col1:

                selected_status = st.selectbox(
                    "Status",
                    [
                        "Not Contacted",
                        "Contacted",
                        "Follow-up Required",
                        "Responded",
                        "Interview",
                        "Closed",
                    ],
                    index=[
                        "Not Contacted",
                        "Contacted",
                        "Follow-up Required",
                        "Responded",
                        "Interview",
                        "Closed",
                    ].index(status),
                    key=f"status_{index}",
                )


            with col2:

                selected_date = st.text_input(
                    "Next Follow-up Date",
                    value=follow_up_date,
                    key=f"date_{index}",
                )


            selected_notes = st.text_area(
                "Notes",
                value=notes,
                key=f"notes_{index}",
            )


            # --------------------------------------------------
            # UPDATE
            # --------------------------------------------------

            if st.button(
                "💾 Update Recruiter",
                key=f"update_{index}",
                use_container_width=True,
            ):

                updates = {

                    "name":
                        name,

                    "company":
                        company,

                    "designation":
                        designation,

                    "email":
                        email,

                    "phone":
                        phone,

                    "linkedin":
                        linkedin,

                    "follow_up_status":
                        selected_status,

                    "follow_up_date":
                        selected_date,

                    "notes":
                        selected_notes,
                }


                try:

                    current_recruiters = (
                        manager._load()
                    )


                    recruiter_index = (
                        index - 1
                    )


                    if (
                        0
                        <= recruiter_index
                        < len(
                            current_recruiters
                        )
                    ):

                        current_recruiters[
                            recruiter_index
                        ].update(
                            updates
                        )


                        manager._save(
                            current_recruiters
                        )


                        st.success(
                            "Recruiter updated successfully."
                        )

                        st.rerun()


                    else:

                        st.error(
                            "Recruiter not found."
                        )


                except Exception as error:

                    st.error(
                        "Unable to update recruiter."
                    )

                    st.exception(error)