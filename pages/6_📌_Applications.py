import streamlit as st
import pandas as pd

from modules.application_manager import ApplicationManager

from modules.ui_components import (
    page_header,
    section_header,
    success_box,
    empty_state,
)

st.set_page_config(
    page_title="Applications Tracker",
    page_icon="📌",
    layout="wide",
)

page_header(
    "📌 Executive Application Tracker",
    "Track and manage your global executive job applications."
)

manager = ApplicationManager()

tab1, tab2 = st.tabs(
    [
        "➕ Add Application",
        "📋 Application Pipeline",
    ]
)

# --------------------------------------------------
# ADD APPLICATION
# --------------------------------------------------

with tab1:

    section_header("New Executive Application")

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
            "Rejected",
        ],
    )

    notes = st.text_area(
        "Notes"
    )

    if st.button(
        "💾 Save Application",
        type="primary",
    ):

        manager.add_application(
            company,
            role,
            country,
            location,
            status,
            notes,
        )

        success_box(
            "✅ Application saved successfully."
        )

# --------------------------------------------------
# APPLICATION PIPELINE
# --------------------------------------------------

with tab2:

    section_header(
        "Application Pipeline"
    )

    applications = manager.get_applications()

    if applications:

        df = pd.DataFrame(
            applications
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        empty_state(
            "No applications tracked yet."
        )