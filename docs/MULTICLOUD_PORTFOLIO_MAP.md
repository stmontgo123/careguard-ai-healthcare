# CareGuard Multicloud Portfolio Map

| Control | Oracle care coordination | AWS ClaimGuard |
|---|---|---|
| Identity | Synthetic workforce context | Claims-specialist session |
| Purpose | CARE_COORDINATION | PAYMENT |
| Scope | Patient + encounter | Member + assigned case |
| Structured evidence | Oracle SQL facts | FHIR-shaped synthetic JSON |
| Knowledge retrieval | Authorized Oracle vector path / mock ranker | Filter-first deterministic ranker |
| Reasoning | Local/swapppable LLM | Deterministic baseline / optional Bedrock |
| Consequential action | Draft care-coordination task | Draft corrected-claim package |
| Approval | Authorized healthcare staff | Authorized claims specialist |
| Audit | Request, evidence, recommendation, decision | Authorization, FHIR, policy, model, action, decision |

The cloud services change. The governance contract does not.
