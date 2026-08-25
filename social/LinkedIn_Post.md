# LinkedIn post - CareGuard AI

I built another version of my secure enterprise AI demo - this time for healthcare.

**CareGuard AI** is a HIPAA-aligned RAG and agentic AI proof of concept built around a synthetic discharge-coordination scenario. No real PHI is used.

The interesting part is not the chatbot. It is the control model around it:

- role, purpose-of-use and patient scope before retrieval
- minimum-necessary data before model context
- approved/current policy sources for RAG
- Oracle Database 26ai for structured facts, vector search and audit
- a local LLM to keep the base demo inside a controlled data boundary
- human approval before consequential workflow actions
- security tests for cross-patient access, prompt injection, stale policy, bulk export and excessive agency

The core design principle is simple: **the LLM is not the security boundary.**

HIPAA obligations still require an organization-specific risk analysis, governance, policies, training, contracts/BAAs where applicable, and operational controls. The demo is designed to make those boundaries visible rather than hiding them behind a prompt.

**Secure by design. Evidence-driven. Human accountable.**

#HealthcareAI #HIPAA #RAG #AgenticAI #OracleDatabase #Oracle26ai #Cybersecurity #EnterpriseArchitecture #ResponsibleAI
