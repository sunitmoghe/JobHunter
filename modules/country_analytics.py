import streamlit as st


def render_country_analytics(jobs):

    if not jobs:
        return

    st.subheader("🌍 Jobs by Country")

    country_summary = {}

    for job in jobs:

        country = job.get(
            "country",
            "Unknown"
        )

        country_summary[country] = (
            country_summary.get(country, 0) + 1
        )

    for country, count in sorted(
        country_summary.items(),
        key=lambda x: x[1],
        reverse=True
    ):

        st.write(
            f"**{country}** : {count} jobs"
        )