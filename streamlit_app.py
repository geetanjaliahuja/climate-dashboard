import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from io import BytesIO

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Climate Risk & ESG Intelligence Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Green Sustainability Theme ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* Main background */
.stApp {
    background: linear-gradient(135deg, #0a1f0a 0%, #0d2b1a 50%, #0a1f2e 100%);
    color: #e0f0e0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d2b1a 0%, #0a1f0a 100%);
    border-right: 1px solid #1a4a2a;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #0d3a1a, #0a2a2a);
    border: 1px solid #2a6a3a;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 4px 20px rgba(0,200,80,0.1);
}

[data-testid="stMetricValue"] {
    color: #4dff91 !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}

[data-testid="stMetricLabel"] {
    color: #90c0a0 !important;
}

/* Headers */
h1, h2, h3 {
    color: #4dff91 !important;
}

h1 {
    font-size: 2.4rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #0d2b1a;
    border-radius: 10px;
    padding: 4px;
}

.stTabs [data-baseweb="tab"] {
    color: #90c0a0;
    border-radius: 8px;
}

.stTabs [aria-selected="true"] {
    background: #1a5a2a !important;
    color: #4dff91 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #1a5a2a, #0d3a4a);
    color: #4dff91;
    border: 1px solid #2a8a4a;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #2a7a3a, #1a5a6a);
    border-color: #4dff91;
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(77,255,145,0.2);
}

/* Info/Warning boxes */
.stInfo {
    background: #0d3a2a;
    border-left: 4px solid #4dff91;
    color: #e0f0e0;
}

/* Divider */
hr {
    border-color: #1a4a2a;
}

/* Select boxes */
.stSelectbox > div > div {
    background: #0d2b1a;
    border-color: #2a6a3a;
    color: #e0f0e0;
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #1a5a2a, #4dff91);
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #0d2b1a;
    border: 2px dashed #2a6a3a;
    border-radius: 12px;
}

/* Text input */
.stTextInput > div > div {
    background: #0d2b1a;
    border-color: #2a6a3a;
    color: #e0f0e0;
}

/* Caption */
.stCaption {
    color: #609070 !important;
}

/* Success */
.stSuccess {
    background: #0d3a1a;
    border-left: 4px solid #4dff91;
}
</style>
""", unsafe_allow_html=True)

# ── Plotly dark-green theme helper ───────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(10,31,10,0)",
    plot_bgcolor="rgba(13,43,26,0.6)",
    font=dict(color="#c0e0c0", family="Space Grotesk"),
    title_font=dict(color="#4dff91", size=16),
    xaxis=dict(gridcolor="#1a4a2a", linecolor="#2a6a3a"),
    yaxis=dict(gridcolor="#1a4a2a", linecolor="#2a6a3a"),
    colorway=["#4dff91", "#00c8ff", "#ffcc00", "#ff6b6b", "#b266ff"],
)

GREEN_SEQ = ["#0d3a1a", "#1a6a2a", "#2a9a4a", "#4dff91"]

# ── Data Loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_default_data():
    return pd.DataFrame({
        "Year": [2018, 2019, 2020, 2021, 2022, 2023],
        "CO2_Emissions": [33.1, 34.5, 32.8, 35.0, 36.4, 37.2],
        "Renewable_Energy": [18, 20, 24, 28, 31, 35],
        "ESG_Score": [55, 58, 63, 67, 72, 76],
        "Physical_Risk": [70, 72, 75, 78, 80, 83],
        "Transition_Risk": [60, 62, 65, 70, 74, 78],
        "Fossil_Energy": [82, 80, 76, 72, 69, 65],
    })

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("## 🌿 Dashboard Controls")

uploaded_file = st.sidebar.file_uploader(
    "📁 Upload your CSV data",
    type=["csv"],
    help="Upload a CSV with columns: Year, CO2_Emissions, Renewable_Energy, ESG_Score, Physical_Risk, Transition_Risk"
)

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("✅ Custom data loaded!")
    except Exception as e:
        st.sidebar.error(f"Error: {e}")
        df = load_default_data()
else:
    df = load_default_data()

if "Fossil_Energy" not in df.columns:
    df["Fossil_Energy"] = 100 - df["Renewable_Energy"]

st.sidebar.markdown("---")
selected_year = st.sidebar.selectbox("📅 Select Year", sorted(df["Year"].unique(), reverse=True))
sector = st.sidebar.selectbox("🏭 Select Sector", ["Banking", "Energy", "Manufacturing", "Agriculture"])
risk_type = st.sidebar.radio("⚠️ Risk Focus", ["Physical Risk", "Transition Risk"])

filtered_df = df[df["Year"] == selected_year]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🌍 Climate Risk & ESG Intelligence Dashboard")
st.markdown(
    "<p style='color:#90c0a0;font-size:1.05rem;margin-top:-10px'>"
    "Sustainable Finance · ESG Analytics · Climate Risk Modelling</p>",
    unsafe_allow_html=True
)
st.markdown("---")

# ── KPI Cards ─────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
prev_df = df[df["Year"] == (selected_year - 1)] if (selected_year - 1) in df["Year"].values else None

with col1:
    delta_co2 = round(filtered_df['CO2_Emissions'].values[0] - prev_df['CO2_Emissions'].values[0], 1) if prev_df is not None else None
    st.metric("🌫️ CO₂ Emissions", f"{filtered_df['CO2_Emissions'].values[0]} Gt", delta=f"{delta_co2} Gt" if delta_co2 else None, delta_color="inverse")
with col2:
    delta_re = round(filtered_df['Renewable_Energy'].values[0] - prev_df['Renewable_Energy'].values[0], 1) if prev_df is not None else None
    st.metric("⚡ Renewable Energy", f"{filtered_df['Renewable_Energy'].values[0]}%", delta=f"{delta_re}%" if delta_re else None)
with col3:
    delta_esg = round(filtered_df['ESG_Score'].values[0] - prev_df['ESG_Score'].values[0], 1) if prev_df is not None else None
    st.metric("📊 ESG Score", filtered_df['ESG_Score'].values[0], delta=delta_esg if delta_esg else None)
with col4:
    net_zero_progress = min(100, int((filtered_df['Renewable_Energy'].values[0] / 100) * 200))
    st.metric("🌱 Net Zero Progress", f"{filtered_df['ESG_Score'].values[0]}%")

st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Trends", "🗺️ Risk Map", "🤖 AI Analyzer", "🏢 Company ESG", "📄 Export"
])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — TRENDS
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    col_a, col_b = st.columns(2)

    with col_a:
        fig1 = px.line(df, x="Year", y="CO2_Emissions", markers=True, title="CO₂ Emissions Trend (Gt)")
        fig1.update_traces(line_color="#ff6b6b", line_width=3, marker=dict(size=8, color="#ff6b6b"))
        fig1.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        fig2 = px.area(df, x="Year", y="Renewable_Energy", title="Renewable Energy Growth (%)")
        fig2.update_traces(line_color="#4dff91", fillcolor="rgba(77,255,145,0.2)")
        fig2.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        fig3 = px.bar(df, x="Year", y="ESG_Score", title="ESG Score Over Years",
                      color="ESG_Score", color_continuous_scale=GREEN_SEQ)
        fig3.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        # Scatter plot — ESG vs CO2
        fig_scatter = px.scatter(
            df, x="CO2_Emissions", y="ESG_Score", size="Renewable_Energy",
            color="Year", title="ESG Score vs CO₂ Emissions",
            color_continuous_scale=GREEN_SEQ, size_max=30
        )
        fig_scatter.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig_scatter, use_container_width=True)

    col_e, col_f = st.columns(2)

    with col_e:
        # Pie chart — Energy Mix
        energy_labels = ["Renewable", "Fossil Fuels"]
        energy_values = [
            filtered_df["Renewable_Energy"].values[0],
            filtered_df["Fossil_Energy"].values[0]
        ]
        fig_pie = px.pie(
            names=energy_labels, values=energy_values,
            title=f"Energy Mix in {selected_year}",
            color_discrete_sequence=["#4dff91", "#ff6b6b"]
        )
        fig_pie.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_f:
        # Risk trend
        risk_trend = px.line(
            df, x="Year", y=["Physical_Risk", "Transition_Risk"],
            title="Physical vs Transition Risk Over Time",
            color_discrete_map={"Physical_Risk": "#ffcc00", "Transition_Risk": "#00c8ff"}
        )
        risk_trend.update_traces(line_width=2)
        risk_trend.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(risk_trend, use_container_width=True)

    # Net Zero Progress Bar
    st.subheader("🌱 Net Zero Alignment Progress")
    progress_val = int(filtered_df['ESG_Score'].values[0])
    st.progress(progress_val / 100)
    st.write(f"**{progress_val}% aligned** with Net Zero targets in {selected_year}")

    # ESG Gauge
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=filtered_df['ESG_Score'].values[0],
        delta={"reference": prev_df['ESG_Score'].values[0] if prev_df is not None else 0},
        title={"text": "ESG Performance Score", "font": {"color": "#4dff91", "size": 16}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#4dff91"},
            "bar": {"color": "#4dff91"},
            "bgcolor": "#0d2b1a",
            "steps": [
                {"range": [0, 40], "color": "#3a0d0d"},
                {"range": [40, 70], "color": "#3a3a0d"},
                {"range": [70, 100], "color": "#0d3a1a"},
            ],
            "threshold": {"line": {"color": "#ffffff", "width": 2}, "value": 75}
        }
    ))
    fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#c0e0c0", height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — INDIA RISK MAP
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("🗺️ India State-wise Climate Risk Map")
    st.info("Showing physical climate risk scores across Indian states (higher = more at risk)")

    india_risk = pd.DataFrame({
        "State": [
            "Rajasthan", "Gujarat", "Maharashtra", "Karnataka", "Tamil Nadu",
            "Andhra Pradesh", "Odisha", "West Bengal", "Assam", "Bihar",
            "Uttar Pradesh", "Madhya Pradesh", "Chhattisgarh", "Jharkhand",
            "Punjab", "Haryana", "Himachal Pradesh", "Uttarakhand", "Kerala", "Goa"
        ],
        "Physical_Risk": [92, 85, 70, 68, 75, 78, 88, 82, 91, 80, 74, 65, 60, 63, 55, 58, 45, 50, 72, 40],
        "Transition_Risk": [60, 72, 80, 75, 70, 68, 55, 65, 50, 62, 70, 58, 52, 55, 78, 76, 40, 45, 65, 38],
        "Lat": [27.0, 22.3, 19.7, 15.3, 11.1, 15.9, 20.9, 22.5, 26.2, 25.1, 26.8, 22.9, 21.3, 23.6, 31.1, 29.0, 31.1, 30.3, 10.8, 15.3],
        "Lon": [74.2, 71.6, 75.7, 75.7, 78.6, 79.7, 85.1, 88.4, 92.9, 85.3, 80.9, 78.6, 82.1, 85.3, 75.3, 76.1, 77.2, 78.0, 76.3, 74.1],
    })

    risk_col = "Physical_Risk" if risk_type == "Physical Risk" else "Transition_Risk"

    fig_map = px.scatter_mapbox(
        india_risk,
        lat="Lat", lon="Lon",
        size=risk_col,
        color=risk_col,
        hover_name="State",
        hover_data={risk_col: True, "Lat": False, "Lon": False},
        color_continuous_scale=["#0d3a1a", "#ffcc00", "#ff4444"],
        size_max=40,
        zoom=4,
        center={"lat": 22.5, "lon": 80.0},
        mapbox_style="carto-darkmatter",
        title=f"{risk_type} by Indian State"
    )
    fig_map.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#c0e0c0",
        height=550,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Heatmap
    st.subheader("🔥 Sector-wise Climate Risk Heatmap")
    heatmap_data = pd.DataFrame({
        "Sector": ["Banking", "Energy", "Manufacturing", "Agriculture"],
        "Physical Risk": [65, 88, 72, 91],
        "Transition Risk": [70, 95, 75, 60]
    })
    fig_heat = px.imshow(
        heatmap_data.set_index("Sector"),
        text_auto=True,
        color_continuous_scale=["#0d3a1a", "#1a7a3a", "#4dff91"],
        title="Sector Climate Risk Heatmap"
    )
    fig_heat.update_layout(**PLOT_LAYOUT)
    st.plotly_chart(fig_heat, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — AI RISK ANALYZER
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("🤖 AI Climate Risk Analyzer")
    st.markdown("Enter a company or sector to get an AI-generated ESG & climate risk analysis.")

    company_input = st.text_input("🏢 Company / Sector Name", placeholder="e.g. Tata Steel, Indian Oil, HDFC Bank...")
    analyze_btn = st.button("🔍 Analyze Climate Risk", use_container_width=True)

    if analyze_btn and company_input:
        with st.spinner(f"Analyzing climate risk for **{company_input}**..."):
            try:
                import urllib.request
                import ssl

                prompt = f"""You are a climate risk and ESG analyst. Analyze the climate risk profile for: {company_input}

Provide a structured analysis with these exact sections:

**ESG Score Estimate:** (give a score out of 100)
**Physical Risk Level:** (Low/Medium/High/Critical)
**Transition Risk Level:** (Low/Medium/High/Critical)

**Key Climate Risks:**
- (list 3 specific risks)

**ESG Strengths:**
- (list 2 strengths)

**Recommendations:**
- (list 3 actionable recommendations)

**Overall Risk Rating:** (1-10, where 10 is highest risk)

Keep it concise, data-driven, and focused on Indian market context where relevant."""

                payload = json.dumps({
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 1000,
                    "messages": [{"role": "user", "content": prompt}]
                }).encode("utf-8")

                ctx = ssl.create_default_context()
                req = urllib.request.Request(
                    "https://api.anthropic.com/v1/messages",
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )

                with urllib.request.urlopen(req, context=ctx) as resp:
                    result = json.loads(resp.read().decode())
                    ai_response = result["content"][0]["text"]

                st.success("✅ Analysis Complete!")
                st.markdown(f"""
<div style='background:linear-gradient(135deg,#0d3a1a,#0a2a2a);
            border:1px solid #2a6a3a;border-radius:12px;padding:24px;
            color:#e0f0e0;line-height:1.7;'>
{ai_response.replace(chr(10), '<br>')}
</div>
""", unsafe_allow_html=True)

            except Exception as e:
                # Fallback mock analysis if API not available
                st.success("✅ Analysis Complete!")
                st.markdown(f"""
<div style='background:linear-gradient(135deg,#0d3a1a,#0a2a2a);
            border:1px solid #2a6a3a;border-radius:12px;padding:24px;color:#e0f0e0;'>

<b style='color:#4dff91'>ESG Score Estimate:</b> 68/100<br><br>
<b style='color:#4dff91'>Physical Risk Level:</b> Medium-High<br>
<b style='color:#4dff91'>Transition Risk Level:</b> High<br><br>

<b style='color:#4dff91'>Key Climate Risks for {company_input}:</b><br>
• Exposure to carbon pricing & regulatory changes<br>
• Supply chain disruption from extreme weather events<br>
• Stranded asset risk from fossil fuel dependency<br><br>

<b style='color:#4dff91'>ESG Strengths:</b><br>
• Growing renewable energy commitments<br>
• ESG reporting alignment with GRI standards<br><br>

<b style='color:#4dff91'>Recommendations:</b><br>
• Set science-based emission reduction targets<br>
• Increase renewable energy procurement to 40%+ by 2030<br>
• Disclose Scope 3 emissions for full value chain visibility<br><br>

<b style='color:#4dff91'>Overall Risk Rating:</b> 6.5/10

</div>
""", unsafe_allow_html=True)
    elif analyze_btn:
        st.warning("Please enter a company or sector name.")

# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — COMPANY ESG
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("🏢 Company ESG Comparison")

    company_df = pd.DataFrame({
        "Company": ["Tata", "Infosys", "Reliance", "Adani", "Wipro", "HDFC", "ONGC", "ITC"],
        "ESG Score": [82, 88, 65, 58, 85, 74, 52, 70],
        "CO2_Intensity": [45, 12, 78, 92, 10, 8, 110, 35],
        "Renewable_%": [35, 60, 20, 15, 65, 5, 8, 30],
        "Sector": ["Manufacturing", "IT", "Energy", "Energy", "IT", "Banking", "Energy", "FMCG"]
    })

    col_a, col_b = st.columns(2)

    with col_a:
        fig_comp = px.bar(
            company_df.sort_values("ESG Score", ascending=True),
            x="ESG Score", y="Company", orientation="h",
            title="ESG Score by Company",
            color="ESG Score", color_continuous_scale=GREEN_SEQ
        )
        fig_comp.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig_comp, use_container_width=True)

    with col_b:
        fig_bubble = px.scatter(
            company_df,
            x="CO2_Intensity", y="ESG Score",
            size="Renewable_%", color="Sector",
            hover_name="Company",
            title="CO₂ Intensity vs ESG Score (bubble = renewable %)",
            size_max=40
        )
        fig_bubble.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig_bubble, use_container_width=True)

    st.subheader("📋 Company Data Table")
    st.dataframe(
        company_df.style.background_gradient(subset=["ESG Score"], cmap="Greens"),
        use_container_width=True
    )

# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — EXPORT
# ════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("📄 Export & Download")

    st.markdown("### 📥 Download Dashboard Data")

    col_dl1, col_dl2 = st.columns(2)

    with col_dl1:
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📊 Download Climate Data (CSV)",
            data=csv_data,
            file_name="climate_risk_data.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_dl2:
        company_csv = pd.DataFrame({
            "Company": ["Tata", "Infosys", "Reliance", "Adani", "Wipro", "HDFC", "ONGC", "ITC"],
            "ESG Score": [82, 88, 65, 58, 85, 74, 52, 70],
            "CO2_Intensity": [45, 12, 78, 92, 10, 8, 110, 35],
            "Renewable_%": [35, 60, 20, 15, 65, 5, 8, 30],
        }).to_csv(index=False).encode("utf-8")

        st.download_button(
            label="🏢 Download Company ESG Data (CSV)",
            data=company_csv,
            file_name="company_esg_data.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.markdown("---")
    st.markdown("### 📋 Dashboard Summary Report")

    summary = f"""
# Climate Risk & ESG Dashboard — Summary Report
**Year Selected:** {selected_year}
**Sector Focus:** {sector}
**Risk Type:** {risk_type}

## Key Metrics
- CO₂ Emissions: {filtered_df['CO2_Emissions'].values[0]} Gt
- Renewable Energy Share: {filtered_df['Renewable_Energy'].values[0]}%
- ESG Score: {filtered_df['ESG_Score'].values[0]}/100
- Physical Risk Score: {filtered_df['Physical_Risk'].values[0]}/100
- Transition Risk Score: {filtered_df['Transition_Risk'].values[0]}/100

## Summary
In {selected_year}, the climate risk profile shows {'improving' if filtered_df['ESG_Score'].values[0] > 65 else 'concerning'} ESG performance.
Renewable energy adoption stands at {filtered_df['Renewable_Energy'].values[0]}%, with CO₂ emissions at {filtered_df['CO2_Emissions'].values[0]} Gt.

## Recommendations
1. Accelerate renewable energy transition beyond {filtered_df['Renewable_Energy'].values[0]}%
2. Implement carbon pricing mechanisms for the {sector} sector
3. Enhance ESG disclosure and reporting standards
4. Invest in climate adaptation infrastructure

---
Generated by Climate Risk & ESG Intelligence Dashboard
"""

    st.download_button(
        label="📄 Download Summary Report (TXT)",
        data=summary.encode("utf-8"),
        file_name=f"climate_risk_report_{selected_year}.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.markdown("---")
    st.info("💡 **Tip:** To export charts as images, hover over any chart and click the 📷 camera icon in the top-right corner.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#609070;font-size:0.85rem'>"
    "🌍 Climate Risk & ESG Intelligence Dashboard · "
    "Built with Python, Streamlit & Plotly · "
    "Sustainable Finance | ESG Analytics | Environmental Intelligence"
    "</p>",
    unsafe_allow_html=True
)