"""Consequential boundaries for the read-only, redacted review candidate helper."""

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / ".agents/skills/code-review/scripts/scan_changes.py"
SPEC = importlib.util.spec_from_file_location("code_review_scan", SCRIPT)
SCAN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCAN)


class ScanChangesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git("init", "-q")
        (self.repo / "app.txt").write_text("ordinary baseline\n", encoding="utf-8")
        self.git("add", "app.txt")
        self.git("-c", "user.name=Review test", "-c", "user.email=review@example.invalid", "commit", "-qm", "baseline")

    def git(self, *args):
        return subprocess.run(
            ["git", *args], cwd=self.repo, check=True, capture_output=True, text=True,
        ).stdout.strip()

    def write(self, text, name="app.txt"):
        (self.repo / name).write_text(text, encoding="utf-8")

    def cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(self.repo), *args],
            capture_output=True, text=True,
        )

    def test_staged_scan_uses_index_when_worktree_differs(self):
        token = "ghp_" + "A" * 36
        self.write('token = "' + token + '"\n')
        self.git("add", "app.txt")
        self.write("ordinary worktree replacement\n")
        staged = SCAN.scan_changes(self.repo, mode="staged")
        worktree = SCAN.scan_changes(self.repo)
        self.assertEqual([item["id"] for item in staged["findings"]], ["secret.provider-token"])
        self.assertEqual(worktree["findings"], [])
        self.assertNotEqual(staged["context"]["fingerprint"], worktree["context"]["fingerprint"])

    def test_cli_redacts_secret_values_and_source_lines(self):
        token = "ghp_" + "B" * 36
        source_line = 'source_sentinel = "' + token + '"'
        self.write(source_line + "\n")
        result = self.cli()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertNotIn(token, result.stdout)
        self.assertNotIn(source_line, result.stdout)
        self.assertNotIn("source_sentinel", result.stdout)
        data = json.loads(result.stdout)
        self.assertEqual(data["status"], "FINDINGS")
        self.assertEqual(data["findings"][0]["line"], 1)
        self.assertEqual(data["findings"][0]["kind"], "candidate")
        self.assertTrue(any("complete credential absence" in limit for limit in data["limitations"]))

    def test_placeholder_and_environment_values_are_not_generic_candidates(self):
        self.write("\n".join([
            'password = "${DATABASE_PASSWORD}"',
            'api_key = "your-api-key-here"',
            'secret = "<replace-with-secret>"',
            'token = "xxxxxxxxxxxxxxxxxx"',
            'authToken = "process.env.API_TOKEN"',
            'client_secret = "not-a-real-secret"',
            'password = "password123"',
        ]) + "\n")
        result = SCAN.scan_changes(self.repo)
        self.assertEqual([(item["id"], item["line"]) for item in result["findings"]], [
            ("secret.credential-assignment", 7),
        ])

    def test_high_signal_patterns_are_distinct_candidates(self):
        self.write("\n".join([
            "-----BEGIN PRIVATE KEY-----",
            "AKIA" + "C" * 16,
            "https://example.invalid/blob?sv=2024-01-01&sig=" + "D" * 32,
        ]) + "\n")
        result = SCAN.scan_changes(self.repo)
        self.assertEqual([item["id"] for item in result["findings"]], [
            "secret.private-key", "secret.aws-access-id", "secret.azure-sas",
        ])
        self.assertIn("identifier", result["findings"][1]["message"])

    def test_custom_exclusion_cannot_hide_secret(self):
        self.write('FIXME token = "ghp_' + "E" * 36 + '"\n')
        result = SCAN.scan_changes(self.repo, rules={
            "exclude": ["*.txt"],
            "rules": [{"id": "no-fixme", "contains": "FIXME", "severity": "LOW"}],
        })
        self.assertEqual([item["id"] for item in result["findings"]], ["secret.provider-token"])

    def test_nearby_is_same_file_physical_added_line_distance(self):
        self.write("THROW\n" + "padding\n" * 5 + "LOG\n")
        self.write("LOG\n", "other.txt")
        rules = {"rules": [{
            "id": "requires-log", "contains": "THROW", "requires_nearby": "LOG", "severity": "HIGH",
        }]}
        result = SCAN.scan_changes(self.repo, rules=rules)
        self.assertEqual([(item["path"], item["line"]) for item in result["findings"]], [("app.txt", 1)])
        self.write("THROW\n" + "padding\n" * 4 + "LOG\n")
        self.assertEqual(SCAN.scan_changes(self.repo, rules=rules)["findings"], [])

    def test_nearby_does_not_use_unchanged_or_cross_file_lines(self):
        self.write("LOG\n" + "padding\n" * 20)
        self.git("add", "app.txt")
        self.git("-c", "user.name=Review test", "-c", "user.email=review@example.invalid", "commit", "-qm", "context")
        self.write("LOG\nTHROW\n" + "padding\n" * 20)
        self.write("LOG\n", "other.txt")
        result = SCAN.scan_changes(self.repo, rules={"rules": [{
            "id": "requires-log", "contains": "THROW", "requires_nearby": "LOG", "severity": "HIGH",
        }]})
        self.assertEqual([(item["path"], item["line"]) for item in result["findings"]], [("app.txt", 2)])

    def test_literal_rules_do_not_execute_regex_and_can_ignore_case(self):
        self.write("A.*B\nfixme\nAXXB\n")
        result = SCAN.scan_changes(self.repo, rules={"rules": [
            {"id": "literal", "contains": "A.*B", "severity": "LOW"},
            {"id": "casefold", "contains": "FIXME", "severity": "MEDIUM", "case_sensitive": False},
        ]})
        self.assertEqual([(item["id"], item["line"]) for item in result["findings"]], [
            ("literal", 1), ("casefold", 2),
        ])

    def test_invalid_configs_fail_closed_without_echoing_values(self):
        bad_configs = [
            {"rules": [{"id": "bad", "pattern": "secret-sentinel", "severity": "HIGH"}]},
            {"rules": [{"id": "bad", "contains": "x", "severity": "HIGH", "case_sensitive": "false"}]},
            {"rules": [{"id": "bad", "contains": "", "severity": "HIGH"}]},
            {"rules": [{"id": "bad", "contains": "x", "severity": "BLOCKER"}]},
            {"rules": [{"id": "same", "contains": "x", "severity": "HIGH"}] * 2},
            {"rules": [], "exclude": "*"},
            {"rules": [], "unexpected": "secret-sentinel"},
        ]
        for config in bad_configs:
            with self.subTest(config=config):
                with self.assertRaises(SCAN.ScanError) as error:
                    SCAN.scan_changes(self.repo, rules=config)
                self.assertNotIn("secret-sentinel", str(error.exception))
        rule_file = self.repo / "rules.json"
        for raw in (
            '{"rules": [], "rules": [], "sentinel": "secret-sentinel"}',
            '{"rules": NaN}',
            "secret-sentinel" * SCAN.MAX_RULE_FILE_BYTES,
            '{"rules": [',
        ):
            rule_file.write_text(raw, encoding="utf-8")
            result = self.cli("--rules", str(rule_file))
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertNotIn("secret-sentinel", result.stderr)

    def test_cli_accepts_explicit_rules_only(self):
        self.write("FIXME\n")
        self.write(json.dumps({"rules": [{"id": "fixme", "contains": "FIXME", "severity": "LOW"}]}), "rules.json")
        self.assertEqual(self.cli().returncode, 0)
        result = self.cli("--rules", str(self.repo / "rules.json"))
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(result.stdout)["findings"][0]["id"], "fixme")

    def test_rule_fingerprint_binds_rules_without_echoing_literal_text(self):
        literal = "CONTEXT_RULE_SENSITIVE_MARKER"
        self.write(literal + "\n")
        rules = {"rules": [{"id": "private-rule", "contains": literal, "severity": "LOW"}]}
        initial = SCAN.scan_changes(self.repo, rules=rules)
        self.assertNotIn(literal, json.dumps(initial))
        self.assertRegex(initial["rules_fingerprint"], r"^[0-9a-f]{64}$")
        rules["rules"][0]["contains"] = "another-literal"
        changed = SCAN.scan_changes(self.repo, rules=rules)
        self.assertNotEqual(initial["rules_fingerprint"], changed["rules_fingerprint"])
        self.assertIsNone(SCAN.scan_changes(self.repo)["rules_fingerprint"])

    def test_cli_does_not_create_helper_bytecode_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            tool_dir = Path(directory)
            for name in ("scan_changes.py", "review_context.py"):
                shutil.copyfile(SCRIPT.with_name(name), tool_dir / name)
            environment = dict(os.environ)
            environment.pop("PYTHONDONTWRITEBYTECODE", None)
            result = subprocess.run(
                [sys.executable, str(tool_dir / "scan_changes.py"), "--repo", str(self.repo)],
                env=environment, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(sorted(path.name for path in tool_dir.iterdir()), [
                "review_context.py", "scan_changes.py",
            ])

    def test_no_findings_is_complete_with_limits_and_deleted_secrets_are_not_scanned(self):
        self.write('token = "ghp_' + "F" * 36 + '"\n')
        self.git("add", "app.txt")
        self.git("-c", "user.name=Review test", "-c", "user.email=review@example.invalid", "commit", "-qm", "historical fixture")
        self.write("ordinary replacement\n")
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["findings"], [])
        self.assertEqual(data["status"], "COMPLETE_WITH_LIMITS")

    def test_missing_repository_and_invalid_arguments_are_redacted_errors(self):
        for args in (
            ["--repo", str(self.repo / "missing-secret-sentinel")],
            ["--base", "missing-secret-sentinel", "--mode", "range"],
            ["--mode", "secret-sentinel"],
            ["--git-command", "missing-secret-sentinel"],
        ):
            result = self.cli(*args)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertNotIn("secret-sentinel", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_scan_preserves_worktree_and_index(self):
        self.write("FIXME\n")
        self.git("add", "app.txt")
        self.write("FIXME plus worktree edit\n")
        before = self.git("status", "--porcelain=v1")
        index_before = (self.repo / ".git/index").read_bytes()
        source_before = (self.repo / "app.txt").read_bytes()
        SCAN.scan_changes(self.repo)
        self.assertEqual(self.git("status", "--porcelain=v1"), before)
        self.assertEqual((self.repo / ".git/index").read_bytes(), index_before)
        self.assertEqual((self.repo / "app.txt").read_bytes(), source_before)


if __name__ == "__main__":
    unittest.main()
