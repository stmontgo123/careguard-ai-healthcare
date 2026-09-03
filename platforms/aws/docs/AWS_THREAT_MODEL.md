# ClaimGuard AWS Threat Model

## Assets

- synthetic claim, authorization and FHIR evidence;
- role and purpose assertions;
- approved policy content;
- model prompt and grounded output;
- pending action and human decision;
- audit evidence;
- AWS credentials and execution role.

## Trust boundaries

1. User/session to deterministic authorization.
2. Authorization to FHIR/claim evidence retrieval.
3. Filtered evidence to policy ranking.
4. Minimum context to deterministic or Bedrock reasoning.
5. Recommendation to human approval.
6. Runtime to audit/logging.

## Key threats and controls

| Threat | Control | Acceptance evidence |
|---|---|---|
| Cross-member access | Exact member and assigned-case check | Test denies before model call |
| Wrong purpose | Role-purpose allow-list | Test denies TREATMENT for claims role |
| Excessive chart retrieval | FHIR type allow-list and field minimization | DiagnosticReport excluded |
| Special-category disclosure | Sensitivity labels and explicit-consent gate | SUD-tagged document excluded |
| Prompt injection | Retrieved text treated as data, flagged and sanitized | Malicious instruction removed |
| Stale policy | approved/current predicate before ranking | Superseded rule absent |
| Model overreach | No submission tool; PENDING action only | Action type is preparation, not submission |
| Output down-classification | Highest-source classification inheritance | Output remains RESTRICTED |
| Credential leakage | Standard AWS credential chain; no keys in Git | Example env contains no secrets |
| Runaway spend | Deterministic default, no DB/NAT/ALB, teardown | SAM stack is minimal |

## Out of scope

The public proof of concept does not provide production identity federation, BAA/legal determination, clinical safety validation, payer integration, high availability, disaster recovery, formal model evaluation, enterprise retention, immutable audit storage or autonomous claim submission.
