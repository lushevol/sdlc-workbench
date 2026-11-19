"""Knowledge reader boundaries, native links, and existing graph integration."""

import hashlib
import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from ai_sdlc_workbench.knowledge_web.server import KnowledgeCatalog, _PreviewServer


class KnowledgeWebTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="knowledge-preview-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.write("knowledge/evidence/manifest.yaml", "schema_version: 1\nsources: []\n")
        self.write("knowledge/records/candidates/index.md", "# Candidate index\n\n[Demo](settlement/demo.md).\n")
        self.write("knowledge/records/candidates/settlement/demo.md",
                   '---\n{"type": "KnowledgeTopic", "id": "KT-demo", "status": "draft"}\n---\n'
                   "# Demo record\n\nCanonical candidate.\n")
        self.write("knowledge/llm-wiki/wiki/index.md", "# Wiki index\n\n[[summaries/demo]].\n")
        self.write("knowledge/llm-wiki/wiki/summaries/demo.md",
                   "---\ntype: Summary\nfull_text: sources/demo.md\n---\n# Demo summary\n\nDerived preview page.\n")
        self.write("knowledge/README.md", "# Knowledge guide\n")
        self.write("knowledge/index.md", "# Knowledge index\n")
        self.write("knowledge/evidence/sources/collection/source.md", "# Retained source\n\nSource preview.\n")
        self.write("knowledge/evidence/selections/selection.json", '{"decision":"selected"}\n')
        self.write("knowledge/evidence/findings/open.md", "# Open finding\n")
        self.write("docs/README.md", "# Out of scope docs\n\nOutside-only marker.\n")
        self.write("tasks/demo/evidence/run.md", "# Linked task snapshot\n\nOutside-only marker.\n")
        self.write("knowledge/evidence/audit/event.yaml", "audit-only-marker: true\n")
        self.write("knowledge/evidence/processing/receipt.json", '{"processing-only-marker":true}\n')
        self.write("knowledge/evidence/incoming/import.md", "# Incoming-only marker\n")
        self.write("knowledge/llm-wiki/.openkb/config.yaml", "private-only-marker: true\n")
        self.write("knowledge/llm-wiki/wiki/log.md", "# Audit-only-marker\n")
        self.write("knowledge/llm-wiki/wiki/AGENTS.md", "# Private instructions\n")
        self.catalog = KnowledgeCatalog(self.root)

    def write(self, path, content):
        destination = self.root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        return destination

    def server(self):
        server = _PreviewServer(("127.0.0.1", 0), self.catalog)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        def close():
            server.shutdown()
            server.server_close()
            thread.join()

        self.addCleanup(close)
        return f"http://127.0.0.1:{server.server_address[1]}"

    def test_catalog_preserves_layers_and_json_frontmatter(self):
        self.assertEqual(self.catalog.health()["collections"], {"records": 2, "wiki": 2, "guide": 2, "evidence": 4})
        document = self.catalog.document("records:knowledge/records/candidates/settlement/demo.md")
        self.assertEqual(document.metadata["type"], "KnowledgeTopic")
        self.assertEqual(document.metadata["status"], "draft")
        paths = [item["path"] for group in self.catalog.navigation()["collections"] for item in group["documents"]]
        self.assertTrue(all(path.startswith("knowledge/") for path in paths))
        for marker in ("outside-only-marker", "audit-only-marker", "processing-only-marker", "incoming-only-marker", "private-only-marker"):
            self.assertEqual(self.catalog.search(marker, None, 100), [])

    def test_manifest_link_does_not_expose_task_snapshots(self):
        self.write("knowledge/evidence/manifest.yaml", "sources:\n  - snapshot: tasks/demo/evidence/run.md\n")
        self.catalog.refresh()
        with self.assertRaises(KeyError):
            self.catalog.document("evidence:tasks/demo/evidence/run.md")
        with self.assertRaises(KeyError):
            self.catalog.resolve("guide:knowledge/README.md", "../tasks/demo/evidence/run.md")

    def test_search_filters_and_limits_source_snippets(self):
        results = self.catalog.search("preview", "evidence", 1)
        self.assertEqual(len(results), 1)
        self.assertIn("preview", results[0]["snippet"])
        self.assertEqual(results[0]["collection"], "evidence")

    def test_native_relative_wiki_links_and_fragments(self):
        key = "records:knowledge/records/candidates/index.md"
        self.assertEqual(self.catalog.resolve(key, "settlement/demo.md#L3-L6"),
                         {"key": "records:knowledge/records/candidates/settlement/demo.md", "fragment": "L3-L6"})
        wiki_key = "wiki:knowledge/llm-wiki/wiki/index.md"
        for target in ("wiki:summaries/demo", "summaries/demo.md", "wiki:demo"):
            self.assertEqual(self.catalog.resolve(wiki_key, target)["key"], "wiki:knowledge/llm-wiki/wiki/summaries/demo.md")
        self.assertEqual(self.catalog.resolve(key, "#candidate-index"), {"key": key, "fragment": "candidate-index"})
        for target in ("../../../../.env", "https://example.com/knowledge/index.md", "//example.com/x", "../../../evidence/audit/event.yaml"):
            with self.assertRaises(KeyError, msg=target):
                self.catalog.resolve(key, target)

    def test_source_alias_requires_manifest_and_exact_canonical_symlink(self):
        origin = "knowledge/records/candidates/settlement/demo.md"
        self.write("knowledge/llm-wiki/source-manifest.json", json.dumps({"sources": [{"doc_name": "demo", "origin": origin}]}))
        for folder in ("raw", "wiki/sources"):
            alias = self.root / "knowledge/llm-wiki" / folder / "demo.md"
            alias.parent.mkdir(parents=True, exist_ok=True)
            alias.symlink_to(self.root / origin)
        self.catalog.refresh()
        key = "wiki:knowledge/llm-wiki/wiki/summaries/demo.md"
        for target in ("sources/demo.md", "../../raw/demo.md", "../sources/demo.md"):
            self.assertEqual(self.catalog.resolve(key, target)["key"], "records:" + origin)
        alias = self.root / "knowledge/llm-wiki/wiki/sources/demo.md"
        alias.unlink()
        alias.symlink_to(self.root / "docs/README.md")
        self.catalog.refresh()
        with self.assertRaises(KeyError):
            self.catalog.resolve(key, "sources/demo.md")
        self.write("knowledge/llm-wiki/source-manifest.json", '{"sources":[{"origin":{},"doc_name":"demo"}]}')
        self.catalog.refresh()
        with self.assertRaises(KeyError):
            self.catalog.resolve(key, "../../raw/demo.md")

    def test_symlink_directory_cannot_expand_scope(self):
        (self.root / "knowledge/records/candidates/leaked").symlink_to(self.root / "docs", target_is_directory=True)
        source_root = self.root / "knowledge/evidence/sources"
        for path in source_root.rglob("*"):
            if path.is_file():
                path.unlink()
        (source_root / "collection").rmdir()
        source_root.rmdir()
        source_root.symlink_to(self.root / "docs", target_is_directory=True)
        self.catalog.refresh()
        self.assertEqual(self.catalog.search("outside-only-marker", None, 100), [])
        paths = [item["path"] for group in self.catalog.navigation()["collections"] for item in group["documents"]]
        self.assertFalse(any("leaked" in path for path in paths))

    def test_refresh_discovers_new_and_removed_pages(self):
        path = self.write("knowledge/llm-wiki/wiki/concepts/added.md", "# Newly added\n")
        self.catalog.refresh()
        self.assertEqual(len(self.catalog.search("Newly added", "wiki", 10)), 1)
        path.unlink()
        self.catalog.refresh()
        self.assertEqual(self.catalog.search("Newly added", "wiki", 10), [])

    def test_graph_reuses_exact_bytes_and_isolates_scripts(self):
        base = self.server()
        self.assertFalse(self.catalog.graph()["available"])
        with self.assertRaises(HTTPError) as error:
            urlopen(base + "/wiki-graph")
        self.assertEqual(error.exception.code, 404)
        error.exception.close()
        payload = "<!doctype html><html><script>window.graphLoaded=true</script><p>Original graph</p></html>"
        graph = self.write("knowledge/llm-wiki/output/visualize/graph.html", payload)
        with urlopen(base + "/api/graph") as response:
            metadata = json.loads(response.read())
        self.assertTrue(metadata["available"])
        self.assertEqual(metadata["sha256"], hashlib.sha256(graph.read_bytes()).hexdigest())
        with urlopen(base + metadata["url"]) as response:
            self.assertEqual(response.read(), graph.read_bytes())
            policy = response.headers["Content-Security-Policy"]
        self.assertIn("frame-ancestors 'self'", policy)
        self.assertIn("sandbox allow-scripts", policy)
        self.assertIn("script-src 'unsafe-inline'", policy)
        self.assertNotIn("allow-same-origin", policy)
        self.assertNotIn("https:", policy)
        graph.unlink()
        graph.symlink_to(self.root / "docs/README.md")
        self.assertFalse(self.catalog.graph()["available"])

    def test_http_routes_remain_read_only_and_do_not_create_audit_files(self):
        before = sorted(path.relative_to(self.root).as_posix() for path in self.root.rglob("*") if path.is_file())
        base = self.server()
        with urlopen(base + "/api/health") as response:
            self.assertEqual(json.loads(response.read())["documents"], 10)
        with urlopen(base + "/api/refresh") as response:
            self.assertEqual(json.loads(response.read())["status"], "READY")
        key = "records:knowledge/records/candidates/settlement/demo.md"
        with urlopen(base + "/api/document?" + urlencode({"key": key})) as response:
            self.assertEqual(json.loads(response.read())["metadata"]["id"], "KT-demo")
        with urlopen(base + "/api/resolve?" + urlencode({"from": key, "target": "../index.md#candidate-index"})) as response:
            self.assertEqual(json.loads(response.read())["fragment"], "candidate-index")
        for method in ("POST", "PUT", "DELETE"):
            with self.assertRaises(HTTPError) as error:
                urlopen(Request(base + "/api/health", method=method))
            self.assertEqual(error.exception.code, 405)
            error.exception.close()
        after = sorted(path.relative_to(self.root).as_posix() for path in self.root.rglob("*") if path.is_file())
        self.assertEqual(after, before)

    def test_unknown_keys_unsafe_assets_and_foreign_host_are_rejected(self):
        base = self.server()
        for path in ("/api/document?key=../../.env", "/assets/../server.py", "/knowledge/evidence/audit/event.yaml"):
            with self.assertRaises(HTTPError) as error:
                urlopen(base + path)
            self.assertEqual(error.exception.code, 404)
            error.exception.close()
        for host in ("untrusted.example", "[invalid"):
            with self.assertRaises(HTTPError) as error:
                urlopen(Request(base + "/api/health", headers={"Host": host}))
            self.assertEqual(error.exception.code, 403)
            error.exception.close()
