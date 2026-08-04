import streamlit as st

from modules.executive_ai_agent import ExecutiveAIAgent
from modules.priority_engine import PriorityEngine
from modules.executive_scoring_engine import ExecutiveScoringEngine
from modules.profile_manager import ProfileManager
from modules.job_skill_matcher import JobSkillMatcher
from modules.resume_tailor_engine import ResumeTailorEngine
from modules.application_assistant import ApplicationAssistant
from modules.application_tracker import ApplicationTracker

from modules.company_intelligence import CompanyIntelligence
from modules.salary_intelligence import SalaryIntelligence
from modules.duplicate_job_detector import DuplicateJobDetector
from modules.recruiter_intelligence import RecruiterIntelligence
from modules.saved_jobs_manager import SavedJobsManager
from modules.job_cache import JobCache
from modules.search_progress import SearchProgress
from modules.background_job_search import BackgroundJobSearch
from modules.live_company_intelligence import LiveCompanyIntelligence	
from modules.job_card_renderer import JobCardRenderer
from modules.executive_job_renderer import render_jobs
from modules.executive_analytics import render_executive_analytics
from modules.country_analytics import render_country_analytics
from modules.saved_jobs_dashboard import render_saved_jobs_dashboard
from modules.application_summary import render_application_summary
from modules.cache_management import render_cache_management
from modules.salary_dashboard import render_salary_dashboard
from modules.sprint_dashboard import render_sprint_dashboard


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Executive Jobs",
    page_icon="🔥",
    layout="wide"
)

resume_tailor = ResumeTailorEngine()

st.title("🔥 AI Executive Live Job Recommendations")

st.write(
    "Search global executive opportunities using the AI Executive Job Engine."
)

st.divider()


# --------------------------------------------------
# EXECUTIVE DASHBOARD
# --------------------------------------------------

st.subheader("🧠 AI Executive Recommendations")

col1, col2 = st.columns(2)

with col1:

    selected_countries = st.multiselect(
    "Search Countries",
    options=[
        "Singapore",
        "UAE",
        "Saudi Arabia",
        "Qatar",
        "Oman",
        "Kuwait",
        "Bahrain",
        "Germany",
        "Netherlands",
        "Poland",
        "United Kingdom",
        "Canada",
        "Australia",
        "India",
        "Malaysia",
        "Thailand",
        "Vietnam",
        "Indonesia",
    ],
    default=[
        "Singapore",
        "UAE",
        "Germany",
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
            "General Manager",
        ],
    )

st.divider()

filter_col1, filter_col2 = st.columns(2)

with filter_col1:

    visa_filter = st.selectbox(
        "Visa Sponsorship",
        [
            "All",
            "Visa Sponsorship Only",
            "No Sponsorship"
        ]
    )

with filter_col2:

    remote_filter = st.selectbox(
        "Work Mode",
        [
            "All",
            "Remote Friendly",
            "Onsite / Hybrid"
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
# SESSION STATE
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

    experience = profile.get("experience", 0)

else:

    profile = {}

    st.warning(
        "⚠ No Executive Profile found. Please analyse your resume first."
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

company_engine = CompanyIntelligence()

live_company_engine = LiveCompanyIntelligence()

salary_engine = SalaryIntelligence()

recruiter_engine = RecruiterIntelligence()

duplicate_detector = DuplicateJobDetector()

saved_jobs_manager = SavedJobsManager()

job_cache = JobCache()

search_progress = SearchProgress()

background_search = BackgroundJobSearch()

job_renderer = JobCardRenderer(
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
)

# --------------------------------------------------
# JOB SEARCH ENGINE
# --------------------------------------------------

st.subheader("🌍 Global Executive Job Search")

if st.button(
    "🚀 Search Global Executive Jobs",
    type="primary",
):

    search_progress.start()

    with st.spinner("Searching executive opportunities..."):

        try:

            agent = ExecutiveAIAgent()

            jobs = agent.search_all_roles(
                selected_countries=selected_countries
            )

            # ------------------------------------------
            # Company Intelligence
            # ------------------------------------------

            jobs = company_engine.enrich_jobs(
                jobs
            )

            # ------------------------------------------
            # Recruiter Intelligence
            # ------------------------------------------

            jobs = recruiter_engine.enrich_jobs(
                jobs
            )

            # ------------------------------------------
            # Live Company Intelligence
            # ------------------------------------------

            # TEMPORARILY DISABLED
            # Live Company Intelligence is slowing down search.
            #

            jobs = [
                live_company_engine.enrich(job)
                for job in jobs
            ]


            # ------------------------------------------
            # Remove Duplicate Jobs
            # ------------------------------------------

            duplicate_result = duplicate_detector.remove_duplicates(
                jobs
            )

            jobs = duplicate_result["jobs"]

            duplicates_removed = duplicate_result[
                "duplicates_removed"
            ]

            # ------------------------------------------
            # Cache Results
            # ------------------------------------------

            job_cache.save_jobs(
                "executive_search",
                jobs
            )

            st.session_state.executive_jobs = jobs

            st.session_state.duplicates_removed = (
                duplicates_removed
            )

            st.session_state.search_completed = True

            search_progress.finish()

        except Exception as e:

            search_progress.reset()

            st.error(
                f"Job search failed: {e}"
            )

# --------------------------------------------------
# LOAD RESULTS
# --------------------------------------------------

duplicates_removed = st.session_state.get(
    "duplicates_removed",
    0
)

jobs = []


if st.session_state.search_completed:

    jobs = st.session_state.executive_jobs

else:

    cached_jobs = job_cache.get_jobs(
        "executive_search"
    )

    if cached_jobs:

        jobs = cached_jobs

        st.info(
            "⚡ Loaded jobs from cache."
        )


# --------------------------------------------------
# SEARCH PROGRESS
# --------------------------------------------------

if background_search.is_running():

    st.progress(
        background_search.get_progress()
    )

    st.info
    f"🔎 Searching Executive Role : {background_search.get_current_role()}"
    
    

elif background_search.is_completed():

    st.success(
        f"✅ Background Search Completed ({len(background_search.get_jobs())} jobs)"
    )    


# --------------------------------------------------
# SEARCH SUMMARY
# --------------------------------------------------

if jobs:

    st.success(
        f"Found {len(jobs)} Executive Opportunities"
    )

    if duplicates_removed > 0:

        st.info(
            f"🔄 Removed {duplicates_removed} duplicate jobs."
        )

else:

    if st.session_state.search_completed:

        st.warning(
            "No executive jobs found."
        )


# --------------------------------------------------
# SEARCH STATISTICS
# --------------------------------------------------

if jobs:

    # ------------------------------------------
    # Role Filter
    # ------------------------------------------

    if preferred_role != "All":

        jobs = [
            job
            for job in jobs
            if preferred_role.lower()
            in job.get(
                "role",
                job.get("title", "")
            ).lower()
        ]

# ------------------------------------------
# Visa Filter
# ------------------------------------------

if visa_filter == "Visa Sponsorship Only":

    jobs = [
        job
        for job in jobs
        if job.get("visa_sponsorship", False)
    ]

elif visa_filter == "No Sponsorship":

    jobs = [
        job
        for job in jobs
        if not job.get("visa_sponsorship", False)
    ]


# ------------------------------------------
# Remote Filter
# ------------------------------------------

if remote_filter == "Remote Friendly":

    jobs = [
        job
        for job in jobs
        if job.get("remote_friendly", False)
    ]

elif remote_filter == "Onsite / Hybrid":

    jobs = [
        job
        for job in jobs
        if not job.get("remote_friendly", False)
    ]

    total_jobs = len(jobs)

    cache_stats = job_cache.statistics()

    saved_stats = saved_jobs_manager.statistics()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Jobs Found",
            total_jobs
        )

    with col2:

        st.metric(
            "Saved Jobs",
            saved_stats["saved_jobs"]
        )

    with col3:

        st.metric(
            "Duplicates Removed",
            duplicates_removed
        )

    with col4:

        st.metric(
            "Cached Searches",
            cache_stats["cached_roles"]
        )

    st.divider()


# --------------------------------------------------
# DISPLAY LIMIT
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
# DISPLAY EXECUTIVE JOBS
# --------------------------------------------------

render_jobs(
    jobs=jobs,
    profile=profile,
    job_renderer=job_renderer,
)

# --------------------------------------------------
# EXECUTIVE ANALYTICS
# --------------------------------------------------

render_executive_analytics(jobs)

render_salary_dashboard(
    jobs,
    salary_engine,
    experience,
)
# --------------------------------------------------
# SAVED JOBS DASHBOARD
# --------------------------------------------------

render_saved_jobs_dashboard(saved_jobs_manager)

# --------------------------------------------------
# APPLICATION SUMMARY
# --------------------------------------------------

render_application_summary(
    saved_jobs_manager,
    job_cache,
)

st.divider()
# --------------------------------------------------
# CACHE MANAGEMENT
# --------------------------------------------------

render_cache_management(
    job_cache,
    saved_jobs_manager,
)

st.divider()

render_sprint_dashboard()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    """
JobHunter AI • Executive Career Intelligence Platform

Version : Sprint 19

Designed and Developed by : Sunit S Moghe

© 2026 JobHunter AI
"""
)