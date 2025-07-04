import streamlit as st
from hr_policy_bot import read_docx

st.title("Expense Reimbursement Policy")
st.write(read_docx("hr_docs/Expense Reimbursement Policy.docx"))