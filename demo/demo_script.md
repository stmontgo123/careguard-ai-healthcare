# CareGuard AI Demo Script

1. Run the baseline:
   `python -m src.healthcare_rag_demo --no-ollama`
2. Show the synthetic encounter facts and approved evidence sources.
3. Point out that authorization occurs before retrieval.
4. Show the injected document is flagged and sanitized.
5. Show the draft action remains in `DRAFT` / `PENDING` approval state.
6. Run:
   `python scripts/security_tests.py`
7. Close with:
   **The model is replaceable. Authorization, patient scope, evidence, bounded tools, human approval, and auditability are the architecture.**
