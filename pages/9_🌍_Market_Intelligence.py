import streamlit as st
import pandas as pd

from modules.market_analytics import MarketAnalytics
from modules.salary_intelligence import SalaryIntelligence

from modules.ui_components import (
    page_header,
    section_header,
    metric_row,
    success_box,
    warning_box,
    info_box,
    divider,
)


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Market Intelligence",
    page_icon="🌍",
    layout="wide"
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

page_header(
    "🌍 Executive Market Intelligence Dashboard",
    "Global executive opportunities, demand trends and compensation intelligence."
)


market = MarketAnalytics()

salary = SalaryIntelligence()



# --------------------------------------------------
# TOP MARKETS
# --------------------------------------------------

section_header(
    "🔥 Top Executive Markets"
)


top_markets = market.get_top_markets()


cols = st.columns(3)


for index, item in enumerate(top_markets[:3]):

    with cols[index]:

        st.metric(
            item["country"],
            f"{item['demand_score']}% Demand"
        )

        st.write(
            f"Salary Index: {item['salary_index']}%"
        )


divider()



# --------------------------------------------------
# ROLE DEMAND
# --------------------------------------------------

section_header(
    "📈 Executive Role Demand"
)


role_demand = market.get_role_demand()


for role, count in role_demand:

    success_box(
        f"{role} → Market Demand Score: {count*25}%"
    )


divider()



# --------------------------------------------------
# SKILL TRENDS
# --------------------------------------------------

section_header(
    "🧠 Executive Skill Trends"
)


skill_trends = market.get_skill_trends()


for skill, count in skill_trends:

    info_box(
        f"{skill} → Demand Index: {count*25}%"
    )


divider()



# --------------------------------------------------
# COUNTRY ANALYSIS
# --------------------------------------------------

section_header(
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


metric_row(
    [

        (
            "Hiring Demand",
            f"{analysis.get('demand_score',0)}%"
        ),

        (
            "Salary Index",
            f"{analysis.get('salary_index',0)}%"
        ),

        (
            "Market",
            country
        )

    ]
)


st.subheader(
    "Recommended Executive Roles"
)


for role in analysis.get(
    "top_roles",
    []
):

    success_box(
        role
    )


st.subheader(
    "Required Skills"
)


for skill in analysis.get(
    "skills",
    []
):

    warning_box(
        skill
    )


divider()



# --------------------------------------------------
# SALARY BENCHMARK
# --------------------------------------------------

section_header(
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


    metric_row(

        [

            (
                "Low Range",
                f"{benchmark['currency']} {benchmark['low']:,}"
            ),

            (
                "Average",
                f"{benchmark['currency']} {benchmark['average']:,}"
            ),

            (
                "High Range",
                f"{benchmark['currency']} {benchmark['high']:,}"
            )

        ]

    )


else:

    warning_box(
        benchmark.get(
            "message",
            "No salary data available"
        )
    )


divider()



# --------------------------------------------------
# CAREER RECOMMENDATION
# --------------------------------------------------

section_header(
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


success_box(

    "Recommended Markets: "
    +
    ", ".join(
        recommendation["recommended_markets"]
    )

)


info_box(

    recommendation[
        "recommended_strategy"
    ]

)



divider()


st.success(
    "✅ Market Intelligence Dashboard operational."
)


st.caption(
    "JobHunter AI • Executive Market Intelligence Suite"
)