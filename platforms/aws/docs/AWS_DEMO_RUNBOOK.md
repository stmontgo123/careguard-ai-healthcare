# ClaimGuard AI One-Hour Demo Runbook

## Audience outcome

By the end, healthcare operations and technology leaders should see that AI can shorten claim-denial investigation while keeping PHI scope, decision authority and audit evidence explicit.

## 60-minute flow

| Time | Segment | What to show |
|---|---|---|
| 0-5 | Business problem | A paid-for MRI is denied because the claim does not match the order and authorization. |
| 5-12 | Case setup | Maria Lopez, claim CLM-784291, authorization PA-55219, 73722 submitted versus 73721 authorized. |
| 12-20 | Privacy boundary | PAYMENT purpose, assigned case, FHIR security labels, minimum-necessary fields. |
| 20-32 | Live investigation | Run the CLI or Streamlit app and narrate each governed stage. |
| 32-40 | Human approval | Show PENDING; approve preparation or reject and route to UM. No automatic submission. |
| 40-48 | Attack tests | Wrong purpose, unassigned case, cross-member request, prompt injection, stale policy. |
| 48-55 | AWS architecture | Local-free baseline, small SAM stack, optional Bedrock, least privilege. |
| 55-60 | Executive close | The model is replaceable; authorization, evidence, approval and audit are the architecture. |

## Pre-demo checklist

- Run python3 -m unittest discover -s tests -p "test_*.py" -v.
- Run python3 -m src.cli once.
- If using Streamlit, open the app and reset session state.
- If using AWS, invoke the endpoint and verify the stack has no Bedrock permission by default.
- Keep the executive deck, this runbook and INTERVIEW_QA.md open.

## Live narration

1. “This is the healthcare equivalent of tracing a failed bank transaction.”
2. “The EHR order and authorization agree on 73721; the submitted claim says 73722.”
3. “Before retrieving anything, the system verifies the claims role, PAYMENT purpose and case assignment.”
4. “FHIR labels and allowed resource types exclude the full diagnostic report and a specially protected record.”
5. “Approved and current policy is filtered before relevance ranking.”
6. “The reasoning layer explains the mismatch and cites policy, but creates only a PENDING action.”
7. “The claims specialist owns the decision; the audit trail records both AI and human stages.”

## Expected resolution

Prepare a corrected claim using CPT 73721 only after a human verifies the source order and coding. If the documentation supports 73722 instead, route the case to Utilization Management for appeal review.

## Recovery

- CLI issue: rerun from platforms/aws so the demo JSON resolves correctly.
- Streamlit issue: use the CLI; it is the dependency-free baseline.
- AWS issue: use local mode; the control story is identical.
- Bedrock issue: return MODEL_PROVIDER to deterministic.
