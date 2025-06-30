import streamlit as st
from hr_policy_bot import read_docx

st.title("Equal Employment Opportunity (EEO) & Non-Discrimination Policy")
st.write(read_docx("hr_docs/Equal Employment Opportunity (EEO) & Non-Discrimination Policy.docx"))