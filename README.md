# CareGuard AI

![CareGuard AI - Secure Enterprise AI for Healthcare](assets/healthcare-ai-hipaa-preview.png)

## Secure Enterprise AI for Healthcare - HIPAA-Aligned RAG Demo

CareGuard AI is a **synthetic-data-only** portfolio demonstration of secure Retrieval-Augmented Generation (RAG) and bounded agentic workflow for healthcare operations. It combines Oracle Database 26ai structured data + vector search with a local Large Language Model (LLM), deterministic authorization, minimum-necessary retrieval, human approval, and full auditability.

> **Important:** This repository is a design/demo pattern, not a claim of HIPAA certification or compliance. Do not load real PHI/ePHI into the demo.

## Demo use case

A synthetic care coordinator asks what remains before a synthetic knee-replacement patient can be discharged. The agent:

1. gathers authorized structured encounter facts;
2. retrieves only approved, role/purpose-authorized policies;
3. produces a grounded checklist with citations;
4. drafts a care-coordination action;
5. pauses for human approval; and
6. records an audit trail.

## Why it matters

Healthcare AI has to do more than answer questions. It must respect workforce identity, patient scope, minimum necessary access, trusted-source rules, workflow authority, auditability, and vendor/data-boundary obligations.

## Architecture

```text
Authenticated Browser
        |
        v
Role + Purpose + Patient-Scope Policy
        |
        v
Python Agent Orchestrator
   |         |
   |         +--> Local LLM / Local Embeddings
   |
   +--> Oracle Database 26ai
          - structured synthetic facts
          - VECTOR policy chunks
          - approvals
          - AI audit log
          - security events
```

## HIPAA-oriented design patterns

- **Minimum necessary:** filter fields and documents before they reach model context.
- **Access control:** role, purpose, assignment and patient scope drive authorization.
- **Audit controls:** record authorization, evidence, model/tool activity, approval and outcome.
- **Integrity:** only approved/current trusted policy content is authoritative.
- **Transmission security:** encrypted connections and restricted endpoints.
- **Business associates:** external services handling ePHI require appropriate BAA/vendor governance.
- **Human accountability:** no autonomous diagnosis, treatment order, disclosure, claim submission or external action in the base demo.

## Security tests

- Cross-patient access -> **DENY before LLM context**
- Overbroad data request -> **MINIMIZE**
- Prompt injection in policy -> **IGNORE as untrusted data**
- Stale/unapproved policy -> **EXCLUDE / FLAG**
- Auto-submit referral -> **BLOCK until human approval**
- Bulk export -> **BLOCK / ALERT**
- Secret request -> **DENY; secrets never enter context**

## Build order

1. OCI / database preflight
2. Synthetic schema + users/roles
3. Synthetic patient + policy data
4. Chunk + embed approved knowledge
5. Secure vector retrieval
6. SQL tools + orchestration
7. HIPAA/security guardrails
8. Human approval + audit
9. Attack-mode tests
10. Streamlit polish + executive demo

## Portfolio artifacts

- [`Executive Demo Deck (PPTX)`](docs/CareGuard_AI_HIPAA_Executive_Demo_Deck.pptx)
- [`Build Runbook (DOCX)`](docs/CareGuard_AI_HIPAA_Build_Runbook.docx)
- [`Security Architecture & Threat Model (DOCX)`](docs/CareGuard_AI_HIPAA_Security_Threat_Model.docx)
- [`LinkedIn Post`](social/LinkedIn_Post.md)
- [`Healthcare AI Preview`](assets/healthcare-ai-hipaa-preview.png)

## Regulatory note

As of August 25, 2026, HHS states that the current HIPAA Security Rule remains in effect while the December 2024 Security Rule cybersecurity changes remain proposed. Always validate the current rule, organizational obligations, BAAs, risk analysis, and applicable state/federal requirements before a production deployment.

### Primary references

- HHS Security Rule: https://www.hhs.gov/hipaa/for-professionals/security/index.html
- HHS HIPAA Security Rule NPRM: https://www.hhs.gov/hipaa/for-professionals/security/hipaa-security-rule-nprm/index.html
- HHS Guidance on HIPAA & Cloud Computing: https://www.hhs.gov/hipaa/for-professionals/special-topics/health-information-technology/cloud-computing/index.html
- HHS Minimum Necessary Requirement: https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/minimum-necessary-requirement/index.html
