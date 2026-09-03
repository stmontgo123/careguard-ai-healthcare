from __future__ import annotations

import json
from pathlib import Path
from typing import Any


BASE = Path(__file__).resolve().parents[1]
DEMO = BASE / "demo"


def load_json(name: str) -> Any:
    return json.loads((DEMO / name).read_text(encoding="utf-8"))


def load_case(case_id: str) -> dict:
    case = load_json("synthetic_case.json")
    if case["case_id"] != case_id:
        raise KeyError(f"Unknown synthetic case: {case_id}")
    return case


def load_fhir_resources() -> list[dict]:
    return [item["resource"] for item in load_json("ehr_fhir_bundle.json")["entry"]]


def load_policies() -> list[dict]:
    return load_json("policies.json")
