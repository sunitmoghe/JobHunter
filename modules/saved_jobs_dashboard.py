import streamlit as st


def render_saved_jobs_dashboard(saved_jobs_manager):

    st.header("❤️ Saved Jobs Dashboard")

    saved_jobs = saved_jobs_manager.load_jobs()

    if saved_jobs:

        st.success(f"{len(saved_jobs)} Saved Executive Jobs")

        for idx, saved in enumerate(saved_jobs):

            with st.expander(
                f"{saved.get('role','Executive')} | {saved.get('company','Company')}"
            ):

                st.write(f"📍 Location : {saved.get('location','N/A')}")
                st.write(f"🌍 Country : {saved.get('country','N/A')}")
                st.write(f"📅 Saved : {saved.get('saved_date','')}")
                st.write(f"📌 Status : {saved.get('application_status','Saved')}")

                if st.button(
                    "🗑 Remove Job",
                    key=f"remove_saved_{idx}"
                ):

                    removed = saved_jobs_manager.remove_job(
                        saved.get("company", ""),
                        saved.get(
                            "role",
                            saved.get("title", "")
                        ),
                        saved.get("location", "")
                    )

                    if removed:

                        st.success("Job removed.")
                        st.rerun()

    else:

        st.info("No saved jobs available.")