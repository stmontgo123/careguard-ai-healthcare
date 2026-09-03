from __future__ import annotations

import argparse
import json

from .models import AccessContext, AuditEvent
from .orchestrator import investigate_claim


def main() -> None:
    parser = argparse.ArgumentParser(description="ClaimGuard AWS synthetic claim-denial demo")
    parser.add_argument("--case-id", default="CASE-2026-0917")
    parser.add_argument("--json", action="store_true", help="Print machine-readable output")
    args = parser.parse_args()

    events: list[AuditEvent] = []
    ctx = AccessContext(
        user_id="claims-demo-01",
        role="CLAIMS_SPECIALIST",
        purpose="PAYMENT",
        member_id="MEM-2048",
        case_id=args.case_id,
        assigned_case_ids=(args.case_id,),
    )
    result = investigate_claim(ctx, args.case_id, audit_sink=events.append)

    if args.json:
        print(json.dumps({"result": result, "audit": [event.to_dict() for event in events]}, indent=2))
        return

    print("\nCLAIMGUARD AI - AWS EDITION")
    print("Synthetic data only - no real PHI/ePHI\n")
    for number, event in enumerate(events, start=1):
        print(f"[{number}] {event.stage}: {event.outcome}")
    print("\nGROUNDED RECOMMENDATION")
    print(result["recommendation"])
    print(f"\nAction: {result['action']['action_id']} | Status: {result['action']['status']}")
    print("AI has not submitted, corrected, or appealed the claim.")


if __name__ == "__main__":
    main()
