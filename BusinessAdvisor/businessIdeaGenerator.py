import streamlit as st
import requests

# =========================
# 🎨 Neo-Glassmorphism Futuristic CSS
# =========================
st.markdown("""
    <style>
    /* Background utama */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e293b, #0f2027);
        font-family: "Segoe UI", sans-serif;
        color: #e2e8f0;
    }

    /* Card form */
    .form-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 2rem;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.6), inset 0px 0px 15px rgba(0,234,255,0.1);
        margin-top: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .form-card:hover {
        transform: translateY(-5px);
        box-shadow: 0px 12px 30px rgba(0,234,255,0.3), inset 0px 0px 20px rgba(0,234,255,0.15);
    }

    /* Title */
    .form-title {
        font-size: 24px;
        font-weight: 800;
        background: linear-gradient(90deg, #00eaff, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 18px;
        text-shadow: 0px 0px 8px rgba(0,234,255,0.6);
    }

    /* Input & textarea */
    .stTextInput input, .stTextArea textarea {
        background: rgba(15, 23, 42, 0.75) !important;
        border: 1px solid rgba(0,234,255,0.3) !important;
        border-radius: 12px !important;
        padding: 12px !important;
        color: #f1f5f9 !important;
        transition: all 0.3s ease;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #00eaff !important;
        box-shadow: 0px 0px 10px rgba(0,234,255,0.6);
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #94a3b8 !important;
    }

    /* Slider */
    .stSlider > div > div > div {
        color: #f8fafc !important;
    }

    }
    div.stButton > button:hover {
        transform: scale(1.07);
        box-shadow: 0px 8px 28px rgba(0,234,255,0.8);
    }

    /* Result box */
    .result-box {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(0,234,255,0.25);
        border-radius: 14px;
        padding: 1.5rem;
        margin-top: 20px;
        color: #e2e8f0;
        font-size: 15px;
        line-height: 1.6;
        box-shadow: inset 0px 0px 15px rgba(0,234,255,0.15);
    }
     /* === Fix Input Text Visibility === */
    .stTextInput input, .stTextArea textarea {
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(0,234,255,0.5) !important;
        border-radius: 12px !important;
        padding: 12px !important;
        color: #ffffff !important;     /* teks input putih */
        font-weight: 500 !important;
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #a0aec0 !important;     /* abu-abu terang */
        font-style: italic !important;
    }
    .stTextInput label, .stTextArea label, .stSlider label {
        color: #f8fafc !important;     /* label putih terang */
        font-weight: 600 !important;
    }

    /* === Slider Label & Value === */
    .stSlider label, .stSlider span {
        color: #f8fafc !important;
        font-weight: 600 !important;
    }
    
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("# 💡 Business Idea Generator Page ")
st.markdown("# 💡 Business Idea Generator")
st.sidebar.text_input("Enter your OpenRouter API Key:", type="password", key="api_key")

# =========================
# 📌 Prompt Generator
# =========================
def generate_prompt(industry, target_audience, location, budget, goals):
    return [
        {"role": "system", "content": "You are a professional business consultant and startup advisor."},
        {"role": "user", "content": f"""
        Industry/Field: {industry}  
        Target Market: {target_audience}  
        Location: {location}  
        Initial Budget: {budget} IDR  
        Main Goal: {goals}  

        Task: Generate 3–5 structured business ideas with details.
        """}
    ]


# =========================
# 📌 API Call
# =========================
def get_response(api_key, prompt, temperature=0.7, max_tokens=1200): 
    if not api_key:
        st.error("Please enter your API key first.")
        return None
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Content-Type": "application/json","Authorization": f"Bearer {api_key}"},
            json={"model": "meta-llama/Llama-3.3-70B-Instruct","messages": prompt,"max_tokens": max_tokens,"temperature": temperature,},
            timeout=30
        )
        if response.status_code != 200:
            st.error(f"⚠️ API Error {response.status_code}: {response.text}")
            return None
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
        return None





# =========================
# 🚀 Business Idea Generator Form
# =========================
st.markdown('<div class="form-card">', unsafe_allow_html=True)


industry = st.text_input("Industry (e.g., technology, healthcare):")
target_audience = st.text_input("Target Audience (e.g., millennials, small businesses):")
location = st.text_input("Location (e.g., Jakarta, Bandung, online):")
budget = st.slider("Budget (IDR):", 30000, 500000000, step=10000)
goals = st.text_area("Business Goals (e.g., market leader, sustainable growth):")

    
st.markdown("""
<style>
/* Target tombol submit dalam form */
div.stForm button[kind="formSubmit"] {
    background: linear-gradient(90deg, #00c6ff, #0072ff) !important;
    color: white !important;
    font-weight: bold !important;
    border-radius: 8px !important;
    padding: 12px 22px !important;
    border: none !important;
    font-size: 16px !important;
    transition: all 0.3s ease-in-out !important;
    box-shadow: 0px 4px 10px rgba(0, 118, 255, 0.4) !important;
}

/* Hover effect */
div.stForm button[kind="formSubmit"]:hover {
    background: linear-gradient(90deg, #00eaff, #00bcd4) !important;
    transform: scale(1.05) !important;
    box-shadow: 0px 6px 20px rgba(0,234,255,0.6) !important;
}
</style>
""", unsafe_allow_html=True)


submitted = st.button("Generate Business Idea")

# =========================
# 📌 Handle Submission
# =========================
if submitted:
    if not industry or not target_audience or not location or not goals:
        st.error("⚠️ Please fill in all the fields.")
    else:
        st.info("⏳ Generating business ideas...")
        api_key = st.session_state.get("api_key", "")
        prompt = generate_prompt(industry, target_audience, location, budget, goals)
        response = get_response(api_key, prompt)

        if response:
            st.success("✅ Business Ideas Generated!")
            st.subheader("📊 Generated Business Idea(s):")
            st.markdown(f'<div class="result-box">{response}</div>', unsafe_allow_html=True)
