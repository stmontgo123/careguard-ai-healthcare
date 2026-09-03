# AWS infrastructure

The default stack is intentionally small:

~~~text
Browser or curl -> API Gateway HTTP API -> Lambda -> deterministic ClaimGuard control flow
~~~

It deploys no database, vector service, NAT gateway, load balancer, or always-on compute. The request and response use synthetic data bundled with the function.

## Deploy

From platforms/aws:

~~~bash
sam build --template-file infra/template.yaml
sam deploy --guided --stack-name careguard-claim-guard-demo
~~~

Use MODEL_PROVIDER=deterministic for the no-model-cost baseline. Bedrock is an optional enhancement:

1. Confirm the model is available in the selected Region.
2. Attach only policy/optional-bedrock-iam-policy.json to the function role.
3. Set MODEL_PROVIDER=bedrock.
4. Set a short test window and monitor billing.

The template deliberately does not grant Bedrock access by default.

## Remove

~~~bash
sam delete --stack-name careguard-claim-guard-demo
~~~

AWS Free Tier eligibility depends on the account and current AWS terms. API Gateway, Lambda, CloudWatch, data transfer, and Bedrock may incur charges. See ../docs/AWS_COST_CONTROL.md.
