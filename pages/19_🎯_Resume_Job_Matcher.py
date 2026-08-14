import streamlit as st

from modules.multi_resume_matcher import MultiResumeMatcher


st.set_page_config(
    page_title="Resume Job Matcher",
    page_icon="🎯",
    layout="wide",
)


st.title("🎯 Resume → Job Matcher")

st.caption(
    "Compare all active resumes against a job description and identify the strongest resume for the opportunity."
)


matcher = MultiResumeMatcher()


# ==========================================================
# JOB INPUT
# ==========================================================

st.subheader("📄 Job Description")

job_title = st.text_input(
    "Job Title",
    value="Head of Sales",
)

company = st.text_input(
    "Company",
    value="",
)

job_description = st.text_area(
    "Paste Job Description",
    height=320,
    placeholder=(
        "Paste the complete job description here..."
    ),
)


# ==========================================================
# ANALYZE
# ==========================================================

if st.button(
    "🎯 Compare All Resumes",
    type="primary",
    use_container_width=True,
):

    if not job_description.strip():

        st.error(
            "Please paste a job description."
        )

    else:

        with st.spinner(
            "Comparing all active resumes..."
        ):

            results = matcher.match_all(
                job_description
            )

            best = matcher.best_resume(
                job_description
            )

            st.session_state[
                "resume_match_results"
            ] = results

            st.session_state[
                "resume_match_best"
            ] = best

            st.session_state[
                "resume_match_job_title"
            ] = job_title

            st.session_state[
                "resume_match_company"
            ] = company


# ==========================================================
# RESULTS
# ==========================================================

results = st.session_state.get(
    "resume_match_results",
    [],
)

best = st.session_state.get(
    "resume_match_best",
    None,
)


if results:

    st.divider()

    # ------------------------------------------------------
    # BEST RESUME
    # ------------------------------------------------------

    st.subheader(
        "🏆 Best Resume for This Job"
    )

    if best:

        best_score = float(
            best.get(
                "score",
                0,
            )
            or 0
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Best Resume",
                best.get(
                    "resume_name",
                    "Resume",
                ),
            )

        with col2:

            st.metric(
                "ATS Match",
                f"{best_score:.2f}%",
            )

        with col3:

            st.metric(
                "Matched Skills",
                best.get(
                    "matched_count",
                    0,
                ),
            )

        with col4:

            st.metric(
                "Missing Skills",
                best.get(
                    "missing_count",
                    0,
                ),
            )

        if best_score >= 90:

            st.success(
                "✅ Excellent ATS compatibility."
            )

        elif best_score >= 75:

            st.warning(
                "🟠 Strong match. Tailoring can improve the score."
            )

        else:

            st.error(
                "🔴 Resume should be tailored before applying."
            )

    else:

        st.warning(
            "No usable active resume was found."
        )


    st.divider()


    # ------------------------------------------------------
    # ALL RESUME COMPARISON
    # ------------------------------------------------------

    st.subheader(
        "📊 Resume Comparison"
    )

    comparison = []

    for index, result in enumerate(
        results,
        start=1,
    ):

        comparison.append(
            {
                "Rank":
                    index,

                "Resume":
                    result.get(
                        "resume_name",
                        "Resume",
                    ),

                "ATS Match":
                    round(
                        float(
                            result.get(
                                "score",
                                0,
                            )
                            or 0
                        ),
                        2,
                    ),

                "Matched":
                    result.get(
                        "matched_count",
                        0,
                    ),

                "Missing":
                    result.get(
                        "missing_count",
                        0,
                    ),

                "Interview Probability":
                    result.get(
                        "interview_probability",
                        0,
                    ),

                "Status":
                    (
                        "BEST"
                        if best
                        and result.get(
                            "resume_id"
                        )
                        == best.get(
                            "resume_id"
                        )
                        else ""
                    ),
            }
        )

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True,
    )


    # ------------------------------------------------------
    # INDIVIDUAL DETAILS
    # ------------------------------------------------------

    st.subheader(
        "🔍 Resume Analysis Details"
    )

    for index, result in enumerate(
        results,
        start=1,
    ):

        resume_name = result.get(
            "resume_name",
            "Resume",
        )

        score = float(
            result.get(
                "score",
                0,
            )
            or 0
        )

        status = (
            "🏆 BEST MATCH"
            if best
            and result.get(
                "resume_id"
            )
            == best.get(
                "resume_id"
            )
            else ""
        )

        with st.expander(
            f"{index}. {resume_name} — ATS {score:.2f}% {status}"
        ):

            if result.get(
                "error"
            ):

                st.error(
                    result["error"]
                )

                continue


            col1, col2 = st.columns(2)


            with col1:

                st.write(
                    f"**ATS Score:** {score:.2f}%"
                )

                st.write(
                    f"**Matched Skills:** "
                    f"{result.get('matched_count', 0)}"
                )

                st.write(
                    f"**Missing Skills:** "
                    f"{result.get('missing_count', 0)}"
                )

                st.write(
                    f"**Interview Probability:** "
                    f"{result.get('interview_probability', 0)}%"
                )


            with col2:

                roles = result.get(
                    "target_roles",
                    [],
                )

                countries = result.get(
                    "target_countries",
                    [],
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


            matched = result.get(
                "matched",
                [],
            )

            if matched:

                with st.expander(
                    "✅ Matched Skills"
                ):

                    for item in matched:

                        st.write(
                            f"• {item.get('skill', '')}"
                        )


            missing = result.get(
                "missing",
                [],
            )

            if missing:

                with st.expander(
                    "⚠️ Missing Skills"
                ):

                    for item in missing:

                        st.write(
                            f"• {item.get('skill', '')}"
                        )


            dynamic_missing = result.get(
                "dynamic_missing_keywords",
                [],
            )

            if dynamic_missing:

                with st.expander(
                    "🔑 Missing JD Keywords"
                ):

                    st.write(
                        ", ".join(
                            dynamic_missing
                        )
                    )


            recommendations = result.get(
                "recommendations",
                [],
            )

            if recommendations:

                with st.expander(
                    "💡 ATS Recommendations"
                ):

                    for recommendation in recommendations:

                        st.write(
                            f"• {recommendation}"
                        )


    st.divider()


    # ------------------------------------------------------
    # APPLICATION READINESS
    # ------------------------------------------------------

    st.subheader(
        "🚀 Application Readiness"
    )

    if best:

        score = float(
            best.get(
                "score",
                0,
            )
            or 0
        )

        best_name = best.get(
            "resume_name",
            "Resume",
        )

        job_label = (
            job_title.strip()
            if job_title.strip()
            else "this opportunity"
        )

        company_label = (
            company.strip()
            if company.strip()
            else "the company"
        )

        if score >= 90:

            st.success(
                f"✅ {best_name} is ready for "
                f"{job_label} at {company_label}."
            )

        elif score >= 75:

            st.warning(
                f"🟠 {best_name} is the strongest available resume, "
                "but tailoring is recommended before applying."
            )

        else:

            st.error(
                f"🔴 No active resume currently reaches a strong ATS "
                f"match for {job_label}. Tailoring is recommended."
            )

else:

    st.info(
        "Paste a job description and click 'Compare All Resumes'."
    )