import streamlit as st
import pandas as pd

from modules.executive_ai_agent import ExecutiveAIAgent
from modules.market_intelligence_engine import MarketIntelligenceEngine

st.set_page_config(
    page_title="Market Intelligence",
    page_icon="🌍",
    layout="wide",
)

st.title("🌍 Global Executive Market Intelligence")

agent = ExecutiveAIAgent()
engine = MarketIntelligenceEngine()

jobs = agent.search_all_roles(max_roles=100)

markets = engine.analyse(jobs)

if markets:

    df = pd.DataFrame(markets)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    st.success(
        f"Markets analysed : {len(df)}"
    )

    top = df.iloc[0]

    st.info(
        f"🏆 Top Market : {top['Country']} ({top['Jobs']} Jobs)"
    )

else:

    st.warning("No market intelligence available.")

st.success("Market Intelligence Ready")