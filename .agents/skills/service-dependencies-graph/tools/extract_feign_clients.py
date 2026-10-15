"""Read Feign service identities from parsed annotations, excluding comments."""
from __future__ import annotations

import json
from tree_sitter import Language, Parser
import tree_sitter_java


MAPPINGS = {"RequestMapping", "GetMapping", "PostMapping", "PutMapping", "DeleteMapping", "PatchMapping"}


def extract_feign_clients(source):
    encoded = source.encode()
    root = Parser(Language(tree_sitter_java.language())).parse(encoded).root_node
    results = []

    def text(node):
        return encoded[node.start_byte:node.end_byte].decode() if node else ''

    def walk(node):
        yield node
        for child in node.named_children:
            yield from walk(child)

    for node in walk(root):
        if node.type != 'annotation' or node.has_error or text(node.child_by_field_name('name')).rsplit('.', 1)[-1] != 'FeignClient':
            continue
        values = {}
        arguments = node.child_by_field_name('arguments')
        for item in arguments.named_children if arguments else []:
            if item.type == 'element_value_pair':
                values[text(item.child_by_field_name('key'))] = item.child_by_field_name('value')
            else:
                values['value'] = item
        def literal(key):
            item = values.get(key)
            if item and item.type == 'string_literal':
                try:
                    return json.loads(text(item))
                except ValueError:
                    pass
            return None
        # A configured URL overrides discovery by name; keep this boundary unresolved.
        direct_url = 'url' in values and literal('url') != ''
        alias = literal('name') or literal('value')
        if direct_url:
            alias = None
        operations = []
        # The Feign annotation is nested in the declaration's ``modifiers``
        # node.  The previous lookup searched that modifier list for the
        # interface/class body, so every real client silently produced zero
        # method contracts.  Walk to the declaration first, then inspect its
        # body.  Keep this structural lookup instead of scanning text so
        # comments and nested declarations cannot become operations.
        declaration = node.parent.parent if node.parent is not None else None
        body = next((child for child in declaration.named_children
                     if child.type in {"interface_body", "class_body"}), None) if declaration else None

        def annotations(owner):
            modifiers = next((child for child in owner.named_children if child.type == "modifiers"), None)
            result = []
            for annotation in modifiers.named_children if modifiers else []:
                if annotation.type not in {"annotation", "marker_annotation"}:
                    continue
                name = text(annotation.child_by_field_name("name")).rsplit('.', 1)[-1]
                arguments = annotation.child_by_field_name("arguments")
                values = {}
                for argument in arguments.named_children if arguments else []:
                    if argument.type == "element_value_pair":
                        values[text(argument.child_by_field_name("key"))] = argument.child_by_field_name("value")
                    else:
                        values["value"] = argument
                result.append((name, annotation, values))
            return result

        def literal_value(item):
            if item is None or item.type != "string_literal":
                return None
            try:
                return json.loads(text(item))
            except ValueError:
                return None

        def mapping_values(item):
            if item is None:
                return [""]
            if item.type == "string_literal":
                value = literal_value(item)
                return [value] if value is not None else None
            if item.type in {"element_value_array_initializer", "array_initializer"}:
                values = []
                for child in item.named_children:
                    child_values = mapping_values(child)
                    if child_values is None:
                        return None
                    values.extend(child_values)
                return values
            return None

        if body:
            for method in body.named_children:
                if method.type != "method_declaration":
                    continue
                mapped = [item for item in annotations(method) if item[0] in MAPPINGS]
                if len(mapped) != 1:
                    continue
                mapping_name, mapping_annotation, mapping_args = mapped[0]
                path_node = mapping_args.get("path", mapping_args.get("value"))
                paths = mapping_values(path_node)
                if paths is None or any("${" in path or "#{" in path for path in paths):
                    continue
                methods = {mapping_name.removesuffix("Mapping").upper()} if mapping_name != "RequestMapping" else {"ANY"}
                if "method" in mapping_args:
                    method_node = mapping_args["method"]
                    parts = method_node.named_children if method_node.type in {"element_value_array_initializer", "array_initializer"} else [method_node]
                    methods = {text(part).rsplit('.', 1)[-1] for part in parts}
                    if not methods <= {"GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"}:
                        continue
                for method_name in sorted(methods):
                    for path_name in paths:
                        operations.append({
                            "method": method_name, "path": "/" + path_name.strip("/"),
                            "line": mapping_annotation.start_point.row + 1,
                            "declaration": text(mapping_annotation)[:500],
                        })
        results.append({'alias': alias, 'line': node.start_point.row + 1,
                        'reason': 'Feign URL overrides service discovery' if direct_url else 'Feign name/value needs constant or configuration resolution' if not alias or '${' in alias else '',
                        'declaration': 'FeignClient service identity ' + (alias if alias and '${' not in alias else '[unresolved]'),
                        'operations': operations})
    return results
