from .authz import AccessContext, require_patient_scope, AuthorizationError

SYNTHETIC_ENCOUNTERS = {
    ("PAT-1001", "ENC-240817"): {
        "patient_id": "PAT-1001",
        "encounter_id": "ENC-240817",
        "synthetic_name": "Jordan Lee",
        "procedure": "Synthetic knee-replacement encounter",
        "medication_reconciliation": "COMPLETE",
        "follow_up": "SCHEDULED",
        "home_oxygen": "PENDING_VENDOR_CONFIRMATION",
        "transportation": "PENDING_FAMILY_CONFIRMATION",
        "discharge_order": "NOT_PLACED",
    }
}

def get_encounter_summary(ctx: AccessContext, patient_id: str, encounter_id: str) -> dict:
    require_patient_scope(ctx, patient_id, encounter_id)
    key = (patient_id, encounter_id)
    if key not in SYNTHETIC_ENCOUNTERS:
        raise KeyError("Synthetic encounter not found")
    return SYNTHETIC_ENCOUNTERS[key].copy()

ALLOWED_ACTIONS = {"DRAFT_CARE_COORDINATION_TASK"}

def request_action(action_type: str, payload: dict) -> dict:
    if action_type not in ALLOWED_ACTIONS:
        raise AuthorizationError(
            f"Action {action_type} is not exposed to the model. Consequential clinical actions are blocked."
        )
    return {"action_type": action_type, "status": "DRAFT", "payload": payload}
