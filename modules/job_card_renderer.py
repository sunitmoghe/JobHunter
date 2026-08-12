import streamlit as st


class JobCardRenderer:

    def render_job(
        self,
        job,
    ):

        title = job.get(
            "title",
            job.get(
                "role",
                "Executive Position"
            )
        )

        company = job.get(
            "company",
            "Company"
        )

        location = job.get(
            "location",
            ""
        )

        score = job.get(
            "executive_score",
            0
        )

        apply_url = job.get(
            "apply_link",
            ""
        )

        st.markdown(
            f"### {title}"
        )

        st.write(
            f"**Company:** {company}"
        )

        if location:

            st.write(
                f"**Location:** {location}"
            )

        st.metric(
            "Executive Fit",
            f"{score}%"
        )

        if apply_url:

            st.link_button(
                "🚀 Apply Now",
                apply_url,
                use_container_width=True,
            )

        else:

            st.warning(
                "Apply link not available."
            )

        st.divider()