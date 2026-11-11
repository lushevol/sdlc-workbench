"""Keep compiled wiki assets outside canonical Workbench knowledge scanners."""

import hashlib
import os
from pathlib import Path
import tempfile
import unittest

import yaml

from ai_sdlc_workbench.governance import validate_knowledge
from ai_sdlc_workbench.governance.schemas import HEADINGS
from ai_sdlc_workbench.ingestion.harness import _governed
from ai_sdlc_workbench.models import Context, Resource
from ai_sdlc_workbench.providers.knowledge import LocalKnowledgeProvider
from ai_sdlc_workbench.relationships.skill import load_graph_tool


class DerivedKnowledgeBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="derived-knowledge-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.source = {"resource": "fixture://policy", "revision": "v1", "sha256": "a" * 64}
        self.write("evidence/knowledge/manifest.yaml", yaml.safe_dump({
            "schema_version": 1, "sources": [{"id": "SRC-policy", **self.source,
                "classification": "business", "ingested_at": "2026-11-11T00:00:00Z"}]}))
        metadata = {
            "type": "KnowledgeTopic", "id": "KT-policy", "version": 1, "owner": "unknown",
            "governance_state": "candidate", "status": "draft", "sources": [self.source],
            "generated": {"by": "agent:fixture", "at": "2026-11-11T00:00:00Z"}, "verified": [],
            "classification": "policy", "scope": "One policy.", "summary": "Review orders.",
            "related": [], "open_questions": [],
        }
        self.content = ("---\n" + yaml.safe_dump(metadata) + "---\n# Order policy\n\n" +
            "\n\n".join("## " + heading + "\n\nReview orders." for heading in HEADINGS["KnowledgeTopic"]))
        self.canonical = self.write("knowledge/candidates/policy.md", self.content)
        self.provider = LocalKnowledgeProvider()
        self.resource = Resource("knowledge", "knowledge", "knowledge.local", "test", {"path": "knowledge"},
                                 ["list", "search", "read", "ingest"])
        self.context = Context(self.root, self.root / "run")

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def derived_workspace(self):
        self.write("knowledge/llm-wiki/wiki/AGENTS.md", "# Native OpenKB instructions\n")
        self.write("knowledge/llm-wiki/wiki/concepts/orders.md", "---\ntype: concept\n---\nDerived orders.\n")
        self.write("knowledge/llm-wiki/wiki/summaries/canonical-shaped.md", self.content)
        self.write("knowledge/llm-wiki/.openkb/config.yaml", "model: fixture/model\n")
        self.write("knowledge/llm-wiki/output/visualize/graph.html", "<html>Graph</html>\n")
        self.write("knowledge/llm-wiki/source-manifest.json", "{}\n")
        link = self.root / "knowledge/llm-wiki/wiki/sources/policy.md"
        link.parent.mkdir(parents=True)
        link.symlink_to(os.path.relpath(self.canonical, link.parent))
        (link.parent / "unavailable.md").symlink_to(self.root.parent / "unavailable-source.md")

    def invoke(self, operation, arguments=None):
        return self.provider.invoke(operation, self.resource, arguments or {}, self.context)

    def test_derived_schema_state_and_source_links_do_not_affect_canonical_validation_or_ingestion(self):
        expected = {"valid": True, "documents": 1, "findings": []}
        self.assertEqual(validate_knowledge(self.root), expected)
        governed = _governed(self.root)
        self.derived_workspace()
        self.assertEqual(validate_knowledge(self.root), expected)
        self.assertEqual(_governed(self.root), governed)
        self.assertEqual(set(governed), {"knowledge/candidates/policy.md"})

    def test_canonical_provider_excludes_derived_pages_and_blocks_read_or_write_through_source_links(self):
        self.derived_workspace()
        before = hashlib.sha256(self.canonical.read_bytes()).hexdigest()
        listing = self.invoke("list")
        self.assertEqual([row["relative_path"] for row in listing["files"]], ["candidates/policy.md"])
        search = self.invoke("search", {"query": "Review orders"})
        self.assertEqual({row["relative_path"] for row in search["matches"]}, {"candidates/policy.md"})
        (self.root / "knowledge/wiki-alias").symlink_to("llm-wiki/wiki/summaries", target_is_directory=True)
        for path in ("llm-wiki/wiki/sources/policy.md", "llm-wiki/wiki/summaries/canonical-shaped.md",
                     "candidates/../llm-wiki/wiki/sources/policy.md", "wiki-alias/canonical-shaped.md"):
            for operation in ("read", "ingest"):
                arguments = {"path": path}
                if operation == "ingest":
                    arguments["content"] = self.content.replace("Review orders.", "Changed intent.")
                with self.subTest(path=path, operation=operation):
                    self.assertEqual(self.invoke(operation, arguments)["code"], "INVALID_DOCUMENT")
        self.assertEqual(hashlib.sha256(self.canonical.read_bytes()).hexdigest(), before)

    def test_reserved_boundary_does_not_exempt_other_canonical_directories(self):
        self.derived_workspace()
        invalid = self.write("knowledge/candidates/llm-wiki/invalid.md", "# Invalid canonical record\n")
        result = validate_knowledge(self.root)
        self.assertFalse(result["valid"])
        self.assertEqual(result["documents"], 2)
        self.assertEqual([(row["path"], row["code"]) for row in result["findings"]],
                         [(invalid.relative_to(self.root).as_posix(), "document_invalid")])

    def test_service_graph_knowledge_projection_ignores_wiki_before_symlink_checks(self):
        projection = load_graph_tool("knowledge_projection")
        build = load_graph_tool("build_graph")
        before = projection.input_fingerprints(self.root)
        self.derived_workspace()
        self.assertEqual(projection.input_fingerprints(self.root), before)
        graph = build.Graph(self.root)
        projection.apply_knowledge(graph)
        records = [node for node in graph.nodes.values() if node["type"] == "KNOWLEDGE_RECORD"]
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["source_paths"], ["knowledge/candidates/policy.md"])
        self.write("knowledge/candidates/invalid.md", "# Invalid canonical record\n")
        with self.assertRaisesRegex(ValueError, "require YAML frontmatter"):
            projection.apply_knowledge(build.Graph(self.root))


if __name__ == "__main__":
    unittest.main()
