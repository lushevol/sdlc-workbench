#!/usr/bin/env python3
"""Extract database tables and Kafka topics from runtime client declarations.

Database tables intentionally come from application client code (Spring Data,
JPA mappings, native repository queries, and JdbcTemplate calls). Migration SQL
is never read because it describes ownership/history, not necessarily runtime use.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from ai_sdlc_workbench.relationships.graph.extract_kafka_dependencies import extract_kafka
from ai_sdlc_workbench.relationships.graph.source_inventory import iter_source_files

# Keep the full annotation body so both positional Spring Data annotations and
# named JPA/Spring Data forms (`name =` and `value =`) resolve to the same
# table declaration.  A body parser is used below because annotations can
# contain additional attributes before the table name.
TABLE_ANNOTATION = re.compile(r"@Table\s*\((?P<body>[^)]*)\)", re.S)
# Framework configuration can declare a runtime table without an entity class
# (for example ShedLock and outbox/event stores).  These declarations are
# explicit table identities, but the static source does not prove the exact
# read/write operations, so rows are emitted as inferred READ_WRITE access.
TABLE_CONFIGURATION = re.compile(
    r"\.(?P<method>withTableName|tableName)\s*\(\s*[\"'](?P<name>[^\"']+)[\"']\s*\)",
    re.S,
)
CLASS = re.compile(r"\bclass\s+(\w+)")
REPOSITORY = re.compile(r"\binterface\s+(\w+)\s+extends\s+[\w.]*Repository\s*<\s*(\w+)\s*,", re.S)
BASE_MAPPER = re.compile(r"\binterface\s+(\w+)\s+extends\s+[\w.]*BaseMapper\s*<\s*(\w+)\s*>", re.S)
SQL_TABLE = re.compile(r"\b(?:from|join|update|into|delete\s+from)\s+([A-Za-z_][\w.$]*)", re.I)
WRITE_SQL = re.compile(r"\b(?:insert\s+into|update|delete\s+from)\b", re.I)
NATIVE_QUERY = re.compile(r"@Query\s*\(\s*(?:value\s*=\s*)?[\"']([^\"']+)[\"'](?:(?!\)).)*nativeQuery\s*=\s*true(?:(?!\)).)*\)", re.I | re.S)
JDBC_CALL = re.compile(r"\b(?:jdbcTemplate|namedParameterJdbcTemplate)\.\w+\s*\(\s*[\"']([^\"']+)[\"']", re.I | re.S)
CONFIG_TOPIC = re.compile(r"(?im)^[ \t]*([\w.-]*(?:topic|route)[\w.-]*)[ \t]*:[ \t]*(?:kafka://|kafka:)?([^\s?#]+)")
JAVA_TOPIC_LITERAL = re.compile(r"\b([A-Za-z_]\w*(?:TOPIC|Topic)\w*)\s*=\s*[\"']([^\"']+)[\"']")
TOPIC_SECTION = re.compile(r"(?m)^([ \t]*)topic:[ \t]*$\n((?:(?:\1[ \t]+)[^\n]*\n?)*)")


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def topic_direction(key: str, topic: str) -> str:
    clue = f"{key} {topic}".lower()
    if any(word in clue for word in ("input", "inbound", "consumer", "_in", "-in", "record_in")):
        return "CONSUMES"
    if any(word in clue for word in ("output", "outbound", "publish", "producer", "send", "enriched", "_out", "-out")):
        return "PUBLISHES"
    return "CONFIGURED"


def table_annotation_name(match: re.Match[str]) -> str | None:
    """Return a literal table name from a ``@Table`` annotation.

    Spring Data accepts a positional value (``@Table("orders")``), while JPA
    and Spring Data also accept ``name =`` or ``value =``.  Keep dynamic or
    non-literal expressions unresolved by returning ``None``.
    """
    body = match.group("body")
    named = re.search(r"\b(?:name|value)\s*=\s*[\"']([^\"']+)[\"']", body)
    if named:
        return named.group(1)
    positional = re.match(r"\s*[\"']([^\"']+)[\"']", body)
    return positional.group(1) if positional else None


def extract(repo: Path) -> dict[str, list[dict[str, Any]]]:
    java_root = repo / "src" / "main" / "java"
    resource_root = repo / "src" / "main" / "resources"
    entities: dict[str, tuple[str, str, int]] = {}
    classes: dict[str, tuple[str, int]] = {}
    files: list[tuple[Path, str]] = []
    if java_root.exists():
        for path in iter_source_files(repo, root=java_root, suffixes={'.java'}):
            text = read_text(path)
            if text is None:
                continue
            files.append((path, text))
            table = TABLE_ANNOTATION.search(text)
            table_name = table_annotation_name(table) if table else None
            klass = CLASS.search(text)
            if klass:
                classes[klass.group(1)] = (
                    path.relative_to(repo).as_posix(), line_number(text, klass.start())
                )
            if table_name and klass:
                entities[klass.group(1)] = (
                    table_name.lower(), path.relative_to(repo).as_posix(), line_number(text, table.start())
                )

    # Keep declarations until canonical graph aggregation. A table/path/access
    # key loses separate clients and source lines within the same source file.
    tables: list[dict[str, Any]] = []
    referenced_entities: set[str] = set()
    for _, text in files:
        for declaration in (REPOSITORY.search(text), BASE_MAPPER.search(text)):
            if declaration and declaration.group(2) in entities:
                referenced_entities.add(declaration.group(2))
    # An entity mapping is useful architecture evidence even when the
    # repository adapter is generated, inherited, or outside the scanned
    # source tree. Keep it as an inferred row so consumers can see the table
    # boundary without claiming that a concrete CRUD call was observed.
    for entity, (table, entity_path, entity_line) in entities.items():
        if entity in referenced_entities:
            continue
        tables.append({
            "name": table,
            "access": "READ_WRITE",
            "client": "SPRING_DATA_ENTITY",
            "path": entity_path,
            "line": entity_line,
            "related_paths": [entity_path],
            "assertion_status": "INFERRED",
            "mapping_kind": "ENTITY",
        })
    for path, text in files:
        relative = path.relative_to(repo).as_posix()
        repository = REPOSITORY.search(text)
        if repository and repository.group(2) in entities:
            table, entity_path, entity_line = entities[repository.group(2)]
            tables.append({
                "name": table, "access": "READ_WRITE", "client": "SPRING_DATA",
                "path": relative, "line": line_number(text, repository.start()),
                "related_paths": [relative, entity_path], "entity_line": entity_line,
                "assertion_status": "INFERRED",
            })
        mapper = BASE_MAPPER.search(text)
        if mapper and mapper.group(2) in classes:
            entity = mapper.group(2)
            entity_path, entity_line = classes[entity]
            table = entities.get(entity, (camel_to_snake(entity), entity_path, entity_line))[0]
            tables.append({
                "name": table, "access": "READ_WRITE", "client": "MYBATIS_PLUS_CONVENTION",
                "path": relative, "line": line_number(text, mapper.start()),
                "related_paths": [relative, entity_path], "entity_line": entity_line,
                "assertion_status": "INFERRED", "score": 0.75,
            })
        client_queries = [(match, "NATIVE_QUERY") for match in NATIVE_QUERY.finditer(text)]
        client_queries.extend((match, "JDBC_TEMPLATE") for match in JDBC_CALL.finditer(text))
        for declaration, client in client_queries:
            sql = declaration.group(1)
            for match in SQL_TABLE.finditer(sql):
                table = match.group(1).split(".")[-1].lower()
                access = "READ" if match.group(0).lstrip().split(None, 1)[0].upper() in {"FROM", "JOIN"} else "WRITE"
                tables.append({
                    "name": table, "access": access, "client": client,
                    "path": relative, "line": line_number(text, declaration.start()),
                    "related_paths": [relative],
                })
        for declaration in TABLE_CONFIGURATION.finditer(text):
            tables.append({
                "name": declaration.group("name").lower(),
                "access": "READ_WRITE",
                "client": "FRAMEWORK_CONFIG",
                "path": relative,
                "line": line_number(text, declaration.start()),
                "related_paths": [relative],
                "assertion_status": "INFERRED",
                "configuration_method": declaration.group("method"),
            })

    mapper_root = resource_root / "mapperxml"
    if mapper_root.exists():
        for path in iter_source_files(repo, root=mapper_root, suffixes={'.xml'}):
            text = read_text(path)
            if text is None:
                continue
            relative = path.relative_to(repo).as_posix()
            sql_text = re.sub(r"<!--.*?-->|<[^>]+>", lambda item: "\n" * item.group(0).count("\n"), text, flags=re.S)
            for match in SQL_TABLE.finditer(sql_text):
                table = match.group(1).split(".")[-1].lower()
                operation = match.group(0).lstrip().split(None, 1)[0].upper()
                access = "READ" if operation in {"FROM", "JOIN"} else "WRITE"
                tables.append({
                    "name": table, "access": access, "client": "MYBATIS_MAPPER",
                    "path": relative, "line": line_number(sql_text, match.start()),
                    "related_paths": [relative],
                })

    kafka = extract_kafka(repo)
    return {"tables": sorted(tables, key=lambda item: (item["name"], item["path"], item["line"], item["client"], item["access"])),
            "topics": kafka["topics"], "diagnostics": kafka["diagnostics"]}


def camel_to_snake(value: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    args = parser.parse_args()
    print(json.dumps(extract(args.repository.resolve()), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
