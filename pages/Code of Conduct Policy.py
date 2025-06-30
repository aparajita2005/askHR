import streamlit as st
from hr_policy_bot import read_docx

st.title("Code of Conduct Policy")
st.write(read_docx("hr_docs/Code of Conduct Policy.docx"))