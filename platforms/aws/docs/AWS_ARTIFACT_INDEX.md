# ClaimGuard AWS Artifact Index

## Application

- ../app.py - polished Streamlit interface
- ../src/cli.py - dependency-free command-line demo
- ../src/orchestrator.py - bounded claim-resolution workflow
- ../src/authorization.py - role, purpose, case, resource and label controls
- ../src/retrieval.py - filter-first policy retrieval and injection handling
- ../src/bedrock.py - deterministic baseline plus optional Bedrock adapter

## Synthetic data

- ../demo/synthetic_case.json - anchor denial case
- ../demo/ehr_fhir_bundle.json - labeled FHIR-shaped evidence
- ../demo/policies.json - current, stale and hostile policy examples

## AWS

- ../infra/template.yaml - small SAM stack
- ../infra/policy/optional-bedrock-iam-policy.json - opt-in model permission
- ../scripts/deploy.sh and ../scripts/destroy.sh - lifecycle helpers

## Assurance

- ../tests/test_security.py - ten security acceptance tests
- AWS_SECURITY_AND_PRIVACY.md - classification and EHR boundary
- AWS_THREAT_MODEL.md - threats and controls
- AWS_COST_CONTROL.md - free-first operating guide

## Presentation

- supporting/ClaimGuard_AI_AWS_Executive_Demo_Deck.pptx
- supporting/ClaimGuard_AI_AWS_Executive_Demo_Deck.pdf

## Runbooks

- AWS_BUILD_RUNBOOK.md
- AWS_DEMO_RUNBOOK.md
- AWS_DECISION_RATIONALE.md
- INTERVIEW_QA.md
