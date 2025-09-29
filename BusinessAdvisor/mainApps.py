import streamlit as st


main_page = st.Page("businessIdeaGenerator.py", title="Business Idea Generator ", icon="🚀")
page_2 = st.Page("marketingStrategyGenerator.py", title="Marketing Strategy Generator", icon="🎯")
page_3 = st.Page("customerReviewAnalyzier.py", title="Customer Review Analyzier", icon="⭐")
page_4 = st.Page("SocialMediaContentGenerator.py", title="Social Media Content Generator", icon="📱")
page_5 = st.Page("FinancialAdvisor.py", title="Financial Advisor", icon="💰")
page_6 = st.Page("businessAdviceGenerator.py", title="business Advice Generator", icon="🧠")

# Set up navigation
pg = st.navigation([main_page,page_2, page_3,page_4,page_5,page_6])

# Run the selected page
pg.run()

