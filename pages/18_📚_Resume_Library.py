import streamlit as st

from modules.resume_library_engine import ResumeLibraryEngine


st.set_page_config(
    page_title="Resume Library",
    page_icon="📚",
    layout="wide",
)


st.title("📚 Resume Library")

st.caption(
    "Store multiple executive resumes and manage them independently."
)


engine = ResumeLibraryEngine()


# ==========================================================
# UPLOAD NEW RESUME
# ==========================================================

st.subheader("➕ Add Resume")

uploaded_file = st.file_uploader(
    "Upload resume",
    type=["pdf", "docx", "doc"],
)

col1, col2, col3 = st.columns(3)

with col1:

    resume_name = st.text_input(
        "Resume Name",
        placeholder="e.g. Sales & BD — APAC",
    )

with col2:

    target_roles = st.text_input(
        "Target Roles",
        placeholder="Head of Sales, Sales Director, VP Sales",
    )

with col3:

    target_countries = st.text_input(
        "Target Countries",
        placeholder="Singapore, Australia, Malaysia",
    )

industries = st.text_input(
    "Target Industries",
    placeholder="SaaS, Telecom, Technology, Renewable Energy",
)


if st.button(
    "💾 Save Resume",
    type="primary",
    use_container_width=True,
):

    if uploaded_file is None:

        st.error(
            "Please upload a resume first."
        )

    else:

        try:

            record = engine.add_resume(
                file_bytes=uploaded_file.getvalue(),
                original_filename=uploaded_file.name,
                resume_name=resume_name.strip()
                if resume_name.strip()
                else None,
                target_roles=target_roles,
                target_countries=target_countries,
                industries=industries,
            )

            st.success(
                f"Resume '{record['resume_name']}' saved successfully."
            )

            st.rerun()

        except Exception as error:

            st.error(
                "Unable to save resume."
            )

            st.exception(
                error
            )


st.divider()


# ==========================================================
# RESUME LIBRARY
# ==========================================================

st.subheader("📁 Your Resume Library")

resumes = engine.get_all_resumes()


if not resumes:

    st.info(
        "No resumes saved yet. Upload your first executive resume above."
    )

else:

    active_count = sum(
        1
        for resume in resumes
        if resume.get(
            "status",
            "Active",
        ) == "Active"
    )

    archived_count = sum(
        1
        for resume in resumes
        if resume.get(
            "status",
            "Active",
        ) == "Archived"
    )

    metric1, metric2, metric3 = st.columns(3)

    with metric1:

        st.metric(
            "Total Resumes",
            len(resumes),
        )

    with metric2:

        st.metric(
            "Active",
            active_count,
        )

    with metric3:

        st.metric(
            "Archived",
            archived_count,
        )

    st.divider()


    for index, resume in enumerate(
        resumes,
        start=1,
    ):

        resume_id = resume.get(
            "resume_id",
            "",
        )

        name = resume.get(
            "resume_name",
            "Resume",
        )

        original_filename = resume.get(
            "original_filename",
            "",
        )

        file_format = resume.get(
            "format",
            "",
        )

        status = resume.get(
            "status",
            "Active",
        )

        roles = resume.get(
            "target_roles",
            [],
        )

        countries = resume.get(
            "target_countries",
            [],
        )

        resume_industries = resume.get(
            "industries",
            [],
        )

        ats_score = resume.get(
            "ats_baseline_score",
            None,
        )

        created_at = resume.get(
            "created_at",
            "",
        )

        updated_at = resume.get(
            "updated_at",
            "",
        )


        if status == "Active":

            status_label = "🟢 ACTIVE"

        else:

            status_label = "⚪ ARCHIVED"


        with st.container(
            border=True
        ):

            title_col, status_col = st.columns(
                [5, 2]
            )

            with title_col:

                st.markdown(
                    f"### {index}. {name}"
                )

                st.caption(
                    original_filename
                )

            with status_col:

                st.markdown(
                    f"**{status_label}**"
                )


            info1, info2, info3, info4 = st.columns(4)

            with info1:

                st.write(
                    f"**Format:** {file_format}"
                )

            with info2:

                st.write(
                    f"**Created:** {created_at}"
                )

            with info3:

                st.write(
                    f"**Updated:** {updated_at}"
                )

            with info4:

                if ats_score is None:

                    st.write(
                        "**ATS Baseline:** Not calculated"
                    )

                else:

                    st.write(
                        f"**ATS Baseline:** {ats_score}%"
                    )


            if roles:

                st.write(
                    "**Target Roles:** "
                    + ", ".join(
                        roles
                    )
                )


            if countries:

                st.write(
                    "**Target Countries:** "
                    + ", ".join(
                        countries
                    )
                )


            if resume_industries:

                st.write(
                    "**Industries:** "
                    + ", ".join(
                        resume_industries
                    )
                )


            st.divider()


            action1, action2, action3 = st.columns(3)


            # --------------------------------------------------
            # RENAME / UPDATE
            # --------------------------------------------------

            with action1:

                with st.expander(
                    "✏️ Edit Metadata"
                ):

                    new_name = st.text_input(
                        "Resume Name",
                        value=name,
                        key=f"name_{resume_id}",
                    )

                    new_roles = st.text_input(
                        "Target Roles",
                        value=", ".join(
                            roles
                        ),
                        key=f"roles_{resume_id}",
                    )

                    new_countries = st.text_input(
                        "Target Countries",
                        value=", ".join(
                            countries
                        ),
                        key=f"countries_{resume_id}",
                    )

                    new_industries = st.text_input(
                        "Industries",
                        value=", ".join(
                            resume_industries
                        ),
                        key=f"industries_{resume_id}",
                    )


                    if st.button(
                        "💾 Update",
                        key=f"update_{resume_id}",
                        use_container_width=True,
                    ):

                        success = engine.update_resume(
                            resume_id,
                            {
                                "resume_name":
                                    new_name,

                                "target_roles":
                                    new_roles,

                                "target_countries":
                                    new_countries,

                                "industries":
                                    new_industries,
                            },
                        )

                        if success:

                            st.success(
                                "Resume updated."
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Unable to update resume."
                            )


            # --------------------------------------------------
            # ARCHIVE / ACTIVATE
            # --------------------------------------------------

            with action2:

                if status == "Active":

                    if st.button(
                        "📦 Archive",
                        key=f"archive_{resume_id}",
                        use_container_width=True,
                    ):

                        success = (
                            engine.archive_resume(
                                resume_id
                            )
                        )

                        if success:

                            st.success(
                                "Resume archived."
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Unable to archive resume."
                            )

                else:

                    if st.button(
                        "♻️ Activate",
                        key=f"activate_{resume_id}",
                        use_container_width=True,
                    ):

                        success = (
                            engine.activate_resume(
                                resume_id
                            )
                        )

                        if success:

                            st.success(
                                "Resume activated."
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Unable to activate resume."
                            )


            # --------------------------------------------------
            # DELETE
            # --------------------------------------------------

            with action3:

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{resume_id}",
                    use_container_width=True,
                ):

                    success = engine.delete_resume(
                        resume_id
                    )

                    if success:

                        st.success(
                            "Resume deleted."
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Unable to delete resume."
                        )