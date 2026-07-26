import streamlit as st
import pandas as pd

from modules.recruiter_manager import RecruiterManager


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Recruiter CRM",
    page_icon="👥",
    layout="wide"
)


st.title(
    "👥 Recruiter Relationship Manager"
)

st.caption(
    "Manage recruiter contacts, follow-ups and hiring relationships."
)


manager = RecruiterManager()


tab1, tab2 = st.tabs(
    [
        "➕ Add Recruiter",
        "📋 Recruiter Database"
    ]
)


# --------------------------------------------------
# ADD RECRUITER
# --------------------------------------------------

with tab1:

    recruiter_name = st.text_input(
        "Recruiter Name"
    )

    company = st.text_input(
        "Company"
    )

    designation = st.text_input(
        "Recruiter Designation"
    )

    linkedin = st.text_input(
        "LinkedIn Profile"
    )

    email = st.text_input(
        "Email"
    )

    role = st.text_input(
        "Hiring Role"
    )

    status = st.selectbox(
        "Status",
        [
            "New",
            "Contacted",
            "Connected",
            "Interview Discussion",
            "Closed"
        ]
    )

    follow_up = st.date_input(
        "Follow-up Date"
    )

    notes = st.text_area(
        "Notes"
    )


    if st.button(
        "💾 Save Recruiter",
        type="primary"
    ):


        recruiter = {

            "name": recruiter_name,

            "company": company,

            "designation": designation,

            "linkedin": linkedin,

            "email": email,

            "role": role,

            "status": status,

            "follow_up": str(follow_up),

            "notes": notes

        }


        try:

            manager.add_recruiter(
                recruiter
            )

            st.success(
                "✅ Recruiter saved successfully"
            )


        except Exception as e:

            st.error(
                f"Unable to save recruiter: {e}"
            )



# --------------------------------------------------
# VIEW RECRUITERS
# --------------------------------------------------

with tab2:


    try:

        recruiters = manager.get_recruiters()


    except Exception as e:

        recruiters = []

        st.error(
            f"Unable to load recruiters: {e}"
        )


    if recruiters:


        df = pd.DataFrame(
            recruiters
        )


        st.dataframe(
            df,
            use_container_width=True
        )


    else:


        st.info(
            "No recruiters added yet."
        )



# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "JobHunter AI • Recruiter CRM Suite"
)