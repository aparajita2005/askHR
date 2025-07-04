import streamlit as st
from hr_policy_bot import read_docx

st.title("Performance Management & Appraisal Policy")
st.write(read_docx("hr_docs/Performance Management & Appraisal Policy.docx"))