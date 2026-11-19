from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
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
            "requires": {"tools": ["sh"], "variables": ["DEMO_ROOT"]},
            "provenance": {"task_id": "demo", "evidence": [{"path": "tasks/demo/evidence/result.json", "sha256": digest}]},
            "verification": {"outcome": "successful", "conditions": ["local"], "assertions": ["result status is SUCCEEDED"]},
            "assets": {"procedure": "experience.md", "variables": None, "scripts": ["scripts/run.sh"], "fixtures": []},
            "knowledge": {"records": [], "wiki_topics": []},
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
        self.assertTrue(any("Signals are search hints" in item for item in payload["limits"]))


if __name__ == "__main__":
    unittest.main()
