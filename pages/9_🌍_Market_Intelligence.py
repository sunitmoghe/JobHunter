import streamlit as st

from modules.market_analytics import MarketAnalytics
from modules.salary_intelligence import SalaryIntelligence


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Market Intelligence",
    page_icon="🌍",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title(
    "🌍 Executive Market Intelligence Dashboard"
)

st.write(
    "Analyse global executive opportunities, demand trends and compensation intelligence."
)



market = MarketAnalytics()

salary = SalaryIntelligence()



# --------------------------------------------------
# TOP MARKETS
# --------------------------------------------------

st.subheader(
    "🔥 Top Executive Markets"
)


top_markets = market.get_top_markets()


col1, col2, col3 = st.columns(3)


for index, item in enumerate(top_markets[:3]):

    with [col1, col2, col3][index]:

        st.metric(
            item["country"],
            f"{item['demand_score']}% Demand"
        )

        st.write(
            f"Salary Index: {item['salary_index']}%"
        )



st.divider()



# --------------------------------------------------
# ROLE DEMAND
# --------------------------------------------------

st.subheader(
    "📈 Executive Role Demand"
)


role_demand = market.get_role_demand()


for role, count in role_demand:

    st.success(
        f"{role}  →  Market Demand Score: {count*25}%"
    )



st.divider()



# --------------------------------------------------
# SKILL TRENDS
# --------------------------------------------------

st.subheader(
    "🧠 Executive Skill Trends"
)


skill_trends = market.get_skill_trends()


for skill, count in skill_trends:

    st.info(
        f"{skill}  →  Demand Index: {count*25}%"
    )



st.divider()



# --------------------------------------------------
# COUNTRY ANALYSIS
# --------------------------------------------------

st.subheader(
    "🌍 Country Market Analysis"
)


country = st.selectbox(

    "Select Country",

    [

        "Singapore",

        "UAE",

        "Germany",

        "India"

    ]

)



analysis = market.get_country_analysis(
    country
)


st.write(
    "### Market Position"
)


st.metric(

    "Hiring Demand",

    f"{analysis.get('demand_score',0)}%"

)


st.metric(

    "Salary Index",

    f"{analysis.get('salary_index',0)}%"

)



st.write(
    "### Recommended Roles"
)


for role in analysis.get(
    "top_roles",
    []
):

    st.success(
        role
    )



st.write(
    "### Required Skills"
)


for skill in analysis.get(
    "skills",
    []
):

    st.warning(
        skill
    )



st.divider()



# --------------------------------------------------
# SALARY BENCHMARK
# --------------------------------------------------

st.subheader(
    "💰 Executive Salary Benchmark"
)


role = st.selectbox(

    "Select Executive Role",

    [

        "VP Sales",

        "Head of Sales",

        "Regional Sales Director"

    ]

)



benchmark = salary.get_salary_benchmark(

    country,

    role

)



if "average" in benchmark:


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(

            "Low Range",

            f"{benchmark['currency']} {benchmark['low']:,}"

        )


    with col2:

        st.metric(

            "Average",

            f"{benchmark['currency']} {benchmark['average']:,}"

        )


    with col3:

        st.metric(

            "High Range",

            f"{benchmark['currency']} {benchmark['high']:,}"

        )


else:

    st.warning(
        benchmark.get(
            "message",
            "No salary data available"
        )
    )



st.divider()



# --------------------------------------------------
# CAREER RECOMMENDATION
# --------------------------------------------------

st.subheader(
    "🎯 Executive Career Recommendation"
)


recommendation = market.executive_market_recommendation(

    23,

    [

        "Technology",

        "Telecom",

        "SaaS"

    ]

)



st.success(

    ", ".join(

        recommendation["recommended_markets"]

    )

)


st.info(

    recommendation["recommended_strategy"]

)