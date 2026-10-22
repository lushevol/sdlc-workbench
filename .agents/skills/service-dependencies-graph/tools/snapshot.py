"""Skill-owned snapshot validation and read-only query operations."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from .architecture_context import (APPLIED_CONTEXT, PROVENANCE, read_bundle_context,
                                   freshness as context_freshness)


class SnapshotError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def object_schema(properties=None, required=()):
    return {"type": "object", "properties": properties or {}, "required": list(required), "additionalProperties": False}


def string_schema(maximum=4096):
    return {"type": "string", "minLength": 1, "maxLength": maximum}


def integer_schema(minimum, maximum):
    return {"type": "integer", "minimum": minimum, "maximum": maximum}


OPERATIONS = {
    "coverage": {"description": "Read graph coverage, source fingerprints, and extraction limits.", "input_schema": object_schema()},
    "relationships": {"description": "Read source-backed repository links and unresolved boundaries.", "input_schema": object_schema({"repository": string_schema(256), "limit": integer_schema(1, 200)})},
    "services": {"description": "Read static application and service projections.", "input_schema": object_schema({"repository": string_schema(256)})},
    "search": {"description": "Find graph nodes and their source evidence.", "input_schema": object_schema({"query": string_schema(500), "repository": string_schema(256), "limit": integer_schema(1, 100)}, ("query",))},
    "neighborhood": {"description": "Read direct graph edges and evidence for one node.", "input_schema": object_schema({"node_id": string_schema(512), "limit": integer_schema(1, 200)}, ("node_id",))},
}


def _bundle(root: Path) -> tuple[dict, dict[str, bytes], str]:
    manifest_bytes = (root / "manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    if (not isinstance(manifest, dict) or
            any(not isinstance(manifest.get(key), str) or not manifest[key]
                for key in ('generated_at', 'graph_sha256')) or
            manifest.get('canonical_graph') != 'graph.json' or
            not isinstance(manifest.get('artifacts'), list)):
        raise SnapshotError("INVALID_SNAPSHOT", "The graph manifest has an invalid structure.")
    artifacts = {}
    for row in manifest["artifacts"]:
        relative = row["path"]
        path = (root / relative).resolve()
        if Path(relative).is_absolute() or not path.is_relative_to(root.resolve()) or relative in artifacts:
            raise SnapshotError("INVALID_SNAPSHOT", "A graph artifact does not match its manifest.")
        content = path.read_bytes()
        if hashlib.sha256(content).hexdigest() != row["sha256"]:
            raise SnapshotError("INVALID_SNAPSHOT", "A graph artifact does not match its manifest.")
        artifacts[relative] = content
    required = {"graph.json", "analysis-coverage.json", "repository-relationships.json", "services.json"}
    if not required <= artifacts.keys():
        raise SnapshotError("INVALID_SNAPSHOT", "The graph snapshot lacks required projections.")
    coverage = _read(artifacts, 'analysis-coverage.json')
    audit = coverage.get('declaration_audit')
    if audit is not None and (audit != 'coverage-declarations.json' or audit not in artifacts):
        raise SnapshotError('INVALID_SNAPSHOT', 'The graph snapshot lacks its declared coverage audit.')
    if hashlib.sha256(artifacts["graph.json"]).hexdigest() != manifest["graph_sha256"]:
        raise SnapshotError("INVALID_SNAPSHOT", "The canonical graph checksum does not match its manifest.")
    try:
        declaration = manifest.get('architecture_context')
        context = None
        if {APPLIED_CONTEXT, PROVENANCE} & artifacts.keys() or declaration is not None:
            graph = _read(artifacts, 'graph.json')
            context = read_bundle_context(artifacts, {row['id'] for row in graph['repositories']})
        expected = {'input': APPLIED_CONTEXT, 'provenance': PROVENANCE, 'status': 'USER_REPORTED'}
        if (context is None and declaration is not None) or (context is not None and declaration != expected):
            raise ValueError('Architecture context manifest declaration does not match saved artifacts')
    except (KeyError, ValueError, TypeError) as error:
        raise SnapshotError('INVALID_SNAPSHOT', 'The architecture context bundle is invalid: ' + str(error)) from error
    return manifest, artifacts, hashlib.sha256(manifest_bytes).hexdigest()


def _read(artifacts: dict[str, bytes], name: str) -> dict:
    return json.loads(artifacts[name])


def query(root: Path, operation: str, arguments: dict, workspace_root: Path) -> dict:
    """Query captured, checksum-verified bytes with the skill's input contract."""
    if operation not in OPERATIONS:
        raise SnapshotError("UNKNOWN_OPERATION", "The skill does not support this operation.")
    if not Draft202012Validator(OPERATIONS[operation]["input_schema"]).is_valid(arguments):
        raise SnapshotError("INVALID_ARGUMENT", "Arguments do not match the operation schema.")
    if any(isinstance(value, str) and "\x00" in value for value in arguments.values()):
        raise SnapshotError("INVALID_ARGUMENT", "Arguments must not contain null bytes.")
    try:
        manifest, artifacts, manifest_sha256 = _bundle(root)
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise SnapshotError("INVALID_SNAPSHOT", "The graph manifest has an invalid structure.") from error
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
        context = None
        if manifest.get('architecture_context') is not None:
            context = read_bundle_context(artifacts, {row['id'] for row in _read(artifacts, 'graph.json')['repositories']})
        if context is not None:
            result['architecture_context'] = {**context, 'freshness': context_freshness(context, workspace_root)}
        if 'coverage-declarations.json' in artifacts:
            audit = _read(artifacts, 'coverage-declarations.json')
            result['declaration_audit'] = {key: audit[key] for key in
                                           ('schema_version', 'repositories', 'families', 'limitations')}
        from .repository_inventory import inventory, extraction_fingerprints
        try:
            current = inventory(workspace_root, workspace_root / coverage["repository_root"])
            saved, present = extraction_fingerprints(coverage), extraction_fingerprints(current)
            changed = sorted(key for key in saved.keys() | present.keys() if saved.get(key) != present.get(key))
            result["freshness"] = {"status": "STALE" if changed else "CURRENT", "changed_paths": changed}
            if context is not None:
                context_changed = result['architecture_context']['freshness']['changed_paths']
                result['freshness']['changed_paths'] = sorted(set(changed) | set(context_changed))
                result['freshness']['status'] = 'STALE' if result['freshness']['changed_paths'] else 'CURRENT'
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
            from .graph_query import search_graph
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
                raise SnapshotError("UNKNOWN_NODE", "The graph contains no node with this ID.")
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


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--data-dir", type=Path, default=Path("relationships/service-dependencies/generated"))
    parser.add_argument("operation", choices=sorted(OPERATIONS))
    parser.add_argument("--args", default="{}")
    args = parser.parse_args(argv)
    workspace = args.workspace.expanduser().resolve()
    data = (args.data_dir if args.data_dir.is_absolute() else workspace / args.data_dir).resolve()
    try:
        payload = json.loads(args.args)
        result = query(data, args.operation, payload, workspace)
    except SnapshotError as error:
        result = {"status": "ERROR", "code": error.code, "message": error.message}
    except (OSError, ValueError, TypeError) as error:
        result = {"status": "ERROR", "code": "QUERY_FAILED", "message": str(error)}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("status") == "SUCCEEDED" else 1
