"""
Streamlit UI for AI Risk Advisor.

Run:
    streamlit run app/ui.py
"""

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from app.agents.orchestrator import run_orchestrator


st.set_page_config(
    page_title="AI Risk Advisor",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ AI Risk Advisor")
st.subheader("Multi-Agent RAG System using NIST AI RMF")

st.write(
    "This advisor uses Azure OpenAI, Azure AI Search, and specialized agents "
    "aligned with GOVERN, MAP, MEASURE, and MANAGE."
)

st.markdown("### Try an example")

col1, col2 = st.columns(2)

with col1:
    finance_example = st.button("Customer Chatbot (Finance)")

with col2:
    healthcare_example = st.button("Healthcare Diagnosis AI")

default_question = (
    "Assess the AI risks of deploying a customer-facing AI chatbot "
    "for a financial services company."
)

if "question" not in st.session_state:
    st.session_state.question = default_question

if finance_example:
    st.session_state.question = default_question

if healthcare_example:
    st.session_state.question = (
        "Assess the AI risks of deploying an AI system used for medical diagnosis in hospitals."
    )

question = st.text_area(
    "Enter an AI risk scenario:",
    value=st.session_state.question,
    height=120,
)

run_button = st.button("Generate AI Risk Advisory Report")

if run_button:
    if not question.strip():
        st.warning("Please enter a risk scenario.")
    else:
        with st.status("Running AI Risk Analysis...", expanded=True) as status:
            st.write("Running GOVERN analysis...")
            st.write("Running MAP analysis...")
            st.write("Running MEASURE analysis...")
            st.write("Running MANAGE analysis...")
            st.write("Synthesizing final report...")

            report = run_orchestrator(question)

            status.update(label="Analysis complete", state="complete")

        st.success("Report generated.")

        st.markdown("## Advisory Report")
        st.markdown(report)

        st.markdown("## Copyable Markdown")
        st.code(report, language="markdown")