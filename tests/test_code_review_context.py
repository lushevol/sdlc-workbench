"""Exercise review scope boundaries against real temporary Git repositories."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / ".agents/skills/code-review/scripts/review_context.py"
SPEC = importlib.util.spec_from_file_location("code_review_context", SCRIPT)
context = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = context
SPEC.loader.exec_module(context)


class ReviewContextTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git("init", "-b", "main")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Review Test")
        self.git("config", "core.autocrlf", "false")

    def git(self, *args):
        result = subprocess.run(["git", *args], cwd=self.repo, check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode().strip()

    def write(self, name, data):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data.encode() if isinstance(data, str) else data)
        return path

    def commit(self, message="baseline"):
        self.git("add", "--all")
        self.git("commit", "-m", message)
        return self.git("rev-parse", "HEAD")

    def collect(self, mode="worktree", **kwargs):
        return context.collect_changes(self.repo, mode, **kwargs)

    def test_initial_repository_and_nonignored_untracked_scope(self):
        self.write(".gitignore", "ignored.txt\n")
        self.write("ignored.txt", "do not inspect\n")
        self.write(".env", "SECRET=value\n")
        self.write(".codeshield-ignore", ".env\n")
        result, lines = self.collect()
        self.assertIsNone(result["head"])
        self.assertIn(".env", {file["path"] for file in result["files"]})
        self.assertNotIn("ignored.txt", {file["path"] for file in result["files"]})
        self.assertIn({"path": ".env", "line": 1, "text": "SECRET=value"}, lines)
        staged, staged_lines = self.collect("staged")
        self.assertEqual(staged["change_count"], 0)
        self.assertEqual(staged_lines, [])
        self.git("add", "--", ".env")
        staged, _ = self.collect("staged")
        self.assertEqual(staged["files"][0]["path"], ".env")

    def test_staged_scope_excludes_unstaged_and_untracked_content(self):
        self.write("code.py", "old\n")
        self.commit()
        self.write("code.py", "staged\n")
        self.git("add", "--", "code.py")
        self.write("code.py", "unstaged\n")
        self.write("new.py", "untracked\n")
        staged, lines = self.collect("staged")
        self.assertEqual(lines, [{"path": "code.py", "line": 1, "text": "staged"}])
        final, lines = self.collect()
        self.assertEqual({line["text"] for line in lines}, {"unstaged", "untracked"})
        self.assertNotEqual(staged["fingerprint"], final["fingerprint"])
        self.write("code.py", "changed again\n")
        self.assertEqual(staged["fingerprint"], self.collect("staged")[0]["fingerprint"])

    def test_branch_uses_merge_base_while_range_uses_exact_base(self):
        self.write("common", "common\n")
        ancestor = self.commit()
        self.git("checkout", "-b", "feature")
        self.write("feature", "feature change\n")
        feature = self.commit("feature")
        self.git("checkout", "main")
        self.write("main", "main change\n")
        base = self.commit("main")
        branch, _ = self.collect("branch", base="main", head="feature")
        exact, _ = self.collect("range", base="main", head="feature")
        self.assertEqual(branch["comparison_base"], ancestor)
        self.assertEqual(branch["base"], base)
        self.assertEqual(branch["head"], feature)
        self.assertEqual({file["path"] for file in branch["files"]}, {"feature"})
        self.assertEqual({file["path"] for file in exact["files"]}, {"feature", "main"})
        self.assertEqual(exact["comparison_base"], base)
        self.assertEqual(self.git("branch", "--show-current"), "main")

    def test_rename_deletion_and_arbitrary_path_names(self):
        old = "old name é.txt"
        new = "new\nname é.txt"
        self.write(old, "kept\n")
        self.write("delete", "remove\n")
        self.commit()
        self.git("mv", "--", old, new)
        (self.repo / "delete").unlink()
        self.write("+++ literal", "+++ actual content\n")
        result, lines = self.collect()
        files = {file["path"]: file for file in result["files"]}
        self.assertEqual(files[new]["status"], "R")
        self.assertEqual(files[new]["old_path"], old)
        self.assertEqual(files["delete"]["status"], "D")
        self.assertEqual(files["delete"]["added_ranges"], [])
        self.assertEqual(lines, [{"path": "+++ literal", "line": 1, "text": "+++ actual content"}])
        json.dumps(result)

    def test_binary_oversized_symlink_and_gitlink_limits(self):
        self.write("binary", b"a\0b")
        self.write("large", b"a" * (context.MAX_FILE_BYTES + 1))
        outside = self.repo.parent / (self.repo.name + "-target")
        outside.write_text("must not scan this payload")
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        os.symlink(outside, self.repo / "link")
        result, lines = self.collect()
        files = {file["path"]: file for file in result["files"]}
        self.assertTrue(files["binary"]["binary"])
        self.assertFalse(files["large"]["binary"])
        self.assertEqual(lines, [])
        self.assertTrue(any("symlink" in limit for limit in result["limitations"]))
        self.assertTrue(any("exceeds" in limit for limit in result["limitations"]))
        self.assertEqual(len(files["large"]["content_sha256"]), 64)
        self.commit()
        commit = self.git("rev-parse", "HEAD")
        self.git("update-index", "--add", "--cacheinfo", "160000," + commit + ",submodule")
        staged, lines = self.collect("staged")
        self.assertEqual(staged["files"][0]["path"], "submodule")
        self.assertEqual(lines, [])
        self.assertTrue(any("gitlink" in limit for limit in staged["limitations"]))

    def test_fingerprint_changes_with_content_index_untracked_and_mode(self):
        path = self.write("tracked", "one\n")
        self.commit()
        self.write("tracked", "two\n")
        first = self.collect()[0]["fingerprint"]
        self.assertEqual(first, self.collect()[0]["fingerprint"])
        self.write("tracked", "three\n")
        second = self.collect()[0]["fingerprint"]
        self.assertNotEqual(first, second)
        self.git("add", "--", "tracked")
        staged_before = self.collect("staged")[0]["fingerprint"]
        self.write("tracked", "four\n")
        self.git("add", "--", "tracked")
        self.assertNotEqual(staged_before, self.collect("staged")[0]["fingerprint"])
        third = self.collect()[0]["fingerprint"]
        self.write("untracked", "new\n")
        fourth = self.collect()[0]["fingerprint"]
        self.assertNotEqual(third, fourth)
        path.chmod(0o755)
        self.assertNotEqual(fourth, self.collect()[0]["fingerprint"])

    def test_deletion_only_hunk_has_no_added_lines(self):
        self.write("code", "keep\ndelete\nlast\n")
        self.commit()
        self.write("code", "keep\nlast\n")
        result, lines = self.collect()
        self.assertEqual(result["change_count"], 1)
        self.assertEqual(lines, [])
        self.assertEqual(result["files"][0]["added_ranges"], [])

    def test_binary_to_text_transition_still_scans_all_current_text(self):
        self.write("code", b"binary\0data")
        self.commit()
        self.write("code", "secret added as text\n")
        result, lines = self.collect()
        self.assertEqual(lines, [{"path": "code", "line": 1, "text": "secret added as text"}])
        self.assertTrue(result["limitations"])

    def test_worktree_fingerprint_includes_index_even_when_final_bytes_match(self):
        self.write("code", "old\n")
        self.commit()
        self.write("code", "final\n")
        first = self.collect()[0]["fingerprint"]
        self.git("add", "--", "code")
        self.assertNotEqual(first, self.collect()[0]["fingerprint"])

    def test_intent_to_add_is_worktree_only_until_staged(self):
        self.write("baseline", "old\n")
        self.commit()
        self.write("intent", "not yet staged\n")
        self.git("add", "-N", "--", "intent")
        staged, lines = self.collect("staged")
        self.assertEqual(staged["change_count"], 0)
        self.assertEqual(lines, [])
        worktree, lines = self.collect()
        self.assertEqual(worktree["files"][0]["path"], "intent")
        self.assertEqual(lines, [{"path": "intent", "line": 1, "text": "not yet staged"}])
        self.git("add", "--", "intent")
        self.assertEqual(self.collect("staged")[0]["change_count"], 1)

    def test_line_numbers_count_lf_instead_of_unicode_separators(self):
        self.write("code", "first\u2028part\rlone\nsecond\n")
        self.commit()
        self.write("code", "first\u2028part\rlone\nchanged\n")
        result, lines = self.collect()
        self.assertEqual(result["files"][0]["added_ranges"], [[2, 2]])
        self.assertEqual(lines, [{"path": "code", "line": 2, "text": "changed"}])

    def test_conflicts_fail_closed(self):
        self.write("code", "base\n")
        self.commit()
        self.git("checkout", "-b", "other")
        self.write("code", "other\n")
        self.commit("other")
        self.git("checkout", "main")
        self.write("code", "main\n")
        self.commit("main")
        subprocess.run(["git", "merge", "other"], cwd=self.repo,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for mode in ("worktree", "staged"):
            with self.assertRaisesRegex(context.ContextError, "conflicts"):
                self.collect(mode)

    def test_cli_outputs_metadata_only_and_redacts_git_errors(self):
        self.write("file", "VERY_PRIVATE_PAYLOAD\n")
        result = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(self.repo)],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(b"VERY_PRIVATE_PAYLOAD", result.stdout)
        self.assertEqual(json.loads(result.stdout)["change_count"], 1)
        bad = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(self.repo),
                              "--mode", "range", "--base=--output=PRIVATE_TOKEN"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(bad.returncode, 2)
        self.assertEqual(bad.stdout, b"")
        self.assertNotIn(b"PRIVATE_TOKEN", bad.stderr)
        invalid = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(self.repo),
                                  "--mode", "PRIVATE_TOKEN"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(invalid.returncode, 2)
        self.assertEqual(invalid.stdout, b"")
        self.assertNotIn(b"PRIVATE_TOKEN", invalid.stderr)

    def test_external_diff_is_not_executed_and_repo_is_not_written(self):
        self.write("file", "old\n")
        self.commit()
        self.write("file", "new\n")
        marker = self.repo / "external-ran"
        self.git("config", "diff.external", "touch " + str(marker))
        before = self.git("status", "--porcelain=v1", "--untracked-files=all")
        self.collect()
        self.assertFalse(marker.exists())
        self.assertEqual(before, self.git("status", "--porcelain=v1", "--untracked-files=all"))


if __name__ == "__main__":
    unittest.main()
