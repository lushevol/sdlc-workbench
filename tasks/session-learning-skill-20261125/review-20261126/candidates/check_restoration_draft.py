"""Exercise the candidate against an isolated repository without remote access."""

import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("verify_restored_assets.py")
SPEC = importlib.util.spec_from_file_location("restoration_candidate", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CandidateChecks(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="restoration-learning-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.git("init", "-q")
        self.original = b'<mxfile><diagram id="page" /></mxfile>\n'
        (self.root / "diagram with spaces.drawio").write_bytes(self.original)
        (self.root / "plain.txt").write_text("not XML\n")
        self.git("add", "--", "diagram with spaces.drawio", "plain.txt")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "-qm", "fixture")

    def git(self, *arguments):
        return subprocess.check_output(["git", "-C", str(self.root), *arguments], timeout=30)

    def test_matching_xml_preserves_original_and_index(self):
        before = (self.root / ".git/index").read_bytes()
        result = MODULE.verify(self.root, "HEAD", ["diagram with spaces.drawio"], xml=True)
        self.assertEqual(result["status"], "PASSED")
        self.assertEqual(result["files"][0]["diagram_pages"], 1)
        self.assertEqual((self.root / "diagram with spaces.drawio").read_bytes(), self.original)
        self.assertEqual((self.root / ".git/index").read_bytes(), before)

    def test_mismatch_is_reported_and_not_repaired(self):
        path = self.root / "diagram with spaces.drawio"
        path.write_bytes(b"changed\n")
        result = MODULE.verify(self.root, "HEAD", [path.name])
        self.assertEqual(result["status"], "FAILED")
        self.assertNotEqual(result["files"][0]["historical_sha256"], result["files"][0]["current_sha256"])
        self.assertEqual(path.read_bytes(), b"changed\n")

    def test_missing_file_fails_without_restoration(self):
        path = self.root / "diagram with spaces.drawio"
        path.unlink()
        with self.assertRaises(FileNotFoundError):
            MODULE.verify(self.root, "HEAD", [path.name])
        self.assertFalse(path.exists())

    def test_parent_escape_is_rejected(self):
        with self.assertRaises(ValueError):
            MODULE.verify(self.root, "HEAD", ["../outside.txt"])

    def test_symlink_is_rejected(self):
        (self.root / "linked.drawio").symlink_to("diagram with spaces.drawio")
        with self.assertRaises(ValueError):
            MODULE.verify(self.root, "HEAD", ["linked.drawio"])

    def test_invalid_xml_fails(self):
        with self.assertRaises(MODULE.ET.ParseError):
            MODULE.verify(self.root, "HEAD", ["plain.txt"], xml=True)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CandidateChecks)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({"tests": result.testsRun, "failed": len(result.failures),
                      "errors": len(result.errors), "skipped": len(result.skipped)}))
    raise SystemExit(0 if result.wasSuccessful() else 1)
