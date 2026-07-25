import streamlit as st

from modules.profile_pipeline import process_resume


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Resume Intelligence",
    page_icon="📄",
    layout="wide"
)


# --------------------------------------------------
# RESUME INTELLIGENCE
# --------------------------------------------------

st.title(
    "📄 Resume Intelligence Engine"
)


st.write(
    "Upload your resume and generate your Executive Profile."
)


uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)


if uploaded_resume:


    with open(
        "temp_resume.pdf",
        "wb"
    ) as f:

        f.write(
            uploaded_resume.getbuffer()
        )


    with st.spinner(
        "Analysing resume and creating executive profile..."
    ):

        profile = process_resume(
            "temp_resume.pdf"
        )


    st.success(
        "✅ Executive Profile Created Successfully"
    )


    st.divider()


    st.subheader(
        "👤 Executive Profile"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.write(
            "**Name:**",
            profile.get(
                "name",
                "Not Available"
            )
        )


        st.write(
            "**Email:**",
            profile.get(
                "email",
                "Not Available"
            )
        )


        st.write(
            "**Phone:**",
            profile.get(
                "phone",
                "Not Available"
            )
        )


        st.write(
            "**Experience:**",
            profile.get(
                "experience",
                "Not Available"
            )
        )


    with col2:

        st.write(
            "**LinkedIn:**",
            profile.get(
                "linkedin",
                "Not Available"
            )
        )


        st.write(
            "**Location:**",
            profile.get(
                "location",
                "Not Available"
            )
        )


        st.write(
            "**Current Role:**",
            profile.get(
                "current_role",
                "Not Available"
            )
        )


        st.write(
            "**Industry:**",
            profile.get(
                "industry",
                "Not Available"
            )
        )


    st.divider()


    st.subheader(
        "🛠 Skills Detected"
    )


    skills = profile.get(
        "skills",
        []
    )


    if skills:

        for skill in skills:

            st.success(
                skill
            )

    else:

        st.info(
            "No skills detected"
        )


    st.divider()


    st.subheader(
        "📊 Profile Summary"
    )


    st.json(
        profile
    )


else:

    st.info(
        "Please upload a PDF resume to begin analysis."
    )