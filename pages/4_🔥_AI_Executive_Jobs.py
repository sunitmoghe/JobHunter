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

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Executive Jobs",
    page_icon="🔥",
    layout="wide"
)

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
            "Australia",
        ],
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

            jobs = agent.search_all_roles()

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

progress_state = search_progress.get_state()

if progress_state["running"]:

    st.progress(
        progress_state["progress"]
    )

    st.caption(
        f"Searching : {progress_state['current_role']}"
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
    # Country Filter
    # ------------------------------------------

    if preferred_country != "All":

        jobs = [
            job
            for job in jobs
            if preferred_country.lower()
            in job.get("country", "").lower()
        ]

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


# --------------------------------------------------
# SALARY INTELLIGENCE
# --------------------------------------------------

if jobs:

    st.header("💰 Executive Salary Intelligence")

    selected_job = st.selectbox(

        "Select Job",

        range(len(jobs)),

        format_func=lambda x:

        f"{jobs[x].get('role','')} - {jobs[x].get('company','')}"

    )

    selected = jobs[selected_job]

    role = selected.get(

        "role",

        selected.get(

            "title",

            ""

        )

    )

    country = selected.get(

        "country",

        "Singapore"

    )

    salary = salary_engine.get_salary_benchmark(

        country,

        role

    )

    if "average" in salary:

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(

                "Low",

                f"{salary['currency']} {salary['low']:,}"

            )

        with col2:

            st.metric(

                "Average",

                f"{salary['currency']} {salary['average']:,}"

            )

        with col3:

            st.metric(

                "High",

                f"{salary['currency']} {salary['high']:,}"

            )

    else:

        st.warning(

            salary.get(

                "message",

                "Salary benchmark unavailable."

            )

        )

# --------------------------------------------------
# OFFER COMPARISON
# --------------------------------------------------

    st.subheader("📈 Compare Your Offer")

    offered_salary = st.number_input(

        "Enter Offered Salary",

        min_value=0,

        step=1000

    )

    if offered_salary > 0:

        comparison = salary_engine.compare_offer(

            country,

            role,

            offered_salary

        )

        if "rating" in comparison:

            col1, col2 = st.columns(2)

            with col1:

                st.metric(

                    "Market Average",

                    f"{salary['currency']} {comparison['market_average']:,}"

                )

            with col2:

                st.metric(

                    "Difference",

                    f"{comparison['difference_percentage']}%"

                )

            if comparison["rating"] == "Excellent Offer":

                st.success(

                    "🎉 Excellent Offer"

                )

            elif comparison["rating"] == "Good Offer":

                st.info(

                    "👍 Good Market Offer"

                )

            else:

                st.warning(

                    "⚠ Below Market Average"

                )

# --------------------------------------------------
# EXECUTIVE MARKET POSITION
# --------------------------------------------------

    st.subheader("🎯 Executive Market Position")

    recommendation = salary_engine.recommend_market_position(

        experience,

        "Executive"

    )

    st.success(

        recommendation["level"]

    )

    st.write(

        "### Recommended Roles"

    )

    for item in recommendation[

        "recommended_roles"

    ]:

        st.write(

            "•",

            item

        )

# --------------------------------------------------
# MARKET INSIGHTS
# --------------------------------------------------

    st.subheader("🌍 AI Market Intelligence")

    if country == "Singapore":

        st.success(

            "Singapore remains one of the strongest executive hiring markets for technology, SaaS, Industrial Automation and Manufacturing."

        )

    elif country == "Germany":

        st.info(

            "Germany continues strong hiring across Industry 4.0, Manufacturing and Automation."

        )

    elif country == "UAE":

        st.success(

            "UAE has strong demand for enterprise sales leaders across Technology, Energy and Infrastructure."

        )

    elif country == "India":

        st.info(

            "India continues expanding executive hiring across SaaS, AI, Manufacturing and Telecom."

        )

    else:

        st.info(

            "Market intelligence is continuously improving."

        )

    st.divider()

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
# --------------------------------------------------
# SPRINT 19 DASHBOARD
# --------------------------------------------------

st.header("🚀 Sprint 19 Intelligence Dashboard")

dashboard_col1, dashboard_col2 = st.columns(2)

with dashboard_col1:

    st.success("✅ Company Intelligence")

    st.success("✅ Salary Intelligence")

    st.success("✅ Duplicate Detection")

    st.success("✅ Saved Jobs")

with dashboard_col2:

    st.success("✅ Job Cache")

    st.success("✅ Search Progress")

    st.success("✅ Executive Analytics")

    st.success("✅ AI Resume Tailoring")

st.divider()

# --------------------------------------------------
# PLATFORM STATISTICS
# --------------------------------------------------

st.header("📊 Platform Statistics")

if jobs:

    st.write(

        f"Executive Jobs Available : {len(jobs)}"

    )

    st.write(

        f"Saved Jobs : {saved_stats['saved_jobs']}"

    )

    st.write(

        f"Duplicate Jobs Removed : {duplicates_removed}"

    )

    st.write(

        f"Cached Searches : {cache_stats['cached_roles']}"

    )

st.divider()

# --------------------------------------------------
# EMPTY STATE
# --------------------------------------------------

if not jobs and not st.session_state.search_completed:

    st.info(
        """
👋 **Welcome to AI Executive Jobs**

Click **🚀 Search Global Executive Jobs**
to discover international executive opportunities.

Powered by:

• AI Executive Search Engine
• Company Intelligence
• Salary Intelligence
• Duplicate Detection
• Executive Scoring Engine
• AI Resume Tailoring
• Application Assistant
• Saved Jobs Dashboard
• Executive Analytics
"""
    )

# --------------------------------------------------
# SPRINT 19 FEATURES
# --------------------------------------------------

st.divider()

st.header("🚀 Sprint 19 Features")

feature_col1, feature_col2 = st.columns(2)

with feature_col1:

    st.success("✅ AI Executive Search")

    st.success("✅ Company Intelligence")

    st.success("✅ Salary Intelligence")

    st.success("✅ Duplicate Job Detection")

    st.success("✅ Executive Analytics")

    st.success("✅ AI Resume Tailoring")

with feature_col2:

    st.success("✅ Saved Jobs Manager")

    st.success("✅ Job Cache")

    st.success("✅ Search Progress")

    st.success("✅ Executive Score Engine")

    st.success("✅ Application Assistant")

    st.success("✅ Recruiter CRM Integration")

# --------------------------------------------------
# AI STATUS
# --------------------------------------------------

st.divider()

st.subheader("🤖 AI Platform Status")

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:

    st.metric(

        "Sprint",

        "19"

    )

with status_col2:

    st.metric(

        "Platform",

        "Operational"

    )

with status_col3:

    st.metric(

        "AI Modules",

        "13"

    )

# --------------------------------------------------
# FUTURE ROADMAP
# --------------------------------------------------

with st.expander("🛣 Upcoming Sprint Roadmap"):

    st.write("### Sprint 20")

    st.write("• Live LinkedIn Executive Search")

    st.write("• Executive Recruiter Finder")

    st.write("• Executive Referral Engine")

    st.write("• AI Cover Letter Optimiser")

    st.write("• Salary Negotiation AI")

    st.write("• Executive Networking Assistant")

    st.write("• Interview Success Predictor")

    st.write("• Executive Career Copilot")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    """
JobHunter AI • Executive Career Intelligence Platform

Version : Sprint 19

Designed for Global Executive Careers

© 2026 JobHunter AI
"""
)