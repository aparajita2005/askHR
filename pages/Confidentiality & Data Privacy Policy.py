import streamlit as st
from hr_policy_bot import read_docx

st.title("Confidentiality & Data Privacy Policy")
st.write(read_docx("hr_docs/Confidentiality & Data Privacy Policy.docx"))