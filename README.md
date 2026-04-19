# acc102_mini_assignment_2469739
Mini Assignment track 4
# Financial Health Checker

A Streamlit app that visualizes Altman Z-Score trends for 30 public companies (Apple, Microsoft, Tesla) to help investors assess bankruptcy risk.

## Problem & Audience
Investors need a quick way to see a company's financial health. This tool provides an interactive Z-Score trend chart with safe/distress zones and a ranking bar chart under five sectors.

## Data Source
Compustat (via WRDS), accessed April 2026. Data includes 2015-2025 for AAPL, MSFT, TSLA and so on.

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
