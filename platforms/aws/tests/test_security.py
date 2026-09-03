from __future__ import annotations

import unittest

from src.authorization import AuthorizationError, filter_authorized_resources
from src.data_store import load_fhir_resources, load_policies
from src.models import AccessContext
from src.orchestrator import investigate_claim
from src.retrieval import retrieve_policies


def claims_context(**overrides) -> AccessContext:
    values = {
        "user_id": "claims-demo-01",
        "role": "CLAIMS_SPECIALIST",
        "purpose": "PAYMENT",
        "member_id": "MEM-2048",
        "case_id": "CASE-2026-0917",
        "assigned_case_ids": ("CASE-2026-0917",),
    }
    values.update(overrides)
    return AccessContext(**values)


class ClaimGuardSecurityTests(unittest.TestCase):
    def test_authorized_case_returns_pending_action(self):
        result = investigate_claim(claims_context(), "CASE-2026-0917")
        self.assertEqual("PENDING", result["action"]["status"])
        self.assertIn("73721", result["recommendation"])

    def test_wrong_purpose_denied_before_model(self):
        called = False
        def model(*_):
            nonlocal called
            called = True
            return "should not run", "test"
        with self.assertRaises(AuthorizationError):
            investigate_claim(claims_context(purpose="TREATMENT"), "CASE-2026-0917", model_call=model)
        self.assertFalse(called)

    def test_unassigned_case_denied_before_model(self):
        called = False
        def model(*_):
            nonlocal called
            called = True
            return "should not run", "test"
        with self.assertRaises(AuthorizationError):
            investigate_claim(claims_context(assigned_case_ids=()), "CASE-2026-0917", model_call=model)
        self.assertFalse(called)

    def test_cross_member_denied(self):
        with self.assertRaises(PermissionError):
            investigate_claim(claims_context(member_id="MEM-9999"), "CASE-2026-0917")

    def test_special_category_without_consent_excluded(self):
        resources = filter_authorized_resources(claims_context(), load_fhir_resources())
        self.assertNotIn("doc-sud-001", {item["id"] for item in resources})

    def test_minimum_necessary_excludes_diagnostic_report_for_claims_role(self):
        resources = filter_authorized_resources(claims_context(), load_fhir_resources())
        self.assertNotIn("DiagnosticReport", {item["resourceType"] for item in resources})

    def test_stale_policy_excluded_before_ranking(self):
        docs = retrieve_policies(claims_context(), "MRI claim appeal", load_policies(), limit=20)
        self.assertNotIn("STALE-MRI-01", {item["policy_id"] for item in docs})

    def test_prompt_injection_is_flagged_and_removed(self):
        docs = retrieve_policies(claims_context(), "claim procedure", load_policies(), limit=20)
        attack = next(item for item in docs if item["policy_id"] == "ATTACK-01")
        self.assertTrue(attack["prompt_injection_flag"])
        self.assertNotIn("ignore all previous instructions", attack["text"].lower())

    def test_output_inherits_restricted_classification(self):
        result = investigate_claim(claims_context(), "CASE-2026-0917")
        self.assertEqual("RESTRICTED", result["output_classification"])

    def test_no_autonomous_claim_submission(self):
        result = investigate_claim(claims_context(), "CASE-2026-0917")
        self.assertEqual("PREPARE_CORRECTED_CLAIM", result["action"]["action_type"])
        self.assertNotIn("SUBMIT", result["action"]["action_type"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
