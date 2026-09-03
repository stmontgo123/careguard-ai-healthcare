from __future__ import annotations

import json
import os


def deterministic_recommendation(case: dict, evidence: dict, policies: list[dict]) -> str:
    policy_ids = ", ".join(item["policy_id"] for item in policies if item.get("score", 0) > 0)
    return (
        f"Claim {case['claim_id']} was denied with {case['denial_code']} because the submitted "
        f"procedure {case['submitted_cpt']} does not match prior authorization {case['authorization_id']} "
        f"or the EHR order, both of which specify {evidence['authorized_cpt']}. "
        f"Recommended next step: verify the coding against the source document, then prepare a corrected "
        f"claim using {evidence['authorized_cpt']}. If documentation supports the submitted code instead, "
        "route the case to Utilization Management for appeal review. No claim is submitted automatically. "
        f"Sources: {policy_ids or 'MRI-PA-04, HIPAA-MIN-01'}."
    )


def generate_recommendation(prompt: str, case: dict, evidence: dict, policies: list[dict]) -> tuple[str, str]:
    provider = os.getenv("MODEL_PROVIDER", "deterministic").strip().lower()
    if provider != "bedrock":
        return deterministic_recommendation(case, evidence, policies), "deterministic"

    try:
        import boto3
    except ImportError as exc:
        raise RuntimeError("Install optional dependencies before MODEL_PROVIDER=bedrock") from exc

    model_id = os.getenv("BEDROCK_GEN_MODEL", "amazon.nova-lite-v1:0")
    client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))
    body = {
        "messages": [{"role": "user", "content": [{"text": prompt}]}],
        "inferenceConfig": {"maxTokens": 600, "temperature": 0.0},
    }
    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json",
    )
    payload = json.loads(response["body"].read())
    text = payload["output"]["message"]["content"][0]["text"].strip()
    return text, f"bedrock:{model_id}"
