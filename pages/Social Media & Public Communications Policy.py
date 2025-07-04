import streamlit as st
from hr_policy_bot import read_docx

st.title("Social Media & Public Communications Policy")
st.write(read_docx("hr_docs/Social Media & Public Communications Policy.docx"))