from dataclasses import dataclass
from typing import Iterable

ROLE_RULES = {
    "CLINICIAN": {
        "purposes": {"TREATMENT", "CARE_COORDINATION"},
        "classes": {"PUBLIC", "INTERNAL", "CLINICAL"},
    },
    "CARE_COORDINATOR": {
        "purposes": {"CARE_COORDINATION", "OPERATIONS"},
        "classes": {"PUBLIC", "INTERNAL", "CARE_COORDINATION"},
    },
    "UTILIZATION_MANAGEMENT": {
        "purposes": {"UTILIZATION_MANAGEMENT"},
        "classes": {"PUBLIC", "INTERNAL", "UM"},
    },
    "PRIVACY_SECURITY": {
        "purposes": {"SECURITY_REVIEW", "PRIVACY_REVIEW"},
        "classes": {"PUBLIC", "INTERNAL", "SECURITY"},
    },
    "EXECUTIVE_READONLY": {
        "purposes": {"EXECUTIVE_REPORTING"},
        "classes": {"PUBLIC", "AGGREGATED"},
    },
}

@dataclass(frozen=True)
class AccessContext:
    user_id: str
    role: str
    purpose: str
    patient_id: str | None = None
    encounter_id: str | None = None

class AuthorizationError(PermissionError):
    pass

def normalize(value: str | None) -> str:
    return (value or "").strip().upper()

def authorize_context(ctx: AccessContext) -> None:
    role = normalize(ctx.role)
    purpose = normalize(ctx.purpose)
    if role not in ROLE_RULES:
        raise AuthorizationError(f"Unknown role: {role}")
    if purpose not in ROLE_RULES[role]["purposes"]:
        raise AuthorizationError(f"Role {role} is not authorized for purpose {purpose}")

def allowed_classifications(ctx: AccessContext) -> set[str]:
    authorize_context(ctx)
    return ROLE_RULES[normalize(ctx.role)]["classes"]

def filter_authorized_documents(ctx: AccessContext, documents: Iterable[dict]) -> list[dict]:
    allowed = allowed_classifications(ctx)
    out = []
    for doc in documents:
        if normalize(doc.get("classification")) not in allowed:
            continue
        if not doc.get("approved", False):
            continue
        patient_id = doc.get("patient_id")
        encounter_id = doc.get("encounter_id")
        if patient_id and patient_id != ctx.patient_id:
            continue
        if encounter_id and encounter_id != ctx.encounter_id:
            continue
        purposes = {normalize(p) for p in doc.get("allowed_purposes", [])}
        if purposes and normalize(ctx.purpose) not in purposes:
            continue
        roles = {normalize(r) for r in doc.get("allowed_roles", [])}
        if roles and normalize(ctx.role) not in roles:
            continue
        out.append(doc)
    return out

def require_patient_scope(ctx: AccessContext, patient_id: str, encounter_id: str | None = None) -> None:
    authorize_context(ctx)
    if patient_id != ctx.patient_id:
        raise AuthorizationError("Cross-patient access denied")
    if encounter_id and ctx.encounter_id and encounter_id != ctx.encounter_id:
        raise AuthorizationError("Wrong-encounter access denied")
