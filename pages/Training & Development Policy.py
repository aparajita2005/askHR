import streamlit as st
from hr_policy_bot import read_docx

st.title("Training & Development Policy")
st.write(read_docx("hr_docs/Training & Development Policy.docx"))