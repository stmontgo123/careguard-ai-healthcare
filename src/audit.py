from pathlib import Path
from datetime import datetime, timezone
import json
import uuid

DEFAULT_AUDIT_PATH = Path("careguard_audit.jsonl")

def audit_event(event_type: str, payload: dict, path: str | Path = DEFAULT_AUDIT_PATH) -> dict:
    event = {
        "event_id": str(uuid.uuid4()),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        **payload,
    }
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, sort_keys=True) + "\n")
    return event
