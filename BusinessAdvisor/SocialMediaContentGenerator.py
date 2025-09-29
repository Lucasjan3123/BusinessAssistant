import streamlit as st

st.markdown("# Social Media Content Generator Page  📱")
st.sidebar.markdown("# Social Media Content Generator Page  📱")

with st.form("social_media_form"):
    col1, col2 = st.columns(2)

    with col1:
        platform = st.selectbox(
            "Enter the platform :",["instagram", "facebook", "twitter", "tiktok"]
        )
        type_of_content = st.selectbox(
            "Enter the type of content :",["promotional","diskon" "education", "brand awareness","testimonial"]
        )
        target_of_audiens  = st.selectbox(
            "Enter the target audiens :",["millennials", "gen z", "gen x", "baby boomers","workers","students","entrepreneurs","communities","hobbyists"]
        )

    with col2:
        Theme_event = st.text_area(
            "Enter the Theme/Event (e.g., year-end sale, store anniversary, Independence Day):"
        )
        Tone_of_voice = st.selectbox(
            "Enter your Tone of voice :" ,["formal", "casual", "humorous", "persuasive"]
        )

    submit_button = st.form_submit_button("Generate Marketing Strategy")