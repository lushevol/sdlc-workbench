"""Read checksum-validated static dependency snapshots through existing grants."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from ..models import Context, Operation, Resource
from .common import (BuiltinProvider, ProviderError, configured_path, integer_schema,
                     object_schema, string_schema)


def _bundle(root: Path) -> tuple[dict, dict[str, bytes], str]:
    manifest_bytes = (root / "manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    artifacts = {}
    for row in manifest["artifacts"]:
        relative = row["path"]
        path = (root / relative).resolve()
        if Path(relative).is_absolute() or not path.is_relative_to(root.resolve()) or relative in artifacts:
            raise ProviderError("INVALID_SNAPSHOT", "A graph artifact does not match its manifest.")
        content = path.read_bytes()
        if hashlib.sha256(content).hexdigest() != row["sha256"]:
            raise ProviderError("INVALID_SNAPSHOT", "A graph artifact does not match its manifest.")
        artifacts[relative] = content
    required = {"graph.json", "analysis-coverage.json", "repository-relationships.json", "services.json"}
    if not required <= artifacts.keys():
        raise ProviderError("INVALID_SNAPSHOT", "The graph snapshot lacks required projections.")
    if hashlib.sha256(artifacts["graph.json"]).hexdigest() != manifest["graph_sha256"]:
        raise ProviderError("INVALID_SNAPSHOT", "The canonical graph checksum does not match its manifest.")
    return manifest, artifacts, hashlib.sha256(manifest_bytes).hexdigest()


def _read(artifacts: dict[str, bytes], name: str) -> dict:
    return json.loads(artifacts[name])


class GraphSnapshotProvider(BuiltinProvider):
    id = "graph.snapshot"
    resource_kind = "dependency_graph"
    operations = {
        "coverage": Operation("coverage", "Read graph coverage, source fingerprints, and extraction limits.", object_schema()),
        "relationships": Operation("relationships", "Read source-backed repository links and unresolved boundaries.", object_schema({
            "repository": string_schema(maximum=256), "limit": integer_schema(1, 200)})),
        "services": Operation("services", "Read static application and service projections.", object_schema({
            "repository": string_schema(maximum=256)})),
        "search": Operation("search", "Find graph nodes and their source evidence.", object_schema({
            "query": string_schema(maximum=500), "repository": string_schema(maximum=256),
            "limit": integer_schema(1, 100)}, ("query",))),
        "neighborhood": Operation("neighborhood", "Read direct graph edges and evidence for one node.", object_schema({
            "node_id": string_schema(maximum=512), "limit": integer_schema(1, 200)}, ("node_id",))),
    }

    def _invoke(self, operation: str, resource: Resource, arguments: dict, context: Context) -> dict:
        root = configured_path(resource, context)
        try:
            manifest, artifacts, manifest_sha256 = _bundle(root)
        except (KeyError, TypeError, json.JSONDecodeError) as error:
            raise ProviderError("INVALID_SNAPSHOT", "The graph manifest has an invalid structure.") from error
        result = {"status": "SUCCEEDED", "snapshot": {
            "generated_at": manifest["generated_at"], "graph_sha256": manifest["graph_sha256"],
            "manifest_sha256": manifest_sha256,
        }, "limitations": ["Static declarations do not prove deployment or runtime execution.",
                            "Snapshot checksums identify saved bytes. Check source freshness before drawing current conclusions."]}
        repository = arguments.get("repository")
        repository_id = repository if not repository or repository.startswith("repo:") else "repo:" + repository
        if operation == "coverage":
            coverage = _read(artifacts, "analysis-coverage.json")
            result["coverage"] = coverage
            from ..relationships.graph.repository_inventory import inventory
            try:
                current = inventory(context.workspace_root, context.workspace_root / coverage["repository_root"])
                def fingerprints(census):
                    return {row["path"]: (row["content_sha256"], row.get("commit"), row.get("dirty"))
                            for row in census["repositories"]}
                saved, present = fingerprints(coverage), fingerprints(current)
                changed = sorted(key for key in saved.keys() | present.keys() if saved.get(key) != present.get(key))
                result["freshness"] = {"status": "STALE" if changed else "CURRENT", "changed_paths": changed}
            except (KeyError, OSError, ValueError):
                result["freshness"] = {"status": "UNKNOWN", "reason": "Current repository sources could not be compared."}
        elif operation == "services":
            services = _read(artifacts, "services.json")
            if repository_id:
                services["services"] = [row for row in services["services"] if row["id"] == repository_id]
                services.pop("counts", None)
            result["catalog"] = services
        elif operation == "relationships":
            report = _read(artifacts, "repository-relationships.json")
            limit = arguments.get("limit", 60)
            totals = {}
            for name in ("relationships", "candidates", "unresolved_boundaries"):
                rows = report.get(name, [])
                if repository_id:
                    rows = [row for row in rows if repository_id in (
                        row.get("source_repository"), row.get("target_repository"), row.get("repository"))]
                totals[name] = len(rows)
                report[name] = rows[:limit]
            result.update(report=report, matching_totals=totals, limit=limit)
        else:
            graph = _read(artifacts, "graph.json")
            evidence = {row["id"]: row for row in graph["evidence"]}
            nodes = {row["id"]: row for row in graph["nodes"]}
            if operation == "search":
                from ..relationships.graph.graph_query import search_graph
                matches = search_graph(graph, arguments["query"], repository=repository_id,
                                       limit=arguments.get("limit", 25))
                for row in matches:
                    edges = [edge for edge in graph["edges"] if edge["source"] == row["id"]
                             and edge["relationship"] == "IMPORTS_MODULE"]
                    evidence_ids = set(nodes[row["id"]]["evidence"])
                    evidence_ids.update(key for edge in edges for key in edge["evidence"])
                    row["evidence"] = [evidence[key] for key in sorted(evidence_ids)]
                    if edges:
                        row["module_imports"] = edges
                result.update(matches=matches, limit=arguments.get("limit", 25))
            else:
                node_id = arguments["node_id"]
                if node_id not in nodes:
                    raise ProviderError("UNKNOWN_NODE", "The graph contains no node with this ID.")
                edges = [edge for edge in graph["edges"] if node_id in (edge["source"], edge["target"])]
                total = len(edges)
                edges = edges[:arguments.get("limit", 60)]
                ids = {node_id} | {edge[key] for edge in edges for key in ("source", "target")}
                evidence_ids = {key for edge in edges for key in edge["evidence"]}
                evidence_ids.update(key for identifier in ids for key in nodes[identifier]["evidence"])
                result.update(nodes=[nodes[key] for key in sorted(ids)], edges=edges,
                              evidence=[evidence[key] for key in sorted(evidence_ids)],
                              total_edges=total, limit=arguments.get("limit", 60))
        return result
