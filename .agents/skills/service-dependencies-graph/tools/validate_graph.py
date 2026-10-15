#!/usr/bin/env python3
"""Validate the compact schema-v2 Service Dependencies Graph and its source evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


TOP_FIELDS = {"schema_version", "generated_at", "generator", "repositories", "nodes", "edges", "evidence", "diagnostics"}
NODE_FIELDS = {"id", "type", "name", "repository", "dimensions", "component_kind", "functional_role", "business_meaning", "source_paths", "evidence", "assertion_status", "properties"}
EDGE_FIELDS = {"id", "source", "target", "relationship", "dimension", "evidence", "assertion_status", "resolution_status", "properties"}
EVIDENCE_FIELDS = {"id", "repository", "path", "line", "declaration", "extractor", "directness"}
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "references" / "architecture" / "architecture-graph.schema.json"


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("graph root must be an object")
    return value


def wildcard_parent(workspace: Path, value: str) -> Path:
    concrete = value.split("*", 1)[0].rstrip("/")
    return workspace / concrete


def validate(graph: dict[str, Any], workspace: Path) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [f"schema {'.'.join(map(str, error.absolute_path)) or '$'}: {error.message}"
              for error in sorted(validator.iter_errors(graph), key=lambda item: str(list(item.absolute_path)))]
    if errors:
        return errors
    if set(graph) != TOP_FIELDS:
        errors.append(f"top-level fields must be exactly {sorted(TOP_FIELDS)}")
    if graph.get("schema_version") != "2.0.0":
        errors.append("schema_version must be 2.0.0")
    collections = {name: graph.get(name) for name in ("repositories", "nodes", "edges", "evidence", "diagnostics")}
    for name, values in collections.items():
        if not isinstance(values, list):
            errors.append(f"{name} must be an array")
    if errors:
        return errors

    ids: dict[str, set[str]] = {}
    for name in ("repositories", "nodes", "edges", "evidence", "diagnostics"):
        values = collections[name]
        item_ids = [item.get("id") for item in values if isinstance(item, dict)]
        ids[name] = {item_id for item_id in item_ids if isinstance(item_id, str)}
        if len(item_ids) != len(ids[name]):
            errors.append(f"{name} has a missing or duplicate ID")
        if item_ids != sorted(item_ids):
            errors.append(f"{name} is not sorted by ID")

    repositories = {item["id"]: item for item in graph["repositories"]}
    nodes = {item["id"]: item for item in graph["nodes"]}
    evidence = {item["id"]: item for item in graph["evidence"]}
    hidden = {item["id"] for item in graph["repositories"] if not item.get("visible")}

    for index, node in enumerate(graph["nodes"]):
        prefix = f"nodes[{index}]"
        unknown = set(node) - NODE_FIELDS
        if unknown:
            errors.append(f"{prefix} has unsupported fields {sorted(unknown)}")
        required = NODE_FIELDS - {"component_kind", "properties"}
        missing = required - set(node)
        if missing:
            errors.append(f"{prefix} misses {sorted(missing)}")
        repository = node.get("repository")
        if repository is not None and repository not in repositories:
            errors.append(f"{prefix} references missing repository {repository}")
        if repository in hidden:
            errors.append(f"{prefix} belongs to excluded foundation repository {repository}")
        if not set(node.get("dimensions", [])) <= {"RUNTIME", "BUSINESS"} or not node.get("dimensions"):
            errors.append(f"{prefix} has invalid dimensions")
        for ref in node.get("evidence", []):
            if ref not in evidence:
                errors.append(f"{prefix} references missing evidence {ref}")
        for path in node.get("source_paths", []):
            if not isinstance(path, str) or path.startswith("/") or ".." in Path(path).parts or not wildcard_parent(workspace, path).resolve().is_relative_to(workspace.resolve()):
                errors.append(f"{prefix} has unsafe source path {path!r}")
            elif not wildcard_parent(workspace, path).exists():
                errors.append(f"{prefix} source path does not exist: {path}")
        if node.get("type") == "TABLE":
            if node.get('properties', {}).get('mapping_only'):
                mapping_evidence = {evidence.get(ref, {}).get('extractor') for ref in node.get('evidence', [])}
                if not mapping_evidence & {'orm-entity', 'sql-column-reference'}:
                    errors.append(f'{prefix} declarative table lacks ORM or SQL reference evidence')
                if any(edge['target'] == node['id'] and edge['relationship'] in {'READS', 'WRITES'} for edge in graph['edges']):
                    errors.append(f'{prefix} mapping-only table cannot assert access operations')
                if node.get('properties', {}).get('access'):
                    errors.append(f'{prefix} mapping-only table cannot declare runtime access')
                continue
            if not any(evidence.get(ref, {}).get("extractor") == "java-database-client" for ref in node.get("evidence", [])):
                errors.append(f"{prefix} table lacks database-client evidence")
            accesses = {"READ" if edge["relationship"] == "READS" else "WRITE" for edge in graph["edges"]
                        if edge["target"] == node["id"] and edge["relationship"] in {"READS", "WRITES"}}
            expected_access = "READ_WRITE" if accesses == {"READ", "WRITE"} else next(iter(accesses), None)
            if node.get("properties", {}).get("access") != expected_access:
                errors.append(f"{prefix} table access contradicts READS/WRITES edges")
            clients = sorted({client for edge in graph["edges"] if edge["target"] == node["id"] and edge["relationship"] in {"READS", "WRITES"}
                              for client in edge.get("properties", {}).get("clients", [])})
            if not clients or node.get("properties", {}).get("clients") != clients:
                errors.append(f"{prefix} table clients contradict declaration edges")
        if node.get('type') == 'COLUMN':
            if not any(evidence.get(ref, {}).get('extractor') in {'orm-column', 'sql-column-reference'}
                       for ref in node.get('evidence', [])):
                errors.append(f'{prefix} column lacks mapping or SQL reference evidence')
        if node.get('type') in {'CONFIGURATION_KEY', 'CONFIGURATION_SOURCE'}:
            if not node.get('evidence'):
                errors.append(f'{prefix} configuration requires source evidence')
            if any(key in node.get('properties', {}) for key in {'value', 'password', 'secret', 'token_value'}):
                errors.append(f'{prefix} configuration must not retain secret values')
        if node.get("id") == "data-platform:dqsl":
            if node.get("properties", {}).get("platform_kind") != "EXTERNAL_DATA_LAKE":
                errors.append("DQSL must be classified as EXTERNAL_DATA_LAKE")

    for index, edge in enumerate(graph["edges"]):
        prefix = f"edges[{index}]"
        unknown = set(edge) - EDGE_FIELDS
        if unknown:
            errors.append(f"{prefix} has unsupported fields {sorted(unknown)}")
        required = EDGE_FIELDS - {"resolution_status", "properties"}
        missing = required - set(edge)
        if missing:
            errors.append(f"{prefix} misses {sorted(missing)}")
        if edge.get("source") not in nodes or edge.get("target") not in nodes:
            errors.append(f"{prefix} has a dangling endpoint")
        if edge.get("dimension") not in {"RUNTIME", "BUSINESS"}:
            errors.append(f"{prefix} has invalid dimension")
        if edge.get('relationship') == 'DEPENDS_ON_PACKAGE':
            properties = edge.get('properties', {})
            if (properties.get('dependency_kind') != 'BUILD' or not properties.get('coordinate')
                    or not isinstance(properties.get('scopes'), list) or not properties['scopes']):
                errors.append(f'{prefix} package dependency requires build coordinate and scopes')
        if edge.get('relationship') == 'IMPORTS_MODULE':
            properties = edge.get('properties', {})
            if (properties.get('dependency_kind') != 'MODULE'
                    or not isinstance(properties.get('module'), str) or not properties['module']):
                errors.append(f'{prefix} module import requires a module name and MODULE dependency kind')
        if edge.get("relationship") == "EXPOSES" and edge.get("source") in nodes and edge.get("target") in nodes:
            source, target = nodes[edge["source"]], nodes[edge["target"]]
            if source["type"] != "SERVICE" or target["type"] != "API_OPERATION" or source["repository"] != target["repository"] or target.get("properties", {}).get("provider_kind") not in {"CONTROLLER", "GRAPHQL", "GATEWAY_TRANSPORT"}:
                errors.append(f"{prefix} EXPOSES requires an owned provider operation")
            if target.get("properties", {}).get("provider_kind") == "GATEWAY_TRANSPORT":
                route_evidence = [evidence.get(ref, {}) for ref in target.get("evidence", [])]
                if (target.get("properties", {}).get("implementation_status") != "UNKNOWN"
                        or not any(item.get("extractor") == "spring-open-api-route"
                                   and item.get("repository") == target["repository"]
                                   and item.get("path") in target.get("source_paths", [])
                                   for item in route_evidence)):
                    errors.append(f"{prefix} gateway transport requires an owned route and unknown implementation status")
        if edge.get("resolution_status") == "RESOLVED" and edge.get("source") in nodes and edge.get("target") in nodes:
            source_repo = nodes[edge["source"]].get("repository")
            target_repo = nodes[edge["target"]].get("repository")
            if source_repo and target_repo and source_repo != target_repo:
                origins = {evidence.get(ref, {}).get("repository") for ref in edge.get("evidence", [])}
                if not {source_repo, target_repo} <= origins:
                    errors.append(f"{prefix} resolved repository link requires consumer and provider evidence")
                if not edge.get("properties", {}).get("resolution_rule"):
                    errors.append(f"{prefix} resolved repository link requires a resolution rule")
        if edge.get("relationship") in {"READS", "WRITES"} and edge.get("target") in nodes and nodes[edge["target"]]["type"] == "TABLE":
            expected_access = "READ" if edge["relationship"] == "READS" else "WRITE"
            if edge.get("properties", {}).get("access") != expected_access or not edge.get("properties", {}).get("clients"):
                errors.append(f"{prefix} database access lacks matching declaration metadata")
        for ref in edge.get("evidence", []):
            if ref not in evidence:
                errors.append(f"{prefix} references missing evidence {ref}")

    for index, item in enumerate(graph["evidence"]):
        prefix = f"evidence[{index}]"
        unknown = set(item) - EVIDENCE_FIELDS
        if unknown:
            errors.append(f"{prefix} has unsupported fields {sorted(unknown)}")
        if set(item) != EVIDENCE_FIELDS:
            errors.append(f"{prefix} must contain exactly {sorted(EVIDENCE_FIELDS)}")
        repository = item.get("repository")
        if repository is not None and repository not in repositories:
            errors.append(f"{prefix} references missing repository {repository}")
        path = item.get("path")
        if not isinstance(path, str) or path.startswith("/") or ".." in Path(path).parts or not wildcard_parent(workspace, path).resolve().is_relative_to(workspace.resolve()):
            errors.append(f"{prefix} has unsafe evidence path {path!r}")
        elif not wildcard_parent(workspace, path).exists():
            errors.append(f"{prefix} path does not exist: {path}")

    for repository in graph["repositories"]:
        if not repository.get("visible"):
            continue
        owned = [node for node in graph["nodes"] if node.get("repository") == repository["id"]]
        if not any("RUNTIME" in node.get("dimensions", []) for node in owned):
            errors.append(f"{repository['id']} has no runtime projection")
        if repository["kind"] not in {"INFRA", "TESTING"} and not any("BUSINESS" in node.get("dimensions", []) for node in owned):
            errors.append(f"{repository['id']} has no business projection")
    return errors


def validate_dependencies(data: dict[str, Any], graph: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {repo["id"] for repo in graph["repositories"] if repo["visible"]}
    if not isinstance(data, dict) or not isinstance(data.get("repositories"), dict):
        return ["dependency catalog must contain a repositories object"]
    repositories = data["repositories"]
    detail_categories = {'configuration_keys', 'entities', 'columns', 'internal_dependencies', 'api_calls', 'orm_mappings'}
    legacy = graph.get('generator', {}).get('version') == '2.0.0'
    if data.get("schema_version") != "2.0.0" or set(repositories) != expected:
        errors.append("dependency catalog version or repository set does not match graph")
        return errors
    for repository, groups in repositories.items():
        if not isinstance(groups, dict):
            errors.append(f"{repository} dependencies must be an object")
            continue
        for category in ("tables", "kafka_topics", "message_channels", "packages", "modules", "remote_applications", "data_platforms", "service_calls",
                         'configuration_keys', 'entities', 'columns', 'internal_dependencies', 'api_calls', 'orm_mappings'):
            if legacy and category in detail_categories and category not in groups:
                continue
            rows = groups.get(category)
            if not isinstance(rows, list):
                errors.append(f"{repository}.{category} must be an array")
                continue
            if not all(isinstance(row, dict) and isinstance(row.get("name"), str) for row in rows):
                errors.append(f"{repository}.{category} rows must be named objects")
                continue
            names = [row.get('id', row.get("name")) for row in rows]
            if len(names) != len(set(names)):
                errors.append(f"{repository}.{category} contains duplicate dependencies")
            for row in rows:
                if not row.get("source_paths") or not row.get("relationships"):
                    errors.append(f"{repository}.{category}.{row.get('name')} lacks paths or relationships")
                if category == "tables" and (not row.get("access") or not row.get("clients")):
                    errors.append(f"{repository}.tables.{row.get('name')} lacks access or database-client evidence")
    if not errors:
        # The catalog is a projection, never an independent source of claims.
        from .build_graph import Graph, dependencies
        canonical = Graph(Path("."))
        canonical.repositories = graph["repositories"]
        canonical.nodes = {item["id"]: item for item in graph["nodes"]}
        canonical.edges = {(item["source"], item["target"], item["relationship"], item["dimension"]): item for item in graph["edges"]}
        canonical.evidence = {item["id"]: item for item in graph["evidence"]}
        projection = dependencies(canonical)
        if legacy:
            for repository, groups in projection['repositories'].items():
                for category in detail_categories - repositories[repository].keys():
                    groups.pop(category, None)
        if data != projection:
            errors.append("dependency catalog does not equal the canonical graph projection")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", type=Path)
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--dependencies", type=Path)
    parser.add_argument("--relationships", type=Path)
    args = parser.parse_args(argv)
    args.workspace = args.workspace.expanduser().resolve()
    for name in ('graph', 'dependencies', 'relationships'):
        path = getattr(args, name)
        if path is not None:
            path = path.expanduser()
            setattr(args, name, (path if path.is_absolute() else args.workspace / path).resolve())
    graph = load(args.graph)
    errors = validate(graph, args.workspace.resolve())
    if args.dependencies and not errors:
        errors.extend(validate_dependencies(load(args.dependencies), graph))
    if args.relationships and not errors:
        from .repository_reports import relationship_report
        if load(args.relationships) != relationship_report(graph):
            errors.append("Repository relationship report does not equal the canonical graph projection")
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2))
        return 1
    print(json.dumps({"valid": True, "graph": str(args.graph.resolve())}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
