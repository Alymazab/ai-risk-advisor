# AI Risk Advisor

Live Demo:  
https://nist-ai-risk-advisor-encddzhaedgvd5hb.canadacentral-01.azurewebsites.net/

AI Risk Advisor is a multi-agent AI governance and risk assessment platform built using Azure AI services and aligned with the NIST AI Risk Management Framework (AI RMF 1.0).

The platform analyzes AI deployment scenarios, evaluates governance and operational risks, generates executive-style advisory reports, visualizes enterprise risk posture, and exports professional PDF reports with charts and intelligence summaries.

---

# Features

## Multi-Agent AI Architecture

Specialized AI agents aligned with NIST AI RMF functions:

- GOVERN Agent
- MAP Agent
- MEASURE Agent
- MANAGE Agent
- Orchestrator Agent
- Risk Scoring Agent
- NIST Playbook Intelligence Agent

---

## Enterprise Risk Dashboard

Interactive dashboard with:

- Executive risk scorecards
- NIST function scoring
- Risk radar chart
- Likelihood vs impact matrix
- Risk posture visualization
- Intelligence summaries
- Executive decision recommendations

---

## PDF Report Export

Generate downloadable executive-ready PDF reports including:

- Risk analysis
- Governance findings
- Visual charts
- Risk matrix
- Recommendations
- Source references
- Scoring rationale

---

# Azure AI Services Integration

Built using:

- Azure OpenAI
- Azure AI Search
- Azure Key Vault
- Azure App Service
- Streamlit
- Python

---

# Architecture

## Workflow

1. User submits AI deployment scenario
2. Specialized agents analyze the scenario
3. Azure AI Search retrieves NIST RMF context
4. NIST Playbook intelligence enriches recommendations
5. Orchestrator synthesizes enterprise report
6. Risk scoring engine evaluates posture
7. Dashboard visualizes results
8. PDF export generates executive report

---

# Tech Stack

## Backend

- Python
- Streamlit
- OpenAI SDK
- Azure SDK
- ReportLab
- Matplotlib

## Azure Services

- Azure OpenAI
- Azure AI Search
- Azure Key Vault
- Azure App Service

## AI Governance Standards

- NIST AI RMF 1.0
- NIST AI Playbook

---

# Example Scenarios

- Financial AI Chatbot
- Healthcare Diagnosis AI
- AI Hiring Assistant
- Enterprise Copilot
- AI Fraud Detection
- Autonomous Decision Systems

---

# Security Design

- Azure Key Vault secret management
- Managed Identity authentication
- Environment variable isolation
- Retrieval-grounded responses
- Verified source extraction
- Hallucination reduction prompting

---

# Screenshots

## Enterprise Dashboard

Add dashboard screenshot here.

## Risk Radar Visualization

Add radar chart screenshot here.

## Executive PDF Report

Add PDF export screenshot here.

---

# Local Development

## Clone Repository

```bash
git clone https://github.com/Alymazab/ai-risk-advisor.git
cd ai-risk-advisor
Create Virtual Environment
python -m venv .venv
Activate Environment
Windows
.venv\Scripts\activate
Linux / macOS
source .venv/bin/activate
Install Dependencies
pip install -r requirements.txt
Environment Variables

Create a .env file:

AZURE_KEY_VAULT_URL=

AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=
AZURE_OPENAI_CHAT_DEPLOYMENT=
AZURE_OPENAI_API_VERSION=

AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_INDEX_NAME=
Run Locally
streamlit run app/ui.py
Deployment

This project is deployed on Azure App Service using:

GitHub Actions
Azure App Service Linux
Managed Identity
Azure Key Vault integration
Future Enhancements
Live internet threat intelligence
OWASP LLM attack simulation
Real-time compliance mapping
Advanced risk analytics
SOC integration
Executive governance analytics
RAG evaluation metrics
Threat trend monitoring
Resume Bullet

Built an enterprise-style multi-agent AI governance and risk assessment platform using Azure OpenAI, Azure AI Search, Azure Key Vault, and Streamlit, aligned with the NIST AI RMF to generate executive AI risk reports, interactive dashboards, and downloadable PDF intelligence assessments.