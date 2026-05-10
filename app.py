import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="Climate Risk & ESG Intelligence Dashboard",
    layout="wide"
)

# Dashboard Title
st.title("🌍 Climate Risk & ESG Intelligence Dashboard")

st.markdown("""
### Sustainable Finance | ESG Analytics | Climate Risk Modelling

This dashboard provides insights into:
- Climate Risk Assessment
- ESG Performance Tracking
- Renewable Energy Transition
- Sustainable Finance Indicators
- Physical & Transition Risk Analytics
""")

# Load Dataset
@st.cache_data
def load_data():
    data = pd.read_csv("climate_data.csv")
    return data

df = load_data()

# Sidebar
st.sidebar.header("Dashboard Filters")

selected_year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))

sector = st.sidebar.selectbox(
    "Select Sector",
    ["Banking", "Energy", "Manufacturing", "Agriculture"]
)

risk_type = st.sidebar.radio(
    "Select Risk Type",
    ["Physical Risk", "Transition Risk"]
)

filtered_df = df[df["Year"] == selected_year]

# KPI Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "CO₂ Emissions",
        f"{filtered_df['CO2_Emissions'].values[0]} Gt"
    )

with col2:
    st.metric(
        "Renewable Energy",
        f"{filtered_df['Renewable_Energy'].values[0]}%"
    )

with col3:
    st.metric(
        "ESG Score",
        filtered_df['ESG_Score'].values[0]
    )

st.markdown("---")

# Executive Summary
st.subheader("📌 Executive Summary")

st.info(f"""
The selected year {selected_year} indicates increasing ESG performance and renewable energy adoption.

Sector Selected: {sector}

Risk Focus:
- Physical risks involve climate disasters and environmental exposure.
- Transition risks involve policy, carbon taxes and green transition impacts.

The dashboard highlights climate-risk trends aligned with sustainable finance frameworks.
""")

# CO2 Emissions Trend
fig1 = px.line(
    df,
    x="Year",
    y="CO2_Emissions",
    markers=True,
    title="CO₂ Emissions Trend"
)

st.plotly_chart(fig1, use_container_width=True)

# Renewable Energy Growth
fig2 = px.area(
    df,
    x="Year",
    y="Renewable_Energy",
    title="Renewable Energy Growth"
)

st.plotly_chart(fig2, use_container_width=True)

# ESG Score Trend
fig3 = px.bar(
    df,
    x="Year",
    y="ESG_Score",
    title="ESG Score Trend"
)

st.plotly_chart(fig3, use_container_width=True)

# Climate Risk Heatmap
heatmap_data = pd.DataFrame({
    "Sector": ["Banking", "Energy", "Manufacturing", "Agriculture"],
    "Physical Risk": [65, 88, 72, 91],
    "Transition Risk": [70, 95, 75, 60]
})

fig_heatmap = px.imshow(
    heatmap_data.set_index("Sector"),
    text_auto=True,
    title="Sector-wise Climate Risk Heatmap"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# ESG Company Comparison
company_df = pd.DataFrame({
    "Company": ["Tata", "Infosys", "Reliance", "Adani"],
    "ESG Score": [82, 88, 65, 58]
})

fig_company = px.bar(
    company_df,
    x="Company",
    y="ESG Score",
    title="ESG Score Comparison"
)

st.plotly_chart(fig_company, use_container_width=True)

# Risk Comparison
risk_df = pd.DataFrame({
    "Risk Type": ["Physical Risk", "Transition Risk"],
    "Score": [
        filtered_df['Physical_Risk'].values[0],
        filtered_df['Transition_Risk'].values[0]
    ]
})

fig4 = px.bar(
    risk_df,
    x="Risk Type",
    y="Score",
    title="Climate Risk Comparison"
)

st.plotly_chart(fig4, use_container_width=True)

# Net Zero Progress
st.subheader("🌱 Net Zero Progress Tracker")

progress_value = 76

st.progress(progress_value / 100)

st.write(f"Current Net Zero Alignment Progress: {progress_value}%")

# ESG Gauge Chart
fig5 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=filtered_df['ESG_Score'].values[0],
    title={'text': "ESG Performance"},
    gauge={
        'axis': {'range': [0, 100]}
    }
))

st.plotly_chart(fig5, use_container_width=True)

# Footer
st.markdown("---")

st.caption("""
Built using Python, Streamlit, Pandas & Plotly

Climate Risk | ESG Analytics | Sustainable Finance | Environmental Intelligence
""")