import streamlit as st

# =========================
# 🌟 Page Navigation Setup
# =========================
main_page = st.Page("businessIdeaGenerator.py", title="Business Idea Generator", icon="🚀")
page_2 = st.Page("marketingStrategyGenerator.py", title="Marketing Strategy Generator", icon="🎯")
page_3 = st.Page("customerReviewAnalyzier.py", title="Customer Review Analyzer", icon="⭐")
page_4 = st.Page("SocialMediaContentGenerator.py", title="Social Media Content Generator", icon="📱")
page_5 = st.Page("FinancialAdvisor.py", title="Financial Advisor", icon="💰")
page_6 = st.Page("testPdf.py", title="Generate PDF", icon="📄")

# Setup Navigation
pg = st.navigation([main_page, page_2, page_3, page_4, page_5, page_6])


# =========================
# 🎨 Custom Global CSS
# =========================
st.markdown("""
    <style>
    /* ========== GLOBAL APP ========== */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e293b, #334155);
        font-family: "Poppins", sans-serif;
        color: #e2e8f0;
    }

    /* ========== NAVIGATION BAR ========== */
    .stNavigation {
        background: linear-gradient(90deg, #0f172a, #1e293b, #334155) !important;
        border-bottom: 2px solid rgba(0, 234, 255, 0.3);
        padding: 0.8rem 1rem !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    .stNavigation button {
        background: transparent !important;
        color: #e2e8f0 !important;
        font-weight: 500;
        border-radius: 8px !important;
        margin: 0 4px !important;
        padding: 6px 16px !important;
        transition: all 0.3s ease;
    }
    .stNavigation button:hover {
        background: rgba(0, 234, 255, 0.15) !important;
        transform: translateY(-2px);
    }
    .stNavigation .active {
        background: linear-gradient(90deg, #00eaff, #00bcd4) !important;
        color: #0f172a !important;
        font-weight: 700 !important;
        box-shadow: 0 0 15px rgba(0,234,255,0.7);
    }

    /* ========== HEADERS ========== */
    h1, h2, h3, h4 {
        font-weight: 700 !important;
        color: #f1f5f9 !important;
        letter-spacing: 0.5px;
    }

    /* ========== CARDS ========== */
    .block-container {
        padding-top: 2rem !important;
    }
    .stMarkdown div, .stDataFrame, .stTextInput, .stTextArea, .stSelectbox, .stSlider, .stButton {
        border-radius: 10px !important;
    }
    .stTextInput>div>div>input, textarea, select {
        background: rgba(30,41,59,0.8) !important;
        color: #f8fafc !important;
        border: 1px solid #00eaff !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
    }
    .stTextInput input::placeholder, textarea::placeholder {
        color: #94a3b8 !important;
    }

    /* ========== BUTTONS ========== */
    div.stButton > button {
        background: linear-gradient(90deg, #00eaff, #0072ff);
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        font-size: 15px;
        transition: all 0.3s ease;
        box-shadow: 0px 4px 12px rgba(0,234,255,0.3);
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0px 6px 20px rgba(0,234,255,0.6);
    }

    /* ========== ALERTS & INFO BOXES ========== */
    .stAlert {
        border-radius: 10px !important;
        font-weight: 500 !important;
    }
    .stAlert > div {
        background: rgba(15,23,42,0.85) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(0,234,255,0.5);
    }
            
      /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2027, #203a43, #2c5364);
        color: #f8fafc;
        font-family: "Poppins", sans-serif;
        border-right: 2px solid rgba(0,234,255,0.2);
    }

    /* ===== NAVIGATION MENU ===== */
    [data-testid="stSidebar"] ul {
        padding: 0;
    }
    [data-testid="stSidebar"] ul li {
        list-style: none;
        margin: 6px 0;
    }
    [data-testid="stSidebar"] ul li a {
        display: block;
        padding: 10px 14px;
        border-radius: 8px;
        color: #e2e8f0 !important;   /* teks default lebih terang */
        font-weight: 500;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    [data-testid="stSidebar"] ul li a:hover {
        background: rgba(0,234,255,0.15);
        color: #00eaff !important;
        transform: translateX(5px);
    }
    [data-testid="stSidebar"] ul li a.active {
        background: linear-gradient(90deg, #00eaff, #0072ff);
        color: #0f172a !important;  /* teks aktif jadi kontras */
        font-weight: 700;
        box-shadow: 0px 4px 10px rgba(0,234,255,0.5);
    }

    /* ===== API KEY INPUT ===== */
    [data-testid="stSidebar"] input {
        background: rgba(30,41,59,0.9);
        color: #f8fafc;
        border-radius: 8px;
        border: 1px solid #00eaff;
        padding: 8px 10px;
        font-size: 14px;
    }
    [data-testid="stSidebar"] input::placeholder {
        color: #94a3b8;
    }
    /* Pastikan semua teks navigasi sidebar jadi putih */
    [data-testid="stSidebar"] a, 
    [data-testid="stSidebar"] div, 
    [data-testid="stSidebar"] span {
        color: #ffffff !important;
        font-weight: 500 !important;
    }

    /* Hover effect */
    [data-testid="stSidebar"] a:hover {
        color: #00eaff !important;
        text-shadow: 0 0 6px rgba(0,234,255,0.8);
    }

    /* Aktif page (highlight lebih kontras) */
    [data-testid="stSidebar"] .st-emotion-cache-1v0mbdj, 
    [data-testid="stSidebar"] .st-emotion-cache-16txtl3 {
        color: #0f172a !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #00eaff, #0072ff);
        border-radius: 8px;
        box-shadow: 0px 4px 12px rgba(0,234,255,0.5);
    }
    </style>
""", unsafe_allow_html=True)


# =========================
# ▶️ Run the Selected Page
# =========================
pg.run()
