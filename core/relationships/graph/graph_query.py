"""Search and project the canonical static dependency graph."""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from typing import Any, Iterable

STOP_WORDS = {
    "a", "allow", "an", "and", "as", "be", "by", "data", "for", "from",
    "in", "is", "of", "on", "operator", "operators", "or", "support", "the",
    "to", "with",
}


def tokens(value: str) -> set[str]:
    return {
        item for item in re.findall(r"[a-z0-9]+", value.lower())
        if len(item) > 2 and item not in STOP_WORDS
    }


def compact_node(node: dict[str, Any]) -> dict[str, Any]:
    """Keep the useful public fields while avoiding evidence-id noise."""
    fields = (
        "id", "type", "name", "repository", "dimensions", "functional_role",
        "business_meaning", "source_paths", "assertion_status", "component_kind",
        "properties",
    )
    return {field: node[field] for field in fields if field in node}


def search_graph(
    graph: dict[str, Any], query: str, repository: str | None = None,
    dimension: str | None = None, node_types: Iterable[str] | None = None, limit: int = 25,
) -> list[dict[str, Any]]:
    requested = tokens(query)
    allowed_types = set(node_types or [])
    repository_id = None if not repository else (repository if repository.startswith("repo:") else f"repo:{repository}")
    modules = defaultdict(list)
    for edge in graph["edges"]:
        if edge["relationship"] == "IMPORTS_MODULE":
            modules[edge["source"]].append(edge.get("properties", {}).get("module", ""))
    ranked = []
    for node in graph["nodes"]:
        if repository_id and node.get("repository") != repository_id:
            continue
        if dimension and dimension.upper() not in node.get("dimensions", []):
            continue
        if allowed_types and node["type"] not in allowed_types:
            continue
        searchable = " ".join([
            node["name"], node.get("functional_role", ""), node.get("business_meaning", ""),
            " ".join(node.get("source_paths", [])), " ".join(str(value) for value in node.get("properties", {}).values()),
            " ".join(modules[node["id"]]),
        ])
        overlap = requested & tokens(searchable)
        phrase = query.lower() in searchable.lower()
        if not overlap and not phrase:
            continue
        score = (2.0 if phrase else 0.0) + len(overlap) / max(len(requested), 1)
        ranked.append((score, node["id"], compact_node(node)))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return [{"score": round(score, 3), **node} for score, _, node in ranked[:max(1, min(limit, 100))]]


def service_catalog(graph: dict[str, Any], dependencies: dict[str, Any]) -> dict[str, Any]:
    """Build the compact system picture used by Workbench graph clients."""
    nodes_by_repo: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in graph["nodes"]:
        if node.get("repository"):
            nodes_by_repo[node["repository"]].append(node)
    nodes = {node["id"]: node for node in graph["nodes"]}
    services = []
    for repo in graph["repositories"]:
        if not repo["visible"]:
            continue
        owned = nodes_by_repo.get(repo["id"], [])
        roots = [node for node in owned if node["type"] in {"APPLICATION", "SERVICE"}]
        capabilities = [compact_node(node) for node in owned if node["type"] == "BUSINESS_CAPABILITY"]
        pages = [compact_node(node) for node in owned if node["type"] == "PAGE"]
        components = [node for node in owned if node["type"] == "COMPONENT"]
        operations = {}
        for edge in graph["edges"]:
            source = nodes[edge["source"]]
            target = nodes[edge["target"]]
            if source.get("repository") != repo["id"] or target["type"] != "API_OPERATION":
                continue
            key = (target["id"], edge["relationship"])
            row = operations.setdefault(key, {
                "id": target["id"], "name": target["name"], "relationship": edge["relationship"],
                "protocol": target.get("properties", {}).get("protocol"),
                "path": target.get("properties", {}).get("path"), "source_paths": set(),
            })
            row["source_paths"].update(source.get("source_paths", []))
        api_operations = [
            {key: sorted(value) if isinstance(value, set) else value for key, value in row.items() if value is not None}
            for row in operations.values()
        ]
        api_operations.sort(key=lambda row: (row.get("protocol", ""), row["name"], row["relationship"]))
        databases = [compact_node(node) for node in owned if node["type"] == "DATABASE"]
        services.append({
            "id": repo["id"], "name": repo["name"], "kind": repo["kind"], "path": repo["path"],
            "root": compact_node(roots[0]) if roots else None,
            "business": {
                "capabilities": capabilities,
                "pages": pages,
                "component_count": len(components),
                "component_kinds": dict(sorted(Counter(node.get("component_kind", "UNCLASSIFIED") for node in components).items())),
            },
            "runtime": {
                "api_operations": api_operations,
                "databases": databases,
                **dependencies.get("repositories", {}).get(repo["id"], {}),
            },
        })
    return {
        "schema_version": graph["schema_version"],
        "purpose": "Static repository picture with source evidence and unresolved boundaries",
        "counts": {
            "services": sum(service["kind"] == "SPRING" for service in services),
            "web_applications": sum(service["kind"] == "WEB" for service in services),
            "infrastructure_repositories": sum(service["kind"] == "INFRA" for service in services),
            "nodes": len(graph["nodes"]), "edges": len(graph["edges"]),
        },
        "services": services,
    }
