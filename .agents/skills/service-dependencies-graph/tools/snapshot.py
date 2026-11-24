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
    "patterns": {"description": "Search dependency candidates, optional sanitized snippets, and matching canonical source evidence.", "input_schema": object_schema({
        "repository": string_schema(256), "family": string_schema(128), "query": string_schema(500),
        "candidate_id": string_schema(512),
        "service_only": {"type": "boolean", "default": False},
        "include_snippets": {"type": "boolean", "default": False},
        "occurrence_offset": {"type": "integer", "minimum": 0, "default": 0},
        "occurrence_limit": {**integer_schema(1, 500), "default": 10},
        "limit": integer_schema(1, 500), "offset": {"type": "integer", "minimum": 0, "default": 0}}, ())},
    "relationships": {"description": "Read source-backed repository links and unresolved boundaries.", "input_schema": object_schema({"repository": string_schema(256), "limit": integer_schema(1, 200)})},
    "services": {"description": "Read static application and service projections.", "input_schema": object_schema({"repository": string_schema(256)})},
    "search": {"description": "Find graph nodes and their source evidence.", "input_schema": object_schema({"query": string_schema(500), "repository": string_schema(256), "limit": integer_schema(1, 100)}, ("query",))},
    "neighborhood": {"description": "Read direct graph edges and evidence for one node.", "input_schema": object_schema({"node_id": string_schema(512), "limit": integer_schema(1, 200)}, ("node_id",))},
}


SERVICE_PATTERN_FAMILIES = {
    'HTTP_ENDPOINT', 'HTTP_CLIENT', 'HTTP_PROVIDER', 'GRAPHQL_SCHEMA', 'GRAPHQL_CLIENT', 'GRAPHQL_OPERATION', 'GATEWAY_ROUTE',
    'MESSAGE_CHANNEL', 'MESSAGE_CLIENT', 'MESSAGE_OPERATION', 'RPC_INTERFACE',
    'DATABASE_TABLE', 'DATABASE_CLIENT', 'DIRECTORY_CLIENT', 'CACHE_CLIENT', 'STORAGE_CLIENT',
    'FILE_CLIENT', 'NETWORK_CLIENT', 'NETWORK_ENDPOINT', 'CONFIG_READ', 'CONFIG_DECLARATION', 'API_CONTRACT', 'CALL_HINT',
}


def _pattern_matches(row: dict, query: str) -> bool:
    def text_values(value):
        if isinstance(value, dict):
            for item in value.values():
                yield from text_values(item)
        elif isinstance(value, list):
            for item in value:
                yield from text_values(item)
        elif isinstance(value, str):
            yield value

    fields = {key: row.get(key) for key in ('repository', 'path', 'family', 'pattern_id', 'value',
                                           'role_hints', 'protocol_hints', 'occurrences')}
    return any(query.casefold() in value.casefold() for value in text_values(fields))


def _pattern_results(rows: list[dict], graph: dict, include_snippets: bool,
                     occurrence_offset: int = 0, occurrence_limit: int = 10) -> list[dict]:
    """Link source locations for investigation without asserting relationship joins."""
    from collections import defaultdict
    evidence_by_source, nodes_by_evidence = defaultdict(list), defaultdict(set)
    for evidence in graph['evidence']:
        evidence_by_source[(evidence.get('repository'), evidence['path'])].append(evidence)
    for node in graph['nodes']:
        for identifier in node['evidence']:
            nodes_by_evidence[identifier].add(node['id'])
    for edge in graph['edges']:
        for identifier in edge['evidence']:
            nodes_by_evidence[identifier].update((edge['source'], edge['target']))
    results = []
    for row in rows:
        result = dict(row)
        all_occurrences = row.get('occurrences', [])
        occurrences = all_occurrences[occurrence_offset:occurrence_offset + occurrence_limit]
        ranges = [(occurrence.get('start_line', row['line']), occurrence.get('end_line', row['line']))
                  for occurrence in occurrences]
        if not all_occurrences:
            ranges = [(row['line'], row['line'])]
        evidence_ids = sorted(evidence['id'] for evidence in evidence_by_source[(row.get('repository'), row['path'])]
                              if any(start <= evidence['line'] <= end for start, end in ranges))
        result['canonical_evidence_ids'] = evidence_ids
        result['related_node_ids'] = sorted({identifier for evidence_id in evidence_ids
                                             for identifier in nodes_by_evidence[evidence_id]})
        if 'occurrences' in row:
            result['occurrence_count'] = len(all_occurrences)
            result['occurrence_offset'] = occurrence_offset
            next_offset = occurrence_offset + occurrence_limit
            result['next_occurrence_offset'] = next_offset if next_offset < len(all_occurrences) else None
            result['occurrences'] = [{key: value for key, value in occurrence.items()
                                      if include_snippets or key != 'snippet'} for occurrence in occurrences]
        if not include_snippets:
            result.pop('snippet', None)
        results.append(result)
    return results


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
    graph = _read(artifacts, 'graph.json')
    from .validate_graph import SCHEMA_PATH
    schema = json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
    if not Draft202012Validator(schema).is_valid(graph):
        raise SnapshotError('INVALID_SNAPSHOT', 'The dependency graph does not match its saved graph schema.')
    try:
        declaration = manifest.get('architecture_context')
        context = None
        if {APPLIED_CONTEXT, PROVENANCE} & artifacts.keys() or declaration is not None:
            graph = _read(artifacts, 'graph.json')
            context = read_bundle_context(artifacts, {row['id'] for row in graph['repositories']})
        expected = {'input': APPLIED_CONTEXT, 'provenance': PROVENANCE,
                    'status': context['status'] if context else 'USER_REPORTED'}
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
            current = inventory(workspace_root, workspace_root / coverage["repository_root"],
                                layout=coverage.get('repository_layout', 'auto'))
            discovery_captured = all('discovery_sha256' in row for row in coverage.get('repositories', []))
            saved = extraction_fingerprints(coverage, include_discovery=discovery_captured)
            present = extraction_fingerprints(current, include_discovery=discovery_captured)
            changed = sorted(key for key in saved.keys() | present.keys() if saved.get(key) != present.get(key))
            result["freshness"] = {"status": "STALE" if changed else "CURRENT", "changed_paths": changed}
            if not discovery_captured:
                result['discovery_freshness'] = {'status': 'UNKNOWN',
                                                 'reason': 'This snapshot predates the broad discovery file inventory.'}
            if context is not None:
                context_changed = result['architecture_context']['freshness']['changed_paths']
                result['freshness']['changed_paths'] = sorted(set(changed) | set(context_changed))
                result['freshness']['status'] = 'STALE' if result['freshness']['changed_paths'] else 'CURRENT'
        except (KeyError, OSError, ValueError):
            result["freshness"] = {"status": "UNKNOWN", "reason": "Current repository sources could not be compared."}
    elif operation == "patterns":
        coverage = _read(artifacts, "analysis-coverage.json")
        audit_name = coverage.get('declaration_audit')
        if not audit_name or audit_name not in artifacts:
            raise SnapshotError('UNAVAILABLE', 'This snapshot has no deterministic pattern census.')
        audit = _read(artifacts, audit_name)
        rows = audit.get('pattern_candidates', [])
        family = arguments.get('family')
        if arguments.get('candidate_id'):
            rows = [row for row in rows if row.get('id') == arguments['candidate_id']]
        if repository_id:
            rows = [row for row in rows if row.get('repository') == repository_id]
        if family:
            rows = [row for row in rows if row.get('family') == family]
        if arguments.get('service_only', False):
            rows = [row for row in rows if row.get('family') in SERVICE_PATTERN_FAMILIES]
        if arguments.get('query'):
            rows = [row for row in rows if _pattern_matches(row, arguments['query'])]
        limit = arguments.get('limit', 100)
        offset = arguments.get('offset', 0)
        from collections import Counter
        scoped_summary = dict(audit.get('pattern_summary', {}))
        scoped_families = {}
        for name, counts in sorted(Counter((row.get('family'), row.get('accountability', 'UNKNOWN'))
                                           for row in rows).items()):
            family_name, disposition = name
            scoped_families.setdefault(family_name, {})[disposition] = counts
        scoped_summary['families'] = scoped_families
        scoped_summary['scope'] = {'repository': repository_id, 'family': family}
        for name in ('query', 'candidate_id', 'service_only', 'include_snippets', 'occurrence_offset', 'occurrence_limit'):
            if name in arguments:
                scoped_summary['scope'][name] = arguments[name]
        result.update(pattern_summary=scoped_summary, global_pattern_summary=audit.get('pattern_summary', {}),
                      matches=_pattern_results(rows[offset:offset + limit], _read(artifacts, 'graph.json'),
                                               arguments.get('include_snippets', False),
                                               arguments.get('occurrence_offset', 0),
                                               arguments.get('occurrence_limit', 10)),
                      matching_total=len(rows), limit=limit,
                      offset=offset, next_offset=offset + limit if offset + limit < len(rows) else None)
        result['limitations'].append('Pattern filters select investigation candidates. Matching source locations do not establish service calls or provider identity.')
    elif operation == "services":
        services = _read(artifacts, "services.json")
        if repository_id:
            services["services"] = [row for row in services["services"] if row["id"] == repository_id]
            if 'architecture_relationships' in services:
                services['architecture_relationships'] = [row for row in services['architecture_relationships']
                                                          if repository_id in (row['source_repository'], row['target_repository'])]
            services.pop("counts", None)
        result["catalog"] = services
    elif operation == "relationships":
        report = _read(artifacts, "repository-relationships.json")
        limit = arguments.get("limit", 60)
        totals = {}
        for name in ("relationships", "candidates", "unresolved_boundaries", "architecture_relationships"):
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
