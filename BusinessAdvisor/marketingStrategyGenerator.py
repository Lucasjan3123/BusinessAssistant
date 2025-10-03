import streamlit as st
import requests

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
            
    </style>
""", unsafe_allow_html=True)



st.sidebar.markdown("# Marketing Strategy Generator Page  🎯")
st.markdown("# 🎯 Marketing Strategy Generator Page")
st.sidebar.text_input("Enter your OpenRouter API Key:", type="password", key="api_key")

def generate_prompt(business_type, target_audience, primary_media, budget_marketing, goals_marketing):
    prompt = [
        {
            "role": "system",
            "content": (
                "You are one of the world’s top-ranked marketing strategists and business consultants, "
                "with over 30 years of global experience advising Fortune 500 companies, startups, and international brands. "
                "Your expertise is widely recognized and trusted worldwide, making you a thought leader in marketing and business strategy. "
                "You specialize in creating innovative, actionable, and data-driven strategies that deliver measurable results. "
                "Always respond with authority, clarity, and precision, providing structured recommendations "
                "as if presenting to executives, investors, or global clients."
            )
        },
        {
            "role": "user",
            "content": f"""
    The user is looking for a marketing strategy. Here are the details:

    - Business Type: {business_type}  
    - Target Audience: {target_audience}  
    - Primary Marketing Media: {primary_media}  
    - Budget: {budget_marketing} IDR  
    - Marketing Goals: {goals_marketing}  

    Task:  
    1. Generate a comprehensive marketing strategy tailored to the above inputs.  
    2. The strategy must include:  
    - **Executive Summary** (high-level direction of the strategy)  
    - **Key Messages** (core ideas to communicate to the target audience)  
    - **Tactics & Channels** (specific actions and campaigns for the chosen media)  
    - **Budget Allocation Plan** (optimized allocation of the given budget)  
    - **Success Metrics (KPIs)** (clear measurements of success)  
    - **Risks and Mitigation** (potential challenges and recommended solutions)  

    Present the output in a highly structured, professional, and globally competitive format.
    """
        }
    ]

    return prompt



def get_response(api_key,prompt, temperature, max_tokens): 
    if not api_key:
        st.error("Please enter your API key first.")
        return None
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "model": "meta-llama/Llama-3.3-70B-Instruct",
                "messages": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
            timeout=30
        )

        if response.status_code != 200:
            try:
                error_msg = response.json().get("error", {}).get("message", response.text)
            except:
                error_msg = response.text
            st.error(f"⚠️ Model Error ({response.status_code}): {error_msg}")
            return "⚠️ AI unable to generate response"

        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        return answer

    except requests.exceptions.Timeout:
        st.error("⚠️ Request timeout. Try again.")
        return "⚠️ Request timeout. Try again."

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Unable to connect to the model server. Please check your internet connection.")
        return "⚠️ Unable to connect to the model server. Please check your internet connection."

    except Exception:
        return "⚠️ AI unable to generate response"
    

st.markdown('<div class="form-card">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    business_types = st.text_input(
        "Enter the business Type (e.g., technology, healthcare):"
    )
    target_audience = st.text_input(
        "Enter the target audience (e.g., millennials, small businesses):"
    )
    primary_media = st.text_input(
        "Enter the primary marketing media (e.g., social media, email, SEO):"
    )

with col2:
    budget_marketing = st.slider(
        "Enter the budget (e.g., 1000, 5000, 10000):",
        10000000,
        1000000000,
        step=100,
    )
    goals_marketing = st.text_area(
        "Enter your marketing goals (e.g., brand awareness, lead generation):"
    )

submit_button = st.button("Generate Marketing Strategy")

if submit_button:
    if not business_types or not target_audience or not primary_media or not budget_marketing or not goals_marketing:
        st.error("⚠️ Please fill in all the fields.")
    else:
        st.info("⏳ Generating marketing strategy...")

        api_key = st.session_state.get("api_key", "")
        prompt = generate_prompt(business_types, target_audience, primary_media, budget_marketing, goals_marketing)
        response = get_response(api_key, prompt, temperature=0.7, max_tokens=1200)

        if response:
                st.success("✅ Marketing Strategy Generated!")
                st.subheader("📊 Generated Marketing Strategy:")
                st.markdown(f'<div class="result-box">{response}</div>', unsafe_allow_html=True) 