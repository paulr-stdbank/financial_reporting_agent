import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader   import load_financials   # ← implement to read your store
from utils.analytics     import calc_ratios, yoy_growth
from utils.bedrock_client import llm_complete

st.set_page_config("Financial Statement Explorer", page_icon="💹", layout="wide")

# --- Sidebar ------------------------------------------------------------------------------------------------------
st.sidebar.title("🔍 Select company")
companies = load_financials().index.get_level_values("company").unique().tolist()
company   = st.sidebar.selectbox("Company", companies)

metric    = st.sidebar.selectbox("Primary metric", ["revenue", "netIncome", "operatingIncome"])
show_rat  = st.sidebar.checkbox("Show key ratios", True)
show_yoy  = st.sidebar.checkbox("Show YoY growth", True)

# --- Data prep ----------------------------------------------------------------------------------------------------
df_raw    = load_financials().loc[pd.IndexSlice[company, :], :].reset_index(drop=True)
df_ratios = calc_ratios(df_raw)

# --- Visuals ------------------------------------------------------------------------------------------------------
st.subheader(f"{company} – {metric} over time")
fig = px.line(df_raw, x="date", y=metric, markers=True, title=f"{metric} trend")
st.plotly_chart(fig, use_container_width=True)

if show_yoy:
    st.subheader("Year-on-Year (%)")
    yoy = yoy_growth(df_raw, metric)
    st.bar_chart(yoy, use_container_width=True)

if show_rat:
    st.subheader("Selected ratios")
    st.dataframe(df_ratios[["gross_margin", "oper_margin", "net_margin",
                            "debt_equity", "return_on_eq"]])

# --- LLM narrative ------------------------------------------------------------------------------------------------
with st.expander("📄 Auto-generated commentary"):
    prompt = (
        "Write a concise (≈200-word) financial analysis for {comp}. "
        "Use the following JSON:\n\n"
        f"{df_raw.tail(5).to_json(orient='records')}\n\n"
        "Highlight revenue trajectory, profitability, leverage, and any notable YoY changes. "
        "Close with an outlook statement."
    ).format(comp=company)
    if st.button("Generate report"):
        with st.spinner("Calling Bedrock…"):
            analysis = llm_complete(prompt)
        st.markdown(analysis)
