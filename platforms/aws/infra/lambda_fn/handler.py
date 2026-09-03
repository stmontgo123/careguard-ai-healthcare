from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.models import AccessContext
from src.orchestrator import investigate_claim


def lambda_handler(event, _context):
    case_id = (event.get("pathParameters") or {}).get("case_id", "CASE-2026-0917")
    ctx = AccessContext(
        user_id="claims-demo-01",
        role="CLAIMS_SPECIALIST",
        purpose="PAYMENT",
        member_id="MEM-2048",
        case_id=case_id,
        assigned_case_ids=(case_id,),
    )
    audit = []
    result = investigate_claim(ctx, case_id, audit_sink=audit.append)
    return {
        "statusCode": 200,
        "headers": {
            "content-type": "application/json",
            "cache-control": "no-store",
        },
        "body": json.dumps({
            "synthetic_data_only": True,
            "result": result,
            "audit": [item.to_dict() for item in audit],
        }),
    }
