"""Extract Java type relationships and configuration declarations without values.

The analysis records declared types and bounded typed calls. It does not choose
Spring beans, active profiles, runtime dispatch targets, or deployed values.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from tree_sitter import Language, Parser
import tree_sitter_java
import yaml
from yaml.nodes import MappingNode, ScalarNode, SequenceNode

from . import source_inventory


TYPE_NODES = {"class_declaration", "interface_declaration", "enum_declaration", "record_declaration", "annotation_type_declaration"}
METHOD_NODES = {"method_declaration", "constructor_declaration", "compact_constructor_declaration", "lambda_expression"}
PRIMITIVES = {"void", "byte", "short", "int", "long", "float", "double", "char", "boolean", "var", "extends", "super"}
SPRING_ANNOTATIONS = {
    "ConfigurationProperties": "org.springframework.boot.context.properties",
    "Configuration": "org.springframework.context.annotation",
    "Profile": "org.springframework.context.annotation",
    "Bean": "org.springframework.context.annotation",
    "ConditionalOnProperty": "org.springframework.boot.autoconfigure.condition",
    "Service": "org.springframework.stereotype",
    "Component": "org.springframework.stereotype",
    "Repository": "org.springframework.stereotype",
    "Controller": "org.springframework.stereotype",
    "RestController": "org.springframework.web.bind.annotation",
    "FeignClient": "org.springframework.cloud.openfeign", "KafkaListener": "org.springframework.kafka.annotation",
    "Autowired": "org.springframework.beans.factory.annotation",
    "Value": "org.springframework.beans.factory.annotation",
    "Inject": "jakarta.inject",
    "Data": "lombok", "Getter": "lombok", "RequiredArgsConstructor": "lombok", "AllArgsConstructor": "lombok",
}
PLACEHOLDER = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_.\[\]-]*)")
SAFE_KEY = re.compile(r"[A-Za-z_][A-Za-z0-9_.\[\]*-]*\Z")
ENV_TYPES = {"org.springframework.core.env.Environment", "org.springframework.core.env.ConfigurableEnvironment", "org.springframework.core.env.AbstractEnvironment"}


def _walk(node):
    yield node
    for child in node.named_children:
        yield from _walk(child)


def _nearest(node, types):
    while node is not None and node.type not in types:
        node = node.parent
    return node


def _sid(prefix, *parts):
    return prefix + ":" + hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()[:24]


def _canonical(key):
    """Match Spring relaxed punctuation without selecting a property value."""
    return ".".join(re.sub(r"[-_]", "", part).lower() for part in key.split("."))


def _kebab(name):
    return re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", name).lower()


def _literal(unit, node):
    if node is None or node.type != "string_literal":
        return None
    try:
        value = json.loads(unit.text(node))
    except (ValueError, TypeError):
        return None
    return value if isinstance(value, str) else None


def _type_names(raw):
    return [name for name in re.findall(r"[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*", raw) if name not in PRIMITIVES]


class _Unit:
    def __init__(self, path, repo):
        self.path = path
        self.relative = path.relative_to(repo).as_posix()
        self.encoded = path.read_bytes()
        self.root = Parser(Language(tree_sitter_java.language())).parse(self.encoded).root_node
        self.package = ""
        self.imports = defaultdict(set)
        self.wildcards = set()
        self.types = {}
        self.local_names = set()
        for node in self.root.named_children:
            value = self.text(node)
            if node.type == "package_declaration":
                self.package = value.removeprefix("package").strip().rstrip(";").strip()
            elif node.type == "import_declaration" and not re.match(r"import\s+static\b", value):
                value = value.removeprefix("import").strip().rstrip(";").strip()
                if value.endswith(".*"):
                    self.wildcards.add(value[:-2])
                else:
                    self.imports[value.rsplit(".", 1)[-1]].add(value)

    def text(self, node):
        return self.encoded[node.start_byte:node.end_byte].decode("utf-8", errors="replace") if node is not None else ""

    def annotation(self, node, name):
        package = SPRING_ANNOTATIONS.get(name)
        alternatives = {package + "." + name} if package else set()
        if name == "Inject":
            alternatives.add("javax.inject.Inject")
        modifiers = next((child for child in node.named_children if child.type == "modifiers"), None)
        for item in modifiers.named_children if modifiers is not None else []:
            if item.type not in {"annotation", "marker_annotation"}:
                continue
            declared = self.text(item.child_by_field_name("name"))
            if declared in alternatives or (declared == name and
                    (bool(self.imports.get(name, set()) & alternatives) or (name not in self.local_names and any(value.rsplit(".", 1)[0] in self.wildcards for value in alternatives)))):
                return item
        return None

    def arguments(self, annotation):
        result = {}
        args = annotation.child_by_field_name("arguments") if annotation is not None else None
        for child in args.named_children if args is not None else []:
            if child.type == "element_value_pair":
                result[self.text(child.child_by_field_name("key"))] = child.child_by_field_name("value")
            else:
                result["value"] = child
        return result

    def annotation_strings(self, annotation, key="value"):
        node = self.arguments(annotation).get(key)
        values = node.named_children if node is not None and node.type == "element_value_array_initializer" else [node]
        return [value for child in values if (value := _literal(self, child)) is not None]

    def owner(self, node):
        declaration = _nearest(node, TYPE_NODES)
        return self.types.get(declaration.start_byte) if declaration is not None else None


def _role(unit, node):
    for annotation, role in [("ConfigurationProperties", "CONFIGURATION_PROPERTIES"), ("Configuration", "CONFIGURATION"),
                             ("FeignClient", "FEIGN_CLIENT"), ("KafkaListener", "KAFKA_CONSUMER"), ("RestController", "CONTROLLER"), ("Controller", "CONTROLLER"), ("Repository", "REPOSITORY"),
                             ("Service", "APPLICATION_SERVICE"), ("Component", "COMPONENT")]:
        if unit.annotation(node, annotation) is not None:
            return role
    return {"interface_declaration": "INTERFACE", "enum_declaration": "ENUM", "record_declaration": "RECORD", "annotation_type_declaration": "ANNOTATION"}.get(node.type, "JAVA_TYPE")


def _roots(repo, name, default):
    helper = getattr(source_inventory, name, None)
    return helper(repo) if helper is not None else [repo / default]


def _record(path, line, declaration, extractor="java-structure", **extra):
    return {"path": path, "line": line, "declaration": declaration, "extractor": extractor, **extra}


def _resolve(name, unit, owner, index):
    if name in index:
        return sorted(index[name])
    imported = unit.imports.get(name.split(".", 1)[0], set())
    if imported:
        tail = name.partition(".")[2]
        return sorted({key for value in imported for key in index.get(value + ("." + tail if tail else ""), [])})
    # Java member types and enclosing types take precedence over package wildcards.
    context = owner["qualified_name"] if owner else ""
    while context and context != unit.package:
        qualified = context + "." + name
        if qualified in index:
            return sorted(index[qualified])
        context = context.rpartition(".")[0]
    qualified = (unit.package + "." if unit.package else "") + name
    if qualified in index:
        return sorted(index[qualified])
    return sorted({key for wildcard in unit.wildcards for key in index.get(wildcard + "." + name, [])})


def _external_type(name, unit):
    if "." in name:
        return name
    candidates = unit.imports.get(name, set())
    if len(candidates) == 1:
        return next(iter(candidates))
    if name in {"Environment", "ConfigurableEnvironment", "AbstractEnvironment"} and "org.springframework.core.env" in unit.wildcards:
        return "org.springframework.core.env." + name
    return name


def _config_sources(repo):
    """Read names, references, profile labels, and locations. Never return values."""
    declarations, references, diagnostics = [], [], []
    paths = set()
    for root in _roots(repo, "resource_source_roots", "src/main/resources"):
        paths.update(source_inventory.iter_source_files(repo, root=root, suffixes={".yaml", ".yml", ".properties"}))
    for path in sorted(paths):
        relative = path.relative_to(repo).as_posix()
        stem = re.match(r"(?:application|bootstrap)(?:-(.+))?$", path.stem)
        filename_profile = stem.group(1) if stem else None
        profile = filename_profile if filename_profile and re.fullmatch(r"[A-Za-z0-9_.!&|, -]{1,100}", filename_profile) else "UNSELECTED"
        try:
            source = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            diagnostics.append(_record(relative, 1, "Configuration source cannot be read", code="UNREADABLE_CONFIGURATION_SOURCE"))
            continue

        def retain(key, line, value, document=0, active_profile=profile):
            if not SAFE_KEY.fullmatch(key) or len(key) > 240:
                diagnostics.append(_record(relative, line, "Unsupported configuration key syntax", code="UNSUPPORTED_CONFIGURATION_KEY"))
                return
            declaration = _record(relative, line, "Configuration key " + key, "configuration-source", key=key,
                                  canonical_key=_canonical(key), profile=active_profile, document=document)
            declarations.append(declaration)
            for match in PLACEHOLDER.finditer(value):
                target = match.group(1)
                references.append(_record(relative, line, f"Configuration key {key} references {target}", "configuration-source",
                                          source_key=key, key=target, canonical_key=_canonical(target), profile=active_profile, document=document))

        if path.suffix == ".properties":
            continuation = False
            for line, value in enumerate(source.splitlines(), 1):
                continued = bool((len(value) - len(value.rstrip("\\"))) % 2)
                if continuation:
                    continuation = continued
                    continue
                if value.lstrip().startswith(("#", "!")) or not value.strip():
                    continue
                if continued:
                    continuation = True
                    diagnostics.append(_record(relative, line, "Properties continuation requires unsupported expression analysis", code="UNSUPPORTED_CONFIGURATION_CONTINUATION"))
                    continue
                match = re.match(r"\s*([^\s=:]+)\s*[:=]\s*(.*)", value)
                if match:
                    retain(match.group(1), line, match.group(2))
                else:
                    diagnostics.append(_record(relative, line, "Unsupported properties declaration", code="UNSUPPORTED_CONFIGURATION_SYNTAX"))
            continue
        try:
            documents = list(yaml.compose_all(source, Loader=yaml.SafeLoader))
        except yaml.YAMLError:
            diagnostics.append(_record(relative, 1, "YAML source cannot be parsed", code="CONFIGURATION_PARSE_ERROR"))
            continue
        for document_index, document in enumerate(documents):
            items = []
            def visit(node, prefix="", ancestors=frozenset()):
                if node is None or id(node) in ancestors:
                    return
                ancestors = ancestors | {id(node)}
                if isinstance(node, MappingNode):
                    for key_node, value_node in node.value:
                        if isinstance(key_node, ScalarNode):
                            key = prefix + ("." if prefix else "") + key_node.value
                            if isinstance(value_node, (MappingNode, SequenceNode)):
                                visit(value_node, key, ancestors)
                            else:
                                items.append((key, key_node.start_mark.line + 1, value_node.value if isinstance(value_node, ScalarNode) else ""))
                elif isinstance(node, SequenceNode):
                    for position, child in enumerate(node.value):
                        key = prefix + f"[{position}]"
                        if isinstance(child, ScalarNode):
                            items.append((key, child.start_mark.line + 1, child.value))
                        else:
                            visit(child, key, ancestors)
            visit(document)
            profile_items = [value for key, _, value in items if key in {"spring.config.activate.on-profile", "spring.profiles"}]
            active_profile = profile
            if len(profile_items) == 1 and re.fullmatch(r"[A-Za-z0-9_.!&|, -]{1,100}", profile_items[0]):
                active_profile = profile_items[0]
            for key, line, value in items:
                retain(key, line, value, document_index, active_profile)
    return declarations, references, diagnostics


def extract(repo: Path) -> dict[str, Any]:
    """Return independently inspectable source records and coverage accounting."""
    repo = repo.absolute()
    result = {name: [] for name in ["types", "type_dependencies", "configuration_classes", "configuration_keys", "configuration_reads", "configuration_bindings", "configuration_references", "diagnostics", "ledger"]}
    units = []
    paths = set()
    for root in _roots(repo, "java_source_roots", "src/main/java"):
        paths.update(source_inventory.iter_source_files(repo, root=root, suffixes={".java"}))
    types, index = {}, defaultdict(list)
    for path in sorted(paths):
        try:
            unit = _Unit(path, repo)
        except OSError:
            result["diagnostics"].append(_record(path.relative_to(repo).as_posix(), 1, "Java source cannot be read", code="UNREADABLE_JAVA_SOURCE"))
            continue
        units.append(unit)
        result["ledger"].append({"family": "java_source_file", "path": unit.relative, "line": 1,
                                 "disposition": "UNRESOLVED" if unit.root.has_error else "EXTRACTED", "evidence": [],
                                 **({"reason": "JAVA_PARSE_ERROR"} if unit.root.has_error else {})})
        if unit.root.has_error:
            result["diagnostics"].append(_record(unit.relative, 1, "Java parse contains unsupported or invalid syntax", code="JAVA_STRUCTURE_PARSE_ERROR"))
        for node in _walk(unit.root):
            if node.type not in TYPE_NODES:
                continue
            name = unit.text(node.child_by_field_name("name"))
            outer = unit.owner(node.parent)
            qualified = (outer["qualified_name"] if outer else unit.package) + "." + name
            qualified = qualified.lstrip(".")
            identity = unit.relative + "#" + qualified
            body = node.child_by_field_name("body")
            item = _record(unit.relative, node.start_point.row + 1, f"Java {node.type.removesuffix('_declaration')} {qualified}",
                           type_id=identity, name=name, qualified_name=qualified, role=_role(unit, node), type_kind=node.type.removesuffix("_declaration"),
                           profile=unit.annotation_strings(unit.annotation(node, "Profile")), fields=[], methods=[])
            item.update(_node=node, _unit=unit)
            unit.types[node.start_byte] = item
            types[identity] = item
            index[qualified].append(identity)
            for child in body.named_children if body is not None else []:
                if child.type in {"field_declaration", "constant_declaration"}:
                    modifiers = next((part for part in child.named_children if part.type == "modifiers"), None)
                    for variable in child.named_children:
                        if variable.type != "variable_declarator":
                            continue
                        item["fields"].append({"name": unit.text(variable.child_by_field_name("name")), "type": unit.text(child.child_by_field_name("type")),
                                               "line": child.start_point.row + 1, "static": bool(re.search(r"\bstatic\b", unit.text(modifiers))),
                                               "final": bool(re.search(r"\bfinal\b", unit.text(modifiers))), "initialized": variable.child_by_field_name("value") is not None, "_node": child})
                elif child.type == "method_declaration":
                    item["methods"].append({"name": unit.text(child.child_by_field_name("name")), "return_type": unit.text(child.child_by_field_name("type")),
                                            "line": child.start_point.row + 1, "_node": child})
            if node.type == "record_declaration":
                parameters = node.child_by_field_name("parameters")
                for parameter in parameters.named_children if parameters is not None else []:
                    if parameter.type == "formal_parameter":
                        item["fields"].append({"name": unit.text(parameter.child_by_field_name("name")), "type": unit.text(parameter.child_by_field_name("type")),
                                               "line": parameter.start_point.row + 1, "static": False, "final": True, "initialized": False, "_node": parameter})

    for unit in units:
        unit.local_names = {qualified.rsplit(".", 1)[-1] for qualified in index if qualified.rpartition(".")[0] == unit.package}
        for item in unit.types.values():
            item["role"] = _role(unit, item["_node"])

    def diagnostic(owner, line, code, message):
        result["diagnostics"].append(_record(owner["path"], line, message, code=code))

    def ledger(family, row, disposition="EXTRACTED", reason=None):
        result["ledger"].append({"family": family, "path": row["path"], "line": row["line"], "disposition": disposition,
                                 "evidence": [], **{key: row[key] for key in ["key", "canonical_key", "read_kind", "type_id"] if key in row}, **({"reason": reason} if reason else {})})

    def dependency(owner, type_name, line, relationship, declaration, **properties):
        candidates = _resolve(type_name, owner["_unit"], owner, index)
        if not candidates:
            return
        row = _record(owner["path"], line, declaration, source_type=owner["type_id"], declared_type=type_name,
                      candidates=candidates, relationship=relationship, **properties)
        if len(candidates) != 1:
            diagnostic(owner, line, "AMBIGUOUS_JAVA_TYPE", "Declared Java type has multiple local definitions: " + type_name)
            ledger("java_type_dependency", row, "UNRESOLVED", "AMBIGUOUS_JAVA_TYPE")
            return
        if candidates[0] == owner["type_id"]:
            return
        row["target_type"] = candidates[0]
        result["type_dependencies"].append(row)
        ledger("java_type_dependency", row)

    # Retain all parsed types. Presentation can hide low-level data models.
    for item in types.values():
        ledger("java_type", item)
        unit, node = item["_unit"], item["_node"]
        for child in node.named_children:
            if child.type in {"superclass", "super_interfaces", "extends_interfaces"}:
                relation = "EXTENDS_TYPE" if child.type in {"superclass", "extends_interfaces"} else "IMPLEMENTS_TYPE"
                declared = []
                for part in child.named_children:
                    declared.extend(part.named_children if part.type == "type_list" else [part])
                for part in declared:
                    raw_types = _type_names(unit.text(part))
                    for position, raw in enumerate(raw_types):
                        relationship = relation if position == 0 else "DEPENDS_ON_TYPE"
                        dependency(item, raw, child.start_point.row + 1, relationship, f"{item['qualified_name']} declares {relationship} {raw}")
        constructors = [child for child in node.child_by_field_name("body").named_children if child.type == "constructor_declaration"] if node.child_by_field_name("body") is not None else []
        spring = item["role"] in {"APPLICATION_SERVICE", "COMPONENT", "CONFIGURATION", "CONTROLLER", "REPOSITORY"}
        lombok_injection = spring and (unit.annotation(node, "RequiredArgsConstructor") is not None or unit.annotation(node, "AllArgsConstructor") is not None)
        for field in item["fields"]:
            raw_types = _type_names(field["type"])
            for raw in raw_types:
                dependency(item, raw, field["line"], "DEPENDS_ON_TYPE", f"{item['qualified_name']}.{field['name']} declares type {raw}", declaration_kind="FIELD")
            explicit = unit.annotation(field["_node"], "Autowired") is not None or unit.annotation(field["_node"], "Inject") is not None
            implicit = lombok_injection and not field["static"] and not field["initialized"] and (field["final"] or unit.annotation(node, "AllArgsConstructor") is not None)
            if raw_types and not field["static"] and (explicit or implicit):
                dependency(item, raw_types[0], field["line"], "INJECTS", f"{item['qualified_name']}.{field['name']} declares injection of {raw_types[0]}",
                           injection_rule="ANNOTATED_FIELD" if explicit else "LOMBOK_CONSTRUCTOR")
        for constructor in constructors:
            explicit = unit.annotation(constructor, "Autowired") is not None or unit.annotation(constructor, "Inject") is not None
            parameters = constructor.child_by_field_name("parameters")
            for parameter in parameters.named_children if parameters is not None else []:
                if parameter.type != "formal_parameter":
                    continue
                raw_types = _type_names(unit.text(parameter.child_by_field_name("type")))
                for raw in raw_types:
                    dependency(item, raw, parameter.start_point.row + 1, "DEPENDS_ON_TYPE", f"{item['qualified_name']} constructor declares type {raw}", declaration_kind="CONSTRUCTOR_PARAMETER")
                if raw_types and (explicit or spring and len(constructors) == 1):
                    dependency(item, raw_types[0], parameter.start_point.row + 1, "INJECTS", f"{item['qualified_name']} constructor declares injection of {raw_types[0]}",
                               injection_rule="ANNOTATED_CONSTRUCTOR" if explicit else "SPRING_SINGLE_CONSTRUCTOR")
        for method in item["methods"]:
            for raw in _type_names(method["return_type"]):
                dependency(item, raw, method["line"], "DEPENDS_ON_TYPE", f"{item['qualified_name']}.{method['name']} declares return type {raw}", declaration_kind="RETURN_TYPE")
            parameters = method["_node"].child_by_field_name("parameters")
            for parameter in parameters.named_children if parameters is not None else []:
                if parameter.type != "formal_parameter":
                    continue
                for raw in _type_names(unit.text(parameter.child_by_field_name("type"))):
                    dependency(item, raw, parameter.start_point.row + 1, "DEPENDS_ON_TYPE", f"{item['qualified_name']}.{method['name']} declares parameter type {raw}", declaration_kind="METHOD_PARAMETER")

    declarations, references, config_diagnostics = _config_sources(repo)
    result["configuration_keys"].extend(declarations)
    result["configuration_references"].extend(references)
    result["diagnostics"].extend(config_diagnostics)
    for row in declarations:
        ledger("configuration_declaration", row)
    for row in references:
        ledger("configuration_reference", row)
    config_fields = defaultdict(lambda: defaultdict(list))
    duplicates = Counter((row["path"], row["document"], row["canonical_key"]) for row in declarations)
    for (path, document, key), count in duplicates.items():
        if count > 1:
            result["diagnostics"].append(_record(path, next(row["line"] for row in declarations if row["path"] == path and row["document"] == document and row["canonical_key"] == key),
                                                    "Duplicate configuration key declaration: " + key, code="DUPLICATE_CONFIGURATION_KEY"))
    for item in types.values():
        unit, node = item["_unit"], item["_node"]
        annotation = unit.annotation(node, "ConfigurationProperties")
        if annotation is None:
            continue
        prefixes = unit.annotation_strings(annotation, "prefix") or unit.annotation_strings(annotation)
        prefix = prefixes[0] if len(prefixes) == 1 and SAFE_KEY.fullmatch(prefixes[0]) else ""
        row = _record(item["path"], annotation.start_point.row + 1, "Configuration properties class " + item["qualified_name"],
                      "java-configuration", type_id=item["type_id"], prefix=prefix, profile=item["profile"])
        result["configuration_classes"].append(row)
        ledger("configuration_class", row, "EXTRACTED" if prefix else "UNRESOLVED", None if prefix else "UNRESOLVED_CONFIGURATION_PREFIX")
        if not prefix:
            diagnostic(item, row["line"], "UNRESOLVED_CONFIGURATION_PREFIX", "Configuration prefix is empty, dynamic, or unsupported")
            continue

        def fields(owner, current_prefix, ancestry=()):
            if owner["type_id"] in ancestry or len(ancestry) >= 5:
                diagnostic(owner, owner["line"], "UNRESOLVED_CONFIGURATION_NESTING", "Configuration nesting is cyclic or exceeds the supported depth")
                return
            for field in owner["fields"]:
                if field["static"]:
                    continue
                key = current_prefix + "." + _kebab(field["name"])
                binding = _record(owner["path"], field["line"], f"Configuration field {owner['qualified_name']}.{field['name']} binds {key}",
                                  "java-configuration", type_id=item["type_id"], declaring_type=owner["type_id"], field=field["name"], key=key,
                                  canonical_key=_canonical(key), profile=item["profile"], binding_kind="CONFIGURATION_PROPERTIES",
                                  prefix_evidence={k: row[k] for k in ["path", "line", "declaration", "extractor"]})
                result["configuration_bindings"].append(binding)
                config_fields[owner["type_id"]][field["name"]].append(binding)
                ledger("configuration_binding", binding)
                names = _type_names(field["type"])
                nested_name = names[-1] if names else ""
                nested = _resolve(nested_name, owner["_unit"], owner, index)
                if len(nested) == 1 and nested[0] != owner["type_id"] and "Map" not in field["type"]:
                    suffix = "[]" if any(token in field["type"] for token in ["List<", "Set<", "Collection<", "[]"]) else ""
                    fields(types[nested[0]], key + suffix, ancestry + (owner["type_id"],))
        fields(item, prefix)

    def read_config(owner, line, key, kind, **extra):
        if not key or not SAFE_KEY.fullmatch(key):
            diagnostic(owner, line, "UNRESOLVED_CONFIGURATION_READ", "Configuration read has no supported static key")
            row = _record(owner["path"], line, "Configuration read has no supported static key")
            ledger("configuration_read", row, "UNRESOLVED", "UNRESOLVED_CONFIGURATION_READ")
            return
        row = _record(owner["path"], line, f"{kind} reads configuration key {key}", "java-configuration", type_id=owner["type_id"],
                      key=key, canonical_key=_canonical(key), read_kind=kind, profile=owner["profile"], **extra)
        result["configuration_reads"].append(row)
        ledger("configuration_read", row)

    for unit in units:
        bindings = []
        for node in _walk(unit.root):
            owner = unit.owner(node)
            if owner is None:
                continue
            if node.type == "variable_declarator" and node.parent.type in {"field_declaration", "local_variable_declaration"}:
                parent = node.parent
                field = parent.type == "field_declaration"
                scope = _nearest(parent, TYPE_NODES if field else {"block", "for_statement", "enhanced_for_statement", "constructor_body"})
                if scope is not None:
                    bindings.append({"name": unit.text(node.child_by_field_name("name")), "raw_type": unit.text(parent.child_by_field_name("type")),
                                     "scope": scope, "start": parent.start_byte, "field": field, "owner": owner})
            elif node.type in {"formal_parameter", "spread_parameter", "catch_formal_parameter"}:
                scope = _nearest(node, METHOD_NODES | {"catch_clause"})
                if scope is not None:
                    bindings.append({"name": unit.text(node.child_by_field_name("name")), "raw_type": unit.text(node.child_by_field_name("type")),
                                     "scope": scope, "start": scope.start_byte, "field": False, "owner": owner})
            elif node.type == "enhanced_for_statement":
                bindings.append({"name": unit.text(node.child_by_field_name("name")), "raw_type": unit.text(node.child_by_field_name("type")),
                                 "scope": node, "start": node.start_byte, "field": False, "owner": owner})
            elif node.type == "lambda_expression":
                parameters = node.child_by_field_name("parameters")
                names = [parameters] if parameters is not None and parameters.type == "identifier" else parameters.named_children if parameters is not None and parameters.type == "inferred_parameters" else []
                for parameter in names:
                    bindings.append({"name": unit.text(parameter), "raw_type": "", "scope": node, "start": node.start_byte, "field": False, "owner": owner})
            # Annotation defaults and configuration scalar values never enter a record.
            if node.type in {"field_declaration", "formal_parameter", "method_declaration"}:
                annotation = unit.annotation(node, "Value")
                if annotation is not None:
                    values = unit.annotation_strings(annotation)
                    keys = sorted({match.group(1) for value in values for match in PLACEHOLDER.finditer(value)})
                    if not keys:
                        read_config(owner, annotation.start_point.row + 1, "", "VALUE_ANNOTATION")
                    for key in keys:
                        read_config(owner, annotation.start_point.row + 1, key, "VALUE_ANNOTATION")
            if node.type in TYPE_NODES | {"method_declaration"}:
                annotation = unit.annotation(node, "ConditionalOnProperty")
                if annotation is not None:
                    prefix = unit.annotation_strings(annotation, "prefix")
                    names = unit.annotation_strings(annotation, "name") or unit.annotation_strings(annotation)
                    for name in names or [""]:
                        key = ((prefix[0].rstrip(".") + ".") if len(prefix) == 1 else "") + name
                        read_config(owner, annotation.start_point.row + 1, key, "CONDITIONAL_ON_PROPERTY")

        def binding_for(receiver, invocation):
            owner = unit.owner(invocation)
            if receiver.type == "field_access" and unit.text(receiver.child_by_field_name("object")) == "this":
                name = unit.text(receiver.child_by_field_name("field"))
                candidates = [binding for binding in bindings if binding["name"] == name and binding["field"] and binding["owner"] is owner]
            elif receiver.type == "identifier":
                name = unit.text(receiver)
                ancestors, parent = [], invocation.parent
                while parent is not None:
                    ancestors.append(parent)
                    parent = parent.parent
                candidates = [binding for binding in bindings if binding["name"] == name and binding["scope"] in ancestors
                              and (binding["field"] or binding["start"] <= invocation.start_byte)
                              and (not binding["field"] or binding["owner"] is owner)]
                if candidates:
                    distance = min(ancestors.index(binding["scope"]) for binding in candidates)
                    candidates = [binding for binding in candidates if ancestors.index(binding["scope"]) == distance]
            else:
                return None
            return candidates[0] if len(candidates) == 1 else None

        def receiver_types(receiver, invocation, depth=0):
            if receiver is None or depth > 3:
                return [], ""
            binding = binding_for(receiver, invocation)
            if binding is not None:
                names = _type_names(binding["raw_type"])
                raw = names[0] if names else ""
                return _resolve(raw, unit, unit.owner(invocation), index), _external_type(raw, unit)
            if receiver.type == "identifier":
                # An in-scope nonmatching variable must shadow a same-named type.
                return _resolve(unit.text(receiver), unit, unit.owner(invocation), index), _external_type(unit.text(receiver), unit)
            if receiver.type == "object_creation_expression":
                raw = unit.text(receiver.child_by_field_name("type"))
                return _resolve(raw, unit, unit.owner(invocation), index), _external_type(raw, unit)
            if receiver.type == "method_invocation":
                parent_types, _ = receiver_types(receiver.child_by_field_name("object"), invocation, depth + 1)
                method_name = unit.text(receiver.child_by_field_name("name"))
                returns = []
                for type_id in parent_types:
                    item = types[type_id]
                    methods = [method for method in item["methods"] if method["name"] == method_name]
                    if len(methods) == 1:
                        returns.extend(_resolve(methods[0]["return_type"], item["_unit"], item, index))
                    if method_name.startswith("get") and len(method_name) > 3:
                        field = method_name[3:4].lower() + method_name[4:]
                        for declaration in item["fields"]:
                            names = _type_names(declaration["type"])
                            if declaration["name"] == field and len(names) == 1:
                                returns.extend(_resolve(names[0], item["_unit"], item, index))
                return sorted(set(returns)), ""
            return [], ""

        for node in _walk(unit.root):
            if node.type != "method_invocation":
                continue
            owner = unit.owner(node)
            receiver = node.child_by_field_name("object")
            if owner is None or receiver is None:
                continue
            method = unit.text(node.child_by_field_name("name"))
            targets, external = receiver_types(receiver, node)
            if external in ENV_TYPES and method in {"getProperty", "getRequiredProperty", "containsProperty"}:
                arguments = node.child_by_field_name("arguments")
                first = arguments.named_children[0] if arguments is not None and arguments.named_children else None
                read_config(owner, node.start_point.row + 1, _literal(unit, first) or "", "ENVIRONMENT")
            if len(targets) > 1:
                diagnostic(owner, node.start_point.row + 1, "AMBIGUOUS_JAVA_CALL_TARGET", "Typed receiver has multiple local declarations")
                ledger("java_typed_call", _record(owner["path"], node.start_point.row + 1, "Ambiguous typed call"), "UNRESOLVED", "AMBIGUOUS_JAVA_CALL_TARGET")
                continue
            if len(targets) != 1:
                continue
            target = types[targets[0]]
            if target["type_id"] != owner["type_id"]:
                row = _record(owner["path"], node.start_point.row + 1, f"{target['qualified_name']}.{method}(...)", source_type=owner["type_id"],
                              target_type=target["type_id"], relationship="CALLS_COMPONENT", method=method, dispatch="DECLARED_TYPE")
                result["type_dependencies"].append(row)
                ledger("java_typed_call", row)
            names = []
            explicit_methods = [item for item in target["methods"] if item["name"] == method]
            if explicit_methods:
                # A custom getter can return another property. Follow only a
                # single direct field return; do not infer JavaBean semantics.
                getter = explicit_methods[0]["_node"] if len(explicit_methods) == 1 else None
                body = getter.child_by_field_name("body") if getter is not None else None
                statements = body.named_children if body is not None else []
                if len(statements) == 1 and statements[0].type == "return_statement" and len(statements[0].named_children) == 1:
                    value = statements[0].named_children[0]
                    getter_unit = target["_unit"]
                    field_names = {field["name"] for field in target["fields"]}
                    parameters = getter.child_by_field_name("parameters")
                    shadowed = {getter_unit.text(parameter.child_by_field_name("name")) for parameter in parameters.named_children} if parameters is not None else set()
                    # A pure return expression can transform a property value
                    # (for example Duration.ofMillis(timeout)). Retain only
                    # field identities, never expressions or scalar literals.
                    for part in _walk(value):
                        if _nearest(part, {"lambda_expression", "class_declaration"}) not in {None, target["_node"]}:
                            continue
                        if part.type == "field_access" and getter_unit.text(part.child_by_field_name("object")) == "this":
                            name = getter_unit.text(part.child_by_field_name("field"))
                            if name in field_names:
                                names.append(name)
                        elif part.type == "identifier":
                            name = getter_unit.text(part)
                            parent = part.parent
                            if name not in field_names or name in shadowed or parent is None:
                                continue
                            if parent.type == "method_invocation" and parent.child_by_field_name("name") == part:
                                continue
                            if parent.type == "field_access":
                                continue
                            names.append(name)
            synthetic = (target["_unit"].annotation(target["_node"], "Data") is not None
                         or target["_unit"].annotation(target["_node"], "Getter") is not None
                         or target["type_kind"] == "record") and not explicit_methods
            expected_field = method[3:4].lower() + method[4:] if method.startswith("get") else method[2:3].lower() + method[3:] if method.startswith("is") else ""
            synthetic = synthetic or (not explicit_methods and any(field["name"] == expected_field and target["_unit"].annotation(field["_node"], "Getter") is not None for field in target["fields"]))
            if synthetic and method.startswith("get") and len(method) > 3:
                names.append(method[3:4].lower() + method[4:])
            if synthetic and method.startswith("is") and len(method) > 2:
                names.append(method[2:3].lower() + method[3:])
            # Records use the field name as an accessor method.
            if synthetic and target["type_kind"] == "record":
                names.append(method)
            matched = False
            for field_name in sorted(set(names)):
                keys = {binding["canonical_key"]: binding for binding in config_fields[target["type_id"]].get(field_name, [])}
                if len(keys) == 1:
                    matched = True
                    binding = next(iter(keys.values()))
                    read_config(owner, node.start_point.row + 1, binding["key"], "PROPERTIES_GETTER",
                                binding_evidence={key: binding[key] for key in ["path", "line", "declaration", "extractor"]},
                                accessor=method, receiver_type=target["qualified_name"],
                                receiver_name=unit.text(receiver) if receiver.type == "identifier" else "this." + unit.text(receiver.child_by_field_name("field")) if receiver.type == "field_access" and unit.text(receiver.child_by_field_name("object")) == "this" else None,
                                source_start_byte=node.start_byte, source_end_byte=node.end_byte)
                elif len(keys) > 1:
                    matched = True
                    diagnostic(owner, node.start_point.row + 1, "AMBIGUOUS_CONFIGURATION_READ", "Configuration accessor has multiple binding contexts")
                    ledger("configuration_read", _record(owner["path"], node.start_point.row + 1, "Ambiguous configuration accessor"), "UNRESOLVED", "AMBIGUOUS_CONFIGURATION_READ")
            if not matched and config_fields[target["type_id"]] and method != "getClass" and method.startswith(("get", "is")):
                diagnostic(owner, node.start_point.row + 1, "UNRESOLVED_CONFIGURATION_ACCESSOR", "Configuration accessor has no supported direct field binding")
                ledger("configuration_read", _record(owner["path"], node.start_point.row + 1, "Unsupported configuration accessor"), "UNRESOLVED", "UNRESOLVED_CONFIGURATION_ACCESSOR")

    # Declared interface dependencies never select an implementation bean.
    implementations = defaultdict(set)
    for row in result["type_dependencies"]:
        if row["relationship"] == "IMPLEMENTS_TYPE":
            implementations[row["target_type"]].add(row["source_type"])
    for row in result["type_dependencies"]:
        target = types[row["target_type"]]
        if target["type_kind"] != "interface" or row["relationship"] not in {"INJECTS", "CALLS_COMPONENT"}:
            continue
        row["dispatch"] = "DECLARED_INTERFACE"
        row["implementation_candidates"] = sorted(types[identity]["qualified_name"] for identity in implementations[target["type_id"]])
        if len(row["implementation_candidates"]) > 1:
            source = types[row["source_type"]]
            diagnostic(source, row["line"], "AMBIGUOUS_JAVA_INTERFACE_DISPATCH", "Declared interface has multiple local implementations; no runtime implementation is selected")

    # Strip parser nodes and byte buffers from the reusable records.
    result["types"] = [{key: value for key, value in item.items() if not key.startswith("_") and key not in {"fields", "methods"}} for item in types.values()]
    for key in result:
        if isinstance(result[key], list):
            result[key].sort(key=lambda row: (row.get("path", ""), row.get("line", 0), row.get("declaration", ""), row.get("relationship", "")))
    result["statistics"] = {"java_files": len(units), "java_types": len(types), "type_dependencies": len(result["type_dependencies"]),
                            "configuration_classes": len(result["configuration_classes"]), "configuration_keys": len(result["configuration_keys"]),
                            "configuration_bindings": len(result["configuration_bindings"]), "configuration_reads": len(result["configuration_reads"]),
                            "configuration_references": len(result["configuration_references"]), "diagnostics": len(result["diagnostics"]),
                            "ledger_counts": dict(sorted(Counter((row["family"] + ":" + row["disposition"]) for row in result["ledger"]).items()))}
    return result


def add_to_graph(graph, repo: Path, repository: str, component_by_path: dict[str, str]) -> dict[str, Any]:
    """Add source-backed detail; preserve existing exact class node identities."""
    extracted = extract(repo)
    type_nodes, evidence_by_type = {}, {}
    ledger = [dict(row) for row in extracted["ledger"]]
    evidence_at = defaultdict(set)

    def evidence(row):
        path = (repo / row["path"]).relative_to(graph.workspace).as_posix()
        identity = graph.add_evidence(repository, path, row["line"], row["declaration"], row.get("extractor", "java-structure"))
        evidence_at[(row["path"], row["line"])].add(identity)
        return identity

    root_id = next((node["id"] for node in graph.nodes.values() if node.get("repository") == repository and node["type"] in {"SERVICE", "APPLICATION"}), None)
    for row in extracted["ledger"]:
        if row["family"] == "java_source_file":
            evidence(_record(row["path"], row["line"], "Parsed Java source", "java-structure"))
    for row in extracted["types"]:
        ev = evidence(row)
        path = (repo / row["path"]).relative_to(graph.workspace).as_posix()
        previous_id = component_by_path.get(row["path"])
        previous = graph.nodes.get(previous_id, {})
        primary = Path(row["path"]).stem == row["name"]
        if primary and previous.get("properties", {}).get("detail_level") == "CLASS":
            identity = previous_id
            graph.add_node(identity, "COMPONENT", row["name"], repository, dimensions=("RUNTIME", "BUSINESS"),
                           component_kind=row["role"], functional_role="Declares Java type " + row["qualified_name"],
                           business_meaning="Static source structure; business responsibility requires review", source_paths=(path,), evidence=(ev,),
                           properties={"qualified_name": row["qualified_name"], "type_kind": row["type_kind"], "profiles": row["profile"], "detail_level": "CLASS"})
            if row["role"] != "JAVA_TYPE":
                graph.nodes[identity]["component_kind"] = row["role"]
        else:
            identity = _sid("component:java-type", repository, row["type_id"])
            graph.add_node(identity, "COMPONENT", row["name"], repository, dimensions=("RUNTIME", "BUSINESS"),
                           component_kind=row["role"], functional_role="Declares Java type " + row["qualified_name"],
                           business_meaning="Static source structure; business responsibility requires review", source_paths=(path,), evidence=(ev,),
                           properties={"qualified_name": row["qualified_name"], "type_kind": row["type_kind"], "profiles": row["profile"], "detail_level": "CLASS"})
            if previous_id and previous_id != identity:
                graph.add_edge(previous_id, identity, "CONTAINS_COMPONENT", "RUNTIME", (ev,), assertion_status="INFERRED")
            elif root_id:
                graph.add_edge(root_id, identity, "CONTAINS_COMPONENT", "RUNTIME", (ev,))
        if primary or row["path"] not in component_by_path:
            component_by_path[row["path"]] = identity
        type_nodes[row["type_id"]] = identity
        evidence_by_type[row["type_id"]] = ev

    for row in extracted["configuration_classes"]:
        ev = evidence(row)
        identity = type_nodes[row["type_id"]]
        graph.nodes[identity]["evidence"] = sorted(set(graph.nodes[identity]["evidence"]) | {ev})
        graph.nodes[identity].setdefault("properties", {}).update(configuration_prefix=row["prefix"])

    config_nodes, source_nodes = {}, {}
    def config_node(row):
        canonical = row["canonical_key"]
        identity = _sid("configuration-key", repository, canonical)
        ev = evidence(row)
        graph.add_node(identity, "CONFIGURATION_KEY", row["key"], repository, dimensions=("RUNTIME",), component_kind=None,
                       functional_role="Names a configuration property declaration or read", business_meaning="Static configuration dependency; active value is unknown",
                       source_paths=((repo / row["path"]).relative_to(graph.workspace).as_posix(),), evidence=(ev,),
                       properties={"key": row["key"], "canonical_key": canonical, "value_retained": False})
        config_nodes[canonical] = identity
        return identity, ev

    for row in extracted["configuration_keys"]:
        target, ev = config_node(row)
        source_key = (row["path"], row["profile"], row["document"])
        source_id = _sid("configuration-source", repository, *source_key)
        path = (repo / row["path"]).relative_to(graph.workspace).as_posix()
        if source_key not in source_nodes:
            graph.add_node(source_id, "CONFIGURATION_SOURCE", Path(row["path"]).name + " [" + row["profile"] + "]", repository,
                           dimensions=("RUNTIME",), component_kind=None, functional_role="Declares configuration keys in a source document",
                           business_meaning="Configuration declarations do not establish the active runtime profile", source_paths=(path,), evidence=(ev,),
                           properties={"profile": row["profile"], "document": row["document"], "profile_selected": False, "value_retained": False})
            source_nodes[source_key] = source_id
            if root_id:
                graph.add_edge(root_id, source_id, "CONTAINS_COMPONENT", "RUNTIME", (ev,))
        graph.add_edge(source_id, target, "DECLARES_CONFIG", "RUNTIME", (ev,), properties={"profile": row["profile"], "document": row["document"]})
    for row in extracted["configuration_bindings"] + extracted["configuration_reads"]:
        target, ev = config_node(row)
        source = type_nodes.get(row["type_id"])
        evs = {ev}
        for key in ["prefix_evidence", "binding_evidence"]:
            if row.get(key):
                evs.add(evidence(row[key]))
        if source:
            relation = "BINDS_CONFIG" if "binding_kind" in row else "READS_CONFIG"
            graph.add_edge(source, target, relation, "RUNTIME", evs,
                           properties={key: row[key] for key in ["binding_kind", "read_kind", "profile"] if key in row})
    for row in extracted["configuration_references"]:
        target, ev = config_node(row)
        source = _sid("configuration-key", repository, _canonical(row["source_key"]))
        if source in graph.nodes:
            graph.add_edge(source, target, "REFERENCES_CONFIG", "RUNTIME", (ev,), properties={"profiles": [row["profile"]], "documents": [row["document"]]})
    for row in extracted["type_dependencies"]:
        source, target = type_nodes[row["source_type"]], type_nodes[row["target_type"]]
        evs = {evidence(row), evidence_by_type[row["target_type"]]}
        properties = {key: row[key] for key in ["declared_type", "method", "dispatch", "declaration_kind", "injection_rule", "implementation_candidates"] if key in row}
        graph.add_edge(source, target, row["relationship"], "RUNTIME", evs, properties=properties)
    for row in extracted["diagnostics"]:
        evidence(row)
        graph.diagnostic(row["code"], f"Line {row['line']}: {row['declaration']}", repository, (repo / row["path"]).relative_to(graph.workspace).as_posix())
    for row in ledger:
        row["evidence"] = sorted(evidence_at[(row["path"], row["line"])])
    return {"statistics": extracted["statistics"], "ledger": ledger,
            "configuration_reads": [{**row, "component_id": type_nodes.get(row["type_id"]), "configuration_key_node": config_nodes.get(row["canonical_key"])} for row in extracted["configuration_reads"]],
            "configuration_bindings": extracted["configuration_bindings"]}


__all__ = ["extract", "add_to_graph"]
