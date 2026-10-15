"""Extract static Java HTTP calls that use ``URI`` values.

This extractor covers the narrow form used by the orchestration service:
``client.execute(new URI(CONSTANT), body)`` and ``URI.create(CONSTANT)``.
It resolves only string literals and unambiguous string constants found in the
same repository. Dynamic configuration and computed URLs remain diagnostics.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from tree_sitter import Language, Parser
import tree_sitter_java

from .source_inventory import iter_source_files


CALL = re.compile(
    r"(?P<receiver>[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*)\s*\.\s*"
    r"(?P<method>execute|exchange|getForEntity|getForObject|getForRequest|postForEntity|"
    r"postForObject|put|delete|send|request)\s*\(\s*"
    r"(?:(?:new\s+URI)|(?:URI\s*\.\s*create))\s*\(\s*(?P<expression>[^)]*)\)",
)
URI_CONSTRUCTION = re.compile(
    r"(?P<constructor>new\s+URI|URI\s*\.\s*create)\s*\(\s*(?P<expression>[^)]*)\)",
)


def _without_comments(text: str) -> str:
    encoded = bytearray(text.encode('utf-8'))
    root = Parser(Language(tree_sitter_java.language())).parse(bytes(encoded)).root_node
    for node in _walk(root):
        if node.type in {'line_comment', 'block_comment'}:
            for index in range(node.start_byte, node.end_byte):
                if encoded[index] not in {10, 13}:
                    encoded[index] = 32
    return encoded.decode('utf-8')


def _walk(node):
    yield node
    for child in node.named_children:
        yield from _walk(child)


def _static_constants(source: str, path: Path, repo: Path):
    encoded = source.encode('utf-8')
    root = Parser(Language(tree_sitter_java.language())).parse(encoded).root_node
    def text(node):
        return encoded[node.start_byte:node.end_byte].decode('utf-8') if node else ''
    package = next((text(node).removeprefix('package').strip().rstrip(';').strip()
                    for node in root.named_children if node.type == 'package_declaration'), '')
    imports = [text(node).removeprefix('import').strip().rstrip(';').strip()
               for node in root.named_children if node.type == 'import_declaration']
    constants, contexts = [], []
    for node in _walk(root):
        if node.type in {'class_declaration', 'interface_declaration', 'enum_declaration', 'record_declaration'}:
            owners, owner = [], node
            while owner:
                if owner.type in {'class_declaration', 'interface_declaration', 'enum_declaration', 'record_declaration'}:
                    owners.insert(0, text(owner.child_by_field_name('name')))
                owner = owner.parent
            qualified = '.'.join(([package] if package else []) + owners)
            contexts.append((node.start_byte, node.end_byte, qualified))
        if node.type not in {'field_declaration', 'constant_declaration'} or text(node.child_by_field_name('type')) != 'String':
            continue
        modifiers = next((text(child) for child in node.named_children if child.type == 'modifiers'), '')
        owner = node.parent.parent if node.parent else None
        if not owner or (owner.type != 'interface_declaration' and not {'static', 'final'} <= set(modifiers.split())):
            continue
        context = next((row[2] for row in reversed(contexts) if row[0] <= node.start_byte < row[1]), None)
        for variable in node.named_children:
            if variable.type != 'variable_declarator':
                continue
            value_node = variable.child_by_field_name('value')
            value = _literal(text(value_node)) if value_node and value_node.type == 'string_literal' else None
            if value is not None and context:
                constants.append({
                    'identity': context + '.' + text(variable.child_by_field_name('name')), 'value': value,
                    'path': path.relative_to(repo).as_posix(), 'line': node.start_point.row + 1,
                    'declaration': text(node)[:500], 'extractor': 'java-http-constant',
                })
    return constants, package, imports, contexts


def _line(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _literal(expression: str) -> str | None:
    expression = expression.strip()
    if len(expression) >= 2 and expression[0] in {"'", '"'} and expression[-1] == expression[0]:
        try:
            value = json.loads(expression) if expression[0] == '"' else expression[1:-1]
        except (TypeError, ValueError):
            return None
        return value if isinstance(value, str) else None
    return None


def extract(repo: Path) -> dict[str, list[dict[str, Any]]]:
    repo = repo.resolve()
    java_root = repo / "src/main/java"
    files: list[tuple[Path, str, str]] = []
    constants: dict[str, list[dict]] = {}
    scopes = {}
    if java_root.exists():
        for path in iter_source_files(repo, root=java_root, suffixes={".java"}):
            try:
                original = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            source = _without_comments(original)
            files.append((path, original, source))
            records, package, imports, contexts = _static_constants(source, path, repo)
            scopes[path] = (package, imports, contexts)
            for record in records:
                constants.setdefault(record['identity'], []).append(record)

    def resolve_constant(expression, path, offset):
        if not re.fullmatch(r'(?:[A-Za-z_$][\w$]*\.)*[A-Za-z_$][\w$]*', expression):
            return None
        package, imports, contexts = scopes[path]
        identities = {expression, (package + '.' + expression) if package else expression}
        for imported in imports:
            if imported.startswith('static '):
                imported = imported.removeprefix('static ')
                if imported.endswith('.*'):
                    identities.add(imported[:-2] + '.' + expression)
                elif imported.rsplit('.', 1)[-1] == expression:
                    identities.add(imported)
            else:
                prefix, _, rest = expression.partition('.')
                if imported.rsplit('.', 1)[-1] == prefix and rest:
                    identities.add(imported + '.' + rest)
        byte_offset = len(files_source[path][:offset].encode('utf-8'))
        local = [row for row in contexts if row[0] <= byte_offset < row[1]]
        if local:
            identities.add(min(local, key=lambda row: row[1] - row[0])[2] + '.' + expression)
        records = [record for identity in identities for record in constants.get(identity, [])]
        return records[0] if len(records) == 1 else None

    files_source = {path: source for path, _, source in files}

    calls: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    for path, original, source in files:
        parsed = Parser(Language(tree_sitter_java.language())).parse(source.encode('utf-8')).root_node
        invocations = {node.start_byte for node in _walk(parsed) if node.type == 'method_invocation' and not node.has_error}
        constructions = {node.start_byte for node in _walk(parsed)
                         if node.type in {'method_invocation', 'object_creation_expression'} and not node.has_error}
        byte_offset = lambda position: len(source[:position].encode('utf-8'))
        for match in CALL.finditer(source):
            if byte_offset(match.start()) not in invocations:
                continue
            expression = match.group("expression").strip()
            value = _literal(expression)
            constant = resolve_constant(expression, path, match.start()) if value is None else None
            if constant:
                value = constant['value']
            if not value:
                diagnostics.append({
                    "code": "UNRESOLVED_JAVA_HTTP_URI",
                    "path": path.relative_to(repo).as_posix(),
                    "line": _line(source, match.start()),
                    "message": "Java HTTP URI uses a dynamic or ambiguous expression",
                })
                continue
            if not re.match(r"^(?:https?|wss?)://", value, re.I):
                diagnostics.append({
                    "code": "UNRESOLVED_JAVA_HTTP_URI",
                    "path": path.relative_to(repo).as_posix(),
                    "line": _line(source, match.start()),
                    "message": "Java HTTP URI is not an absolute HTTP URL",
                })
                continue
            calls.append({
                "path": path.relative_to(repo).as_posix(),
                "line": _line(source, match.start()),
                "method": "ANY",
                "path_value": value,
                "receiver": match.group("receiver"),
                "client_method": match.group("method"),
                "declaration": match.group(0)[:500],
                "supporting_evidence": [constant] if constant else [],
            })
        # Surface direct URI construction that is not in a recognized client
        # call. It is a boundary candidate, but its use cannot be proven here.
        recognized = [(m.start(), m.end()) for m in CALL.finditer(source) if byte_offset(m.start()) in invocations]
        for construction in URI_CONSTRUCTION.finditer(source):
            if byte_offset(construction.start()) not in constructions:
                continue
            if any(start <= construction.start() < end for start, end in recognized):
                continue
            expression = construction.group("expression").strip()
            if expression and not _literal(expression) and not resolve_constant(expression, path, construction.start()):
                diagnostics.append({
                    "code": "UNRESOLVED_JAVA_HTTP_URI",
                    "path": path.relative_to(repo).as_posix(),
                    "line": _line(source, construction.start()),
                    "message": "Java URI construction uses a dynamic or unresolved expression",
                })

    return {"calls": calls, "diagnostics": diagnostics}


__all__ = ["extract"]
