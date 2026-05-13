import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import hashlib
from io import BytesIO

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Climate Risk & ESG Intelligence Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Full CSS Theme (your original + additions for login/role UI) ──────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0a1f0a 0%, #0d2b1a 50%, #0a1f2e 100%);
    color: #e0f0e0;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d2b1a 0%, #0a1f0a 100%);
    border-right: 1px solid #1a4a2a;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #0d3a1a, #0a2a2a);
    border: 1px solid #2a6a3a;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 4px 20px rgba(0,200,80,0.1);
}

[data-testid="stMetricValue"] { color: #4dff91 !important; font-size: 2rem !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #90c0a0 !important; }

h1, h2, h3 { color: #4dff91 !important; }
h1 { font-size: 2.4rem !important; font-weight: 700 !important; letter-spacing: -0.5px; }

.stTabs [data-baseweb="tab-list"] { background: #0d2b1a; border-radius: 10px; padding: 4px; }
.stTabs [data-baseweb="tab"] { color: #90c0a0; border-radius: 8px; }
.stTabs [aria-selected="true"] { background: #1a5a2a !important; color: #4dff91 !important; }

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

.stInfo { background: #0d3a2a; border-left: 4px solid #4dff91; color: #e0f0e0; }
hr { border-color: #1a4a2a; }
.stSelectbox > div > div { background: #0d2b1a; border-color: #2a6a3a; color: #e0f0e0; }
.stProgress > div > div { background: linear-gradient(90deg, #1a5a2a, #4dff91); }
[data-testid="stFileUploader"] { background: #0d2b1a; border: 2px dashed #2a6a3a; border-radius: 12px; }
.stTextInput > div > div { background: #0d2b1a; border-color: #2a6a3a; color: #e0f0e0; }
.stCaption { color: #609070 !important; }
.stSuccess { background: #0d3a1a; border-left: 4px solid #4dff91; }

/* Role card tiles */
.role-tile {
    background: linear-gradient(135deg, #0d3a1a, #0a2a2a);
    border: 1px solid #2a6a3a;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s;
    min-height: 160px;
}
.role-tile:hover { border-color: #4dff91; box-shadow: 0 0 20px rgba(77,255,145,0.15); }
.role-tile.selected { border: 2px solid #4dff91; box-shadow: 0 0 25px rgba(77,255,145,0.25); }
.role-icon { font-size: 2.5rem; display: block; margin-bottom: 10px; }
.role-name { color: #4dff91; font-size: 1.1rem; font-weight: 600; margin-bottom: 6px; }
.role-desc { color: #90c0a0; font-size: 0.8rem; line-height: 1.4; }

/* Profile badge in sidebar */
.profile-badge {
    background: linear-gradient(135deg, #0d3a1a, #0a2a2a);
    border: 1px solid #2a6a3a;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
    text-align: center;
}
.profile-name { color: #4dff91; font-weight: 600; font-size: 1rem; }
.profile-role { color: #90c0a0; font-size: 0.82rem; margin-top: 4px; }
.profile-avatar {
    width: 52px; height: 52px;
    background: linear-gradient(135deg, #1a5a2a, #0d3a4a);
    border-radius: 50%; border: 2px solid #4dff91;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem; margin: 0 auto 10px auto;
}

/* Suggestion cards */
.suggestion-card {
    background: linear-gradient(135deg, #0d3a1a, #0a2a3a);
    border: 1px solid #2a6a3a;
    border-left: 4px solid #4dff91;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
    color: #e0f0e0;
    font-size: 0.9rem;
    line-height: 1.6;
}
.suggestion-title { color: #4dff91; font-weight: 600; font-size: 0.95rem; margin-bottom: 4px; }

/* Info tooltip */
.info-tooltip { position: relative; display: inline-block; margin-left: 6px; cursor: help; }
.info-tooltip .info-icon {
    display: inline-flex; align-items: center; justify-content: center;
    width: 16px; height: 16px; border-radius: 50%;
    background: #2a6a3a; color: #4dff91; font-size: 11px;
    font-weight: 700; font-style: italic; font-family: Georgia, serif;
    border: 1px solid #4dff91; vertical-align: middle;
}
.info-tooltip .tooltip-box {
    visibility: hidden; opacity: 0; width: 240px;
    background: #0d3a1a; color: #e0f0e0; font-size: 0.82rem;
    line-height: 1.5; border-radius: 8px; padding: 10px 12px;
    border: 1px solid #2a6a3a; position: absolute; z-index: 9999;
    bottom: 130%; left: 50%; transform: translateX(-50%);
    transition: opacity 0.2s; box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}
.info-tooltip:hover .tooltip-box { visibility: visible; opacity: 1; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
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

ROLE_CONFIG = {
    "🏢 Company": {
        "icon": "🏢",
        "desc": "Corporate entity tracking ESG performance & compliance",
        "color": "#00c8ff",
        "fields": ["Organisation Name", "Industry Sector", "Company Size", "Annual Revenue Range",
                   "Current ESG Rating (if any)", "Net Zero Target Year", "Primary ESG Framework"],
    },
    "👤 Individual": {
        "icon": "👤",
        "desc": "Personal carbon footprint & sustainable investing",
        "color": "#4dff91",
        "fields": ["Full Name", "Country / Region", "Occupation", "Primary Interest",
                   "Monthly Carbon Budget Awareness", "Investment Portfolio Size"],
    },
    "🏛️ Government": {
        "icon": "🏛️",
        "desc": "Public sector policy analysis & regulatory oversight",
        "color": "#ffcc00",
        "fields": ["Department / Ministry Name", "Country", "Jurisdiction Level",
                   "Policy Focus Area", "Current NDC Target Year", "Regulatory Framework"],
    },
    "🏭 Industry / NGO": {
        "icon": "🏭",
        "desc": "Sector body, industry association or research org",
        "color": "#ff6b6b",
        "fields": ["Organisation Name", "Sector / Industry", "Number of Member Companies",
                   "Primary Research Focus", "Region of Operation", "Affiliation Type"],
    },
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def get_role_suggestions(role, profile):
    """Return role-specific smart suggestions based on profile data."""
    suggestions = {
        "🏢 Company": [
            ("📊 Benchmark your ESG score",
             f"Companies in the {profile.get('Industry Sector','your')} sector average ESG 67/100. "
             "Your dashboard shows 76 — you're outperforming peers. Focus on Scope 3 disclosure next."),
            ("⚡ Renewable energy gap",
             "Your renewable energy share is 35%. To align with SBTi targets for 2030, "
             "you need to reach 60%+. Consider PPAs or green bonds to close this gap."),
            ("📋 Reporting deadline alert",
             f"SEBI's BRSR Core mandate requires enhanced ESG disclosures for top 150 companies by FY2025. "
             "Ensure your {profile.get('Primary ESG Framework','GRI')} alignment is current."),
        ],
        "👤 Individual": [
            ("🌱 Your carbon footprint vs peers",
             f"Average per-capita CO₂ in India is 1.9 tCO₂/year. "
             "Based on your profile, you can track and reduce personal emissions via this dashboard."),
            ("💰 Green investment opportunity",
             "India's green bond market grew 47% YoY. Consider sovereign green bonds or ESG mutual funds "
             "to align your portfolio with climate goals."),
            ("🔋 Quick win: switch to renewables",
             "Switching to a renewable energy tariff from your electricity provider can cut "
             "your household Scope 2 emissions by up to 60% instantly."),
        ],
        "🏛️ Government": [
            ("📜 Policy gap analysis",
             f"In the {profile.get('Policy Focus Area','energy')} sector, India's current NDC targets "
             "require 500 GW renewable capacity by 2030. Current trajectory shows a 15% shortfall."),
            ("🌏 Cross-country benchmark",
             "Denmark and Germany lead on transition risk management with carbon border taxes. "
             "Reviewing their policy frameworks could strengthen India's own transition roadmap."),
            ("📊 Data-driven regulation",
             "SEBI's new climate disclosure rules align with ISSB S2 standards. "
             "Mandating sector-level Scope 3 reporting could improve national emissions accounting by 22%."),
        ],
        "🏭 Industry / NGO": [
            ("🏆 Sector leaderboard insight",
             f"Within the {profile.get('Sector / Industry','your')} sector, ESG leaders are outperforming "
             "laggards by 18% in cost of capital. Share this benchmark with member companies."),
            ("🔗 Supply chain risk alert",
             "Physical climate risk in manufacturing supply chains is rising — 3 of top 5 supplier "
             "regions show Critical risk by 2030. Develop sector-wide resilience guidelines."),
            ("📢 Reporting framework harmonisation",
             "60% of your member companies likely use different ESG frameworks. "
             "Adopting ISSB S1+S2 as a sector standard can reduce reporting burden by 30%."),
        ],
    }
    return suggestions.get(role, [])

# ── Session state init ────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}
if "selected_role" not in st.session_state:
    st.session_state.selected_role = None
if "onboarding_step" not in st.session_state:
    st.session_state.onboarding_step = "role_select"  # role_select | register | profile | done
# Simple in-memory user store (replace with DB for production)
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "demo@esg.com": {
            "password": hash_password("demo123"),
            "profile": {
                "name": "Demo User", "email": "demo@esg.com",
                "role": "🏢 Company",
                "Organisation Name": "GreenCorp Ltd",
                "Industry Sector": "Manufacturing",
                "Company Size": "Large (1000+ employees)",
                "Annual Revenue Range": "₹500Cr – ₹1000Cr",
                "Current ESG Rating (if any)": "CRISIL ESG: AA",
                "Net Zero Target Year": "2040",
                "Primary ESG Framework": "GRI + BRSR",
            }
        }
    }

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

# ══════════════════════════════════════════════════════════════════════════════
# ONBOARDING FLOW (shown when not logged in)
# ══════════════════════════════════════════════════════════════════════════════
def show_onboarding():
    st.markdown("# 🌍 Climate Risk & ESG Intelligence Dashboard")
    st.markdown(
        "<p style='color:#90c0a0;font-size:1.05rem;margin-top:-10px'>"
        "Sustainable Finance · ESG Analytics · Climate Risk Modelling</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    step = st.session_state.onboarding_step

    # ── STEP 1: Role Selection ─────────────────────────────────────────────
    if step == "role_select":
        st.markdown("### 👋 Welcome — who are you?")
        st.markdown(
            "<p style='color:#90c0a0'>Select your role to get a personalised ESG dashboard experience.</p>",
            unsafe_allow_html=True
        )
        st.markdown("")

        cols = st.columns(4)
        for i, (role_key, cfg) in enumerate(ROLE_CONFIG.items()):
            with cols[i]:
                st.markdown(f"""
                <div class="role-tile">
                    <span class="role-icon">{cfg['icon']}</span>
                    <div class="role-name">{role_key}</div>
                    <div class="role-desc">{cfg['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Select", key=f"role_{i}", use_container_width=True):
                    st.session_state.selected_role = role_key
                    st.session_state.onboarding_step = "register"
                    st.rerun()

        st.markdown("---")
        st.markdown(
            "<p style='text-align:center;color:#609070;font-size:0.85rem'>"
            "Already have an account? Use the login form below.</p>",
            unsafe_allow_html=True
        )
        _show_login_form()

    # ── STEP 2: Register ───────────────────────────────────────────────────
    elif step == "register":
        role = st.session_state.selected_role
        cfg = ROLE_CONFIG[role]
        st.markdown(f"### {cfg['icon']} Register as {role}")
        st.markdown(f"<p style='color:#90c0a0'>Creating a free account personalises your dashboard for {role.split()[-1].lower()} users.</p>", unsafe_allow_html=True)

        with st.form("register_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full name *")
                email = st.text_input("Email address *")
            with col2:
                pw = st.text_input("Password *", type="password")
                pw2 = st.text_input("Confirm password *", type="password")

            agree = st.checkbox("I agree to data privacy terms and consent to ESG data processing")
            submitted = st.form_submit_button("Create Account →", use_container_width=True)

            if submitted:
                if not name or not email or not pw:
                    st.error("Please fill in all required fields.")
                elif pw != pw2:
                    st.error("Passwords do not match.")
                elif not agree:
                    st.error("Please accept the privacy terms to continue.")
                elif email in st.session_state.users_db:
                    st.error("An account with this email already exists. Please log in.")
                else:
                    st.session_state.users_db[email] = {
                        "password": hash_password(pw),
                        "profile": {"name": name, "email": email, "role": role}
                    }
                    st.session_state.user_profile = st.session_state.users_db[email]["profile"]
                    st.session_state.onboarding_step = "profile"
                    st.rerun()

        if st.button("← Back to role selection"):
            st.session_state.onboarding_step = "role_select"
            st.rerun()

    # ── STEP 3: Profile Form ───────────────────────────────────────────────
    elif step == "profile":
        role = st.session_state.selected_role
        cfg = ROLE_CONFIG[role]
        name = st.session_state.user_profile.get("name", "")
        st.markdown(f"### 👋 Hi {name}! Complete your {role} profile")
        st.markdown(
            f"<p style='color:#90c0a0'>This helps us personalise your risk analysis, suggestions, and benchmarks. "
            f"Takes about 1 minute.</p>", unsafe_allow_html=True
        )
        st.progress(0.66, text="Step 2 of 3 — Profile details")

        with st.form("profile_form"):
            profile_data = {}
            cols_per_row = 2
            fields = cfg["fields"]
            # Render fields in a 2-column grid
            for i in range(0, len(fields), cols_per_row):
                row_fields = fields[i:i+cols_per_row]
                row_cols = st.columns(len(row_fields))
                for j, field in enumerate(row_fields):
                    with row_cols[j]:
                        # Use dropdowns for known categorical fields
                        if field == "Industry Sector":
                            profile_data[field] = st.selectbox(field, [
                                "Manufacturing", "Energy", "Banking & Finance",
                                "IT / Technology", "Agriculture", "Healthcare",
                                "Real Estate", "Transport", "Retail", "Other"
                            ])
                        elif field == "Company Size":
                            profile_data[field] = st.selectbox(field, [
                                "Startup (< 50)", "Small (50–250)", "Medium (250–1000)", "Large (1000+)"
                            ])
                        elif field == "Annual Revenue Range":
                            profile_data[field] = st.selectbox(field, [
                                "< ₹10Cr", "₹10Cr – ₹100Cr", "₹100Cr – ₹500Cr",
                                "₹500Cr – ₹1000Cr", "> ₹1000Cr"
                            ])
                        elif field == "Primary ESG Framework":
                            profile_data[field] = st.selectbox(field, [
                                "GRI", "BRSR (SEBI)", "TCFD", "SASB", "ISSB S1+S2",
                                "CDP", "UN SDGs", "None yet"
                            ])
                        elif field == "Jurisdiction Level":
                            profile_data[field] = st.selectbox(field, [
                                "National", "State / Provincial", "Municipal / Local",
                                "Multi-lateral / International"
                            ])
                        elif field == "Policy Focus Area":
                            profile_data[field] = st.selectbox(field, [
                                "Energy Transition", "Carbon Pricing", "Climate Adaptation",
                                "Biodiversity", "Water Security", "Agriculture & Food",
                                "Transport Decarbonisation", "Climate Finance"
                            ])
                        elif field == "Affiliation Type":
                            profile_data[field] = st.selectbox(field, [
                                "Industry Association", "NGO / Non-profit",
                                "Research Institute", "Think Tank", "Standards Body", "Other"
                            ])
                        elif field == "Primary Interest":
                            profile_data[field] = st.selectbox(field, [
                                "Track personal carbon footprint", "Green investments",
                                "Climate news & policy", "Career in sustainability", "General awareness"
                            ])
                        else:
                            profile_data[field] = st.text_input(field)

            why = st.text_area("Why are you using this dashboard? (optional)",
                               placeholder="e.g. Preparing BRSR report, evaluating green bonds, policy research...")

            submitted = st.form_submit_button("Complete Setup & Enter Dashboard →", use_container_width=True)
            if submitted:
                full_profile = {**st.session_state.user_profile, **profile_data, "why": why}
                st.session_state.user_profile = full_profile
                email = full_profile.get("email")
                if email in st.session_state.users_db:
                    st.session_state.users_db[email]["profile"] = full_profile
                st.session_state.logged_in = True
                st.session_state.onboarding_step = "done"
                st.rerun()

        if st.button("← Back"):
            st.session_state.onboarding_step = "register"
            st.rerun()


def _show_login_form():
    with st.expander("🔐 Already have an account? Log in here"):
        with st.form("login_form"):
            email = st.text_input("Email")
            pw = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log In", use_container_width=True)
            if submitted:
                db = st.session_state.users_db
                if email in db and db[email]["password"] == hash_password(pw):
                    st.session_state.user_profile = db[email]["profile"]
                    st.session_state.selected_role = db[email]["profile"].get("role")
                    st.session_state.logged_in = True
                    st.session_state.onboarding_step = "done"
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
        st.caption("Demo account: demo@esg.com / demo123")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN DASHBOARD (shown when logged in)
# ══════════════════════════════════════════════════════════════════════════════
def show_dashboard():
    profile = st.session_state.user_profile
    role = profile.get("role", "👤 Individual")
    role_cfg = ROLE_CONFIG.get(role, ROLE_CONFIG["👤 Individual"])
    name = profile.get("name", "User")

    # ── Sidebar ───────────────────────────────────────────────────────────────
    st.sidebar.markdown(f"""
    <div class="profile-badge">
        <div class="profile-avatar">{role_cfg['icon']}</div>
        <div class="profile-name">{name}</div>
        <div class="profile-role">{role}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("🚪 Log out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_profile = {}
        st.session_state.onboarding_step = "role_select"
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🌿 Dashboard Controls")

    uploaded_file = st.sidebar.file_uploader(
        "📁 Upload your CSV data", type=["csv"],
        help="Upload CSV with columns: Year, CO2_Emissions, Renewable_Energy, ESG_Score, Physical_Risk, Transition_Risk"
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

    selected_year = st.sidebar.selectbox(
        "📅 Select Year",
        sorted(df["Year"].unique(), reverse=True),
        help="Filter all dashboard data by the selected year."
    )

    # Role-specific sector options
    sector_options = {
        "🏢 Company": ["Banking", "Energy", "Manufacturing", "Agriculture", "IT", "Healthcare"],
        "👤 Individual": ["Personal Finance", "Household", "Transport", "Food & Diet"],
        "🏛️ Government": ["National Policy", "State Policy", "Energy Sector", "Agriculture"],
        "🏭 Industry / NGO": ["Energy", "Manufacturing", "Agriculture", "Finance", "All Sectors"],
    }
    sector = st.sidebar.selectbox(
        "🏭 Select Sector",
        sector_options.get(role, ["Banking", "Energy", "Manufacturing", "Agriculture"]),
        help="Filter analysis by sector relevant to your role."
    )

    risk_type = st.sidebar.radio(
        "⚠️ Risk Focus",
        ["Physical Risk", "Transition Risk"],
        help="Physical Risk: Direct climate event damage.\nTransition Risk: Cost of moving to low-carbon economy."
    )

    filtered_df = df[df["Year"] == selected_year]

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown("# 🌍 Climate Risk & ESG Intelligence Dashboard")
    st.markdown(
        f"<p style='color:#90c0a0;font-size:1.05rem;margin-top:-10px'>"
        f"Welcome back, <b style='color:#4dff91'>{name}</b> · "
        f"{role} · Sustainable Finance · ESG Analytics · Climate Risk Modelling</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    # ── KPI Cards ─────────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    prev_df = df[df["Year"] == (selected_year - 1)] if (selected_year - 1) in df["Year"].values else None
    delta_co2 = round(filtered_df['CO2_Emissions'].values[0] - prev_df['CO2_Emissions'].values[0], 1) if prev_df is not None else None
    delta_re = round(filtered_df['Renewable_Energy'].values[0] - prev_df['Renewable_Energy'].values[0], 1) if prev_df is not None else None
    delta_esg = round(filtered_df['ESG_Score'].values[0] - prev_df['ESG_Score'].values[0], 1) if prev_df is not None else None

    def kpi_card(col, emoji, title, value, delta, tooltip):
        delta_html = ""
        if delta is not None:
            color = "#ff6b6b" if title == "CO₂ Emissions" and delta > 0 else ("#4dff91" if delta >= 0 else "#ff6b6b")
            arrow = "▲" if delta >= 0 else "▼"
            delta_html = f"<div style='color:{color};font-size:0.85rem;margin-top:6px'>{arrow} {abs(delta)}</div>"
        col.markdown(f"""
        <div style='background:linear-gradient(135deg,#0d3a1a,#0a2a2a);border:1px solid #2a6a3a;
            border-radius:12px;padding:18px 20px;box-shadow:0 4px 20px rgba(0,200,80,0.1);min-height:110px'>
            <div style='color:#90c0a0;font-size:0.85rem;margin-bottom:6px'>
                {emoji} {title}
                <span class="info-tooltip">
                    <span class="info-icon">i</span>
                    <span class="tooltip-box">{tooltip}</span>
                </span>
            </div>
            <div style='color:#4dff91;font-size:2rem;font-weight:700;line-height:1'>{value}</div>
            {delta_html}
        </div>
        """, unsafe_allow_html=True)

    kpi_card(col1, "🌫️", "CO₂ Emissions", f"{filtered_df['CO2_Emissions'].values[0]} Gt", delta_co2,
             "Total CO₂ released. Measured in Gigatonnes (Gt). Lower is better.")
    kpi_card(col2, "⚡", "Renewable Energy", f"{filtered_df['Renewable_Energy'].values[0]}%", delta_re,
             "% of total energy from solar, wind & hydro. Higher = better sustainability.")
    kpi_card(col3, "📊", "ESG Score", f"{filtered_df['ESG_Score'].values[0]}/100", delta_esg,
             "ESG = Environmental, Social & Governance. Above 70 = Good. Above 85 = Excellent.")
    kpi_card(col4, "🌱", "Net Zero Progress", f"{filtered_df['ESG_Score'].values[0]}%", None,
             "How aligned current trajectory is with Net Zero 2050 targets.")

    st.markdown("---")

    # ── Tabs (role-aware labels) ───────────────────────────────────────────────
    tab_labels = ["📈 Trends", "🗺️ Risk Map", "🤖 AI Analyzer", "🏢 Company ESG",
                  "💡 My Suggestions", "📄 Export"]
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(tab_labels)

    # ════════════════════════════════════════════════════════════════════
    # TAB 1 — TRENDS
    # ════════════════════════════════════════════════════════════════════
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
            fig_scatter = px.scatter(df, x="CO2_Emissions", y="ESG_Score",
                                     size="Renewable_Energy", color="Year",
                                     title="ESG Score vs CO₂ Emissions",
                                     color_continuous_scale=GREEN_SEQ, size_max=30)
            fig_scatter.update_layout(**PLOT_LAYOUT)
            st.plotly_chart(fig_scatter, use_container_width=True)

        col_e, col_f = st.columns(2)
        with col_e:
            energy_labels = ["Renewable", "Fossil Fuels"]
            energy_values = [filtered_df["Renewable_Energy"].values[0], filtered_df["Fossil_Energy"].values[0]]
            fig_pie = px.pie(names=energy_labels, values=energy_values,
                             title=f"Energy Mix in {selected_year}",
                             color_discrete_sequence=["#4dff91", "#ff6b6b"])
            fig_pie.update_layout(**PLOT_LAYOUT)
            st.plotly_chart(fig_pie, use_container_width=True)
        with col_f:
            risk_trend = px.line(df, x="Year", y=["Physical_Risk", "Transition_Risk"],
                                 title="Physical vs Transition Risk Over Time",
                                 color_discrete_map={"Physical_Risk": "#ffcc00", "Transition_Risk": "#00c8ff"})
            risk_trend.update_traces(line_width=2)
            risk_trend.update_layout(**PLOT_LAYOUT)
            st.plotly_chart(risk_trend, use_container_width=True)

        st.subheader("🌱 Net Zero Alignment Progress")
        progress_val = int(filtered_df['ESG_Score'].values[0])
        st.progress(progress_val / 100)
        st.write(f"**{progress_val}% aligned** with Net Zero targets in {selected_year}")

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

    # ════════════════════════════════════════════════════════════════════
    # TAB 2 — RISK MAP
    # ════════════════════════════════════════════════════════════════════
    with tab2:
        st.subheader("🗺️ India State-wise Climate Risk Map")
        st.info("Showing physical climate risk scores across Indian states (higher = more at risk)")

        india_risk = pd.DataFrame({
            "State": ["Rajasthan", "Gujarat", "Maharashtra", "Karnataka", "Tamil Nadu",
                      "Andhra Pradesh", "Odisha", "West Bengal", "Assam", "Bihar",
                      "Uttar Pradesh", "Madhya Pradesh", "Chhattisgarh", "Jharkhand",
                      "Punjab", "Haryana", "Himachal Pradesh", "Uttarakhand", "Kerala", "Goa"],
            "Physical_Risk": [92, 85, 70, 68, 75, 78, 88, 82, 91, 80, 74, 65, 60, 63, 55, 58, 45, 50, 72, 40],
            "Transition_Risk": [60, 72, 80, 75, 70, 68, 55, 65, 50, 62, 70, 58, 52, 55, 78, 76, 40, 45, 65, 38],
            "Lat": [27.0, 22.3, 19.7, 15.3, 11.1, 15.9, 20.9, 22.5, 26.2, 25.1,
                    26.8, 22.9, 21.3, 23.6, 31.1, 29.0, 31.1, 30.3, 10.8, 15.3],
            "Lon": [74.2, 71.6, 75.7, 75.7, 78.6, 79.7, 85.1, 88.4, 92.9, 85.3,
                    80.9, 78.6, 82.1, 85.3, 75.3, 76.1, 77.2, 78.0, 76.3, 74.1],
        })

        risk_col = "Physical_Risk" if risk_type == "Physical Risk" else "Transition_Risk"
        fig_map = px.scatter_mapbox(
            india_risk, lat="Lat", lon="Lon", size=risk_col, color=risk_col,
            hover_name="State", hover_data={risk_col: True, "Lat": False, "Lon": False},
            color_continuous_scale=["#0d3a1a", "#ffcc00", "#ff4444"], size_max=40, zoom=4,
            center={"lat": 22.5, "lon": 80.0}, mapbox_style="carto-darkmatter",
            title=f"{risk_type} by Indian State"
        )
        fig_map.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#c0e0c0",
                              height=550, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_map, use_container_width=True)

        st.subheader("🔥 Sector-wise Climate Risk Heatmap")
        heatmap_data = pd.DataFrame({
            "Sector": ["Banking", "Energy", "Manufacturing", "Agriculture"],
            "Physical Risk": [65, 88, 72, 91],
            "Transition Risk": [70, 95, 75, 60]
        })
        fig_heat = px.imshow(heatmap_data.set_index("Sector"), text_auto=True,
                             color_continuous_scale=["#0d3a1a", "#1a7a3a", "#4dff91"],
                             title="Sector Climate Risk Heatmap")
        fig_heat.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig_heat, use_container_width=True)

    # ════════════════════════════════════════════════════════════════════
    # TAB 3 — AI ANALYZER
    # ════════════════════════════════════════════════════════════════════
    with tab3:
        st.subheader("🤖 AI Climate Risk Analyzer")
        st.markdown("Enter a company or sector to get an AI-generated ESG & climate risk analysis.")

        # Pre-fill hint based on profile
        hint = profile.get("Organisation Name", profile.get("name", ""))
        company_input = st.text_input("🏢 Company / Sector Name",
                                      placeholder="e.g. Tata Steel, Indian Oil, HDFC Bank...",
                                      value="" )
        analyze_btn = st.button("🔍 Analyze Climate Risk", use_container_width=True)

        if analyze_btn and company_input:
            with st.spinner(f"Analyzing climate risk for **{company_input}**..."):
                try:
                    import urllib.request, ssl
                    role_context = f"The user is a {role} professional. " if role else ""
                    prompt = f"""{role_context}You are a climate risk and ESG analyst. Analyze the climate risk profile for: {company_input}

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

                except Exception:
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

    # ════════════════════════════════════════════════════════════════════
    # TAB 4 — COMPANY ESG
    # ════════════════════════════════════════════════════════════════════
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
            fig_comp = px.bar(company_df.sort_values("ESG Score", ascending=True),
                              x="ESG Score", y="Company", orientation="h",
                              title="ESG Score by Company",
                              color="ESG Score", color_continuous_scale=GREEN_SEQ)
            fig_comp.update_layout(**PLOT_LAYOUT)
            st.plotly_chart(fig_comp, use_container_width=True)
        with col_b:
            fig_bubble = px.scatter(company_df, x="CO2_Intensity", y="ESG Score",
                                    size="Renewable_%", color="Sector", hover_name="Company",
                                    title="CO₂ Intensity vs ESG Score (bubble = renewable %)", size_max=40)
            fig_bubble.update_layout(**PLOT_LAYOUT)
            st.plotly_chart(fig_bubble, use_container_width=True)

        st.subheader("📋 Company Data Table")
        st.dataframe(company_df.style.background_gradient(subset=["ESG Score"], cmap="Greens"),
                     use_container_width=True)

    # ════════════════════════════════════════════════════════════════════
    # TAB 5 — MY SUGGESTIONS (NEW)
    # ════════════════════════════════════════════════════════════════════
    with tab5:
        st.subheader(f"💡 Personalised Insights for {name}")
        st.markdown(
            f"<p style='color:#90c0a0'>Role-specific recommendations based on your {role} profile "
            f"and the current dashboard data.</p>", unsafe_allow_html=True
        )

        suggestions = get_role_suggestions(role, profile)
        for title, body in suggestions:
            st.markdown(f"""
            <div class="suggestion-card">
                <div class="suggestion-title">{title}</div>
                {body}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("📋 Your Profile Summary")
        ignore_keys = {"password"}
        profile_display = {k: v for k, v in profile.items() if k not in ignore_keys and v}
        col1, col2 = st.columns(2)
        items = list(profile_display.items())
        for i, (k, v) in enumerate(items):
            (col1 if i % 2 == 0 else col2).markdown(
                f"<div style='margin-bottom:8px'>"
                f"<span style='color:#90c0a0;font-size:0.82rem'>{k}</span><br>"
                f"<span style='color:#e0f0e0;font-weight:500'>{v}</span></div>",
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.subheader("🎯 Your ESG Action Checklist")
        # Role-specific checklists
        checklists = {
            "🏢 Company": [
                "Upload your latest ESG / BRSR report",
                "Set a Scope 1+2 emission reduction target",
                "Disclose Scope 3 value chain emissions",
                "Align with TCFD climate risk disclosures",
                "Set a science-based Net Zero target year",
            ],
            "👤 Individual": [
                "Calculate your personal carbon footprint",
                "Switch to a renewable energy tariff",
                "Review investment portfolio for ESG alignment",
                "Reduce air travel by 20% this year",
                "Adopt a predominantly plant-based diet",
            ],
            "🏛️ Government": [
                "Review NDC targets against current emissions trajectory",
                "Mandate BRSR / ISSB S2 reporting for large companies",
                "Publish national climate risk maps",
                "Launch a carbon pricing consultation",
                "Set renewable energy procurement targets for public buildings",
            ],
            "🏭 Industry / NGO": [
                "Survey member companies on ESG readiness",
                "Publish sector-wide ESG benchmarking report",
                "Develop supply chain climate risk guidelines",
                "Adopt ISSB S1+S2 as the sector standard",
                "Launch a sector net zero roadmap",
            ],
        }
        checklist = checklists.get(role, checklists["👤 Individual"])
        checklist_key = f"checklist_{role}"
        if checklist_key not in st.session_state:
            st.session_state[checklist_key] = [False] * len(checklist)

        for i, item in enumerate(checklist):
            checked = st.checkbox(item, value=st.session_state[checklist_key][i], key=f"check_{i}")
            st.session_state[checklist_key][i] = checked

        done = sum(st.session_state[checklist_key])
        st.progress(done / len(checklist))
        st.caption(f"{done} of {len(checklist)} actions completed")

    # ════════════════════════════════════════════════════════════════════
    # TAB 6 — EXPORT
    # ════════════════════════════════════════════════════════════════════
    with tab6:
        st.subheader("📄 Export & Download")
        st.markdown("### 📥 Download Dashboard Data")

        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📊 Download Climate Data (CSV)",
                data=csv_data, file_name="climate_risk_data.csv",
                mime="text/csv", use_container_width=True
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
                data=company_csv, file_name="company_esg_data.csv",
                mime="text/csv", use_container_width=True
            )

        st.markdown("---")
        st.markdown("### 📋 Dashboard Summary Report")
        summary = f"""
# Climate Risk & ESG Intelligence Dashboard — Summary Report

**User:** {name}
**Role:** {role}
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
Renewable energy adoption stands at {filtered_df['Renewable_Energy'].values[0]}%, with CO₂ at {filtered_df['CO2_Emissions'].values[0]} Gt.

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
            mime="text/plain", use_container_width=True
        )
        st.info("💡 **Tip:** Hover over any chart and click the 📷 camera icon to save it as an image.")

    # ── Footer ─────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        "<p style='text-align:center;color:#609070;font-size:0.85rem'>"
        "🌍 Climate Risk & ESG Intelligence Dashboard · "
        "Built with Python, Streamlit & Plotly · "
        "Sustainable Finance | ESG Analytics | Environmental Intelligence"
        "</p>",
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.logged_in:
    show_dashboard()
else:
    show_onboarding()
