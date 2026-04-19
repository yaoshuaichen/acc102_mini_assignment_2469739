import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Financial Health Analyzer", layout="wide")
st.title("📊 Altman Z-Score Financial Health Analyzer")
st.markdown("Compare companies' bankruptcy risk within their industry")

@st.cache_data
def load_data():
    df = pd.read_excel("data/companies_zscore.xlsx")
    return df

df = load_data()
companies = df["tic"].unique()
sectors = sorted(df["sector"].dropna().unique())

st.sidebar.header("Filters")
selected_sector = st.sidebar.selectbox("Industry Sector", ["All"] + sectors)

if selected_sector != "All":
    sector_companies = df[df["sector"] == selected_sector]["tic"].unique()
else:
    sector_companies = companies

st.sidebar.header("Select Company")
cols_per_row = 3
button_cols = st.sidebar.columns(cols_per_row)
selected_company = None
for i, comp in enumerate(sorted(sector_companies)):
    col = button_cols[i % cols_per_row]
    if col.button(comp, key=comp, use_container_width=True):
        selected_company = comp

if selected_company is None and len(sector_companies) > 0:
    selected_company = sorted(sector_companies)[0]

if selected_company is None:
    st.warning("No companies in this sector.")
    st.stop()

company_df = df[df["tic"] == selected_company].sort_values("year")
sector_name = company_df["sector"].iloc[0]
sector_avg = df[df["sector"] == sector_name].groupby("year")["zscore"].mean().reset_index()
sector_avg.columns = ["year", "sector_avg_zscore"]
merged = company_df.merge(sector_avg, on="year", how="left")

latest = company_df.iloc[-1]
st.subheader(f"{latest['conm']} ({selected_company})")
col1, col2, col3 = st.columns(3)
col1.metric("Latest Z-Score", f"{latest['zscore']:.2f}")
col2.metric("Status", latest["status"])
col3.metric("Year", latest["year"])

fig_line = go.Figure()
fig_line.add_trace(go.Scatter(x=merged["year"], y=merged["zscore"], mode='lines+markers', name=selected_company))
fig_line.add_trace(go.Scatter(x=merged["year"], y=merged["sector_avg_zscore"], mode='lines', name=f"{sector_name} Avg", line=dict(dash='dash')))
fig_line.add_hline(y=2.99, line_dash="dash", line_color="green", annotation_text="Safe Zone (2.99)")
fig_line.add_hline(y=1.81, line_dash="dash", line_color="red", annotation_text="Distress Zone (1.81)")
fig_line.update_layout(title="Z-Score Trend vs Industry Average", xaxis_title="Year", yaxis_title="Z-Score")
st.plotly_chart(fig_line, use_container_width=True)

sector_latest = df[(df["sector"] == sector_name) & (df["year"] == latest["year"])].sort_values("zscore", ascending=False)
fig_bar = px.bar(sector_latest, x="tic", y="zscore", color="status", title=f"{sector_name} Sector - Latest Z-Score Ranking")
st.plotly_chart(fig_bar, use_container_width=True)

with st.expander("View historical data"):
    st.dataframe(company_df[["year", "zscore", "status"]])

st.info("""
**Z-Score Interpretation**:
- 🟢 > 2.99 : Safe Zone - Very low bankruptcy risk
- 🟡 1.81 – 2.99 : Gray Zone - Moderate risk
- 🔴 < 1.81 : Distress Zone - High bankruptcy risk
""")