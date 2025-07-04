import streamlit as st
from hr_policy_bot import read_docx

st.title("IT Acceptable Use & BYOD Policy")
st.write(read_docx("hr_docs/IT Acceptable Use & BYOD Policy.docx"))