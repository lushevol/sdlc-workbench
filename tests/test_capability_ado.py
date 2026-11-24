"""Exercise exact ADO read selection and minimized learning evidence offline."""

import hashlib
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from ai_sdlc_workbench.capability_ado import artifact_scope, resolve_artifact, verify_artifact_rule
from ai_sdlc_workbench.models import Resource, WorkbenchError
from ai_sdlc_workbench.providers.connectors import ConnectorMcpProvider


FIXTURES = Path(__file__).with_name("fixtures") / "capability_learning"
ENDPOINT = "https://azure.example.test/collection"
BEARER = "fixture-secret-not-retained"
ARGUMENTS = {"resource_id": "external-ado", "project": "project-id", "repository_id": "repository-id",
             "pipeline_id": 27, "source_ref": "refs/heads/develop"}


def _resource(grants=("report_builds", "report_build_artifacts")):
    return Resource("external-ado", "connector", "connector.mcp", "external",
                    {"connector": "ado", "allowed_tools": list(grants),
                     "command": ["node", "core/connectors/workbench/bridge.js"]}, ["list", "call"])


class AdoCapabilityTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        self.workbench = SimpleNamespace(root=self.root, config={"timeout_seconds": 5},
                                         resources={"external-ado": _resource()})
        environment = patch.dict(os.environ, {"AZURE_DEVOPS_ORG_URL": ENDPOINT,
                                             "AZURE_DEVOPS_PAT": BEARER}, clear=True)
        environment.start()
        self.addCleanup(environment.stop)
        self.requests = []
        self.overrides = {}
        self.artifacts = [{"id": 2001, "name": "application-package",
                           "resource": {"downloadUrl": f"https://unsigned.example.test/?sig={BEARER}"}},
                          {"id": 2002, "name": BEARER}]
        provider = patch.object(ConnectorMcpProvider, "invoke", side_effect=self._reply)
        provider.start()
        self.addCleanup(provider.stop)

    def _reply(self, operation, resource, request, context):
        self.requests.append((operation, resource.id, request))
        tool = request["tool"]
        arguments = request["arguments"]
        if tool == "report_builds":
            build_id = arguments["ids"][0]
            build = {"id": build_id, "status": "completed", "result": "succeeded",
                     "url": ENDPOINT + f"/project-id/_apis/build/builds/{build_id}",
                     "project": {"id": "project-id"}, "repository": {"id": "repository-id"},
                     "definition": {"id": 27}, "sourceBranch": "refs/heads/develop",
                     "sourceVersion": str(build_id) * 40, "requestedFor": {"uniqueName": "private@example.test"}}
            build.update(self.overrides)
            data = {"count": 1, "value": [build]}
        else:
            self.assertEqual(tool, "report_build_artifacts")
            data = self.artifacts
        return {"status": "SUCCEEDED", "result": {"structuredContent": {
            "data": data, "headers": {"authorization": BEARER}}}}

    def resolve(self, build_id=1, **overrides):
        arguments = {**ARGUMENTS, "build_id": build_id, "source_commit": str(build_id) * 40,
                     "artifact_name": "application-package", **overrides}
        return resolve_artifact(self.workbench, **arguments)

    def test_resolves_only_exact_metadata_and_evidence_contains_no_raw_response(self):
        result = self.resolve()
        self.assertEqual((result["status"], result["artifact_id"], result["integrity"]),
                         ("RESOLVED", 2001, "METADATA_ONLY"))
        self.assertEqual(self.requests, [
            ("call", "external-ado", {"tool": "report_builds", "arguments": {"project": "project-id", "ids": [1]}}),
            ("call", "external-ado", {"tool": "report_build_artifacts",
                                      "arguments": {"project": "project-id", "buildId": 1}}),
        ])
        evidence = result["evidence"]
        raw = (self.root / evidence["path"]).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), evidence["sha256"])
        for value in (BEARER, ENDPOINT, "downloadUrl", "private@example.test"):
            self.assertNotIn(value.encode(), raw)
        self.assertEqual(self.resolve()["evidence"], evidence)
        self.assertEqual(len(list((self.root / evidence["path"]).parent.glob("*.json"))), 1)

    def test_rejects_mismatch_without_reading_artifacts(self):
        for field, value in (("sourceBranch", "refs/heads/another"), ("sourceVersion", "f" * 40),
                             ("definition", {"id": 28}), ("id", 2), ("result", "failed"),
                             ("url", "https://elsewhere.example.test/collection"),
                             ("repository", {"id": "other"}), ("project", {"id": "other"})):
            with self.subTest(field=field):
                self.overrides = {field: value}
                self.requests.clear()
                with self.assertRaisesRegex(WorkbenchError, "returned build differs"):
                    self.resolve()
                self.assertEqual([request[2]["tool"] for request in self.requests], ["report_builds"])
        self.assertFalse((self.root / ".workbench").exists())

    def test_ambiguous_name_leaves_no_selection_or_receipt(self):
        self.artifacts.append({"id": 2003, "name": "application-package"})
        with self.assertRaisesRegex(WorkbenchError, "one exact artifact identity"):
            self.resolve()
        choices = self.resolve(artifact_name=None)
        self.assertEqual((choices["status"], choices["available_names"]),
                         ("SELECTION_REQUIRED", ["application-package"]))
        self.assertNotIn("evidence", choices)

    def test_denied_read_or_credential_input_never_dispatches(self):
        with self.assertRaisesRegex(WorkbenchError, "without sensitive data"):
            self.resolve(artifact_name=BEARER)
        self.workbench.resources["external-ado"] = _resource(("report_builds", "pipelines_run_pipeline"))
        with self.assertRaisesRegex(WorkbenchError, "exact artifact read tools must be granted"):
            self.resolve()
        self.assertEqual(self.requests, [])

    def test_capture_off_or_receipt_failure_does_not_interrupt_resolution(self):
        for disabled in ("0", "false", "off"):
            with patch.dict(os.environ, {"WORKBENCH_LEARNING_CAPTURE": disabled}):
                self.assertNotIn("evidence", self.resolve())
        with patch("ai_sdlc_workbench.capability_ado._atomic", side_effect=OSError("test failure")):
            result = self.resolve()
        self.assertEqual((result["status"], result["learning_capture"]), ("RESOLVED", "FAILED"))
        self.assertNotIn("evidence", result)

    def test_scope_change_cannot_reuse_a_name_from_another_organization(self):
        scope = artifact_scope(self.workbench, **ARGUMENTS)
        with patch.dict(os.environ, {"AZURE_DEVOPS_ORG_URL": "https://other.example.test"}):
            with self.assertRaisesRegex(WorkbenchError, "artifact scope changed"):
                self.resolve(expected_scope=scope)
        self.assertEqual(self.requests, [])

    def test_resolver_receipt_pairs_bind_scope_and_distinct_builds(self):
        self.artifacts.pop()
        values, evidence_paths = [], []
        for build_id in (1, 2):
            result = self.resolve(build_id)
            path = self.root / result["evidence"]["path"]
            values.append(json.loads(path.read_bytes()))
            evidence_paths.append(path)
        scope = artifact_scope(self.workbench, **ARGUMENTS)
        def verify(observations):
            return verify_artifact_rule(scope, "artifact-name", "application-package",
                                        observations, root=self.root)
        self.assertTrue(verify(values))
        self.assertFalse(verify([values[0], values[0]]))
        self.assertFalse(verify([values[0], {**values[1], "build_id": 3}]))
        self.assertFalse(verify([values[0], {**values[1], "source": "fixture"}]))
        evidence_paths[1].unlink()
        self.assertFalse(verify(values))

    def test_learned_name_cannot_choose_among_multiple_artifacts(self):
        result = self.resolve(require_unique=True)
        self.assertEqual(result["status"], "SELECTION_REQUIRED")
        self.assertNotIn("evidence", result)

    def test_fixture_verified_names_stay_within_exact_pipeline_and_branch(self):
        pairs = [[json.loads((FIXTURES / f"ado-observation-{index}.json").read_bytes())
                  for index in indices] for indices in ((1, 2), (3, 4))]
        for observations in pairs:
            scope, name = observations[0]["scope"], observations[0]["artifact_name"]
            self.assertTrue(verify_artifact_rule(scope, "artifact-name", name, observations))
            self.assertFalse(verify_artifact_rule({**scope, "pipeline": "28"},
                                                  "artifact-name", name, observations))
            self.assertFalse(verify_artifact_rule({**scope, "branch": "refs/heads/other"},
                                                  "artifact-name", name, observations))


if __name__ == "__main__":
    unittest.main()
