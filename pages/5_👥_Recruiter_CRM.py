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


st.write(
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
        "💾 Save Recruiter"
    ):


        manager.add_recruiter(
            recruiter_name,
            company,
            designation,
            linkedin,
            email,
            role,
            status,
            str(follow_up),
            notes
        )


        st.success(
            "✅ Recruiter saved successfully"
        )



# --------------------------------------------------
# VIEW RECRUITERS
# --------------------------------------------------

with tab2:


    recruiters = manager.get_recruiters()


    if recruiters:


        df = pd.DataFrame(
            recruiters
        )


        st.dataframe(
            df,
            width="stretch"
        )


    else:

        st.info(
            "No recruiters added yet."
        )