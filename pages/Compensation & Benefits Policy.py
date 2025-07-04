import streamlit as st
from hr_policy_bot import read_docx

st.title("Compensation & Benefits Policy")
st.write(read_docx("hr_docs/Compensation & Benefits Policy.docx"))