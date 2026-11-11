"""Exercise local source preparation through the installed CLI contract."""

from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import yaml

from ai_sdlc_workbench.cli import main
from ai_sdlc_workbench.workspace import initialize_workspace


class SourcePreparationCLITests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="source-preparation-cli-")
        self.addCleanup(temporary.cleanup)
        self.root = (Path(temporary.name) / "workspace").resolve()
        initialize_workspace(self.root)
        self.collection = "source-export"
        self.incoming = self.root / "raw/incoming"
        self.incoming.mkdir(parents=True)
        self.page = self.incoming / "page.md"
        self.page.write_text("# Access\nUsers require an entitlement.\nDenied users see a message.\n", encoding="utf-8")
        (self.root / "registry/sources.yaml").write_text(yaml.safe_dump({
            "schema_version": 1,
            "sources": [{"id": self.collection, "type": "filesystem", "purpose": "context",
                         "location": "raw/incoming", "read_only": True}],
        }, sort_keys=False), encoding="utf-8")
        self.index_path = self.root / f"evidence/knowledge/selections/{self.collection}.json"
        self.manifest_path = self.root / "evidence/knowledge/manifest.yaml"
        self.policy = self.root / ".agents/skills/ingest-knowledge/assets/source-filter.yaml"

    @staticmethod
    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def invoke(self, *arguments):
        output = io.StringIO()
        with redirect_stdout(output):
            code = main(["--workspace", str(self.root), "sources", *arguments,
                         "--source", self.collection])
        return code, json.loads(output.getvalue())

    def refresh(self):
        code, result = self.invoke("refresh", "--input", "raw/incoming")
        self.assertEqual(code, 0, result)
        return result

    def index(self):
        return json.loads(self.index_path.read_text(encoding="utf-8"))

    def select(self, decision="KEEP", ranges=None):
        selection = {"path": "page.md", "sha256": self.digest(self.page), "decision": decision,
                     "reason": "Fixture selection for intended access behavior.",
                     "topic": "Security behavior", "intent_status": "documented intent", "context": []}
        if ranges is not None:
            selection["ranges"] = ranges
        decisions = self.root / ".workbench/decisions.json"
        decisions.parent.mkdir(parents=True, exist_ok=True)
        decisions.write_text(json.dumps({"schema_version": 1, "source_id": self.collection,
                                        "decisions": [selection]}), encoding="utf-8")
        code, result = self.invoke("select", "--decisions", ".workbench/decisions.json")
        self.assertEqual(code, 0, result)
        return result

    def test_generated_workspace_review_lifecycle_and_idempotent_refresh(self):
        """Given a complete export, when reviewed, then verification passes without runtime copies."""
        self.assertTrue(self.policy.is_file(), "The default filter policy must ship in generated workspaces.")
        self.assertFalse((self.root / "core/cli.py").exists())
        self.refresh()
        code, result = self.invoke("verify")
        self.assertEqual(code, 1, result)
        self.assertEqual(result["status"], "NEEDS_REVIEW")
        self.assertEqual(self.index()["sources"][0]["decision"], "NEEDS_REVIEW")
        source_hash = self.digest(self.page)
        self.select()
        code, result = self.invoke("verify")
        self.assertEqual(code, 0, result)
        self.assertEqual(result["status"], "READY")
        registered = self.manifest_path.read_bytes()
        index_before = self.index()
        self.refresh()
        self.assertEqual(self.manifest_path.read_bytes(), registered)
        self.assertEqual(self.index()["sources"][0]["decision"], "KEEP")
        self.assertEqual(self.index()["sources"][0]["source"], index_before["sources"][0]["source"])
        self.assertEqual(self.digest(self.page), source_hash)

    def test_changed_excluded_page_requires_review_and_preserves_previous_snapshot(self):
        """Given an excluded page, when its text changes, then the CLI requires a new review."""
        self.refresh()
        self.select("EXCLUDE")
        old_source = self.index()["sources"][0]["source"]
        snapshot = self.root / old_source["snapshot"]
        old_bytes = snapshot.read_bytes()
        self.page.write_text("# Access\nNew users require a second approval.\n", encoding="utf-8")
        code, result = self.invoke("verify")
        self.assertEqual(code, 1, result)
        self.assertNotEqual(result["status"], "READY")
        self.refresh()
        current = self.index()["sources"][0]
        self.assertEqual(current["decision"], "NEEDS_REVIEW")
        self.assertNotEqual(current["source"]["sha256"], old_source["sha256"])
        self.assertEqual(snapshot.read_bytes(), old_bytes)
        self.assertEqual(self.digest(snapshot), old_source["sha256"])
        manifest = yaml.safe_load(self.manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["sources"]), 2)
        self.assertEqual(manifest["sources"][0]["sha256"], old_source["sha256"])

    def test_policy_changes_invalidate_review_without_changing_raw_page(self):
        """Given a reviewed page, when filter rules change, then readiness requires reassessment."""
        self.refresh()
        self.select()
        raw_hash = self.digest(self.page)
        policy = yaml.safe_load(self.policy.read_text(encoding="utf-8"))
        policy["version"] += 1
        self.policy.write_text(yaml.safe_dump(policy, sort_keys=False), encoding="utf-8")
        code, result = self.invoke("verify")
        self.assertEqual(code, 1, result)
        self.assertNotEqual(result["status"], "READY")
        self.refresh()
        self.assertEqual(self.index()["sources"][0]["decision"], "NEEDS_REVIEW")
        self.assertEqual(self.digest(self.page), raw_hash)

    def test_view_rejects_existing_output_without_overwriting_user_file(self):
        """Given an existing output folder, when view runs, then its content remains unchanged."""
        self.refresh()
        self.select()
        output = self.root / ".workbench/filtered/current"
        output.mkdir(parents=True)
        marker = output / "user.txt"
        marker.write_text("Preserve this content.\n", encoding="utf-8")
        code, result = self.invoke("view", "--output", ".workbench/filtered/current")
        self.assertEqual(code, 1, result)
        self.assertEqual(marker.read_text(encoding="utf-8"), "Preserve this content.\n")
        self.assertEqual(sorted(path.name for path in output.iterdir()), ["user.txt"])

    def test_views_bind_whole_page_links_and_partial_excerpts_to_source_hash(self):
        """Given reviewed ranges, when views render, then output hashes and mappings match the source."""
        self.refresh()
        self.select()
        source = self.index()["sources"][0]["source"]
        code, result = self.invoke("view", "--output", ".workbench/filtered/whole")
        self.assertEqual(code, 0, result)
        whole = self.root / ".workbench/filtered/whole"
        manifest = json.loads((whole / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["sources"]), 1)
        entry = manifest["sources"][0]
        rendered = whole / entry["output"]
        self.assertEqual(entry["source"], source)
        self.assertEqual(entry["source_sha256"], self.digest(self.page))
        self.assertEqual(entry["output_sha256"], self.digest(rendered))
        self.assertEqual(rendered.read_bytes(), self.page.read_bytes())
        if entry["kind"] == "symlink":
            self.assertTrue(rendered.is_symlink())
            self.assertEqual(rendered.resolve(), (self.root / source["snapshot"]).resolve())

        self.select("KEEP_SECTIONS", [[2, 2]])
        code, result = self.invoke("view", "--output", ".workbench/filtered/selected")
        self.assertEqual(code, 0, result)
        selected = self.root / ".workbench/filtered/selected"
        manifest = json.loads((selected / "manifest.json").read_text(encoding="utf-8"))
        entry = manifest["sources"][0]
        rendered = selected / entry["output"]
        self.assertEqual(entry["kind"], "excerpt")
        self.assertEqual(rendered.read_text(encoding="utf-8"), "Users require an entitlement.\n")
        self.assertEqual(entry["source_sha256"], source["sha256"])
        self.assertEqual(entry["output_sha256"], self.digest(rendered))
        self.assertEqual(entry["mapping"], [{"source_start": 2, "source_end": 2,
                                             "output_start": 1, "output_end": 1}])
        self.assertEqual(self.digest(self.root / source["snapshot"]), source["sha256"])


if __name__ == "__main__":
    unittest.main()
