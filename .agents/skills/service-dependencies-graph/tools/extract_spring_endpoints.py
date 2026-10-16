"""Extract inbound Spring mappings from Java declarations, not matching text."""

from __future__ import annotations

import itertools
import json
import re
from typing import Any

from tree_sitter import Language, Parser
import tree_sitter_java


MAPPINGS = {"RequestMapping", "GetMapping", "PostMapping", "PutMapping", "DeleteMapping", "PatchMapping"}
GRAPHQL_MAPPINGS = {
    "QueryMapping": "QUERY",
    "MutationMapping": "MUTATION",
    "SubscriptionMapping": "SUBSCRIPTION",
    "DgsQuery": "QUERY",
    "DgsMutation": "MUTATION",
    "DgsSubscription": "SUBSCRIPTION",
    "DgsData": "FIELD",
    "SchemaMapping": "FIELD",
}


def extract_endpoints(source: str) -> dict[str, list[dict[str, Any]]]:
    encoded = source.encode("utf-8")
    tree = Parser(Language(tree_sitter_java.language())).parse(encoded)
    endpoints: list[dict[str, Any]] = []
    graphql: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []

    def text(node: Any) -> str:
        return encoded[node.start_byte:node.end_byte].decode("utf-8") if node else ""

    def walk(node: Any):
        yield node
        for child in node.named_children:
            yield from walk(child)

    def diagnostic(code: str, node: Any, message: str) -> None:
        diagnostics.append({"code": code, "line": node.start_point.row + 1, "message": message})

    def handler_context(method: Any) -> dict[str, Any]:
        parameters = method.child_by_field_name("parameters")
        return {"handler_line": method.start_point.row + 1,
                "handler_arity": sum(child.type in {"formal_parameter", "spread_parameter"}
                                     for child in parameters.named_children) if parameters is not None else 0}

    def annotations(node: Any) -> list[tuple[str, Any, dict[str, Any]]]:
        modifiers = next((child for child in node.named_children if child.type == "modifiers"), None)
        result = []
        for annotation in modifiers.named_children if modifiers else []:
            if annotation.type not in {"annotation", "marker_annotation"}:
                continue
            name = text(annotation.child_by_field_name("name")).rsplit(".", 1)[-1]
            arguments = annotation.child_by_field_name("arguments")
            values = {}
            for argument in arguments.named_children if arguments else []:
                if argument.type == "element_value_pair":
                    values[text(argument.child_by_field_name("key"))] = argument.child_by_field_name("value")
                else:
                    values["value"] = argument
            result.append((name, annotation, values))
        return result

    if tree.root_node.has_error:
        diagnostic("JAVA_PARSE_ERROR", tree.root_node, "Java syntax contains unsupported or incomplete declarations; invalid mappings are omitted")

    for owner in walk(tree.root_node):
        if owner.type not in {"class_declaration", "interface_declaration", "record_declaration"}:
            continue
        owner_annotations = annotations(owner)
        names = {name for name, _, _ in owner_annotations}
        body = owner.child_by_field_name("body")
        methods = [child for child in body.named_children if child.type == "method_declaration"] if body else []
        mapped_methods = [(method, [item for item in annotations(method) if item[0] in MAPPINGS]) for method in methods]
        graphql_methods = [(method, [item for item in annotations(method) if item[0] in GRAPHQL_MAPPINGS]) for method in methods]
        if "FeignClient" in names:
            continue

        # DGS and Spring for GraphQL providers are method-level declarations.
        # They do not use REST controller mappings, so extract them before the
        # REST provider guard below.  Keep nested @DgsData/@SchemaMapping
        # fields visible while marking their operation type as FIELD.
        for method, annotations_for_method in graphql_methods:
            if not annotations_for_method:
                continue
            if len(annotations_for_method) != 1 or method.has_error:
                diagnostic("AMBIGUOUS_GRAPHQL_MAPPING", method, "Invalid or multiple GraphQL provider annotations require review")
                continue
            name, annotation, arguments = annotations_for_method[0]
            operation_type = GRAPHQL_MAPPINGS[name]

            def literal_argument(keys: tuple[str, ...]) -> str | None:
                for key in keys:
                    node = arguments.get(key)
                    if node is None:
                        continue
                    # Keep this local and syntax based.  Expressions such as
                    # DgsConstants.QUERY.TYPE_NAME are handled separately.
                    if node.type == "string_literal":
                        try:
                            return json.loads(text(node))
                        except ValueError:
                            return None
                    return None
                return None

            def expression_tail(keys: tuple[str, ...]) -> str | None:
                for key in keys:
                    node = arguments.get(key)
                    if node is None:
                        continue
                    raw = text(node).strip().strip('"')
                    if raw:
                        # DGS generated constants use
                        # DgsConstants.QUERY.TYPE_NAME. Preserve the root
                        # type instead of returning the generic TYPE_NAME
                        # suffix.
                        for root in ("QUERY", "MUTATION", "SUBSCRIPTION"):
                            if re.search(rf"(?:^|\.){root}(?:\.|$)", raw, re.I):
                                return root.title()
                        if raw.rsplit(".", 1)[-1] == "TYPE_NAME" and "." in raw:
                            return raw.rsplit(".", 2)[-2]
                        return raw.rsplit(".", 1)[-1]
                return None

            field_arguments = ("field", "name", "value")
            explicit_field = any(key in arguments for key in field_arguments)
            field = literal_argument(field_arguments)
            if field is None and explicit_field:
                diagnostic("UNRESOLVED_GRAPHQL_MAPPING", annotation, "GraphQL field name contains an unresolved expression")
                continue
            field = field or text(method.child_by_field_name("name"))
            if not field:
                diagnostic("UNRESOLVED_GRAPHQL_MAPPING", annotation, "GraphQL field name could not be resolved")
                continue

            parent_type = literal_argument(("parentType", "typeName", "type"))
            if parent_type is None:
                parent_type = expression_tail(("parentType", "typeName", "type"))
            # DGS root annotations have no parentType.  Spring root mappings
            # also default from the annotation kind.  @DgsData/@SchemaMapping
            # needs a parent type to distinguish root from nested fields.
            if name in {"DgsData", "SchemaMapping"} and not parent_type:
                diagnostic("UNRESOLVED_GRAPHQL_MAPPING", annotation, "GraphQL field mapping has no resolvable parent type")
                continue
            if name in {"DgsData", "SchemaMapping"}:
                root_type = parent_type.upper() in {"QUERY", "MUTATION", "SUBSCRIPTION"}
                effective_type = parent_type.upper() if root_type else "FIELD"
            else:
                root_type = True
                effective_type = operation_type
                parent_type = parent_type or effective_type.title()
            graphql.append({
                "operation_type": effective_type,
                "operation_name": field,
                "field": field,
                "parent_type": parent_type,
                "root": root_type,
                "line": annotation.start_point.row + 1,
                "declaration": text(annotation),
                "provider_kind": "GRAPHQL",
                "controller": text(owner.child_by_field_name("name")),
                "handler": text(method.child_by_field_name("name")),
                **handler_context(method),
            })

        if not names & {"RestController", "Controller"}:
            if any(mapping for _, mapping in mapped_methods):
                diagnostic("UNRESOLVED_SPRING_PROVIDER", owner, "Mapped methods have no directly declared Controller/RestController; inherited or composed provider annotations require review")
            continue

        # Only constants belonging to this declaration are eligible. Unknown
        # imported/inherited constants remain unknown instead of losing prefixes.
        constants = {}
        for field in body.named_children if body else []:
            if field.type not in {"field_declaration", "constant_declaration"}:
                continue
            modifiers = next((child for child in field.named_children if child.type == "modifiers"), None)
            if "final" not in text(modifiers) and owner.type != "interface_declaration":
                continue
            for declaration in field.named_children:
                if declaration.type == "variable_declarator":
                    constants[text(declaration.child_by_field_name("name"))] = declaration.child_by_field_name("value")

        def values(node: Any, seen: frozenset[str] = frozenset()) -> list[str] | None:
            if node is None:
                return None
            if node.type == "string_literal":
                try:
                    return [json.loads(text(node))]
                except ValueError:
                    return None
            if node.type in {"element_value_array_initializer", "array_initializer"}:
                parts = [values(child, seen) for child in node.named_children]
                return [value for part in parts for value in part] if all(part is not None for part in parts) else None
            if node.type == "binary_expression" and text(node.child_by_field_name("operator")) == "+":
                left, right = values(node.child_by_field_name("left"), seen), values(node.child_by_field_name("right"), seen)
                return [a + b for a, b in itertools.product(left, right)] if left is not None and right is not None else None
            name = text(node)
            owner_name = text(owner.child_by_field_name("name"))
            if name.startswith(owner_name + "."):
                name = name[len(owner_name) + 1:]
            if name in constants and name not in seen:
                return values(constants[name], seen | {name})
            return None

        def mapping(item: tuple[str, Any, dict[str, Any]]) -> tuple[list[str], set[str]] | None:
            name, annotation, arguments = item
            paths = values(arguments.get("path", arguments.get("value"))) if {"path", "value"} & arguments.keys() else [""]
            if paths is None or any("${" in path or "#{" in path for path in paths):
                diagnostic("UNRESOLVED_SPRING_MAPPING", annotation, "Mapping path contains an unresolved constant or configuration expression")
                return None
            methods = {name.removesuffix("Mapping").upper()} if name != "RequestMapping" else set()
            if "method" in arguments:
                expression = arguments["method"]
                parts = expression.named_children if expression.type == "element_value_array_initializer" else [expression]
                methods = {text(part).rsplit(".", 1)[-1] for part in parts}
                if not methods <= {"GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"}:
                    diagnostic("UNRESOLVED_SPRING_MAPPING", annotation, "Mapping HTTP methods could not be resolved")
                    return None
            return paths, methods

        class_mappings = [item for item in owner_annotations if item[0] in MAPPINGS]
        if len(class_mappings) > 1:
            diagnostic("AMBIGUOUS_SPRING_MAPPING", owner, "Multiple mapping annotations on one controller require review")
            continue
        base = mapping(class_mappings[0]) if class_mappings else ([""], set())
        if base is None:
            continue
        for method, annotations_for_method in mapped_methods:
            if not annotations_for_method:
                continue
            if len(annotations_for_method) != 1 or method.has_error:
                diagnostic("AMBIGUOUS_SPRING_MAPPING", method, "Invalid or multiple method mappings require review")
                continue
            item = annotations_for_method[0]
            own = mapping(item)
            if own is None:
                continue
            paths, http_methods = own
            base_paths, base_methods = base
            # RequestMethodsRequestCondition.combine uses the union of both
            # declarations, unlike path composition. An intersection drops
            # valid mappings when class and handler specify different methods.
            effective_methods = http_methods | base_methods or {"ANY"}
            for prefix, suffix, http_method in itertools.product(base_paths, paths, sorted(effective_methods)):
                path = "/" + "/".join(part.strip("/") for part in (prefix, suffix) if part.strip("/"))
                endpoints.append({"path": path, "method": http_method, "line": item[1].start_point.row + 1,
                                  "declaration": text(item[1]), "provider_kind": "CONTROLLER",
                                  "controller": text(owner.child_by_field_name("name")), "handler": text(method.child_by_field_name("name")),
                                  **handler_context(method)})
    return {"endpoints": endpoints, "graphql": graphql, "diagnostics": diagnostics}
