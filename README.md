# CareGuard AI - Secure Enterprise AI for Healthcare

**A multicloud, synthetic-data portfolio showing how AI can improve healthcare operations without making the model the authorization layer.**

CareGuard now contains two governed workflows:

| Module | Scenario | Primary implementation |
|---|---|---|
| Care coordination | What is preventing discharge readiness? | Oracle Database 26ai + local/swapppable LLM |
| ClaimGuard | Why was an authorized MRI claim denied? | AWS serverless + optional Amazon Bedrock |

## One control model, multiple clouds

~~~text
Identity + role + purpose
        -> deterministic authorization
        -> patient/member and case scope
        -> permitted structured data + approved policy
        -> minimum authorized context
        -> replaceable reasoning model
        -> PENDING action
        -> human approval / rejection
        -> audit
~~~

The model can retrieve, summarize and recommend. It cannot widen access, submit a claim, place an order, change medication, bypass approval or rewrite security policy.

## Choose an implementation

### Oracle care-coordination module

The existing root src/, sql/, scripts/, demo/ and docs/ directories contain the Oracle Database 26ai / local-model discharge-readiness proof of concept.

~~~bash
python -m src.healthcare_rag_demo --no-ollama
python scripts/security_tests.py
~~~

### AWS ClaimGuard module

[Open the AWS implementation](platforms/aws/README.md)

~~~bash
cd platforms/aws
python3 -m src.cli
python3 -m unittest discover -s tests -p "test_*.py" -v
~~~

The AWS baseline uses only the Python standard library and synthetic JSON. The optional SAM stack deploys API Gateway and Lambda. Amazon Bedrock is opt-in and has no permission in the default stack.

## Anchor ClaimGuard case

Synthetic member Maria Lopez receives an MRI. Prior authorization PA-55219 and the EHR order specify CPT 73721, but claim CLM-784291 is submitted as CPT 73722 and denied with CO-197.

ClaimGuard verifies the claims specialist, PAYMENT purpose and case assignment; retrieves only minimum-necessary FHIR evidence; filters approved policy before ranking; recommends a correction or UM escalation; creates a PENDING action; and records an audit trail.

## Security acceptance principles

- deny wrong purpose, wrong member, wrong encounter/case and unassigned work before model access;
- exclude unrelated clinical narrative and specially protected records;
- treat retrieved instructions as untrusted data;
- exclude stale/unapproved policy before ranking;
- propagate the highest source classification to generated output;
- expose no raw SQL, broad-chart, clinical-action or autonomous-submission tool;
- keep consequential action human-owned;
- retain an auditable sequence of evidence, recommendation and approval.

## Safety boundary

All records and policies are fictional. Do not place real PHI/ePHI, credentials, EHR tokens, database wallets or AWS keys in this repository.

This project demonstrates technical control patterns. It is not a diagnostic system and does not claim HIPAA compliance, HIPAA certification, payer-policy correctness or production readiness. Production use requires organization-specific legal, privacy, security, clinical/operational, vendor/BAA, identity, monitoring, resilience and model-governance work.

## Portfolio artifacts

- Existing Oracle executive deck, build runbook and threat model: docs/
- AWS application, infrastructure and demo package: platforms/aws/
- AWS deck, runbooks, cost guide, threat model and interview Q&A: platforms/aws/docs/

## Portfolio thesis

> The model is replaceable. Authorization, scope, trusted evidence, bounded tools, human approval and auditability are the architecture.
