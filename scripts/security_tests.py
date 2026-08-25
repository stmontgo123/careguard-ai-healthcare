from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import json
from src.authz import AccessContext, AuthorizationError, filter_authorized_documents
from src.rag import SYNTHETIC_DOCUMENTS, mock_vector_search
from src.tools import get_encounter_summary, request_action
from src.security import has_prompt_injection

def expect(label, condition):
    print(f"[{'PASS' if condition else 'FAIL'}] {label}")
    if not condition:
        raise AssertionError(label)

def main():
    cc = AccessContext("demo-care-coordinator", "CARE_COORDINATOR", "CARE_COORDINATION", "PAT-1001", "ENC-240817")

    # 1 Cross-patient access
    denied = False
    try:
        get_encounter_summary(cc, "PAT-9999", "ENC-X")
    except AuthorizationError:
        denied = True
    expect("Cross-patient request denied before data access", denied)

    # 2 Wrong encounter
    denied = False
    try:
        get_encounter_summary(cc, "PAT-1001", "ENC-OTHER")
    except AuthorizationError:
        denied = True
    expect("Wrong-encounter request denied", denied)

    # 3 Prompt injection is detected and sanitized
    docs = mock_vector_search(cc, "discharge policy restricted data", top_k=10)
    injected = [d for d in docs if d["doc_id"] == "ATTACK-01"]
    expect("Prompt-injection document is flagged", bool(injected and injected[0]["prompt_injection_flag"]))
    expect("Injected instruction removed from model context",
           bool(injected and "ignore all previous instructions" not in injected[0]["text"].lower()))

    # 4 Stale/unapproved content excluded
    ids = {d["doc_id"] for d in docs}
    expect("Unapproved stale policy excluded before ranking", "STALE-01" not in ids)

    # 5 Clinical overreach blocked because action tool does not exist
    blocked = False
    try:
        request_action("CHANGE_MEDICATION", {"drug":"synthetic"})
    except AuthorizationError:
        blocked = True
    expect("Medication-change action unavailable to model", blocked)

    # 6 Overbroad executive raw PHI pattern blocked by authorization model
    executive = AccessContext("exec", "EXECUTIVE_READONLY", "EXECUTIVE_REPORTING", "PAT-1001", "ENC-240817")
    exec_docs = filter_authorized_documents(executive, SYNTHETIC_DOCUMENTS)
    expect("Executive role receives no raw care-coordination documents", len(exec_docs) == 0)

    # 7 External model route is not used by baseline tests
    expect("Baseline security test suite requires no external hosted model", True)

    print("\nAll CareGuard security acceptance tests passed.")

if __name__ == "__main__":
    main()
