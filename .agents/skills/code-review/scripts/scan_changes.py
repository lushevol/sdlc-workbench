#!/usr/bin/env python3
"""Report redacted secret and optional literal-rule candidates in added lines.

This helper reads local Git state. It does not establish credential validity,
execute source files, retain a diff, or change the repository.
"""

import argparse
import fnmatch
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys


def _load_context_helper():
    # Loading by file path also supports callers using importlib on this script.
    module_name = "_code_review_scan_context"
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(
        module_name, Path(__file__).with_name("review_context.py")
    )
    if spec is None or spec.loader is None:
        raise ImportError("Review context helper is unavailable.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    previous_bytecode_setting = sys.dont_write_bytecode
    try:
        # Importing the shipped helper must not create a repository cache file.
        sys.dont_write_bytecode = True
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    finally:
        sys.dont_write_bytecode = previous_bytecode_setting
    return module


class ScanError(ValueError):
    """A failure whose message contains no source text or credential value."""


MAX_RULE_FILE_BYTES = 65536
MAX_RULES = 128
MAX_LITERAL_LENGTH = 512
SEVERITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
_RULE_FIELDS = {"id", "contains", "severity", "case_sensitive", "requires_nearby"}
_PRIVATE_KEY = re.compile(
    r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----"
)
_PROVIDER_TOKEN = re.compile(
    r"(?<![A-Za-z0-9_])(?:"
    r"gh[pousr]_[A-Za-z0-9]{36}"
    r"|github_pat_[A-Za-z0-9_]{22,255}"
    r"|glpat-[A-Za-z0-9_-]{20,255}"
    r"|xox[baprs]-[A-Za-z0-9-]{20,255}"
    r"|sk_(?:live|test)_[A-Za-z0-9]{16,255}"
    r"|AIza[A-Za-z0-9_-]{35}"
    r"|npm_[A-Za-z0-9]{36}"
    r"|pypi-[A-Za-z0-9_-]{48,255}"
    r"|sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,255}"
    r")(?![A-Za-z0-9_])"
)
_AWS_ACCESS_ID = re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")
_SAS_VERSION = re.compile(r"\bsv=\d{4}-\d{2}-\d{2}\b", re.IGNORECASE)
_SAS_SIGNATURE = re.compile(r"\bsig=[A-Za-z0-9%+/=_-]{16,}", re.IGNORECASE)
_ASSIGNMENT = re.compile(
    r"(?<![A-Za-z0-9_])[\"']?(?P<name>[A-Za-z_][A-Za-z0-9_.-]{0,127})"
    r"[\"']?\s*(?:=|:)\s*(?P<quote>[\"'])"
    r"(?P<value>[^\"'\r\n]{8,512})(?P=quote)"
)
_CREDENTIAL_NAMES = (
    "password", "passwd", "pwd", "secret", "token", "pat", "apikey", "privatekey"
)


def _invalid_rules():
    return ScanError("Invalid custom rule configuration; see the documented JSON schema.")


def _literal(value):
    return (
        isinstance(value, str)
        and 0 < len(value) <= MAX_LITERAL_LENGTH
        and bool(value.strip())
        and not any(ord(char) < 32 or ord(char) == 127 for char in value)
    )


def validate_rules(config):
    """Validate opt-in rule data without accepting executable patterns."""
    if not isinstance(config, dict) or set(config) - {"rules", "exclude"}:
        raise _invalid_rules()
    rules = config.get("rules")
    exclusions = config.get("exclude", [])
    if not isinstance(rules, list) or len(rules) > MAX_RULES:
        raise _invalid_rules()
    if not isinstance(exclusions, list) or len(exclusions) > MAX_RULES:
        raise _invalid_rules()
    if any(not _literal(pattern) for pattern in exclusions):
        raise _invalid_rules()
    result = []
    seen = set()
    for rule in rules:
        if not isinstance(rule, dict) or set(rule) - _RULE_FIELDS:
            raise _invalid_rules()
        rule_id = rule.get("id")
        if (
            not isinstance(rule_id, str)
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", rule_id)
            or rule_id in seen
            or not _literal(rule.get("contains"))
            or not isinstance(rule.get("severity"), str)
            or rule["severity"] not in SEVERITIES
            or type(rule.get("case_sensitive", True)) is not bool
            or ("requires_nearby" in rule and not _literal(rule["requires_nearby"]))
        ):
            raise _invalid_rules()
        seen.add(rule_id)
        result.append(dict(rule, case_sensitive=rule.get("case_sensitive", True)))
    return {"rules": result, "exclude": list(exclusions)}


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise _invalid_rules()
        result[key] = value
    return result


def _reject_constant(_value):
    raise _invalid_rules()


def load_rules(path):
    """Read a bounded, strict JSON rule file. Return no file contents on error."""
    try:
        with Path(path).open("rb") as handle:
            raw = handle.read(MAX_RULE_FILE_BYTES + 1)
        if len(raw) > MAX_RULE_FILE_BYTES:
            raise _invalid_rules()
        return validate_rules(json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        ))
    except (OSError, UnicodeError, ValueError, TypeError, RecursionError):
        raise _invalid_rules() from None


def _placeholder(value):
    value = value.strip()
    lower = value.casefold()
    if not value or re.fullmatch(r"[xX*._-]+", value):
        return True
    if re.fullmatch(r"\$(?:\{[^}]+\}|[A-Za-z_][A-Za-z0-9_]*)", value):
        return True
    if value.startswith(("${", "{{", "<")):
        return True
    return bool(re.match(
        r"(?:your[_ -]|replace[_ -]|placeholder\b|example\b|dummy\b|fake\b|"
        r"redacted\b|change[_ -]?me\b|not[_ -]a[_ -]real\b|"
        r"test[_ -](?:token|secret|password|api[_ -]?key)\b|"
        r"(?:process\.env|os\.environ|os\.getenv)\b)", lower
    ))


def _secret_candidates(text):
    results = []
    if _PRIVATE_KEY.search(text):
        results.append(("secret.private-key", "CRITICAL", "Possible private key material."))
    if _PROVIDER_TOKEN.search(text):
        results.append(("secret.provider-token", "HIGH", "Possible provider token."))
    if _AWS_ACCESS_ID.search(text):
        results.append((
            "secret.aws-access-id", "MEDIUM",
            "Possible AWS access key identifier; check for associated credential exposure.",
        ))
    if _SAS_VERSION.search(text) and _SAS_SIGNATURE.search(text):
        results.append(("secret.azure-sas", "HIGH", "Possible Azure SAS credential."))
    if not results:
        for match in _ASSIGNMENT.finditer(text):
            name = re.sub(r"[_.-]", "", match["name"]).casefold()
            if name.endswith(_CREDENTIAL_NAMES) and not _placeholder(match["value"]):
                results.append((
                    "secret.credential-assignment", "MEDIUM",
                    "Possible hard-coded credential assignment.",
                ))
                break
    return results


def _finding(item, rule_id, severity, message, check):
    return {
        "path": item["path"], "line": item["line"], "id": rule_id,
        "severity": severity, "kind": "candidate", "check": check,
        "message": message + " Confirm the surrounding context.",
    }


def scan_changes(repo, mode="worktree", base=None, head="HEAD", git_command=None, rules=None):
    """Scan one exact review context. Custom exclusions never suppress secrets."""
    config = validate_rules(rules) if rules is not None else {"rules": [], "exclude": []}
    try:
        context, added_lines = _load_context_helper().collect_changes(
            repo, mode=mode, base=base, head=head, git_command=git_command,
        )
    except (OSError, ValueError, ImportError):
        raise ScanError(
            "Unable to inspect changes; check the repository, revisions, and Git command."
        ) from None
    findings = []
    by_path = {}
    for item in added_lines:
        by_path.setdefault(item["path"], {})[item["line"]] = item["text"]
        for rule_id, severity, message in _secret_candidates(item["text"]):
            findings.append(_finding(item, rule_id, severity, message, "secret_patterns"))
    for item in added_lines:
        if any(fnmatch.fnmatchcase(item["path"], pattern) for pattern in config["exclude"]):
            continue
        for rule in config["rules"]:
            normalize = (lambda value: value) if rule["case_sensitive"] else str.casefold
            if normalize(rule["contains"]) not in normalize(item["text"]):
                continue
            if "requires_nearby" in rule:
                required = normalize(rule["requires_nearby"])
                if any(
                    required in normalize(by_path[item["path"]].get(number, ""))
                    for number in range(max(1, item["line"] - 5), item["line"] + 6)
                ):
                    continue
            findings.append(_finding(
                item, rule["id"], rule["severity"],
                "Custom literal rule matched an added line.", "custom_rules",
            ))
    limitations = list(context["limitations"])
    limitations.extend([
        "Secret patterns do not establish complete credential absence.",
        "All candidates require contextual confirmation; pattern matches do not establish validity.",
    ])
    if config["rules"]:
        limitations.append(
            "Custom nearby checks inspect added lines within five physical lines in the same file; unchanged lines are unavailable."
        )
    identity_fields = ("repository", "mode", "head", "base", "comparison_base", "fingerprint")
    return {
        "schema_version": 1,
        "status": "FINDINGS" if findings else ("COMPLETE_WITH_LIMITS" if limitations else "COMPLETE"),
        "context": {key: context.get(key) for key in identity_fields},
        "rules_fingerprint": hashlib.sha256(json.dumps(
            config, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        ).encode("utf-8")).hexdigest() if rules is not None else None,
        "checks": {
            "secret_patterns": "COMPLETE",
            "custom_rules": "COMPLETE" if rules is not None else "NOT_REQUESTED",
            "added_lines_scanned": len(added_lines),
            "changed_files": context["change_count"],
        },
        "findings": sorted(findings, key=lambda item: (item["path"], item["line"], item["id"])),
        "limitations": list(dict.fromkeys(limitations)),
    }


class _Parser(argparse.ArgumentParser):
    def error(self, _message):
        self.print_usage(sys.stderr)
        self.exit(2, "scan_changes: invalid arguments; use --help for supported options.\n")


def main(argv=None):
    parser = _Parser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--mode", choices=("worktree", "staged", "branch", "range"), default="worktree")
    parser.add_argument("--base")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--git-command", help="Git executable and optional wrapper arguments, parsed without a shell")
    parser.add_argument("--rules", help="Opt-in JSON file with literal custom rules")
    args = parser.parse_args(argv)
    try:
        result = scan_changes(
            args.repo, mode=args.mode, base=args.base, head=args.head,
            git_command=args.git_command, rules=load_rules(args.rules) if args.rules else None,
        )
    except ScanError as error:
        print("scan_changes: " + str(error), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))
    return 1 if result["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
