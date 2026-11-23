"""Exercise the CES inspector from a copy of the skill outside Workbench."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from jsonschema import Draft202012Validator
import yaml


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
        for value in ("demo-account", "Example East", "Example West", "Private Demo Profile", "Private Demo Role"):
            self.assertNotIn(value, result.stdout + result.stderr)
        if success:
            return json.loads(result.stdout)
        self.assertEqual(result.stdout, "")

    def fixture(self, name):
        if name == "variables.example":
            return self.skill / "Workflows" / "variables.example.json"
        return self.skill / "Contracts/examples" / f"{name}.json"

    def test_packaged_response_schemas_and_uat_origin(self):
        variables = json.loads(self.fixture("variables.example").read_text(encoding="utf-8"))
        self.assertEqual(variables["ces"]["origins"]["uat"], "https://fmcesuat.gdc.standardchartered.com")
        self.assertIsNone(variables["ces"]["base_url"])
        self.assertIsNone(variables["account"]["id"])
        cases = (
            ("catalog", ("catalog",), ("user_ids",), 42),
            ("effective-user", ("user-before", "user-after"), ("entitlements", "data_profiles"), []),
            ("assigned-role", ("roles",), ("featureActionDtos", 0, "actions", "actionName"), 42),
        )
        for view, fixtures, path, invalid_value in cases:
            with self.subTest(view=view):
                schema_path = self.skill / "Contracts/schemas" / f"{view}-response.schema.json"
                schema = json.loads(schema_path.read_text(encoding="utf-8"))
                Draft202012Validator.check_schema(schema)
                validator = Draft202012Validator(schema)
                validator.validate([])
                for fixture in fixtures:
                    body = json.loads(self.fixture(fixture).read_text(encoding="utf-8"))
                    validator.validate(body)
                record = body[0]
                for part in path[:-1]:
                    record = record[part]
                record[path[-1]] = invalid_value
                self.assertFalse(validator.is_valid(body))

    def test_assigned_role_attribution_and_empty_grants(self):
        source = self.fixture("roles")
        lookup = ("--feature", "Reports", "--action", "View")
        assigned = self.run_inspector("assigned-role", source, "--entitlement", "Report Reader", *lookup)
        self.assertEqual(assigned["account_scope"], "CALLER_DECLARED")
        self.assertEqual(assigned["assignment_count"], 2)
        self.assertEqual(assigned["assignments_without_grants"], 1)
        self.assertEqual(assigned["requested_grant"], "PRESENT")
        empty = self.run_inspector("assigned-role", source, "--entitlement", "Unassigned Feature Set", *lookup)
        self.assertEqual((empty["requested_entitlement"], empty["requested_grant"]), ("PRESENT", "ABSENT"))
        self.run_inspector("assigned-role", source, "--app-uid", "999", success=False)

        rows = json.loads(source.read_text(encoding="utf-8"))
        rows[0]["featureActionDtos"][0]["features"]["applicationDto"]["appUID"] = 999
        invalid = self.workspace / "invalid-roles.json"
        invalid.write_text(json.dumps(rows), encoding="utf-8")
        self.run_inspector("assigned-role", invalid, success=False)

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

    def test_reconcile_keeps_assignment_and_role_attribution_differences(self):
        arguments = (self.fixture("catalog"), self.fixture("roles"), self.fixture("user-before"),
                     "--user", "demo-account")
        result = self.run_inspector("reconcile", *arguments)
        comparisons = result["comparisons"]
        self.assertEqual(result["status"], "COMPARED")
        self.assertEqual(comparisons["catalog_vs_assigned_role_assignments"],
                         {"status": "DIFFERENT", "added": 1, "removed": 1})
        self.assertEqual(comparisons["catalog_vs_assigned_role_grants"],
                         {"status": "DIFFERENT", "added": 0, "removed": 2})
        self.assertEqual(comparisons["assigned_role_union_vs_effective_grants"]["status"], "MATCH")
        self.run_inspector("reconcile", *arguments, "--itam-id", "wrong-itam", success=False)

        absent = self.workspace / "absent.json"
        absent.write_text("[]", encoding="utf-8")
        result = self.run_inspector("reconcile", self.fixture("catalog"), self.fixture("roles"),
                                    absent, "--user", "demo-account")
        self.assertEqual(result["status"], "UNASSESSED")
        self.assertEqual(result["comparisons"]["catalog_vs_assigned_role_assignments"]["status"], "DIFFERENT")
        self.assertEqual(result["comparisons"]["assigned_role_union_vs_effective_grants"]["status"], "UNASSESSED")

    def test_profile_distinguishes_exact_value_missing_and_explicit_null(self):
        rows = json.loads(self.fixture("user-before").read_text(encoding="utf-8"))
        rows[0]["user_data"]["itam_id"] = "demo-itam"
        # A synthetic field exercises pointers without asserting a CES profile wire location.
        rows[0]["synthetic/profile"] = {"~value": [None, "Private Demo Profile"]}
        captured = self.workspace / "profile.json"
        captured.write_text(json.dumps(rows), encoding="utf-8")
        expected = self.workspace / "expected.json"
        expected.write_text(json.dumps("Private Demo Profile"), encoding="utf-8")
        selector = ("--user", "demo-account", "--itam-id", "demo-itam", "--expected", str(expected))
        result = self.run_inspector("profile", captured, *selector, "--pointer", "/synthetic~1profile/~0value/1")
        self.assertEqual(result, {"status": "MATCH"})
        self.assertNotIn("Private Demo Profile", json.dumps(result))
        self.assertEqual(self.run_inspector("profile", captured, *selector, "--pointer", "/missing"),
                         {"status": "UNASSESSED", "reason": "VALUE_ABSENT"})
        self.assertEqual(self.run_inspector("profile", captured, *selector, "--pointer", "/synthetic~1profile/~0value/0"),
                         {"status": "DIFFERENT"})
        expected.write_text("null", encoding="utf-8")
        self.assertEqual(self.run_inspector("profile", captured, *selector, "--pointer", "/synthetic~1profile/~0value/0"),
                         {"status": "MATCH"})
        absent = self.workspace / "absent-profile.json"
        absent.write_text("[]", encoding="utf-8")
        self.assertEqual(self.run_inspector("profile", absent, *selector, "--pointer", "/synthetic~1profile/~0value/0"),
                         {"status": "UNASSESSED", "reason": "RECORD_ABSENT"})
        self.run_inspector("profile", captured, *selector, "--pointer", "/invalid~2escape", success=False)
        self.run_inspector("profile", captured, "--user", "demo-account", "--itam-id", "wrong-itam",
                           "--expected", expected, "--pointer", "/synthetic~1profile/~0value/0", success=False)
        expected.write_text("42", encoding="utf-8")
        self.run_inspector("profile", captured, *selector, "--pointer", "/missing", success=False)

    def test_duplicate_evidence_is_rejected_without_echoing_values(self):
        duplicate = self.workspace / "duplicate.json"
        duplicate.write_text('[{"entitlement_name":"Private Demo Role","entitlement_name":"other"}]', encoding="utf-8")
        self.run_inspector("catalog", duplicate, success=False)
        rows = json.loads(self.fixture("catalog").read_text(encoding="utf-8"))
        rows.append(rows[0])
        duplicate.write_text(json.dumps(rows), encoding="utf-8")
        self.run_inspector("reconcile", duplicate, self.fixture("roles"), self.fixture("user-before"),
                           "--user", "demo-account", success=False)

    def test_contract_pairs_and_documented_schema_subset(self):
        contract = yaml.safe_load((self.skill / "Contracts/openapi.yaml").read_text(encoding="utf-8"))
        self.assertEqual(contract["openapi"], "3.1.0")
        operations = {operation["operationId"]: operation
                      for path in contract["paths"].values() for operation in path.values()}
        self.assertEqual(set(operations), {"getApplicationCatalog", "getEffectiveUser", "getAssignedRoles"})
        pairs = sorted((self.skill / "Contracts/examples").glob("*-uat-pair.json"))
        self.assertEqual(len(pairs), 4)
        accounts = set()
        for path in pairs:
            pair = json.loads(path.read_text(encoding="utf-8"))
            operation = operations[pair["operationId"]]
            self.assertEqual(pair["request"]["method"], "GET")
            self.assertEqual(pair["response"]["status"], 200)
            self.assertEqual(pair["evidence"]["classification"], "sanitized-observation")
            self.assertRegex(pair["evidence"]["source_sha256"], r"^[0-9a-f]{64}$")
            schema = operation["responses"]["200"]["content"]["application/json"]["schema"]
            validator = Draft202012Validator({**schema, "components": contract["components"]})
            validator.validate(pair["response"]["body"])
            if pair["operationId"] == "getEffectiveUser":
                accounts.add(pair["request"]["path_parameters"]["user_id"])
                self.assertEqual(pair["request"]["path_parameters"]["user_id"],
                                 pair["response"]["body"][0]["user_data"]["user_id"])
        self.assertEqual(len(accounts), 2)
        role = json.loads((self.skill / "Contracts/examples/assigned-role-body-fixture.json").read_text(encoding="utf-8"))
        self.assertIsNone(role["request"])
        self.assertIsNone(role["response"]["status"])
        self.assertEqual(role["evidence"]["classification"], "sanitized-supplied-body-fixture")
        role_schema = operations["getAssignedRoles"]["responses"]["default"]["x-local-json-body-schema"]
        Draft202012Validator({**role_schema, "components": contract["components"]}).validate(role["response"]["body"])
