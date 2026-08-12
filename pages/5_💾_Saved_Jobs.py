import streamlit as st

from modules.saved_jobs_manager import SavedJobsManager


st.set_page_config(
    page_title="Saved Jobs",
    page_icon="💾",
    layout="wide",
)


st.title("💾 Saved Jobs")

st.caption(
    "Your saved executive job opportunities."
)


manager = SavedJobsManager()

jobs = manager.load_jobs()


st.subheader(
    f"📊 Saved Jobs: {len(jobs)}"
)


if not jobs:

    st.info(
        "No saved jobs yet."
    )

else:

    for index, job in enumerate(
        jobs,
        start=1,
    ):

        title = job.get(
            "title",
            job.get(
                "role",
                "Executive Position",
            ),
        )

        company = job.get(
            "company",
            "Company",
        )

        location = job.get(
            "location",
            "",
        )

        score = job.get(
            "executive_score",
            0,
        )

        apply_link = job.get(
            "apply_link",
            "",
        )

        saved_on = job.get(
            "saved_on",
            "",
        )


        with st.container(
            border=True
        ):

            st.markdown(
                f"### {index}. {title}"
            )

            st.write(
                f"**Company:** {company}"
            )

            if location:

                st.write(
                    f"**Location:** {location}"
                )

            col1, col2, col3 = st.columns(
                3
            )


            with col1:

                st.metric(
                    "Executive Fit",
                    f"{score}%",
                )


            with col2:

                st.write(
                    "**Saved:**"
                )

                st.write(
                    saved_on
                )


            with col3:

                if apply_link:

                    st.link_button(
                        "🚀 Apply Now",
                        apply_link,
                        use_container_width=True,
                    )


            if st.button(
                "🗑️ Remove",
                key=f"remove_{index}",
            ):

                manager.remove_job(
                    job
                )

                st.rerun()