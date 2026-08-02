import streamlit as st
import pandas as pd

from modules.saved_jobs_manager import SavedJobsManager


st.set_page_config(
    page_title="Saved Jobs",
    page_icon="💾",
    layout="wide"
)

st.title("💾 Saved Executive Jobs")

manager = SavedJobsManager()

jobs = manager.load_jobs()

if not jobs:

    st.info(
        "No saved jobs yet."
    )

    st.stop()


df = pd.DataFrame(jobs)


st.sidebar.header("Filters")


company_filter = st.sidebar.selectbox(

    "Company",

    ["All"] + sorted(df["company"].fillna("").unique().tolist())

)


country_filter = st.sidebar.selectbox(

    "Country",

    ["All"] + sorted(df["country"].fillna("").unique().tolist())

)


search = st.sidebar.text_input(
    "Search Role"
)


filtered = df.copy()


if company_filter != "All":

    filtered = filtered[
        filtered["company"] == company_filter
    ]


if country_filter != "All":

    filtered = filtered[
        filtered["country"] == country_filter
    ]


if search:

    filtered = filtered[
        filtered["role"].str.contains(
            search,
            case=False,
            na=False
        )
    ]


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Saved Jobs",
        len(filtered)
    )


with col2:

    st.metric(
        "Companies",
        filtered["company"].nunique()
    )


with col3:

    st.metric(
        "Countries",
        filtered["country"].nunique()
    )


st.divider()


for _, job in filtered.iterrows():

    with st.container():

        st.subheader(job.get("role", ""))

        st.caption(
            f"{job.get('company','')} • {job.get('location','')}"
        )

        st.write(
            f"**Country:** {job.get('country','')}"
        )

        st.write(
            f"**Salary:** {job.get('salary','Not Available')}"
        )

        st.write(
            f"**Saved On:** {job.get('saved_date','')}"
        )

        if job.get("link"):

            st.link_button(
                "Open Job",
                job["link"]
            )

        if st.button(

            "🗑 Remove",

            key=f"{job.get('company')}_{job.get('role')}"

        ):

            manager.remove_job(

                job.get("company", ""),

                job.get("role", ""),

                job.get("location", "")

            )

            st.success(
                "Job removed."
            )

            st.rerun()

        st.divider()


st.download_button(

    "⬇ Export Saved Jobs",

    filtered.to_csv(index=False),

    "saved_jobs.csv",

    "text/csv"

)