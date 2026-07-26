import streamlit as st

from modules.recruiter_manager import RecruiterManager


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Recruiter Manager",
    page_icon="🤝",
    layout="wide"
)


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("🤝 Executive Recruiter Manager")

st.write(
    "Manage executive recruiters, relationships and follow-ups."
)

st.divider()


# --------------------------------------------------
# INITIALISE MANAGER
# --------------------------------------------------

manager = RecruiterManager()


# --------------------------------------------------
# LOAD RECRUITERS
# --------------------------------------------------

recruiters = manager.get_recruiters()


# --------------------------------------------------
# DASHBOARD METRICS
# --------------------------------------------------

stats = manager.get_statistics()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Recruiters", stats["total_recruiters"])

with col2:
    st.metric("Contacted", stats["contacted"])

with col3:
    st.metric("Responded", stats["responded"])

with col4:
    st.metric("Response Rate", f"{stats['response_rate']}%")

st.divider()

# --------------------------------------------------
# ADD NEW RECRUITER
# --------------------------------------------------

st.subheader("➕ Add Executive Recruiter")

with st.form("add_recruiter_form"):

    name = st.text_input("Recruiter Name")

    company = st.text_input("Company")

    designation = st.text_input("Designation")

    email = st.text_input("Email")

    linkedin = st.text_input("LinkedIn URL")

    country = st.text_input("Country")

    notes = st.text_area("Notes")

    submitted = st.form_submit_button("Save Recruiter")

    if submitted:

        recruiter = {

            "name": name,

            "company": company,

            "designation": designation,

            "email": email,

            "linkedin": linkedin,

            "country": country,

            "notes": notes

        }

        manager.add_recruiter(recruiter)

        st.success("✅ Recruiter saved successfully.")

        st.rerun()

# --------------------------------------------------
# RECRUITER DATABASE
# --------------------------------------------------

st.divider()

st.subheader("📋 Recruiter Database")

recruiters = manager.get_recruiters()

if not recruiters:

    st.info("No recruiters have been added yet.")

else:

    search = st.text_input(
        "🔍 Search Recruiters"
    )

    if search:

        recruiters = manager.search_recruiters(search)

    st.write(
        f"Showing {len(recruiters)} recruiter(s)"
    )

    for i, recruiter in enumerate(recruiters):

        with st.expander(
            f"{recruiter.get('name','Unknown')} | {recruiter.get('company','')}"
        ):

            st.write(
                f"**Designation:** {recruiter.get('designation','')}"
            )

            st.write(
                f"**Country:** {recruiter.get('country','')}"
            )

            st.write(
                f"**Email:** {recruiter.get('email','')}"
            )

            st.write(
                f"**LinkedIn:** {recruiter.get('linkedin','')}"
            )

            st.write(
                f"**Status:** {recruiter.get('status','New')}"
            )

            st.write(
                f"**Last Contact:** {recruiter.get('last_contact','')}"
            )

            st.write(
                f"**Notes:** {recruiter.get('notes','')}"
            )

