import streamlit as st
from hr_policy_bot import read_docx

st.title("Anti-Sexual Harrasment Policy")
st.write(read_docx("hr_docs/Anti-Sexual Harassment Policy.docx"))