import streamlit as st
from hr_policy_bot import read_docx

st.title("Dress Code Policy")
st.write(read_docx("hr_docs/Dress Code Policy.docx"))