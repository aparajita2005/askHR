import streamlit as st
from hr_policy_bot import read_docx

st.title("Overtime & Compensatory Time Policy")
st.write(read_docx("hr_docs/Overtime & Compensatory Time Policy.docx"))