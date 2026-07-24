import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Global Executive Job Hunter",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Executive Job Hunter")

jobs = pd.DataFrame([
    ["Head of Sales","Google","Singapore","35 min ago"],
    ["Country Manager","Microsoft","Germany","20 min ago"],
    ["VP Sales","Oracle","UAE","50 min ago"],
    ["Director Sales","SAP","Poland","15 min ago"],
    ["Business Development Director","Amazon","UK","45 min ago"],
    ["Chief Revenue Officer","Siemens","Saudi Arabia","30 min ago"],
])

jobs.columns = ["Role","Company","Country","Posted"]

# ---------- KPIs ----------
c1, c2, c3 = st.columns(3)

c1.metric("Total Jobs", len(jobs))
c2.metric("Countries", jobs["Country"].nunique())
c3.metric("Companies", jobs["Company"].nunique())

st.divider()

# ---------- Filters ----------
role = st.selectbox(
    "Select Role",
    ["All"] + sorted(jobs["Role"].unique().tolist())
)

if role != "All":
    jobs = jobs[jobs["Role"] == role]

st.dataframe(jobs, use_container_width=True)

st.divider()

country_count = jobs.groupby("Country").size().reset_index(name="Jobs")

fig = px.bar(
    country_count,
    x="Country",
    y="Jobs",
    title="Jobs by Country"
)

st.plotly_chart(fig, use_container_width=True)