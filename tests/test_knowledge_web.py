"""Focused checks for the local knowledge preview POC."""

import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from ai_sdlc_workbench.knowledge_web.server import KnowledgeCatalog, _PreviewServer


class KnowledgeWebTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="knowledge-preview-")
        self.root = Path(self.temporary.name)
        (self.root / "knowledge/records/candidates/settlement").mkdir(parents=True)
        (self.root / "knowledge/evidence").mkdir(parents=True)
        (self.root / "knowledge/llm-wiki/wiki/summaries").mkdir(parents=True)
        (self.root / "docs").mkdir()
        (self.root / "tasks/demo/evidence").mkdir(parents=True)
        (self.root / "knowledge/evidence/manifest.yaml").write_text("schema_version: 1\nsources: []\n", encoding="utf-8")
        (self.root / "knowledge/records/candidates/index.md").write_text(
            "---\n{\"type\": \"KnowledgeTopic\", \"id\": \"KT-demo\", \"status\": \"draft\"}\n---\n# Candidate index\n\nDraft navigation.\n",
            encoding="utf-8")
        (self.root / "knowledge/llm-wiki/wiki/summaries/demo.md").write_text(
            "---\ntype: Summary\ndescription: Derived page\n---\n# Demo summary\n\nSee [[summaries/demo]].\n",
            encoding="utf-8")
        (self.root / "docs/README.md").write_text("# Current docs\n\nThe preview works.\n", encoding="utf-8")
        (self.root / "tasks/demo/evidence/run.md").write_text("# Retained run\n\nLinked evidence.\n", encoding="utf-8")
        self.catalog = KnowledgeCatalog(self.root)

    def tearDown(self):
        self.temporary.cleanup()

    def test_catalog_keeps_collections_and_json_frontmatter(self):
        health = self.catalog.health()
        self.assertEqual(health["status"], "READY")
        self.assertEqual(health["collections"], {"records": 1, "wiki": 1, "docs": 1, "evidence": 1})
        document = self.catalog.document("records:knowledge/records/candidates/index.md")
        self.assertEqual(document.metadata["type"], "KnowledgeTopic")
        self.assertEqual(document.metadata["status"], "draft")

    def test_catalog_search_returns_bounded_snippet(self):
        results = self.catalog.search("preview", "docs", 1)
        self.assertEqual(len(results), 1)
        self.assertIn("preview", results[0]["snippet"])

    def test_http_preview_is_read_only_and_returns_document(self):
        server = _PreviewServer(("127.0.0.1", 0), self.catalog)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.shutdown)
        self.addCleanup(server.server_close)
        base = f"http://127.0.0.1:{server.server_address[1]}"
        with urlopen(base + "/api/health") as response:
            self.assertEqual(json.loads(response.read())["documents"], 4)
        with urlopen(base + "/api/refresh") as response:
            self.assertEqual(json.loads(response.read())["status"], "READY")
        key = "records:knowledge/records/candidates/index.md"
        with urlopen(base + "/api/document?key=" + key.replace(":", "%3A").replace("/", "%2F")) as response:
            payload = json.loads(response.read())
        self.assertEqual(payload["metadata"]["id"], "KT-demo")
        request = Request(base + "/api/health", method="POST")
        with self.assertRaises(HTTPError) as error:
            urlopen(request)
        self.assertEqual(error.exception.code, 405)

    def test_unknown_document_is_not_a_filesystem_read(self):
        server = _PreviewServer(("127.0.0.1", 0), self.catalog)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.shutdown)
        self.addCleanup(server.server_close)
        base = f"http://127.0.0.1:{server.server_address[1]}"
        with self.assertRaises(HTTPError) as error:
            urlopen(base + "/api/document?key=records%3A..%2F..%2F.env")
        self.assertEqual(error.exception.code, 404)
