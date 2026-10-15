"""Extract explicit Java local-file operations without publishing file paths.

Only parsed calls to known file APIs establish a declaration. A path value,
``File`` construction, or transfer-library coordinate does not establish use.
The caller's repository is the boundary; path and provider identity stay unknown.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from tree_sitter import Language, Parser
import tree_sitter_java

from ai_sdlc_workbench.relationships.graph.source_inventory import iter_source_files


TYPE_SCOPES = {"class_declaration", "interface_declaration", "enum_declaration", "record_declaration"}
METHOD_SCOPES = {"method_declaration", "constructor_declaration", "lambda_expression"}
KNOWN_TYPES = {
    "java.nio.file.Files", "java.nio.file.Paths", "java.nio.file.Path",
    "org.apache.commons.io.FileUtils", "java.io.File",
    "java.io.FileInputStream", "java.io.FileOutputStream", "java.io.FileReader", "java.io.FileWriter",
    "java.io.InputStream", "java.io.OutputStream",
}

# These methods declare file access directly. Metadata predicates such as
# exists(), model construction, and generic InputStream/OutputStream calls are
# deliberately excluded.
STATIC_OPERATIONS = {
    "java.nio.file.Files": {
        "READS": {"readAllBytes", "readAllLines", "readString", "lines", "list", "walk", "walkFileTree", "newInputStream", "newBufferedReader"},
        "WRITES": {"write", "writeString", "newOutputStream", "newBufferedWriter", "createFile", "createDirectory", "createDirectories", "createTempFile", "createTempDirectory", "delete", "deleteIfExists"},
        "BOTH": {"move"},
    },
    "org.apache.commons.io.FileUtils": {
        "READS": {"readFileToByteArray", "readFileToString", "readLines", "lineIterator", "listFiles", "listFilesAndDirs", "iterateFiles", "iterateFilesAndDirs", "openInputStream"},
        "WRITES": {"write", "writeByteArrayToFile", "writeLines", "writeStringToFile", "openOutputStream", "touch", "forceMkdir", "forceMkdirParent", "deleteDirectory", "deleteQuietly", "forceDelete", "cleanDirectory", "copyInputStreamToFile", "copyToFile"},
        "BOTH": {"copyFileToDirectory", "copyDirectory", "copyDirectoryToDirectory", "copyToDirectory", "moveFile", "moveFileToDirectory", "moveDirectory", "moveDirectoryToDirectory", "moveToDirectory"},
    },
}
INSTANCE_OPERATIONS = {
    "java.io.File": {"READS": {"list", "listFiles"}, "WRITES": {"createNewFile", "mkdir", "mkdirs", "delete"}, "BOTH": {"renameTo"}},
    "java.io.FileInputStream": {"READS": {"read", "readAllBytes", "readNBytes", "transferTo"}},
    "java.io.FileOutputStream": {"WRITES": {"write"}},
    "java.io.FileReader": {"READS": {"read", "transferTo"}},
    "java.io.FileWriter": {"WRITES": {"write", "append"}},
}
CONSTRUCTORS = {
    "java.io.FileInputStream": ("READS",), "java.io.FileOutputStream": ("WRITES",),
    "java.io.FileReader": ("READS",), "java.io.FileWriter": ("WRITES",),
}


def _walk(node):
    yield node
    for child in node.named_children:
        yield from _walk(child)


def _scope(node, kinds):
    while node is not None and node.type not in kinds:
        node = node.parent
    return node


def _source_operations(encoded: bytes, root, package_types: set[str]) -> list[dict[str, Any]]:
    def text(node):
        return encoded[node.start_byte:node.end_byte].decode("utf-8") if node else ""

    imports: dict[str, set[str]] = {}
    wildcards = set()
    local_types = {text(node.child_by_field_name("name")) for node in _walk(root)
                   if node.type in TYPE_SCOPES | {"type_parameter"}}
    for node in root.named_children:
        if node.type != "import_declaration":
            continue
        match = re.fullmatch(r"import\s+([\w.]+)(\.\*)?\s*;", text(node).strip())
        if not match:
            continue
        value = match.group(1)
        if match.group(2):
            wildcards.add(value)
        else:
            imports.setdefault(value.rsplit(".", 1)[-1], set()).add(value)

    def known_type(node):
        value = text(node)
        if value in KNOWN_TYPES:
            return value
        if value in local_types:
            return None
        explicit = imports.get(value)
        if explicit is not None:
            return next(iter(explicit)) if len(explicit) == 1 and explicit <= KNOWN_TYPES else None
        if value in package_types:
            return None
        matches = {name for name in KNOWN_TYPES
                   if name.rsplit(".", 1)[-1] == value and name.rsplit(".", 1)[0] in wildcards}
        return next(iter(matches)) if len(matches) == 1 else None

    # Keep unknown bindings. They can shadow a standard API class or a typed
    # field. A repeated receiver name cannot establish type identity.
    bindings = []
    for node in _walk(root):
        if node.type == "variable_declarator" and node.parent.type in {"field_declaration", "local_variable_declaration"}:
            declaration = node.parent
            field = declaration.type == "field_declaration"
            scope = _scope(declaration, TYPE_SCOPES if field else {"block", "for_statement", "enhanced_for_statement", "switch_block"})
            if scope is not None:
                bindings.append({"name": text(node.child_by_field_name("name")), "scope": scope,
                                 "type": known_type(declaration.child_by_field_name("type")),
                                 "start": declaration.start_byte, "field": field})
        elif node.type in {"formal_parameter", "spread_parameter", "catch_formal_parameter"}:
            scope = _scope(node, METHOD_SCOPES | {"catch_clause"})
            if scope is not None:
                bindings.append({"name": text(node.child_by_field_name("name")), "scope": scope,
                                 "type": known_type(node.child_by_field_name("type")),
                                 "start": scope.start_byte, "field": False})
        elif node.type == "enhanced_for_statement":
            bindings.append({"name": text(node.child_by_field_name("name")), "scope": node,
                             "type": known_type(node.child_by_field_name("type")),
                             "start": node.start_byte, "field": False})
        elif node.type == "resource":
            statement = _scope(node, {"try_with_resources_statement"})
            scope = statement.child_by_field_name("body") if statement is not None else None
            if scope is not None:
                bindings.append({"name": text(node.child_by_field_name("name")), "scope": scope,
                                 "type": known_type(node.child_by_field_name("type")),
                                 "start": node.start_byte, "field": False})
        elif node.type == "lambda_expression":
            parameters = node.child_by_field_name("parameters")
            names = ([parameters] if parameters is not None and parameters.type == "identifier"
                     else parameters.named_children if parameters is not None and parameters.type == "inferred_parameters" else [])
            for parameter in names:
                bindings.append({"name": text(parameter), "scope": node, "type": None,
                                 "start": node.start_byte, "field": False})

    def binding_type(name, call, *, field_only=False):
        ancestors, parent = [], call.parent
        while parent is not None:
            ancestors.append(parent)
            parent = parent.parent
        current_type = _scope(call, TYPE_SCOPES)
        candidates = [binding for binding in bindings
                      if binding["name"] == name and binding["scope"] in ancestors
                      and (binding["field"] or binding["start"] <= call.start_byte)
                      and (not binding["field"] or binding["scope"] == current_type)
                      and (not field_only or binding["field"])]
        if not candidates:
            return False, None
        distance = min(ancestors.index(binding["scope"]) for binding in candidates)
        closest = [binding for binding in candidates if ancestors.index(binding["scope"]) == distance]
        return True, closest[0]["type"] if len(closest) == 1 else None

    def expression_type(node, call):
        if node is None:
            return None
        if node.type == "identifier":
            return binding_type(text(node), call)[1]
        if node.type == "field_access" and text(node.child_by_field_name("object")) == "this":
            return binding_type(text(node.child_by_field_name("field")), call, field_only=True)[1]
        if node.type in {"object_creation_expression", "cast_expression"}:
            return known_type(node.child_by_field_name("type"))
        if node.type == "method_invocation":
            owner = static_type(node.child_by_field_name("object"), call)
            method = text(node.child_by_field_name("name"))
            if (owner, method) in {("java.nio.file.Paths", "get"), ("java.nio.file.Path", "of")}:
                return "java.nio.file.Path"
        return None

    def static_type(receiver, call):
        if receiver is None:
            return None
        value = text(receiver)
        # A variable named Files/FileUtils shadows the imported class. Fully
        # qualified calls must also have no variable named java/org at the root.
        bound, _ = binding_type(value.split(".", 1)[0], call)
        return None if bound else known_type(receiver)

    rows = []
    for node in _walk(root):
        api, method, relationships = None, None, ()
        if node.type == "object_creation_expression":
            api = known_type(node.child_by_field_name("type"))
            method = "<init>"
            relationships = CONSTRUCTORS.get(api, ())
        elif node.type == "method_invocation":
            method = text(node.child_by_field_name("name"))
            receiver = node.child_by_field_name("object")
            api = static_type(receiver, node)
            operations = STATIC_OPERATIONS.get(api, {})
            if not operations:
                api = expression_type(receiver, node)
                operations = INSTANCE_OPERATIONS.get(api, {})
            for relationship, methods in operations.items():
                if method in methods:
                    relationships = ("READS", "WRITES") if relationship == "BOTH" else (relationship,)
                    break
            if api == "java.nio.file.Files" and method == "copy":
                args = node.child_by_field_name("arguments")
                types = [expression_type(argument, node) for argument in args.named_children] if args else []
                # Files.copy has Path/stream overloads. Do not infer disk
                # access in a direction that the typed arguments do not prove.
                relationships = tuple(relationship for index, relationship in enumerate(("READS", "WRITES"))
                                      if len(types) > index and types[index] == "java.nio.file.Path")
            elif api == "org.apache.commons.io.FileUtils" and method == "copyFile":
                args = node.child_by_field_name("arguments")
                values = args.named_children if args else []
                # Every copyFile overload reads a File. Its destination can
                # be an OutputStream, so a file write requires a typed File.
                relationships = (("READS", "WRITES") if len(values) > 1
                                 and expression_type(values[1], node) == "java.io.File" else ("READS",))
        if relationships:
            declaration = (f"new {api}(...)" if method == "<init>" else f"{api}.{method}(...)")
            rows.append({"line": node.start_point.row + 1, "api": api, "method": method,
                         "relationships": list(relationships), "declaration": declaration})
    return rows


def extract(repo: Path) -> dict[str, list[dict[str, Any]]]:
    """Return source-backed operations with argument values omitted."""
    repo = repo.absolute()
    parser = Parser(Language(tree_sitter_java.language()))
    sources = []
    package_types: dict[str, set[str]] = {}
    for path in iter_source_files(repo, root=repo / "src/main/java", suffixes={".java"}):
        try:
            encoded = path.read_bytes()
        except OSError:
            continue
        root = parser.parse(encoded).root_node
        package = next((encoded[node.start_byte:node.end_byte].decode("utf-8")
                        for node in root.named_children if node.type == "package_declaration"), "")
        package_types.setdefault(package, set()).update(
            encoded[node.child_by_field_name("name").start_byte:node.child_by_field_name("name").end_byte].decode("utf-8")
            for node in root.named_children if node.type in TYPE_SCOPES and node.child_by_field_name("name") is not None)
        sources.append((path, encoded, root, package))
    operations = []
    for path, encoded, root, package in sources:
        operations.extend({"path": path.relative_to(repo).as_posix(), **row}
                          for row in _source_operations(encoded, root, package_types[package]))
    return {"operations": operations}


__all__ = ["extract"]
