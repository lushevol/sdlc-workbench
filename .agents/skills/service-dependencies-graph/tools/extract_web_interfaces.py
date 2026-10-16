"""Find HTTP/GraphQL/WebSocket endpoints at parsed invocation sites."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from tree_sitter import Language, Parser
import tree_sitter_typescript

from .source_inventory import is_source_file


def static_http_imports(source: Path, source_text: str, repository: Path, workspace: Path) -> dict[str, dict]:
    """Summarize direct relative imports with inspected HTTP forwarding semantics.

    This bounded rule supports a named wrapper that returns an Axios method,
    with its first argument forwarded unchanged or through one literal-prefix
    helper. Client and helper imports are inspected one level below the wrapper.
    Names, comments, and endpoint-shaped strings cannot establish a client.
    """
    cache: dict[Path, dict] = {}

    def parse(path: Path, value: str | None = None) -> dict:
        if path in cache:
            return cache[path]
        value = path.read_text(encoding="utf-8", errors="replace") if value is None else value
        encoded = value.encode("utf-8")
        language = tree_sitter_typescript.language_tsx() if path.suffix in {".tsx", ".jsx"} else tree_sitter_typescript.language_typescript()
        root = Parser(Language(language)).parse(encoded).root_node

        def text(node):
            return encoded[node.start_byte:node.end_byte].decode("utf-8") if node is not None else ""

        def walk(node):
            yield node
            for child in node.named_children:
                yield from walk(child)

        imports, exports, functions, variables = {}, {}, {}, {}
        for node in root.named_children:
            if node.type == "import_statement" and not text(node).startswith("import type"):
                raw_module = text(node.child_by_field_name("source"))
                module = raw_module[1:-1]
                clause = next((item for item in node.named_children if item.type == "import_clause"), None)
                for item in walk(clause) if clause is not None else ():
                    if item.type == "import_specifier" and not text(item).startswith("type "):
                        imported = text(item.child_by_field_name("name"))
                        local = text(item.child_by_field_name("alias")) or imported
                        imports[local] = (module, imported, node)
                    elif item.type == "identifier" and item.parent == clause:
                        imports[text(item)] = (module, "default", node)
            if node.type == "export_statement":
                declaration = node.child_by_field_name("declaration")
                if declaration is not None and declaration.type == "function_declaration":
                    name = text(declaration.child_by_field_name("name"))
                    exports[name] = name
                elif declaration is not None and declaration.type in {"lexical_declaration", "variable_declaration"}:
                    for item in declaration.named_children:
                        if item.type == "variable_declarator":
                            name = text(item.child_by_field_name("name"))
                            exports[name] = name
                for item in node.named_children:
                    if item.type == "export_clause":
                        for spec in item.named_children:
                            name = text(spec.child_by_field_name("name"))
                            alias = text(spec.child_by_field_name("alias")) or name
                            exports[alias] = name
                default_value = node.child_by_field_name("value")
                if text(node).startswith("export default") and default_value is not None and default_value.type == "identifier":
                    exports["default"] = text(default_value)
        for node in walk(root):
            if node.type == "function_declaration" and node.parent.type in {"program", "export_statement"}:
                functions[text(node.child_by_field_name("name"))] = node
            elif node.type == "variable_declarator" and node.parent.parent.type in {"program", "export_statement"}:
                name = text(node.child_by_field_name("name"))
                value_node = node.child_by_field_name("value")
                variables.setdefault(name, []).append(value_node)
                if value_node is not None and value_node.type in {"arrow_function", "function_expression", "function"}:
                    functions[name] = value_node
        result = {"path": path, "root": root, "text": text, "walk": walk, "imports": imports,
                  "exports": exports, "functions": functions, "variables": variables}
        cache[path] = result
        return result

    def resolve(path: Path, specifier: str) -> Path | None:
        if not specifier.startswith("."):
            return None
        base = Path(os.path.abspath(path.parent / specifier))
        suffixes = (".ts", ".tsx", ".js", ".jsx")
        candidates = [candidate for candidate in (
            base, *(Path(str(base) + suffix) for suffix in suffixes if base.suffix not in suffixes),
            *(base / ("index" + suffix) for suffix in suffixes),
        ) if is_source_file(repository, candidate)]
        unique = sorted(set(candidates))
        return unique[0] if len(unique) == 1 else None

    def support(module: dict, node, declaration: str, extractor="web-http-wrapper") -> dict:
        path = module["path"]
        try:
            path_value = path.relative_to(workspace).as_posix()
        except ValueError:
            path_value = path.as_posix()
        return {"path": path_value, "line": node.start_point.row + 1,
                "declaration": declaration, "extractor": extractor}

    def sole_return(function):
        body = function.child_by_field_name("body")
        if body is None:
            return None
        if body.type != "statement_block":
            return body
        statements = [item for item in body.named_children if item.type != "comment"]
        if len(statements) != 1 or statements[0].type != "return_statement":
            return None
        return statements[0].named_children[0] if len(statements[0].named_children) == 1 else None

    def first_parameter(module, function) -> str | None:
        parameters = function.child_by_field_name("parameters")
        rows = parameters.named_children if parameters is not None else []
        if not rows:
            parameter = function.child_by_field_name("parameter")
            return module["text"](parameter) if parameter is not None and parameter.type == "identifier" else None
        parameter = rows[0]
        name = parameter.child_by_field_name("pattern") or parameter.child_by_field_name("name")
        if name is None and parameter.type == "identifier":
            name = parameter
        return module["text"](name) if name is not None and name.type == "identifier" else None

    def parameter_names(module, function) -> set[str]:
        parameters = function.child_by_field_name("parameters")
        names = set()
        for parameter in parameters.named_children if parameters is not None else ():
            name = parameter.child_by_field_name("pattern") or parameter.child_by_field_name("name")
            if name is None and parameter.type == "identifier":
                name = parameter
            if name is not None:
                names.add(module["text"](name))
        return names

    def prefix_export(module: dict, exported: str) -> dict | None:
        if module["root"].has_error:
            return None
        name = module["exports"].get(exported)
        function = module["functions"].get(name)
        if function is None:
            return None
        parameter, returned = first_parameter(module, function), sole_return(function)
        if not parameter or returned is None:
            return None
        text = module["text"]
        prefix = None
        if returned.type == "template_string":
            expression = text(returned)
            match = re.fullmatch(r"`([^`$\\]*)\$\{\s*" + re.escape(parameter) + r"\s*\}`", expression)
            prefix = match.group(1) if match else None
        elif returned.type == "binary_expression" and text(returned.child_by_field_name("operator")) == "+":
            left, right = returned.child_by_field_name("left"), returned.child_by_field_name("right")
            raw = text(left)
            if left is not None and left.type == "string" and text(right) == parameter and "\\" not in raw:
                prefix = raw[1:-1]
        if prefix is None or not prefix.startswith("/") or not re.fullmatch(r"/[A-Za-z0-9_./-]*", prefix):
            return None
        return {"prefix": prefix, "supporting_evidence": [support(module, function, f"URL helper {name} adds literal prefix {prefix}")]}

    def configured_routing(module: dict, config, seen=()) -> dict:
        """Inspect routing fields without retaining unrelated configuration values."""
        text = module["text"]
        if config is None:
            return {"base_url": "", "has_base_url": False}
        if config.type == "identifier" and text(config) not in seen:
            values = module["variables"].get(text(config), [])
            if len(values) == 1 and values[0] is not None:
                return configured_routing(module, values[0], (*seen, text(config)))
        if config.type != "object":
            return {"routing_limit": "DYNAMIC_CLIENT_CONFIGURATION"}
        fields = {}
        for item in config.named_children:
            if item.type == "comment":
                continue
            if item.type not in {"pair", "shorthand_property_identifier"}:
                return {"routing_limit": "UNSUPPORTED_CLIENT_CONFIGURATION"}
            key = text(item.child_by_field_name("key")).strip("\"'") if item.type == "pair" else text(item)
            if not re.fullmatch(r"[A-Za-z_$][\w$]*", key) or key in fields:
                return {"routing_limit": "UNSUPPORTED_CLIENT_CONFIGURATION"}
            fields[key] = item.child_by_field_name("value") if item.type == "pair" else item
        if {"adapter", "transport", "socketPath", "allowAbsoluteUrls"} & fields.keys():
            return {"routing_limit": "UNSUPPORTED_CLIENT_TRANSPORT_CONFIGURATION"}
        base = fields.get("baseURL")
        if base is None:
            return {"base_url": "", "has_base_url": False}
        raw = text(base)
        if base.type != "string" or "\\" in raw:
            return {"routing_limit": "DYNAMIC_CLIENT_BASE_URL"}
        value = raw[1:-1]
        try:
            parsed = urlsplit(value)
        except ValueError:
            return {"routing_limit": "UNSUPPORTED_CLIENT_BASE_URL"}
        if (parsed.username or parsed.password or parsed.query or parsed.fragment or
                (value and not value.startswith(("/", "http://", "https://")))):
            return {"routing_limit": "UNSUPPORTED_CLIENT_BASE_URL"}
        return {"base_url": value, "has_base_url": True}

    def member_path(module: dict, expression) -> list[str] | None:
        if expression is None:
            return None
        text = module["text"]
        if expression.type == "identifier":
            return [text(expression)]
        if expression.type not in {"member_expression", "subscript_expression"}:
            return None
        parent = member_path(module, expression.child_by_field_name("object"))
        part = expression.child_by_field_name("property") or expression.child_by_field_name("index")
        return [*parent, text(part).strip("\"'")] if parent and part is not None else None

    def request_callback(module: dict, callback) -> list[dict] | None:
        """Accept a bounded callback that returns its request and changes headers only."""
        text = module["text"]
        if callback is not None and callback.type == "identifier":
            name = text(callback)
            function = module["functions"].get(name)
            if function is None:
                imported = module["imports"].get(name)
                path = resolve(module["path"], imported[0]) if imported else None
                if path:
                    other = parse(path)
                    function = other["functions"].get(other["exports"].get(imported[1]))
                    return request_callback(other, function)
            callback = function
        if callback is None or callback.type not in {"arrow_function", "function_expression", "function", "function_declaration"}:
            return None
        parameter = first_parameter(module, callback)
        body = callback.child_by_field_name("body")
        if not parameter or body is None or callback.has_error:
            return None
        if body.type != "statement_block":
            return ([support(module, callback, "Request interceptor returns its unchanged request", "web-http-client")]
                    if text(body) == parameter else None)
        returns = []
        for item in module["walk"](body):
            if item.type in {"arrow_function", "function_expression", "function", "function_declaration"}:
                return None
            if item.type == "return_statement":
                returns.append(item)
                if len(item.named_children) != 1 or text(item.named_children[0]) != parameter:
                    return None
            if item.type in {"assignment_expression", "augmented_assignment_expression", "update_expression", "unary_expression"}:
                left = item.child_by_field_name("left") or item.child_by_field_name("argument")
                parts = member_path(module, left)
                if parts and parts[0] == parameter and parts[1:2] != ["headers"]:
                    return None
            if item.type == "identifier" and text(item) == parameter:
                parent = item.parent
                if parent is not None and parent.type in {"required_parameter", "optional_parameter", "return_statement"}:
                    continue
                if parent is None or parent.type not in {"member_expression", "subscript_expression"} or parent.child_by_field_name("object") != item:
                    return None
            if item.type == "call_expression":
                arguments = item.child_by_field_name("arguments")
                if arguments is not None and any(part.type == "identifier" and text(part) == parameter
                                                  for part in module["walk"](arguments)):
                    return None
                parts = member_path(module, item.child_by_field_name("function"))
                if parts and parts[0] == parameter and parts[1:] != ["url", "includes"]:
                    return None
        if not returns:
            return None
        return [support(module, callback, "Request interceptor returns its request and only changes request headers", "web-http-client")]

    def client_export(module: dict, exported: str) -> dict | None:
        name = module["exports"].get(exported)
        values = module["variables"].get(name, [])
        if module["root"].has_error or len(values) != 1 or values[0] is None or values[0].type != "call_expression":
            return None
        function = values[0].child_by_field_name("function")
        text = module["text"]
        if function is None or function.type != "member_expression" or text(function.child_by_field_name("property")) != "create":
            return None
        base = text(function.child_by_field_name("object"))
        binding = module["imports"].get(base)
        if binding is None or binding[:2] != ("axios", "default"):
            return None
        args = values[0].child_by_field_name("arguments")
        config = args.named_children[0] if args is not None and args.named_children else None
        routing = configured_routing(module, config)
        config_name = text(config) if config is not None and config.type == "identifier" else None
        evidence = [support(module, binding[2], f"Imports Axios client {base}", "web-http-client"),
                    support(module, values[0], f"Axios.create declares client {name}; routing configuration inspected", "web-http-client")]
        for item in module["walk"](module["root"]):
            if item.type in {"assignment_expression", "augmented_assignment_expression", "update_expression"}:
                left = item.child_by_field_name("left") or item.child_by_field_name("argument")
                parts = member_path(module, left)
                if parts and parts[0] in {name, base} and parts[1:3] != ["defaults", "headers"]:
                    routing = {"routing_limit": "CLIENT_ROUTING_MUTATION"}
                if parts and parts[0] == config_name and parts[1:2] != ["headers"]:
                    routing = {"routing_limit": "CLIENT_CONFIGURATION_MUTATION"}
            if item.type == "variable_declarator" and text(item.child_by_field_name("value")) == name:
                routing = {"routing_limit": "CLIENT_ESCAPES_STATIC_ROUTING_INSPECTION"}
            if config_name and item.type == "variable_declarator" and text(item.child_by_field_name("value")) == config_name:
                routing = {"routing_limit": "CLIENT_CONFIGURATION_MUTATION"}
            if item.type != "call_expression":
                continue
            function = item.child_by_field_name("function")
            parts = member_path(module, function)
            arguments = item.child_by_field_name("arguments")
            if parts == [name, "interceptors", "request", "use"]:
                callback = arguments.named_children[0] if arguments is not None and arguments.named_children else None
                inspected = request_callback(module, callback)
                if inspected is None or (arguments is not None and len(arguments.named_children) > 1):
                    routing = {"routing_limit": "UNINSPECTED_REQUEST_INTERCEPTOR"}
                else:
                    evidence.extend(inspected)
            elif arguments is not None and any(text(argument) == name for argument in arguments.named_children):
                routing = {"routing_limit": "CLIENT_ESCAPES_STATIC_ROUTING_INSPECTION"}
            elif (config_name and item != values[0] and arguments is not None and
                  any(text(argument) == config_name for argument in arguments.named_children)):
                routing = {"routing_limit": "CLIENT_CONFIGURATION_MUTATION"}
        return {**routing, "supporting_evidence": evidence}

    def wrapper_export(module: dict, exported: str) -> dict | None:
        name = module["exports"].get(exported)
        function = module["functions"].get(name)
        if module["root"].has_error or function is None:
            return None
        parameter, returned = first_parameter(module, function), sole_return(function)
        if parameter is None or returned is None or returned.type != "call_expression":
            return None
        text = module["text"]
        called = returned.child_by_field_name("function")
        if called is None or called.type != "member_expression":
            return None
        method, client = text(called.child_by_field_name("property")).upper(), text(called.child_by_field_name("object"))
        if method not in {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}:
            return None
        if client in parameter_names(module, function):
            return None
        imported_client = module["imports"].get(client)
        if imported_client is None:
            return None
        client_path = resolve(module["path"], imported_client[0])
        client_binding = client_export(parse(client_path), imported_client[1]) if client_path else None
        if client_binding is None:
            return None
        args = returned.child_by_field_name("arguments")
        first = args.named_children[0] if args is not None and args.named_children else None
        config_index = 1 if method in {"GET", "DELETE", "HEAD", "OPTIONS"} else 2
        config = args.named_children[config_index] if args is not None and len(args.named_children) > config_index else None
        request_config_index = None
        if config is not None:
            parameters = function.child_by_field_name("parameters")
            for index, item in enumerate(parameters.named_children if parameters is not None else ()):
                name_node = item.child_by_field_name("pattern") or item.child_by_field_name("name")
                if name_node is not None and text(name_node) == text(config):
                    request_config_index = index
                    break
            if request_config_index is None:
                overrides = configured_routing(module, config)
                if overrides.get("routing_limit"):
                    client_binding = {**client_binding, **overrides}
                elif overrides.get("has_base_url"):
                    client_binding = {**client_binding, **overrides}
        prefix, helper_evidence = "", []
        if text(first) != parameter:
            if first is None or first.type != "call_expression":
                return None
            helper = text(first.child_by_field_name("function"))
            if helper in parameter_names(module, function):
                return None
            imported_helper = module["imports"].get(helper)
            arguments = first.child_by_field_name("arguments")
            if imported_helper is None or arguments is None or len(arguments.named_children) != 1 or text(arguments.named_children[0]) != parameter:
                return None
            helper_path = resolve(module["path"], imported_helper[0])
            binding = prefix_export(parse(helper_path), imported_helper[1]) if helper_path else None
            if binding is None:
                return None
            prefix, helper_evidence = binding["prefix"], binding["supporting_evidence"]
        return {**client_binding, "method": method, "prefix": prefix,
                "request_config_index": request_config_index, "supporting_evidence": [
            support(module, function, f"HTTP wrapper {name} forwards {parameter} to {client}.{method.lower()} with literal prefix {prefix or '(empty)'}"),
            *client_binding["supporting_evidence"], *helper_evidence,
        ]}

    module = parse(source, source_text)
    result: dict[str, dict] = {"wrappers": {}, "url_helpers": {}, "clients": {}}
    for local, (specifier, imported, import_node) in module["imports"].items():
        target = resolve(source, specifier)
        if target is None:
            continue
        imported_module = parse(target)
        for category, binding in (("wrappers", wrapper_export(imported_module, imported)),
                                  ("url_helpers", prefix_export(imported_module, imported)),
                                  ("clients", client_export(imported_module, imported))):
            if binding is not None:
                import_evidence = support(module, import_node, f"Imports {imported} as {local} from {specifier}")
                result[category][local] = {**binding, "supporting_evidence": [import_evidence, *binding["supporting_evidence"]]}
    return result


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
                       external_rtk_apis: dict[str, dict[str, Any]] | None = None,
                       external_http_bindings: dict[str, dict] | None = None) -> dict[str, Any]:
    encoded = source.encode("utf-8")
    language = tree_sitter_typescript.language_tsx() if tsx else tree_sitter_typescript.language_typescript()
    root = Parser(Language(language)).parse(encoded).root_node
    operations: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    rtk_apis: dict[str, dict[str, Any]] = {}
    http_bindings = external_http_bindings or {}

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

    def external_binding(category: str, name: str, context: Any) -> dict | None:
        # Imported functions lose their summary when a local declaration or
        # parameter shadows them. Inspect all containing function scopes.
        current = context
        while current is not None:
            if (id(current), name) in scoped_declarations:
                return None
            current = parents.get(id(current))
        if name in declarations:
            return None
        return http_bindings.get(category, {}).get(name)

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
            helper = external_binding("url_helpers", function_name, context)
            if helper is not None:
                arguments_node = node.child_by_field_name("arguments")
                arguments = arguments_node.named_children if arguments_node is not None else []
                if len(arguments) == 1:
                    return [helper["prefix"] + item for item in possible_values(arguments[0], seen, context)]
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

    def safe_endpoint(destination: str) -> str | None:
        """Keep a static routing identity, without query values or credentials."""
        try:
            parsed = urlsplit(destination)
            if parsed.scheme and parsed.scheme.lower() not in {"http", "https", "ws", "wss"}:
                return None
            if not parsed.scheme and not destination.startswith("/"):
                return None
            if (parsed.scheme or destination.startswith("//")) and not parsed.hostname:
                return None
            # Removing credentials could make a distinct authenticated request
            # look like an ordinary provider call. Keep this form unresolved.
            if parsed.username is not None or parsed.password is not None:
                return None
            parsed.port  # Reject malformed explicit ports before publication.
            query = urlencode([(key, "{value}") for key, _ in parse_qsl(parsed.query, keep_blank_values=True)])
            if query == parsed.query and not parsed.fragment:
                return destination
            return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, query, ""))
        except ValueError:
            return None

    def safe_invocation(node: Any, endpoint_argument: Any, destination: str) -> str:
        """Retain call syntax while excluding arbitrary request literal values."""
        replacements = []
        methods = {"GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "ANY"}
        for item in walk(node):
            if item.type not in {"string", "template_string"}:
                continue
            ancestor = item.parent
            while ancestor is not None and ancestor != node and ancestor.type not in {"string", "template_string"}:
                ancestor = ancestor.parent
            if ancestor is not None and ancestor != node:
                continue
            raw = text(item)
            resolved = value(item, context=node)
            safe = safe_endpoint(resolved) if resolved else None
            if safe is not None:
                replacement = raw if safe == resolved else json.dumps(safe)
            elif item == endpoint_argument:
                replacement = json.dumps(destination)
            elif resolved in methods:
                replacement = raw
            elif item.parent and item.parent.type == "pair" and item == item.parent.child_by_field_name("key"):
                replacement = raw
            else:
                replacement = '"{value}"'
            if replacement != raw:
                replacements.append((item.start_byte, item.end_byte, replacement.encode("utf-8")))
        declaration = encoded[node.start_byte:node.end_byte]
        for start, end, replacement in sorted(replacements, reverse=True):
            declaration = declaration[:start - node.start_byte] + replacement + declaration[end - node.start_byte:]
        return declaration.decode("utf-8")[:500]

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

    # Additional REST URL prefixes require an explicit fetch or axios client.
    # Ordinary Map/object get methods can accept path-shaped keys.
    axios_clients = {"axios"}
    for import_node in root.named_children:
        if import_node.type == "import_statement" and value(import_node.child_by_field_name("source")) == "axios":
            clause = next((item for item in import_node.named_children if item.type == "import_clause"), None)
            if clause is not None:
                axios_clients.update(text(item) for item in clause.named_children if item.type == "identifier")
    for declaration in walk(root):
        if declaration.type != "variable_declarator":
            continue
        expression = declaration.child_by_field_name("value")
        function = expression.child_by_field_name("function") if expression is not None else None
        if (function is not None and function.type == "member_expression"
                and text(function.child_by_field_name("object")) in axios_clients
                and text(function.child_by_field_name("property")) == "create"):
            axios_clients.add(text(declaration.child_by_field_name("name")))

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
        dynamic_method = False
        forwarding = external_binding("wrappers", function_name, node)
        client_routing = forwarding
        call_support: list[dict] = []
        explicit_rest_client = function_name == "fetch" or function_name in axios_clients or (
            function is not None and function.type == "member_expression"
            and text(function.child_by_field_name("object")) in axios_clients
        )
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
        elif function_name == "fetch" or function_name in axios_clients or leaf == "request":
            protocol = "REST"
            first = arguments[0] if arguments else None
            config = properties(first) or properties(arguments[1] if len(arguments) > 1 else None)
            argument = config.get("url", first)
            method_value = value(config.get("method"))
            dynamic_method = "method" in config and method_value is None
            method = (method_value or ("GET" if function_name == "fetch" and "method" not in config else "ANY")).upper()
        elif function and function.type == "identifier" and function_name in wrappers:
            protocol = wrappers[function_name]
            argument = arguments[0] if arguments else None
            config = properties(argument)
            argument = config.get("url", config.get("uri", argument))
        elif function and function.type == "identifier" and function_name in rest_wrappers:
            protocol, method = "REST", rest_wrappers[function_name]
            argument = arguments[0] if arguments else None
        elif function is not None and function.type == "identifier" and forwarding is not None:
            protocol, method = "REST", forwarding["method"]
            argument = arguments[0] if arguments else None
            explicit_rest_client = True
            call_support.extend(forwarding.get("supporting_evidence", []))
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
        if forwarding is not None:
            urls = [forwarding["prefix"] + url for url in urls]
        if function is not None and function.type == "member_expression":
            binding = external_binding("clients", text(function.child_by_field_name("object")), node)
            if binding is not None:
                explicit_rest_client = True
                client_routing = binding
                call_support.extend(binding.get("supporting_evidence", []))
        if client_routing is not None:
            routing_limit = client_routing.get("routing_limit")
            base_url = client_routing.get("base_url", "")
            config_index = (forwarding.get("request_config_index") if forwarding is not None else
                            1 if method in {"GET", "DELETE", "HEAD", "OPTIONS"} else 2)
            config = arguments[config_index] if config_index is not None and len(arguments) > config_index else None
            if config is not None:
                fields = properties(config)
                if config.type != "object" or any(item.type not in {"pair", "shorthand_property_identifier", "comment"}
                                                   or (item.type == "pair" and item.child_by_field_name("key").type
                                                       not in {"property_identifier", "string", "identifier"})
                                                   for item in config.named_children):
                    routing_limit = "DYNAMIC_REQUEST_CONFIGURATION"
                elif {"adapter", "transport", "socketPath", "allowAbsoluteUrls"} & fields.keys():
                    routing_limit = "UNSUPPORTED_REQUEST_TRANSPORT_CONFIGURATION"
                elif "baseURL" in fields:
                    override = value(fields["baseURL"], context=node)
                    if override is None or safe_endpoint(override) is None:
                        routing_limit = "DYNAMIC_REQUEST_BASE_URL"
                    else:
                        base_url = safe_endpoint(override)
            if routing_limit:
                diagnostics.append({"code": "UNRESOLVED_WEB_CLIENT_ROUTING", "line": node.start_point.row + 1,
                                    "message": "Imported HTTP client destination is not established: " + routing_limit})
                continue
            if base_url:
                urls = [url if re.match(r"^(?:[A-Za-z][A-Za-z0-9+.-]*:)?//", url) else
                        base_url.rstrip("/") + "/" + url.lstrip("/") for url in urls]
        if argument is not None:
            for part in walk(argument):
                if part.type == "call_expression":
                    helper = external_binding("url_helpers", text(part.child_by_field_name("function")), node)
                    if helper is not None:
                        call_support.extend(helper.get("supporting_evidence", []))
        # Endpoint recognition is independent of a workspace's URL prefix.
        # Preserve an absolute authority so resolution cannot match by path alone.
        safe_urls = [safe_endpoint(url) for url in urls]
        recognized_prefix = all(url.startswith("/api/") for url in urls)
        supported_client = protocol != "REST" or explicit_rest_client
        if safe_urls and all(url is not None for url in safe_urls) and (recognized_prefix or supported_client):
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
            for url in sorted(set(safe_urls)):
                operations.append({"path": url, "protocol": protocol, "method": method or "ANY",
                                   "line": node.start_point.row + 1, "declaration": safe_invocation(node, argument, url),
                                   "assertion_status": "INFERRED" if len(set(urls)) > 1 or dynamic_method else "CONFIRMED",
                                   "conditional": len(set(urls)) > 1 or dynamic_method,
                                   **({"supporting_evidence": call_support} if call_support else {})})
        elif argument is not None and (
                "/api/" in text(argument)
                or protocol != "REST"
                or explicit_rest_client
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
                                "message": "Invocation endpoint has no supported static routing identity"})

    if root.has_error:
        diagnostics.append({"code": "WEB_PARSE_ERROR", "line": 1, "message": "Source contains unsupported or incomplete TypeScript/JSX syntax"})
    if "/api/" in source and not operations:
        diagnostics.append({"code": "UNBOUND_WEB_ENDPOINT", "line": 1,
                            "message": "API literals exist without a supported bound invocation; imported clients/configuration require review"})
    for name, declaration in constants.items():
        if declaration is not None and declaration.type == "identifier" and text(declaration) in rtk_apis:
            rtk_apis[name] = dict(rtk_apis[text(declaration)])
    return {"operations": operations, "diagnostics": diagnostics, "rtk_apis": rtk_apis}
