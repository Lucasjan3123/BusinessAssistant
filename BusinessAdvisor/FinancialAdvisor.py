import streamlit as st

st.markdown("# Financial Advisor Page  💰")
st.sidebar.markdown("# Financial Advisor Page  💰")

with st.form("financial_form"):
    file =  st.file_uploader("Please upload your  financial statement", type=["pdf", "txt", "docx"])
    goals = st.text_area("Enter your business goals (e.g., market leader, sustainable growth):")
    submit_button = st.form_submit_button("analyze Financial Statement")