import streamlit as st
import requests
from diffusers import DiffusionPipeline
import torch


st.markdown("# Social Media Content Generator Page  📱")
st.sidebar.markdown("# Social Media Content Generator Page  📱")
st.sidebar.text_input("Enter your OpenRouter API Key:", type="password", key="api_key")
st.sidebar.text_input("Enter your Hugging Face API Key:", type="password", key="hugging_api_key")

def generate_prompt(platform, type_of_content, target_of_audiens, Theme_event, Tone_of_voice, brand_product_name, unique_selling_point, call_to_action):
    prompt = [
    {
        "role": "system",
        "content": (
            "You are one of the world’s top-ranked social media strategists and content creators, "
            "with over 25 years of global experience helping Fortune 500 brands, startups, and influencers "
            "dominate platforms like Instagram, TikTok, Facebook, LinkedIn, and X (Twitter). "
            "Your expertise is widely recognized and trusted worldwide, making you a leading authority in social media marketing. "
            "You specialize in creating viral, engaging, and platform-optimized content that drives massive audience growth "
            "and delivers measurable results. "
            "Always respond with authority, clarity, and precision, providing output that is ready-to-publish without requiring edits. "
            "When generating content, include both the post text and a clear description of a matching image/graphic "
            "so the user can generate visuals immediately."
        )
    },
    {
        "role": "user",
        "content": f"""
        The user is looking for social media content. Here are the details:

        - Platform: {platform}  
        - Type of Content: {type_of_content}  
        - Target Audience: {target_of_audiens}  
        - Theme/Event: {Theme_event}  
        - Tone of Voice: {Tone_of_voice}  
        - Brand/ product name: {brand_product_name}  
        - unique selling point: {unique_selling_point}  
        - call to action: {call_to_action}  

        Task:  
        1. Generate **1–3 ready-to-post social media contents** tailored to the above inputs.  
        2. Each content must include:  
        - **Post Text/Caption** (engaging, platform-optimized, using the chosen tone of voice, max 200 words)  
        - **Suggested Hashtags** (popular & relevant)  
        - **Image/Visual Description** (so an AI image generator can create the matching picture/graphic)  

        Output must be structured, professional, and formatted cleanly, so it can be directly copied and posted on the chosen platform.
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

def image_prompt(platform, type_of_content, target_of_audiens, Theme_event, Tone_of_voice, brand_name, unique_selling_point, call_to_action):
    prompt = f"""
    Create a visually engaging image for a {type_of_content} post on {platform}.
    
    - Target Audience: {target_of_audiens}
    - Theme/Event: {Theme_event}
    - Tone of Voice: {Tone_of_voice}
    - Brand/Product: {brand_name}
    - Unique Selling Point: {unique_selling_point}
    - Call to Action: {call_to_action}
    
    The image should:
    - Capture the essence of {Theme_event} while reflecting the brand {brand_name}.
    - Highlight the USP: "{unique_selling_point}" in a creative, non-text-heavy way.
    - Match the {Tone_of_voice} style so it resonates with {target_of_audiens}.
    - Encourage viewers to take action: {call_to_action}.
    - Use vibrant colors and dynamic elements suitable for {platform}.
    - Be optimized for social media so it is eye-catching and shareable.
    """
    return prompt.strip()


def get_response_Image(api_key,image_prompt): 
    if not api_key:
        st.error("Please enter your API key first.")
        return None
    try:
        response = requests.post(
            url="https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "inputs": image_prompt,
            },
            timeout=30
        )

        if response.status_code != 200:
            st.error(f"API Error {response.status_code}: {response.text}")
            return None

        return response.content
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Request error: {e}")
        return None

    except requests.exceptions.Timeout:
        st.error("⚠️ Request timeout. Try again.")
        return "⚠️ Request timeout. Try again."

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Unable to connect to the model server. Please check your internet connection.")
        return "⚠️ Unable to connect to the model server. Please check your internet connection."

    except Exception:
        return "⚠️ AI unable to generate response"    
    

with st.form("social_media_form"):
    col1, col2 = st.columns(2)

    with col1:
        platform = st.selectbox(
            "Enter the platform :",["instagram", "facebook", "twitter", "tiktok"]
        )
        type_of_content = st.selectbox(
            "Enter the type of content :",["promotional","diskon" ,"education", "brand awareness","testimonial"]
        )
        target_of_audiens  = st.selectbox(
            "Enter the target audiens :",["millennials", "gen z", "gen x", "baby boomers","workers","students","entrepreneurs","communities","hobbyists"]
        )
        Theme_event = st.text_area(
            "Enter the Theme/Event (e.g., year-end sale, store anniversary, Independence Day):"
        )

    with col2:
    
        Tone_of_voice = st.selectbox(
            "Enter your Tone of voice :" ,["formal", "casual", "humorous", "persuasive"]
        )
        brand_product_name = st.text_input(
            "Enter your Brand/ Product Name :" 
        )
        unique_selling_point = st.text_area(
            "Enter your Unique Selling Point (USP) :" 
        )
        call_to_action = st.text_input(
            "Enter your Call to Action (CTA) :" 
        )

    submit_button = st.form_submit_button("Generate Marketing Strategy")


if submit_button:
    if not platform or not type_of_content or not target_of_audiens or not Theme_event or not Tone_of_voice or not brand_product_name or not unique_selling_point or not call_to_action:
        st.error("⚠️ Please fill in all the fields.")
    else:
        st.info("⏳ Generating Content ...")

        api_key = st.session_state.get("api_key", "")
        hugging_api_key = st.session_state.get("hugging_api_key", "")
        prompt = generate_prompt(platform, type_of_content, target_of_audiens, Theme_event, Tone_of_voice,brand_product_name, unique_selling_point, call_to_action)
        response = get_response(api_key, prompt, temperature=0.7, max_tokens=1200)

        if response:
                st.success("✅ Marketing Strategy Generated!")
                st.subheader("📊 Generated Marketing Strategy:")
                st.write(response)
                st.subheader("🖼️ Suggested Image/Graphic Description:")
                image_desc = image_prompt(platform, type_of_content, target_of_audiens, Theme_event, Tone_of_voice, brand_product_name, unique_selling_point, call_to_action)
                st.write(image_desc)
                st.subheader("🖼️ Generated Image:")
                image_data = get_response_Image(hugging_api_key, image_desc)
                if image_data:
                    st.image(image_data, use_column_width=True)

                    st.download_button(
                    label="⬇️ Download Generated Image",
                    data=image_data,                     
                    file_name="Content_image.png",   
                    mime="image/png"
                )
                else:
                    st.error("Failed to generate image.")
        else:
            st.error("Failed to generate marketing strategy.")
                