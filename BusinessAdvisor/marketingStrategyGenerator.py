import streamlit as st

st.markdown("# Marketing Strategy Generator Page  🎯")
st.sidebar.markdown("# Marketing Strategy Generator Page  🎯")

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
            1000,
            1000000,
            step=100,
        )
        goals_marketing = st.text_area(
            "Enter your marketing goals (e.g., brand awareness, lead generation):"
        )

    submit_button = st.form_submit_button("Generate Marketing Strategy")