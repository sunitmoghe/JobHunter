import streamlit as st

from modules.application_assistant import ApplicationAssistant
from modules.application_tracker import ApplicationTracker
from modules.application_assistant import ApplicationAssistant
from modules.recruiter_manager import RecruiterManager
from modules.recruiter_outreach_ai import RecruiterOutreachAI


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Recruiter Manager",
    page_icon="🤝",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title(
    "🤝 Recruiter Intelligence Manager"
)

st.write(
    "Manage recruiter relationships, outreach and follow-ups."
)


recruiter_manager = RecruiterManager()

outreach_ai = RecruiterOutreachAI()

application_assistant = ApplicationAssistant()


# --------------------------------------------------
# ADD RECRUITER
# --------------------------------------------------

st.subheader(
    "➕ Add Recruiter"
)


with st.form(
    "add_recruiter"
):

    name = st.text_input(
        "Recruiter Name"
    )

    company = st.text_input(
        "Company"
    )

    role = st.text_input(
        "Role / Department"
    )

    linkedin = st.text_input(
        "LinkedIn URL"
    )

    email = st.text_input(
        "Email"
    )


    submit = st.form_submit_button(
        "Save Recruiter"
    )


    if submit:

        recruiter_manager.add_recruiter(
            name,
            company,
            role,
            linkedin,
            email
        )

        st.success(
            "✅ Recruiter saved"
        )


st.divider()


# --------------------------------------------------
# RECRUITER LIST
# --------------------------------------------------

st.subheader(
    "📋 Recruiter Pipeline"
)


recruiters = recruiter_manager.get_recruiters()


if recruiters:


    for index, recruiter in enumerate(recruiters):


        with st.expander(
            f"{recruiter.get('name')} - {recruiter.get('company')}"
        ):


            st.write(
                "Role:",
                recruiter.get(
                    "role",
                    ""
                )
            )


            st.write(
                "LinkedIn:",
                recruiter.get(
                    "linkedin",
                    ""
                )
            )


            st.write(
                "Email:",
                recruiter.get(
                    "email",
                    ""
                )
            )


            status = st.selectbox(

                "Status",

                [
                    "New",
                    "Contacted",
                    "Replied",
                    "Interview Support",
                    "Closed"
                ],

                index=[
                    "New",
                    "Contacted",
                    "Replied",
                    "Interview Support",
                    "Closed"
                ].index(
                    recruiter.get(
                        "status",
                        "New"
                    )
                ),

                key=f"status_{index}"

            )


            if st.button(
                "Update Status",
                key=f"update_{index}"
            ):

                recruiter_manager.update_status(
                    index,
                    status
                )

                st.success(
                    "Status updated"
                )


            notes = st.text_area(

                "Notes",

                recruiter.get(
                    "notes",
                    ""
                ),

                key=f"notes_{index}"

            )


            if st.button(
                "Save Notes",
                key=f"notes_save_{index}"
            ):

                recruiter_manager.update_notes(
                    index,
                    notes
                )

                st.success(
                    "Notes saved"
                )
            st.divider()


            st.subheader(
                "🤖 AI Recruiter Outreach"
            )


            if st.button(
                "💬 Generate LinkedIn Message",
                key=f"linkedin_{index}"
            ):

                message = outreach_ai.generate_connection_message(
                    {},
                    recruiter
                )

                st.text_area(
                    "LinkedIn Message",
                    message,
                    height=250,
                    key=f"linkedin_msg_{index}"
                )


            if st.button(
                "📨 Generate Follow-up Message",
                key=f"followup_{index}"
            ):

                message = outreach_ai.generate_followup_message(
                    recruiter
                )

                st.text_area(
                    "Follow-up Message",
                    message,
                    height=250,
                    key=f"followup_msg_{index}"
                )

else:

    st.info(
        "No recruiters added yet."
    )