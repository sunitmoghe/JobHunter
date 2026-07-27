import streamlit as st

from modules.executive_ai_agent import ExecutiveAIAgent
from modules.priority_engine import PriorityEngine
from modules.executive_scoring_engine import ExecutiveScoringEngine
from modules.profile_manager import ProfileManager
from modules.job_skill_matcher import JobSkillMatcher
from modules.resume_tailor_engine import ResumeTailorEngine
from modules.application_assistant import ApplicationAssistant
from modules.application_tracker import ApplicationTracker


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Executive Jobs",
    page_icon="🔥",
    layout="wide"
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title(
    "🔥 AI Executive Live Job Recommendations"
)

st.write(
    "Search global executive opportunities using the AI Executive Job Engine."
)

st.divider()

# ==========================================================
# AI EXECUTIVE DASHBOARD
# ==========================================================

st.subheader("🧠 AI Executive Recommendations")

col1, col2 = st.columns(2)

with col1:

    preferred_country = st.selectbox(
        "Preferred Country",
        [
            "All",
            "Singapore",
            "UAE",
            "Saudi Arabia",
            "Qatar",
            "Oman",
            "Kuwait",
            "Bahrain",
            "Malaysia",
            "Thailand",
            "Vietnam",
            "Indonesia",
            "Germany",
            "Netherlands",
            "Poland",
            "United Kingdom",
            "Canada",
            "Australia"
        ]
    )

with col2:

    preferred_role = st.selectbox(
        "Preferred Role",
        [
            "All",
            "Chief Operating Officer",
            "CEO",
            "Country Manager",
            "Managing Director",
            "Regional Director",
            "Vice President Sales",
            "Head of Sales",
            "Sales Director",
            "Business Development Director",
            "Customer Success Director",
            "Operations Director",
            "General Manager"
        ]
    )

st.info(
f"""
### 📈 AI Insights

✅ Strongest Market : **Singapore**

✅ Best Match : **Head of Sales (92%)**

✅ Customer Success Leadership : **89%**

🚀 High Priority Jobs Today : **27**

💼 Executive Experience : **23+ Years**

🌍 Countries Monitored : **18**

"""
)

st.divider()

# --------------------------------------------------
# SESSION STATE INITIALISATION
# --------------------------------------------------

if "executive_jobs" not in st.session_state:

    st.session_state.executive_jobs = []


if "search_completed" not in st.session_state:

    st.session_state.search_completed = False



# --------------------------------------------------
# LOAD PROFILE
# --------------------------------------------------

profile_manager = ProfileManager()


if profile_manager.profile_exists():

    profile = profile_manager.load_profile()

else:

    profile = {}

    st.warning(
        "⚠ No executive profile found. Please analyse your resume first."
    )


# --------------------------------------------------
# INITIALISE ENGINES
# --------------------------------------------------

priority_engine = PriorityEngine()

scoring_engine = ExecutiveScoringEngine()

skill_matcher = JobSkillMatcher()

resume_tailor = ResumeTailorEngine()

application_assistant = ApplicationAssistant()

application_tracker = ApplicationTracker()

# --------------------------------------------------
# JOB SEARCH ENGINE
# --------------------------------------------------

st.subheader(
    "🌍 Global Executive Job Search"
)


if st.button(
    "🚀 Search Global Executive Jobs",
    type="primary"
):

    with st.spinner(
        "Searching executive opportunities..."
    ):

        try:

            agent = ExecutiveAIAgent()

            st.session_state.executive_jobs = (
                agent.search_all_roles()
            )

            st.session_state.search_completed = True


        except Exception as e:

            st.error(
                f"Job search failed: {e}"
            )


# --------------------------------------------------
# SEARCH RESULTS SUMMARY
# --------------------------------------------------

if st.session_state.search_completed:

    jobs = st.session_state.executive_jobs


    if jobs:

        st.success(
            f"Found {len(jobs)} executive opportunities."
        )


    else:

        st.warning(
            "No executive jobs found."
        )


else:

    jobs = []


# --------------------------------------------------
# JOB COUNT FILTER
# --------------------------------------------------

if jobs:

    col1, col2 = st.columns(2)


    with col1:

        display_limit = st.selectbox(

            "Number of jobs to display",

            [
                10,
                25,
                50
            ],

            index=2

        )


    with col2:

        st.metric(

            "Available Opportunities",

            len(jobs)

        )


    st.divider()

# --------------------------------------------------
# DISPLAY EXECUTIVE JOB CARDS
# --------------------------------------------------

if jobs:


    for index, job in enumerate(
        jobs[:display_limit]
    ):


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



        # ------------------------------------------
        # EXECUTIVE SCORING
        # ------------------------------------------

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


        interview_probability = (

            skill_matcher.interview_probability(

                score["executive_fit"]

            )

        )


        st.subheader(
            f"{role}"
        )


        st.caption(
            f"{company} • {country}"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(

                "Executive Fit",

                f"{score['executive_fit']}%"

            )


        with col2:

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

            priority.get(

                "category",

                "Recommended"

            )

        )


        # ------------------------------------------
        # SAVE APPLICATION
        # ------------------------------------------

        if st.button(

            "📌 Save Application",

            key=f"save_application_{index}"

        ):


            try:

                application_tracker.add_application(

                    job,

                    priority["priority_score"],

                    interview_probability

                )


                st.success(

                    "✅ Application saved to CRM"

                )


            except Exception as e:

                st.error(

                    f"Unable to save application: {e}"

                )


        st.divider()

# --------------------------------------------------
# AI INTELLIGENCE SECTIONS
# --------------------------------------------------

        with st.expander(
            "🧠 AI Skill Analysis"
        ):


            job_analysis = skill_matcher.extract_matching_skills(

                profile.get(
                    "skills",
                    []
                ),

                description

            )


            st.write(
                "### ✅ Matching Skills"
            )


            matched_skills = job_analysis.get(
                "matched",
                []
            )


            if matched_skills:

                for skill in matched_skills:

                    st.success(
                        skill
                    )

            else:

                st.info(
                    "No matching skills detected."
                )


            st.write(
                "### ⚠ Missing Keywords"
            )


            missing_skills = job_analysis.get(
                "missing",
                []
            )


            if missing_skills:

                for skill in missing_skills:

                    st.warning(
                        skill
                    )

            else:

                st.success(
                    "No major keyword gaps detected."
                )



        # --------------------------------------------------
        # RESUME TAILORING
        # --------------------------------------------------

        with st.expander(
            "✨ AI Resume Tailoring"
        ):


            try:

                resume_analysis = resume_tailor.analyze_job_fit(

                    profile,

                    job

                )


                tailored_summary = resume_tailor.generate_executive_summary(

                    profile,

                    job

                )


                st.metric(

                    "Resume Match Score",

                    f"{resume_analysis.get('match_score',0)}%"

                )


                st.write(
                    "### Tailored Executive Summary"
                )


                st.info(
                    tailored_summary
                )


            except Exception as e:


                st.warning(

                    f"Resume tailoring unavailable: {e}"

                )



        # --------------------------------------------------
        # EXECUTIVE SCORE BREAKDOWN
        # --------------------------------------------------

        with st.expander(
            "📊 Executive Score Breakdown"
        ):


            st.write(

                f"ATS Score: {score.get('ats_score',0)}%"

            )


            st.write(

                f"Leadership Score: {score.get('leadership_score',0)}%"

            )


            st.write(

                f"Experience Score: {score.get('experience_score',0)}%"

            )



        # --------------------------------------------------
        # APPLICATION ASSISTANT
        # --------------------------------------------------

        with st.expander(
            "✉️ AI Application Assistant"
        ):


            try:

                linkedin_message = application_assistant.generate_linkedin_message(

                    profile,

                    job

                )


                cover_letter = application_assistant.generate_cover_letter(

                    profile,

                    job

                )


                interview_questions = application_assistant.generate_interview_questions(

                    job

                )


                tab1, tab2, tab3 = st.tabs(

                    [

                        "LinkedIn Message",

                        "Cover Letter",

                        "Interview Preparation"

                    ]

                )


                with tab1:

                    st.text_area(

                        "Recruiter LinkedIn Message",

                        linkedin_message,

                        height=250,

                        key=f"linkedin_{index}"

                    )


                with tab2:

                    st.text_area(

                        "Executive Cover Letter",

                        cover_letter,

                        height=350,

                        key=f"cover_{index}"

                    )


                with tab3:

                    st.write(
                        "### 🎯 Interview Questions"
                    )


                    for question in interview_questions:

                        st.write(

                            "•",

                            question

                        )


            except Exception as e:

                st.warning(

                    f"Application assistant unavailable: {e}"

                )


        # --------------------------------------------------
        # JOB DETAILS
        # --------------------------------------------------

        with st.expander(
            "📄 View Job Details"
        ):

            st.json(
                job
            )


        st.divider()

# --------------------------------------------------
# EMPTY STATE
# --------------------------------------------------

if not jobs and not st.session_state.search_completed:

    st.info(
        """
        👋 Welcome to AI Executive Jobs.

        Click **🚀 Search Global Executive Jobs**
        to discover international executive opportunities.
        """
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "JobHunter AI • Executive Job Intelligence Platform • Version 1.0 RC"
)