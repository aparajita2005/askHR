import streamlit as st
from hr_policy_bot import read_docx

st.title("Employee Exit, Termination & Exit Interview Policy")
st.write(read_docx("hr_docs/Employee Exit, Termination & Exit Interview Policy.docx"))