import streamlit as st
from hr_policy_bot import read_docx

st.title("Working Hours & Attendance Policy")
st.write(read_docx("hr_docs/Working Hours & Attendance Policy.docx"))