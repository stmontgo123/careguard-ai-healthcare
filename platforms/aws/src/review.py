from __future__ import annotations

from .models import AuditEvent, PendingAction


def review_action(
    action: PendingAction,
    decision: str,
    reviewer_id: str,
    *,
    audit_sink=lambda event: None,
) -> PendingAction:
    decision = decision.strip().upper()
    if action.status != "PENDING":
        raise ValueError("Only PENDING actions may be reviewed")
    if decision not in {"APPROVE", "REJECT"}:
        raise ValueError("Decision must be APPROVE or REJECT")
    action.status = "APPROVED" if decision == "APPROVE" else "REJECTED"
    action.reviewed_by = reviewer_id
    audit_sink(AuditEvent("HUMAN_REVIEW", action.status, {
        "action_id": action.action_id,
        "reviewer_id": reviewer_id,
    }))
    return action
