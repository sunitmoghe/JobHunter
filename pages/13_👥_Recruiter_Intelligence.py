import streamlit as st

def success_box(message):
    st.success(message)

def error_box(message):
    st.error(message)

def info_box(message):
    st.info(message)

def warning_box(message):
    st.warning(message)

def page_header(title, subtitle=None, icon=""):
    if icon:
        st.title(f"{icon} {title}")
    else:
        st.title(title)

    if subtitle:
        st.caption(subtitle)

def section_header(title, icon=""):
    if icon:
        st.subheader(f"{icon} {title}")
    else:
        st.subheader(title)

def metric_card(label, value):
    st.metric(label, value)

def divider():
    st.divider()

def job_card(job):
    title = job.get("title", job.get("role", "Executive Position"))
    company = job.get("company", "Company")
    location = job.get("location", "")
    score = job.get("executive_score", job.get("score", 0))
    apply_link = job.get("apply_link", "")

    st.markdown(f"### {title}")
    st.write(f"**Company:** {company}")

    if location:
        st.write(f"**Location:** {location}")

    st.metric("Executive Fit", f"{score}%")

    if apply_link:
        st.link_button(
            "🚀 Apply Now",
            apply_link,
            use_container_width=True
        )

    st.divider()