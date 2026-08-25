from dataclasses import dataclass
from datetime import datetime, timezone
import uuid

@dataclass
class ApprovalRequest:
    request_id: str
    action_type: str
    summary: str
    status: str = "PENDING"
    approved_by: str | None = None
    decided_at: str | None = None

def create_approval(action_type: str, summary: str) -> ApprovalRequest:
    return ApprovalRequest(
        request_id=str(uuid.uuid4()),
        action_type=action_type,
        summary=summary,
    )

def approve(req: ApprovalRequest, user_id: str) -> ApprovalRequest:
    req.status = "APPROVED"
    req.approved_by = user_id
    req.decided_at = datetime.now(timezone.utc).isoformat()
    return req

def reject(req: ApprovalRequest, user_id: str) -> ApprovalRequest:
    req.status = "REJECTED"
    req.approved_by = user_id
    req.decided_at = datetime.now(timezone.utc).isoformat()
    return req
