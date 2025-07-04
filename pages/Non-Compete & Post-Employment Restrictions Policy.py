import streamlit as st
from hr_policy_bot import read_docx

st.title("Non-Compete & Post-Employment Restrictions Policy")
st.write(read_docx("hr_docs/Non-Compete & Post-Employment Restrictions Policy.docx"))