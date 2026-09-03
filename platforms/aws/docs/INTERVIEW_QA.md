# ClaimGuard Interview Q&A

## What is the business value?

It compresses a multi-system denial investigation into a cited resolution package. The measurable outcomes would be reduced touches per denial, shorter resolution time, higher clean-claim rate, lower appeal leakage and fewer unnecessary chart disclosures.

## Where is the agentic behavior?

The orchestrator performs a bounded sequence: authorize, gather facts, filter FHIR resources, retrieve policy, synthesize, propose an action and request approval. It is agentic in workflow, not autonomous in authority.

## Why is the LLM not the authorization layer?

Model behavior is probabilistic. Identity, purpose, member/case scope, classification, policy approval and tool permissions need deterministic enforcement before model context exists.

## Is this HIPAA compliant?

No compliance claim is made. The public demo is synthetic and illustrates HIPAA-aligned technical patterns. Production compliance depends on organization-wide administrative, physical and technical safeguards, contracts, risk analysis, workforce practices and legal review.

## Why not send the whole chart and redact later?

That expands the disclosure and prompt boundary unnecessarily. ClaimGuard filters by role, purpose, case, FHIR type and sensitivity first, then constructs only the payment-task fields.

## How does this relate to the banking demo?

The declined transaction becomes a denied claim; account/fraud evidence becomes coverage, authorization and EHR evidence; the fraud procedure becomes payer policy; a retry request becomes a corrected-claim package; human approval and audit remain identical.

## What is actually AWS-native?

The optional deployment uses AWS SAM, API Gateway HTTP API, Lambda, IAM and CloudWatch logging. Bedrock is supported through an opt-in adapter and least-privilege policy, but the default stack does not grant model access.

## Why not Aurora and pgvector like the bank demo?

They are valid production options but unnecessary for a one-case demonstration. The demo avoids persistent services to keep cost and setup low. The authorization and retrieval interfaces are designed to be replaceable.

## What would you build next?

A prior-authorization module using FHIR Coverage, ServiceRequest, QuestionnaireResponse and Da Vinci DTR/PAS patterns, with the same authorization-first and human-approval controls.
