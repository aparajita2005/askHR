import streamlit as st
from hr_policy_bot import read_docx

st.title("Leave of Absence Policy")
st.write(read_docx("hr_docs/Leave of Absence Policy.docx"))