import streamlit as st
from hr_policy_bot import read_docx

st.title("Disciplinary & Grievance Policy")
st.write(read_docx("hr_docs/Disciplinary & Grievance Policy.docx"))