"""Extract Kafka bindings and direction from configuration and client syntax."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml
from .source_inventory import iter_source_files
from .java_kafka_helpers import index_helpers


def extract_kafka(repo: Path) -> dict[str, list[dict[str, Any]]]:
    configs: dict[str, list[dict[str, Any]]] = {}
    topics: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    # Index literal Java string constants across the repository. This supports
    # the common static-import form used by Kafka annotations while keeping
    # collisions unresolved.
    repository_constants: dict[tuple[str, str], set[str]] = {}
    constant_evidence: dict[tuple[str, str], list[dict[str, Any]]] = {}
    default_evidence: dict[str, list[dict[str, Any]]] = {}
    expression_evidence: dict[tuple[str, int, str], dict[str, Any]] = {}

    def retain_evidence(records: list[dict[str, Any]]) -> None:
        for record in records:
            expression_evidence[(record["path"], record["line"], record["declaration"])] = record
    # Java configuration-properties classes often provide a static default in
    # the field initializer instead of repeating the value in YAML. Keep
    # those defaults keyed by the property name so a getter call such as
    # ``getSsiEventTopic()`` can still resolve to exact static evidence.
    java_property_defaults: dict[str, set[str]] = {}
    resource_root = repo / "src/main/resources"

    def endpoint_protocol(raw: str, key: str = "") -> str:
        """Classify a static Camel/Kafka endpoint without guessing runtime state."""
        lowered = raw.lower().strip()
        parts = key.lower().split(".") if key else []
        route_key = bool(parts) and (parts[-1].endswith("route") or parts[-1] in {
            "inputroute", "outputroute", "eventroute", "exceptionroute",
        })
        if lowered.startswith("kafka:"):
            return "KAFKA"
        if lowered.startswith("file:"):
            return "FILE"
        if route_key and lowered.startswith(("/", "http://", "https://")):
            return "HTTP_ROUTE"
        if "kafka" in parts or "topic" in parts or "topics" in parts or (parts and "topic" in parts[-1]):
            return "KAFKA"
        if route_key:
            return "UNKNOWN_ROUTE"
        return "KAFKA"

    def configuration(key: str, raw: str, path: Path, line: int, is_string: bool = True) -> None:
        row = {"name": raw, "path": path.relative_to(repo).as_posix(), "line": line, "config_key": key}
        configs.setdefault(key, []).append(row)
        parts = key.lower().split(".")
        operational = {"attempts", "concurrency", "consumer-concurrency", "retry-partition", "partitions", "replicas", "enabled", "group-id", "group"}
        topic_key = "topic" in parts or "topics" in parts or "topic" in parts[-1]
        route_key = parts[-1].endswith("route") or parts[-1] in {"inputroute", "outputroute", "eventroute", "exceptionroute"}
        if is_string and raw and not raw.isdecimal() and parts[-1] not in operational and (topic_key or route_key or raw.startswith("kafka:")):
            name = re.sub(r"^kafka:(?://)?", "", raw).split("?", 1)[0]
            protocol = endpoint_protocol(raw, key)
            topics.append({**row, "name": name, "direction": "CONFIGURED", "expression": raw,
                           "protocol": protocol})

    def flatten(node: Any, keys: list[str], path: Path) -> None:
        if isinstance(node, yaml.MappingNode):
            for key, value in node.value:
                flatten(value, keys + [str(key.value)], path)
        elif isinstance(node, yaml.ScalarNode):
            configuration(".".join(keys), node.value, path, node.start_mark.line + 1, node.tag == "tag:yaml.org,2002:str")
        elif isinstance(node, yaml.SequenceNode):
            for value in node.value:
                flatten(value, keys, path)

    for path in iter_source_files(repo, root=resource_root, suffixes={'.yaml', '.yml', '.properties'}):
        source = path.read_text(encoding="utf-8", errors="replace")
        if path.suffix == ".properties":
            for number, line in enumerate(source.splitlines(), 1):
                match = re.match(r"\s*([^#!\s][^:=]*?)\s*[:=]\s*(.*?)\s*$", line)
                if match:
                    configuration(match.group(1), match.group(2), path, number)
        else:
            try:
                for document in yaml.compose_all(source):
                    flatten(document, [], path)
            except yaml.YAMLError:
                diagnostics.append({"code": "INVALID_KAFKA_CONFIGURATION", "path": path.relative_to(repo).as_posix(),
                                    "message": "Configuration could not be parsed; Kafka bindings from this file are unknown"})

    def property_token(value: str) -> str:
        return re.sub(r"[^a-z0-9]", "", value.lower())

    def all_nodes(node: Any):
        yield node
        for child in node.named_children:
            yield from all_nodes(child)

    def strip_java_comments(value: str, root: Any) -> str:
        """Blank Java comments without changing source offsets or lines."""
        result = bytearray(value.encode())
        for node in all_nodes(root):
            if node.type in {"line_comment", "block_comment"}:
                for index in range(node.start_byte, node.end_byte):
                    if result[index] not in {10, 13}:
                        result[index] = 32
        return result.decode()

    # Configuration-property getters are safe to bind only when one exact
    # configuration key has the same terminal property name. Repeated values
    # under one key remain separate evidence rows; conflicting keys remain
    # unresolved.
    property_keys: dict[str, set[str]] = {}
    for key in configs:
        property_keys.setdefault(property_token(key.split(".")[-1]), set()).add(key)

    java_root = repo / "src/main/java"
    java_files = list(iter_source_files(repo, root=java_root, suffixes={'.java'}))
    java_sources = {path: path.read_text(encoding="utf-8", errors="replace") for path in java_files}
    java_roots, helper_calls = index_helpers(java_sources)
    java_code = {path: strip_java_comments(source, java_roots[path]) for path, source in java_sources.items()}
    encoded_sources = {path: source.encode() for path, source in java_sources.items()}

    def java_text(path: Path, node: Any) -> str:
        return encoded_sources[path][node.start_byte:node.end_byte].decode() if node else ""

    packages, imports, wildcard_imports, static_imports = {}, {}, {}, {}
    class_owners: dict[tuple[Path, int], str] = {}
    class_nodes: dict[str, list[tuple[Path, Any]]] = {}
    for path, root in java_roots.items():
        packages[path] = next((java_text(path, child).removeprefix("package ").rstrip(";").strip()
                               for child in root.named_children if child.type == "package_declaration"), "")
        imports[path], wildcard_imports[path], static_imports[path] = {}, [], []
        for child in root.named_children:
            if child.type == "import_declaration":
                value = java_text(path, child).removeprefix("import ").rstrip(";").strip()
                if value.startswith("static "):
                    static_imports[path].append(value.removeprefix("static "))
                elif value.endswith(".*"):
                    wildcard_imports[path].append(value[:-2])
                elif not value.endswith(".*"):
                    imports[path][value.rsplit(".", 1)[-1]] = value
        for cls in all_nodes(root):
            if cls.type not in {"class_declaration", "interface_declaration"}:
                continue
            names, parent = [], cls
            while parent:
                if parent.type in {"class_declaration", "interface_declaration"}:
                    names.insert(0, java_text(path, parent.child_by_field_name("name")))
                parent = parent.parent
            owner = ".".join(([packages[path]] if packages[path] else []) + names)
            class_owners[(path, cls.start_byte)] = owner
            class_nodes.setdefault(owner, []).append((path, cls))

    def owner_identity(path: Path, node: Any) -> str:
        while node and node.type not in {"class_declaration", "interface_declaration"}:
            node = node.parent
        return class_owners.get((path, node.start_byte), "") if node else ""

    def type_identity(path: Path, raw: str) -> str:
        if raw in imports[path]:
            return imports[path][raw]
        local = f"{packages[path]}.{raw}" if packages[path] and "." not in raw else raw
        if local in class_nodes or "." in raw:
            return local
        candidates = {f"{package}.{raw}" for package in wildcard_imports[path] if f"{package}.{raw}" in class_nodes}
        return next(iter(candidates)) if len(candidates) == 1 else local

    def getter_config_keys(path: Path, node: Any) -> set[str]:
        getter = java_text(path, node.child_by_field_name("name"))
        keys = property_keys.get(property_token(getter.removeprefix("get")), set())
        owner = java_text(path, node.child_by_field_name("object"))
        parent = node.parent
        while parent:
            if parent.type == "enhanced_for_statement" and java_text(path, parent.child_by_field_name("name")) == owner:
                collection = parent.child_by_field_name("value")
                if collection and collection.type == "method_invocation":
                    container = property_token(java_text(path, collection.child_by_field_name("name")).removeprefix("get"))
                    keys = {key for key in keys if len(key.split(".")) > 1 and property_token(key.split(".")[-2]) == container}
                break
            parent = parent.parent
        return keys

    def constant_values(path: Path, raw: str, owner: str = "") -> set[str]:
        keys = []
        if "." in raw:
            declared_owner, name = raw.rsplit(".", 1)
            keys.append((type_identity(path, declared_owner), name))
        else:
            keys.append((owner, raw))
            for imported in static_imports[path]:
                declared_owner, name = imported.rsplit(".", 1)
                if name in {raw, "*"}:
                    keys.append((declared_owner, raw))
        candidates = {value for key in keys for value in repository_constants.get(key, set())}
        if len(candidates) == 1:
            retain_evidence([record for key in keys for record in constant_evidence.get(key, [])])
        return candidates

    configuration_property_getters: set[str] = set()
    for source in java_code.values():
        if "ConfigurationProperties" not in source:
            continue
        for field in re.finditer(
                r"(?m)^\s*(?:(?:private|protected|public|static|final|transient|volatile)\s+)+"
                r"(?:String|[A-Za-z_$][\w$]*(?:<[^;\n{}>]+>)?)\s+([A-Za-z_$][\w$]*)"
                r"(?:\s*=\s*[^;]+)?;", source):
            name = field.group(1)
            configuration_property_getters.add("get" + name[:1].upper() + name[1:])

    # Only declared constants can cross a file boundary. Local variables and
    # unrelated fields with equal names cannot supply an owner-qualified value.
    constructor_fields: dict[tuple[str, int], list[list[tuple[str, int]]]] = {}
    for owner, entries in class_nodes.items():
        if len(entries) != 1:
            continue
        path, cls = entries[0]
        body = cls.child_by_field_name("body")
        required, fields = [], set()
        modifiers = next((java_text(path, child) for child in cls.named_children if child.type == "modifiers"), "")
        for field in body.named_children if body else []:
            if field.type not in {"field_declaration", "constant_declaration"}:
                continue
            field_modifiers = next((java_text(path, child) for child in field.named_children if child.type == "modifiers"), "")
            for variable in field.named_children:
                if variable.type != "variable_declarator":
                    continue
                name = java_text(path, variable.child_by_field_name("name"))
                value = variable.child_by_field_name("value")
                fields.add(name)
                if "final" in field_modifiers.split() and "static" not in field_modifiers.split() and value is None:
                    required.append(name)
                if value is None or value.type != "string_literal":
                    continue
                try:
                    literal = json.loads(java_text(path, value))
                except ValueError:
                    continue
                if field.type == "constant_declaration" or {"static", "final"} <= set(field_modifiers.split()):
                    repository_constants.setdefault((owner, name), set()).add(literal)
                    constant_evidence.setdefault((owner, name), []).append({"path": path.relative_to(repo).as_posix(),
                        "line": field.start_point.row + 1, "declaration": java_text(path, field), "extractor": "java-kafka-binding"})
                if "ConfigurationProperties" in modifiers:
                    java_property_defaults.setdefault(property_token(name), set()).add(literal)
                    default_evidence.setdefault(property_token(name), []).append({"path": path.relative_to(repo).as_posix(),
                        "line": field.start_point.row + 1, "declaration": java_text(path, field), "extractor": "java-kafka-binding"})
        if re.search(r"@(?:lombok\.)?RequiredArgsConstructor\b", modifiers):
            constructor_fields.setdefault((owner, len(required)), []).append([(name, index) for index, name in enumerate(required)])
        for constructor in body.named_children if body else []:
            if constructor.type != "constructor_declaration":
                continue
            parameters = constructor.child_by_field_name("parameters")
            parameters = [java_text(path, child.child_by_field_name("name")) for child in parameters.named_children
                          if child.type == "formal_parameter"] if parameters else []
            assignments: dict[str, list[tuple[str, bool]]] = {}
            constructor_body = constructor.child_by_field_name("body")
            for assignment in all_nodes(constructor_body) if constructor_body else []:
                if assignment.type != "assignment_expression":
                    continue
                field = java_text(path, assignment.child_by_field_name("left")).removeprefix("this.")
                argument = java_text(path, assignment.child_by_field_name("right"))
                direct = assignment.parent and assignment.parent.type == "expression_statement" and assignment.parent.parent == constructor_body
                if field in fields:
                    assignments.setdefault(field, []).append((argument, bool(direct)))
            mapping = [(field, parameters.index(values[0][0])) for field, values in assignments.items()
                       if len(values) == 1 and values[0][1] and values[0][0] in parameters]
            constructor_fields.setdefault((owner, len(parameters)), []).append(mapping)

    injected_fields: dict[tuple[str, str], set[str]] = {}
    injection_evidence: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for path, root in java_roots.items():
        for creation in all_nodes(root):
            if creation.type != "object_creation_expression":
                continue
            owner = type_identity(path, java_text(path, creation.child_by_field_name("type")))
            arguments = creation.child_by_field_name("arguments")
            arguments = arguments.named_children if arguments else []
            mappings = constructor_fields.get((owner, len(arguments)), [])
            if len(mappings) != 1:
                continue
            for field, index in mappings[0]:
                argument = arguments[index]
                raw = java_text(path, argument)
                literals = constant_values(path, raw, owner_identity(path, creation))
                if len(literals) == 1:
                    raw = json.dumps(next(iter(literals)))
                elif argument.type != "string_literal" and not re.fullmatch(r"(?:[A-Za-z_$][\w$]*\.)?get[A-Z][A-Za-z0-9_$]*\(\)", raw):
                    raw = "__UNRESOLVED_CONSTRUCTOR_ARGUMENT__"
                injected_fields.setdefault((owner, field), set()).add(raw)
                injection_evidence.setdefault((owner, field), []).append({"path": path.relative_to(repo).as_posix(),
                    "line": creation.start_point.row + 1, "declaration": java_text(path, creation), "extractor": "java-kafka-binding"})
    for path in java_files:
        source = java_sources[path]
        if not helper_calls.get(path) and not re.search(r"kafka|Kafka|CamelContext|\b(?:from|to|toD)\s*\(|getEndpoint\s*\(", source):
            continue
        encoded = source.encode("utf-8")
        root = java_roots[path]

        def text(node: Any) -> str:
            return encoded[node.start_byte:node.end_byte].decode("utf-8") if node else ""

        def walk(node: Any):
            yield node
            for child in node.named_children:
                yield from walk(child)

        def enclosing_method(node: Any):
            while node and node.type not in {"method_declaration", "constructor_declaration"}:
                node = node.parent
            return node

        def enclosing_class(node: Any):
            while node and node.type not in {"class_declaration", "interface_declaration"}:
                node = node.parent
            return node.start_byte if node else -1

        active_method = None
        active_constants: dict[str, Any] = {}
        active_assignments: set[str] = set()

        def parameter_name(name: str) -> bool:
            parameters = active_method.child_by_field_name("parameters") if active_method else None
            return any(text(child.child_by_field_name("name")) == name
                       for child in parameters.named_children if child.type == "formal_parameter") if parameters else False

        constants: dict[tuple[str, str], Any] = {}
        senders = set()
        current_class = next((owner_identity(path, child) for child in root.named_children
                              if child.type in {"class_declaration", "interface_declaration"}), "")
        config_fields: dict[str, str] = {}
        for match in re.finditer(
                r'@Value\s*\(\s*"\$\{([^}:]+)(?::([^}]*))?\}"\s*\)\s*'
                r'(?:(?:public|private|protected|static|final|transient)\s+)*'
                r'[A-Za-z_$][\w$]*(?:\s*<[^;{}]+>)?\s+([A-Za-z_$][\w$]*)', source):
            key, default, field = match.groups()
            config_fields[field] = "${" + key + (":" + default if default is not None else "") + "}"
        builder_topics: dict[str, str] = {}
        # Spring's MessageBuilder sends the topic in a KafkaHeaders.TOPIC
        # header, and the later ``send(messageBuilder.build())`` call carries
        # no topic argument. Bind the builder variable to that header value.
        # The pattern is deliberately bounded by the statement terminator so
        # one builder cannot absorb a later declaration.
        for match in re.finditer(
                r"\b([A-Za-z_$][\w$]*)\s*=\s*MessageBuilder\b[^;]*?"
                r"\.setHeader\s*\(\s*KafkaHeaders\.TOPIC\s*,\s*"
                r"((?:[A-Za-z_$][\w$]*\.)*[A-Za-z_$][\w$]*(?:\(\))?|\"(?:\\.|[^\"])*\"|'(?:\\.|[^'])*')",
                source, re.S):
            builder_topics[match.group(1)] = match.group(2).strip()
        for match in re.finditer(
                r"\b([A-Za-z_$][\w$]*)\.setHeader\s*\(\s*KafkaHeaders\.TOPIC\s*,\s*"
                r"((?:[A-Za-z_$][\w$]*\.)*[A-Za-z_$][\w$]*(?:\(\))?|\"(?:\\.|[^\"])*\"|'(?:\\.|[^'])*')",
                source):
            builder_topics[match.group(1)] = match.group(2).strip()
        # A listener bean can expose a topic through a field populated from a
        # configuration-properties getter in @PostConstruct or init code.
        # Bind only simple assignments whose getter maps to one exact key.
        field_bindings: dict[str, str] = {}
        for match in re.finditer(
                r'\b([A-Za-z_$][\w$]*)\s*=\s*(?:[A-Za-z_$][\w$]*\.)?'
                r'(get[A-Z][A-Za-z0-9_$]*)\s*\(\s*\)', source):
            keys = property_keys.get(property_token(match.group(2).removeprefix("get")), set())
            if len(keys) == 1:
                field_bindings[match.group(1)] = "${" + next(iter(keys)) + "}"
        for node in walk(root):
            if node.type in {"field_declaration", "formal_parameter"}:
                if "KafkaTemplate" in text(node.child_by_field_name("type")):
                    senders.update(text(child.child_by_field_name("name")) for child in node.named_children if child.type == "variable_declarator")
                    if node.type == "formal_parameter":
                        senders.add(text(node.child_by_field_name("name")))
                for child in node.named_children:
                    if child.type == "variable_declarator":
                        constants[(owner_identity(path, node), text(child.child_by_field_name("name")))] = child.child_by_field_name("value")

        method_contexts = {}
        literal_getters: dict[tuple[int, str], list[Any]] = {}
        for method in walk(root):
            if method.type not in {"method_declaration", "constructor_declaration"}:
                continue
            values, assignments = {}, set()
            for node in walk(method):
                if node.type == "local_variable_declaration":
                    for child in node.named_children:
                        if child.type == "variable_declarator":
                            values[text(child.child_by_field_name("name"))] = child.child_by_field_name("value")
                elif node.type == "assignment_expression":
                    assignments.add(text(node.child_by_field_name("left")))
            method_contexts[method.start_byte] = (values, assignments)
            parameters = method.child_by_field_name("parameters")
            body = method.child_by_field_name("body")
            if (method.type == "method_declaration" and parameters and not parameters.named_children
                    and body and len(body.named_children) == 1 and body.named_children[0].type == "return_statement"):
                returned = body.named_children[0].named_children
                if len(returned) == 1 and returned[0].type == "string_literal":
                    literal_getters.setdefault((enclosing_class(method), text(method.child_by_field_name("name"))), []).append(returned[0])

        def expressions(node: Any, seen: frozenset[str] = frozenset()) -> list[tuple[str, bool]]:
            if node is None:
                return []
            if isinstance(node, str):
                raw = node.strip()
                if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "'\"":
                    try:
                        return [(json.loads(raw), True)]
                    except ValueError:
                        return [(raw[1:-1], True)]
                if parameter_name(raw):
                    return [(raw, False)]
                if raw in active_constants:
                    if raw in active_assignments or raw in seen:
                        return [(raw, False)]
                    return expressions(active_constants[raw], seen | {raw}) if active_constants[raw] else [(raw, False)]
                if raw in config_fields:
                    return [(config_fields[raw], False)]
                getter = re.fullmatch(r"(?:[A-Za-z_$][\w$]*\.)?(get[A-Z][A-Za-z0-9_$]*)\(\)", raw)
                if getter:
                    getter_name = getter.group(1).removeprefix("get")
                    keys = property_keys.get(property_token(getter_name), set())
                    if len(keys) == 1:
                        return [("${" + next(iter(keys)) + "}", False)]
                    defaults = java_property_defaults.get(property_token(getter_name), set())
                    if getter.group(1) in configuration_property_getters and len(defaults) == 1:
                        retain_evidence(default_evidence.get(property_token(getter_name), []))
                        return [(next(iter(defaults)), True)]
                if raw in field_bindings:
                    return expressions(field_bindings[raw], seen)
                local_value = constants.get((current_class, raw))
                if local_value is not None and raw not in seen:
                    return expressions(local_value, seen | {raw})
                injected = injected_fields.get((current_class, raw), set())
                if len(injected) == 1:
                    retain_evidence(injection_evidence.get((current_class, raw), []))
                    injected_raw = next(iter(injected)).strip()
                    getter = re.fullmatch(
                        r"(?:[A-Za-z_$][\w$]*\.)?(get[A-Z][A-Za-z0-9_$]*)\(\)", injected_raw)
                    if getter:
                        keys = property_keys.get(property_token(getter.group(1).removeprefix("get")), set())
                        if len(keys) == 1:
                            return [("${" + next(iter(keys)) + "}", False)]
                        defaults = java_property_defaults.get(
                            property_token(getter.group(1).removeprefix("get")), set())
                        if getter.group(1) in configuration_property_getters and len(defaults) == 1:
                            retain_evidence(default_evidence.get(property_token(getter.group(1).removeprefix("get")), []))
                            return [(next(iter(defaults)), True)]
                    if re.fullmatch(r"[A-Za-z_$][\w$]*", injected_raw) and injected_raw not in seen:
                        return expressions(injected_raw, seen | {raw})
                    if len(injected_raw) >= 2 and injected_raw[0] == injected_raw[-1] and injected_raw[0] in "'\"":
                        try:
                            return [(json.loads(injected_raw), True)]
                        except ValueError:
                            pass
                values = constant_values(path, raw, current_class)
                if len(values) == 1:
                    return [(next(iter(values)), True)]
                injected = injected_fields.get((current_class, raw), set())
                if len(injected) == 1:
                    return expressions(next(iter(injected)), seen | {raw})
                return [(raw, False)]
            if node.type == "string_literal":
                try:
                    retain_evidence([{"path": path.relative_to(repo).as_posix(), "line": node.start_point.row + 1,
                                      "declaration": text(node), "extractor": "java-kafka-binding"}])
                    return [(json.loads(text(node)), True)]
                except ValueError:
                    return []
            if node.type in {"element_value_array_initializer", "array_initializer"}:
                return [item for child in node.named_children for item in expressions(child, seen)]
            if node.type == "object_creation_expression" and "ProducerRecord" in text(node):
                arguments = node.child_by_field_name("arguments")
                first = arguments.named_children[0] if arguments and arguments.named_children else None
                return expressions(first, seen) if first is not None else []
            if node.type == "method_invocation":
                method_name = text(node.child_by_field_name("name"))
                owner = text(node.child_by_field_name("object"))
                arguments = node.child_by_field_name("arguments")
                if method_name.startswith("get") and not (arguments and arguments.named_children):
                    returned = literal_getters.get((enclosing_class(active_method), method_name), [])
                    if owner in {"", "this"} and len(returned) == 1:
                        return expressions(returned[0], seen)
                    keys = getter_config_keys(path, node)
                    if len(keys) == 1:
                        return [("${" + next(iter(keys)) + "}", False)]
                    defaults = java_property_defaults.get(
                        property_token(method_name.removeprefix("get")), set())
                    if method_name in configuration_property_getters and len(defaults) == 1:
                        retain_evidence(default_evidence.get(property_token(method_name.removeprefix("get")), []))
                        return [(next(iter(defaults)), True)]
                if method_name == "build" and not (arguments and arguments.named_children):
                    topic = builder_topics.get(owner.removeprefix("this."))
                    if topic:
                        return expressions(topic, seen)
            name = text(node)
            if parameter_name(name):
                return [(name, False)]
            if name in active_constants:
                if name in active_assignments or name in seen:
                    return [(name, False)]
                return expressions(active_constants[name], seen | {name}) if active_constants[name] else [(name, False)]
            if name in config_fields:
                return [(config_fields[name], False)]
            if name in field_bindings:
                return expressions(field_bindings[name], seen)
            value = constants.get((current_class, name))
            if value is None:
                injected = injected_fields.get((current_class, name), set())
                if len(injected) == 1:
                    retain_evidence(injection_evidence.get((current_class, name), []))
                    raw = next(iter(injected)).strip()
                    getter = re.fullmatch(r"(?:[A-Za-z_$][\w$]*\.)?(get[A-Z][A-Za-z0-9_$]*)\(\)", raw)
                    if getter:
                        keys = property_keys.get(property_token(getter.group(1).removeprefix("get")), set())
                        if len(keys) == 1:
                            return [("${" + next(iter(keys)) + "}", False)]
                    if (current_class, raw) in constants and raw not in seen:
                        return expressions(constants[(current_class, raw)], seen | {name})
                    if re.fullmatch(r"[A-Za-z_$][\w$]*", raw) and raw not in seen:
                        return expressions(raw, seen | {name})
                    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "'\"":
                        try:
                            return [(json.loads(raw), True)]
                        except ValueError:
                            pass
            declared_values = constant_values(path, name, current_class)
            if value is None and len(declared_values) == 1:
                value = next(iter(declared_values))
            if value is not None and name not in seen:
                if isinstance(value, str):
                    return [(value, True)]
                return expressions(value, seen | {name})
            return [(name, False)] if name else []

        modeled_binding = False
        for node in walk(root):
            direction, argument = None, None
            expression_evidence = {}
            active_method = enclosing_method(node)
            current_class = owner_identity(path, node)
            active_constants, active_assignments = method_contexts.get(active_method.start_byte, ({}, set())) if active_method else ({}, set())
            helper = helper_calls.get(path, {}).get(node.start_byte)
            if helper and helper.get("unresolved"):
                diagnostics.append({"code": "UNRESOLVED_KAFKA_HELPER", "path": path.relative_to(repo).as_posix(),
                                    "message": f"Line {node.start_point.row + 1}: helper overload, implementation, or topic forwarding is unsupported"})
                continue
            if node.type == "annotation" and text(node.child_by_field_name("name")).endswith("KafkaListener"):
                arguments = node.child_by_field_name("arguments")
                for pair in arguments.named_children if arguments else []:
                    if text(pair.child_by_field_name("key")) == "topics":
                        direction, argument = "CONSUMES", pair.child_by_field_name("value")
            elif node.type == "method_invocation":
                method, owner = text(node.child_by_field_name("name")), text(node.child_by_field_name("object"))
                arguments = node.child_by_field_name("arguments")
                args = arguments.named_children if arguments else []
                if helper:
                    direction, argument = "PUBLISHES", helper["argument"]
                elif method == "send" and owner.removeprefix("this.") in senders and args:
                    direction, argument = "PUBLISHES", args[0]
                elif method in {"from", "to", "toD"} and args and owner.removeprefix("this.") in {"", "this", "super"}:
                    # Literal Camel endpoints are handled here. Known getter
                    # bindings are expanded below from exact configuration
                    # keys, which avoids duplicate and ambiguous rows.
                    expression_text = text(args[0]).strip()
                    candidates = expressions(args[0])
                    if any(candidate.startswith(("kafka:", "file:", "/", "http://", "https://"))
                               for candidate, _ in candidates):
                        direction, argument = ("CONSUMES" if method == "from" else "PUBLISHES"), args[0]
                    elif any(re.fullmatch(r"\$\{[^}]+\}", candidate) and candidate[2:-1] in configs
                             for candidate, _ in candidates):
                        # The property row is expanded from the exact getter
                        # evidence below. Do not report it as an unknown route.
                        pass
                    elif not any(literal and candidate.startswith(("file:", "/", "http://", "https://"))
                                 for candidate, literal in candidates):
                        diagnostics.append({
                            "code": "UNRESOLVED_CAMEL_ENDPOINT",
                            "path": path.relative_to(repo).as_posix(),
                            "message": f"Line {node.start_point.row + 1}: {method} endpoint is dynamic or has no supported static route",
                        })
                elif method == "getEndpoint" and args and "camel" in owner.lower():
                    diagnostics.append({
                        "code": "UNRESOLVED_CAMEL_ENDPOINT",
                        "path": path.relative_to(repo).as_posix(),
                        "message": f"Line {node.start_point.row + 1}: Camel endpoint destination is dynamic",
                    })
            if not direction or argument is None:
                continue
            modeled_binding = True
            for expression, literal in expressions(argument):
                normalized = re.sub(r"^kafka:(?://)?", "", expression).split("?", 1)[0]
                # Spring Kafka commonly wraps a property placeholder in a
                # SpEL string, for example #{'${batch.task-topic}'}. Treat
                # the wrapper as syntax and retain the exact property key.
                spel = re.fullmatch(r"#\{\s*['\"](\$\{[^}]+\})['\"]\s*\}", normalized)
                if spel:
                    normalized = spel.group(1)
                listener = re.fullmatch(r"#\{__listener\.([A-Za-z_$][\w$]*)\}", normalized)
                if listener and listener.group(1) in field_bindings:
                    normalized = field_bindings[listener.group(1)]
                placeholder = re.fullmatch(r"\$\{([^}:]+)(?::([^}]*))?\}", normalized)
                bindings = configs.get(placeholder.group(1), []) if placeholder else []
                if placeholder and not bindings and placeholder.group(2) is not None:
                    bindings = [{"name": placeholder.group(2)}]
                unresolved = ((not literal and not placeholder and not normalized.startswith("${"))
                              or "#{" in normalized or ("${" in normalized and not bindings))
                unresolved_binding = False
                for binding in bindings or [{"name": normalized}]:
                    # Resolving one configuration key does not resolve a nested
                    # environment/SpEL/Camel expression in its configured value.
                    binding_unresolved = unresolved or any(marker in binding["name"] for marker in ("${", "#{", "{{"))
                    unresolved_binding = unresolved_binding or binding_unresolved
                    binding_name = binding["name"]
                    if "path" in binding:
                        retain_evidence([{"path": binding["path"], "line": binding["line"],
                            "declaration": f"{binding.get('config_key', placeholder.group(1) if placeholder else '')}: {binding_name}",
                            "extractor": "java-kafka-binding"}])
                    # A helper parameter is a boundary, not a channel identity.
                    # Retain the diagnostic and inspect its typed callers.
                    if binding_unresolved and (parameter_name(expression) or helper or (direction == "PUBLISHES" and not placeholder)):
                        continue
                    topics.append({"name": binding_name, "direction": direction,
                                   "path": path.relative_to(repo).as_posix(), "line": node.start_point.row + 1,
                                   "expression": expression, "unresolved": binding_unresolved,
                                   "protocol": endpoint_protocol(binding_name),
                                   "related_paths": [binding["path"]] if "path" in binding else [],
                                   **({"runtime_declaration": text(node)} if helper else {}),
                                   **({"related_evidence": [*expression_evidence.values(),
                                         *([{"path": evidence_path.relative_to(repo).as_posix(), "line": line, "declaration": declaration}
                                            for evidence_path, line, declaration in helper["helper_evidence"]] if helper else [])]}
                                      if expression_evidence or helper else {})})
                if unresolved_binding:
                    diagnostics.append({"code": "UNRESOLVED_KAFKA_TOPIC", "path": path.relative_to(repo).as_posix(),
                                        "message": f"Line {node.start_point.row + 1}: topic expression cannot be resolved statically"})
        # A KafkaTemplate bean declaration or constructor alone does not bind
        # a topic. Emit an unsupported-binding diagnostic only when this file
        # contains a concrete listener/send/record pattern that the extractor
        # failed to model.
        has_binding_syntax = re.search(
            r"\.send\s*\(|@(?:KafkaListener|RetryableTopic)\b|ProducerRecord\b|"
            r"topicPattern\s*=|topicPartitions\s*=|MessageBuilder\b",
            java_code[path],
        )
        if has_binding_syntax and not modeled_binding:
            diagnostics.append({"code": "UNSUPPORTED_KAFKA_BINDING", "path": path.relative_to(repo).as_posix(),
                                "message": "Kafka client requires unsupported record/pattern/indirect topic resolution"})
    # Bind dynamic Camel route getters to the matching configuration key. This
    # proves direction from Java call sites while retaining the exact YAML URI
    # as related evidence. Provider identity and deployment remain unresolved.
    getter_rules = {
        "getInputRoute": "CONSUMES", "getSsiNotificationTopic": "CONSUMES",
        "getCompleteTaskTopic": "CONSUMES", "getSsiEventTopic": "CONSUMES",
        "getInternalSsiEventTopic": "CONSUMES", "getSsiNotificationEventTopic": "CONSUMES",
        "getNostroNotificationEventInTopic": "CONSUMES", "getEventRoute": "PUBLISHES",
        "getExceptionRoute": "PUBLISHES", "getExceptionPlatform": "PUBLISHES",
        "getOutputRoute": "PUBLISHES", "getReleaseTopic": "PUBLISHES",
        "getSsiImpactedCashflowOutboundTopic": "PUBLISHES",
    }
    bindings: dict[str, list[dict[str, Any]]] = {}
    for path in java_files:
        for node in all_nodes(java_roots[path]):
            if node.type != "method_invocation":
                continue
            getter = java_text(path, node.child_by_field_name("name"))
            if getter not in getter_rules:
                continue
            keys = getter_config_keys(path, node)
            if len(keys) != 1:
                continue
            key = next(iter(keys))
            bindings.setdefault(key, []).append({"path": path.relative_to(repo).as_posix(),
                "line": node.start_point.row + 1, "direction": getter_rules[getter],
                "declaration": java_text(path, node)})
    expanded: list[dict[str, Any]] = []
    for topic in topics:
        config_key = str(topic.get("config_key", ""))
        matches = bindings.get(config_key, [])
        if topic.get("direction") == "CONFIGURED" and matches:
            for binding in matches:
                row = dict(topic)
                row.update({"direction": binding["direction"], "path": binding["path"], "line": binding["line"],
                            "runtime_declaration": binding["declaration"],
                            "related_paths": [topic["path"]]})
                expanded.append(row)
        else:
            expanded.append(topic)
    unique = {(item["name"], item["path"], item["direction"], item["line"]): item for item in expanded}
    return {"topics": [unique[key] for key in sorted(unique)], "diagnostics": diagnostics}
