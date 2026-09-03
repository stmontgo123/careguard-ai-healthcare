from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class AccessContext:
    user_id: str
    role: str
    purpose: str
    member_id: str | None = None
    case_id: str | None = None
    assigned_case_ids: tuple[str, ...] = ()


@dataclass
class AuditEvent:
    stage: str
    outcome: str
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PendingAction:
    action_id: str
    case_id: str
    action_type: str
    recommendation: str
    status: str = "PENDING"
    reviewed_by: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
