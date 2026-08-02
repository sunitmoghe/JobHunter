import streamlit as st


class JobCardRenderer:

    def __init__(
        self,
        scoring_engine,
        priority_engine,
        skill_matcher,
        salary_engine,
        recruiter_engine,
        company_engine,
        resume_tailor,
        application_assistant,
        application_tracker,
        saved_jobs_manager,
    ):

        self.scoring_engine = scoring_engine
        self.priority_engine = priority_engine
        self.skill_matcher = skill_matcher
        self.salary_engine = salary_engine
        self.recruiter_engine = recruiter_engine
        self.company_engine = company_engine
        self.resume_tailor = resume_tailor
        self.application_assistant = application_assistant
        self.application_tracker = application_tracker
        self.saved_jobs_manager = saved_jobs_manager

    def render(
        self,
        job,
        index,
        profile,
    ):

        role = job.get(
            "role",
            job.get(
                "title",
                "Executive Role"
            )
        )

        company = job.get(
            "company",
            "Unknown Company"
        )

        location = job.get(
            "location",
            job.get(
                "country",
                "Unknown"
            )
        )

        st.subheader(role)

        st.caption(
            f"{company} • {location}"
        )

        st.divider()

        company_col1, company_col2 = st.columns(2)

        with company_col1:

            st.write(
                f"⭐ Company Rating : {job.get('company_rating', 3)}/5"
            )

            if job.get("fortune500"):

                st.success(
                    "🏢 Fortune 500 Company"
                )

            else:

                st.info(
                    "🏢 Standard Company"
                )

            if job.get("verified_company"):

                st.success(
                    "✅ Verified Employer"
                )

        with company_col2:

            if job.get("visa_sponsorship"):

                st.success(
                    "🌍 Visa Sponsorship"
                )

            else:

                st.warning(
                    "No Visa Sponsorship"
                )

            if job.get("remote_friendly"):

                st.success(
                    "🏠 Remote Friendly"
                )

            st.write(
                f"📈 Hiring Trend : {job.get('hiring_trend', 'Unknown')}"
            )

        with st.expander(
            "🌐 Live Company Intelligence",
            expanded=False
        ):

            st.write(
                "🌍 Website"
            )

            st.code(
                job.get(
                    "company_website",
                    "Not Available"
                )
            )

            st.write(
                "💼 Careers"
            )

            st.code(
                job.get(
                    "careers_page",
                    "Not Available"
                )
            )

            st.write(
                "📞 Contact"
            )

            st.code(
                job.get(
                    "contact_page",
                    "Not Available"
                )
            )

            st.write(
                "👥 LinkedIn"
            )

            st.code(
                job.get(
                    "linkedin_company",
                    "Not Available"
                )
            )

        st.divider()

            # ------------------------------------------
        # Salary Intelligence
        # ------------------------------------------

        with st.expander(
            "💰 Salary Intelligence",
            expanded=False,
        ):

            country = job.get(
                "country",
                "Unknown"
            )

            role = job.get(
                "role",
                job.get(
                    "title",
                    "Executive Role"
                )
            )

            salary = self.salary_engine.get_salary_benchmark(
                country,
                role
            )

            if "average" in salary:

                st.write(
                    f"💵 Salary Range : {salary['currency']} {salary['low']:,} - {salary['high']:,}"
                )

                st.write(
                    f"📊 Market Average : {salary['currency']} {salary['average']:,}"
                )

            else:

                st.info(
                    salary.get(
                        "message",
                        "Salary benchmark unavailable."
                    )
                )
        # ------------------------------------------
        # Recruiter Intelligence
        # ------------------------------------------

        with st.expander(
            "👥 Recruiter Intelligence",
            expanded=False,
        ):

            recruiter = self.recruiter_engine.find_recruiter(
                job
            )

            if recruiter:

                st.write(
                    "**Recruiter:**",
                    recruiter.get(
                        "name",
                        "Not Available",
                    ),
                )

                st.write(
                    "**Title:**",
                    recruiter.get(
                        "title",
                        "Not Available",
                    ),
                )

                st.write(
                    "**Recruiter Email:**",
                    recruiter.get(
                        "email",
                        "Not Available",
                    ),
                )

                st.write(
                    "**HR Email:**",
                    recruiter.get(
                        "hr_email",
                        "Not Available",
                    ),
                )

                st.write(
                    "**Confidence:**",
                    recruiter.get(
                        "confidence",
                        "Low",
                    ),
                )

            else:

                st.info(
                    "Recruiter information not available."
                )

        # ------------------------------------------
        # AI Skill Analysis
        # ------------------------------------------

        with st.expander(
            "🎯 AI Skill Analysis",
            expanded=False,
        ):

            try:

                skill_result = self.skill_matcher.match(
                    profile,
                    job,
                )

                st.metric(
                    "ATS Match",
                    f"{skill_result.get('score',0)}%",
                )

                matched = skill_result.get(
                    "matched_skills",
                    [],
                )

                missing = skill_result.get(
                    "missing_skills",
                    [],
                )

                if matched:

                    st.success(
                        "Matched Skills"
                    )

                    st.write(
                        ", ".join(matched)
                    )

                if missing:

                    st.warning(
                        "Missing Skills"
                    )

                    st.write(
                        ", ".join(missing)
                    )

            except Exception as e:

                st.warning(str(e))

        # ------------------------------------------
        # Executive Score
        # ------------------------------------------

        with st.expander(
            "📊 Executive Score Breakdown",
            expanded=False,
        ):

            try:

                score = self.scoring_engine.score_job(
                    job,
                    profile,
                )

                if isinstance(score, dict):

                    st.metric(
                        "Executive Score",
                        score.get(
                            "score",
                            0,
                        ),
                    )

                    if score.get(
                        "reason",
                    ):

                        st.write(
                            score["reason"]
                        )

                else:

                    st.metric(
                        "Executive Score",
                        score,
                    )

            except Exception as e:

                st.warning(str(e))

        st.divider()

        # ------------------------------------------
        # AI Resume Tailoring
        # ------------------------------------------

        with st.expander(
            "📄 AI Resume Tailoring",
            expanded=False,
        ):

            try:

                tailored_resume = self.resume_tailor.tailor_resume(
                    profile,
                    job,
                )

                if tailored_resume:

                    st.success(
                        "Resume successfully tailored."
                    )

                    st.text_area(
                        "Tailored Resume Preview",
                        tailored_resume,
                        height=250,
                    )

                else:

                    st.info(
                        "Resume tailoring not available."
                    )

            except Exception as e:

                st.warning(str(e))

        # ------------------------------------------
        # AI Application Assistant
        # ------------------------------------------

        with st.expander(
            "🤖 AI Application Assistant",
            expanded=False,
        ):

            try:

                assistant = self.application_assistant.generate(
                    profile,
                    job,
                )

                if isinstance(
                    assistant,
                    dict,
                ):

                    if assistant.get("linkedin_message"):

                        st.text_area(
                            "LinkedIn Message",
                            assistant["linkedin_message"],
                            height=120,
                        )

                    if assistant.get("cover_letter"):

                        st.text_area(
                            "Cover Letter",
                            assistant["cover_letter"],
                            height=250,
                        )

                else:

                    st.write(assistant)

            except Exception as e:

                st.warning(str(e))

        st.divider()

        # ------------------------------------------
        # Job Actions
        # ------------------------------------------

        action_col1, action_col2 = st.columns(2)

        with action_col1:

            if st.button(
                "💾 Save Job",
                key=f"save_{index}",
            ):

                try:

                    self.saved_jobs_manager.save_job(job)

                    st.success(
                        "Job saved successfully."
                    )

                except Exception as e:

                    st.warning(str(e))

        with action_col2:

            if st.button(
                "📌 Mark Applied",
                key=f"apply_{index}",
            ):

                try:

                    self.application_tracker.mark_applied(
                        job
                    )

                    st.success(
                        "Application recorded."
                    )

                except Exception as e:

                    st.warning(str(e))

        st.divider()

        # ------------------------------------------
        # Interview Questions
        # ------------------------------------------

        with st.expander(
            "🎤 AI Interview Questions",
            expanded=False,
        ):

            try:

                questions = job.get(
                    "interview_questions",
                    [],
                )

                if questions:

                    for question in questions:

                        st.write(
                            "•",
                            question,
                        )

                else:

                    st.info(
                        "No interview questions available."
                    )

            except Exception as e:

                st.warning(str(e))

        # ------------------------------------------
        # Executive Summary
        # ------------------------------------------

        with st.expander(
            "📋 Executive Summary",
            expanded=False,
        ):

            st.write(
                "**Role:**",
                role,
            )

            st.write(
                "**Company:**",
                company,
            )

            st.write(
                "**Location:**",
                location,
            )

            st.write(
                "**Priority Score:**",
                job.get(
                    "priority_score",
                    "Not Available",
                ),
            )

            st.write(
                "**Executive Score:**",
                job.get(
                    "executive_score",
                    "Not Available",
                ),
            )

            st.write(
                "**Visa Sponsorship:**",
                "Yes"
                if job.get("visa_sponsorship")
                else "No",
            )

        st.divider()

        st.markdown(
            "---"
        )