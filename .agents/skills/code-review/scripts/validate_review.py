#!/usr/bin/env python3
"""Check review structure and raw-content ranges; optionally recollect local scope.

This skill-local format is not a Workbench governance or approval schema.
Validation cannot establish whether a technical claim or citation is correct.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
import re
import sys


MAX_INPUT_BYTES = 4 * 1024 * 1024
MAX_JSON_DEPTH = 64
MAX_ERRORS = 256
AXES = frozenset(("spec", "standards", "security", "integration", "tests"))
AXIS_STATUSES = frozenset(("REVIEWED", "ISSUES_FOUND", "UNVERIFIED", "NOT_APPLICABLE"))
TARGET_KEYS = frozenset(("repository", "mode", "base", "head", "comparison_base", "fingerprint", "line_basis"))
REPORT_KEYS = frozenset(("schema_version", "target", "axes", "outcome", "reviewed_paths", "skipped_paths",
                         "findings", "checks_executed", "suggested_checks", "unverified_assumptions", "summary",
                         "writing_review"))
CONTEXT_KEYS = TARGET_KEYS | {"schema_version", "files", "limitations", "change_count"}
FINDING_KEYS = frozenset(("id", "axis", "priority", "confidence", "title", "path", "location", "side", "line",
                          "trigger", "impact", "owner", "fix", "verification", "evidence_refs", "unverified_conditions"))
FINDING_OPTIONAL_KEYS = frozenset(("related_axes",))
WRITING_LIMIT = "Automated checks do not check the complete approved dictionary or grammar rules."
STRUCTURAL_LIMITS = (
    "Structural and raw-content range checks do not verify technical findings or cited evidence.",
    "Revalidate provider diff anchors and current revisions before publishing inline comments.",
    "Validation does not authenticate reviewers or establish complete ASD-STE100 compliance.",
)
HASH = re.compile(r"[0-9a-f]{64}\Z")
COMMIT = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")


class InputError(ValueError):
    """An input could not be decoded without exposing its contents."""


class Checks:
    def __init__(self):
        self.errors = []

    def require(self, condition, locator, rule):
        if not condition and len(self.errors) < MAX_ERRORS:
            self.errors.append(locator + ": " + rule)
        return bool(condition)

    def object(self, value, locator, required, optional=frozenset()):
        if not self.require(isinstance(value, dict), locator, "object required"):
            return None
        self.require(set(value) >= set(required) and set(value) <= set(required) | set(optional),
                     locator, "unsupported or missing fields")
        return value

    def array(self, value, locator):
        return self.require(isinstance(value, list), locator, "array required")

    def text(self, value, locator):
        return self.require(isinstance(value, str) and bool(value.strip()) and "\0" not in value,
                            locator, "nonempty text required")

    def strings(self, value, locator, *, nonempty=False):
        if not self.array(value, locator):
            return False
        ok = self.require(not nonempty or bool(value), locator, "nonempty array required")
        for index, item in enumerate(value):
            ok = self.text(item, f"{locator}[{index}]") and ok
        return ok

    def enum(self, value, choices, locator):
        return self.require(isinstance(value, str) and value in choices, locator, "unsupported value")

    def path(self, value, locator):
        # Git paths use slash separators. Newlines and backslashes can be literal names.
        ok = isinstance(value, str) and bool(value) and "\0" not in value
        ok = ok and not value.startswith("/") and all(part not in {"", ".", ".."} for part in value.split("/"))
        return self.require(ok, locator, "repository-relative path required")


def _ranges(checks, value, locator):
    if not checks.array(value, locator):
        return
    previous = 0
    for index, pair in enumerate(value):
        name = f"{locator}[{index}]"
        if not checks.require(isinstance(pair, list) and len(pair) == 2, name, "inclusive line pair required"):
            continue
        if not checks.require(all(type(number) is int and number > 0 for number in pair),
                              name, "positive integer lines required"):
            continue
        checks.require(previous < pair[0] <= pair[1], name, "ordered disjoint ranges required")
        previous = pair[1]


def _context(checks, context):
    value = checks.object(context, "context", CONTEXT_KEYS)
    if value is None:
        return {}
    checks.require(type(value.get("schema_version")) is int and value.get("schema_version") == 1,
                   "context.schema_version", "version 1 required")
    checks.text(value.get("repository"), "context.repository")
    checks.enum(value.get("mode"), {"worktree", "staged", "branch", "range"}, "context.mode")
    checks.require(value.get("line_basis") == "raw-content-comparison", "context.line_basis", "raw-content basis required")
    fingerprint = value.get("fingerprint")
    checks.require(isinstance(fingerprint, str) and HASH.fullmatch(fingerprint) is not None,
                   "context.fingerprint", "SHA-256 required")
    commits_valid = True
    for key in ("base", "head", "comparison_base"):
        commit = value.get(key)
        commits_valid = checks.require(commit is None or isinstance(commit, str) and COMMIT.fullmatch(commit) is not None,
                                       "context." + key, "full commit ID or null required") and commits_valid
    if commits_valid:
        commits = [value.get(key) for key in ("base", "head", "comparison_base")]
        checks.require(len({len(commit) for commit in commits if commit is not None}) <= 1,
                       "context", "commit ID lengths must match")
        if value.get("mode") in ("worktree", "staged"):
            checks.require(commits[0] == commits[1] == commits[2], "context", "local revision identities must match")
        else:
            checks.require(all(commit is not None for commit in commits), "context", "committed revisions required")
            if value.get("mode") == "range":
                checks.require(commits[0] == commits[2], "context", "range comparison must use base")
    checks.strings(value.get("limitations"), "context.limitations")
    files = value.get("files")
    records = {}
    if checks.array(files, "context.files"):
        for index, record in enumerate(files):
            name = f"context.files[{index}]"
            record = checks.object(record, name, {"path", "status", "content_sha256", "before_content_sha256", "added_ranges", "removed_ranges", "binary"},
                                   {"old_path"})
            if record is None:
                continue
            path = record.get("path")
            if checks.path(path, name + ".path"):
                checks.require(path not in records, name + ".path", "duplicate context path")
                records[path] = record
            status = record.get("status")
            checks.enum(status, {"A", "D", "M", "R", "T"}, name + ".status")
            if status == "R":
                checks.path(record.get("old_path"), name + ".old_path")
                checks.require(record.get("old_path") != path, name + ".old_path", "rename requires different paths")
            else:
                checks.require("old_path" not in record, name + ".old_path", "old path requires rename status")
            content = record.get("content_sha256")
            for key in ("content_sha256", "before_content_sha256"):
                digest = record.get(key)
                checks.require(digest is None or isinstance(digest, str) and HASH.fullmatch(digest) is not None,
                               name + "." + key, "SHA-256 or null required")
            checks.require(type(record.get("binary")) is bool, name + ".binary", "boolean required")
            _ranges(checks, record.get("added_ranges"), name + ".added_ranges")
            _ranges(checks, record.get("removed_ranges"), name + ".removed_ranges")
            if status == "D":
                checks.require(record.get("added_ranges") == [] and content is None, name, "deleted content cannot have added lines")
            if status == "A":
                checks.require(record.get("removed_ranges") == [], name, "added content cannot have removed lines")
        checks.require(type(value.get("change_count")) is int and value.get("change_count") == len(files),
                       "context.change_count", "file count must match")
    return records


def _writing(checks, value):
    name = "review.writing_review"
    value = checks.object(value, name, {"standard", "automated_check", "asd_review", "reviewer", "reviewed_at", "limitations"})
    if value is None:
        return
    checks.require(value.get("standard") == "ASD-STE100", name + ".standard", "ASD-STE100 required")
    checks.enum(value.get("automated_check"), {"NOT_RUN", "PASSED", "FAILED"}, name + ".automated_check")
    checks.enum(value.get("asd_review"), {"PENDING", "PASSED", "FAILED"}, name + ".asd_review")
    for key in ("reviewer", "reviewed_at"):
        if value.get(key) is not None or value.get("asd_review") == "PASSED":
            checks.text(value.get(key), name + "." + key)
    limits = value.get("limitations")
    if checks.strings(limits, name + ".limitations", nonempty=True):
        checks.require(WRITING_LIMIT in limits, name + ".limitations", "automated writing check limit required")


def validate_review(review, context):
    """Return fixed, redacted structural diagnostics. This function performs no I/O."""
    checks = Checks()
    records = _context(checks, context)
    if checks.errors:
        return checks.errors
    value = checks.object(review, "review", REPORT_KEYS)
    if value is None:
        return checks.errors
    checks.require(value.get("schema_version") == "1.0", "review.schema_version", "version 1.0 required")
    target = checks.object(value.get("target"), "review.target", TARGET_KEYS)
    if target is not None:
        # Compare only primitive expected values. A malformed nested target stays an error.
        for key in sorted(TARGET_KEYS):
            actual, expected = target.get(key), context[key]
            checks.require(type(actual) is type(expected) and actual == expected,
                           "review.target." + key, "context identity mismatch")
    axes = checks.object(value.get("axes"), "review.axes", AXES)
    statuses = {}
    if axes is not None:
        for axis in sorted(AXES):
            state = checks.object(axes.get(axis), "review.axes." + axis, {"status", "reason"})
            if state is not None:
                if checks.enum(state.get("status"), AXIS_STATUSES, "review.axes." + axis + ".status"):
                    statuses[axis] = state["status"]
                checks.text(state.get("reason"), "review.axes." + axis + ".reason")
    reviewed = value.get("reviewed_paths")
    reviewed_set = set()
    if checks.strings(reviewed, "review.reviewed_paths"):
        reviewed_set = set(reviewed)
        checks.require(len(reviewed) == len(reviewed_set), "review.reviewed_paths", "duplicate coverage path")
    skipped = value.get("skipped_paths")
    skipped_names = []
    if checks.array(skipped, "review.skipped_paths"):
        for index, item in enumerate(skipped):
            name = f"review.skipped_paths[{index}]"
            item = checks.object(item, name, {"path", "reason"})
            if item is not None:
                if checks.text(item.get("path"), name + ".path"):
                    skipped_names.append(item["path"])
                checks.text(item.get("reason"), name + ".reason")
    skipped_set = set(skipped_names)
    checks.require(len(skipped_names) == len(skipped_set), "review.skipped_paths", "duplicate coverage path")
    checks.require(not reviewed_set & skipped_set, "review", "reviewed and skipped paths must be disjoint")
    checks.require(reviewed_set | skipped_set == set(records), "review", "coverage must exactly match context paths")
    findings = value.get("findings")
    seen_ids, finding_axes = set(), set()
    if checks.array(findings, "review.findings"):
        for index, finding in enumerate(findings):
            name = f"review.findings[{index}]"
            finding = checks.object(finding, name, FINDING_KEYS, FINDING_OPTIONAL_KEYS)
            if finding is None:
                continue
            if checks.text(finding.get("id"), name + ".id"):
                checks.require(finding["id"] not in seen_ids, name + ".id", "duplicate finding ID")
                seen_ids.add(finding["id"])
            axis = finding.get("axis")
            if checks.enum(axis, AXES, name + ".axis"):
                finding_axes.add(axis)
                checks.require(statuses.get(axis) == "ISSUES_FOUND", name + ".axis", "finding axis must record issues")
            related = finding.get("related_axes", [])
            if checks.strings(related, name + ".related_axes"):
                checks.require(len(related) == len(set(related)), name + ".related_axes", "duplicate related axis")
                checks.require(axis not in related, name + ".related_axes", "primary axis cannot be repeated")
                for index_related, related_axis in enumerate(related):
                    if checks.enum(related_axis, AXES, f"{name}.related_axes[{index_related}]"):
                        finding_axes.add(related_axis)
                        checks.require(statuses.get(related_axis) == "ISSUES_FOUND", name + ".related_axes",
                                       "related axis must record issues")
            checks.enum(finding.get("priority"), {"P0", "P1", "P2", "P3"}, name + ".priority")
            checks.enum(finding.get("confidence"), {"CONFIRMED", "INFERRED"}, name + ".confidence")
            for key in ("title", "trigger", "impact", "owner", "fix", "verification"):
                checks.text(finding.get(key), name + "." + key)
            checks.strings(finding.get("evidence_refs"), name + ".evidence_refs", nonempty=True)
            checks.strings(finding.get("unverified_conditions"), name + ".unverified_conditions",
                           nonempty=finding.get("confidence") == "INFERRED")
            path = finding.get("path")
            valid_path = checks.text(path, name + ".path")
            if valid_path:
                valid_path = checks.require(path in reviewed_set, name + ".path", "finding requires a reviewed path")
            location = finding.get("location")
            checks.enum(location, {"INLINE", "FILE"}, name + ".location")
            line, side = finding.get("line"), finding.get("side")
            if location == "FILE":
                checks.require(line is None and side is None, name, "file finding requires null side and line")
            elif location == "INLINE":
                valid_side = checks.enum(side, {"LEFT", "RIGHT"}, name + ".side")
                valid_line = checks.require(type(line) is int and line > 0, name + ".line", "positive integer line required")
                if valid_path and path in records and valid_side and valid_line:
                    ranges = records[path]["added_ranges" if side == "RIGHT" else "removed_ranges"]
                    checks.require(any(start <= line <= end for start, end in ranges), name + ".line",
                                   "line must belong to the selected raw-content side")
    for axis in sorted(AXES):
        if statuses.get(axis) == "ISSUES_FOUND":
            checks.require(axis in finding_axes, "review.axes." + axis, "issues require a matching finding")
    outcome = value.get("outcome")
    checks.enum(outcome, {"FINDINGS_PRESENT", "INCOMPLETE", "NO_ACTIONABLE_FINDINGS"}, "review.outcome")
    has_findings = isinstance(findings, list) and bool(findings)
    incomplete = bool(skipped_names) or "UNVERIFIED" in statuses.values() or bool(context["limitations"])
    expected = "FINDINGS_PRESENT" if has_findings or "ISSUES_FOUND" in statuses.values() else "INCOMPLETE" if incomplete else "NO_ACTIONABLE_FINDINGS"
    checks.require(outcome == expected, "review.outcome", "outcome must match findings and evidence limits")
    executed = value.get("checks_executed")
    if checks.array(executed, "review.checks_executed"):
        for index, item in enumerate(executed):
            name = f"review.checks_executed[{index}]"
            item = checks.object(item, name, {"command", "result", "notes"})
            if item is not None:
                checks.text(item.get("command"), name + ".command")
                checks.enum(item.get("result"), {"PASSED", "FAILED", "ERROR"}, name + ".result")
                checks.text(item.get("notes"), name + ".notes")
    checks.strings(value.get("suggested_checks"), "review.suggested_checks")
    checks.strings(value.get("unverified_assumptions"), "review.unverified_assumptions")
    checks.text(value.get("summary"), "review.summary")
    _writing(checks, value.get("writing_review"))
    return checks.errors


def _pairs(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise InputError("Duplicate JSON key.")
        value[key] = item
    return value


def _constant(_value):
    raise InputError("Nonfinite JSON number.")


def _finite(value):
    number = float(value)
    if not math.isfinite(number):
        raise InputError("Nonfinite JSON number.")
    return number


def _read_json(path):
    try:
        with Path(path).open("rb") as source:
            raw = source.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise InputError("Input size limit exceeded.")
        # Bound nesting before JSON decoding to prevent decoder recursion failures.
        depth, quoted, escaped = 0, False, False
        for byte in raw:
            if quoted:
                if escaped:
                    escaped = False
                elif byte == 92:
                    escaped = True
                elif byte == 34:
                    quoted = False
            elif byte == 34:
                quoted = True
            elif byte in (91, 123):
                depth += 1
                if depth > MAX_JSON_DEPTH:
                    raise InputError("Input nesting limit exceeded.")
            elif byte in (93, 125):
                depth -= 1
        return json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_constant, parse_float=_finite)
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        raise InputError("Cannot read bounded strict JSON input.") from error


def _recollect(repo, context, git_command):
    # Load the trusted sibling helper, never a module or path from review content.
    path = Path(__file__).resolve().with_name("review_context.py")
    spec = importlib.util.spec_from_file_location("_review_scope_validation", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
        options = {"mode": context["mode"], "git_command": git_command}
        if context["mode"] in {"branch", "range"}:
            options.update(base=context["base"], head=context["head"])
        return module.collect_context(repo, **options)
    finally:
        sys.dont_write_bytecode = bytecode
        sys.modules.pop(spec.name, None)


def main(argv=None):
    class RedactedParser(argparse.ArgumentParser):
        def error(self, _message):
            raise InputError("Invalid validation arguments.")

    parser = RedactedParser(description=__doc__)
    parser.add_argument("--review", required=True)
    parser.add_argument("--context", required=True)
    parser.add_argument("--repo", help="Explicit repository to recollect; no repository path is executed from JSON.")
    parser.add_argument("--git-command", help="Argument wrapper for trusted Git, for example 'sc-cli git'. No shell is used.")
    limits = list(STRUCTURAL_LIMITS)
    try:
        args = parser.parse_args(argv)
        if args.git_command and not args.repo:
            raise InputError("A Git wrapper requires an explicit repository.")
        review, context = _read_json(args.review), _read_json(args.context)
        errors = validate_review(review, context)
        if args.repo and not errors:
            try:
                current = _recollect(args.repo, context, args.git_command)
            except (ValueError, OSError, UnicodeError, ImportError) as error:
                raise InputError("Cannot independently recollect the review context.") from error
            if current != context:
                errors.append("context: recollected scope mismatch")
            limits.append("Recollection checks resolved commit IDs; it does not verify moving refs or the latest remote head.")
        elif not args.repo:
            limits.append("Supplied context was not independently recollected.")
    except InputError:
        print(json.dumps({"status": "INVALID", "errors": ["input: cannot read strict JSON or recollect context"],
                          "limitations": limits}, sort_keys=True))
        return 2
    print(json.dumps({"status": "INVALID" if errors else "VALID", "errors": errors, "limitations": limits}, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
