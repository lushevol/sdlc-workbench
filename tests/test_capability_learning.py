import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from ai_sdlc_workbench.capability_learning import CapabilityRegistry
from ai_sdlc_workbench.hooks import run_hook
from ai_sdlc_workbench.models import WorkbenchError
from ai_sdlc_workbench.workspace import initialize_workspace


FIXTURES = Path(__file__).parent / "fixtures/capability_learning"
ADO = "ado-deploy-artifact"
CES = "ces-entitlement-migration"


class CapabilityLearningTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        switches = patch.dict(os.environ, {
            "WORKBENCH_LEARNING_CAPTURE": "1",
            "WORKBENCH_LEARNING_PROMOTION": "1",
        })
        switches.start()
        self.addCleanup(switches.stop)
        self.root = initialize_workspace(temporary.name)
        self.registry = CapabilityRegistry(self.root)
        self.task = "tasks/fixture/01-maintenance.md"
        self.write(self.task, b"# Fixture artifact investigation\n")
        self.input_path = ".workbench/inputs/discovery.json"

    def write(self, relative, data):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def reference(self, relative, data, locator):
        self.write(relative, data)
        return {"path": relative, "sha256": hashlib.sha256(data).hexdigest(), "locator": locator}

    def discovery(self, *observations):
        data = [(FIXTURES / f"ado-observation-{number}.json").read_bytes() for number in observations]
        first = json.loads(data[0])
        return {
            "category": "contract",
            "title": "ADO artifact publication name",
            "summary": "An exact scoped naming convention for fixture builds.",
            "scope": first["scope"],
            "task": self.task,
            "evidence": [
                self.reference(f"tasks/fixture/evidence/build-{number}.json", raw, "artifact_name")
                for number, raw in zip(observations, data)
            ],
            "observed_facts": ["The fixture declares the published artifact name."],
            "derived_conclusions": ["The name may be reusable within the checked branch and pipeline."],
            "verification_status": "OBSERVED",
            "verification_method": "Compare independent build metadata.",
            "skill_id": ADO,
            "rule": {"key": "artifact-name", "value": first["artifact_name"]},
        }

    def checkpoint(self, discovery):
        self.write(self.input_path, json.dumps(discovery).encode())
        return self.registry.checkpoint(self.input_path)

    def approve(self, change, evidence):
        path = ".workbench/inputs/approval.json"
        self.write(path, json.dumps({
            "change_id": change["id"],
            "authority": "Fixture Workbench owner",
            "verification": "Read the independent fixture review and checked the exact scope.",
            "evidence": evidence,
        }).encode())
        return path

    def test_new_ado_discovery_is_traceable_before_promotion(self):
        discovery = self.discovery(1, 2)
        with patch.dict(os.environ, {"WORKBENCH_LEARNING_PROMOTION": "0"}):
            saved = self.checkpoint(discovery)
        self.assertEqual(saved["status"], "AUTO_ELIGIBLE")
        self.assertEqual(saved["change"]["operation"], "CREATE")
        self.assertEqual(saved["change"]["capability_id"], ADO)
        self.assertEqual(saved["discovery"]["verification_status"], "OBSERVED")
        self.assertEqual(saved["discovery"]["evidence"], discovery["evidence"])
        self.assertEqual(saved["discovery"]["task"], self.task)
        self.assertRegex(saved["discovery"]["id"], r"^[a-f0-9]{64}$")
        self.assertTrue(saved["discovery"]["discovered_at"].endswith("Z"))
        self.assertEqual(CapabilityRegistry(self.root).pending()[0]["discovery"], saved["discovery"])
        self.assertEqual(self.registry.history(ADO), [])

    def test_second_ado_condition_extends_the_same_capability_and_skill(self):
        initial = self.checkpoint(self.discovery(1, 2))
        self.registry = CapabilityRegistry(self.root)
        added = self.checkpoint(self.discovery(3, 4))
        self.assertEqual((initial["status"], added["status"]), ("PROMOTED", "PROMOTED"))
        self.assertEqual((added["change"]["capability_id"], added["change"]["operation"]), (ADO, "EXTEND"))
        self.assertEqual([item["id"] for item in self.registry.available("artifact")], [ADO])
        first, second = self.registry.history(ADO)
        self.assertEqual(second["capability"]["previous"], first["sha256"])
        self.assertEqual(second["capability"]["skills"], [ADO])
        self.assertEqual(second["capability"]["revision"], 2)
        self.assertEqual([rule["value"] for rule in second["capability"]["rules"]],
                         ["application-package", "release-package"])

    def test_contradiction_records_conflict_and_keeps_the_active_revision(self):
        discovery = self.discovery(1, 2)
        self.assertEqual(self.checkpoint(discovery)["status"], "PROMOTED")
        before = self.registry.history(ADO)
        evidence = discovery["evidence"][0]
        conflicting = json.loads((self.root / evidence["path"]).read_bytes())
        conflicting["artifact_name"] = "unexpected-package"
        discovery["evidence"] = [self.reference(
            "tasks/fixture/evidence/conflicting-build.json", json.dumps(conflicting).encode(), "artifact_name"
        )]
        discovery["rule"]["value"] = "unexpected-package"
        result = self.checkpoint(discovery)
        self.assertEqual(result["status"], "CONFLICT")
        self.assertEqual(result["change"]["operation"], "CORRECT")
        self.assertEqual(self.registry.pending(conflicts=True)[0]["change"], result["change"])
        with self.assertRaises(WorkbenchError):
            self.registry.promote(result["discovery"]["id"])
        self.assertEqual(self.registry.history(ADO), before)
        self.assertEqual(self.registry.use(ADO, discovery["scope"])["rules"][0]["value"], "application-package")

    def test_fresh_cli_process_reuses_the_persisted_rule(self):
        discovery = self.discovery(1, 2)
        self.assertEqual(self.checkpoint(discovery)["status"], "PROMOTED")
        process = subprocess.run(
            [sys.executable, "-m", "ai_sdlc_workbench", "--workspace", str(self.root),
             "learning", "use", ADO, "--scope", json.dumps(discovery["scope"])],
            cwd=self.root, capture_output=True, text=True, check=True, timeout=15,
        )
        resolved = json.loads(process.stdout)
        self.assertEqual(resolved["status"], "ACTIVE")
        self.assertEqual(resolved["skills"], [ADO])
        self.assertEqual(resolved["rules"][0]["value"], "application-package")

    def test_pipeline_rule_requires_matching_pipeline_branch_and_instance(self):
        discovery = self.discovery(1, 2)
        self.assertEqual(self.checkpoint(discovery)["status"], "PROMOTED")
        scope = discovery["scope"]
        self.assertEqual(self.registry.use(ADO, scope)["rules"][0]["value"], "application-package")
        for selectors in [
            {**scope, "pipeline": "28"},
            {**scope, "branch": "refs/heads/main"},
            {**scope, "instance": "another-instance"},
            {key: value for key, value in scope.items() if key != "pipeline"},
        ]:
            with self.subTest(selectors=selectors):
                self.assertEqual(self.registry.use(ADO, selectors)["rules"], [])
                self.assertEqual(self.registry.available("artifact", selectors), [])

    def test_sensitive_payload_is_excluded_from_learning_storage(self):
        secret = "fixture-only-" + ("q" * 18)
        hook_payload = {
            "cwd": str(self.root), "session_id": f"native-{secret}",
            "hook_event_name": "PostToolUse", "tool_name": "Bash",
            "tool_input": {"command": f"test {secret}"}, "tool_response": {"password": secret},
        }
        self.assertEqual(run_hook(self.root, "claude", "tool", hook_payload), ({}, "", 0))
        discovery = self.discovery(1, 2)
        discovery["summary"] = f"Password: {secret}"
        with self.assertRaisesRegex(WorkbenchError, "Sensitive-looking metadata") as error:
            self.checkpoint(discovery)
        self.assertNotIn(secret, str(error.exception))
        learning = self.root / ".workbench/learning"
        self.assertTrue(list((learning / "events").glob("*.json")))
        for retained in learning.rglob("*.json"):
            self.assertNotIn(secret.encode(), retained.read_bytes())
        self.assertEqual(self.registry.pending(), [])
        self.assertEqual(self.registry.history(ADO), [])

    def test_failed_validation_preserves_engineering_output_and_active_history(self):
        self.assertEqual(self.checkpoint(self.discovery(1, 2))["status"], "PROMOTED")
        task_path = self.write(self.task, b"# Engineering work completed successfully\n")
        before = self.registry.history(ADO)
        unverified = self.discovery(3)
        unverified["verification_status"] = "VERIFIED"
        result = self.checkpoint(unverified)
        self.assertEqual(result["status"], "INVALID_EVIDENCE")
        self.assertEqual(self.registry.pending()[0]["discovery"]["id"], result["discovery"]["id"])
        self.assertEqual(self.registry.validate(result["discovery"]["id"])["status"], "INVALID_EVIDENCE")
        with self.assertRaises(WorkbenchError):
            self.registry.promote(result["discovery"]["id"])
        self.assertEqual(self.registry.history(ADO), before)
        self.assertEqual(task_path.read_bytes(), b"# Engineering work completed successfully\n")

    def test_ces_rule_requires_governance_even_with_claimed_local_approval(self):
        evidence = self.reference("tasks/fixture/evidence/ces.md", b"Observed fixture entitlement.", "L1")
        discovery = {
            "category": "business-rule", "title": "Fixture CES entitlement mapping",
            "summary": "A candidate mapping derived from one controlled observation.",
            "scope": {"system": "ces", "environment": "fixture"},
            "task": self.task, "evidence": [evidence],
            "rule": {"key": "legacy-role-mapping", "value": "fixture-mapping"},
            "verification_status": "APPROVED", "verification_method": "An unverified caller claim.",
        }
        result = self.checkpoint(discovery)
        self.assertEqual(result["status"], "GOVERNANCE_REQUIRED")
        self.assertEqual(result["change"]["capability_id"], CES)
        approval = self.approve(result["change"], evidence)
        with self.assertRaisesRegex(WorkbenchError, "canonical knowledge governance"):
            self.registry.promote(result["discovery"]["id"], approval)
        self.assertEqual(self.registry.history(CES), [])
        self.assertEqual(self.registry.use(CES, discovery["scope"])["rules"], [])

    def test_repeated_evidence_creates_one_candidate_and_revision(self):
        discovery = self.discovery(1, 2)
        first = self.checkpoint(discovery)
        discovery["evidence"].reverse()
        second = self.checkpoint(discovery)
        self.assertEqual((first["status"], second["status"]), ("PROMOTED", "NO_CHANGE"))
        self.assertEqual(first["discovery"], second["discovery"])
        self.assertEqual(len(list((self.root / ".workbench/learning/discoveries").glob("*.json"))), 1)
        self.assertEqual(len(self.registry.history(ADO)), 1)
        self.assertEqual(self.registry.pending(), [])
        command = [sys.executable, "-m", "ai_sdlc_workbench", "--workspace", str(self.root), "learning",
                   "checkpoint", "--task", self.task,
                   "--ado-observation", discovery["evidence"][0]["path"],
                   "--ado-observation", discovery["evidence"][1]["path"]]
        retry = subprocess.run(command, capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(retry.stdout)["status"], "NO_CHANGE")
        self.assertEqual(len(list((self.root / ".workbench/learning/discoveries").glob("*.json"))), 1)

    def test_rollback_appends_auditable_restoration(self):
        original = self.discovery(1, 2)
        added = self.discovery(3, 4)
        self.assertEqual(self.checkpoint(original)["status"], "PROMOTED")
        self.assertEqual(self.checkpoint(added)["status"], "PROMOTED")
        previous = self.registry.history(ADO)
        restored = self.registry.rollback(ADO, 1)
        self.assertEqual(restored["capability"]["revision"], 3)
        self.assertEqual(restored["capability"]["previous"], previous[-1]["sha256"])
        self.assertEqual(restored["capability"]["rollback_of"], previous[0]["sha256"])
        self.assertEqual(restored["validation"]["status"], "RESTORED")
        self.assertEqual(self.registry.history(ADO)[:2], previous)
        self.assertEqual(self.registry.use(ADO, original["scope"])["rules"], previous[0]["capability"]["rules"])
        self.assertEqual(self.registry.use(ADO, added["scope"])["rules"], [])
        self.assertEqual(self.checkpoint(added)["status"], "NO_CHANGE")
        self.assertEqual(self.registry.use(ADO, added["scope"])["rules"], [])
        self.assertEqual(self.registry.rollback(ADO, 1), restored)
        self.assertEqual(len(self.registry.history(ADO)), 3)

    def test_general_nonexecuting_guidance_requires_bound_approval(self):
        evidence = self.reference("tasks/fixture/evidence/source.md", b"Fixture workflow observation.", "L1")
        discovery = {
            "capability_id": "fixture-inspection", "category": "experience",
            "title": "Fixture inspection", "summary": "A reusable observation for inspecting fixtures.",
            "scope": {"environment": "fixture"}, "task": self.task, "evidence": [evidence],
            "rule": {"key": "inspection-method", "value": "Inspect the fixture manifest."},
            "verification_status": "OBSERVED", "verification_method": "Checked the local fixture.",
        }
        result = self.checkpoint(discovery)
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        with self.assertRaises(WorkbenchError):
            self.registry.promote(result["discovery"]["id"])
        review = self.reference("tasks/fixture/evidence/review.md", b"Fixture owner reviewed the method.", "L1")
        approval_path = self.approve(result["change"], review)
        promoted = self.registry.promote(result["discovery"]["id"], approval_path)
        self.assertEqual(promoted["validation"]["approval"]["evidence"], review)
        self.assertEqual(promoted["validation"]["approval"]["change_id"], result["change"]["id"])
        self.assertEqual(self.registry.use("fixture-inspection", discovery["scope"])["status"], "ACTIVE")
