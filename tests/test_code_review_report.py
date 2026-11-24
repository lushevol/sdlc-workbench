"""Exercise skill-local review reports, redaction, coverage, and frozen scope binding."""

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


SCRIPTS = Path(__file__).resolve().parents[1] / ".agents/skills/code-review/scripts"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


context_helper = load("review_report_context", SCRIPTS / "review_context.py")
validator = load("review_report_validator", SCRIPTS / "validate_review.py")
DEFAULT = object()


def report(scope):
    return {
        "schema_version": "1.0",
        "target": {key: scope[key] for key in validator.TARGET_KEYS},
        "axes": {axis: {"status": "REVIEWED", "reason": "Compared the changed path and its consumers."}
                 for axis in validator.AXES},
        "outcome": "INCOMPLETE" if scope["limitations"] else "NO_ACTIONABLE_FINDINGS",
        "reviewed_paths": [record["path"] for record in scope["files"]],
        "skipped_paths": [],
        "findings": [],
        "checks_executed": [],
        "suggested_checks": [],
        "unverified_assumptions": [],
        "summary": "No actionable findings were identified in the inspected scope.",
        "writing_review": {
            "standard": "ASD-STE100", "automated_check": "NOT_RUN", "asd_review": "PENDING",
            "reviewer": None, "reviewed_at": None, "limitations": [validator.WRITING_LIMIT],
        },
    }


def finding(path="code.py", *, side="RIGHT", line=2, location="INLINE"):
    return {
        "id": "F-001", "axis": "tests", "priority": "P2", "confidence": "CONFIRMED",
        "title": "Retain the regression assertion", "path": path, "location": location,
        "side": side, "line": line,
        "trigger": "The updated branch receives an empty collection.",
        "impact": "The consumer returns an incorrect count.", "owner": "Unknown",
        "fix": "Keep the assertion for empty input.",
        "verification": "Run the affected test with empty input.",
        "evidence_refs": ["code.py:2", "tests/test_code.py:10"], "unverified_conditions": [],
    }


class ReviewReportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.git("init", "-b", "main")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Review Report Test")
        self.write("code.py", "keep\nold\nlast\n")
        self.commit()
        self.write("code.py", "keep\nnew\nlast\n")
        self.scope = context_helper.collect_context(self.repo)
        self.review = report(self.scope)

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, check=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE).stdout.decode().strip()

    def write(self, path, text):
        file = self.repo / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(text.encode() if isinstance(text, str) else text)

    def commit(self):
        self.git("add", "--all")
        self.git("commit", "-m", "baseline")

    def invalid(self, review=DEFAULT, scope=DEFAULT):
        errors = validator.validate_review(self.review if review is DEFAULT else review,
                                           self.scope if scope is DEFAULT else scope)
        self.assertTrue(errors)
        self.assertTrue(all(isinstance(error, str) for error in errors))
        self.assertNotIn("PRIVATE_PAYLOAD", "\n".join(errors))
        return errors

    def with_finding(self, value=None):
        self.review["findings"] = [finding() if value is None else value]
        self.review["axes"]["tests"]["status"] = "ISSUES_FOUND"
        self.review["outcome"] = "FINDINGS_PRESENT"

    def run_cli(self, review=None, scope=None, *, live=False, raw_review=None, raw_context=None, extra=()):
        review_path, scope_path = self.root / "review.json", self.root / "context.json"
        review_path.write_text(json.dumps(self.review if review is None else review) if raw_review is None else raw_review)
        scope_path.write_text(json.dumps(self.scope if scope is None else scope) if raw_context is None else raw_context)
        command = [sys.executable, str(SCRIPTS / "validate_review.py"), "--review", str(review_path),
                   "--context", str(scope_path)]
        if live:
            command.extend(("--repo", str(self.repo)))
        return subprocess.run(command + list(extra), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_real_collector_context_and_valid_report(self):
        self.assertEqual(self.scope["files"][0]["added_ranges"], [[2, 2]])
        self.assertEqual(self.scope["files"][0]["removed_ranges"], [[2, 2]])
        self.assertEqual(validator.validate_review(self.review, self.scope), [])
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["status"], "VALID")
        self.assertIn("Supplied context was not independently recollected.", output["limitations"])

    def test_live_recollection_accepts_unchanged_scope_without_writes(self):
        def snapshot():
            return {str(path.relative_to(self.repo)): path.read_bytes()
                    for path in self.repo.rglob("*") if path.is_file()}
        before = snapshot()
        result = self.run_cli(live=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, snapshot())
        self.assertNotIn("Supplied context was not independently recollected.", json.loads(result.stdout)["limitations"])

    def test_live_recollection_rejects_tampered_range_even_with_same_fingerprint(self):
        self.scope["files"][0]["added_ranges"] = [[2, 100]]
        self.with_finding(finding(line=99))
        self.assertEqual(validator.validate_review(self.review, self.scope), [])
        result = self.run_cli(live=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["errors"], ["context: recollected scope mismatch"])

    def test_live_recollection_rejects_changed_local_content(self):
        self.write("code.py", "changed again\n")
        self.assertEqual(self.run_cli(live=True).returncode, 1)

    def test_live_cli_does_not_create_skill_bytecode_without_environment_override(self):
        tools = self.root / "shipped-skill"
        tools.mkdir()
        for name in ("validate_review.py", "review_context.py"):
            shutil.copy2(SCRIPTS / name, tools / name)
        review_path, context_path = self.root / "review.json", self.root / "context.json"
        review_path.write_text(json.dumps(self.review))
        context_path.write_text(json.dumps(self.scope))
        environment = dict(os.environ)
        environment.pop("PYTHONDONTWRITEBYTECODE", None)
        result = subprocess.run(
            [sys.executable, str(tools / "validate_review.py"), "--review", str(review_path),
             "--context", str(context_path), "--repo", str(self.repo)],
            env=environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((tools / "__pycache__").exists())

    def test_range_recollection_uses_resolved_ids_and_preserves_checked_out_branch(self):
        base = self.git("rev-parse", "HEAD")
        self.commit()
        self.scope = context_helper.collect_context(self.repo, "range", base=base, head="HEAD")
        self.review = report(self.scope)
        self.assertEqual(self.run_cli(live=True).returncode, 0)
        self.assertEqual(self.git("branch", "--show-current"), "main")

    def test_target_requires_all_identity_fields_and_exact_values(self):
        for key in validator.TARGET_KEYS:
            with self.subTest(key=key):
                changed = copy.deepcopy(self.review)
                changed["target"][key] = "PRIVATE_PAYLOAD"
                self.invalid(changed)
                del changed["target"][key]
                self.invalid(changed)

    def test_unknown_fields_are_rejected_at_every_report_level(self):
        self.with_finding()
        self.review["checks_executed"] = [{"command": "python -m unittest", "result": "PASSED", "notes": "Assertions inspected."}]
        for locator in ((), ("target",), ("axes", "tests"), ("findings", 0), ("checks_executed", 0), ("writing_review",)):
            with self.subTest(locator=locator):
                changed = copy.deepcopy(self.review)
                value = changed
                for component in locator:
                    value = value[component]
                value["PRIVATE_PAYLOAD"] = "extra"
                self.invalid(changed)

    def test_axes_require_exact_names_statuses_and_reasons(self):
        for value in (None, [], "PRIVATE_PAYLOAD", {"tests": "PASS"}):
            changed = copy.deepcopy(self.review)
            changed["axes"] = value
            self.invalid(changed)
        for field, value in (("status", "PASS"), ("status", []), ("reason", " "), ("reason", {})):
            changed = copy.deepcopy(self.review)
            changed["axes"]["tests"][field] = value
            self.invalid(changed)

    def test_skips_cover_exact_scope_and_require_reasons(self):
        self.review["reviewed_paths"] = []
        self.review["skipped_paths"] = [{"path": "code.py", "reason": "Required runtime is unavailable."}]
        self.review["outcome"] = "INCOMPLETE"
        self.assertEqual(validator.validate_review(self.review, self.scope), [])
        self.review["skipped_paths"][0]["reason"] = " "
        self.invalid()

    def test_missing_extra_duplicate_or_overlapping_coverage_is_invalid(self):
        for paths in ([], ["extra.py"], ["code.py", "code.py"], [{"path": "PRIVATE_PAYLOAD"}]):
            changed = copy.deepcopy(self.review)
            changed["reviewed_paths"] = paths
            self.invalid(changed)
        self.review["skipped_paths"] = [{"path": "code.py", "reason": "Skipped."}]
        self.invalid()
        self.review["reviewed_paths"] = []
        self.review["skipped_paths"] *= 2
        self.invalid()

    def test_confirmed_and_inferred_findings_have_distinct_conditions(self):
        self.with_finding()
        self.assertEqual(validator.validate_review(self.review, self.scope), [])
        self.review["findings"][0]["confidence"] = "INFERRED"
        self.invalid()
        self.review["findings"][0]["unverified_conditions"] = ["The deployment uses the affected database driver."]
        self.assertEqual(validator.validate_review(self.review, self.scope), [])
        self.review["findings"][0]["confidence"] = 0.99
        self.invalid()

    def test_each_finding_requires_text_evidence_and_supported_priority(self):
        self.with_finding()
        for key in validator.FINDING_KEYS:
            with self.subTest(key=key):
                changed = copy.deepcopy(self.review)
                del changed["findings"][0][key]
                self.invalid(changed)
        for key, value in (("title", " "), ("owner", None), ("evidence_refs", []),
                           ("evidence_refs", [None]), ("unverified_conditions", [" "]),
                           ("priority", "high"), ("priority", {})):
            changed = copy.deepcopy(self.review)
            changed["findings"][0][key] = value
            self.invalid(changed)

    def test_duplicate_findings_and_axis_mismatch_are_invalid(self):
        self.with_finding()
        self.review["findings"] *= 2
        self.invalid()
        self.review["findings"] = [finding()]
        self.review["axes"]["tests"]["status"] = "REVIEWED"
        self.invalid()
        self.review["findings"] = []
        self.review["axes"]["tests"]["status"] = "ISSUES_FOUND"
        self.invalid()

    def test_one_root_cause_can_mark_related_axes_without_duplicate_findings(self):
        self.with_finding()
        self.review["findings"][0]["related_axes"] = ["spec", "security"]
        for axis in ("spec", "security"):
            self.review["axes"][axis]["status"] = "ISSUES_FOUND"
        self.assertEqual(validator.validate_review(self.review, self.scope), [])
        self.assertEqual(len(self.review["findings"]), 1)
        self.review["axes"]["spec"]["status"] = "REVIEWED"
        self.invalid()

    def test_related_axes_require_unique_supported_names_and_exclude_primary_axis(self):
        self.with_finding()
        for value in (None, {}, ["spec", "spec"], ["tests"], ["PRIVATE_PAYLOAD"], [{}]):
            changed = copy.deepcopy(self.review)
            changed["findings"][0]["related_axes"] = value
            self.invalid(changed)

    def test_inline_findings_must_use_reviewed_path_and_raw_changed_side(self):
        self.with_finding()
        for change in ({"line": True}, {"line": 0}, {"line": 1}, {"line": 3}, {"line": 2.0},
                       {"side": None}, {"side": []}, {"path": "PRIVATE_PAYLOAD"}, {"path": {}}):
            changed = copy.deepcopy(self.review)
            changed["findings"][0].update(change)
            self.invalid(changed)
        self.review["reviewed_paths"] = []
        self.review["skipped_paths"] = [{"path": "code.py", "reason": "Not inspected."}]
        self.invalid()

    def test_deletion_findings_can_use_left_raw_content_ranges(self):
        (self.repo / "code.py").unlink()
        self.scope = context_helper.collect_context(self.repo)
        self.review = report(self.scope)
        self.with_finding(finding(side="LEFT", line=3))
        self.assertEqual(validator.validate_review(self.review, self.scope), [])
        self.review["findings"][0]["side"] = "RIGHT"
        self.invalid()

    def test_file_finding_supports_binary_without_inline_anchor(self):
        self.write("binary.dat", b"a\0b")
        self.scope = context_helper.collect_context(self.repo)
        self.review = report(self.scope)
        self.with_finding(finding("binary.dat", side=None, line=None, location="FILE"))
        self.assertEqual(validator.validate_review(self.review, self.scope), [])
        self.review["findings"][0].update(location="INLINE", side="RIGHT", line=1)
        self.invalid()

    def test_file_finding_cannot_claim_inline_line_or_side(self):
        self.with_finding(finding(side=None, line=None, location="FILE"))
        self.assertEqual(validator.validate_review(self.review, self.scope), [])
        for key, value in (("line", 2), ("side", "LEFT")):
            changed = copy.deepcopy(self.review)
            changed["findings"][0][key] = value
            self.invalid(changed)

    def test_outcome_accounts_for_all_findings_and_limitations(self):
        self.with_finding()
        self.review["findings"][0]["priority"] = "P3"
        self.assertEqual(validator.validate_review(self.review, self.scope), [])
        self.review["outcome"] = "NO_ACTIONABLE_FINDINGS"
        self.invalid()
        self.review = report(self.scope)
        self.review["axes"]["spec"]["status"] = "UNVERIFIED"
        self.invalid()
        self.review["outcome"] = "INCOMPLETE"
        self.assertEqual(validator.validate_review(self.review, self.scope), [])
        self.review = report(self.scope)
        self.scope["limitations"] = ["A source contract is unavailable."]
        self.invalid()
        self.review["outcome"] = "INCOMPLETE"
        self.assertEqual(validator.validate_review(self.review, self.scope), [])

    def test_checks_distinguish_execution_from_suggestions(self):
        for state in ("PASSED", "FAILED", "ERROR"):
            self.review["checks_executed"] = [{"command": "python -m unittest", "result": state, "notes": "Recorded output inspected."}]
            self.assertEqual(validator.validate_review(self.review, self.scope), [])
        self.review["checks_executed"][0]["result"] = "SUGGESTED"
        self.invalid()
        self.review["checks_executed"] = []
        self.review["suggested_checks"] = ["Run the database integration suite."]
        self.review["unverified_assumptions"] = ["The remote deployment uses this revision."]
        self.assertEqual(validator.validate_review(self.review, self.scope), [])
        self.review["suggested_checks"] = [""]
        self.invalid()

    def test_writing_metadata_requires_recorded_review_before_pass(self):
        writing = self.review["writing_review"]
        writing["asd_review"] = "PASSED"
        self.invalid()
        writing.update(reviewer="Recorded reviewer", reviewed_at="2026-10-21T10:00:00+08:00")
        self.assertEqual(validator.validate_review(self.review, self.scope), [])
        writing["limitations"] = []
        self.invalid()
        writing["limitations"] = ["Different disclaimer."]
        self.invalid()

    def test_context_shape_revision_ids_hashes_ranges_and_paths_fail_closed(self):
        changes = (
            ("schema_version", True), ("schema_version", "1"), ("mode", {}),
            ("fingerprint", "PRIVATE_PAYLOAD"), ("base", "main"), ("head", []),
            ("comparison_base", "a" * 40), ("line_basis", "provider-diff"),
            ("limitations", [None]), ("change_count", True), ("files", "PRIVATE_PAYLOAD"),
        )
        for key, value in changes:
            with self.subTest(key=key):
                changed = copy.deepcopy(self.scope)
                changed[key] = value
                self.invalid(scope=changed)
        for key, value in (("path", "../PRIVATE_PAYLOAD"), ("status", []), ("binary", 1),
                           ("added_ranges", [[True, 2]]), ("added_ranges", [[2, 1]]),
                           ("removed_ranges", [[2, 3], [3, 4]]), ("removed_ranges", [{}]),
                           ("content_sha256", "PRIVATE_PAYLOAD")):
            changed = copy.deepcopy(self.scope)
            changed["files"][0][key] = value
            self.invalid(scope=changed)
        changed = copy.deepcopy(self.scope)
        changed["files"] *= 2
        changed["change_count"] = 2
        self.invalid(scope=changed)

    def test_unborn_local_context_is_valid_but_unborn_range_is_not(self):
        for key in ("base", "head", "comparison_base"):
            self.scope[key] = None
        self.review = report(self.scope)
        self.assertEqual(validator.validate_review(self.review, self.scope), [])
        self.scope["mode"] = "range"
        self.invalid()

    def test_malformed_nested_values_never_raise_or_echo_source(self):
        deep = {"PRIVATE_PAYLOAD": {"nested": [None]}}
        for key in validator.REPORT_KEYS:
            with self.subTest(key=key):
                changed = copy.deepcopy(self.review)
                changed[key] = copy.deepcopy(deep)
                self.invalid(changed)
        self.with_finding()
        for key in validator.FINDING_KEYS:
            with self.subTest(finding_key=key):
                changed = copy.deepcopy(self.review)
                changed["findings"][0][key] = copy.deepcopy(deep)
                self.invalid(changed)
        for bad in (None, [], "PRIVATE_PAYLOAD", True, 1):
            self.invalid(review=bad)
            self.invalid(scope=bad)

    def test_cli_rejects_duplicate_keys_nonfinite_and_deep_or_oversized_json(self):
        raws = (
            '{"summary":"PRIVATE_PAYLOAD","summary":"again"}',
            '{"value":NaN}', '{"value":Infinity}', '{"value":-Infinity}',
            '{"nested":{"PRIVATE_PAYLOAD":1e999}}', '{"nested":[-1e999]}',
            '[' * 65 + '"PRIVATE_PAYLOAD"' + ']' * 65,
            '"' + 'a' * validator.MAX_INPUT_BYTES + '"',
            '{"nested":{"same":1,"same":2}}',
        )
        for raw in raws:
            with self.subTest(raw=raw[:30]):
                result = self.run_cli(raw_review=raw)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(json.loads(result.stdout)["status"], "INVALID")
                self.assertNotIn(b"PRIVATE_PAYLOAD", result.stdout + result.stderr)
        self.assertEqual(self.run_cli(raw_context='{"a":1,"a":2}').returncode, 2)

    def test_cli_redacts_input_paths_argument_values_and_structure_values(self):
        self.review["summary"] = ""
        self.review["PRIVATE_PAYLOAD"] = "PRIVATE_PAYLOAD"
        result = self.run_cli()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(b"PRIVATE_PAYLOAD", result.stdout + result.stderr)
        for args in (("--unknown=PRIVATE_PAYLOAD",), ("--git-command=PRIVATE_PAYLOAD",)):
            result = self.run_cli(extra=args)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn(b"PRIVATE_PAYLOAD", result.stdout + result.stderr)
        result = subprocess.run([sys.executable, str(SCRIPTS / "validate_review.py"),
                                 "--review", str(self.root / "PRIVATE_PAYLOAD"), "--context", "missing"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(b"PRIVATE_PAYLOAD", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
