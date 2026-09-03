# ClaimGuard AI - AWS Edition

**A synthetic, security-first healthcare claim-denial demo that investigates a failed payment workflow without widening the PHI boundary.**

ClaimGuard applies the same control pattern as the Secure Agentic AI Banking Demo:

~~~text
Workforce identity + purpose
        -> deterministic authorization
        -> minimum-necessary FHIR evidence
        -> approved policy retrieval
        -> deterministic or Bedrock reasoning
        -> PENDING resolution package
        -> human approval / rejection
        -> audit trail
~~~

The model is not the authorization layer and cannot submit a claim.

## The one-hour demo

Synthetic member Maria Lopez received an MRI. Prior authorization PA-55219 and the EHR order both specify CPT 73721, but claim CLM-784291 was submitted as 73722 and denied with CO-197.

ClaimGuard:

1. authenticates a claims specialist and resolves the PAYMENT purpose;
2. verifies assignment to CASE-2026-0917;
3. filters FHIR resources by member, case, role, purpose, type and security label;
4. excludes unrelated clinical narrative and specially protected records;
5. filters approved/current policies before ranking;
6. explains the mismatch with citations;
7. creates a PENDING corrected-claim preparation action;
8. leaves approval and submission to an authorized human;
9. records each stage in the audit trail.

All data is fictional and synthetic.

## Run free, locally

~~~bash
cd platforms/aws
python3 -m src.cli
python3 -m unittest discover -s tests -p "test_*.py" -v
~~~

No AWS account, database, hosted model, package install, or credential is required.

## Optional polished UI

~~~bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
~~~

## Optional AWS serverless deployment

The SAM template deploys an API Gateway HTTP API and one ARM64 Lambda. It deliberately defaults to deterministic reasoning and grants no Bedrock permissions.

~~~bash
cd platforms/aws
./scripts/deploy.sh
~~~

See [AWS infrastructure](infra/README.md) and [cost controls](docs/AWS_COST_CONTROL.md). “Free-first” is a design goal, not a guarantee: eligibility and pricing depend on the AWS account, Region and usage.

## Optional Amazon Bedrock

~~~text
MODEL_PROVIDER=bedrock
AWS_REGION=us-east-1
BEDROCK_GEN_MODEL=amazon.nova-lite-v1:0
~~~

Then attach the narrowly scoped example policy in infra/policy/. Bedrock usage may incur charges. Verify current model availability, pricing, data-governance terms, and BAA eligibility before any production use.

## Evidence and privacy boundary

The public demo uses FHIR-shaped synthetic resources with security labels. The claims persona receives only payment-task fields: coverage status, service date, authorization ID, authorized CPT, submitted CPT, denial code and source IDs. A diagnostic report and a synthetic SUD-tagged document are excluded before model context.

This repository demonstrates technical safeguards; it does not claim HIPAA compliance, HIPAA certification, payer policy correctness, or production readiness.

## Artifact map

- [Build runbook](docs/AWS_BUILD_RUNBOOK.md)
- [One-hour demo runbook](docs/AWS_DEMO_RUNBOOK.md)
- [Privacy and EHR controls](docs/AWS_SECURITY_AND_PRIVACY.md)
- [Threat model](docs/AWS_THREAT_MODEL.md)
- [Cost controls](docs/AWS_COST_CONTROL.md)
- [Decision rationale](docs/AWS_DECISION_RATIONALE.md)
- [Interview Q&A](docs/INTERVIEW_QA.md)
- [Artifact index](docs/AWS_ARTIFACT_INDEX.md)
