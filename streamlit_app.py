import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Climate Risk & ESG Intelligence Dashboard", layout="wide")
st.title("🌍 Climate Risk & ESG Intelligence Dashboard")

@st.cache_data
def load_data():
    data = pd.read_csv("climate_data.csv")
    return data

df = load_data()

st.sidebar.header("Dashboard Filters")
selected_year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))
sector = st.sidebar.selectbox("Select Sector", ["Banking", "Energy", "Manufacturing", "Agriculture"])
risk_type = st.sidebar.radio("Select Risk Type", ["Physical Risk", "Transition Risk"])

filtered_df = df[df["Year"] == selected_year]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("CO₂ Emissions", f"{filtered_df['CO2_Emissions'].values[0]} Gt")
with col2:
    st.metric("Renewable Energy", f"{filtered_df['Renewable_Energy'].values[0]}%")
with col3:
    st.metric("ESG Score", filtered_df['ESG_Score'].values[0])

st.markdown("---")
st.plotly_chart(px.line(df, x="Year", y="CO2_Emissions", markers=True, title="CO₂ Emissions Trend"), use_container_width=True)
st.plotly_chart(px.area(df, x="Year", y="Renewable_Energy", title="Renewable Energy Growth"), use_container_width=True)
st.plotly_chart(px.bar(df, x="Year", y="ESG_Score", title="ESG Score Trend"), use_container_width=True)

heatmap_data = pd.DataFrame({
    "Sector": ["Banking", "Energy", "Manufacturing", "Agriculture"],
    "Physical Risk": [65, 88, 72, 91],
    "Transition Risk": [70, 95, 75, 60]
})
st.plotly_chart(px.imshow(heatmap_data.set_index("Sector"), text_auto=True, title="Sector-wise Climate Risk Heatmap"), use_container_width=True)

risk_df = pd.DataFrame({
    "Risk Type": ["Physical Risk", "Transition Risk"],
    "Score": [filtered_df['Physical_Risk'].values[0], filtered_df['Transition_Risk'].values[0]]
})
st.plotly_chart(px.bar(risk_df, x="Risk Type", y="Score", title="Climate Risk Comparison"), use_container_width=True)

st.subheader("🌱 Net Zero Progress Tracker")
st.progress(76 / 100)
st.write("Current Net Zero Alignment Progress: 76%")

fig5 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=filtered_df['ESG_Score'].values[0],
    title={'text': "ESG Performance"},
    gauge={'axis': {'range': [0, 100]}}
))
st.plotly_chart(fig5, use_container_width=True)
st.caption("Built using Python, Streamlit, Pandas & Plotly")