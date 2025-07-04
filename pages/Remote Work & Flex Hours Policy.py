import streamlit as st
from hr_policy_bot import read_docx

st.title("Remote Work & Flex Hours Policy")
st.write(read_docx("hr_docs/Remote Work & Flex Hours Policy.docx"))