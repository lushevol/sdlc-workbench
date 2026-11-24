"""Check behavior evidence contracts without certifying business behavior."""

from __future__ import annotations

import copy
from contextlib import redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from ai_sdlc_workbench.assurance import (
    analyze_baseline,
    compare_baselines,
    read_baseline,
    save_baseline,
    schema,
)
from ai_sdlc_workbench.models import WorkbenchError
from ai_sdlc_workbench.cli import main


def record_hash(record):
    return hashlib.sha256(json.dumps(record, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False, allow_nan=False).encode()).hexdigest()


@unittest.skipUnless(shutil.which("git"), "Git is required for exact source evidence checks")
class AssuranceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ai-sdlc-assurance-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve() / "workspace"
        self.root.mkdir()
        self.repository = self.root / "repos/fixture"
        self.repository.mkdir(parents=True)
        self.code = "def accept(value):\n    return value == 'valid'\n"
        self.assertion = "from service import accept\nassert accept('valid') is True\n"
        (self.repository / "service.py").write_text(self.code, encoding="utf-8")
        (self.repository / "test_service.py").write_text(self.assertion, encoding="utf-8")
        self.git("init", "-q", "-b", "main")
        self.git("add", "--", ".")
        self.git("-c", "user.name=Test Fixture", "-c", "user.email=fixture@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "-q", "-m", "Create evidence fixture")
        self.revision = self.git("rev-parse", "HEAD").strip()
        (self.root / "registry").mkdir()
        (self.root / "registry/repositories.yaml").write_text(json.dumps({
            "schema_version": 1, "repositories": [{"id": "fixture-repo", "location": "repos/fixture"}],
        }), encoding="utf-8")
        (self.root / "workspace.yaml").write_text(json.dumps({
            "schema_version": 1, "id": "assurance-fixture", "name": "Evidence contract fixture",
            "resources": [], "plugins": [], "registries": {"repositories": "registry/repositories.yaml"},
        }), encoding="utf-8")
        self.baseline = {
            "schema_version": 1, "baseline_id": "fixture-baseline-1", "story_id": "fixture-story",
            "scope": "One isolated fixture criterion. This fixture supplies no business approval.",
            "artifacts": [], "behaviors": [], "links": [], "executions": [], "findings": [],
            "limitations": ["The fixture supplies no recorded human approval."],
        }
        intent = self.add_artifact("intent:one", "INTENT", "evidence/intent.md",
                                   "Given a valid instruction\nWhen it arrives\nThen accept it once\n")
        code = self.add_artifact("code:one", "CODE", "evidence/service.py", self.code,
                                repository_id="fixture-repo", revision=self.revision, source_path="service.py")
        assertion = self.add_artifact("test:one", "TEST", "evidence/test_service.py", self.assertion,
                                     repository_id="fixture-repo", revision=self.revision,
                                     source_path="test_service.py")
        behavior = {
            "id": "fixture-story:AC-1", "version": 1, "criterion_id": "AC-1", "state": "ACTIVE",
            "intent": {"artifact_id": intent["id"], "record_sha256": record_hash(intent),
                       "start_line": 1, "end_line": 3},
            "given": "Given a valid instruction", "when": "When the instruction arrives",
            "then": "Then the service accepts exactly one instruction",
            "measure": {"metric": "accepted instructions", "operator": "equals", "value": 1, "unit": "count"},
            "negative_cases": [], "required_level": "UNIT",
        }
        self.baseline["behaviors"].append(behavior)
        self.add_link("link:code", "IMPLEMENTED_BY", code)
        test_link = self.add_link("link:test", "ASSERTED_BY", assertion)
        run = self.add_artifact("run:one", "EXECUTION", "evidence/result.json", json.dumps({
            "status": "PASSED", "source_sha256": {"service.py": code["sha256"]},
            "checks": [{"name": "accepts valid instruction", "status": "PASSED"}],
            "limits": ["Contract fixture input. No approved business behavior is established."],
        }))
        self.baseline["executions"].append({
            "id": "execution:one", "artifact_id": run["id"], "artifact_record_sha256": record_hash(run),
            "code_artifact_ids": [code["id"]],
            "assertion_bindings": [{"link_id": test_link["id"], "link_record_sha256": record_hash(test_link),
                                    "check_name": "accepts valid instruction"}],
            "mode": "CONTROLLED_SOURCE", "level": "UNIT", "environment": "Isolated evidence contract fixture",
            "command": ["python", "test_service.py"],
            "limitations": ["The assertion binding was declared after the retained fixture result."],
        })

    def git(self, *arguments):
        environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        environment.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")
        result = subprocess.run(["git", *arguments], cwd=self.repository, env=environment,
                                check=True, capture_output=True, text=True, timeout=15)
        return result.stdout

    def add_artifact(self, identifier, kind, relative, content, **source):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        artifact = {"id": identifier, "kind": kind, "path": relative,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), **source}
        self.baseline["artifacts"].append(artifact)
        return artifact

    def add_link(self, identifier, relationship, artifact):
        behavior = self.baseline["behaviors"][0]
        link = {"id": identifier, "behavior_id": behavior["id"],
                "behavior_record_sha256": record_hash(behavior), "artifact_id": artifact["id"],
                "artifact_record_sha256": record_hash(artifact), "relationship": relationship,
                "grade": "CONFIRMED", "start_line": 1, "end_line": 2, "limitations": []}
        if relationship == "ASSERTED_BY":
            link["assertion"] = "The inspected assertion requires True for the valid instruction."
        self.baseline["links"].append(link)
        return link

    def analyze(self, baseline=None):
        return analyze_baseline(self.baseline if baseline is None else baseline, self.root)

    def cli(self, *arguments, workspace=None):
        output = io.StringIO()
        with redirect_stdout(output):
            code = main(["--workspace", str(workspace if workspace is not None else self.root),
                         "assurance", *arguments])
        return code, json.loads(output.getvalue())

    def write_baseline(self, baseline=None, name="baseline.json"):
        path = self.root / name
        path.write_text(json.dumps(self.baseline if baseline is None else baseline), encoding="utf-8")
        return path

    def rewrite_run(self, changes):
        artifact = next(item for item in self.baseline["artifacts"] if item["kind"] == "EXECUTION")
        path = self.root / artifact["path"]
        record = json.loads(path.read_text(encoding="utf-8"))
        changes(record)
        path.write_text(json.dumps(record), encoding="utf-8")
        artifact["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.baseline["executions"][0]["artifact_record_sha256"] = record_hash(artifact)

    def test_installed_schema_identifies_narrow_evidence_contract(self):
        self.assertEqual(schema()["$id"], "urn:ai-sdlc-workbench:behavior-review:1")
        self.assertEqual(schema()["properties"]["schema_version"]["const"], 1)

    def test_current_source_execution_remains_declared_and_business_unverified(self):
        result = self.analyze()
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["contract_status"], "VALID")
        self.assertEqual(result["verification"], "NOT_VERIFIED")
        self.assertEqual(result["executions"][0]["source_freshness"], "CURRENT")
        self.assertEqual(result["executions"][0]["result"], "PASSED")
        self.assertEqual(result["executions"][0]["assertion_bindings"], "DECLARED")
        self.assertTrue(result["behaviors"][0]["code_mapped"])
        self.assertTrue(result["behaviors"][0]["test_mapped"])
        self.assertEqual(result["behaviors"][0]["verification"], "NOT_VERIFIED")

    def test_stale_passing_execution_source_cannot_count_as_current(self):
        self.rewrite_run(lambda record: record["source_sha256"].update({"service.py": "0" * 64}))
        result = self.analyze()
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["executions"][0]["source_freshness"], "STALE")
        self.assertEqual(result["executions"][0]["result"], "PASSED")
        self.assertEqual(result["metrics"]["current_source_execution"]["numerator"], 0)
        self.assertEqual(result["verification"], "NOT_VERIFIED")

    def test_changed_retained_bytes_invalidate_the_artifact(self):
        (self.root / "evidence/service.py").write_text("def accept(value):\n    return False\n", encoding="utf-8")
        result = self.analyze()
        artifact = next(item for item in result["artifacts"] if item["id"] == "code:one")
        self.assertEqual(artifact["freshness"], "STALE")
        self.assertFalse(result["behaviors"][0]["code_mapped"])
        self.assertNotEqual(result["executions"][0]["source_freshness"], "CURRENT")

    def test_changed_revision_metadata_invalidates_bound_mapping(self):
        code = next(item for item in self.baseline["artifacts"] if item["kind"] == "CODE")
        code["revision"] = "a" * 40
        result = self.analyze()
        self.assertFalse(result["behaviors"][0]["code_mapped"])
        self.assertNotEqual(result["executions"][0]["source_freshness"], "CURRENT")

    def test_missing_git_checkout_supplies_unknown_revision_evidence(self):
        shutil.rmtree(self.repository)
        result = self.analyze()
        self.assertTrue(result["valid"], result)
        code = next(item for item in result["artifacts"] if item["id"] == "code:one")
        self.assertEqual(code["freshness"], "UNKNOWN")
        self.assertEqual(result["executions"][0]["source_freshness"], "UNKNOWN")

    def test_unrepresented_and_empty_execution_source_inventories_are_unknown(self):
        for sources in ({}, {"unrepresented.py": "0" * 64}):
            with self.subTest(sources=sources):
                self.rewrite_run(lambda record: record.update(source_sha256=sources))
                result = self.analyze()
                self.assertNotEqual(result["executions"][0]["source_freshness"], "CURRENT")
                self.assertEqual(result["metrics"]["current_source_execution"]["numerator"], 0)

    def test_execution_binding_needs_a_real_named_check(self):
        self.rewrite_run(lambda record: record.update(checks=[]))
        result = self.analyze()
        self.assertNotEqual(result["executions"][0]["source_freshness"], "CURRENT")
        self.assertEqual(result["verification"], "NOT_VERIFIED")

    def test_inventory_denominators_include_unmapped_active_behavior(self):
        unmapped = copy.deepcopy(self.baseline["behaviors"][0])
        unmapped.update(id="fixture-story:AC-2", criterion_id="AC-2")
        self.baseline["behaviors"].append(unmapped)
        result = self.analyze()
        self.assertTrue(result["valid"], result)
        for name in ("behavior_to_code", "behavior_to_test", "current_source_execution"):
            self.assertEqual(result["metrics"][name], {"numerator": 1, "denominator": 2, "percentage": 50.0})

    def test_empty_scope_has_no_successful_coverage_percentage(self):
        empty = copy.deepcopy(self.baseline)
        empty.update(behaviors=[], links=[], executions=[])
        result = self.analyze(empty)
        self.assertFalse(result["valid"])
        self.assertEqual(result["verification"], "NOT_VERIFIED")
        for metric in result["metrics"].values():
            self.assertIsNone(metric["percentage"])

    def test_retired_only_scope_has_no_active_coverage_percentage(self):
        self.baseline["behaviors"][0]["state"] = "RETIRED"
        result = self.analyze()
        self.assertFalse(result["valid"])
        for metric in result["metrics"].values():
            self.assertIsNone(metric["percentage"])

    def test_structural_faults_fail_validation(self):
        changes = {
            "duplicate artifact": lambda item: item["artifacts"].append(copy.deepcopy(item["artifacts"][0])),
            "duplicate behavior": lambda item: item["behaviors"].append(copy.deepcopy(item["behaviors"][0])),
            "future schema": lambda item: item.update(schema_version=2),
            "dangling intent": lambda item: item["behaviors"][0]["intent"].update(artifact_id="intent:missing"),
            "dangling behavior": lambda item: item["links"][0].update(behavior_id="behavior:missing"),
            "dangling artifact": lambda item: item["links"][0].update(artifact_id="code:missing"),
            "wrong link kind": lambda item: item["links"][0].update(relationship="ASSERTED_BY", assertion="Wrong kind."),
            "reversed locator": lambda item: item["links"][0].update(start_line=2, end_line=1),
            "invalid locator": lambda item: item["links"][0].update(start_line=0),
            "dangling execution code": lambda item: item["executions"][0].update(code_artifact_ids=["code:missing"]),
            "dangling assertion link": lambda item: item["executions"][0]["assertion_bindings"][0].update(link_id="link:missing"),
            "dangling finding evidence": lambda item: item["findings"].append({
                "id": "finding:one", "behavior_id": "fixture-story:AC-1", "kind": "EXECUTION_GAP",
                "summary": "Missing evidence.", "consequence": "The claim cannot be assessed.",
                "owner": "unknown", "next_action": "Inspect the source.", "evidence_ids": ["missing:evidence"],
            }),
        }
        for name, change in changes.items():
            with self.subTest(name=name):
                candidate = copy.deepcopy(self.baseline)
                change(candidate)
                result = self.analyze(candidate)
                self.assertFalse(result["valid"], result)
                self.assertEqual(result["contract_status"], "INVALID")
                self.assertTrue(result["diagnostics"])

    def test_evidence_paths_reject_workspace_escape(self):
        with tempfile.TemporaryDirectory(prefix="outside-assurance-") as outside:
            external = Path(outside) / "intent.md"
            external.write_text("Outside evidence\n", encoding="utf-8")
            (self.root / "escape.md").symlink_to(external)
            for relative in ("../outside.md", str(external), "escape.md", "evidence/../../outside.md"):
                with self.subTest(path=relative):
                    candidate = copy.deepcopy(self.baseline)
                    candidate["artifacts"][0]["path"] = relative
                    self.assertFalse(self.analyze(candidate)["valid"])

    def test_strict_json_rejects_ambiguous_or_nonfinite_input(self):
        path = self.root / "input.json"
        for contents in ('{"schema_version":1,"schema_version":2}', '{"value":NaN}',
                         '{"value":1e999}', '{"value":"\\ud800"}', '[1,2]', '{broken'):
            with self.subTest(contents=contents):
                path.write_text(contents, encoding="utf-8")
                with self.assertRaises(WorkbenchError):
                    read_baseline(path)

    def test_read_ignores_access_time_changes_for_unchanged_bytes(self):
        path = self.write_baseline()
        original_stat = Path.stat
        calls = 0

        class AccessTimeStat:
            def __init__(self, actual, increment):
                self.actual = actual
                self.increment = increment

            def __getattr__(self, name):
                if name == "st_atime":
                    return self.actual.st_atime + self.increment
                if name == "st_atime_ns":
                    return self.actual.st_atime_ns + self.increment * 1_000_000_000
                return getattr(self.actual, name)

            def __eq__(self, other):
                return (isinstance(other, AccessTimeStat) and self.actual == other.actual
                        and self.st_atime_ns == other.st_atime_ns)

        def access_time_only(candidate, *args, **kwargs):
            nonlocal calls
            actual = original_stat(candidate, *args, **kwargs)
            if candidate == path:
                calls += 1
                return AccessTimeStat(actual, calls)
            return actual

        with patch.object(Path, "stat", autospec=True, side_effect=access_time_only):
            result = read_baseline(path)
        self.assertEqual(result, self.baseline)
        self.assertGreaterEqual(calls, 2)

    def test_read_rejects_real_byte_changes_during_inspection(self):
        path = self.write_baseline()
        original_open = Path.open

        class ChangedWhileReading:
            def __init__(self, stream):
                self.stream = stream

            def __enter__(self):
                self.stream.__enter__()
                return self

            def read(self, *args):
                data = self.stream.read(*args)
                with original_open(path, "ab") as writer:
                    writer.write(b"\n")
                return data

            def __exit__(self, *args):
                return self.stream.__exit__(*args)

        def mutate_after_read(candidate, *args, **kwargs):
            stream = original_open(candidate, *args, **kwargs)
            return ChangedWhileReading(stream) if candidate == path and args == ("rb",) else stream

        with patch.object(Path, "open", autospec=True, side_effect=mutate_after_read):
            with self.assertRaises(WorkbenchError):
                read_baseline(path)

    def test_direct_api_rejects_nonfinite_measure_without_raising(self):
        for value in (float("inf"), float("-inf"), float("nan")):
            with self.subTest(value=value):
                candidate = copy.deepcopy(self.baseline)
                candidate["behaviors"][0]["measure"]["value"] = value
                result = self.analyze(candidate)
                self.assertFalse(result["valid"], result)
                self.assertEqual(result["contract_status"], "INVALID")

    def test_direct_api_rejects_unpaired_surrogate_without_crashing(self):
        self.baseline["behaviors"][0]["given"] = "Given " + chr(0xD800)
        result = self.analyze()
        self.assertFalse(result["valid"], result)
        self.assertEqual(result["contract_status"], "INVALID")

    def test_malformed_retained_checks_supply_no_current_execution_evidence(self):
        for checks in (None, 5, "PASSED", [None], [{"name": "accepts valid instruction", "status": []}],
                       [{"name": "accepts valid instruction", "status": "PASSED"},
                        {"name": "accepts valid instruction", "status": "PASSED"}]):
            with self.subTest(checks=checks):
                self.rewrite_run(lambda record: record.update(checks=checks))
                result = self.analyze()
                self.assertNotEqual(result["executions"][0]["source_freshness"], "CURRENT")
                self.assertEqual(result["verification"], "NOT_VERIFIED")

    def test_malformed_execution_source_digest_is_unknown_evidence(self):
        for digest in ("short", "A" * 64, "z" * 64, 12):
            with self.subTest(digest=digest):
                self.rewrite_run(lambda record: record.update(source_sha256={"service.py": digest}))
                result = self.analyze()
                self.assertEqual(result["executions"][0]["source_freshness"], "UNKNOWN")
                self.assertEqual(result["metrics"]["current_source_execution"]["numerator"], 0)

    def test_deeply_nested_retained_json_is_reported_without_crashing(self):
        artifact = next(item for item in self.baseline["artifacts"] if item["kind"] == "EXECUTION")
        path = self.root / artifact["path"]
        path.write_text('{"nested":' + "[" * 1500 + "0" + "]" * 1500 + "}", encoding="utf-8")
        artifact["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.baseline["executions"][0]["artifact_record_sha256"] = record_hash(artifact)
        result = self.analyze()
        self.assertEqual(result["executions"][0]["source_freshness"], "UNKNOWN")
        self.assertEqual(result["verification"], "NOT_VERIFIED")

    def test_execution_of_other_code_does_not_count_for_the_bound_behavior(self):
        other_source = "def unrelated():\n    return 'other'\n"
        (self.repository / "unrelated.py").write_text(other_source, encoding="utf-8")
        self.git("add", "--", "unrelated.py")
        self.git("-c", "user.name=Test Fixture", "-c", "user.email=fixture@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "-q", "-m", "Add unrelated fixture source")
        revision = self.git("rev-parse", "HEAD").strip()
        other = self.add_artifact("code:other", "CODE", "evidence/unrelated.py", other_source,
                                 repository_id="fixture-repo", revision=revision, source_path="unrelated.py")
        self.baseline["executions"][0]["code_artifact_ids"] = [other["id"]]
        self.rewrite_run(lambda record: record.update(source_sha256={"unrelated.py": other["sha256"]}))
        result = self.analyze()
        self.assertTrue(result["valid"], result)
        self.assertTrue(result["behaviors"][0]["code_mapped"])
        self.assertEqual(result["metrics"]["current_source_execution"]["numerator"], 0)
        self.assertFalse(result["behaviors"][0]["current_source_execution"])

    def test_save_preserves_immutable_baselines_and_allows_stale_evidence(self):
        self.rewrite_run(lambda record: record["source_sha256"].update({"service.py": "0" * 64}))
        path = save_baseline(self.baseline, self.root)
        self.assertEqual(path, self.root / "relationships/requirement-code/baselines/fixture-baseline-1.json")
        self.assertEqual(read_baseline(path), self.baseline)
        original = path.read_bytes()
        replacement = copy.deepcopy(self.baseline)
        replacement["scope"] = "Another scope must not overwrite earlier evidence."
        with self.assertRaises(WorkbenchError):
            save_baseline(replacement, self.root)
        self.assertEqual(path.read_bytes(), original)

    def test_invalid_baseline_cannot_be_saved(self):
        self.baseline["links"][0]["artifact_id"] = "missing:code"
        with self.assertRaises(WorkbenchError):
            save_baseline(self.baseline, self.root)
        self.assertFalse((self.root / "relationships/requirement-code/baselines/fixture-baseline-1.json").exists())

    def test_baseline_output_directory_cannot_escape_through_symlink(self):
        with tempfile.TemporaryDirectory(prefix="outside-baselines-") as outside:
            (self.root / "relationships/requirement-code").mkdir(parents=True)
            (self.root / "relationships/requirement-code/baselines").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(WorkbenchError):
                save_baseline(self.baseline, self.root)
            self.assertEqual(list(Path(outside).iterdir()), [])

    def test_compare_rejects_identity_and_behavior_history_rewrites(self):
        variants = {
            "same baseline": lambda item: None,
            "different story": lambda item: item.update(baseline_id="fixture-baseline-2", story_id="another-story"),
            "removed behavior": lambda item: item.update(baseline_id="fixture-baseline-2", behaviors=[], links=[], executions=[]),
            "changed same version": lambda item: (item.update(baseline_id="fixture-baseline-2"),
                                                   item["behaviors"][0].update(then="Then reject one instruction")),
        }
        for name, change in variants.items():
            with self.subTest(name=name):
                candidate = copy.deepcopy(self.baseline)
                change(candidate)
                with self.assertRaises(WorkbenchError):
                    compare_baselines(self.baseline, candidate, self.root)

    def test_comparison_follows_changed_artifact_to_dependent_behavior(self):
        candidate = copy.deepcopy(self.baseline)
        candidate["baseline_id"] = "fixture-baseline-2"
        candidate["artifacts"][1]["revision"] = "a" * 40
        result = compare_baselines(self.baseline, candidate, self.root)
        self.assertIn("fixture-story:AC-1", result["affected_behaviors"])
        self.assertTrue(result["changed_records"])
        self.assertEqual(result["before"]["verification"], "NOT_VERIFIED")
        self.assertEqual(result["after"]["verification"], "NOT_VERIFIED")

    def test_comparison_follows_execution_artifact_through_its_assertion_binding(self):
        candidate = copy.deepcopy(self.baseline)
        candidate["baseline_id"] = "fixture-baseline-2"
        run = next(item for item in candidate["artifacts"] if item["kind"] == "EXECUTION")
        run["sha256"] = "0" * 64
        result = compare_baselines(self.baseline, candidate, self.root)
        self.assertIn("fixture-story:AC-1", result["affected_behaviors"])

    def test_comparison_accepts_a_new_behavior_version_and_preserves_inputs(self):
        before = copy.deepcopy(self.baseline)
        candidate = copy.deepcopy(before)
        candidate["baseline_id"] = "fixture-baseline-2"
        candidate["behaviors"][0].update(version=2, then="Then the service accepts exactly two instructions")
        candidate["behaviors"][0]["measure"]["value"] = 2
        retained = copy.deepcopy(candidate)
        result = compare_baselines(before, candidate, self.root)
        self.assertIn("fixture-story:AC-1", result["affected_behaviors"])
        self.assertEqual(before, self.baseline)
        self.assertEqual(candidate, retained)

    def test_comparison_follows_finding_evidence_dependencies(self):
        second = copy.deepcopy(self.baseline["behaviors"][0])
        second.update(id="fixture-story:AC-2", criterion_id="AC-2")
        self.baseline["behaviors"].append(second)
        self.baseline["findings"].append({
            "id": "finding:other", "behavior_id": second["id"], "kind": "EXECUTION_GAP",
            "summary": "This criterion depends on the earlier execution evidence.",
            "consequence": "Changed execution evidence requires this criterion to be reviewed.",
            "owner": "unknown", "next_action": "Inspect the affected execution evidence.",
            "evidence_ids": ["execution:one"],
        })
        candidate = copy.deepcopy(self.baseline)
        candidate["baseline_id"] = "fixture-baseline-2"
        candidate["artifacts"][1]["revision"] = "a" * 40
        result = compare_baselines(self.baseline, candidate, self.root)
        self.assertIn("fixture-story:AC-2", result["affected_behaviors"])

    def test_simulation_and_lower_level_never_become_business_verification(self):
        self.baseline["behaviors"][0]["required_level"] = "SYSTEM"
        self.baseline["links"][0]["behavior_record_sha256"] = record_hash(self.baseline["behaviors"][0])
        self.baseline["links"][1]["behavior_record_sha256"] = record_hash(self.baseline["behaviors"][0])
        self.baseline["executions"][0]["mode"] = "SIMULATION"
        self.baseline["executions"][0]["assertion_bindings"][0]["link_record_sha256"] = record_hash(self.baseline["links"][1])
        result = self.analyze()
        self.assertEqual(result["verification"], "NOT_VERIFIED")
        self.assertEqual(result["behaviors"][0]["verification"], "NOT_VERIFIED")
        self.assertTrue(result["limitations"])

    def test_cli_schema_needs_no_workspace_configuration(self):
        code, result = self.cli("schema", workspace=self.root / "unconfigured")
        self.assertEqual(code, 0)
        self.assertEqual(result["$id"], "urn:ai-sdlc-workbench:behavior-review:1")
        self.assertFalse((self.root / "unconfigured").exists())

    def test_cli_validate_and_report_keep_business_verification_separate(self):
        path = self.write_baseline()
        for command in ("validate", "report"):
            with self.subTest(command=command):
                code, result = self.cli(command, "--baseline", str(path))
                self.assertEqual(code, 0, result)
                self.assertTrue(result["valid"])
                self.assertEqual(result["contract_status"], "VALID")
                self.assertEqual(result["verification"], "NOT_VERIFIED")
        code, result = self.cli("validate", "--baseline", path.name, "--require-current")
        self.assertEqual(code, 0, result)
        self.assertFalse((self.root / ".workbench").exists())

    def test_cli_require_current_rejects_stale_evidence_without_invalidating_contract(self):
        self.rewrite_run(lambda record: record["source_sha256"].update({"service.py": "0" * 64}))
        path = self.write_baseline()
        code, result = self.cli("validate", "--baseline", path.name, "--require-current")
        self.assertEqual(code, 1)
        self.assertTrue(result["valid"])
        self.assertEqual(result["contract_status"], "VALID")
        self.assertEqual(result["freshness"], "STALE")
        code, result = self.cli("report", "--baseline", path.name)
        self.assertEqual(code, 0)
        self.assertEqual(result["verification"], "NOT_VERIFIED")

    def test_cli_require_current_rejects_unknown_repository_evidence(self):
        shutil.rmtree(self.repository)
        path = self.write_baseline()
        code, result = self.cli("validate", "--baseline", path.name, "--require-current")
        self.assertEqual(code, 1)
        self.assertTrue(result["valid"])
        self.assertEqual(result["freshness"], "UNKNOWN")
        self.assertEqual(result["verification"], "NOT_VERIFIED")

    def test_cli_save_rejects_duplicate_id_with_structured_error_and_preserves_bytes(self):
        path = self.write_baseline()
        code, result = self.cli("save", "--baseline", path.name)
        self.assertEqual(code, 0, result)
        saved = self.root / result["saved_path"]
        original = saved.read_bytes()
        self.baseline["scope"] = "A changed review must use another baseline ID."
        self.write_baseline()
        code, result = self.cli("save", "--baseline", path.name)
        self.assertEqual(code, 1)
        self.assertEqual(result["error"]["code"], "WORKBENCH_ERROR")
        self.assertEqual(saved.read_bytes(), original)

    def test_cli_compare_rejects_nonunique_ids_and_different_stories(self):
        first = self.write_baseline(name="before.json")
        candidates = []
        candidates.append(copy.deepcopy(self.baseline))
        other = copy.deepcopy(self.baseline)
        other.update(baseline_id="other-baseline", story_id="other-story")
        other["behaviors"][0]["id"] = "other-story:AC-1"
        for link in other["links"]:
            link["behavior_id"] = "other-story:AC-1"
        candidates.append(other)
        for candidate in candidates:
            with self.subTest(story=candidate["story_id"]):
                second = self.write_baseline(candidate, name="after.json")
                code, result = self.cli("compare", "--before", first.name, "--after", second.name)
                self.assertEqual(code, 1)
                self.assertEqual(result["error"]["code"], "WORKBENCH_ERROR")

    def test_cli_bad_json_and_escaping_input_paths_return_structured_errors(self):
        path = self.root / "bad.json"
        for content in ('{"schema_version":1,"schema_version":2}', '{"given":"\\ud800"}'):
            with self.subTest(content=content):
                path.write_text(content, encoding="utf-8")
                code, result = self.cli("validate", "--baseline", path.name)
                self.assertEqual(code, 1)
                self.assertEqual(result["error"]["code"], "WORKBENCH_ERROR")
        outside = self.root.parent / "outside.json"
        outside.write_text(json.dumps(self.baseline), encoding="utf-8")
        for value in (str(outside), "../outside.json"):
            with self.subTest(path=value):
                code, result = self.cli("validate", "--baseline", value)
                self.assertEqual(code, 1)
                self.assertEqual(result["error"]["code"], "WORKBENCH_ERROR")

    def test_cli_resolves_relative_workspace_and_relative_baseline(self):
        path = self.write_baseline()
        previous = Path.cwd()
        try:
            os.chdir(self.root.parent)
            code, result = self.cli("validate", "--baseline", path.name, workspace="workspace")
        finally:
            os.chdir(previous)
        self.assertEqual(code, 0, result)
        self.assertTrue(result["valid"])
        self.assertEqual(result["verification"], "NOT_VERIFIED")


if __name__ == "__main__":
    unittest.main()
