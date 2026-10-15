#!/usr/bin/env python3
"""Build the schema-v2 Service Dependencies Graph directly from local web and Spring repositories."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import ipaddress
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit

from ai_sdlc_workbench.relationships.graph.extract_java_dependencies import extract as extract_java_dependencies
from ai_sdlc_workbench.relationships.graph.extract_spring_endpoints import extract_endpoints
from ai_sdlc_workbench.relationships.graph.extract_web_interfaces import extract_interfaces, extract_rtk_base_query_wrappers
from ai_sdlc_workbench.relationships.graph.extract_websocket_endpoints import extract_websocket_endpoints
from ai_sdlc_workbench.relationships.graph.extract_feign_clients import extract_feign_clients
from ai_sdlc_workbench.relationships.graph.extract_file_dependencies import extract as extract_file_dependencies
from ai_sdlc_workbench.relationships.graph.extract_gateway_routes import extract_nginx_routes, extract_open_api_routes
from ai_sdlc_workbench.relationships.graph.extract_grpc_dependencies import extract as extract_grpc_dependencies
from ai_sdlc_workbench.relationships.graph.extract_java_http import extract as extract_java_http
from ai_sdlc_workbench.relationships.graph.extract_redis_dependencies import extract as extract_redis_dependencies
from ai_sdlc_workbench.relationships.graph.repository_inventory import inventory, nginx_files, own_git_revision
from ai_sdlc_workbench.relationships.graph.repository_reports import coverage_report, relationship_report, markdown_report
from ai_sdlc_workbench.relationships.graph.resolve_repository_relationships import resolve
from ai_sdlc_workbench.relationships.graph.source_inventory import is_source_directory, is_source_file, iter_source_files, source_directories


SCHEMA_VERSION = "2.0.0"
GENERATOR_VERSION = "2.0.0"
FOUNDATION_REPOS: set[str] = set()
WEB_GROUPS = {
    "components": ("UI_COMPONENT", "renders the user interactions and visual state for"),
    "hooks": ("HOOK", "coordinates reusable React behavior for"),
    "store": ("STATE", "owns client-side state and actions for"),
    "state": ("STATE", "owns client-side state and actions for"),
    "services": ("CLIENT", "integrates runtime data required by"),
    "service": ("CLIENT", "integrates runtime data required by"),
    "utils": ("UTILITY", "provides shared calculations and transformations for"),
    "common": ("UTILITY", "provides shared supporting behavior for"),
    "schema": ("SCHEMA", "defines data contracts used by"),
    "schemas": ("SCHEMA", "defines data contracts used by"),
}
WEB_DETAIL_PARENTS = {"components", "hooks", "services", "service", "utils", "workflow", "store", "state", "adapters"}
GENERIC_WEB_DIRS = {"common", "components", "hooks", "services", "service", "utils", "workflow", "store", "state", "config", "local", "production", "main", "root"}
JAVA_DETAIL_SUFFIXES = ("Controller", "Service", "Repository", "Client", "Listener", "Processor", "Handler", "Command", "Task", "Mapper", "Publisher")


def stable_id(prefix: str, *parts: object) -> str:
    raw = "|".join(str(part) for part in parts)
    return f"{prefix}:{hashlib.sha256(raw.encode()).hexdigest()[:24]}"


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "unknown"


def words(value: str) -> str:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)
    return re.sub(r"[_-]+", " ", value).strip()


def read(path: Path) -> str:
    try:
        if path.stat().st_size > 2 * 1024 * 1024:
            return ""
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def source_path(workspace: Path, path: Path) -> str:
    return path.relative_to(workspace).as_posix()


class Graph:
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace
        self.repositories: list[dict[str, Any]] = []
        self.nodes: dict[str, dict[str, Any]] = {}
        self.edges: dict[tuple[str, str, str, str], dict[str, Any]] = {}
        self.evidence: dict[str, dict[str, Any]] = {}
        self.diagnostics: dict[str, dict[str, Any]] = {}
        self.repo_roots: dict[str, Path] = {}
        # Ephemeral routing declarations consumed by the deterministic resolver.
        # Matching route evidence is copied onto canonical boundary edges.
        self.gateway_routes: list[dict[str, Any]] = []

    def add_repository(self, path: Path, kind: str, visible: bool) -> str:
        repo_id = f"repo:{path.name}"
        self.repo_roots[repo_id] = path
        self.repositories.append({
            "id": repo_id, "name": path.name, "path": source_path(self.workspace, path),
            "kind": kind, "role": "FOUNDATION" if not visible else "APPLICATION",
            "visible": visible, "ref": own_git_revision(path)["ref"],
            "commit": own_git_revision(path)["commit"],
        })
        return repo_id

    def add_evidence(self, repository: str | None, path: str, line: int, declaration: str, extractor: str,
                     *, directness: str = "DIRECT") -> str:
        evidence_id = stable_id("evidence", repository, path, line, declaration, extractor)
        self.evidence[evidence_id] = {
            "id": evidence_id, "repository": repository, "path": path, "line": max(line, 1),
            "declaration": declaration[:500], "extractor": extractor, "directness": directness,
        }
        return evidence_id

    def add_node(self, node_id: str, node_type: str, name: str, repository: str | None, *,
                 dimensions: Iterable[str], component_kind: str | None, functional_role: str,
                 business_meaning: str, source_paths: Iterable[str], evidence: Iterable[str],
                 assertion_status: str = "CONFIRMED", properties: dict[str, Any] | None = None) -> str:
        item = self.nodes.get(node_id)
        if node_type == "TABLE" and properties:
            properties = dict(properties)
            clients = set(properties.pop("clients", []))
            client = properties.pop("client", None)
            if client:
                clients.add(client)
            if item:
                clients.update(item.get("properties", {}).get("clients", []))
                accesses = {item.get("properties", {}).get("access"), properties.get("access")}
                if "READ_WRITE" in accesses or {"READ", "WRITE"} <= accesses:
                    properties["access"] = "READ_WRITE"
                if assertion_status == "INFERRED":
                    item["assertion_status"] = "INFERRED"
            properties["clients"] = sorted(clients)
        if item:
            item["source_paths"] = sorted(set(item["source_paths"]) | set(source_paths))
            item["evidence"] = sorted(set(item["evidence"]) | set(evidence))
            item["dimensions"] = sorted(set(item["dimensions"]) | set(dimensions))
            if properties:
                item.setdefault("properties", {}).update(properties)
            return node_id
        node = {
            "id": node_id, "type": node_type, "name": name, "repository": repository,
            "dimensions": sorted(set(dimensions)), "functional_role": functional_role,
            "business_meaning": business_meaning, "source_paths": sorted(set(source_paths)),
            "evidence": sorted(set(evidence)), "assertion_status": assertion_status,
        }
        if component_kind:
            node["component_kind"] = component_kind
        if properties:
            node["properties"] = properties
        self.nodes[node_id] = node
        return node_id

    def add_edge(self, source: str, target: str, relationship: str, dimension: str, evidence: Iterable[str], *,
                 assertion_status: str = "CONFIRMED", resolution_status: str | None = None,
                 properties: dict[str, Any] | None = None) -> str:
        key = (source, target, relationship, dimension)
        item = self.edges.get(key)
        if item:
            item["evidence"] = sorted(set(item["evidence"]) | set(evidence))
            for name, value in (properties or {}).items():
                current = item.setdefault("properties", {}).get(name)
                item["properties"][name] = sorted(set(current or []) | set(value)) if isinstance(value, list) else value
            if assertion_status == "INFERRED":
                item["assertion_status"] = "INFERRED"
            if resolution_status in {"UNRESOLVED", "AMBIGUOUS"}:
                item["resolution_status"] = resolution_status
            return item["id"]
        edge = {
            "id": stable_id("edge", *key), "source": source, "target": target,
            "relationship": relationship, "dimension": dimension,
            "evidence": sorted(set(evidence)), "assertion_status": assertion_status,
        }
        if resolution_status:
            edge["resolution_status"] = resolution_status
        if properties:
            edge["properties"] = properties
        self.edges[key] = edge
        return edge["id"]

    def diagnostic(self, code: str, message: str, repository: str | None = None, path: str | None = None) -> None:
        diagnostic_id = stable_id("diagnostic", code, repository, path, message)
        self.diagnostics[diagnostic_id] = {
            "id": diagnostic_id, "severity": "WARNING", "code": code,
            "message": message, **({"repository": repository} if repository else {}),
            **({"path": path} if path else {}),
        }

    def document(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "generator": {"name": "service-dependencies-graph", "version": GENERATOR_VERSION},
            "repositories": sorted(self.repositories, key=lambda item: item["id"]),
            "nodes": sorted(self.nodes.values(), key=lambda item: item["id"]),
            "edges": sorted(self.edges.values(), key=lambda item: item["id"]),
            "evidence": sorted(self.evidence.values(), key=lambda item: item["id"]),
            "diagnostics": sorted(self.diagnostics.values(), key=lambda item: item["id"]),
        }


def code_files(root: Path, suffixes: tuple[str, ...], repository: Path | None = None) -> Iterable[Path]:
    yield from iter_source_files(repository or root, root=root, suffixes=suffixes)


def line_at(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def resolve_import(source: Path, specifier: str, repository: Path) -> Path | None:
    if not specifier.startswith("."):
        return None
    base = Path(os.path.abspath(source.parent / specifier))
    for candidate in (base, *(base.with_suffix(suffix) for suffix in (".tsx", ".ts", ".jsx", ".js")),
                      *(base / f"index{suffix}" for suffix in (".tsx", ".ts", ".jsx", ".js"))):
        if is_source_file(repository, candidate):
            return candidate
    return None


def static_import_values(source: Path, text: str, repository: Path) -> dict[str, str]:
    """Resolve same-repository named imports that export literal API paths.

    This is intentionally narrow. It binds only ``export const NAME =
    \"/api/...\"`` (and equivalent single-quoted literals), because a
    cross-file expression or runtime configuration cannot be proven by the
    static graph extractor. Ambiguous imports are dropped so they remain
    visible as unresolved evidence.
    """
    candidates: dict[str, set[str]] = {}
    for match in re.finditer(r'import\s*\{([^}]+)\}\s*from\s*["\']([^"\']+)["\']', text):
        target = resolve_import(source, match.group(2), repository)
        if target is None:
            continue
        imported_source = read(target)
        exports: dict[str, str] = {}
        for export in re.finditer(
                r'\bexport\s+(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(["\'])(.*?)\2',
                imported_source, re.S):
            try:
                value = ast.literal_eval(export.group(2) + export.group(3) + export.group(2))
            except (SyntaxError, ValueError):
                continue
            if isinstance(value, str) and value.startswith("/api/"):
                exports[export.group(1)] = value
        for item in match.group(1).split(","):
            parts = re.split(r'\s+as\s+', item.strip())
            imported = parts[0].strip()
            local = parts[-1].strip()
            if imported in exports and re.fullmatch(r'[A-Za-z_$][\w$]*', local):
                candidates.setdefault(local, set()).add(exports[imported])
    return {name: values.pop() for name, values in candidates.items() if len(values) == 1}


def static_rtk_imports(source: Path, text: str, repository: Path, workspace: Path) -> tuple[dict, dict]:
    """Resolve only direct local imports with an inspected RTK declaration.

    The local wrapper rule proves base URL composition and method forwarding.
    A GraphQL API import proves only its transport endpoint, not its fields or
    runtime invocation. Keep that supporting source evidence on the emitted
    caller edge.
    """
    base_queries: dict = {}
    apis: dict = {}

    def resolve_rtk_import(specifier: str) -> tuple[Path | None, list[dict]]:
        target = resolve_import(source, specifier, repository)
        if target is not None or specifier.startswith("."):
            return target, []
        config_path = repository / "tsconfig.json"
        if not is_source_file(repository, config_path):
            return None, []
        # TypeScript JSONC allows comments and trailing commas. Preserve
        # quoted strings while removing only those syntax extensions.
        config_text = read(config_path)
        cleaned = re.sub(
            r'"(?:[^"\\]|\\.)*"|//[^\n]*|/\*.*?\*/|,\s*(?=[}\]])',
            lambda match: match.group(0) if match.group(0).startswith('"') else "",
            config_text, flags=re.S,
        )
        try:
            config = json.loads(cleaned)
        except (ValueError, TypeError):
            return None, []
        options = config.get("compilerOptions", {})
        if not isinstance(options, dict) or not isinstance(options.get("baseUrl"), str):
            return None, []
        aliases = options.get("paths", {})
        if not isinstance(aliases, dict):
            return None, []
        candidates: dict[Path, tuple[Path, str, str]] = {}
        for alias, paths in aliases.items():
            if not isinstance(alias, str) or not isinstance(paths, list) or alias.count("*") > 1:
                continue
            if "*" in alias:
                prefix, suffix = alias.split("*")
                if not specifier.startswith(prefix) or not specifier.endswith(suffix):
                    continue
                middle = specifier[len(prefix):len(specifier) - len(suffix) if suffix else None]
            elif specifier == alias:
                middle = ""
            else:
                continue
            for mapped in paths:
                if not isinstance(mapped, str) or mapped.count("*") > 1:
                    continue
                path = repository / options["baseUrl"] / mapped.replace("*", middle)
                for candidate in (path, *(path.with_suffix(suffix) for suffix in (".ts", ".tsx", ".js", ".jsx")),
                                  *(path / f"index{suffix}" for suffix in (".ts", ".tsx", ".js", ".jsx"))):
                    if is_source_file(repository, candidate):
                        candidates[candidate.resolve()] = (candidate, alias, mapped)
        if len(candidates) != 1:
            return None, []
        target, alias, mapped = next(iter(candidates.values()))
        line = line_at(config_text, config_text.find(json.dumps(alias)))
        return target, [{"path": source_path(workspace, config_path), "line": line,
                         "declaration": f'TypeScript baseUrl={options["baseUrl"]}; paths {alias} -> {mapped}',
                         "extractor": "web-typescript-path-alias"}]

    for match in re.finditer(r'import\s*\{([^}]+)\}\s*from\s*["\']([^"\']+)["\']', text):
        target, import_evidence = resolve_rtk_import(match.group(2))
        if target is None:
            continue
        imported_source = read(target)
        wrappers = extract_rtk_base_query_wrappers(imported_source)
        imported_interfaces = extract_interfaces(imported_source)
        exported_apis = imported_interfaces.get("rtk_apis", {})
        for item in match.group(1).split(","):
            parts = re.split(r'\s+as\s+', item.strip())
            imported, local = parts[0].strip(), parts[-1].strip()
            if not re.fullmatch(r'[A-Za-z_$][\w$]*', local):
                continue
            if imported in wrappers:
                wrapper = dict(wrappers[imported])
                wrapper["supporting_evidence"] = [*import_evidence, {
                    "path": source_path(workspace, target), "line": wrapper["line"],
                    "declaration": wrapper["declaration"], "extractor": "web-rtk-base-query",
                }]
                base_queries[local] = wrapper
            if imported in exported_apis:
                api = dict(exported_apis[imported])
                supporting = []
                for operation in imported_interfaces["operations"]:
                    if operation["protocol"] == api.get("protocol") and operation["path"] in api.get("paths", []):
                        supporting.append({
                            "path": source_path(workspace, target), "line": operation["line"],
                            "declaration": operation["declaration"], "extractor": "web-rtk-base-query",
                        })
                if supporting:
                    api["supporting_evidence"] = [*import_evidence, *supporting]
                    apis[local] = api
    return base_queries, apis


def web_owner_for(path: Path, page_roots: dict[Path, str], app_id: str) -> str:
    matches = [(root, node_id) for root, node_id in page_roots.items() if path == root or root in path.parents]
    return max(matches, key=lambda item: len(item[0].parts))[1] if matches else app_id


def web_detail_kind(path: Path) -> tuple[str, str, str]:
    lower_parts = {part.lower() for part in path.parts}
    name = words(path.name)
    if "quick search" in name.lower() or "quicksearch" in path.as_posix().lower():
        return "QUICK_SEARCH", f"Captures, validates, and transforms rapid search criteria for {name}", f"Lets users narrow operational data quickly without constructing an advanced query"
    if "components" in lower_parts:
        return "UI_COMPONENT", f"Renders the {name} user interface and interaction states", f"Presents the {name} portion of its owning workflow"
    if "hooks" in lower_parts:
        return "HOOK", f"Coordinates reusable React behavior for {name}", f"Keeps {name} workflow behavior consistent across screens"
    if "workflow" in lower_parts:
        return "WORKFLOW_COMPONENT", f"Coordinates the frontend steps for {name}", f"Implements the user journey for {name}"
    if lower_parts & {"services", "service", "adapters"}:
        return "CLIENT", f"Integrates data and actions required by {name}", f"Connects the {name} workflow to runtime capabilities"
    if lower_parts & {"store", "state"}:
        return "STATE", f"Owns client-side state and actions for {name}", f"Preserves the working state of the {name} workflow"
    return "UTILITY", f"Provides supporting frontend behavior for {name}", f"Supports the {name} portion of its owning business capability"


def extract_web_details(graph: Graph, repo: Path, repository: str, domain_roots: dict[str, Path],
                        page_roots: dict[Path, str]) -> None:
    src = repo / "src"
    for directory in sorted(source_directories(repo, root=src)):
        relative = directory.relative_to(src)
        if len(relative.parts) > 7:
            continue
        name_lower = directory.name.lower()
        parent_lower = directory.parent.name.lower()
        is_quick_search = "quicksearch" in directory.as_posix().lower() or "quick-search" in directory.as_posix().lower()
        if is_quick_search and any("quicksearch" in parent.name.lower() or "quick-search" in parent.name.lower() for parent in directory.parents if parent != src):
            continue
        if not is_quick_search and (parent_lower not in WEB_DETAIL_PARENTS or name_lower in GENERIC_WEB_DIRS):
            continue
        direct_files = sorted(path for path in iter_source_files(repo, root=directory, suffixes={".ts", ".tsx", ".js", ".jsx", ".json"})
                              if path.parent == directory
                              and not path.name.endswith((".test.ts", ".test.tsx", ".spec.ts", ".spec.tsx")))
        if not direct_files:
            continue
        domain_name, domain_root = next(((name, root) for name, root in domain_roots.items() if root == directory or root in directory.parents), (relative.parts[0], src / relative.parts[0]))
        capability_id = f"capability:{repo.name}:{slug(domain_name)}"
        if capability_id not in graph.nodes:
            continue
        kind, role, meaning = web_detail_kind(directory)
        path_value = source_path(graph.workspace, directory) + "/**/*"
        ev = graph.add_evidence(repository, source_path(graph.workspace, direct_files[0]), 1,
                                f"Detailed frontend component {directory.name}", "web-component-detail", directness="SEMANTIC")
        component_id = f"component:{repo.name}:web-detail:{slug(relative.as_posix())}"
        graph.add_node(component_id, "COMPONENT", f"{words(domain_name)} / {words(directory.name)}", repository,
                       dimensions=("RUNTIME", "BUSINESS"), component_kind=kind, functional_role=role,
                       business_meaning=meaning, source_paths=(path_value,), evidence=(ev,), assertion_status="INFERRED",
                       properties={"description_source": "SOURCE_INFERRED", "detail_level": "MODULE"})
        graph.add_edge(capability_id, component_id, "REALIZED_BY", "BUSINESS", (ev,), assertion_status="INFERRED")
        domain_component = f"component:{repo.name}:{slug(domain_name)}:domain"
        if domain_component in graph.nodes:
            graph.add_edge(domain_component, component_id, "CONTAINS_COMPONENT", "RUNTIME", (ev,), assertion_status="INFERRED")
        for page_root, page_id in page_roots.items():
            if domain_root == page_root or domain_root in page_root.parents or page_root in domain_root.parents:
                graph.add_edge(page_id, component_id, "USES_COMPONENT", "RUNTIME", (ev,), assertion_status="INFERRED")


def extract_web(graph: Graph, repo: Path, repository: str, visible: bool) -> None:
    app_id = f"application:{repo.name}"
    manifest = repo / "package.json"
    if not is_source_file(repo, manifest):
        graph.diagnostic('EXCLUDED_REPOSITORY_MANIFEST', 'Repository manifest is excluded by the scan policy',
                         repository, source_path(graph.workspace, manifest))
        return
    evidence = graph.add_evidence(repository, source_path(graph.workspace, manifest), 1, "Web application manifest", "web-manifest")
    graph.add_node(
        app_id, "APPLICATION", repo.name, repository, dimensions=("RUNTIME", "BUSINESS"),
        component_kind="MICRO_FRONTEND" if visible else "FOUNDATION", functional_role="Hosts a React micro-frontend runtime",
        business_meaning="Provides shared platform behavior" if not visible else f"Delivers the {words(repo.name)} user experience",
        source_paths=(source_path(graph.workspace, repo / "src" if is_source_directory(repo, repo / "src") else repo) + "/**/*",), evidence=(evidence,),
        properties={"visible": visible},
    )
    imports: dict[Path, dict[str, Path]] = {}
    files = list(code_files(repo / "src", (".ts", ".tsx", ".js", ".jsx"), repo))
    for path in files:
        text = read(path)
        mapping: dict[str, Path] = {}
        for match in re.finditer(r'import\s+(?:\{[^}]+\}|\*\s+as\s+)?([A-Za-z_$][\w$]*)?[^"\']*from\s*["\']([^"\']+)["\']', text):
            target = resolve_import(path, match.group(2), repo)
            if match.group(1) and target:
                mapping[match.group(1)] = target
        imports[path] = mapping

    page_roots: dict[Path, str] = {}
    for path in files:
        text = read(path)
        for match in re.finditer(r'<Route\b[^>]*\bpath\s*=\s*(?:["\']([^"\']+)["\']|\{([^}]+)\})[^>]*\belement\s*=\s*\{\s*<([A-Za-z_$][\w$]*)', text, re.S):
            route, route_expression, component = match.groups()
            route = route or route_expression.strip()
            component_path = imports.get(path, {}).get(component, path)
            page_root = component_path.parent if component_path.name.startswith("index.") else component_path
            route_ev = graph.add_evidence(repository, source_path(graph.workspace, path), line_at(text, match.start()), match.group(0), "react-router")
            page_id = f"page:{repo.name}:{slug(route)}"
            graph.add_node(
                page_id, "PAGE", words(component), repository, dimensions=("RUNTIME", "BUSINESS"), component_kind="PAGE",
                functional_role=f"Renders the React route {route}", business_meaning=f"Supports the {words(component)} business workflow",
                source_paths=(source_path(graph.workspace, component_path),), evidence=(route_ev,),
                properties={"route": route},
            )
            graph.add_edge(app_id, page_id, "ROUTES_TO", "RUNTIME", (route_ev,))
            graph.add_edge(app_id, page_id, "DELIVERS", "BUSINESS", (route_ev,), assertion_status="INFERRED")
            page_roots[page_root] = page_id

    domain_roots: dict[str, Path] = {}
    included_directories = source_directories(repo, root=repo / "src")
    for child in sorted(included_directories):
        if child.parent == repo / "src" and child.name not in {"Root", "root", "LazyAntd"}:
            domain_roots[child.name] = child
    for name, root in domain_roots.items():
        capability_ev = graph.add_evidence(repository, source_path(graph.workspace, root), 1, f"Domain source area {name}", "web-domain-grouping", directness="SEMANTIC")
        capability_id = f"capability:{repo.name}:{slug(name)}"
        graph.add_node(
            capability_id, "BUSINESS_CAPABILITY", words(name), repository, dimensions=("BUSINESS",), component_kind=None,
            functional_role=f"Groups the frontend behavior for {words(name)}", business_meaning=f"Represents the {words(name)} business capability",
            source_paths=(source_path(graph.workspace, root) + "/**/*",), evidence=(capability_ev,), assertion_status="INFERRED",
        )
        graph.add_edge(app_id, capability_id, "IMPLEMENTS", "BUSINESS", (capability_ev,), assertion_status="INFERRED")
        domain_component_id = f"component:{repo.name}:{slug(name)}:domain"
        graph.add_node(
            domain_component_id, "COMPONENT", f"{words(name)} domain", repository,
            dimensions=("RUNTIME", "BUSINESS"), component_kind="DOMAIN_COMPONENT",
            functional_role=f"Coordinates the frontend behavior owned by {words(name)}",
            business_meaning=f"Implements the user-facing portion of the {words(name)} capability",
            source_paths=(source_path(graph.workspace, root) + "/**/*",), evidence=(capability_ev,), assertion_status="INFERRED",
        )
        graph.add_edge(capability_id, domain_component_id, "REALIZED_BY", "BUSINESS", (capability_ev,), assertion_status="INFERRED")
        related_pages = [node_id for page_root, node_id in page_roots.items() if page_root == root or root in page_root.parents]
        for page_id in related_pages:
            graph.add_edge(capability_id, page_id, "REALIZED_BY", "BUSINESS", (capability_ev,), assertion_status="INFERRED")
            graph.add_edge(page_id, domain_component_id, "USES_COMPONENT", "RUNTIME", (capability_ev,), assertion_status="INFERRED")
        for group_name, (kind, role) in WEB_GROUPS.items():
            group = root / group_name
            if group not in included_directories:
                continue
            component_id = f"component:{repo.name}:{slug(name)}:{kind.lower()}"
            graph.add_node(
                component_id, "COMPONENT", f"{words(name)} {words(group_name)}", repository,
                dimensions=("RUNTIME", "BUSINESS"), component_kind=kind,
                functional_role=f"{role.capitalize()} {words(name)}",
                business_meaning=f"Supports the {words(name)} workflow without defining a separate business capability",
                source_paths=(source_path(graph.workspace, group) + "/**/*",), evidence=(capability_ev,), assertion_status="INFERRED",
            )
            graph.add_edge(capability_id, component_id, "REALIZED_BY", "BUSINESS", (capability_ev,), assertion_status="INFERRED")
            for page_id in related_pages:
                graph.add_edge(page_id, component_id, "USES_COMPONENT", "RUNTIME", (capability_ev,), assertion_status="INFERRED")

    extract_web_details(graph, repo, repository, domain_roots, page_roots)

    for path in files:
        if path.name.endswith((".test.ts", ".test.tsx", ".spec.ts", ".spec.tsx")) or path.name.lower().startswith("readme"):
            continue
        text = read(path)
        owner = web_owner_for(path, page_roots, app_id)
        path_value = source_path(graph.workspace, path)
        for match in re.finditer(r'System\.import\s*\(\s*["\']([^"\']+)["\']\s*\)', text):
            name = match.group(1)
            ev = graph.add_evidence(repository, path_value, line_at(text, match.start()), match.group(0), "systemjs-import")
            remote_id = f"remote:{slug(name)}"
            graph.add_node(remote_id, "REMOTE_APPLICATION", name, None, dimensions=("RUNTIME",), component_kind=None,
                           functional_role="Provides a remotely loaded micro-frontend", business_meaning="External or separately deployed user capability",
                           source_paths=(), evidence=(ev,), properties={"module": name})
            graph.add_edge(owner, remote_id, "LOADS_REMOTE", "RUNTIME", (ev,), resolution_status="UNRESOLVED")
        rtk_base_queries, rtk_apis = static_rtk_imports(path, text, repo, graph.workspace)
        interfaces = extract_interfaces(
            text,
            tsx=path.suffix in {".tsx", ".jsx"},
            external_values=static_import_values(path, text, repo),
            external_base_queries=rtk_base_queries,
            external_rtk_apis=rtk_apis,
        )
        for diagnostic in interfaces["diagnostics"]:
            graph.diagnostic(diagnostic["code"], f"Line {diagnostic['line']}: {diagnostic['message']}", repository, path_value)
        for operation in interfaces["operations"]:
            url, protocol = operation["path"], operation["protocol"]
            relationship = {"REST": "CALLS_REST", "GRAPHQL": "CALLS_GRAPHQL", "WEBSOCKET": "SUBSCRIBES_WS"}[protocol]
            ev = graph.add_evidence(repository, path_value, operation["line"], operation["declaration"], f"web-{protocol.lower()}")
            operation_evidence = {ev}
            for support in operation.get("supporting_evidence", []):
                operation_evidence.add(graph.add_evidence(
                    repository, support.get("path", path_value), support["line"], support["declaration"], support["extractor"],
                ))
            operation_id = stable_id(f"operation:{protocol.lower()}", operation["method"], url)
            graph.add_node(operation_id, "API_OPERATION", url, None, dimensions=("RUNTIME",), component_kind=None,
                           functional_role=f"Provides a {protocol} runtime interface", business_meaning="Supplies data or actions required by a user workflow",
                           source_paths=(), evidence=operation_evidence, assertion_status=operation.get("assertion_status", "CONFIRMED"),
                           properties={"protocol": protocol, "path": url, "method": operation["method"],
                                       **({"conditional": True} if operation.get("conditional") else {})})
            client_id = f"component:{repo.name}:client:{stable_id('path', path_value, protocol).split(':')[1]}"
            graph.add_node(client_id, "COMPONENT", path.stem, repository, dimensions=("RUNTIME", "BUSINESS"),
                           component_kind=f"{protocol}_CLIENT", functional_role=f"Calls {protocol} operation {url}",
                           business_meaning=f"Connects {graph.nodes.get(owner, {}).get('name', repo.name)} to required runtime data",
                           source_paths=(path_value,), evidence=operation_evidence)
            graph.add_edge(owner, client_id, "USES_COMPONENT", "RUNTIME", (ev,))
            graph.add_edge(client_id, operation_id, relationship, "RUNTIME", operation_evidence,
                           assertion_status=operation.get("assertion_status", "CONFIRMED"),
                           resolution_status="UNRESOLVED")
        for match in re.finditer(r'\bgql\s*`\s*(query|mutation|subscription)\s+([A-Za-z_$][\w$]*)', text, re.I):
            operation_type, operation_name = match.groups()
            protocol = "WEBSOCKET" if operation_type.lower() == "subscription" else "GRAPHQL"
            relationship = "SUBSCRIBES_WS" if protocol == "WEBSOCKET" else "CALLS_GRAPHQL"
            ev = graph.add_evidence(repository, path_value, line_at(text, match.start()), match.group(0), "web-graphql-operation")
            operation_id = f"operation:{protocol.lower()}:{slug(operation_name)}"
            graph.add_node(
                operation_id, "API_OPERATION", operation_name, None, dimensions=("RUNTIME",), component_kind=None,
                functional_role=f"Provides a {operation_type.lower()} GraphQL operation",
                business_meaning="Supplies data or actions required by a user workflow", source_paths=(), evidence=(ev,),
                properties={"protocol": protocol, "operation_type": operation_type.upper(), "operation_name": operation_name},
            )
            client_id = f"component:{repo.name}:client:{stable_id('path', path_value, protocol).split(':')[1]}"
            graph.add_node(
                client_id, "COMPONENT", path.stem, repository, dimensions=("RUNTIME", "BUSINESS"),
                component_kind=f"{protocol}_CLIENT", functional_role=f"Invokes GraphQL operation {operation_name}",
                business_meaning=f"Connects {graph.nodes.get(owner, {}).get('name', repo.name)} to required runtime data",
                source_paths=(path_value,), evidence=(ev,),
            )
            graph.add_edge(owner, client_id, "USES_COMPONENT", "RUNTIME", (ev,))
            graph.add_edge(client_id, operation_id, relationship, "RUNTIME", (ev,), resolution_status="UNRESOLVED")


def extract_gateway_configuration(graph: Graph, repo: Path, repository: str) -> None:
    """Index nginx and Spring OpenAPI routes for later exact path joins."""
    for path in nginx_files(repo):
        if path.name.endswith(".j2"):
            path_value = source_path(graph.workspace, path)
            graph.diagnostic("UNRESOLVED_NGINX_TEMPLATE", "Nginx template requires environment values before route resolution", repository, path_value)
            graph.add_evidence(repository, path_value, 1, "Nginx configuration template; environment values are unknown", "nginx-template")
            continue
        routes, diagnostics = extract_nginx_routes(path)
        path_value = source_path(graph.workspace, path)
        for diagnostic in diagnostics:
            graph.diagnostic(diagnostic["code"], diagnostic["message"], repository, path_value)
        for route in routes:
            ev = graph.add_evidence(repository, path_value, int(route["line"]),
                                    f"nginx location {route['location']} proxy_pass {route['upstream']}",
                                    "nginx-route")
            graph.gateway_routes.append({"kind": "NGINX", "evidence": ev, "repository": repository, **route})
    for path in iter_source_files(repo, root=repo / "src/main/resources", suffixes={".yml", ".yaml"}):
        if not path.name.startswith("application"):
            continue
        routes, diagnostics = extract_open_api_routes(path)
        path_value = source_path(graph.workspace, path)
        for diagnostic in diagnostics:
            graph.diagnostic(diagnostic["code"], diagnostic["message"], repository, path_value)
        for route in routes:
            ev = graph.add_evidence(repository, path_value, int(route["line"]),
                                    f"open-api {route['method']} {route['path']} -> {route['service']} {route['endpoint_path']}",
                                    "spring-open-api-route")
            graph.gateway_routes.append({"kind": "OPEN_API", "evidence": ev, "repository": repository, **route})


def extract_infrastructure(graph: Graph, repo: Path, repository: str) -> None:
    """Retain nginx configurations and their explicit upstream boundaries."""
    files = nginx_files(repo)
    if not files:
        return
    service_id = f"service:{repo.name}"
    first = source_path(graph.workspace, files[0])
    manifest = graph.add_evidence(repository, first, 1, "Nginx configuration source", "nginx-configuration")
    graph.add_node(service_id, "SERVICE", repo.name, repository, dimensions=("RUNTIME",),
                   component_kind="NGINX_GATEWAY", functional_role="Declares static proxy routing configuration",
                   business_meaning="Business purpose requires separate reviewed evidence",
                   source_paths=[source_path(graph.workspace, path) for path in files], evidence=[manifest])
    extract_gateway_configuration(graph, repo, repository)
    for path in files:
        if not path.name.endswith(".j2"):
            continue
        path_value = source_path(graph.workspace, path)
        refs = [ev["id"] for ev in graph.evidence.values()
                if ev["path"] == path_value and ev["extractor"] == "nginx-template"]
        component = stable_id("component:nginx-template", repository, path_value)
        graph.add_node(component, "COMPONENT", path.name, repository, dimensions=("RUNTIME",),
                       component_kind="CONFIGURATION_TEMPLATE", functional_role="Declares unresolved environment-dependent proxy configuration",
                       business_meaning="Environment values and active configuration remain unknown",
                       source_paths=[path_value], evidence=refs)
        graph.add_edge(service_id, component, "USES_COMPONENT", "RUNTIME", refs)
    for route in graph.gateway_routes:
        if route.get("kind") != "NGINX" or route.get("repository") != repository:
            continue
        ev = route["evidence"]
        path_value = graph.evidence[ev]["path"]
        component = stable_id("component:nginx-route", repository, path_value, route["line"])
        graph.add_node(component, "COMPONENT", "location " + route["location"], repository,
                       dimensions=("RUNTIME",), component_kind="GATEWAY_ROUTE",
                       functional_role="Declares a proxy route to an upstream boundary",
                       business_meaning="Static routing does not establish deployment or runtime reachability",
                       source_paths=[path_value], evidence=[ev], properties={
                           "location": route["location"], "upstream": route["upstream"],
                           "rewrite_pattern": route.get("rewrite_pattern"), "rewrite_target": route.get("rewrite_target")})
        graph.add_edge(service_id, component, "USES_COMPONENT", "RUNTIME", [ev])
        authority = route.get("upstream_server") or route["upstream"]
        host = ""
        try:
            host = urlsplit("//" + authority).hostname or ""
            ipaddress.ip_address(host)
            alias = ""
        except ValueError:
            alias = host if host and not any(token in host for token in ("$", "{", "}")) else ""
        if route.get("upstream_ambiguous"):
            alias = ""
        boundary = stable_id("external:nginx-upstream", repository, authority)
        graph.add_node(boundary, "EXTERNAL_SYSTEM", authority, None, dimensions=("RUNTIME",),
                       component_kind=None, functional_role="Names a configured nginx upstream",
                       business_meaning="Provider identity remains unresolved until an exact declared identity matches",
                       source_paths=[], evidence=[ev], properties={"service_alias": alias, "upstream": authority})
        graph.add_edge(component, boundary, "CALLS_SERVICE", "RUNTIME", [ev], resolution_status="UNRESOLVED",
                       properties={"client": "NGINX"})


def java_area(relative: Path) -> str:
    parts = relative.parts
    for marker in ("domain", "application", "service", "entrypoint", "infra", "shared"):
        if marker in parts:
            index = parts.index(marker)
            if index + 1 < len(parts) - 1:
                return parts[index + 1]
            return f"{marker}-core"
    if "controller" in parts or "web" in parts:
        stem = relative.stem.removesuffix("Controller")
        return stem or "api"
    if "feign" in parts:
        return "external-services"
    if "listener" in parts or "consumer" in parts or "event" in parts:
        return "messaging"
    if "repository" in parts or "mapper" in parts or "entity" in parts:
        return "persistence"
    if "configuration" in parts or "config" in parts:
        return "configuration"
    return "service-core"


def java_kind(path: Path, text: str) -> tuple[str, str]:
    if "@RestController" in text or "@Controller" in text:
        return "CONTROLLER", "entrypoint"
    if "@FeignClient" in text:
        return "FEIGN_CLIENT", "infrastructure"
    if "@KafkaListener" in text:
        return "KAFKA_CONSUMER", "entrypoint"
    if "KafkaTemplate" in text or "ProducerRecord" in text:
        return "KAFKA_PRODUCER", "infrastructure"
    if "Dqsl" in text or "DQSL" in text or "/dqsl/" in path.as_posix().lower():
        return "DATA_PLATFORM_CLIENT", "infrastructure"
    if any(token in text for token in ("Repository<", "JpaRepository", "CrudRepository", "BaseMapper", "JdbcTemplate")) or "repository" in path.as_posix().lower():
        return "REPOSITORY", "infrastructure"
    if "/domain/" in path.as_posix():
        return "DOMAIN_COMPONENT", "domain"
    if "Service" in path.stem or "/application/" in path.as_posix():
        return "APPLICATION_SERVICE", "application"
    return "COMPONENT", "support"


def ensure_java_component(graph: Graph, repo: Path, repository: str, service_id: str, path: Path, text: str,
                          capabilities: dict[str, str]) -> str:
    relative = path.relative_to(repo)
    area = java_area(relative)
    kind, layer = java_kind(relative, text)
    component_id = f"component:{repo.name}:{slug(area)}:{slug(layer)}"
    path_value = source_path(graph.workspace, path)
    ev = graph.add_evidence(repository, path_value, 1, f"{kind} in {area}", "spring-component-grouping", directness="SEMANTIC")
    graph.add_node(
        component_id, "COMPONENT", f"{words(area)} {words(layer)}", repository,
        dimensions=("RUNTIME", "BUSINESS"), component_kind=kind,
        functional_role=f"Implements the {layer} responsibilities for {words(area)}",
        business_meaning=f"Supports the {words(area)} business capability",
        source_paths=(source_path(graph.workspace, path.parent) + "/**/*.java",), evidence=(ev,), assertion_status="INFERRED",
        properties={"layer": layer},
    )
    capability_id = capabilities.get(area)
    if not capability_id:
        capability_id = f"capability:{repo.name}:{slug(area)}"
        capabilities[area] = capability_id
        graph.add_node(capability_id, "BUSINESS_CAPABILITY", words(area), repository, dimensions=("BUSINESS",), component_kind=None,
                       functional_role=f"Groups service behavior for {words(area)}", business_meaning=f"Represents the {words(area)} business capability",
                       source_paths=(source_path(graph.workspace, path.parent) + "/**/*.java",), evidence=(ev,), assertion_status="INFERRED")
        graph.add_edge(service_id, capability_id, "IMPLEMENTS", "BUSINESS", (ev,), assertion_status="INFERRED")
    graph.add_edge(capability_id, component_id, "REALIZED_BY", "BUSINESS", (ev,), assertion_status="INFERRED")
    return component_id


def java_detail_description(path: Path, kind: str, area: str) -> tuple[str, str]:
    name = words(path.stem)
    roles = {
        "CONTROLLER": f"Exposes inbound operations that invoke {name} behavior",
        "FEIGN_CLIENT": f"Calls a remote service required by {name}",
        "KAFKA_CONSUMER": f"Consumes Kafka messages and starts {name} processing",
        "KAFKA_PRODUCER": f"Publishes Kafka messages produced by {name}",
        "DATA_PLATFORM_CLIENT": f"Fetches selected upstream data through DQSL for {name}",
        "REPOSITORY": f"Reads and writes persistent data required by {name}",
        "DOMAIN_COMPONENT": f"Applies domain rules implemented by {name}",
        "APPLICATION_SERVICE": f"Coordinates the application use cases implemented by {name}",
        "COMPONENT": f"Provides supporting service behavior implemented by {name}",
    }
    meanings = {
        "CONTROLLER": f"Makes the {words(area)} capability available to callers",
        "FEIGN_CLIENT": f"Obtains external capabilities needed by {words(area)}",
        "KAFKA_CONSUMER": f"Responds asynchronously to events affecting {words(area)}",
        "KAFKA_PRODUCER": f"Notifies downstream consumers about {words(area)} outcomes",
        "DATA_PLATFORM_CLIENT": f"Supplies governed upstream data used by {words(area)} decisions",
        "REPOSITORY": f"Preserves the operational state of {words(area)}",
        "DOMAIN_COMPONENT": f"Enforces business behavior for {words(area)}",
        "APPLICATION_SERVICE": f"Carries out the {name} business operation within {words(area)}",
        "COMPONENT": f"Supports the {words(area)} business capability",
    }
    return roles[kind], meanings[kind]


def extract_redis_dependency(graph: Graph, repo: Path, repository: str, service_id: str) -> None:
    """Record explicit Spring Redis configuration and runtime clients.

    Redis is a runtime cache/data dependency even when the application uses a
    higher-level cache manager.  The extractor records the platform and keeps
    cluster identity unknown when it is supplied by deployment configuration.
    """
    extracted = extract_redis_dependencies(repo)
    for diagnostic in extracted["diagnostics"]:
        graph.diagnostic(diagnostic["code"], f"Line {diagnostic['line']}: {diagnostic['message']}", repository,
                         source_path(graph.workspace, repo / diagnostic["path"]))
    hits = [(repo / row["path"], row["line"], row["declaration"]) for row in extracted["hits"]]
    if not hits:
        return
    evidence = tuple(graph.add_evidence(repository, source_path(graph.workspace, path), line, declaration, "redis-client")
                     for path, line, declaration in hits)
    redis_id = f"data-platform:{repo.name}:redis"
    graph.add_node(redis_id, "DATA_PLATFORM", "Redis", repository, dimensions=("RUNTIME",), component_kind=None,
                   functional_role="Provides cache and key-value storage used by the service",
                   business_meaning="Runtime Redis cache or key-value dependency",
                   source_paths=tuple(source_path(graph.workspace, path) for path, _, _ in hits), evidence=evidence,
                   properties={"platform_kind": "CACHE", "cluster_identity": "UNKNOWN"})
    graph.add_edge(service_id, redis_id, "CONNECTS_TO", "RUNTIME", evidence)


def extract_grpc_data_provider_dependency(graph: Graph, repo: Path, repository: str,
                                           calls: list[dict[str, Any]],
                                           dependencies: list[dict[str, Any]]) -> None:
    """Record direct calls to the internal Ratan data-provider gRPC SDK.

    The SDK provider is external to the checked-in repositories.  A direct
    Java call is confirmed static client evidence, while the provider identity
    and deployment endpoint remain unresolved.  A Maven coordinate is attached
    as corroborating build evidence and is never sufficient on its own.
    """
    if not calls:
        return
    data_provider_id = "data-platform:ratan-business-data-provider"
    source_paths = [source_path(graph.workspace, repo / call["path"]) for call in calls]
    evidence: list[str] = []
    for call in calls:
        path = repo / call["path"]
        path_value = source_path(graph.workspace, path)
        evidence.append(graph.add_evidence(
            repository, path_value, int(call["line"]), call["declaration"], "grpc-sdk-client",
        ))
    properties: dict[str, Any] = {
        "platform_kind": "DATA_PROVIDER_GRPC",
        "protocol": "GRPC",
        "client_kind": "INTERNAL_SDK",
        "service_type": calls[0]["service_type"],
        "methods": sorted({call["method"] for call in calls}),
        "provider_identity": "UNKNOWN",
    }
    if dependencies:
        dependency = dependencies[0]
        pom_path = dependency["path"]
        pom_value = source_path(graph.workspace, pom_path)
        pom_ev = graph.add_evidence(
            repository, pom_value, int(dependency["line"]), dependency["declaration"], "maven-dependency",
        )
        evidence.append(pom_ev)
        source_paths.append(pom_value)
        properties["sdk_coordinate"] = f"{dependency['group_id']}:{dependency['artifact_id']}"
        if dependency.get("version"):
            properties["sdk_version"] = dependency["version"]
    graph.add_node(
        data_provider_id, "DATA_PLATFORM", "Ratan Business Data Provider", None,
        dimensions=("RUNTIME",), component_kind=None,
        functional_role="Provides governed business data through an internal gRPC SDK",
        business_meaning="External data-provider service queried by the application",
        source_paths=source_paths, evidence=evidence,
        properties=properties,
    )
    by_component: dict[str, list[str]] = {}
    for call in calls:
        component = call.get("component")
        if component:
            by_component.setdefault(component, []).append(call["path"])
    for component, paths in by_component.items():
        call_evidence = [ev for ev, call in zip(evidence, calls) if call["path"] in paths]
        graph.add_edge(
            component, data_provider_id, "QUERIES_DATA_PLATFORM", "RUNTIME", call_evidence,
            resolution_status="UNRESOLVED",
            properties={
                "protocol": "GRPC",
                "client_kind": "INTERNAL_SDK",
                "service_type": calls[0]["service_type"],
                "methods": sorted({call["method"] for call in calls if call["path"] in paths}),
                "provider_identity": "UNKNOWN",
            },
        )


def ensure_java_detail_component(graph: Graph, repo: Path, repository: str, path: Path, text: str,
                                 group_component: str, capabilities: dict[str, str]) -> str:
    relative = path.relative_to(repo)
    kind, layer = java_kind(relative, text)
    significant = kind in {"CONTROLLER", "FEIGN_CLIENT", "KAFKA_CONSUMER", "KAFKA_PRODUCER", "DATA_PLATFORM_CLIENT", "REPOSITORY"} or path.stem.endswith(JAVA_DETAIL_SUFFIXES)
    if not significant:
        return group_component
    area = java_area(relative)
    path_value = source_path(graph.workspace, path)
    ev = graph.add_evidence(repository, path_value, 1, f"Detailed Spring component {path.stem}", "spring-component-detail", directness="SEMANTIC")
    component_id = f"component:{repo.name}:java-detail:{stable_id('path', relative.as_posix()).split(':')[1]}"
    role, meaning = java_detail_description(path, kind, area)
    graph.add_node(component_id, "COMPONENT", path.stem, repository, dimensions=("RUNTIME", "BUSINESS"),
                   component_kind=kind, functional_role=role, business_meaning=meaning,
                   source_paths=(path_value,), evidence=(ev,), assertion_status="INFERRED",
                   properties={"description_source": "SOURCE_INFERRED", "detail_level": "CLASS", "layer": layer})
    graph.add_edge(group_component, component_id, "CONTAINS_COMPONENT", "RUNTIME", (ev,), assertion_status="INFERRED")
    capability_id = capabilities[area]
    graph.add_edge(capability_id, component_id, "REALIZED_BY", "BUSINESS", (ev,), assertion_status="INFERRED")
    return component_id


def extract_spring(graph: Graph, repo: Path, repository: str) -> None:
    service_id = f"service:{repo.name}"
    pom = repo / "pom.xml"
    if not is_source_file(repo, pom):
        graph.diagnostic('EXCLUDED_REPOSITORY_MANIFEST', 'Repository manifest is excluded by the scan policy',
                         repository, source_path(graph.workspace, pom))
        return
    manifest_ev = graph.add_evidence(repository, source_path(graph.workspace, pom), 1, "Spring service manifest", "spring-manifest")
    graph.add_node(service_id, "SERVICE", repo.name, repository, dimensions=("RUNTIME", "BUSINESS"), component_kind="SPRING_SERVICE",
                   functional_role="Runs a Spring service and its runtime adapters", business_meaning=f"Delivers the {words(repo.name)} business service",
                   source_paths=(source_path(graph.workspace, repo / "src/main" if is_source_directory(repo, repo / "src/main") else repo) + "/**/*",), evidence=(manifest_ev,))
    extract_redis_dependency(graph, repo, repository, service_id)
    java_root = repo / "src/main/java"
    files = list(code_files(java_root, (".java",), repo))
    grpc_extracted = extract_grpc_dependencies(repo)
    java_http = extract_java_http(repo)
    grpc_calls_by_path: dict[str, list[dict[str, Any]]] = {}
    for call in grpc_extracted.get("calls", []):
        grpc_calls_by_path.setdefault(call["path"], []).append(call)
    capabilities: dict[str, str] = {}
    component_by_path: dict[str, str] = {}
    for path in files:
        text = read(path)
        path_value = source_path(graph.workspace, path)
        group_component = ensure_java_component(graph, repo, repository, service_id, path, text, capabilities)
        component = ensure_java_detail_component(graph, repo, repository, path, text, group_component, capabilities)
        component_by_path[path.relative_to(repo).as_posix()] = component
        for call in grpc_calls_by_path.get(path.relative_to(repo).as_posix(), []):
            call["component"] = component
        endpoints = extract_endpoints(text)
        for diagnostic in endpoints["diagnostics"]:
            graph.diagnostic(diagnostic["code"], f"Line {diagnostic['line']}: {diagnostic['message']}", repository, path_value)
        for provider in endpoints.get("graphql", []):
            operation_type = provider["operation_type"]
            operation_name = provider["operation_name"]
            parent_type = provider.get("parent_type", operation_type.title())
            ev = graph.add_evidence(repository, path_value, provider["line"], provider["declaration"], "spring-graphql")
            operation_id = stable_id(f"operation:{repo.name}:graphql", operation_type, parent_type, operation_name)
            graph.add_node(
                operation_id, "API_OPERATION", f"{operation_type} {operation_name}", repository,
                dimensions=("RUNTIME",), component_kind=None,
                functional_role="Exposes a GraphQL runtime field",
                business_meaning=f"Allows callers to query {words(java_area(path.relative_to(repo)))} data or actions",
                source_paths=(path_value,), evidence=(ev,), properties={
                    "protocol": "GRAPHQL", "operation_type": operation_type,
                    "operation_name": operation_name, "field": provider["field"],
                    "parent_type": parent_type, "provider_kind": "GRAPHQL",
                    "controller": provider["controller"], "handler": provider["handler"],
                    "root": provider.get("root", operation_type != "FIELD"),
                })
            graph.add_edge(service_id, operation_id, "EXPOSES", "RUNTIME", (ev,))
            graph.add_edge(operation_id, component, "INVOKES", "RUNTIME", (ev,))
        for endpoint in endpoints["endpoints"]:
            method, url = endpoint["method"], endpoint["path"]
            ev = graph.add_evidence(repository, path_value, endpoint["line"], endpoint["declaration"], "spring-rest")
            operation_id = stable_id(f"operation:{repo.name}", method, url)
            graph.add_node(operation_id, "API_OPERATION", f"{method} {url}", repository, dimensions=("RUNTIME",), component_kind=None,
                           functional_role="Exposes a REST operation", business_meaning=f"Allows callers to invoke {words(java_area(path.relative_to(repo)))} behavior",
                           source_paths=(path_value,), evidence=(ev,), properties={"protocol": "REST", "method": method, "path": url,
                           "provider_kind": "CONTROLLER", "controller": endpoint["controller"], "handler": endpoint["handler"]})
            graph.add_edge(service_id, operation_id, "EXPOSES", "RUNTIME", (ev,))
            graph.add_edge(operation_id, component, "INVOKES", "RUNTIME", (ev,))
        for feign in extract_feign_clients(text):
            target = feign["alias"] or "unresolved-service"
            ev = graph.add_evidence(repository, path_value, feign["line"], feign["declaration"], "spring-feign")
            if feign["reason"]:
                graph.diagnostic("UNRESOLVED_FEIGN_IDENTITY", feign["reason"], repository, path_value)
            target_id = stable_id("external-service", repository, path_value, target)
            graph.add_node(target_id, "EXTERNAL_SYSTEM", target, None, dimensions=("RUNTIME",), component_kind=None,
                           functional_role="Provides a service called through Feign", business_meaning="External runtime dependency",
                           source_paths=(), evidence=(ev,), properties={"service_alias": target if not feign["reason"] else ""})
            graph.add_edge(component, target_id, "CALLS_SERVICE", "RUNTIME", (ev,), resolution_status="UNRESOLVED", properties={"client": "FEIGN"})
            for operation in feign.get("operations", []):
                operation_id = stable_id("operation:feign", target, operation["method"], operation["path"])
                operation_ev = graph.add_evidence(repository, path_value, int(operation["line"]), operation["declaration"], "spring-feign")
                graph.add_node(
                    operation_id, "API_OPERATION", f"{operation['method']} {operation['path']}", None,
                    dimensions=("RUNTIME",), component_kind=None,
                    functional_role="Provides a REST runtime interface called through Feign",
                    business_meaning="Supplies a remote operation required by the service",
                    source_paths=(), evidence=(operation_ev,), properties={
                        "protocol": "REST", "method": operation["method"], "path": operation["path"],
                        "client_kind": "FEIGN", "service_alias": target,
                    })
                graph.add_edge(
                    component, operation_id, "CALLS_REST", "RUNTIME", (operation_ev,),
                    resolution_status="UNRESOLVED", properties={
                        "protocol": "REST", "method": operation["method"], "path": operation["path"],
                        "service_alias": target, "client": "FEIGN",
                    })
        if "Dqsl" in text or "DQSL" in text or "/dqsl/" in path.as_posix().lower():
            ev = graph.add_evidence(repository, path_value, 1, "Source mentions DQSL; runtime client use requires evidence", "dqsl-client",
                                    directness="SEMANTIC")
            dqsl_id = "data-platform:dqsl"
            graph.add_node(dqsl_id, "DATA_PLATFORM", "DQSL", None, dimensions=("RUNTIME", "BUSINESS"), component_kind=None,
                           functional_role="Allows consumers to fetch data from selected upstream sources",
                           business_meaning="External data-lake access platform mediating governed upstream data retrieval",
                           source_paths=(), evidence=(ev,), assertion_status="INFERRED", properties={"platform_kind": "EXTERNAL_DATA_LAKE"})
            graph.add_edge(component, dqsl_id, "CALLS_DATA_PLATFORM", "RUNTIME", (ev,),
                           assertion_status="INFERRED", resolution_status="UNRESOLVED")
            graph.diagnostic("UNRESOLVED_DATA_PLATFORM_CLIENT", "DQSL source reference does not establish a bound runtime client call", repository, path_value)
        if re.search(r'Elasticsearch|OpenSearch|RestHighLevelClient|ElasticsearchClient', text):
            ev = graph.add_evidence(repository, path_value, 1, "Source mentions a search client; runtime use requires evidence", "search-client",
                                    directness="SEMANTIC")
            search_id = f"data-platform:{repo.name}:search"
            graph.add_node(search_id, "DATA_PLATFORM", "Search engine", None, dimensions=("RUNTIME",), component_kind=None,
                           functional_role="Provides indexed search operations", business_meaning="External indexed data dependency",
                           source_paths=(), evidence=(ev,), assertion_status="INFERRED", properties={"platform_kind": "SEARCH_ENGINE"})
            graph.add_edge(component, search_id, "QUERIES_DATA_PLATFORM", "RUNTIME", (ev,),
                           assertion_status="INFERRED", resolution_status="UNRESOLVED")
            graph.diagnostic("UNRESOLVED_DATA_PLATFORM_CLIENT", "Search source reference does not establish a bound runtime client call", repository, path_value)

    for diagnostic in java_http.get("diagnostics", []):
        graph.diagnostic(diagnostic["code"], f"Line {diagnostic['line']}: {diagnostic['message']}", repository,
                         source_path(graph.workspace, repo / diagnostic["path"]))
    for call in java_http.get("calls", []):
        path_value = source_path(graph.workspace, repo / call["path"])
        ev = graph.add_evidence(repository, path_value, int(call["line"]), call["declaration"], "java-http-client")
        call_evidence = {ev}
        for support in call.get('supporting_evidence', []):
            call_evidence.add(graph.add_evidence(
                repository, source_path(graph.workspace, repo / support['path']), support['line'],
                support['declaration'], support['extractor']))
        target = call["path_value"]
        operation_id = stable_id("operation:java-http", call["method"], target)
        graph.add_node(
            operation_id, "API_OPERATION", f"{call['method']} {target}", None,
            dimensions=("RUNTIME",), component_kind=None,
            functional_role="Provides a REST runtime interface called by a Java HTTP client",
            business_meaning="Supplies a remote operation required by the service",
            source_paths=(), evidence=call_evidence, properties={
                "protocol": "REST", "method": call["method"], "path": target,
                "client_kind": "JAVA_URI", "service_alias": "",
            })
        component = component_by_path.get(call["path"], service_id)
        graph.add_edge(
            component, operation_id, "CALLS_REST", "RUNTIME", call_evidence,
            resolution_status="UNRESOLVED", properties={
                "protocol": "REST", "method": call["method"], "path": target,
                "client_kind": "JAVA_URI",
            })

    extract_grpc_data_provider_dependency(
        graph, repo, repository, grpc_extracted.get("calls", []), grpc_extracted.get("dependencies", []),
    )

    extracted = extract_java_dependencies(repo)
    for diagnostic in extracted.get("diagnostics", []):
        graph.diagnostic(diagnostic["code"], diagnostic["message"], repository, source_path(graph.workspace, repo / diagnostic["path"]))
    if extracted["tables"]:
        postgres_evidence = next(
            (path for path in (repo / "pom.xml", repo / "src/main/resources/application.yml", repo / "src/main/resources/application.yaml")
             if is_source_file(repo, path) and re.search(r"postgres(?:ql)?", read(path), re.I)),
            None,
        )
        if postgres_evidence:
            postgres_path = source_path(graph.workspace, postgres_evidence)
            postgres_text = read(postgres_evidence)
            match = re.search(r"postgres(?:ql)?", postgres_text, re.I)
            ev = graph.add_evidence(
                repository, postgres_path, line_at(postgres_text, match.start()) if match else 1,
                "PostgreSQL runtime dependency", "postgres-client",
            )
            database_id = f"database:{repo.name}:postgresql"
            graph.add_node(
                database_id, "DATABASE", "PostgreSQL", repository, dimensions=("RUNTIME",), component_kind=None,
                functional_role="Hosts relational data accessed by the running service",
                business_meaning="Durable service-owned operational data store", source_paths=(postgres_path,), evidence=(ev,),
                properties={"engine": "POSTGRESQL"},
            )
            graph.add_edge(service_id, database_id, "CONNECTS_TO", "RUNTIME", (ev,))
    for table in extracted["tables"]:
        path_value = source_path(graph.workspace, repo / table["path"])
        ev = graph.add_evidence(repository, path_value, int(table["line"]), f"{table['client']} {table['access']} {table['name']}", "java-database-client",
                                directness="SEMANTIC" if table.get("assertion_status") == "INFERRED" else "DIRECT")
        table_id = f"table:{repo.name}:{slug(table['name'])}"
        graph.add_node(table_id, "TABLE", table["name"], repository, dimensions=("RUNTIME",), component_kind=None,
                       functional_role="Stores data accessed by the running service", business_meaning="Persists state required by service workflows",
                       source_paths=tuple(source_path(graph.workspace, repo / item) for item in table.get("related_paths", [table["path"]])), evidence=(ev,),
                       assertion_status=table.get("assertion_status", "CONFIRMED"), properties={"client": table["client"], "access": table["access"]})
        owner = component_by_path.get(table["path"], service_id)
        operations = ("READS", "WRITES") if table["access"] == "READ_WRITE" else (("READS",) if table["access"] == "READ" else ("WRITES",))
        for relationship in operations:
            graph.add_edge(owner, table_id, relationship, "RUNTIME", (ev,), assertion_status=table.get("assertion_status", "CONFIRMED"),
                           properties={"clients": [table["client"]], "access": "READ" if relationship == "READS" else "WRITE"})
        database_id = f"database:{repo.name}:postgresql"
        if database_id in graph.nodes:
            graph.add_edge(database_id, table_id, "CONTAINS", "RUNTIME", (ev,))
    for topic in extracted["topics"]:
        path_value = source_path(graph.workspace, repo / topic["path"])
        protocol = topic.get("protocol", "KAFKA")
        declaration = topic.get("runtime_declaration", f"{topic['direction']} {topic['name']}")
        # The Kafka extractor also records static Camel routes. Preserve the
        # protocol in provenance so FILE/HTTP/unknown route evidence is not
        # reported as a Kafka client finding.
        extractor = "java-kafka-client" if protocol == "KAFKA" else "camel-route"
        ev = graph.add_evidence(repository, path_value, int(topic["line"]), f"{declaration}: {topic['direction']} {topic['name']}", extractor)
        related_evidence = tuple(graph.add_evidence(
            repository, source_path(graph.workspace, repo / item["path"]), int(item["line"]),
            item["declaration"], item.get("extractor", "java-kafka-helper")) for item in topic.get("related_evidence", []))
        evidence = (ev, *related_evidence)
        topic_id = stable_id(f"message-channel:{protocol.lower()}", repository, topic["name"])
        graph.add_node(topic_id, "MESSAGE_CHANNEL", topic["name"], None, dimensions=("RUNTIME",), component_kind=None,
                       functional_role=f"Carries {protocol} messages between runtime components", business_meaning="Asynchronous event or command channel",
                       source_paths=(), evidence=evidence, assertion_status="INFERRED" if topic.get("unresolved") or topic["direction"] == "CONFIGURED" else "CONFIRMED",
                       properties={"protocol": protocol, "topic": topic["name"],
                                   **({"cluster_identity": "UNKNOWN"} if protocol == "KAFKA" else {})})
        owner = component_by_path.get(topic["path"], service_id)
        relationship = topic["direction"] if topic["direction"] in {"PUBLISHES", "CONSUMES"} else "CONFIGURES_TOPIC"
        graph.add_edge(owner, topic_id, relationship, "RUNTIME", evidence,
                       assertion_status="CONFIRMED" if relationship != "CONFIGURES_TOPIC" and not topic.get("unresolved") else "INFERRED",
                       resolution_status="UNRESOLVED" if topic.get("unresolved") or protocol != "KAFKA" else None,
                       properties={"expressions": [topic.get("expression", topic["name"])],
                                   **({"configuration_paths": [source_path(graph.workspace, repo / item) for item in topic["related_paths"]]} if topic.get("related_paths") else {})})

    for operation in extract_file_dependencies(repo)["operations"]:
        path_value = source_path(graph.workspace, repo / operation["path"])
        ev = graph.add_evidence(repository, path_value, int(operation["line"]),
                                operation["declaration"], "java-file-client")
        channel_id = stable_id("message-channel:file", repository, "local-files")
        graph.add_node(channel_id, "MESSAGE_CHANNEL", "Local files", repository,
                       dimensions=("RUNTIME",), component_kind=None,
                       functional_role="Files referenced by explicit file operations",
                       business_meaning="File input or output declared by the service",
                       source_paths=(path_value,), evidence=(ev,),
                       properties={"protocol": "FILE", "channel_kind": "LOCAL_FILES", "path_identity": "UNKNOWN"})
        owner = component_by_path.get(operation["path"], service_id)
        for relationship in operation["relationships"]:
            graph.add_edge(owner, channel_id, relationship, "RUNTIME", (ev,),
                           resolution_status="UNRESOLVED",
                           properties={"file_apis": [operation["api"]], "file_methods": [operation["method"]]})
        graph.diagnostic("UNRESOLVED_FILE_IDENTITY", "Local file operations have unknown path and provider identity",
                         repository, path_value)

    websocket = extract_websocket_endpoints(repo)
    for diagnostic in websocket.get("diagnostics", []):
        graph.diagnostic(diagnostic["code"], diagnostic["message"], repository,
                         source_path(graph.workspace, repo / diagnostic["path"]))
    for endpoint in websocket.get("endpoints", []):
        registration_path = repo / endpoint["source_path"]
        registration_path_value = source_path(graph.workspace, registration_path)
        ev = graph.add_evidence(repository, registration_path_value, int(endpoint["line"]), endpoint["declaration"], "spring-websocket")
        related_evidence = []
        for related in endpoint.get("related_paths", []):
            related_path = repo / related
            if is_source_file(repo, related_path):
                related_evidence.append(graph.add_evidence(repository, source_path(graph.workspace, related_path), 1,
                                                           "WebSocket endpoint default", "spring-websocket"))
        evidence = (ev, *related_evidence)
        operation_id = stable_id("operation:websocket", "ANY", endpoint["path"])
        graph.add_node(operation_id, "API_OPERATION", endpoint["path"], repository,
                       dimensions=("RUNTIME",), component_kind=None,
                       functional_role="Exposes a WebSocket/STOMP endpoint",
                       business_meaning="Carries server-pushed runtime notifications",
                       source_paths=(registration_path_value,), evidence=evidence,
                       properties={"protocol": "WEBSOCKET", "method": "ANY", "path": endpoint["path"],
                                   "provider_kind": "CONTROLLER", "controller": endpoint["controller"],
                                   "handler": endpoint["handler"]})
        graph.add_edge(service_id, operation_id, "EXPOSES", "RUNTIME", evidence)
        component = component_by_path.get(endpoint["source_path"], service_id)
        graph.add_edge(operation_id, component, "INVOKES", "RUNTIME", evidence)


def resolve_cross_repository(graph: Graph) -> None:
    resolve(graph)


def apply_description_overrides(graph: Graph, path: Path) -> None:
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    for description in data.get("descriptions", []):
        node_id = description.get("node_id")
        node = graph.nodes.get(node_id)
        if not node:
            graph.diagnostic("UNKNOWN_DESCRIPTION_NODE", f"Description override references unknown node {node_id}", path=source_path(graph.workspace, path))
            continue
        evidence_ids = []
        for evidence_path in description.get("evidence_paths", []):
            candidate = graph.workspace / evidence_path.split("*", 1)[0].rstrip("/")
            if not candidate.exists():
                graph.diagnostic("INVALID_DESCRIPTION_EVIDENCE", f"Description evidence path does not exist: {evidence_path}", node.get("repository"), evidence_path)
                continue
            evidence_ids.append(graph.add_evidence(node.get("repository"), evidence_path, 1,
                                                   description.get("rationale", "AI-assisted business description"),
                                                   "business-description-override", directness="SEMANTIC"))
        for field in ("functional_role", "business_meaning"):
            value = description.get(field)
            if isinstance(value, str) and value.strip():
                node[field] = value.strip()
        node["evidence"] = sorted(set(node["evidence"]) | set(evidence_ids))
        node.setdefault("properties", {}).update({
            "description_source": description.get("source", "AI_INFERRED"),
            "description_confidence": description.get("confidence", "LOW"),
            "description_rationale": description.get("rationale", "AI inference from source context"),
        })


def dependencies(graph: Graph) -> dict[str, Any]:
    keys = ("tables", "kafka_topics", "message_channels", "packages", "modules", "remote_applications", "data_platforms", "service_calls")
    buckets: dict[str, dict[str, dict[str, dict[str, Any]]]] = {
        repo["id"]: {key: {} for key in keys} for repo in graph.repositories if repo["visible"]
    }
    for edge in graph.edges.values():
        source, target = graph.nodes.get(edge["source"]), graph.nodes.get(edge["target"])
        if not source or not target:
            continue
        repository = source.get("repository")
        if repository not in buckets:
            continue
        category = None
        if edge["relationship"] == "IMPORTS_MODULE": category = "modules"
        elif target["type"] == "TABLE" and edge["relationship"] in {"READS", "WRITES"}: category = "tables"
        elif target["type"] == "MESSAGE_CHANNEL":
            # Keep Kafka topic projections strict. Camel file, HTTP, and
            # unknown routes remain visible as generic message channels.
            category = ("kafka_topics" if target.get("properties", {}).get("protocol") == "KAFKA"
                        else "message_channels")
        elif target["type"] == "REMOTE_APPLICATION": category = "remote_applications"
        elif target["type"] == "DATA_PLATFORM": category = "data_platforms"
        elif edge["relationship"] == "CALLS_SERVICE": category = "service_calls"
        elif edge["relationship"] == "DEPENDS_ON_PACKAGE": category = "packages"
        if not category:
            continue
        row = buckets[repository][category].setdefault(target["name"], {"name": target["name"], "source_paths": set()})
        row["source_paths"].update(graph.evidence[ref]["path"] for ref in edge["evidence"] if ref in graph.evidence)
        row.setdefault("relationships", set()).add(edge["relationship"])
        if category == "packages":
            row.setdefault('scopes', set()).update(edge.get('properties', {}).get('scopes', []))
            row['dependency_kind'] = 'BUILD'
        if category == "modules":
            row['dependency_kind'] = 'MODULE'
            row.setdefault('declared_modules', set()).add(edge['properties']['module'])
        if category == "tables":
            row.setdefault("access", set()).add("READ" if edge["relationship"] == "READS" else "WRITE")
            row.setdefault("clients", set()).update(edge.get("properties", {}).get("clients", []))
        for key, value in target.get("properties", {}).items():
            if category == "tables" and key in {"access", "client", "clients"}:
                continue
            if key in {"access", "client"}:
                row.setdefault({"access": "access", "client": "clients"}[key], set()).add(value)
            else:
                row[key] = value
        if edge.get("resolution_status"):
            row.setdefault("resolution_statuses", set()).add(edge["resolution_status"])
    result: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for repository, values in buckets.items():
        result[repository] = {}
        for key, rows in values.items():
            normalized = []
            for row in rows.values():
                normalized.append({name: sorted(value) if isinstance(value, set) else value for name, value in row.items()})
            result[repository][key] = sorted(normalized, key=lambda row: (row["name"], json.dumps(row, sort_keys=True)))
    return {"schema_version": SCHEMA_VERSION, "repositories": result}


def write_outputs(graph: Graph, out: Path, census: dict | None = None) -> None:
    out.mkdir(parents=True, exist_ok=True)
    document = graph.document()
    (out / "graph.json").write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "dependencies.json").write_text(json.dumps(dependencies(graph), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if census is not None:
        coverage = coverage_report(document, census)
        relationships = relationship_report(document)
        for name, value in (("analysis-coverage.json", coverage), ("repository-relationships.json", relationships)):
            (out / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out / "analysis-report.md").write_text(markdown_report(coverage, relationships), encoding="utf-8")
    repository_root = out / "repositories"
    for repo in document["repositories"]:
        if not repo["visible"]:
            continue
        directory = repository_root / repo["name"]
        directory.mkdir(parents=True, exist_ok=True)
        view = {"schema_version": SCHEMA_VERSION, "graph": "../../graph.json", "repository": repo["id"],
                "dimensions": {"runtime": {"repository": repo["id"], "dimension": "RUNTIME"},
                               "business": {"repository": repo["id"], "dimension": "BUSINESS"}}}
        (directory / "view.json").write_text(json.dumps(view, indent=2) + "\n", encoding="utf-8")
    counts = {collection: len(document[collection]) for collection in ("repositories", "nodes", "edges", "evidence", "diagnostics")}
    (out / "summary.json").write_text(json.dumps({"schema_version": SCHEMA_VERSION, "counts": counts}, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--repos", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--descriptions", type=Path)
    args = parser.parse_args(argv)
    workspace = args.workspace.resolve()
    repos_root = (args.repos or workspace / "repos").resolve()
    out = (args.out or workspace / "relationships/service-dependencies/generated").resolve()
    graph = Graph(workspace)
    census = inventory(workspace, repos_root)
    for row in census["repositories"]:
        repo = workspace / row["path"]
        for exclusion in row['source_exclusions']:
            graph.diagnostic('SOURCE_' + exclusion['reason'], 'Source path is excluded by the scan policy',
                             repository='repo:' + row['name'] if row['kind'] else None,
                             path=source_path(workspace, repo / exclusion['path']))
        if row["status"] in {"MISSING", "UNSUPPORTED"}:
            graph.diagnostic(row["status"] + "_REPOSITORY", "; ".join(row["limitations"]) or "Manifest repository is not present", path=row["path"])
            continue
        visible = repo.name not in FOUNDATION_REPOS
        repository = graph.add_repository(repo, row["kind"], visible)
        for limitation in row["limitations"]:
            graph.diagnostic("PARTIAL_REPOSITORY_COVERAGE", limitation, repository, row["path"])
        if visible:
            if row["kind"] == "WEB":
                extract_web(graph, repo, repository, visible)
                extract_gateway_configuration(graph, repo, repository)
            elif row["kind"] == "INFRA":
                extract_infrastructure(graph, repo, repository)
            else:
                extract_spring(graph, repo, repository)
                extract_gateway_configuration(graph, repo, repository)
        elif repo.name in FOUNDATION_REPOS:
            # Foundation configuration is scan-only metadata, but its route
            # declarations are valid evidence for resolving application calls.
            extract_gateway_configuration(graph, repo, repository)
    resolve_cross_repository(graph)
    apply_description_overrides(graph, (args.descriptions or workspace / "architecture-descriptions.json").resolve())
    write_outputs(graph, out, census)
    print(json.dumps({"output": str(out), "repositories": len(graph.repositories), "visible_repositories": sum(bool(r["visible"]) for r in graph.repositories),
                      "nodes": len(graph.nodes), "edges": len(graph.edges), "evidence": len(graph.evidence), "diagnostics": len(graph.diagnostics)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
