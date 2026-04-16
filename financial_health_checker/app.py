import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Financial Health Checker", layout="wide")
st.title("📊 Financial Health Checker")
st.markdown("Altman Z-Score based bankruptcy risk indicator for public companies")

@st.cache_data
def load_data():
    df = pd.read_excel("data/companies.xlsx")
    return df

df = load_data()
companies = df["company_name"].unique()
ticker_map = dict(zip(df["company_name"], df["ticker"]))

st.sidebar.header("Select Company")
selected_company = st.sidebar.selectbox("Company", companies)

company_data = df[df["company_name"] == selected_company].sort_values("year")
ticker = ticker_map[selected_company]

latest = company_data.iloc[-1]
st.subheader(f"{selected_company} ({ticker})")

col1, col2, col3 = st.columns(3)
col1.metric("Latest Z-Score", f"{latest['zscore']:.2f}")
col2.metric("Financial Status", latest["status"])
col3.metric("Year", latest["year"])

st.subheader("📈 Z-Score Historical Trend")
fig = px.line(company_data, x="year", y="zscore", markers=True)
fig.add_hline(y=2.99, line_dash="dash", line_color="green", annotation_text="Safe Zone (2.99)")
fig.add_hline(y=1.81, line_dash="dash", line_color="red", annotation_text="Distress Zone (1.81)")
st.plotly_chart(fig, use_container_width=True)

with st.expander("View Detailed Data"):
    st.dataframe(company_data[["year", "zscore", "status"]])

st.info("""
**Z-Score Interpretation**:
- 🟢 > 2.99 : Safe Zone - Very low bankruptcy risk
- 🟡 1.81 – 2.99 : Gray Zone - Moderate risk
- 🔴 < 1.81 : Distress Zone - High bankruptcy risk
""")
