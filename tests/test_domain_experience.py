from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / ".agents/skills/package-domain-experience/scripts/validate_packet.py"
INDEXER = ROOT / ".agents/skills/package-domain-experience/scripts/rebuild_index.py"
SCANNER = ROOT / ".agents/skills/learn-domain-experience/scripts/scan_history.py"


class DomainExperienceScriptsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="domain-experience-")
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name) / "workspace"
        self.workspace.mkdir()

    def write_packet(self, *, experience="Run the safe workflow.\n", script="#!/bin/sh\necho ok\n"):
        evidence = self.workspace / "tasks/demo/evidence/result.json"
        evidence.parent.mkdir(parents=True)
        evidence.write_text('{"status":"SUCCEEDED"}\n', encoding="utf-8")
        packet = self.workspace / "assets/experience/packets/exp.demo.workflow.v1"
        (packet / "scripts").mkdir(parents=True)
        (packet / "fixtures").mkdir()
        (packet / "experience.md").write_text(experience, encoding="utf-8")
        (packet / "scripts/run.sh").write_text(script, encoding="utf-8")
        digest = hashlib.sha256(evidence.read_bytes()).hexdigest()
        manifest = {
            "schema_version": 1,
            "id": "exp.demo.workflow.v1",
            "title": "Demo workflow",
            "domain": "demo",
            "status": "observed",
            "applies_when": ["A demo workflow is required"],
            "retrospective": {
                "summary": "The demo task completed.",
                "successful_path": "Run the parameterized shell script.",
                "reusable_reason": "The same inputs produce the same local result.",
                "discarded": ["Verbose logs"],
            },
            "requires": {"tools": ["sh"], "variables": ["DEMO_ROOT"]},
            "provenance": {"task_id": "demo", "evidence": [{"path": "tasks/demo/evidence/result.json", "sha256": digest}]},
            "verification": {"outcome": "successful", "conditions": ["local"], "assertions": ["result status is SUCCEEDED"]},
            "assets": {"primary": {"kind": "script", "path": "scripts/run.sh"}, "procedure": "experience.md", "variables": None, "scripts": ["scripts/run.sh"], "fixtures": []},
            "knowledge": {"records": [], "wiki_topics": []},
            "promotions": [],
            "security": {"classification": "synthetic", "secrets_present": False},
            "limits": ["Demo data only"],
        }
        (packet / "manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
        return packet

    def run_script(self, script, *arguments):
        return subprocess.run([sys.executable, str(script), *map(str, arguments)],
                              capture_output=True, text=True, check=False)

    def test_validator_checks_evidence_hash_and_packet_files(self):
        packet = self.write_packet()
        result = self.run_script(VALIDATOR, packet, "--workspace", self.workspace)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "PASSED")

        evidence = self.workspace / "tasks/demo/evidence/result.json"
        evidence.write_text('{"status":"CHANGED"}\n', encoding="utf-8")
        result = self.run_script(VALIDATOR, packet, "--workspace", self.workspace)
        self.assertEqual(result.returncode, 1)
        self.assertIn("hash does not match", result.stdout)

    def test_validator_rejects_obvious_secret_patterns(self):
        packet = self.write_packet(script="-----BEGIN PRIVATE KEY-----\n")
        result = self.run_script(VALIDATOR, packet)
        self.assertEqual(result.returncode, 1)
        self.assertIn("possible secret", result.stdout)

    def test_validator_requires_a_primary_end_to_end_recipe(self):
        packet = self.write_packet()
        manifest_path = packet / "manifest.yaml"
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        manifest["assets"].pop("primary")
        manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
        result = self.run_script(VALIDATOR, packet)
        self.assertEqual(result.returncode, 1)
        self.assertIn("assets.primary", result.stdout)

    def test_validator_binds_shared_workbench_asset_promotions(self):
        packet = self.write_packet()
        target = self.workspace / "AGENTS.md"
        target.write_text("Shared guidance.\n", encoding="utf-8")
        manifest_path = packet / "manifest.yaml"
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        manifest["promotions"] = [{
            "target": "AGENTS.md",
            "kind": "guide",
            "action": "update",
            "source": "experience.md",
            "purpose": "Add the reusable workflow to shared guidance.",
            "before_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "after_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "checks": ["markdown-link-check"],
        }]
        manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
        result = self.run_script(VALIDATOR, packet, "--workspace", self.workspace)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_validator_rejects_application_source_promotion_targets(self):
        packet = self.write_packet()
        manifest_path = packet / "manifest.yaml"
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        manifest["promotions"] = [{
            "target": "repos/application/src/main.py",
            "kind": "script",
            "action": "update",
            "source": "experience.md",
            "purpose": "Invalid broad promotion.",
            "before_sha256": None,
            "after_sha256": "0" * 64,
            "checks": ["tests"],
        }]
        manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
        result = self.run_script(VALIDATOR, packet)
        self.assertEqual(result.returncode, 1)
        self.assertIn("unsupported Workbench asset target", result.stdout)

    def test_indexer_writes_compact_retrieval_index(self):
        self.write_packet()
        result = self.run_script(INDEXER, "--root", self.workspace / "assets/experience")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        index = yaml.safe_load((self.workspace / "assets/experience/index.yaml").read_text(encoding="utf-8"))
        self.assertEqual(index["schema_version"], 1)
        self.assertEqual(index["experiences"][0]["id"], "exp.demo.workflow.v1")
        check = self.run_script(INDEXER, "--root", self.workspace / "assets/experience", "--check")
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_history_scanner_indexes_retained_tasks_and_explicit_sessions(self):
        task = self.workspace / "tasks/demo/01-maintenance.md"
        task.parent.mkdir(parents=True)
        task.write_text("# Demo\n## Workflow\n## Validation result\n", encoding="utf-8")
        session = self.workspace / ".workbench/session-export.md"
        session.parent.mkdir()
        session.write_text("# Session\n## Recovery steps\n", encoding="utf-8")
        output = self.workspace / ".workbench/experience/history.json"
        result = self.run_script(SCANNER, "--workspace", self.workspace, "--path", session,
                                 "--output", output)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(output.read_text(encoding="utf-8"))
        paths = {item["path"] for item in payload["files"]}
        self.assertIn("tasks/demo/01-maintenance.md", paths)
        self.assertIn(".workbench/session-export.md", paths)
        self.assertTrue(any("workflow" in item["signals"] for item in payload["files"]))
        self.assertTrue(any("Signals and candidates are search hints" in item for item in payload["limits"]))
        self.assertEqual(payload["review"]["review_status"], "PENDING")
        self.assertEqual(payload["promotion"]["packets_created"], 0)
        self.assertFalse((self.workspace / "assets/experience").exists())

    def test_history_scanner_applies_default_week_duration_to_sessions(self):
        session = self.workspace / "retained-session"
        session.mkdir()
        recent = session / "recent.md"
        old = session / "old.md"
        recent.write_text("# Recent\n## Workflow\n", encoding="utf-8")
        old.write_text("# Old\n## Workflow\n", encoding="utf-8")
        os.utime(old, (time.time() - 9 * 86400, time.time() - 9 * 86400))
        output = self.workspace / ".workbench/experience/week.json"
        result = self.run_script(SCANNER, "--workspace", self.workspace, "--path", session, "--output", output)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        paths = {item["path"] for item in json.loads(output.read_text(encoding="utf-8"))["files"]}
        self.assertIn("retained-session/recent.md", paths)
        self.assertNotIn("retained-session/old.md", paths)

    def test_history_scanner_skips_unchanged_sessions_and_rescans_changes(self):
        session = self.workspace / "retained-session"
        session.mkdir()
        source = session / "workflow.md"
        source.write_text("# Session\n## Workflow\n", encoding="utf-8")
        first = self.workspace / ".workbench/experience/first.json"
        second = self.workspace / ".workbench/experience/second.json"
        self.assertEqual(self.run_script(SCANNER, "--workspace", self.workspace, "--path", session, "--output", first).returncode, 0)
        second_result = self.run_script(SCANNER, "--workspace", self.workspace, "--path", session, "--output", second)
        self.assertEqual(second_result.returncode, 0, second_result.stdout + second_result.stderr)
        second_payload = json.loads(second.read_text(encoding="utf-8"))
        self.assertEqual(len(second_payload["session_scan"]["skipped_sessions"]), 1)
        self.assertEqual(second_payload["session_scan"]["scanned_sessions"], [])
        source.write_text("# Session\n## Workflow\n## Recovery steps\n", encoding="utf-8")
        third = self.workspace / ".workbench/experience/third.json"
        third_result = self.run_script(SCANNER, "--workspace", self.workspace, "--path", session, "--output", third)
        self.assertEqual(third_result.returncode, 0, third_result.stdout + third_result.stderr)
        third_payload = json.loads(third.read_text(encoding="utf-8"))
        self.assertEqual(len(third_payload["session_scan"]["scanned_sessions"]), 1)

    def test_history_scanner_rejects_invalid_duration(self):
        result = self.run_script(SCANNER, "--workspace", self.workspace, "--past-duration", "0d",
                                 "--output", self.workspace / ".workbench/experience/invalid.json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("positive duration", result.stderr)


if __name__ == "__main__":
    unittest.main()
