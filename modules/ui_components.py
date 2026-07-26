import streamlit as st


def page_header(title: str, subtitle: str = ""):
    """Render a consistent page header."""
    st.title(title)

    if subtitle:
        st.write(subtitle)

    st.divider()


def section_header(title: str):
    """Render a section heading."""
    st.subheader(title)


def metric_row(metrics):
    """
    Display KPI metrics.

    metrics = [
        ("Applications", 24),
        ("Recruiters", 15),
        ("Offers", 2),
        ("Countries", 7),
    ]
    """

    cols = st.columns(len(metrics))

    for col, (label, value) in zip(cols, metrics):
        with col:
            st.metric(label, value)


def success_box(message: str):
    st.success(message)


def warning_box(message: str):
    st.warning(message)


def info_box(message: str):
    st.info(message)


def error_box(message: str):
    st.error(message)


def empty_state(message="No data available."):
    st.info(message)


def divider():
    st.divider()