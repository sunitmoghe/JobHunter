import streamlit as st

from modules.database import DatabaseManager


st.set_page_config(
    page_title="Executive Profile",
    page_icon="👤",
    layout="wide"
)


st.title("👤 Executive Profile")


db = DatabaseManager()

profile = db.get_latest_profile()

db.close()


if profile:

    st.success("Profile loaded from database")


    col1, col2 = st.columns(2)


    with col1:

        st.subheader("Personal Information")

        st.write("**Name:**", profile["name"])

        st.write("**Email:**", profile["email"])

        st.write("**Phone:**", profile["phone"])


    with col2:

        st.subheader("Professional Information")

        st.write(
            "**Experience:**",
            profile["experience"]
        )

        st.write(
            "**LinkedIn:**",
            profile["linkedin"]
        )


    st.divider()


    st.subheader("🛠 Skills Portfolio")


    skills = profile["skills"]


    for skill in skills:
        st.success(skill)


else:

    st.warning(
        "No executive profile found. Please upload a resume first."
    )