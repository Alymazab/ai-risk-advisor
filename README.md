# AI Risk Advisor (NIST AI RMF)

A multi-agent AI system that analyzes AI risk scenarios using the NIST AI Risk Management Framework (AI RMF 1.0). Built with Azure OpenAI, Azure AI Search, and Azure Key Vault.

---

## Overview

AI Risk Advisor translates the NIST AI RMF into an executable multi-agent system.

Given a real-world scenario (e.g., a customer-facing chatbot), the system:

1. Retrieves relevant framework context using Retrieval-Augmented Generation (RAG)
2. Runs specialized agents aligned with NIST functions:
   - GOVERN
   - MAP
   - MEASURE
   - MANAGE
3. Produces a structured AI Risk Advisory Report

---

## Architecture

User Query  
→ Retriever (Azure AI Search + Embeddings)  
→ Specialist Agents (GOVERN, MAP, MEASURE, MANAGE)  
→ Orchestrator Agent  
→ Final AI Risk Advisory Report

---

## Tech Stack

- Python
- Azure OpenAI (chat completions and embeddings)
- Azure AI Search (hybrid + vector search)
- Azure Key Vault (secure secret management)
- Streamlit (UI)

---

## Agents (NIST AI RMF)

GOVERN  
Focuses on governance, accountability, and organizational controls.

MAP  
Identifies context, stakeholders, impacts, and risk sources.

MEASURE  
Evaluates metrics, testing strategies, and monitoring requirements.

MANAGE  
Handles risk mitigation, prioritization, and response planning.

---

## Features

- Multi-agent architecture aligned to a real regulatory framework
- Retrieval-Augmented Generation (RAG)
- Source-grounded responses with page references
- Secure secret handling via Azure Key Vault
- Modular and extensible design

---

## Security

- No secrets stored in code or repository
- All sensitive keys retrieved from Azure Key Vault
- Uses DefaultAzureCredential for secure authentication

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Alymazab/ai-risk-advisor.git
cd ai-risk-advisor
```

---

### 2. Create .env from template

Copy `.env.example` to `.env` and fill in the following values:

```env
AZURE_KEY_VAULT_URL=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=
AZURE_OPENAI_CHAT_DEPLOYMENT=
AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_INDEX_NAME=
```

---

### 3. Azure Setup

You need the following resources:

- Azure OpenAI
- Azure AI Search
- Azure Key Vault

Add the following secrets to Azure Key Vault:

```
AZURE-OPENAI-API-KEY
AZURE-SEARCH-ADMIN-KEY
```

---

## Running the Project

### Upload and index data

```bash
python -m app.ingestion.upload_chunks_to_search
```

### Run orchestrator (CLI)

```bash
python -m app.agents.orchestrator
```

### Run UI

```bash
streamlit run app/ui.py
```

---

## Example Use Case

Input:

Assess the AI risks of deploying a customer-facing AI chatbot for a financial services company.

Output:

- Executive Summary  
- GOVERN Findings  
- MAP Findings  
- MEASURE Findings  
- MANAGE Findings  
- Actionable Recommendations  
- Verified NIST source references  

---

## Future Improvements

- Managed Identity (removing API keys entirely)
- Agent confidence scoring
- Prompt injection defenses
- Evaluation framework for outputs
- Deployment to Azure App Service or Container Apps

---

## Why this project matters

This project demonstrates:

- AI system design using a real-world governance framework  
- Multi-agent orchestration  
- RAG pipelines using enterprise cloud tools  
- Secure architecture with Azure Key Vault  
- Practical implementation of AI risk management  

---

## License

License to be added.