#!/usr/bin/env python3
"""Prepare compact, evidence-backed context for AI business-description enrichment."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--focus", help="Case-insensitive component-name or source-path pattern")
    parser.add_argument("--limit", type=int, default=2000)
    args = parser.parse_args(argv)
    graph = json.loads(args.graph.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    evidence = {item["id"]: item for item in graph["evidence"]}
    relationships: dict[str, list[dict[str, str]]] = {node_id: [] for node_id in nodes}
    for edge in graph["edges"]:
        relationships[edge["source"]].append({"direction": "OUT", "relationship": edge["relationship"], "node": edge["target"], "name": nodes[edge["target"]]["name"]})
        relationships[edge["target"]].append({"direction": "IN", "relationship": edge["relationship"], "node": edge["source"], "name": nodes[edge["source"]]["name"]})
    pattern = re.compile(args.focus, re.I) if args.focus else None
    candidates = []
    for node in graph["nodes"]:
        if node["type"] != "COMPONENT" or node.get("properties", {}).get("description_source") not in {"SOURCE_INFERRED", "AI_INFERRED"}:
            continue
        searchable = " ".join([node["name"], *node.get("source_paths", [])])
        if pattern and not pattern.search(searchable):
            continue
        candidates.append({
            "node_id": node["id"], "name": node["name"], "repository": node["repository"],
            "component_kind": node.get("component_kind"), "source_paths": node["source_paths"],
            "description_source": node.get("properties", {}).get("description_source"),
            "description_confidence": node.get("properties", {}).get("description_confidence"),
            "current_functional_role": node["functional_role"], "current_business_meaning": node["business_meaning"],
            "relationships": sorted(relationships[node["id"]], key=lambda row: (row["relationship"], row["name"]))[:30],
            "evidence": [{"path": evidence[ref]["path"], "line": evidence[ref]["line"], "declaration": evidence[ref]["declaration"]}
                         for ref in node["evidence"] if ref in evidence][:8],
        })
    payload: dict[str, Any] = {
        "schema_version": "1.0.0",
        "purpose": "AI input for evidence-backed functional and business descriptions; canonical static graph facts supply source evidence",
        "requested_authoritative_context": [
            "business capability definitions and domain glossary",
            "user personas and the workflow before and after this component",
            "product requirements, acceptance criteria, and operational runbooks",
            "meaning of domain fields, statuses, rules, exceptions, and events",
            "business owners or SME confirmations for ambiguous names",
        ],
        "output_contract": {
            "file": "relationships/service-dependencies/architecture-descriptions.json",
            "fields": ["node_id", "functional_role", "business_meaning", "confidence", "rationale", "evidence_paths", "source"],
            "rules": ["Do not alter runtime relationships", "Use AI_INFERRED unless an authoritative business source confirms the description", "Keep uncertainty explicit"],
        },
        "components": candidates[:args.limit],
        "omitted": max(0, len(candidates) - args.limit),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output.resolve()), "components": len(payload["components"]), "omitted": payload["omitted"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
