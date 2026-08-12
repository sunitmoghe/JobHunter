import streamlit as st


class ExecutivePerformanceEngine:

    def calculate(self, profile, jobs):

        st.write("DEBUG PROFILE:", profile)
        st.write("DEBUG EXPERIENCE:", profile.get("experience"))
        st.write("DEBUG TYPE:", type(profile.get("experience")))

        st.stop()

        return {}