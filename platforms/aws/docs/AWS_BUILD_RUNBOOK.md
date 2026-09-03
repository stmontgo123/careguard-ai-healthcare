# ClaimGuard AI AWS Build Runbook

## Purpose

Build and deploy the synthetic ClaimGuard denied-claim demonstration with the smallest practical AWS footprint. The local deterministic path is the required baseline; the AWS and Bedrock paths are optional.

## Guardrails

- Synthetic data only. Never load PHI/ePHI, production EHR exports, credentials, tokens or payer secrets.
- The public code demonstrates technical control patterns, not HIPAA compliance or certification.
- Authorization, classification and minimum-necessary filtering run before policy ranking and before any model call.
- The model has no submit, appeal, payment, coding-change or clinical-action tool.
- Every proposed resolution remains PENDING until human review.

## Local build

~~~bash
git clone https://github.com/stmontgo123/careguard-ai-healthcare.git
cd careguard-ai-healthcare/platforms/aws
python3 -m src.cli
python3 -m unittest discover -s tests -p "test_*.py" -v
~~~

Expected: ten security tests pass and the demo produces a grounded recommendation with a PENDING action.

## Optional UI

~~~bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
~~~

## Optional AWS deployment

Prerequisites: AWS CLI, AWS SAM CLI and an authenticated least-privilege deployment profile.

~~~bash
aws sts get-caller-identity
cd platforms/aws
sam validate --template-file infra/template.yaml
sam build --template-file infra/template.yaml
sam deploy --guided --stack-name careguard-claim-guard-demo
~~~

Select a short-lived demonstration stack, retain MODEL_PROVIDER=deterministic, and record the generated API endpoint. The default stack creates one API Gateway HTTP API and one Lambda.

## Validate

~~~bash
curl -sS "https://YOUR_API_ID.execute-api.YOUR_REGION.amazonaws.com/demo/cases/CASE-2026-0917/investigate"
~~~

Confirm:

- synthetic_data_only is true;
- the recommendation identifies the 73722-to-73721 mismatch;
- output_classification is RESTRICTED;
- action.status is PENDING;
- no raw diagnostic report or specially protected document appears;
- the audit sequence includes authorization, FHIR retrieval, policy retrieval, model response and action request.

## Optional Bedrock test

Do this only after reviewing current AWS pricing, Region/model availability, service terms, logging settings, and BAA requirements.

1. Attach the example least-privilege Bedrock policy to the Lambda role.
2. Set MODEL_PROVIDER=bedrock.
3. Limit the test window and invoke only the synthetic case.
4. Confirm the model receives the minimized evidence payload, not the original bundle.
5. Remove the policy and return MODEL_PROVIDER to deterministic after the test.

## Teardown

~~~bash
sam delete --stack-name careguard-claim-guard-demo
~~~

Verify the CloudFormation stack is gone and review billing/Cost Explorer for unexpected usage.
