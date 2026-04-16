import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="财务健康检查器", layout="wide")
st.title("📊 财务健康检查器")
st.markdown("基于 Altman Z-Score 模型，查看上市公司的破产风险趋势")

@st.cache_data
def load_data():
    df = pd.read_excel("data/companies.xlsx")
    return df

df = load_data()
companies = df["company_name"].unique()
ticker_map = dict(zip(df["company_name"], df["ticker"]))

st.sidebar.header("选择公司")
selected_company = st.sidebar.selectbox("公司", companies)

company_data = df[df["company_name"] == selected_company].sort_values("year")
ticker = ticker_map[selected_company]

latest = company_data.iloc[-1]
st.subheader(f"{selected_company} ({ticker})")

col1, col2, col3 = st.columns(3)
col1.metric("最新 Z-Score", f"{latest['zscore']:.2f}")
col2.metric("财务状态", latest["status"])
col3.metric("数据年份", latest["year"])

st.subheader("📈 Z-Score 历史趋势")
fig = px.line(company_data, x="year", y="zscore", markers=True)
fig.add_hline(y=2.99, line_dash="dash", line_color="green", annotation_text="安全区 (2.99)")
fig.add_hline(y=1.81, line_dash="dash", line_color="red", annotation_text="危险区 (1.81)")
st.plotly_chart(fig, use_container_width=True)

with st.expander("查看详细数据"):
    st.dataframe(company_data[["year", "zscore", "status"]])

st.info("""
**Z-Score 解读**：
- 🟢 > 2.99 : 安全区，破产风险极低
- 🟡 1.81 – 2.99 : 灰色区，存在一定风险
- 🔴 < 1.81 : 危险区，破产风险较高
""")