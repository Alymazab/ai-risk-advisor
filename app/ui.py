"""
Responsive modern Streamlit UI for AI Risk Advisor.

Run:
    streamlit run app/ui.py
"""

import sys
import time
from pathlib import Path
from datetime import datetime
from app.risk.scoring import calculate_risk_scores
from app.risk.llm_scoring import score_report_with_llm


import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from app.agents.orchestrator import run_orchestrator
from app.risk.scoring import calculate_risk_scores
from app.risk.charts import generate_risk_chart
from app.risk.charts import (
    generate_risk_chart,
    generate_radar_chart,
    generate_likelihood_impact_matrix,
)
from app.report.pdf_generator import generate_pdf_report

st.set_page_config(
    page_title="AI Risk Advisor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #020617 0%, #0f172a 45%, #111827 100%);
    color: #f8fafc;
}

[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid #1e293b;
}

[data-testid="stHeader"] {
    background: rgba(15, 23, 42, 0);
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.hero {
    padding: clamp(22px, 4vw, 38px);
    border-radius: 28px;
    background:
        radial-gradient(circle at top left, rgba(34,197,94,.28), transparent 32%),
        linear-gradient(135deg, rgba(15,23,42,.92), rgba(30,41,59,.72));
    border: 1px solid rgba(34,197,94,.35);
    box-shadow: 0 0 24px rgba(34,197,94,.16), 0 24px 80px rgba(0,0,0,.45);
    margin-bottom: 26px;
}

.hero-title {
    font-size: clamp(32px, 6vw, 56px);
    line-height: 1.05;
    font-weight: 950;
    letter-spacing: -1.4px;
    color: #f8fafc;
    margin-bottom: 10px;
}

.hero-subtitle {
    font-size: clamp(14px, 2vw, 18px);
    color: #cbd5e1;
    max-width: 900px;
}

.badge {
    display: inline-block;
    padding: 7px 12px;
    border-radius: 999px;
    background: rgba(34,197,94,.12);
    border: 1px solid rgba(34,197,94,.45);
    color: #86efac;
    font-size: clamp(11px, 1.5vw, 13px);
    font-weight: 800;
    margin-right: 8px;
    margin-bottom: 12px;
}

.online-row {
    display: flex;
    align-items: center;
    margin-bottom: 18px;
    color: #22c55e;
    font-weight: 900;
    letter-spacing: .8px;
    font-size: clamp(13px, 2vw, 16px);
}

.pulse-dot {
    width: 12px;
    height: 12px;
    min-width: 12px;
    border-radius: 50%;
    background: #22c55e;
    display: inline-block;
    margin-right: 10px;
    box-shadow: 0 0 10px #22c55e;
    animation: pulse 1.2s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); opacity: 0.55; }
    50% { transform: scale(1.6); opacity: 1; }
    100% { transform: scale(1); opacity: 0.55; }
}

.terminal-box {
    background: #020617;
    border: 1px solid rgba(34,197,94,.35);
    border-radius: 18px;
    padding: clamp(14px, 3vw, 18px);
    font-family: Consolas, monospace;
    color: #22c55e;
    box-shadow: inset 0 0 20px rgba(34,197,94,.08), 0 0 24px rgba(34,197,94,.12);
    margin-top: 18px;
    margin-bottom: 18px;
    overflow-x: auto;
    font-size: clamp(12px, 1.8vw, 15px);
}

.cursor {
    display: inline-block;
    width: 8px;
    height: 16px;
    background: #22c55e;
    margin-left: 4px;
    animation: blink 1s infinite;
}

@keyframes blink {
    0% { opacity: 0 }
    50% { opacity: 1 }
    100% { opacity: 0 }
}

.small-card {
    padding: clamp(15px, 3vw, 18px);
    border-radius: 18px;
    background: rgba(15, 23, 42, .78);
    border: 1px solid rgba(34,197,94,.22);
    min-height: 132px;
    box-shadow: 0 12px 36px rgba(0,0,0,.22);
}

.card-title {
    color: #f8fafc;
    font-size: clamp(16px, 2vw, 18px);
    font-weight: 900;
    margin-bottom: 8px;
}

.card-text {
    color: #cbd5e1;
    font-size: clamp(13px, 1.8vw, 14px);
}

.report-box {
    padding: clamp(18px, 4vw, 30px);
    border-radius: 24px;
    background: #f8fafc;
    color: #0f172a;
    border: 1px solid #e2e8f0;
    box-shadow: 0 24px 70px rgba(0,0,0,.42);
    overflow-x: auto;
    word-wrap: break-word;
}

.report-box h1, .report-box h2, .report-box h3 {
    color: #0f172a;
}

.glass-card {
    padding: clamp(16px, 3vw, 22px);
    border-radius: 22px;
    background: rgba(15, 23, 42, .72);
    border: 1px solid rgba(34,197,94,.22);
    box-shadow: 0 18px 50px rgba(0,0,0,.28);
    color: #e2e8f0;
    overflow-x: auto;
}

.stButton > button {
    border-radius: 16px !important;
    padding: 0.75rem 1rem !important;
    font-weight: 900 !important;
    letter-spacing: 0.45px !important;
    border: 1px solid rgba(34,197,94,.75) !important;
    background: linear-gradient(135deg, #16a34a, #22c55e) !important;
    color: #022c22 !important;
    box-shadow: 0 0 8px rgba(34,197,94,.65), 0 0 18px rgba(34,197,94,.42), inset 0 0 6px rgba(255,255,255,.14);
    transition: all 0.25s ease-in-out !important;
    white-space: normal !important;
    min-height: 44px !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #22c55e, #4ade80) !important;
    box-shadow: 0 0 12px rgba(34,197,94,.95), 0 0 28px rgba(34,197,94,.68), 0 0 45px rgba(34,197,94,.34);
    transform: translateY(-2px) scale(1.02);
}

.stDownloadButton > button {
    border-radius: 16px !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #16a34a, #22c55e) !important;
    color: #022c22 !important;
    border: 1px solid rgba(34,197,94,.75) !important;
    box-shadow: 0 0 8px rgba(34,197,94,.65), 0 0 18px rgba(34,197,94,.42);
    white-space: normal !important;
}

textarea {
    border-radius: 18px !important;
    font-size: clamp(13px, 2vw, 15px) !important;
}

[data-testid="stMetric"] {
    background: rgba(15, 23, 42, .76);
    border: 1px solid rgba(34,197,94,.22);
    padding: clamp(12px, 2vw, 18px);
    border-radius: 18px;
    box-shadow: 0 10px 28px rgba(0,0,0,.22);
}

[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
}

[data-testid="stMetricValue"] {
    color: #f8fafc !important;
    font-size: clamp(18px, 2.5vw, 28px) !important;
}

hr {
    border-color: rgba(34,197,94,.18);
}

@media (max-width: 900px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 1rem;
    }

    .hero {
        border-radius: 20px;
    }

    .small-card {
        min-height: auto;
        margin-bottom: 10px;
    }

    .report-box {
        border-radius: 18px;
    }

    .stButton > button {
        font-size: 13px !important;
        padding: 0.65rem 0.75rem !important;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


with st.sidebar:
    st.markdown("## 🛡️ AI Risk Advisor")
    st.caption("Azure-based multi-agent AI risk reporting system.")

    st.divider()

    st.markdown("### Stack")
    st.write("Azure OpenAI")
    st.write("Azure AI Search")
    st.write("Azure Key Vault")
    st.write("NIST AI RMF")
    st.write("Multi-Agent RAG")

    st.divider()

    st.markdown("### Report Settings")
    report_style = st.selectbox(
        "Report style",
        ["Board-ready", "Technical", "Executive"],
        index=0,
    )

    show_markdown = st.toggle("Show copyable Markdown", value=False)

    st.divider()
    st.caption("Built for AI governance, risk, and security assessment.")


st.markdown(
    """
<div class="hero">
    <span class="badge">Azure OpenAI</span>
    <span class="badge">Azure AI Search</span>
    <span class="badge">Key Vault</span>
    <span class="badge">NIST AI RMF</span>
    <span class="badge">Multi-Agent RAG</span>
    <div class="hero-title">AI Risk Advisor</div>
    <div class="hero-subtitle">
        Generate enterprise-style AI risk advisory reports using a multi-agent RAG system aligned with
        GOVERN, MAP, MEASURE, and MANAGE from the NIST AI Risk Management Framework.
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="online-row">
    <span class="pulse-dot"></span>
    AI SYSTEM ONLINE
</div>
""",
    unsafe_allow_html=True,
)

metric1, metric2, metric3, metric4 = st.columns(4, gap="medium")

with metric1:
    st.metric("Framework", "NIST AI RMF")

with metric2:
    st.metric("Agents", "4")

with metric3:
    st.metric("Retrieval", "Azure AI Search")

with metric4:
    st.metric("Secrets", "Key Vault")


st.markdown("### Select a scenario")

sc1, sc2, sc3 = st.columns(3, gap="medium")

with sc1:
    st.markdown(
        """
<div class="small-card">
    <div class="card-title">Financial Chatbot</div>
    <div class="card-text">Customer-facing AI assistant for banking, support, and financial guidance.</div>
</div>
""",
        unsafe_allow_html=True,
    )
    finance_example = st.button("Use finance scenario", use_container_width=True)

with sc2:
    st.markdown(
        """
<div class="small-card">
    <div class="card-title">Healthcare Diagnosis AI</div>
    <div class="card-text">Clinical decision-support AI used by hospitals and medical staff.</div>
</div>
""",
        unsafe_allow_html=True,
    )
    healthcare_example = st.button("Use healthcare scenario", use_container_width=True)

with sc3:
    st.markdown(
        """
<div class="small-card">
    <div class="card-title">AI Hiring Assistant</div>
    <div class="card-text">AI system used to screen resumes, rank candidates, and support hiring.</div>
</div>
""",
        unsafe_allow_html=True,
    )
    hr_example = st.button("Use hiring scenario", use_container_width=True)


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

if hr_example:
    st.session_state.question = (
        "Assess the AI risks of deploying an AI hiring assistant used to screen job applicants."
    )


st.markdown("### Describe the AI system")

question = st.text_area(
    "Include business context, users, model purpose, possible harms, and deployment environment.",
    value=st.session_state.question,
    height=145,
)

generate = st.button(
    "Generate AI Risk Advisory Report",
    type="primary",
    use_container_width=True,
)

if generate:
    if not question.strip():
        st.warning("Please enter a risk scenario.")
    else:
        status_placeholder = st.empty()

        status_placeholder.markdown(
            """
<div class="terminal-box">
<span class="pulse-dot"></span>
Initializing AI Risk Analysis<span class="cursor"></span>
</div>
""",
            unsafe_allow_html=True,
        )

        time.sleep(0.4)

        status_placeholder.markdown(
            """
<div class="terminal-box">
✔ Loading NIST AI RMF context<br>
✔ Connecting to Azure AI Search<br>
✔ Loading secure credentials from Azure Key Vault<br>
</div>
""",
            unsafe_allow_html=True,
        )

        time.sleep(0.4)

        status_placeholder.markdown(
            """
<div class="terminal-box">
✔ Running GOVERN agent<br>
✔ Running MAP agent<br>
✔ Running MEASURE agent<br>
✔ Running MANAGE agent<br>
</div>
""",
            unsafe_allow_html=True,
        )

        time.sleep(0.4)

        status_placeholder.markdown(
            """
<div class="terminal-box">
✔ Synthesizing final advisory report<br>
<span class="pulse-dot"></span>Generating board-ready output<span class="cursor"></span>
</div>
""",
            unsafe_allow_html=True,
        )

        report = run_orchestrator(question)
        risk_score = score_report_with_llm(question, report)

        scores = {
            "GOVERN": risk_score.get("govern_score", 0),
            "MAP": risk_score.get("map_score", 0),
            "MEASURE": risk_score.get("measure_score", 0),
            "MANAGE": risk_score.get("manage_score", 0),
        }

        level = risk_score.get("overall_risk_level", "Unknown")
        overall_score = risk_score.get("overall_score", 0)
        likelihood_score = risk_score.get("likelihood_score", 0)
        impact_score = risk_score.get("impact_score", 0)
        bar_chart_fig = generate_risk_chart(scores)
        radar_chart_fig = generate_radar_chart(scores)
        matrix_chart_fig = generate_likelihood_impact_matrix(likelihood_score, impact_score)

        status_placeholder.markdown(
            """
<div class="terminal-box">
✔ Analysis complete<br>
✔ Report ready
</div>
""",
            unsafe_allow_html=True,
        )

        st.success("Report generated successfully.")

        generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        st.markdown("---")

        a, b, c, d = st.columns(4, gap="medium")

        with a:
            st.metric("Overall Risk", level)

        with b:
            st.metric("Risk Score", f"{overall_score}/100")

        with c:
            st.metric("Likelihood", f"{likelihood_score}/100")

        with d:
            st.metric("Impact", f"{impact_score}/100")

        st.markdown("### Enterprise Risk Dashboard")

        score_card_1, score_card_2, score_card_3, score_card_4 = st.columns(4, gap="medium")

        with score_card_1:
            st.metric("Overall Risk", level)

        with score_card_2:
            st.metric("Risk Score", f"{overall_score}/100")

        with score_card_3:
            st.metric("Likelihood", f"{likelihood_score}/100")

        with score_card_4:
            st.metric("Impact", f"{impact_score}/100")

        st.markdown("### Risk Visualizations")

        viz1, viz2 = st.columns(2, gap="medium")

        with viz1:
            st.subheader("NIST Function Scores")
            st.pyplot(bar_chart_fig)

        with viz2:
            st.subheader("Risk Posture Radar")
            st.pyplot(radar_chart_fig)

        st.subheader("Likelihood vs Impact Matrix")
        st.pyplot(matrix_chart_fig)

        st.markdown("### Risk Intelligence Summary")

        summary_col1, summary_col2 = st.columns(2, gap="medium")

        with summary_col1:
            st.subheader("Top Risk Categories")
            for category in risk_score.get("top_risk_categories", []):
                st.write(f"- {category}")

        with summary_col2:
            st.subheader("Executive Decision")
            st.info(risk_score.get("executive_decision", "Review required"))

        st.subheader("Scoring Rationale")
        st.write(risk_score.get("scoring_rationale", "No rationale returned."))

        tab1, tab2, tab3, tab4 = st.tabs(
            ["Report", "Scenario", "Architecture", "Export"]
        )

        with tab1:
            st.markdown("## Advisory Report")
            st.markdown(
                f"""
<div class="report-box">
{report}
</div>
""",
                unsafe_allow_html=True,
            )

        with tab2:
            st.markdown("## Assessed Scenario")
            st.info(question)

        with tab3:
            st.markdown("## System Architecture")
            st.markdown(
                """
<div class="glass-card">
<b>User Scenario</b><br>
↓<br>
<b>Streamlit Product UI</b><br>
↓<br>
<b>Multi-Agent Orchestrator</b><br>
↓<br>
<b>GOVERN / MAP / MEASURE / MANAGE Agents</b><br>
↓<br>
<b>Azure AI Search Retrieval over NIST AI RMF</b><br>
↓<br>
<b>Azure OpenAI Synthesis</b><br>
↓<br>
<b>Verified Source Advisory Report</b>
</div>
""",
                unsafe_allow_html=True,
            )

        with tab4:
            st.markdown("## Export")

            pdf_bytes = generate_pdf_report(
                question=question,
                report=report,
                risk_score=risk_score,
                scores=scores,
                bar_chart_fig=bar_chart_fig,
                radar_chart_fig=radar_chart_fig,
                matrix_chart_fig=matrix_chart_fig,
            )

            st.download_button(
                label="Download full PDF report",
                data=pdf_bytes,
                file_name="ai_risk_advisory_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

            st.download_button(
                label="Download Markdown report",
                data=report,
                file_name="ai_risk_advisory_report.md",
                mime="text/markdown",
                use_container_width=True,
            )

            if show_markdown:
                st.markdown("## Copyable Markdown")
                st.code(report, language="markdown")

            if show_markdown:
                st.markdown("## Copyable Markdown")
                st.code(report, language="markdown")