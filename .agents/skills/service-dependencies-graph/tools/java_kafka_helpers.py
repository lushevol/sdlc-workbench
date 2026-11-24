"""Index bounded, typed Java helper calls that forward a Kafka topic parameter.

This is declaration analysis, not compiler-level call or data-flow analysis.
Overloads with equal arity and interfaces with multiple local implementations
remain unsupported. Each discovered call retains the exact helper send sites.
"""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from tree_sitter import Language, Parser
import tree_sitter_java


def index_helpers(sources: dict[Path, str]) -> tuple[dict[Path, Any], dict[Path, dict[int, dict[str, Any]]]]:
    parser = Parser(Language(tree_sitter_java.language()))
    roots = {path: parser.parse(source.encode()).root_node for path, source in sources.items()}
    encoded = {path: source.encode() for path, source in sources.items()}

    def text(path: Path, node: Any) -> str:
        return encoded[path][node.start_byte:node.end_byte].decode() if node else ""

    def walk(node: Any):
        yield node
        for child in node.named_children:
            yield from walk(child)

    classes: dict[str, list[dict[str, Any]]] = {}
    file_types: dict[Path, dict[str, str]] = {}
    wildcard_imports: dict[Path, list[str]] = {}
    file_packages: dict[Path, str] = {}
    methods: dict[tuple[str, str, int], list[dict[str, Any]]] = {}
    for path, root in roots.items():
        package = next((text(path, child).removeprefix("package ").rstrip(";").strip()
                        for child in root.named_children if child.type == "package_declaration"), "")
        file_packages[path] = package
        imports = {}
        wildcard_imports[path] = []
        for child in root.named_children:
            if child.type != "import_declaration":
                continue
            name = text(path, child).removeprefix("import ").rstrip(";").strip()
            if not name.startswith("static ") and not name.endswith(".*"):
                imports[name.rsplit(".", 1)[-1]] = name
            elif not name.startswith("static ") and name.endswith(".*"):
                wildcard_imports[path].append(name[:-2])
        file_types[path] = imports
        for cls in root.named_children:
            if cls.type not in {"class_declaration", "interface_declaration"}:
                continue
            name = text(path, cls.child_by_field_name("name"))
            identity = f"{package}.{name}" if package else name
            body = cls.child_by_field_name("body")
            fields = {}
            for field in body.named_children if body else []:
                if field.type != "field_declaration":
                    continue
                field_type = re.sub(r"<.*", "", text(path, field.child_by_field_name("type"))).strip()
                for variable in field.named_children:
                    if variable.type == "variable_declarator":
                        fields[text(path, variable.child_by_field_name("name"))] = field_type
            record = {"path": path, "node": cls, "fields": fields, "identity": identity}
            classes.setdefault(identity, []).append(record)
            for method in body.named_children if body else []:
                if method.type != "method_declaration" or method.child_by_field_name("body") is None:
                    continue
                params = method.child_by_field_name("parameters")
                parameters = [child for child in params.named_children if child.type == "formal_parameter"] if params else []
                row = {**record, "method": method, "parameters": parameters}
                signature = (identity, text(path, method.child_by_field_name("name")), len(parameters))
                methods.setdefault(signature, []).append(row)

    def identity(path: Path, raw: str) -> str:
        raw = re.sub(r"<.*", "", raw).strip()
        if "." in raw:
            return raw
        if raw in file_types[path]:
            return file_types[path][raw]
        local = f"{file_packages[path]}.{raw}" if file_packages[path] else raw
        if local in classes:
            return local
        candidates = {f"{package}.{raw}" for package in wildcard_imports[path] if f"{package}.{raw}" in classes}
        return next(iter(candidates)) if len(candidates) == 1 else local

    implementations: dict[str, set[str]] = {}
    for name, rows in classes.items():
        for row in rows:
            interfaces = row["node"].child_by_field_name("interfaces")
            for child in walk(interfaces) if interfaces else []:
                if child.type == "type_identifier":
                    implementations.setdefault(identity(row["path"], text(row["path"], child)), set()).add(name)

    unique = {signature: rows[0] for signature, rows in methods.items() if len(rows) == 1}
    callers = {(*signature, row["method"].start_byte): row
               for signature, rows in methods.items() for row in rows}
    analysis = {**unique, **callers}

    def context(row: dict[str, Any]) -> tuple[dict[str, str], dict[str, Any], set[str]]:
        path, method = row["path"], row["method"]
        types = dict(row["fields"])
        values = {}
        assigned = set()
        for param in row["parameters"]:
            types[text(path, param.child_by_field_name("name"))] = text(path, param.child_by_field_name("type"))
        for child in walk(method.child_by_field_name("body")):
            if child.type == "local_variable_declaration":
                for variable in child.named_children:
                    if variable.type == "variable_declarator":
                        name = text(path, variable.child_by_field_name("name"))
                        types[name] = text(path, child.child_by_field_name("type"))
                        values[name] = variable.child_by_field_name("value")
            elif child.type == "assignment_expression":
                assigned.add(text(path, child.child_by_field_name("left")))
        return types, values, assigned

    contexts = {signature: context(row) for signature, row in analysis.items()}

    def candidate_targets(signature: tuple[Any, ...], call: Any) -> set[tuple[str, str, int]]:
        row = analysis[signature]
        path = row["path"]
        owner = text(path, call.child_by_field_name("object")).removeprefix("this.")
        types, _, _ = contexts[signature]
        declared = signature[0] if owner in {"", "this"} else identity(path, types.get(owner, ""))
        if declared not in classes:
            return set()
        candidates = implementations.get(declared, {declared})
        args = call.child_by_field_name("arguments")
        return {(candidate, text(path, call.child_by_field_name("name")), len(args.named_children) if args else 0)
                for candidate in candidates}

    def target(signature: tuple[Any, ...], call: Any) -> tuple[str, str, int] | None:
        candidates = candidate_targets(signature, call)
        if len(candidates) != 1:
            return None
        key = next(iter(candidates))
        return key if key in unique else None

    def parameter(signature: tuple[str, str, int], value: Any, seen: frozenset[str] = frozenset()) -> int | None:
        row = analysis[signature]
        path = row["path"]
        _, values, assigned = contexts[signature]
        name = text(path, value)
        names = [text(path, item.child_by_field_name("name")) for item in row["parameters"]]
        if name in assigned:
            return None
        if name in names:
            return names.index(name)
        if name in values and name not in seen:
            return parameter(signature, values[name], seen | {name})
        if value and value.type == "object_creation_expression" and text(path, value.child_by_field_name("type")).startswith("ProducerRecord"):
            args = value.child_by_field_name("arguments")
            return parameter(signature, args.named_children[0], seen) if args and args.named_children else None
        if value and value.type == "method_invocation" and text(path, value.child_by_field_name("name")) == "build":
            builder = text(path, value.child_by_field_name("object"))
            headers = []
            for child in walk(row["method"].child_by_field_name("body")):
                if child.type != "method_invocation" or text(path, child.child_by_field_name("name")) != "setHeader":
                    continue
                args = child.child_by_field_name("arguments")
                if not args or len(args.named_children) != 2 or text(path, args.named_children[0]) != "KafkaHeaders.TOPIC":
                    continue
                owner = text(path, child.child_by_field_name("object"))
                enclosing = child.parent
                while enclosing and enclosing.type not in {"variable_declarator", "expression_statement", "method_declaration"}:
                    enclosing = enclosing.parent
                if owner == builder or (enclosing and enclosing.type == "variable_declarator" and text(path, enclosing.child_by_field_name("name")) == builder):
                    headers.append(args.named_children[1])
            if len(headers) == 1:
                return parameter(signature, headers[0], seen)
        return None

    rules: dict[tuple[str, str, int], dict[int, set[tuple[Path, int, str]]]] = {}
    candidate_parameters: dict[tuple[str, str, int], set[int]] = {}
    for signature, row in callers.items():
        path = row["path"]
        types, _, _ = contexts[signature]
        for call in walk(row["method"].child_by_field_name("body")):
            if call.type == "method_invocation" and text(path, call.child_by_field_name("name")) == "send":
                owner = text(path, call.child_by_field_name("object")).removeprefix("this.")
                if identity(path, types.get(owner, "")) == "org.springframework.kafka.core.KafkaTemplate":
                    args = call.child_by_field_name("arguments")
                    index = parameter(signature, args.named_children[0]) if args and args.named_children else None
                    if index is not None:
                        candidate_parameters.setdefault(signature[:3], set()).add(index)
    for signature, row in unique.items():
        path = row["path"]
        types, _, _ = contexts[signature]
        for call in walk(row["method"].child_by_field_name("body")):
            if call.type != "method_invocation" or text(path, call.child_by_field_name("name")) != "send":
                continue
            owner = text(path, call.child_by_field_name("object")).removeprefix("this.")
            if identity(path, types.get(owner, "")) != "org.springframework.kafka.core.KafkaTemplate":
                continue
            args = call.child_by_field_name("arguments")
            index = parameter(signature, args.named_children[0]) if args and args.named_children else None
            if index is not None:
                rules.setdefault(signature, {}).setdefault(index, set()).add((path, call.start_point.row + 1, text(path, call)))

    # Each iteration adds a finite signature/parameter rule. Cycles cannot
    # create rules without a concrete Kafka send site.
    changed = True
    while changed:
        changed = False
        for signature, row in unique.items():
            for call in walk(row["method"].child_by_field_name("body")):
                if call.type != "method_invocation":
                    continue
                callee = target(signature, call)
                args = call.child_by_field_name("arguments")
                for index, evidence in list(rules.get(callee, {}).items()):
                    parameter_index = parameter(signature, args.named_children[index])
                    if parameter_index is None:
                        continue
                    records = rules.setdefault(signature, {}).setdefault(parameter_index, set())
                    previous = len(records)
                    records.update(evidence)
                    records.add((row["path"], call.start_point.row + 1, text(row["path"], call)))
                    changed |= len(records) != previous

    changed = True
    while changed:
        changed = False
        for signature, row in callers.items():
            for call in walk(row["method"].child_by_field_name("body")):
                if call.type != "method_invocation":
                    continue
                args = call.child_by_field_name("arguments")
                for callee in candidate_targets(signature, call):
                    for index in list(candidate_parameters.get(callee, set())):
                        forwarded = parameter(signature, args.named_children[index])
                        if forwarded is None:
                            continue
                        params = candidate_parameters.setdefault(signature[:3], set())
                        previous = len(params)
                        params.add(forwarded)
                        changed |= len(params) != previous

    calls: dict[Path, dict[int, dict[str, Any]]] = {}
    for signature, row in callers.items():
        for call in walk(row["method"].child_by_field_name("body")):
            if call.type != "method_invocation":
                continue
            callee = target(signature, call)
            candidates = candidate_targets(signature, call)
            if len(rules.get(callee, {})) > 1:
                calls.setdefault(row["path"], {})[call.start_byte] = {"unresolved": True}
                continue
            if not rules.get(callee) and candidates & candidate_parameters.keys():
                calls.setdefault(row["path"], {})[call.start_byte] = {"unresolved": True}
            for index, evidence in rules.get(callee, {}).items():
                calls.setdefault(row["path"], {})[call.start_byte] = {
                    "argument": call.child_by_field_name("arguments").named_children[index],
                    "helper_evidence": sorted(evidence),
                    "forwarded_parameter": parameter(signature, call.child_by_field_name("arguments").named_children[index]) is not None,
                }
    return roots, calls
