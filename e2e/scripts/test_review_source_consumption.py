"""Check evidence boundaries for selective source-drift reruns."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("review-source-consumption.mjs").resolve()


@unittest.skipUnless(shutil.which("node"), "Node is required for TypeScript import analysis.")
class SourceConsumptionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.root = self.workspace / "audit"
        self.run = self.root / "application" / "run-001"
        self.sources = {
            "e2e/audit-specs/case.spec.ts": "import {value} from '../support/helper.js';\n"
            "import type {Shape} from '../support/types.js';\nvoid value;\n",
            "e2e/support/helper.ts": "export {value} from './transitive.js';\n",
            "e2e/support/transitive.ts": "export const value = 'retained';\n",
            "e2e/support/types.ts": "export type Shape = {old: string};\n",
            "e2e/audit-specs/unrelated.spec.ts": "export const unused = 'retained';\n",
            "e2e/audit.config.ts": "export default {};\n",
            "e2e/audit.reporter.ts": "export default class Reporter {}\n",
        }
        records = []
        for name, text in self.sources.items():
            current = self.workspace / name
            current.parent.mkdir(parents=True, exist_ok=True)
            current.write_text(text)
            snapshot = self.run / "source-snapshots" / name
            snapshot.parent.mkdir(parents=True, exist_ok=True)
            snapshot.write_text(text)
            records.append({"path": name, "sha256": self.hash(current), "snapshotPath": str(snapshot)})
        self.save(self.run / "run-inputs.json", {"sourceHashes": records})
        self.save(self.run / "run-result.json", {"status": "completed"})
        self.save(self.run / "cases" / "attempt-1" / "result.json", {
            "canonicalIdsMentioned": ["CASE-001"], "endedAt": "2026-10-22T01:00:00Z",
            "source": {"file": str(self.workspace / "e2e/audit-specs/case.spec.ts")}, "actualStatus": "passed"})
        catalog = self.workspace / "test-cases.md"
        catalog.write_text("Frozen canonical case\n")
        inventory = self.root / "inventory"
        self.save(inventory / "cases.jsonl", {"caseId": "CASE-001"}, jsonl=True)
        self.save(inventory / "summary.json", {
            "caseRecords": {"path": str(inventory / "cases.jsonl"), "sha256": self.hash(inventory / "cases.jsonl")},
            "inputs": [{"path": str(catalog), "sha256": self.hash(catalog)}]})
        self.exclusions = self.workspace / "scope.json"
        self.save(self.exclusions, {"catalogSha256": self.hash(catalog), "cases": []})

    @staticmethod
    def hash(file):
        return hashlib.sha256(file.read_bytes()).hexdigest()

    @staticmethod
    def save(file, value, jsonl=False):
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(json.dumps(value, indent=None if jsonl else 2) + "\n")

    def review(self):
        result = subprocess.run(["node", str(SCRIPT), "--workspace", str(self.workspace),
                                 "--audit-root", str(self.root), "--scope-exclusions", str(self.exclusions)],
                                capture_output=True, text=True, check=True)
        return json.loads(result.stdout)

    def test_type_only_and_unrelated_changes_do_not_trigger_runtime_reruns(self):
        (self.workspace / "e2e/support/types.ts").write_text("export type Shape = {new: number};\n")
        (self.workspace / "e2e/audit-specs/unrelated.spec.ts").write_text("throw new Error('unconsumed');\n")
        result = self.review()
        case = result["cases"][0]
        self.assertEqual(case["status"], "CONSUMED_IMPORT_BYTES_MATCH")
        self.assertEqual(case["consumedSourceDrift"], [])
        self.assertEqual({item["path"] for item in case["unconsumedSourceDrift"]},
                         {"e2e/support/types.ts", "e2e/audit-specs/unrelated.spec.ts"})
        graph = result["importClosures"][case["graphKey"]]["current"]
        self.assertTrue(any(item["specifier"] == "../support/types.js" for item in graph["typeOnlyImports"]))
        self.assertNotIn("e2e/support/types.ts", {node["path"] for node in graph["nodes"]})

    def test_transitive_reexport_change_requires_changed_symbol_review(self):
        changed = self.workspace / "e2e/support/transitive.ts"
        changed.write_text("export const value = 'changed predicate';\n")
        before = self.hash(self.run / "cases" / "attempt-1" / "result.json")
        result = self.review()
        case = result["cases"][0]
        self.assertEqual(case["status"], "CONSUMED_IMPORT_BYTES_CHANGED")
        self.assertEqual([item["path"] for item in case["consumedSourceDrift"]], ["e2e/support/transitive.ts"])
        self.assertEqual(case["rerunDecision"], "REVIEW_CHANGED_SYMBOLS_BEFORE_SCHEDULING")
        self.assertEqual(self.hash(self.run / "cases" / "attempt-1" / "result.json"), before)
        graph = result["importClosures"][case["graphKey"]]["snapshot"]
        self.assertEqual(graph["errors"], [])
        self.assertTrue(any(edge["from"] == "e2e/support/helper.ts" and edge["to"] == "e2e/support/transitive.ts"
                            for edge in graph["edges"]))


if __name__ == "__main__":
    unittest.main()
