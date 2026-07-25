import streamlit as st
import pandas as pd
import plotly.express as px

from modules.application_analytics import ApplicationAnalytics


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📈",
    layout="wide"
)


st.title(
    "📈 Executive Career Analytics Dashboard"
)


st.write(
    "Monitor your job search performance and application pipeline."
)


analytics = ApplicationAnalytics()


summary = analytics.get_summary()


# --------------------------------------------------
# METRICS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Total Applications",
    summary.get(
        "total",
        0
    )
)


col2.metric(
    "Applied",
    summary.get(
        "statuses",
        {}
    ).get(
        "Applied",
        0
    )
)


col3.metric(
    "Interviews",
    summary.get(
        "statuses",
        {}
    ).get(
        "Interview",
        0
    )
)


col4.metric(
    "Offers",
    summary.get(
        "statuses",
        {}
    ).get(
        "Offer",
        0
    )
)


st.divider()


# --------------------------------------------------
# PIPELINE CHART
# --------------------------------------------------

statuses = summary.get(
    "statuses",
    {}
)


if statuses:


    chart = pd.DataFrame(
        statuses.items(),
        columns=[
            "Status",
            "Count"
        ]
    )


    fig = px.bar(
        chart,
        x="Status",
        y="Count",
        title="Application Pipeline"
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


else:

    st.info(
        "No application data available yet."
    )


st.divider()


st.subheader(
    "🎯 Career Search Insights"
)


st.write(
    """
    Recommended tracking:

    ✅ Applications per week  
    ✅ Interview conversion rate  
    ✅ Offer conversion rate  
    ✅ Recruiter engagement  
    ✅ Country-wise opportunities
    """
)