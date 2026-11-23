"""Exercise the CES inspector from a copy of the skill outside Workbench."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SKILL = Path(__file__).resolve().parents[1] / ".agents/skills/ces-domain-capability"


class CesDomainSkillTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.skill = self.workspace / "ces-domain-capability"
        shutil.copytree(SKILL, self.skill)

    def run_inspector(self, command, *arguments, success=True):
        result = subprocess.run(
            [sys.executable, "-I", "-S", str(self.skill / "scripts/inspect_ces.py"),
             command, *arguments, "--app", "DEMO_REPORTS"],
            cwd=self.workspace, text=True, capture_output=True, timeout=15,
        )
        self.assertEqual(result.returncode, 0 if success else 2, result.stderr)
        for value in ("demo-account", "Example East", "Example West"):
            self.assertNotIn(value, result.stdout + result.stderr)
        if success:
            return json.loads(result.stdout)
        self.assertEqual(result.stdout, "")

    def fixture(self, name):
        return self.skill / "assets" / f"{name}.json"

    def test_copied_skill_checks_catalog_grant_and_snapshot_differences(self):
        catalog = self.run_inspector("catalog", self.fixture("catalog"))
        self.assertEqual(catalog["application_scope"], "CALLER_DECLARED")
        self.assertEqual((catalog["entitlement_count"], catalog["assignment_count"]), (3, 3))
        for action, status in (("View", "PRESENT"), ("Edit", "ABSENT")):
            with self.subTest(action=action):
                captured = self.run_inspector(
                    "user", self.fixture("user-before"), "--user", "demo-account",
                    "--feature", "Reports", "--action", action,
                )
                self.assertEqual(captured["requested_grant"], status)
        comparison = self.run_inspector(
            "compare", self.fixture("user-before"), self.fixture("user-after"), "--user", "demo-account",
        )
        self.assertEqual(comparison["assignments"], {"added": 1, "removed": 1})
        self.assertEqual(comparison["effective_grants"], {"added": 1, "removed": 0})
        self.assertEqual(comparison["data_sections_changed"], ["data_entitlements"])

    def test_absent_record_empty_grants_and_conflicting_identity(self):
        absent = self.workspace / "absent.json"
        absent.write_text("[]", encoding="utf-8")
        record = json.loads(self.fixture("user-before").read_text(encoding="utf-8"))
        record[0]["entitlements"]["role_entitlements"] = []
        empty = self.workspace / "empty.json"
        empty.write_text(json.dumps(record), encoding="utf-8")
        selector = ("--user", "demo-account", "--feature", "Reports", "--action", "View")
        self.assertEqual(self.run_inspector("user", absent, *selector),
                         {"status": "RECORD_ABSENT", "requested_grant": "UNASSESSED"})
        self.assertEqual(self.run_inspector("user", empty, *selector)["requested_grant"], "ABSENT")
        self.assertEqual(self.run_inspector("compare", absent, empty, "--user", "demo-account")["status"],
                         "UNASSESSED")
        self.run_inspector("user", empty, "--user", "another-demo-account", success=False)
        self.run_inspector("user", empty, "--user", "demo-account", "--feature", "Reports", success=False)
