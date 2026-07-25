import streamlit as st
import pandas as pd

from modules.application_manager import ApplicationManager


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Applications Tracker",
    page_icon="📌",
    layout="wide"
)


st.title(
    "📌 Executive Application Tracker"
)


st.write(
    "Track your global executive job applications."
)


manager = ApplicationManager()


tab1, tab2 = st.tabs(
    [
        "➕ Add Application",
        "📋 Application Pipeline"
    ]
)


# --------------------------------------------------
# ADD APPLICATION
# --------------------------------------------------

with tab1:


    company = st.text_input(
        "Company"
    )


    role = st.text_input(
        "Role"
    )


    country = st.text_input(
        "Country"
    )


    location = st.text_input(
        "Location"
    )


    status = st.selectbox(
        "Application Status",
        [
            "Applied",
            "Recruiter Contacted",
            "Interview",
            "Offer",
            "Rejected"
        ]
    )


    notes = st.text_area(
        "Notes"
    )


    if st.button(
        "💾 Save Application"
    ):


        manager.add_application(
            company,
            role,
            country,
            location,
            status,
            notes
        )


        st.success(
            "✅ Application saved successfully"
        )


# --------------------------------------------------
# VIEW APPLICATIONS
# --------------------------------------------------

with tab2:


    applications = manager.get_applications()


    if applications:


        df = pd.DataFrame(
            applications
        )


        st.dataframe(
            df,
            width="stretch"
        )


    else:

        st.info(
            "No applications tracked yet."
        )