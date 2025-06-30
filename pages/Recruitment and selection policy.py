import streamlit as st
from hr_policy_bot import read_docx

st.title("Recruitment and selection policy")
st.write(read_docx("hr_docs/Recruitment and selection policy.docx"))