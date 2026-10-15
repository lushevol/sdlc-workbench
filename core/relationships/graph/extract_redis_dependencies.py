"""Extract Spring Redis configuration and typed client declarations."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml
from tree_sitter import Language, Parser
import tree_sitter_java
from yaml.nodes import MappingNode, ScalarNode

from ai_sdlc_workbench.relationships.graph.source_inventory import iter_source_files


CLIENT_TYPES = {
    "org.springframework.data.redis.core.RedisTemplate",
    "org.springframework.data.redis.core.StringRedisTemplate",
    "org.springframework.data.redis.core.RedisOperations",
    "org.springframework.data.redis.core.ReactiveRedisTemplate",
    "org.springframework.data.redis.core.ReactiveStringRedisTemplate",
    "org.springframework.data.redis.core.ReactiveRedisOperations",
    "org.springframework.data.redis.connection.RedisConnectionFactory",
    "org.springframework.data.redis.connection.ReactiveRedisConnectionFactory",
    "org.springframework.data.redis.connection.lettuce.LettuceConnectionFactory",
    "org.springframework.data.redis.connection.jedis.JedisConnectionFactory",
    "org.springframework.data.redis.cache.RedisCacheManager",
    "org.springframework.data.redis.cache.RedisCacheWriter",
}
CONFIG_PREFIXES = ("spring.redis.", "spring.data.redis.")
CONFIG_LEAVES = {
    "host", "port", "url", "database", "username", "password", "client-type",
    "timeout", "connect-timeout", "ssl", "ssl.enabled", "ssl.bundle",
    "cluster.nodes", "cluster.max-redirects", "sentinel.master", "sentinel.nodes",
    "sentinel.username", "sentinel.password", "sentinel.data-node.username",
    "sentinel.data-node.password", "lettuce.shutdown-timeout",
    "lettuce.cluster.refresh.adaptive", "lettuce.cluster.refresh.period",
    "lettuce.cluster.refresh.dynamic-refresh-sources",
}
POOL_LEAVES = {"enabled", "max-active", "max-idle", "min-idle", "max-wait", "time-between-eviction-runs"}


def is_redis_key(key: str) -> bool:
    for prefix in CONFIG_PREFIXES:
        if not key.startswith(prefix):
            continue
        leaf = key[len(prefix):]
        if leaf in CONFIG_LEAVES:
            return True
        return any(leaf.startswith(client + ".pool.") and leaf[len(client + ".pool."):] in POOL_LEAVES
                   for client in ("lettuce", "jedis"))
    return False


def extract(repo: Path) -> dict[str, list[dict[str, Any]]]:
    repo = repo.absolute()
    hits: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []

    def record(path: Path, line: int, declaration: str) -> None:
        hits.append({"path": path.relative_to(repo).as_posix(), "line": line, "declaration": declaration})

    for path in iter_source_files(repo, root=repo / "src/main/resources", suffixes={".yml", ".yaml", ".properties"}):
        if not path.name.startswith("application"):
            continue
        source = path.read_text(encoding="utf-8", errors="replace")
        if path.suffix == ".properties":
            for line, raw in enumerate(source.splitlines(), 1):
                stripped = raw.strip()
                if not stripped or stripped.startswith(("#", "!")):
                    continue
                match = re.match(r"([^\s:=]+)\s*(?:[=:]\s*|\s+)(.+)$", stripped)
                if match and is_redis_key(match.group(1)) and match.group(2).strip():
                    record(path, line, "Spring Redis configuration key: " + match.group(1))
            continue
        try:
            documents = list(yaml.compose_all(source, Loader=yaml.SafeLoader))
        except yaml.YAMLError:
            diagnostics.append({"code": "REDIS_CONFIGURATION_PARSE_ERROR", "path": path.relative_to(repo).as_posix(),
                                "line": 1, "message": "Redis configuration cannot be inspected because YAML parsing failed"})
            continue

        def configuration(node: Any, prefix: tuple[str, ...] = ()) -> None:
            if not isinstance(node, MappingNode):
                return
            for key_node, value_node in node.value:
                if not isinstance(key_node, ScalarNode):
                    continue
                parts = (*prefix, *key_node.value.split("."))
                key = ".".join(parts)
                if isinstance(value_node, MappingNode):
                    configuration(value_node, parts)
                elif is_redis_key(key) and value_node.tag != "tag:yaml.org,2002:null" and (
                        getattr(value_node, "value", None) not in (None, "", [])):
                    record(path, key_node.start_mark.line + 1, "Spring Redis configuration key: " + key)

        for document in documents:
            configuration(document)

    for path in iter_source_files(repo, root=repo / "src/main/java", suffixes={".java"}):
        encoded = path.read_bytes()
        root = Parser(Language(tree_sitter_java.language())).parse(encoded).root_node

        def text(node: Any) -> str:
            return encoded[node.start_byte:node.end_byte].decode("utf-8", errors="replace") if node else ""

        def walk(node: Any):
            yield node
            for child in node.named_children:
                yield from walk(child)

        imports: dict[str, set[str]] = {}
        for node in root.named_children:
            if node.type != "import_declaration":
                continue
            name_node = next((child for child in node.named_children if child.type in {"scoped_identifier", "identifier"}), None)
            imported = text(name_node)
            if imported in CLIENT_TYPES and not any(child.type == "asterisk" for child in node.named_children):
                imports.setdefault(imported.rsplit(".", 1)[-1], set()).add(imported)
        for node in walk(root):
            if node.type not in {"field_declaration", "local_variable_declaration", "formal_parameter",
                                 "spread_parameter", "method_declaration", "object_creation_expression"} or node.has_error:
                continue
            type_node = node.child_by_field_name("type")
            type_name = text(type_node).split("<", 1)[0].strip().removesuffix("[]")
            identity = type_name if type_name in CLIENT_TYPES else (
                next(iter(imports[type_name])) if len(imports.get(type_name, set())) == 1 else None)
            if identity is not None:
                record(path, type_node.start_point.row + 1, "Redis typed client declaration: " + identity)
    unique = {(row["path"], row["line"], row["declaration"]): row for row in hits}
    return {"hits": [unique[key] for key in sorted(unique)], "diagnostics": diagnostics}
