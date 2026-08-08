import streamlit as st

from modules.profile_manager import ProfileManager


st.set_page_config(
    page_title="Executive Profile",
    page_icon="👤",
    layout="wide",
)

st.title("👤 Executive Profile")

st.caption(
    "Your central executive career profile used across JobHunter."
)


profile_manager = ProfileManager()
profile = profile_manager.load_profile()


# --------------------------------------------------
# DEFAULT PROFILE
# --------------------------------------------------

if not isinstance(profile, dict):
    profile = {}


defaults = {
    "name": "",
    "email": "",
    "phone": "",
    "linkedin": "",
    "location": "",
    "current_role": "",
    "experience": "23+ Years",
    "target_roles": [],
    "target_countries": [],
    "skills": [],
    "achievements": [],
    "education": [],
}


for key, default_value in defaults.items():

    if key not in profile:
        profile[key] = default_value


# --------------------------------------------------
# PROFILE STATUS
# --------------------------------------------------

if profile_manager.profile_exists():

    st.success(
        "✅ Executive profile loaded successfully."
    )

else:

    st.info(
        "No saved profile found yet. "
        "Complete the profile below and click Save Executive Profile."
    )


# --------------------------------------------------
# PERSONAL INFORMATION
# --------------------------------------------------

st.subheader("👤 Personal Information")

col1, col2 = st.columns(2)


with col1:

    name = st.text_input(
        "Full Name",
        value=str(profile.get("name", "")),
    )

    email = st.text_input(
        "Email",
        value=str(profile.get("email", "")),
    )

    phone = st.text_input(
        "Phone",
        value=str(profile.get("phone", "")),
    )


with col2:

    linkedin = st.text_input(
        "LinkedIn",
        value=str(profile.get("linkedin", "")),
    )

    location = st.text_input(
        "Current Location",
        value=str(profile.get("location", "")),
    )


# --------------------------------------------------
# PROFESSIONAL INFORMATION
# --------------------------------------------------

st.divider()

st.subheader("💼 Professional Information")

col1, col2 = st.columns(2)


with col1:

    current_role = st.text_input(
        "Current / Target Executive Role",
        value=str(profile.get("current_role", "")),
    )


with col2:

    experience = st.text_input(
        "Total Experience",
        value=str(
            profile.get(
                "experience",
                "23+ Years",
            )
        ),
    )


# --------------------------------------------------
# TARGET ROLES
# --------------------------------------------------

st.subheader("🎯 Target Roles")

target_roles = profile.get(
    "target_roles",
    [],
)

if not isinstance(target_roles, list):
    target_roles = []


target_roles_text = st.text_area(
    "One role per line",
    value="\n".join(
        str(role)
        for role in target_roles
    ),
    height=120,
    placeholder=(
        "Head of Sales\n"
        "VP Sales\n"
        "Regional Sales Director\n"
        "Head of Business Development"
    ),
)


# --------------------------------------------------
# TARGET COUNTRIES
# --------------------------------------------------

st.subheader("🌍 Target Countries")

target_countries = profile.get(
    "target_countries",
    [],
)

if not isinstance(target_countries, list):
    target_countries = []


target_countries_text = st.text_area(
    "One country / market per line",
    value="\n".join(
        str(country)
        for country in target_countries
    ),
    height=120,
    placeholder=(
        "Singapore\n"
        "UAE\n"
        "Saudi Arabia\n"
        "Germany"
    ),
)


# --------------------------------------------------
# SKILLS
# --------------------------------------------------

st.divider()

st.subheader("🧠 Skills Portfolio")

skills = profile.get(
    "skills",
    [],
)

if not isinstance(skills, list):
    skills = []


skills_text = st.text_area(
    "One skill per line",
    value="\n".join(
        str(skill)
        for skill in skills
    ),
    height=220,
    placeholder=(
        "Strategic Sales Leadership\n"
        "P&L Management\n"
        "Business Development\n"
        "SaaS\n"
        "CRM\n"
        "Customer Success"
    ),
)


# --------------------------------------------------
# ACHIEVEMENTS
# --------------------------------------------------

st.subheader("🏆 Key Achievements")

achievements = profile.get(
    "achievements",
    [],
)

if not isinstance(achievements, list):
    achievements = []


achievements_text = st.text_area(
    "One achievement per line",
    value="\n".join(
        str(item)
        for item in achievements
    ),
    height=220,
    placeholder=(
        "Scaled ARR from $2.4M to $6M.\n"
        "Managed $12M+ revenue operations.\n"
        "Led teams of 450+ personnel."
    ),
)


# --------------------------------------------------
# EDUCATION
# --------------------------------------------------

st.subheader("🎓 Education")

education = profile.get(
    "education",
    [],
)

if not isinstance(education, list):
    education = []


education_text = st.text_area(
    "One qualification per line",
    value="\n".join(
        str(item)
        for item in education
    ),
    height=140,
    placeholder=(
        "Electronics & Communication Engineering\n"
        "Additional Executive Certifications"
    ),
)


# --------------------------------------------------
# SAVE PROFILE
# --------------------------------------------------

st.divider()

if st.button(
    "💾 Save Executive Profile",
    type="primary",
    use_container_width=True,
):

    updated_profile = {

        "name": name.strip(),

        "email": email.strip(),

        "phone": phone.strip(),

        "linkedin": linkedin.strip(),

        "location": location.strip(),

        "current_role": current_role.strip(),

        "experience": experience.strip(),

        "target_roles": [
            item.strip()
            for item in target_roles_text.splitlines()
            if item.strip()
        ],

        "target_countries": [
            item.strip()
            for item in target_countries_text.splitlines()
            if item.strip()
        ],

        "skills": [
            item.strip()
            for item in skills_text.splitlines()
            if item.strip()
        ],

        "achievements": [
            item.strip()
            for item in achievements_text.splitlines()
            if item.strip()
        ],

        "education": [
            item.strip()
            for item in education_text.splitlines()
            if item.strip()
        ],
    }


    if profile_manager.save_profile(
        updated_profile
    ):

        st.success(
            "✅ Executive profile saved successfully."
        )

        st.rerun()

    else:

        st.error(
            "❌ Unable to save Executive Profile."
        )