"""Extract typed LDAP and JNDI directory operations without argument values.

Directory identities remain unknown. JNDI InitialDirContext can use a non-LDAP
provider, so its declaration retains the broader DIRECTORY protocol.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from tree_sitter import Language, Parser
import tree_sitter_java

from .source_inventory import iter_source_files


TYPE_SCOPES = {"class_declaration", "interface_declaration", "enum_declaration", "record_declaration"}
METHOD_SCOPES = {"method_declaration", "constructor_declaration", "lambda_expression"}
TEMPLATES = {"org.springframework.ldap.core.LdapTemplate", "org.springframework.ldap.core.LdapOperations"}
CONTEXT_SOURCES = {
    "org.springframework.ldap.core.ContextSource", "org.springframework.ldap.core.support.BaseLdapPathContextSource",
    "org.springframework.ldap.core.support.LdapContextSource", "org.springframework.ldap.core.support.AbstractContextSource",
}
LDAP_CONTEXTS = {"javax.naming.ldap.LdapContext", "javax.naming.ldap.InitialLdapContext"}
DIRECTORY_CONTEXTS = {"javax.naming.directory.DirContext", "javax.naming.directory.InitialDirContext"}
KNOWN_TYPES = TEMPLATES | CONTEXT_SOURCES | LDAP_CONTEXTS | DIRECTORY_CONTEXTS
DIRECTORY_OPERATIONS = {"lookup", "lookupLink", "search", "getAttributes", "bind", "rebind", "unbind",
                        "rename", "modifyAttributes", "createSubcontext", "destroySubcontext", "list", "listBindings"}
TEMPLATE_OPERATIONS = DIRECTORY_OPERATIONS | {"authenticate", "find", "findAll", "findByDn", "create", "update", "delete",
                                             "executeReadOnly", "executeReadWrite"}
CONTEXT_OPERATIONS = {"getContext", "getReadOnlyContext", "getReadWriteContext", "getAnonymousContext"}


def _walk(node):
    yield node
    for child in node.named_children:
        yield from _walk(child)


def _scope(node, kinds):
    while node is not None and node.type not in kinds:
        node = node.parent
    return node


def _operations(encoded: bytes, root, package_types: set[str]) -> list[dict[str, Any]]:
    def text(node):
        return encoded[node.start_byte:node.end_byte].decode("utf-8", errors="replace") if node else ""

    imports: dict[str, set[str]] = {}
    wildcards = set()
    local_types = {text(node.child_by_field_name("name")) for node in _walk(root) if node.type in TYPE_SCOPES}
    generic_types = [(text(next((child for child in node.named_children if child.type == "type_identifier"), None)),
                      node.parent.parent) for node in _walk(root) if node.type == "type_parameter"]
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
        if not value:
            return None
        if value in KNOWN_TYPES:
            return value
        if value in local_types:
            return None
        if any(value == name and scope.start_byte <= node.start_byte and node.end_byte <= scope.end_byte
               for name, scope in generic_types):
            return None
        explicit = imports.get(value)
        if explicit is not None:
            return next(iter(explicit)) if len(explicit) == 1 and explicit <= KNOWN_TYPES else None
        if value in package_types:
            return None
        matches = {name for name in KNOWN_TYPES
                   if name.rsplit(".", 1)[-1] == value and name.rsplit(".", 1)[0] in wildcards}
        return next(iter(matches)) if len(matches) == 1 else None

    # Unknown bindings must also participate, because they can shadow LDAP fields.
    bindings = []
    for node in _walk(root):
        if node.type == "variable_declarator" and node.parent.type in {"field_declaration", "local_variable_declaration"}:
            declaration = node.parent
            field = declaration.type == "field_declaration"
            scope = _scope(declaration, TYPE_SCOPES if field else {"block", "for_statement", "enhanced_for_statement", "switch_block"})
            if scope is not None:
                bindings.append((text(node.child_by_field_name("name")), scope,
                                 known_type(declaration.child_by_field_name("type")), declaration.start_byte, field))
        elif node.type in {"formal_parameter", "spread_parameter", "catch_formal_parameter"}:
            scope = _scope(node, METHOD_SCOPES | {"catch_clause"})
            if scope is not None:
                bindings.append((text(node.child_by_field_name("name")), scope,
                                 known_type(node.child_by_field_name("type")), scope.start_byte, False))
        elif node.type == "enhanced_for_statement":
            bindings.append((text(node.child_by_field_name("name")), node,
                             known_type(node.child_by_field_name("type")), node.start_byte, False))
        elif node.type == "resource":
            statement = _scope(node, {"try_with_resources_statement"})
            scope = statement.child_by_field_name("body") if statement is not None else None
            if scope is not None:
                bindings.append((text(node.child_by_field_name("name")), scope,
                                 known_type(node.child_by_field_name("type")), node.start_byte, False))
        elif node.type == "lambda_expression":
            parameters = node.child_by_field_name("parameters")
            names = ([parameters] if parameters is not None and parameters.type == "identifier"
                     else parameters.named_children if parameters is not None and parameters.type == "inferred_parameters" else [])
            bindings.extend((text(parameter), node, None, node.start_byte, False) for parameter in names)

    def binding_type(name, call, *, field_only=False):
        ancestors, parent = [], call.parent
        while parent is not None:
            ancestors.append(parent)
            parent = parent.parent
        current_type = _scope(call, TYPE_SCOPES)
        candidates = [binding for binding in bindings if binding[0] == name and binding[1] in ancestors
                      and (binding[4] or binding[3] <= call.start_byte)
                      and (not binding[4] or binding[1] == current_type) and (not field_only or binding[4])]
        if not candidates:
            return None
        distance = min(ancestors.index(binding[1]) for binding in candidates)
        closest = [binding for binding in candidates if ancestors.index(binding[1]) == distance]
        return closest[0][2] if len(closest) == 1 else None

    def expression_type(node, call):
        if node is None:
            return None
        if node.type == "identifier":
            return binding_type(text(node), call)
        if node.type == "field_access" and text(node.child_by_field_name("object")) == "this":
            return binding_type(text(node.child_by_field_name("field")), call, field_only=True)
        if node.type in {"object_creation_expression", "cast_expression"}:
            return known_type(node.child_by_field_name("type"))
        if node.type == "method_invocation":
            owner = expression_type(node.child_by_field_name("object"), call)
            if owner in TEMPLATES and text(node.child_by_field_name("name")) == "getContextSource":
                return "org.springframework.ldap.core.ContextSource"
        return None

    rows = []
    for node in _walk(root):
        if node.has_error:
            continue
        api, method = None, None
        if node.type == "object_creation_expression":
            api = known_type(node.child_by_field_name("type"))
            if api in {"javax.naming.directory.InitialDirContext", "javax.naming.ldap.InitialLdapContext"}:
                method = "<init>"
        elif node.type == "method_invocation":
            api = expression_type(node.child_by_field_name("object"), node)
            candidate = text(node.child_by_field_name("name"))
            allowed = (TEMPLATE_OPERATIONS if api in TEMPLATES else CONTEXT_OPERATIONS if api in CONTEXT_SOURCES
                       else DIRECTORY_OPERATIONS if api in LDAP_CONTEXTS | DIRECTORY_CONTEXTS else set())
            if candidate in allowed:
                method = candidate
        if method:
            rows.append({"line": node.start_point.row + 1, "api": api, "method": method,
                         "protocol": "DIRECTORY" if api in DIRECTORY_CONTEXTS else "LDAP",
                         "provider_identity": "UNKNOWN",
                         "declaration": f"new {api}(...)" if method == "<init>" else f"{api}.{method}(...)"})
    return rows


def extract(repo: Path) -> dict[str, list[dict[str, Any]]]:
    """Read one Maven module; the build adapter supplies module-relative paths."""
    repo = repo.absolute()
    parser = Parser(Language(tree_sitter_java.language()))
    sources, package_types = [], {}
    for path in iter_source_files(repo, root=repo / "src/main/java", suffixes={".java"}):
        encoded = path.read_bytes()
        root = parser.parse(encoded).root_node
        package = next((encoded[node.start_byte:node.end_byte].decode("utf-8", errors="replace")
                        for node in root.named_children if node.type == "package_declaration"), "")
        package_types.setdefault(package, set()).update(
            encoded[node.child_by_field_name("name").start_byte:node.child_by_field_name("name").end_byte].decode("utf-8")
            for node in root.named_children if node.type in TYPE_SCOPES and node.child_by_field_name("name") is not None)
        sources.append((path, encoded, root, package))
    operations = [{"path": path.relative_to(repo).as_posix(), **row}
                  for path, encoded, root, package in sources for row in _operations(encoded, root, package_types[package])]
    return {"operations": operations}


__all__ = ["extract"]
