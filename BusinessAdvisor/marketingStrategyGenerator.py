import streamlit as st
import requests

st.markdown("# Marketing Strategy Generator Page  🎯")
st.sidebar.markdown("# Marketing Strategy Generator Page  🎯")
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
    
with st.form("marketing_strategy_form"):
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

    submit_button = st.form_submit_button("Generate Marketing Strategy")

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
                st.write(response)