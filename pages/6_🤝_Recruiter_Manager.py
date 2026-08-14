import streamlit as st

from modules.recruiter_manager import RecruiterManager
from modules.executive_recruiter_action_center import (
    ExecutiveRecruiterActionCenter,
)
from modules.profile_manager import ProfileManager


st.set_page_config(
    page_title="Recruiter Manager",
    page_icon="🤝",
    layout="wide",
)


st.title("🤝 Recruiter Manager")

st.caption(
    "Manage recruiter relationships, outreach and follow-ups."
)


manager = RecruiterManager()
profile_manager = ProfileManager()
action_center = ExecutiveRecruiterActionCenter()


# ==========================================================
# PROFILE
# ==========================================================

if profile_manager.profile_exists():

    profile = profile_manager.load_profile()

else:

    profile = {
        "name": "Sunit Moghe",
        "experience": 23,
    }


# ==========================================================
# LOAD RECRUITERS
# ==========================================================

try:

    recruiters = manager.get_all_recruiters()

except Exception as error:

    st.error(
        "Unable to load recruiters."
    )

    st.exception(error)

    recruiters = []


# ==========================================================
# STATISTICS
# ==========================================================

total_recruiters = len(
    recruiters
)

contacted_recruiters = sum(
    1
    for recruiter in recruiters
    if recruiter.get(
        "follow_up_status",
        "",
    )
    in [
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
    )
    == "Follow-up Required"
)

interviews = sum(
    1
    for recruiter in recruiters
    if recruiter.get(
        "follow_up_status",
        "",
    )
    == "Interview"
)


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


# ==========================================================
# RECRUITER ACTION CENTER
# ==========================================================

st.subheader(
    "🎯 Recruiter Action Center"
)

st.caption(
    "Prioritize recruiters and generate outreach from your existing recruiter database."
)


job_role = st.text_input(
    "Target executive role",
    value="Head of Sales",
    key="recruiter_target_role",
)

job_company = st.text_input(
    "Target company",
    value="",
    key="recruiter_target_company",
)


if st.button(
    "🔄 Analyze Recruiters",
    type="primary",
    use_container_width=True,
):

    try:

        actions = (
            action_center
            .prioritize_recruiters(
                profile,
                recruiters,
                {
                    "role": job_role,
                    "company": job_company,
                },
            )
        )

        st.session_state[
            "recruiter_actions"
        ] = actions

    except Exception as error:

        st.error(
            "Unable to analyze recruiters."
        )

        st.exception(error)


recruiter_actions = st.session_state.get(
    "recruiter_actions",
    [],
)


if recruiter_actions:

    for index, action in enumerate(
        recruiter_actions,
        start=1,
    ):

        priority = action.get(
            "priority",
            "Medium",
        )

        if priority == "High":

            badge = "🔴"

        elif priority == "Medium":

            badge = "🟠"

        else:

            badge = "⚪"


        with st.container(
            border=True
        ):

            st.markdown(
                f"### {index}. {action.get('recruiter_name', 'Recruiter')}"
            )

            st.write(
                f"**Company:** {action.get('company', '')}"
            )

            st.write(
                f"**Role:** {action.get('role', '')}"
            )


            score1, score2, score3 = st.columns(3)

            with score1:

                st.metric(
                    "Recruiter Score",
                    action.get(
                        "recruiter_score",
                        0,
                    ),
                )

            with score2:

                st.metric(
                    "Priority",
                    f"{badge} {priority}",
                )

            with score3:

                st.metric(
                    "Response Rate",
                    action.get(
                        "response_rate",
                        "—",
                    ),
                )


            if action.get(
                "recommendation"
            ):

                st.info(
                    action[
                        "recommendation"
                    ]
                )


            linkedin = action.get(
                "linkedin",
                "",
            )

            if linkedin:

                st.link_button(
                    "🔗 Open LinkedIn",
                    linkedin,
                )


            with st.expander(
                "💬 Connection Message"
            ):

                st.text_area(
                    "",
                    action.get(
                        "connection_message",
                        "",
                    ),
                    height=220,
                    key=f"connection_{index}",
                )


            with st.expander(
                "📩 Follow-up Message"
            ):

                st.text_area(
                    "",
                    action.get(
                        "follow_up_message",
                        "",
                    ),
                    height=220,
                    key=f"followup_{index}",
                )


            st.write(
                f"**Suggested Follow-up:** "
                f"{action.get('follow_up_date', '')}"
            )


    st.divider()


# ==========================================================
# ADD RECRUITER
# ==========================================================

st.subheader(
    "➕ Add Recruiter"
)


with st.form(
    "add_recruiter_form"
):

    left, right = st.columns(2)

    with left:

        name = st.text_input(
            "Recruiter Name"
        )

        company = st.text_input(
            "Company"
        )

        designation = st.text_input(
            "Designation"
        )

    with right:

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


# ==========================================================
# RECRUITER DATABASE
# ==========================================================

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
            recruiter.get(
                "recruiter_name",
                "Recruiter",
            ),
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

                st.link_button(
                    "🔗 LinkedIn Profile",
                    linkedin,
                )


            st.markdown(
                "#### 📅 Follow-up Management"
            )


            col1, col2 = st.columns(2)


            with col1:

                statuses = [
                    "Not Contacted",
                    "Contacted",
                    "Follow-up Required",
                    "Responded",
                    "Interview",
                    "Closed",
                ]

                current_index = (
                    statuses.index(status)
                    if status in statuses
                    else 0
                )

                selected_status = st.selectbox(
                    "Status",
                    statuses,
                    index=current_index,
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


            if st.button(
                "💾 Update Recruiter",
                key=f"update_{index}",
                use_container_width=True,
            ):

                success = manager.update_recruiter(
                    index - 1,
                    {
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
                    },
                )

                if success:

                    st.success(
                        "Recruiter updated successfully."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Unable to update recruiter."
                    )