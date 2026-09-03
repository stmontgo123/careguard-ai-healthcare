# AWS Security, Privacy and EHR Classification

## Classification model

ClaimGuard combines enterprise classification, HIPAA status, special sensitivity, purpose of use and FHIR security labels. No single label answers every access question.

| Dimension | Demo values | Enforcement |
|---|---|---|
| Enterprise class | PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED, HIGHLY_RESTRICTED | Role/class allow-list before retrieval |
| HIPAA status | Synthetic; production analog may be PHI/ePHI | Public demo blocks real data |
| Purpose | PAYMENT, UTILIZATION_MANAGEMENT, PRIVACY_REVIEW, SECURITY_REVIEW | Role-purpose pair validated before access |
| Special sensitivity | SUD, PSYCH-NOTE, HIV, GENETIC | Excluded without explicit authority/consent |
| FHIR type | Patient, Coverage, ServiceRequest, Claim, ClaimResponse, DocumentReference | Persona-specific resource allow-list |
| Case scope | Member and assigned case | Exact match before content access |

## Minimum necessary for the PAYMENT use case

The model receives only:

- synthetic member ID;
- coverage status;
- service date;
- authorization ID;
- authorized CPT;
- submitted CPT;
- denial code;
- source resource and policy IDs.

It does not receive the full diagnostic report, unrelated conditions, raw notes, specially protected documents, credentials or a broad chart export.

## FHIR application

Each synthetic resource carries meta.security labels plus demo-only access metadata. In production, policy evaluation should combine enterprise IAM, user attributes, purpose of use, case assignment, Consent, jurisdiction, data segmentation rules and FHIR security labels.

The derived AI recommendation inherits the highest confidentiality classification of the resources used to create it. Model output is not automatically “less sensitive” than its inputs.

## Model boundary

The model:

- never decides who may access data;
- receives only filtered evidence;
- treats retrieved text as untrusted;
- cannot query raw EHR or claims databases;
- cannot submit a claim or appeal;
- cannot override classification or policy;
- produces a draft with citations;
- remains replaceable.

## Logging

The demo audit records stage, outcome and identifiers. Production logs should avoid raw PHI, use encryption, least privilege, retention controls, immutable/centralized evidence where required, monitoring and incident response.

## Regulatory references

- HHS, Uses and Disclosures for Treatment, Payment, and Health Care Operations: https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/disclosures-treatment-payment-health-care-operations/index.html
- HHS, Minimum Necessary Requirement: https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/minimum-necessary-requirement/index.html
- HHS, De-identification of PHI: https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html
- HHS, 42 CFR Part 2: https://www.hhs.gov/hipaa/part-2/index.html
- HL7 FHIR Security Labels: https://www.hl7.org/fhir/security-labels.html

Validate current law, contracts, payer rules, AWS eligibility and organization-specific policy before production use.
