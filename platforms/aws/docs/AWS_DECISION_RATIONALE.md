# AWS Decision Rationale and Defense Guide

## Why this use case

Claim denial resolution is financially measurable, operationally repetitive and evidence-heavy. It also exposes the governance problem cleanly: the system needs enough EHR and payer context to explain the exception, but not the entire chart.

## Why the deterministic baseline comes first

The valuable architecture is authorization, minimization, evidence, approval and audit. Keeping the baseline model-free makes the controls reproducible in interviews, CI and workshops without AWS credentials or usage charges.

## Why serverless AWS

API Gateway plus Lambda gives the repository a real AWS deployment path without always-on compute, database, NAT gateway or load balancer. The stack is disposable and easy to explain.

## Why Bedrock is optional

Bedrock can improve natural-language synthesis, but it should not become the security boundary or a prerequisite for the demo. The application performs authorization and builds minimum context before any invoke-model call.

## Why FHIR-shaped data

FHIR resources make the EHR boundary visible and allow security labeling, purpose-of-use, consent and provenance concepts to be discussed using industry language. The public dataset remains synthetic.

## Why no vector database

Four small demo policies do not justify persistent vector infrastructure. Filter-first deterministic ranking proves the security order of operations at zero cost. Production can replace the ranker with an approved vector service without changing the authorization contract.

## Why no autonomous submission

A corrected claim can have financial, contractual and compliance consequences. ClaimGuard prepares a resolution package and stops at PENDING. A human verifies coding and owns submission or escalation.

## Production evolution

Replace synthetic JSON with governed payer/EHR adapters; federate identity; enforce DS4P/consent/jurisdiction rules; use private connectivity and KMS; add persistent audit/provenance; evaluate models; create segregation-of-duties approvals; and complete legal, privacy, security and BAA review.
