import streamlit as st

from modules.executive_ai_agent import ExecutiveAIAgent
from modules.priority_engine import PriorityEngine
from modules.executive_scoring_engine import ExecutiveScoringEngine
from modules.profile_manager import ProfileManager
from modules.job_skill_matcher import JobSkillMatcher
from modules.resume_tailor_engine import ResumeTailorEngine


st.set_page_config(
    page_title="AI Executive Jobs",
    page_icon="🔥",
    layout="wide"
)


st.title(
    "🔥 AI Executive Live Job Recommendations"
)

st.write(
    "Search global executive opportunities using the AI Executive Job Engine."
)


profile_manager = ProfileManager()

if profile_manager.profile_exists():

    profile = profile_manager.load_profile()

else:

    profile = {}

    st.warning(
        "⚠ No executive profile found. Please analyse your resume first."
    )


if st.button(
    "🚀 Search Global Executive Jobs"
):

    with st.spinner(
        "Searching executive opportunities..."
    ):

        agent = ExecutiveAIAgent()

        jobs = agent.search_all_roles()


    if jobs:

        st.success(
            f"Found {len(jobs)} executive opportunities."
        )


        priority_engine = PriorityEngine()

        scoring_engine = ExecutiveScoringEngine()

        skill_matcher = JobSkillMatcher()

        resume_tailor = ResumeTailorEngine()


        for job in jobs[:50]:

            role = job.get(
                "role",
                "Executive Role"
            )


            company = job.get(
                "company",
                "Not Available"
            )


            country = job.get(
                "country",
                "Not Available"
            )


            description = job.get(
                "description",
                ""
            )


            experience = profile.get(
                "experience",
                20
            )


            try:

                experience = int(
                    experience
                )

            except:

                experience = 20



            score = scoring_engine.calculate_score(

                {
                    "role": role,
                    "country": country
                },

                ats_score=80,

                experience_years=experience
            )



            priority = priority_engine.calculate_priority(

                {
                    "role": role,
                    "country": country
                },

                score["executive_fit"]
            )



            job_analysis = skill_matcher.extract_matching_skills(

                profile.get(
                    "skills",
                    []
                ),

                description
            )



            interview_probability = skill_matcher.interview_probability(

                score["executive_fit"]

            )



            resume_analysis = resume_tailor.analyze_job_fit(

                profile,

                job

            )



            tailored_summary = resume_tailor.generate_executive_summary(

                profile,

                job

            )



            st.subheader(
                role
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.write(
                    "🏢 Company:",
                    company
                )

                st.write(
                    "🌍 Country:",
                    country
                )


            with col2:

                st.metric(
                    "Executive Fit",
                    f"{score['executive_fit']}%"
                )

                st.metric(
                    "Priority Score",
                    f"{priority['priority_score']}%"
                )


            with col3:

                st.metric(
                    "Interview Probability",
                    f"{interview_probability}%"
                )



            st.success(
                priority["category"]
            )



            with st.expander(
                "🧠 AI Skill Analysis"
            ):

                st.write(
                    "### Matching Skills"
                )


                for skill in job_analysis.get(
                    "matched",
                    []
                ):

                    st.success(
                        skill
                    )


                st.write(
                    "### Missing Keywords"
                )


                for skill in job_analysis.get(
                    "missing",
                    []
                ):

                    st.warning(
                        skill
                    )



            with st.expander(
                "✨ AI Resume Tailoring"
            ):

                st.metric(
                    "Resume Match Score",
                    f"{resume_analysis['match_score']}%"
                )


                st.write(
                    "### Tailored Executive Summary"
                )


                st.info(
                    tailored_summary
                )



            with st.expander(
                "📊 Executive Score Breakdown"
            ):

                st.write(
                    f"ATS Score: {score['ats_score']}%"
                )

                st.write(
                    f"Leadership Score: {score['leadership_score']}%"
                )

                st.write(
                    f"Experience Score: {score['experience_score']}%"
                )



            with st.expander(
                "📄 View Job Details"
            ):

                st.json(
                    job
                )


            st.divider()


    else:

        st.warning(
            "No executive jobs found."
        )