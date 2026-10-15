"""Find HTTP/GraphQL/WebSocket endpoints at parsed invocation sites."""

from __future__ import annotations

import json
import re
from typing import Any

from tree_sitter import Language, Parser
import tree_sitter_typescript


def extract_rtk_base_query_wrappers(source: str) -> dict[str, dict[str, Any]]:
    """Find exported typed wrappers that forward the declared HTTP URL/method.

    Custom RTK Query factories have no standard URL semantics. This narrow
    rule supports a BaseQueryFn factory that returns an arrow function and
    passes ``baseUrl + url`` with an unchanged ``method`` to a client. It does
    not assume the client's default method from the wrapper's name.
    """
    encoded = source.encode("utf-8")
    root = Parser(Language(tree_sitter_typescript.language_typescript())).parse(encoded).root_node

    def text(node: Any) -> str:
        return encoded[node.start_byte:node.end_byte].decode("utf-8") if node else ""

    def walk(node: Any):
        yield node
        for child in node.named_children:
            yield from walk(child)

    typed_import = bool(re.search(
        r'import\s*(?:type\s*)?\{[^}]*\bBaseQueryFn\b[^}]*\}\s*from\s*["\']@reduxjs/toolkit/query(?:/react)?["\']',
        source,
    ))
    if not typed_import or root.has_error:
        return {}
    axios_names: set[str] = set()
    for import_node in root.named_children:
        if import_node.type != "import_statement" or text(import_node.child_by_field_name("source")).strip('"\'') != "axios":
            continue
        clause = next((item for item in import_node.named_children if item.type == "import_clause"), None)
        if clause is not None:
            axios_names.update(text(item) for item in clause.named_children if item.type == "identifier")
    axios_clients = set(axios_names)
    for declaration in walk(root):
        if declaration.type != "variable_declarator":
            continue
        expression = declaration.child_by_field_name("value")
        if expression is None or expression.type != "call_expression":
            continue
        function = expression.child_by_field_name("function")
        if function is not None and function.type == "member_expression" and text(function.child_by_field_name("object")) in axios_names and text(function.child_by_field_name("property")) == "create":
            axios_clients.add(text(declaration.child_by_field_name("name")))
    result: dict[str, dict[str, Any]] = {}
    for declaration in walk(root):
        if declaration.type != "variable_declarator":
            continue
        name = text(declaration.child_by_field_name("name"))
        factory = declaration.child_by_field_name("value")
        if factory is None or factory.type != "arrow_function" or "BaseQueryFn" not in text(factory.child_by_field_name("return_type")):
            continue
        returned = factory.child_by_field_name("body")
        if returned is None or returned.type != "arrow_function":
            continue
        exported = declaration.parent and declaration.parent.parent and declaration.parent.parent.type == "export_statement"
        if not exported:
            continue
        parameters = text(factory.child_by_field_name("parameters"))
        returned_parameters = text(returned.child_by_field_name("parameters"))
        if "baseUrl" not in parameters or not re.search(r'\{[^}]*\burl\b[^}]*\bmethod\b', returned_parameters):
            continue
        for call in walk(returned):
            if call.type != "call_expression":
                continue
            arguments = call.child_by_field_name("arguments")
            config = arguments.named_children[0] if arguments and arguments.named_children else None
            if config is None or config.type != "object":
                continue
            pairs = {text(item.child_by_field_name("key")): item.child_by_field_name("value")
                     for item in config.named_children if item.type == "pair"}
            for item in config.named_children:
                if item.type == "shorthand_property_identifier":
                    pairs[text(item)] = item
            url, method = pairs.get("url"), pairs.get("method")
            if url is None or method is None or text(method) != "method":
                continue
            if url.type != "binary_expression" or text(url.child_by_field_name("operator")) != "+":
                continue
            if text(url.child_by_field_name("left")) != "baseUrl" or text(url.child_by_field_name("right")) != "url":
                continue
            function = call.child_by_field_name("function")
            is_axios = text(function) in axios_clients or (
                function is not None and function.type == "member_expression"
                and text(function.child_by_field_name("object")) in axios_clients
                and text(function.child_by_field_name("property")) == "request"
            )
            result[name] = {
                "protocol": "REST", "base_field": "baseUrl", "join": "CONCAT",
                "default_method": "GET" if is_axios else "ANY",
                "assertion_status": "CONFIRMED" if is_axios else "INFERRED",
                "line": declaration.start_point.row + 1,
                "declaration": text(call)[:500],
            }
    return result


def extract_interfaces(source: str, *, tsx: bool = False,
                       external_values: dict[str, str] | None = None,
                       external_base_queries: dict[str, dict[str, Any]] | None = None,
                       external_rtk_apis: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    encoded = source.encode("utf-8")
    language = tree_sitter_typescript.language_tsx() if tsx else tree_sitter_typescript.language_typescript()
    root = Parser(Language(language)).parse(encoded).root_node
    operations: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    rtk_apis: dict[str, dict[str, Any]] = {}

    def text(node: Any) -> str:
        return encoded[node.start_byte:node.end_byte].decode("utf-8") if node else ""

    parents: dict[int, Any] = {}

    def walk(node: Any, parent: Any = None):
        if parent is not None:
            parents[id(node)] = parent
        yield node
        for child in node.named_children:
            yield from walk(child, node)

    scope_types = {"function_declaration", "function", "arrow_function", "method_definition", "method_declaration"}

    def enclosing_scope(node: Any) -> Any:
        current = node
        while current is not None:
            if current.type in scope_types:
                return current
            current = parents.get(id(current))
        return root

    # File-global names are safe only if uniquely declared. A shadowed variable
    # cannot establish which URL a call receives without a scope resolver.
    declarations: dict[str, list[Any]] = {}
    object_declarations: dict[str, list[Any]] = {}
    scoped_declarations: dict[tuple[int, str], list[Any]] = {}
    scoped_objects: dict[tuple[int, str], list[Any]] = {}
    for node in walk(root):
        if node.type == "variable_declarator":
            name_node = node.child_by_field_name("name")
            name = text(name_node)
            value_node = node.child_by_field_name("value")
            declarations.setdefault(name, []).append(value_node)
            scope_id = id(enclosing_scope(node))
            scoped_declarations.setdefault((scope_id, name), []).append(value_node)
            if value_node is not None and value_node.type == "object":
                object_declarations.setdefault(name, []).append(value_node)
                scoped_objects.setdefault((scope_id, name), []).append(value_node)
            # Destructuring declarations (for example ``const {url} =
            # props``) also shadow file-global constants. Track each bound
            # property as unknown unless a later flow can prove its value.
            if name_node is not None and name_node.type == "object_pattern":
                for binding in name_node.named_children:
                    if binding.type == "shorthand_property_identifier_pattern":
                        binding_name = text(binding)
                    elif binding.type == "pair":
                        binding_name = text(binding.child_by_field_name("value"))
                    else:
                        binding_name = ""
                    if re.fullmatch(r"[A-Za-z_$][\w$]*", binding_name):
                        scoped_declarations.setdefault((scope_id, binding_name), []).append(None)
        if node.type in scope_types:
            parameters = node.child_by_field_name("parameters")
            for parameter in parameters.named_children if parameters else ():
                # A function parameter shadows any same-named file-global
                # constant. Record the shadow without evaluating its value.
                parameter_name = text(parameter).split(":", 1)[0].strip()
                if re.fullmatch(r"[A-Za-z_$][\w$]*", parameter_name):
                    scoped_declarations.setdefault((id(node), parameter_name), []).append(None)
    constants = {name: values[0] for name, values in declarations.items() if len(values) == 1}
    objects = {name: values[0] for name, values in object_declarations.items() if len(values) == 1}

    # Resolve a small, bounded class of local URL helpers.  These helpers are
    # source declarations, but a feature flag or runtime argument can select
    # one of several returned paths.  Keep every literal branch and mark the
    # resulting operation as inferred so a provider join cannot be reported as
    # a confirmed runtime route.
    helper_values: dict[str, tuple[str, ...]] = {}
    rest_wrappers: dict[str, str] = {}
    for node in walk(root):
        if node.type == "function_declaration":
            name = text(node.child_by_field_name("name"))
            body = node.child_by_field_name("body")
        elif node.type == "variable_declarator":
            name = text(node.child_by_field_name("name"))
            value_node = node.child_by_field_name("value")
            body = value_node if value_node is not None and value_node.type in {"arrow_function", "function"} else None
        else:
            continue
        if not name or body is None:
            continue
        body_text = re.sub(r"//[^\n]*|/\*.*?\*/", "", text(body), flags=re.S)
        literals = sorted({match.group(2) for match in re.finditer(r"([\"'])(/api/[^\"']*)\1", body_text)})
        if literals:
            helper_values[name] = tuple(literals)
        methods = [method.upper() for method in ("get", "post", "put", "delete", "patch", "head", "options")
                   if re.search(r"\.\s*" + method + r"\s*\(", body_text)]
        if methods and name:
            # A local wrapper can carry a URL argument into the HTTP client.
            # Keep only one method when the body is consistent; mixed methods
            # remain unresolved at the wrapper call site.
            if len(set(methods)) == 1:
                rest_wrappers[name] = methods[0]

    # A local wrapper that constructs an Apollo/GraphQL/WebSocket client is a
    # supported call boundary. Propagate the protocol through local helper
    # calls so a public subscribe function can carry a literal URL to a lower
    # level SockJS factory. Imported wrappers remain unresolved.
    wrappers: dict[str, str] = {}
    for _ in range(4):
        changed = False
        known_websocket = tuple(name for name, protocol in wrappers.items() if protocol == "WEBSOCKET")
        for node in walk(root):
            if node.type == "function_declaration":
                body = text(node.child_by_field_name("body"))
                name = text(node.child_by_field_name("name"))
            elif node.type == "variable_declarator":
                value_node = node.child_by_field_name("value")
                if value_node is None or value_node.type not in {"arrow_function", "function"}:
                    name = text(node.child_by_field_name("name"))
                    body = text(value_node)
                    if name and "graphql" in name.lower() and any(token in body for token in ("getWrappedGraphQLQuery", "originalQueryGraphQL")):
                        if wrappers.get(name) != "GRAPHQL":
                            wrappers[name] = "GRAPHQL"
                            changed = True
                    continue
                body = text(value_node)
                name = text(node.child_by_field_name("name"))
            else:
                continue
            if not name:
                continue
            if "HttpLink" in body or "ApolloClient" in body or "GraphQLClient" in body:
                protocol = "GRAPHQL"
            elif ("WebSocketLink" in body or "SubscriptionClient" in body or
                  "SockJS" in body or "Stomp.over" in body or
                  any(re.search(r"\b" + re.escape(call) + r"\s*\(", body) for call in known_websocket)):
                protocol = "WEBSOCKET"
            else:
                continue
            if wrappers.get(name) != protocol:
                wrappers[name] = protocol
                changed = True
        if not changed:
            break

    wrapper_scopes: set[int] = set()
    wrapper_ranges: list[tuple[int, int]] = []
    for node in walk(root):
        if node.type != "variable_declarator":
            continue
        value_node = node.child_by_field_name("value")
        name = text(node.child_by_field_name("name"))
        if value_node is not None and value_node.type in {"arrow_function", "function"} and name in wrappers:
            wrapper_scopes.add(id(value_node))
            wrapper_ranges.append((value_node.start_byte, value_node.end_byte))

    def inside_wrapper(node: Any) -> bool:
        if any(start <= node.start_byte <= end for start, end in wrapper_ranges):
            return True
        current = node
        while current is not None:
            if id(current) in wrapper_scopes:
                return True
            current = parents.get(id(current))
        return False

    def value(node: Any, seen: frozenset[str] = frozenset(), context: Any = None) -> str | None:
        if node is None:
            return None
        context = context or node
        raw = text(node)
        if node.type == "string":
            if raw.startswith('"'):
                try:
                    return json.loads(raw)
                except ValueError:
                    return None
            return raw[1:-1] if "\\" not in raw else None
        if node.type in {"identifier", "shorthand_property_identifier", "shorthand_property_identifier_pattern"} and raw not in seen:
            scope_id = id(enclosing_scope(context))
            scoped = scoped_declarations.get((scope_id, raw), [])
            target = scoped[0] if len(scoped) == 1 else (constants.get(raw) if not scoped else None)
            if target is not None:
                return value(target, seen | {raw}, context)
            if external_values and raw in external_values:
                return external_values[raw]
        if node.type == "member_expression":
            object_node = node.child_by_field_name("object")
            property_node = node.child_by_field_name("property")
            object_name, property_name = text(object_node), text(property_node)
            scope_id = id(enclosing_scope(context))
            scoped_object_values = scoped_objects.get((scope_id, object_name), [])
            object_node = scoped_object_values[0] if len(scoped_object_values) == 1 else objects.get(object_name)
            if object_node is not None and property_name:
                for pair in object_node.named_children:
                    if pair.type != "pair" or text(pair.child_by_field_name("key")).strip("\"'") != property_name:
                        continue
                    return value(pair.child_by_field_name("value"), seen | {object_name + "." + property_name}, context)
        if node.type == "template_string":
            parts = []
            cursor = node.start_byte + 1
            for child in node.named_children:
                if child.type != "template_substitution":
                    continue
                parts.append(encoded[cursor:child.start_byte].decode("utf-8"))
                expression = child.named_children[0] if child.named_children else None
                resolved = value(expression, seen, context)
                # Preserve a named dynamic path segment; do not evaluate code.
                if resolved is None:
                    name = text(expression)
                    if not re.fullmatch(r"[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*", name):
                        return None
                    resolved = "{" + name + "}"
                parts.append(resolved)
                cursor = child.end_byte
            parts.append(encoded[cursor:node.end_byte - 1].decode("utf-8"))
            return "".join(parts)
        if node.type == "binary_expression" and text(node.child_by_field_name("operator")) == "+":
            left = value(node.child_by_field_name("left"), seen, context)
            right = value(node.child_by_field_name("right"), seen, context)
            return left + right if left is not None and right is not None else None
        return None

    def possible_values(node: Any, seen: frozenset[str] = frozenset(), context: Any = None) -> list[str]:
        """Return bounded literal alternatives for one request expression."""
        if node is None:
            return []
        context = context or node
        raw = text(node)
        if node.type == "call_expression":
            function_node = node.child_by_field_name("function")
            function_name = text(function_node)
            if function_node is not None and function_node.type == "member_expression":
                property_name = text(function_node.child_by_field_name("property"))
                if property_name == "replace":
                    base = possible_values(function_node.child_by_field_name("object"), seen, context)
                    arguments_node = node.child_by_field_name("arguments")
                    arguments = arguments_node.named_children if arguments_node else []
                    if base and len(arguments) >= 2:
                        pattern = text(arguments[0]).strip("\"'")
                        if pattern.startswith("/") and pattern.count("/") >= 2:
                            pattern = pattern[1:pattern.rfind("/")]
                        replacement = possible_values(arguments[1], seen, context)
                        if not replacement:
                            expression_name = text(arguments[1])
                            replacement = ["{" + expression_name + "}"] if re.fullmatch(
                                r"[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*", expression_name) else []
                        if replacement:
                            return [item.replace(pattern, replacement_value, 1)
                                    for item in base for replacement_value in replacement]
            if function_node is not None and function_node.type == "identifier" and function_name in helper_values:
                return list(helper_values[function_name])
        if node.type == "template_string":
            alternatives = [""]
            cursor = node.start_byte + 1
            for child in node.named_children:
                if child.type != "template_substitution":
                    continue
                literal = encoded[cursor:child.start_byte].decode("utf-8")
                nested = child.named_children[0] if child.named_children else None
                values = possible_values(nested, seen, context) or ([value(nested, seen, context)] if value(nested, seen, context) is not None else [])
                if not values:
                    expression_name = text(nested)
                    if re.fullmatch(r"[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*", expression_name):
                        values = ["{" + expression_name + "}"]
                    else:
                        return []
                alternatives = [prefix + literal + item for prefix in alternatives for item in values]
                cursor = child.end_byte
            suffix = encoded[cursor:node.end_byte - 1].decode("utf-8")
            return [item + suffix for item in alternatives]
        if node.type == "binary_expression" and text(node.child_by_field_name("operator")) == "+":
            left = possible_values(node.child_by_field_name("left"), seen, context)
            right = possible_values(node.child_by_field_name("right"), seen, context)
            return [a + b for a in left for b in right]
        if node.type in {"identifier", "shorthand_property_identifier", "shorthand_property_identifier_pattern"}:
            name = raw
            if name in seen:
                return []
            scope_id = id(enclosing_scope(context))
            scoped = scoped_declarations.get((scope_id, name), [])
            target = scoped[0] if len(scoped) == 1 else (constants.get(name) if not scoped else None)
            if target is not None:
                return possible_values(target, seen | {name}, context)
        resolved = value(node, seen, context)
        return [resolved] if resolved is not None else []

    def properties(node: Any) -> dict[str, Any]:
        if node is None or node.type != "object":
            return {}
        result: dict[str, Any] = {}
        for child in node.named_children:
            if child.type == "pair":
                result[text(child.child_by_field_name("key")).strip("\"'")] = child.child_by_field_name("value")
            elif child.type == "shorthand_property_identifier":
                result[text(child)] = child
        return result

    imported_symbols: dict[str, tuple[str, str]] = {}
    for import_node in root.named_children:
        if import_node.type != "import_statement":
            continue
        module_node = import_node.child_by_field_name("source")
        module = value(module_node)
        if not module:
            continue
        for item in walk(import_node):
            if item.type != "import_specifier":
                continue
            imported_name = text(item.child_by_field_name("name"))
            local_name = text(item.child_by_field_name("alias")) or imported_name
            imported_symbols[local_name] = (module, imported_name)

    create_api_names = {name for name, (module, imported) in imported_symbols.items()
                        if module in {"@reduxjs/toolkit/query", "@reduxjs/toolkit/query/react"}
                        and imported == "createApi"}
    graphql_base_names = {name for name, (module, imported) in imported_symbols.items()
                          if module == "@rtk-query/graphql-request-base-query"
                          and imported == "graphqlRequestBaseQuery"}
    fetch_base_names = {name for name, (module, imported) in imported_symbols.items()
                        if module in {"@reduxjs/toolkit/query", "@reduxjs/toolkit/query/react"}
                        and imported == "fetchBaseQuery"}

    def unwrap_expression(node: Any) -> Any:
        """Unwrap the expression wrappers used by TypeScript arrow returns."""
        while node is not None and node.type in {
                "parenthesized_expression", "as_expression", "satisfies_expression",
        }:
            children = node.named_children
            node = children[0] if children else None
        return node

    def rtk_query_operations(create_call: Any, inherited: dict[str, Any] | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Extract static RTK Query endpoint declarations.

        ``createApi`` keeps the HTTP client configuration and endpoint paths in
        one AST object.  Reading that declaration is stronger evidence than
        searching for ``/api`` strings, and it also covers relative endpoint
        paths that are joined to an ``axiosBaseQuery`` base URL.  Runtime
        expressions remain diagnostics and never become fabricated paths.
        """
        found: list[dict[str, Any]] = []
        unresolved: list[dict[str, Any]] = []
        args = create_call.child_by_field_name("arguments")
        config = unwrap_expression(args.named_children[0]) if args and args.named_children else None
        config_props = properties(config)
        base_pair = config_props.get("baseQuery")
        binding = dict(inherited or {})
        base_values: list[str] = list(binding.get("paths", []))
        if base_pair is not None:
            base_call = unwrap_expression(base_pair)
            if base_call is not None and base_call.type == "call_expression":
                base_args = base_call.child_by_field_name("arguments")
                base_config = unwrap_expression(base_args.named_children[0]) if base_args and base_args.named_children else None
                base_props = properties(base_config)
                base_function = text(base_call.child_by_field_name("function"))
                if base_function in graphql_base_names:
                    binding = {"protocol": "GRAPHQL", "base_field": "url", "default_method": "POST", "join": "TRANSPORT"}
                elif base_function in fetch_base_names:
                    binding = {"protocol": "REST", "base_field": "baseUrl", "default_method": "GET", "join": "URL"}
                else:
                    binding = dict((external_base_queries or {}).get(base_function, {}))
                base_node = base_props.get(binding.get("base_field", ""))
                base_values = possible_values(base_node, context=create_call) if base_node is not None else []
                if not base_values and base_node is not None:
                    resolved = value(base_node, context=create_call)
                    if resolved:
                        base_values = [resolved]
                binding["paths"] = base_values
                binding["supporting_evidence"] = [*binding.get("supporting_evidence", []), {
                    "line": base_call.start_point.row + 1, "declaration": text(base_call)[:500],
                    "extractor": "web-rtk-api-base-query",
                }]
                if binding.get("assertion_status") == "INFERRED":
                    unresolved.append({"line": base_call.start_point.row + 1,
                                       "message": "Custom RTK base query forwards a URL and method to a client with unresolved HTTP identity"})

        # Keep local API aliases for injectEndpoints and same-repository
        # imported APIs. A URL-only descriptor cannot establish runtime use.
        parent = create_call.parent
        if parent is not None and parent.type == "variable_declarator" and binding and base_values:
            rtk_apis[text(parent.child_by_field_name("name"))] = binding

        endpoint_fn = unwrap_expression(config_props.get("endpoints"))
        endpoint_object = None
        if endpoint_fn is not None and endpoint_fn.type in {"arrow_function", "function"}:
            endpoint_body = unwrap_expression(endpoint_fn.child_by_field_name("body"))
            endpoint_object = endpoint_body if endpoint_body is not None and endpoint_body.type == "object" else None
        if endpoint_object is None:
            return found, unresolved

        def join_path(base: str, path: str) -> str:
            if not path:
                return base
            if path.startswith("http://") or path.startswith("https://"):
                return path
            if not base:
                return path
            if binding.get("join") == "CONCAT":
                return base + path
            return base.rstrip("/") + "/" + path.lstrip("/")

        for endpoint in endpoint_object.named_children:
            if endpoint.type != "pair":
                continue
            endpoint_name = text(endpoint.child_by_field_name("key"))
            endpoint_call = endpoint.child_by_field_name("value")
            if endpoint_call is None or endpoint_call.type != "call_expression":
                continue
            endpoint_fn_node = endpoint_call.child_by_field_name("function")
            if endpoint_fn_node is None or endpoint_fn_node.type != "member_expression":
                continue
            kind = text(endpoint_fn_node.child_by_field_name("property"))
            if kind not in {"query", "mutation"}:
                continue
            endpoint_args = endpoint_call.child_by_field_name("arguments")
            endpoint_config = unwrap_expression(endpoint_args.named_children[0]) if endpoint_args and endpoint_args.named_children else None
            endpoint_props = properties(endpoint_config)
            query_fn = unwrap_expression(endpoint_props.get("query"))
            query_body = unwrap_expression(query_fn.child_by_field_name("body")) if query_fn is not None and query_fn.type in {"arrow_function", "function"} else None
            query_props = properties(query_body)
            url_node = query_props.get("url")
            method_node = query_props.get("method")
            if binding.get("protocol") == "GRAPHQL" and base_values and "document" in query_props:
                document_node = query_props["document"]
                document = value(document_node, context=endpoint_call)
                if document is None:
                    unresolved.append({"line": endpoint_call.start_point.row + 1,
                                       "message": f"RTK GraphQL endpoint {endpoint_name} has a dynamic or unsupported document"})
                for base in base_values:
                    if not base.startswith("/api/"):
                        continue
                    found.append({"path": base, "protocol": "GRAPHQL", "method": "POST",
                                  "line": endpoint_call.start_point.row + 1,
                                  "declaration": text(endpoint_call)[:500],
                                  "assertion_status": "CONFIRMED", "endpoint_name": endpoint_name,
                                  "supporting_evidence": binding.get("supporting_evidence", []),
                                  **({"graphql_document": document} if document is not None else {})})
                continue
            paths = possible_values(url_node, context=endpoint_call) if url_node is not None else []
            if not paths and url_node is not None:
                resolved = value(url_node, context=endpoint_call)
                if resolved:
                    paths = [resolved]
            methods = possible_values(method_node, context=endpoint_call) if method_node is not None else []
            if not methods and method_node is None:
                methods = [binding.get("default_method", "ANY")]
            methods = [item.upper() for item in methods]
            if not paths or not base_values or not binding or not methods:
                unresolved.append({
                    "line": endpoint_call.start_point.row + 1,
                    "message": f"RTK Query endpoint {endpoint_name} has no statically bound base URL or path",
                })
                continue
            declarations = text(endpoint_call)[:500]
            for base in base_values:
                for path in paths:
                    joined = join_path(base, path)
                    if not joined.startswith("/api/") and not joined.startswith("http://") and not joined.startswith("https://"):
                        unresolved.append({
                            "line": endpoint_call.start_point.row + 1,
                            "message": f"RTK Query endpoint {endpoint_name} resolved outside the supported API path boundary: {joined}",
                        })
                        continue
                    for method_value in methods:
                        found.append({
                            "path": joined,
                            "protocol": "REST",
                            "method": method_value,
                            "line": endpoint_call.start_point.row + 1,
                            "declaration": declarations,
                            "assertion_status": "INFERRED" if len(base_values) * len(paths) * len(methods) > 1 or method_value == "ANY" or binding.get("assertion_status") == "INFERRED" else "CONFIRMED",
                            "conditional": len(base_values) * len(paths) * len(methods) > 1 or method_value == "ANY",
                            "endpoint_name": endpoint_name,
                            "supporting_evidence": binding.get("supporting_evidence", []),
                        })
        return found, unresolved

    for node in walk(root):
        if node.type not in {"call_expression", "new_expression"}:
            continue
        function = node.child_by_field_name("function") or node.child_by_field_name("constructor")
        # TypeScript permits ``await queryGraphql<T>(...)``. Tree-sitter
        # attaches the await expression as the call's function, so unwrap it
        # before protocol and wrapper matching.
        if function is not None and function.type == "await_expression":
            function = function.named_children[0] if function.named_children else function
        function_name = text(function)
        leaf = function_name.rsplit(".", 1)[-1]
        args = node.child_by_field_name("arguments")
        arguments = args.named_children if args else []
        protocol, method, argument = None, None, None
        # SockJS is the transport used by the checked-in STOMP client.  The
        # outer ``Stomp.over(...)`` call carries no endpoint itself; the
        # nested ``new SockJS(url)`` expression is the static boundary.
        if leaf in {"WebSocket", "WebSocketLink", "GraphQLWsLink", "SockJS", "EventSource"}:
            protocol = "WEBSOCKET"
            argument = arguments[0] if arguments else None
            config = properties(argument)
            argument = config.get("url", config.get("uri", argument))
        elif leaf == "over" and function and function.type == "member_expression":
            # stompjs exposes ``Stomp.over(new SockJS(url))``. The outer
            # call is the client boundary, while the nested SockJS
            # constructor carries the endpoint expression.
            object_name = text(function.child_by_field_name("object"))
            if object_name.rsplit(".", 1)[-1] in {"Stomp", "stomp"}:
                protocol = "WEBSOCKET"
                argument = arguments[0] if arguments else None
                if argument is not None and argument.type in {"new_expression", "call_expression"}:
                    nested_function = argument.child_by_field_name("constructor") or argument.child_by_field_name("function")
                    if text(nested_function).rsplit(".", 1)[-1] == "SockJS":
                        nested_args = argument.child_by_field_name("arguments")
                        argument = nested_args.named_children[0] if nested_args and nested_args.named_children else None
                config = properties(argument)
                argument = config.get("url", config.get("uri", argument))
        elif leaf == "Client" and node.type == "new_expression":
            # @stomp/stompjs uses ``new Client({ brokerURL })``. Require the
            # brokerURL/webSocketFactory property so ordinary classes named
            # Client do not become false WebSocket boundaries.
            config = properties(arguments[0] if arguments else None)
            if "brokerURL" in config or "webSocketFactory" in config:
                protocol = "WEBSOCKET"
                argument = config.get("brokerURL", config.get("webSocketFactory"))
        elif leaf in {"HttpLink", "createHttpLink", "GraphQLClient"} or function_name in graphql_base_names:
            protocol = "GRAPHQL"
            argument = arguments[0] if arguments else None
            config = properties(argument)
            argument = config.get("uri", config.get("url", argument))
            # graphql-request's RTK base query issues POST requests.  Other
            # GraphQL clients keep the historical ANY method marker because
            # their transport method is not stated at this invocation site.
            if function_name in graphql_base_names:
                method = "POST"
        elif leaf.lower() in {"get", "post", "put", "delete", "patch", "head", "options"} and function and function.type == "member_expression":
            protocol, method = "REST", leaf.upper()
            argument = arguments[0] if arguments else None
        elif function_name in {"fetch", "axios"} or leaf == "request":
            protocol = "REST"
            first = arguments[0] if arguments else None
            config = properties(first) or properties(arguments[1] if len(arguments) > 1 else None)
            argument = config.get("url", first)
            method = (value(config.get("method")) or ("GET" if function_name == "fetch" else "ANY")).upper()
        elif function and function.type == "identifier" and function_name in wrappers:
            protocol = wrappers[function_name]
            argument = arguments[0] if arguments else None
            config = properties(argument)
            argument = config.get("url", config.get("uri", argument))
        elif function and function.type == "identifier" and function_name in rest_wrappers:
            protocol, method = "REST", rest_wrappers[function_name]
            argument = arguments[0] if arguments else None
        if not protocol:
            if function_name in create_api_names:
                # RTK Query endpoint declarations are nested under createApi
                # and are not invocation expressions.
                rtk_operations, rtk_unresolved = rtk_query_operations(node)
                operations.extend(rtk_operations)
                diagnostics.extend({"code": "UNRESOLVED_WEB_ENDPOINT", **item} for item in rtk_unresolved)
            elif leaf == "injectEndpoints" and function is not None and function.type == "member_expression":
                api_name = text(function.child_by_field_name("object"))
                binding = rtk_apis.get(api_name, (external_rtk_apis or {}).get(api_name))
                rtk_operations, rtk_unresolved = rtk_query_operations(node, binding)
                operations.extend(rtk_operations)
                diagnostics.extend({"code": "UNRESOLVED_WEB_ENDPOINT", **item} for item in rtk_unresolved)
            continue
        # Resolve identifiers in the lexical scope of this call. This keeps
        # repeated local names such as ``queryUrl`` distinct across functions.
        urls = possible_values(argument, context=node)
        if not urls:
            resolved = value(argument, context=node)
            urls = [resolved] if resolved else []
        if urls and all(url.startswith("/api/") for url in urls):
            # ``new SockJS(...)`` is the transport nested inside
            # ``Stomp.over(...)``. Record the outer STOMP boundary once.
            if leaf == "SockJS":
                parent = parents.get(id(node))
                nested_in_stomp = False
                while parent is not None:
                    if parent.type == "call_expression":
                        parent_function = parent.child_by_field_name("function")
                        if text(parent_function).rsplit(".", 1)[-1] == "over":
                            nested_in_stomp = True
                            break
                    parent = parents.get(id(parent))
                if nested_in_stomp:
                    continue
            for url in sorted(set(urls)):
                operations.append({"path": url, "protocol": protocol, "method": method or "ANY",
                                   "line": node.start_point.row + 1, "declaration": text(node)[:500],
                                   "assertion_status": "INFERRED" if len(set(urls)) > 1 else "CONFIRMED",
                                   "conditional": len(set(urls)) > 1})
        elif argument is not None and (
                "/api/" in text(argument)
                or protocol != "REST"
                or function_name in {"fetch", "axios"}
                # Keep dynamic REST helpers visible as unresolved evidence.
                # A call such as ``service.get(VIEWS_BUILDER(type))`` or
                # ``service.get(CONSTANT.replace(...))`` cannot be promoted
                # without evaluating feature flags or runtime parameters.
                or (protocol == "REST" and value(argument, context=node) is None
                    and argument.type in {
                        "call_expression", "member_expression", "identifier",
                        "template_string", "binary_expression",
                    })
        ):
            # A wrapper can legitimately accept a runtime URL parameter. Its
            # call site is inspected separately; do not report a duplicate
            # warning for the wrapper's internal construction.
            scope = enclosing_scope(node)
            scope_name = text(scope.child_by_field_name("name")) if scope is not None else ""
            if protocol in {"WEBSOCKET", "GRAPHQL"} and (function_name in wrappers or scope_name in wrappers or inside_wrapper(node)):
                continue
            diagnostics.append({"code": "UNRESOLVED_WEB_ENDPOINT", "line": node.start_point.row + 1,
                                "message": "Invocation endpoint could not be bound to a workspace API path"})

    if root.has_error:
        diagnostics.append({"code": "WEB_PARSE_ERROR", "line": 1, "message": "Source contains unsupported or incomplete TypeScript/JSX syntax"})
    if "/api/" in source and not operations:
        diagnostics.append({"code": "UNBOUND_WEB_ENDPOINT", "line": 1,
                            "message": "API literals exist without a supported bound invocation; imported clients/configuration require review"})
    for name, declaration in constants.items():
        if declaration is not None and declaration.type == "identifier" and text(declaration) in rtk_apis:
            rtk_apis[name] = dict(rtk_apis[text(declaration)])
    return {"operations": operations, "diagnostics": diagnostics, "rtk_apis": rtk_apis}
