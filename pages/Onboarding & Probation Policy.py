import streamlit as st
from hr_policy_bot import read_docx

st.title("Onboarding & Probation Policy")
st.write(read_docx("hr_docs/Onboarding & Probation Policy.docx"))