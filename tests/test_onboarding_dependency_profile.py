"""Check dependency coverage and field certainty without weakening exact source evidence."""

import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = (Path(__file__).resolve().parents[1]
          / ".agents/skills/repository-onboarding/scripts/validate_evidence.py")
SPEC = importlib.util.spec_from_file_location("dependency_evidence_validator", SCRIPT)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)

FAMILIES = (
    "api", "messaging", "managed-events", "data", "identity", "trust", "configuration",
    "storage", "network", "platform", "scheduling", "observability", "frontend",
    "business-provider", "delivery", "other",
)
ATTRIBUTES = (
    "component", "peer", "protocol", "operation", "environment", "activation", "trigger",
    "conditions", "timing", "interaction", "authentication", "authorization", "network_access",
    "configuration", "resilience", "impact", "criticality", "family_details",
)


def unknown_attribute():
    return {"value": None, "status": "unknown", "reason": "No applicable source establishes this field.",
            "claim_ids": []}


def dependency(ident="DEP-001", family="api"):
    return {
        "id": ident, "family": family, "direction": "outbound", "phase": "runtime",
        "attributes": {name: unknown_attribute() for name in ATTRIBUTES},
        "review": {"owner": "unknown", "next_action": "Inspect deployment evidence with the owning team."},
    }


@unittest.skipUnless(shutil.which("git"), "Git is required for source revision checks")
class OnboardingDependencyProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        self.environment.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull})
        self.git("init", "--template=")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        (self.repo / "client.py").write_text("client = RemoteClient()\nclient.send()\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-m", "Dependency source fixture")
        self.legacy = {
            "schema_version": "1.0",
            "repository": {"path": str(self.repo), "revision": self.git("rev-parse", "HEAD")},
            "claims": [self.claim("OBS-001", "observed", 1)],
        }
        self.report = copy.deepcopy(self.legacy)
        self.report.update({
            "dependency_profile": "external-dependencies/1",
            "external_dependencies": [dependency()],
            "dependency_coverage": [{
                "family": family, "status": "inspected" if family == "api" else "not-observed",
                "scope": ["client.py"],
                "reason": "The inspected file defines this relationship." if family == "api"
                          else "No relationship was observed in the inspected file.",
                "dependency_ids": ["DEP-001"] if family == "api" else [],
            } for family in FAMILIES],
        })

    def git(self, *arguments):
        result = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", "-C", str(self.repo), *arguments],
            env=self.environment, capture_output=True, text=True, check=True,
        )
        return result.stdout.strip()

    @staticmethod
    def claim(ident, status, line, evidence=True):
        claim = {
            "id": ident, "category": "dependency", "statement": "The inspected source declares a client.",
            "status": status,
            "evidence": [{"path": "client.py", "start_line": line, "end_line": line, "kind": "source"}]
                        if evidence else [],
        }
        if status != "observed":
            claim["reason"] = "The available evidence limits this interpretation."
        return claim

    def errors(self, report=None):
        return validator.validate(self.repo, self.report if report is None else report)

    def assert_error(self, report, text):
        errors = self.errors(report)
        self.assertTrue(any(text in error for error in errors), errors)

    def attribute(self, status, claim_ids, value="REST", reason=None):
        result = {"value": value, "status": status, "claim_ids": claim_ids}
        if reason is not None:
            result["reason"] = reason
        return result

    def test_legacy_and_explicit_unknown_profile_remain_valid(self):
        self.assertEqual([], self.errors(self.legacy))
        self.assertEqual([], self.errors())
        self.report["external_dependencies"][0]["attributes"]["protocol"] = self.attribute("observed", ["OBS-001"])
        self.assertEqual([], self.errors())

    def test_profile_declaration_cannot_be_omitted_or_mismatched(self):
        for key, value in (("external_dependencies", []), ("dependency_coverage", []),
                           ("dependency_profile", None), ("dependency_profile", "external-dependencies/2"),
                           ("dependency_profile", [])):
            with self.subTest(key=key, value=value):
                report = copy.deepcopy(self.legacy)
                report[key] = value
                self.assert_error(report, "dependency_profile must be")
        for key in ("external_dependencies", "dependency_coverage"):
            report = copy.deepcopy(self.report)
            del report[key]
            self.assert_error(report, f"{key} must be an array")

    def test_empty_register_requires_justified_complete_coverage(self):
        self.report["external_dependencies"] = []
        self.report["dependency_coverage"][0].update(status="not-observed", dependency_ids=[])
        self.assertEqual([], self.errors())
        self.report["dependency_coverage"][0]["status"] = "unknown"
        self.assertEqual([], self.errors())
        self.report["dependency_coverage"][0]["status"] = "inspected"
        self.assert_error(self.report, "inspected coverage needs at least one dependency")

    def test_required_record_fields_and_enums_are_enforced(self):
        for field in ("id", "family", "direction", "phase", "attributes", "review"):
            with self.subTest(missing_field=field):
                report = copy.deepcopy(self.report)
                del report["external_dependencies"][0][field]
                self.assertTrue(self.errors(report))
        for field, value in (("id", " "), ("family", "grpc"), ("direction", "provided"),
                             ("phase", "production"), ("attributes", []), ("review", [])):
            with self.subTest(field=field):
                report = copy.deepcopy(self.report)
                report["external_dependencies"][0][field] = value
                self.assertTrue(self.errors(report))
        for field in ("owner", "next_action"):
            report = copy.deepcopy(self.report)
            del report["external_dependencies"][0]["review"][field]
            self.assert_error(report, f"review.{field}")
        for field in ATTRIBUTES:
            with self.subTest(missing_attribute=field):
                report = copy.deepcopy(self.report)
                del report["external_dependencies"][0]["attributes"][field]
                self.assert_error(report, f"attributes.{field}: required attribute missing")

    def test_all_family_direction_phase_mappings_and_extra_attributes_are_supported(self):
        directions = ("inbound", "outbound", "bidirectional", "local")
        phases = ("runtime", "build", "test", "deployment", "configuration")
        self.report["external_dependencies"] = []
        for index, family in enumerate(FAMILIES):
            record = dependency(f"DEP-{index}", family)
            record.update(direction=directions[index % len(directions)], phase=phases[index % len(phases)])
            record["attributes"]["technology_specific_limit"] = unknown_attribute()
            self.report["external_dependencies"].append(record)
            self.report["dependency_coverage"][index].update(status="inspected", dependency_ids=[record["id"]])
        self.assertEqual([], self.errors())
        self.report["external_dependencies"][0]["attributes"]["technology_specific_limit"] = "unchecked"
        self.assert_error(self.report, "technology_specific_limit: must be an object")

    def test_duplicate_dependency_and_claim_references_fail(self):
        report = copy.deepcopy(self.report)
        report["external_dependencies"].append(copy.deepcopy(report["external_dependencies"][0]))
        self.assert_error(report, "duplicate id DEP-001")
        for references, expected in ((["OBS-001", "OBS-001"], "duplicate id OBS-001"),
                                      (["MISSING"], "unknown claim id MISSING"),
                                      ([[]], "must be a nonempty string"),
                                      (None, "must be an array")):
            with self.subTest(references=references):
                report = copy.deepcopy(self.report)
                report["external_dependencies"][0]["attributes"]["protocol"] = self.attribute("observed", references)
                self.assert_error(report, expected)

    def test_unknown_fields_require_null_values_and_nonempty_reasons(self):
        for value, reason in (("public", "No source."), (None, ""), (None, []), (None, None)):
            with self.subTest(value=value, reason=reason):
                report = copy.deepcopy(self.report)
                report["external_dependencies"][0]["attributes"]["authorization"] = self.attribute(
                    "unknown", [], value=value, reason=reason,
                )
                self.assertTrue(self.errors(report))
        del self.report["external_dependencies"][0]["attributes"]["authorization"]["value"]
        self.assert_error(self.report, "authorization: value required")

    def test_observed_permissions_cannot_escalate_inferences_or_conflicts(self):
        self.report["claims"].append(self.claim("INF-001", "inferred", 1))
        conflicting = self.claim("CON-001", "conflicting", 1)
        conflicting["evidence"].append(self.claim("other", "observed", 2)["evidence"][0])
        self.report["claims"].append(conflicting)
        attributes = self.report["external_dependencies"][0]["attributes"]
        attributes["authorization"] = self.attribute("observed", ["INF-001"], "Requires a token.")
        self.assert_error(self.report, "authorization: observed attribute needs an observed evidence-bearing claim")
        attributes["authorization"]["claim_ids"] = ["OBS-001", "CON-001"]
        self.assert_error(self.report, "authorization: observed attribute cannot reference conflicting claims")
        self.report["claims"][0]["evidence"] = []
        attributes["authorization"]["claim_ids"] = ["OBS-001"]
        self.assert_error(self.report, "authorization: observed attribute needs an observed evidence-bearing claim")

    def test_inferences_need_observed_or_inferred_evidence(self):
        self.report["claims"].append(self.claim("INF-001", "inferred", 1))
        self.report["claims"].append(self.claim("UNK-001", "unknown", 1, evidence=False))
        attr = self.attribute("inferred", ["INF-001"], reason="The caller suggests this protocol.")
        self.report["external_dependencies"][0]["attributes"]["protocol"] = attr
        self.assertEqual([], self.errors())
        attr["claim_ids"] = ["UNK-001"]
        self.assert_error(self.report, "inferred attribute needs observed or inferred evidence-bearing support")
        attr["claim_ids"] = ["OBS-001"]
        self.assertEqual([], self.errors())
        conflicting = self.claim("CON-001", "conflicting", 1)
        conflicting["evidence"].append(self.claim("other", "observed", 2)["evidence"][0])
        self.report["claims"].append(conflicting)
        attr["claim_ids"] = ["CON-001"]
        self.assert_error(self.report, "inferred attribute needs observed or inferred evidence-bearing support")
        attr["claim_ids"] = ["OBS-001"]
        del attr["reason"]
        self.assert_error(self.report, "reason required for inferred attribute")

    def test_conflicts_need_distinct_claims_and_distinct_citations(self):
        self.report["claims"].extend([self.claim("OBS-002", "observed", 2), self.claim("INF-001", "inferred", 1)])
        attr = self.attribute("conflicting", ["OBS-001", "OBS-002"], reason="Two declarations disagree.")
        self.report["external_dependencies"][0]["attributes"]["protocol"] = attr
        self.assertEqual([], self.errors())
        attr["claim_ids"] = ["OBS-001", "INF-001"]
        self.assert_error(self.report, "conflicting attribute needs conflicting evidence")
        self.report["claims"][-1]["evidence"][0]["kind"] = "documentation"
        self.assert_error(self.report, "conflicting attribute needs conflicting evidence")
        attr["claim_ids"] = ["OBS-002"]
        self.report["claims"][1]["evidence"].append(self.claim("unused", "observed", 1)["evidence"][0])
        self.assert_error(self.report, "conflicting attribute needs conflicting evidence")
        conflicting = self.claim("CON-001", "conflicting", 1)
        conflicting["evidence"].append(self.claim("unused", "observed", 2)["evidence"][0])
        self.report["claims"].append(conflicting)
        attr["claim_ids"] = ["CON-001"]
        self.assertEqual([], self.errors())
        distinct_evidence = copy.deepcopy(conflicting["evidence"])
        conflicting["evidence"] = [copy.deepcopy(distinct_evidence[0]), copy.deepcopy(distinct_evidence[0])]
        self.assert_error(self.report, "conflicting attribute needs conflicting evidence")
        conflicting["evidence"][1]["kind"] = "documentation"
        self.assert_error(self.report, "conflicting attribute needs conflicting evidence")
        conflicting["evidence"] = distinct_evidence
        self.assertEqual([], self.errors())

    def test_coverage_must_partition_dependencies_by_family(self):
        mutations = (
            (lambda report: report["dependency_coverage"].pop(), "missing family other"),
            (lambda report: report["dependency_coverage"].append(copy.deepcopy(report["dependency_coverage"][0])),
             "duplicate family api"),
            (lambda report: report["dependency_coverage"][0].update(dependency_ids=[]), "must appear once"),
            (lambda report: report["dependency_coverage"][0].update(dependency_ids=["MISSING"]),
             "unknown dependency id MISSING"),
            (lambda report: report["dependency_coverage"][1].update(status="unknown", dependency_ids=["DEP-001"]),
             "belongs to a different family"),
            (lambda report: report["dependency_coverage"][0].update(dependency_ids=["DEP-001", "DEP-001"]),
             "duplicate id DEP-001"),
        )
        for mutate, expected in mutations:
            with self.subTest(expected=expected):
                report = copy.deepcopy(self.report)
                mutate(report)
                self.assert_error(report, expected)
        self.report["dependency_coverage"][0]["status"] = "unknown"
        self.assertEqual([], self.errors())
        for status in ("not-observed", "out-of-scope"):
            self.report["dependency_coverage"][0]["status"] = status
            self.assert_error(self.report, f"{status} coverage must not reference dependencies")

    def test_coverage_requires_scope_reason_and_valid_status(self):
        for field, value in (("scope", []), ("scope", [""]), ("scope", [[]]), ("scope", "client.py"),
                             ("reason", ""), ("reason", {}), ("status", "complete"), ("family", "LDAP")):
            with self.subTest(field=field, value=value):
                report = copy.deepcopy(self.report)
                report["dependency_coverage"][0][field] = value
                self.assertTrue(self.errors(report))

    def test_inline_dependency_evidence_is_rejected(self):
        for target in ("dependency", "attribute", "coverage"):
            with self.subTest(target=target):
                report = copy.deepcopy(self.report)
                containers = {
                    "dependency": report["external_dependencies"][0],
                    "attribute": report["external_dependencies"][0]["attributes"]["protocol"],
                    "coverage": report["dependency_coverage"][0],
                }
                containers[target]["evidence"] = []
                self.assert_error(report, "evidence belongs in claims")

    def test_malformed_extension_types_never_abort_validation(self):
        for value in (None, True, 7, [], {}, " "):
            with self.subTest(value=value):
                if not isinstance(value, list):
                    for field in ("external_dependencies", "dependency_coverage"):
                        report = copy.deepcopy(self.report)
                        report[field] = value
                        self.assert_error(report, f"{field} must be an array")
                for field in ("family", "direction", "phase", "id", "review", "attributes"):
                    report = copy.deepcopy(self.report)
                    report["external_dependencies"][0][field] = value
                    self.assertTrue(self.errors(report))
                for field in ("status", "claim_ids", "value"):
                    report = copy.deepcopy(self.report)
                    report["external_dependencies"][0]["attributes"]["protocol"] = self.attribute("observed", ["OBS-001"])
                    report["external_dependencies"][0]["attributes"]["protocol"][field] = value
                    self.assertTrue(self.errors(report))
                for field in ("family", "status", "scope", "reason", "dependency_ids"):
                    report = copy.deepcopy(self.report)
                    report["dependency_coverage"][0][field] = value
                    self.assertTrue(self.errors(report))
                for field in ("external_dependencies", "dependency_coverage"):
                    report = copy.deepcopy(self.report)
                    report[field] = [value]
                    self.assertTrue(self.errors(report))
        self.report["claims"][0]["status"] = []
        self.report["external_dependencies"][0]["attributes"]["protocol"] = self.attribute("observed", ["OBS-001"])
        self.assert_error(self.report, "invalid status")

    def test_dependency_profile_preserves_exact_source_checks(self):
        self.report["external_dependencies"][0]["attributes"]["protocol"] = self.attribute("observed", ["OBS-001"])
        self.git("update-index", "--assume-unchanged", "client.py")
        (self.repo / "client.py").write_text("changed = RemoteClient()\nclient.send()\n", encoding="utf-8")
        self.assert_error(self.report, "file bytes differ from the report revision")

    def test_cli_distinguishes_structural_profile_and_legacy_limits(self):
        report_path = self.root / "report.json"
        for report, expected in ((self.legacy, "Legacy report: dependency profile structure was not checked."),
                                 (self.report, "Dependency profile structural validation passed (1 dependencies).")):
            with self.subTest(expected=expected):
                report_path.write_text(json.dumps(report), encoding="utf-8")
                result = subprocess.run(
                    [sys.executable, str(SCRIPT), "--repo", str(self.repo), "--report", str(report_path)],
                    env=self.environment, capture_output=True, text=True,
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn(expected, result.stdout)
                self.assertIn("does not validate completeness", result.stdout)
                self.assertIn("effective permissions, or runtime behavior", result.stdout)
        self.report["external_dependencies"][0]["attributes"]["authorization"] = self.attribute("observed", ["MISSING"])
        report_path.write_text(json.dumps(self.report), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(self.repo), "--report", str(report_path)],
            env=self.environment, capture_output=True, text=True,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("authorization: unknown claim id MISSING", result.stderr)
        self.assertNotIn("validation passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
