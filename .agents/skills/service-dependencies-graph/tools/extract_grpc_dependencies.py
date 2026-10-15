#!/usr/bin/env python3
"""Extract explicit internal gRPC/data-provider SDK calls from Java sources.

The extractor deliberately requires both an SDK service type and a direct
method invocation.  A protobuf model import or a Maven coordinate alone is a
build/declaration fact; it does not prove a runtime boundary.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from tree_sitter import Language, Parser
import tree_sitter_java

from .source_inventory import iter_source_files


SDK_GROUP = "com.scb.ratan.grpc.sdk"
SDK_ARTIFACT = "ratanone-data-provider-internal-client"
SERVICE_TYPE = "RatanBusinessDataProviderService"
METHOD = "performCashflowInternallyQuery"

IMPORT = re.compile(
    r"^\s*import\s+com\.scb\.ratan\.grpc\.sdk(?:\.[\w]+)*\.RatanBusinessDataProviderService\s*;",
    re.M,
)
POM_DEPENDENCY = re.compile(
    r"<dependency\b(?P<body>.*?)</dependency>", re.I | re.S,
)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _walk(node):
    yield node
    for child in node.named_children:
        yield from _walk(child)


TYPE_SCOPES = {"class_declaration", "interface_declaration", "enum_declaration", "record_declaration"}
METHOD_SCOPES = {"method_declaration", "constructor_declaration", "lambda_expression"}


def _scope(node, kinds):
    while node is not None and node.type not in kinds:
        node = node.parent
    return node


def _source_calls(original: str) -> list[dict[str, Any]]:
    """Extract calls only from parsed Java invocation nodes and typed bindings."""
    encoded = original.encode("utf-8")
    root = Parser(Language(tree_sitter_java.language())).parse(encoded).root_node

    def text(node):
        return encoded[node.start_byte:node.end_byte].decode("utf-8") if node else ""

    imported = any(
        node.type == "import_declaration" and IMPORT.fullmatch(text(node))
        for node in root.named_children
    )

    def sdk_type(node):
        name = text(node)
        return (imported and name == SERVICE_TYPE) or bool(re.fullmatch(
            r"com\.scb\.ratan\.grpc\.sdk(?:\.[\w]+)*\.RatanBusinessDataProviderService", name,
        ))

    # Record other types too. They can shadow an SDK field and must prevent a
    # false join based on a repeated receiver name.
    bindings = []
    for node in _walk(root):
        if node.type == "variable_declarator" and node.parent.type in {"field_declaration", "local_variable_declaration"}:
            declaration = node.parent
            field = declaration.type == "field_declaration"
            scope = _scope(declaration, TYPE_SCOPES if field else {"block", "for_statement", "enhanced_for_statement"})
            if scope is not None:
                bindings.append({"name": text(node.child_by_field_name("name")), "scope": scope,
                                 "sdk": sdk_type(declaration.child_by_field_name("type")),
                                 "start": declaration.start_byte, "field": field})
        elif node.type in {"formal_parameter", "spread_parameter", "catch_formal_parameter"}:
            scope = _scope(node, METHOD_SCOPES | {"catch_clause"})
            if scope is not None:
                bindings.append({"name": text(node.child_by_field_name("name")), "scope": scope,
                                 "sdk": sdk_type(node.child_by_field_name("type")),
                                 "start": scope.start_byte, "field": False})
        elif node.type == "enhanced_for_statement":
            bindings.append({"name": text(node.child_by_field_name("name")), "scope": node,
                             "sdk": sdk_type(node.child_by_field_name("type")),
                             "start": node.start_byte, "field": False})
        elif node.type == "lambda_expression":
            parameters = node.child_by_field_name("parameters")
            names = ([parameters] if parameters is not None and parameters.type == "identifier"
                     else parameters.named_children if parameters is not None and parameters.type == "inferred_parameters" else [])
            for parameter in names:
                bindings.append({"name": text(parameter), "scope": node, "sdk": False,
                                 "start": node.start_byte, "field": False})

    calls = []
    for node in _walk(root):
        if node.type != "method_invocation" or text(node.child_by_field_name("name")) != METHOD:
            continue
        receiver = node.child_by_field_name("object")
        if receiver is None or receiver.type != "identifier":
            continue
        name = text(receiver)
        ancestors, parent = [], node.parent
        while parent is not None:
            ancestors.append(parent)
            parent = parent.parent
        candidates = [binding for binding in bindings
                      if binding["name"] == name and binding["scope"] in ancestors
                      and (binding["field"] or binding["start"] <= node.start_byte)
                      and (not binding["field"] or binding["scope"] == _scope(node, TYPE_SCOPES))]
        if not candidates:
            continue
        distance = min(ancestors.index(binding["scope"]) for binding in candidates)
        closest = [binding for binding in candidates if ancestors.index(binding["scope"]) == distance]
        if len(closest) != 1 or not closest[0]["sdk"]:
            continue
        calls.append({"line": node.start_point.row + 1, "method": METHOD,
                      "service_type": SERVICE_TYPE, "variable": name,
                      "declaration": f"{SERVICE_TYPE}.{METHOD}(...)",
                      "sdk_group": SDK_GROUP, "sdk_artifact": SDK_ARTIFACT})
    return calls


def _pom_coordinate(path: Path) -> dict[str, Any] | None:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return None
    for element in root.iter():
        element.tag = element.tag.rsplit("}", 1)[-1]
    for dependency_node in root.findall("./dependencies/dependency"):
        values = {child.tag.lower(): (child.text or "").strip()
                  for child in dependency_node if child.tag in {"groupId", "artifactId", "version"}}
        if values.get("groupid") != SDK_GROUP or values.get("artifactid") != SDK_ARTIFACT:
            continue
        # Use the parsed direct dependency as the authority. Locate its source
        # line only after it passed the root-dependencies scope check.
        source = re.sub(r"<!--.*?-->", lambda match: re.sub(r"[^\n]", " ", match.group(0)), text, flags=re.S)
        matches = [match for match in POM_DEPENDENCY.finditer(source)
                   if SDK_GROUP in match.group("body") and SDK_ARTIFACT in match.group("body")]
        # If the same coordinate appears in multiple model sections, do not
        # attach an arbitrary source line to the parsed direct dependency.
        line = line_number(text, matches[0].start()) if len(matches) == 1 else 1
        return {
            "group_id": SDK_GROUP,
            "artifact_id": SDK_ARTIFACT,
            "version": values.get("version"),
            "path": path,
            "line": line,
            "declaration": f"Maven dependency {SDK_GROUP}:{SDK_ARTIFACT}",
        }
    return None


def extract(repo: Path) -> dict[str, list[dict[str, Any]]]:
    """Return direct SDK calls and an optional exact Maven coordinate.

    A source row is emitted only when the imported SDK service is declared and
    the same variable is used for a direct SDK method call.  This prevents
    protobuf-only code and comments from becoming false gRPC dependencies.
    """
    # Keep lexical symlinks intact.  The graph workspace may use `/var` while
    # a temporary checkout resolves to `/private/var`; `absolute()` preserves
    # the workspace's path identity for evidence links.
    repo = repo.absolute()
    calls: list[dict[str, Any]] = []
    java_root = repo / "src" / "main" / "java"
    for path in iter_source_files(repo, root=java_root, suffixes={".java"}):
        try:
            original = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        calls.extend({"path": path.relative_to(repo).as_posix(), **call} for call in _source_calls(original))

    dependency = _pom_coordinate(repo / "pom.xml")
    return {"calls": calls, "dependencies": [dependency] if dependency else []}


__all__ = ["extract"]
