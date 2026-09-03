from __future__ import annotations

from collections.abc import Iterable

from .models import AccessContext


class AuthorizationError(PermissionError):
    """Raised before any protected case content is retrieved."""


ROLE_RULES = {
    "CLAIMS_SPECIALIST": {
        "purposes": {"PAYMENT"},
        "classes": {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"},
        "resource_types": {
            "Patient", "Coverage", "ServiceRequest", "Claim", "ClaimResponse",
            "DocumentReference", "Provenance", "AuditEvent",
        },
    },
    "UTILIZATION_MANAGEMENT": {
        "purposes": {"PAYMENT", "UTILIZATION_MANAGEMENT"},
        "classes": {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"},
        "resource_types": {
            "Patient", "Coverage", "ServiceRequest", "Claim", "ClaimResponse",
            "DocumentReference", "Condition", "DiagnosticReport", "Provenance",
            "AuditEvent",
        },
    },
    "PRIVACY_SECURITY": {
        "purposes": {"PRIVACY_REVIEW", "SECURITY_REVIEW"},
        "classes": {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED", "HIGHLY_RESTRICTED"},
        "resource_types": {"AuditEvent", "Provenance", "Consent"},
    },
    "EXECUTIVE_READONLY": {
        "purposes": {"EXECUTIVE_REPORTING"},
        "classes": {"PUBLIC", "AGGREGATED"},
        "resource_types": set(),
    },
}

SPECIAL_SENSITIVITY = {"SUD", "PSYCH-NOTE", "HIV", "GENETIC"}
CLASS_RANK = {
    "PUBLIC": 0,
    "INTERNAL": 1,
    "CONFIDENTIAL": 2,
    "RESTRICTED": 3,
    "HIGHLY_RESTRICTED": 4,
}


def normalize(value: str | None) -> str:
    return (value or "").strip().upper()


def authorize_context(ctx: AccessContext) -> None:
    role = normalize(ctx.role)
    purpose = normalize(ctx.purpose)
    if role not in ROLE_RULES:
        raise AuthorizationError(f"Unknown role: {role}")
    if purpose not in ROLE_RULES[role]["purposes"]:
        raise AuthorizationError(f"Role {role} is not authorized for purpose {purpose}")
    if role in {"CLAIMS_SPECIALIST", "UTILIZATION_MANAGEMENT"}:
        if not ctx.member_id or not ctx.case_id:
            raise AuthorizationError("Member and case scope are required")
        if ctx.case_id not in ctx.assigned_case_ids:
            raise AuthorizationError("Case is not assigned to this workforce user")


def _labels(resource: dict) -> set[str]:
    security = resource.get("meta", {}).get("security", [])
    return {normalize(label.get("code")) for label in security if label.get("code")}


def _classification(resource: dict) -> str:
    labels = _labels(resource)
    present = [name for name in CLASS_RANK if name in labels]
    return max(present, key=CLASS_RANK.get) if present else "INTERNAL"


def filter_authorized_resources(
    ctx: AccessContext,
    resources: Iterable[dict],
) -> list[dict]:
    """Filter by identity, purpose, case, FHIR type and security label before ranking or AI."""
    authorize_context(ctx)
    rules = ROLE_RULES[normalize(ctx.role)]
    output: list[dict] = []
    for resource in resources:
        access = resource.get("_demo_access", {})
        if resource.get("resourceType") not in rules["resource_types"]:
            continue
        if access.get("member_id") and access["member_id"] != ctx.member_id:
            continue
        if access.get("case_id") and access["case_id"] != ctx.case_id:
            continue
        purposes = {normalize(x) for x in access.get("allowed_purposes", [])}
        if purposes and normalize(ctx.purpose) not in purposes:
            continue
        roles = {normalize(x) for x in access.get("allowed_roles", [])}
        if roles and normalize(ctx.role) not in roles:
            continue
        labels = _labels(resource)
        if labels & SPECIAL_SENSITIVITY and not access.get("explicit_consent", False):
            continue
        if _classification(resource) not in rules["classes"]:
            continue
        output.append(resource)
    return output


def inherited_output_classification(resources: Iterable[dict]) -> str:
    classes = [_classification(resource) for resource in resources]
    return max(classes, key=CLASS_RANK.get) if classes else "INTERNAL"
