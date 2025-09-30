import streamlit as st
import requests

st.markdown("# Business Idea Generator Page  🚀")
st.sidebar.markdown("# Business Idea Generator Page  🚀")
st.sidebar.text_input("Enter your OpenRouter API Key:", type="password", key="api_key")


def generate_prompt(industry, target_audience, location, budget, goals):
    prompt = [
        {
            "role": "system",
            "content": (
                "You are a professional business consultant and startup advisor. "
                "Your expertise is in analyzing industries, identifying opportunities, "
                "and creating innovative but practical business ideas tailored to clients' needs. "
                "Always provide structured, clear, and professional recommendations "
                "as if presenting to investors or executives."
            )
        },
        {
            "role": "user",
            "content": f"""
    The user is looking for new business ideas. Here are the details:

    - Industry/Field: {industry}  
    - Target Market: {target_audience}  
    - Location: {location}  
    - Initial Budget: {budget} IDR  
    - Main Goal: {goals}  

    Task:  
    1. Generate 3–5 business ideas that align with the above details.  
    2. For each idea, provide:  
    - **Business Name / Concept**  
    - **Short Description** (what the business does and why it fits)  
    - **Unique Value Proposition** (why customers should choose it)  
    - **Potential Revenue Streams**  
    - **Risks and Considerations**  

    Present the output in a structured, professional format.
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
    




with st.form("idea_form"):
    st.subheader("💡 Business Idea Generator")

    industry = st.text_input("Industry (e.g., technology, healthcare):")
    target_audience = st.text_input("Target Audience (e.g., millennials, small businesses):")
    location = st.text_input("Location (e.g., Jakarta, Bandung, online):")
    budget = st.slider("Budget (IDR):", 30000, 500000000, step=10000)
    goals = st.text_area("Business Goals (e.g., market leader, sustainable growth):")

    submit_button = st.form_submit_button("Generate Business Idea")

# ✅ Generate AI di luar form
if submit_button:
    if not industry or not target_audience or not location or not budget or not goals:
        st.error("⚠️ Please fill in all the fields.")
    else:
        st.info("⏳ Generating business ideas...")

        api_key = st.session_state.get("api_key", "")
        prompt = generate_prompt(industry, target_audience, location, budget, goals)
        response = get_response(api_key, prompt, temperature=0.7, max_tokens=1200)

        if response:
            st.success("✅ Business Ideas Generated!")
            st.subheader("📊 Generated Business Idea(s):")
            st.write(response)
