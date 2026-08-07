import streamlit as st

from modules.opportunity_score_engine import OpportunityScoreEngine


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

        self.opportunity_engine = OpportunityScoreEngine()

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
                "Executive Role",
            ),
        )

        company = job.get(
            "company",
            "Unknown Company",
        )

        location = job.get(
            "location",
            job.get(
                "country",
                "Unknown",
            ),
        )

        executive_score = job.get(
            "executive_score",
            0,
        )

        jobhunter_score = job.get(
            "jobhunter_score",
            executive_score,
        )

        st.subheader(role)

        st.caption(
            f"{company} • {location}"
        )

        score1, score2, score3, score4 = st.columns(4)

        opportunity = self.opportunity_engine.calculate(job)

        st.success(
            f"🏆 Executive Opportunity Score : {opportunity['score']}/100"
        )

        st.info(
            opportunity["rating"]
        )

        st.divider()

        with score1:

            st.metric(
                "🏆 JobHunter Score",
                jobhunter_score,
            )

        with score2:

            st.metric(
                "⭐ Executive Score",
                executive_score,
            )

        with score3:

            st.metric(
                "💰 Salary",
                "Yes" if job.get("salary") else "-",
            )

        with score4:

            st.metric(
                "🌍 Visa",
                "Yes" if job.get("visa_sponsorship") else "No",
            )

        st.divider()

        company_col1, company_col2 = st.columns(2)

        with company_col1:

            st.write(
                f"⭐ Company Rating : {job.get('company_rating', 'N/A')}/5"
            )

            st.write(
                f"📈 Hiring Trend : {job.get('hiring_trend', 'Unknown')}"
            )

            if job.get("fortune500"):
                st.success("🏢 Fortune 500 Company")

            if job.get("verified_company"):
                st.success("✅ Verified Employer")

        with company_col2:
            with st.expander(
                "🌐 Executive Company Intelligence",
                expanded=False,
            ):

                st.write(f"🏭 Industry : {job.get('industry','Unknown')}")
                st.write(f"👥 Employees : {job.get('employee_count','Unknown')}")
                st.write(f"🌍 Headquarters : {job.get('headquarters','Unknown')}")
                st.write(f"💰 Revenue : {job.get('estimated_revenue','Unknown')}")
                st.write(f"📈 Growth Score : {job.get('growth_score',0)}/100")
                st.write(f"🚨 Layoff Risk : {job.get('layoff_risk','Unknown')}")

            with st.expander(
                "💰 Salary Intelligence",
                expanded=False,
            ):

                salary = self.salary_engine.get_salary_benchmark(
                    job.get("country", "Unknown"),
                    role,
                )

                if isinstance(salary, dict) and "average" in salary:

                    st.write(
                        f"Average : {salary['currency']} {salary['average']:,}"
                    )

                    st.write(
                        f"Range : {salary['currency']} {salary['low']:,} - {salary['high']:,}"
                    )

                else:

                    st.info("Salary benchmark unavailable.")

            with st.expander(
                "👥 Recruiter Intelligence",
                expanded=False,
            ):

                recruiter = self.recruiter_engine.find_recruiter(job)

                if recruiter:
                    st.write(recruiter)
                else:
                    st.info("Recruiter information unavailable.")

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
                        st.success("Matched Skills")
                        st.write(", ".join(matched))

                    if missing:
                        st.warning("Missing Skills")
                        st.write(", ".join(missing))

                except Exception as e:
                    st.warning(str(e))

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
                            score.get("score", 0),
                        )

                        reason = score.get("reason")

                        if reason:
                            st.write(reason)

                    else:

                        st.metric(
                            "Executive Score",
                            score,
                        )

                except Exception as e:

                    st.warning(str(e))

            st.divider()

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

                        st.success("Resume successfully tailored.")

                        st.text_area(
                            "Tailored Resume Preview",
                            tailored_resume,
                            height=220,
                        )

                    else:

                        st.info("Resume tailoring unavailable.")

                except Exception as e:

                    st.warning(str(e))

            with st.expander(
                "🤖 AI Application Assistant",
                expanded=False,
            ):

                try:

                    assistant = self.application_assistant.generate(
                        profile,
                        job,
                    )

                    if isinstance(assistant, dict):

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

        st.subheader("🚀 Executive Actions")

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "💾 Save Job",
                key=f"save_{index}",
            ):

                try:

                    self.saved_jobs_manager.save_job(job)

                    st.success("✅ Job Saved")

                except Exception as e:

                    st.error(str(e))

        with col2:

            if st.button(
                "🚀 One Click Apply",
                key=f"apply_{index}",
            ):

                try:

                    self.saved_jobs_manager.save_job(job)

                    self.application_tracker.mark_applied(job)

                    resume = self.resume_tailor.tailor_resume(
                        profile,
                        job,
                    )

                    package = self.application_assistant.generate_apply_package(
                        profile,
                        job,
                    )

                    st.session_state[f"resume_{index}"] = resume

                    st.session_state[f"package_{index}"] = package or {}

                    st.success("✅ Job Saved")
                    st.success("✅ Application Recorded")
                    st.success("✅ ATS Resume Generated")

                except Exception as e:

                    st.error(str(e))

        if f"resume_{index}" in st.session_state:

            st.download_button(
                "📄 Download ATS Resume",
                st.session_state[f"resume_{index}"],
                file_name=f"{role}_ATS_Resume.txt",
                mime="text/plain",
                key=f"resume_download_{index}",
            )

        package = st.session_state.get(
            f"package_{index}",
            {},
        )

        downloads = [

            (
                "📄 Download Cover Letter",
                "cover_letter",
                "Cover_Letter",
            ),

            (
                "💼 Download LinkedIn Message",
                "linkedin_message",
                "LinkedIn_Message",
            ),

            (
                "📧 Download Recruiter Email",
                "recruiter_email",
                "Recruiter_Email",
            ),

            (
                "📨 Download HR Email",
                "hr_email",
                "HR_Email",
            ),

            (
                "👔 Download Hiring Manager Email",
                "hiring_manager_email",
                "Hiring_Manager_Email",
            ),

            (
                "🎤 Download Executive Pitch",
                "executive_pitch",
                "Executive_Pitch",
            ),

        ]

        for label, field, filename in downloads:

            value = package.get(field)

            if value:

                st.download_button(

                    label,

                    value,

                    file_name=f"{role}_{filename}.txt",

                    mime="text/plain",

                    key=f"{field}_{index}",

                )

        apply_link = job.get("apply_link") or job.get("url")

        if apply_link:

            st.link_button(

                "🌍 Apply on Company Website",

                apply_link,

            )

        else:

            st.info("Company website unavailable.")

        with st.expander(

            "📋 Executive Summary",

            expanded=False,

        ):

            st.write("**Role:**", role)
            st.write("**Company:**", company)
            st.write("**Location:**", location)
            st.write("**Executive Score:**", executive_score)
            st.write("**JobHunter Score:**", jobhunter_score)
            st.write(
                "**Visa Sponsorship:**",
                "Yes" if job.get("visa_sponsorship") else "No",
            )

        st.markdown("---")