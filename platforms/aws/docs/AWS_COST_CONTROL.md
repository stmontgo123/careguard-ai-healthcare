# AWS Cost-Control Guide

## Cost posture

The default ClaimGuard demo is free to run locally. The AWS stack is designed for short-lived, low-volume demonstrations, but no AWS deployment is guaranteed to be free.

| Component | Default | Cost control |
|---|---|---|
| Python CLI | Local deterministic | No cloud account or hosted model |
| Streamlit | Local | Stop the process after the demo |
| Lambda | 256 MB ARM64, 10-second timeout | No provisioned concurrency |
| API Gateway | HTTP API | Invoke only during the demo |
| Bedrock | Disabled | No permission in default SAM stack |
| Database/vector store | None | Synthetic JSON bundled with Lambda |
| NAT gateway | None | Avoid hourly and data-processing charges |
| Load balancer | None | Avoid hourly charges |
| Persistent storage | None | No demo database to forget |

## Before deployment

1. Review current AWS pricing and Free Tier terms for the selected account and Region.
2. Create an AWS Budget and low-dollar alert.
3. Use a dedicated demo stack and tags.
4. Keep MODEL_PROVIDER=deterministic.
5. Confirm the template creates only the expected API and Lambda.

## During the demo

- Use one synthetic case.
- Do not load production datasets.
- Avoid repeated automated invocations.
- Watch CloudWatch logs and Lambda duration.
- If Bedrock is enabled, use temperature 0, a small token limit and a short test window.

## After the demo

~~~bash
sam delete --stack-name careguard-claim-guard-demo
~~~

Then confirm deletion in CloudFormation and check Billing/Cost Explorer. Remove any temporary Bedrock permission.
