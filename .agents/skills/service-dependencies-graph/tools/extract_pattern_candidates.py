"""High-recall dependency-shaped source search.

This pass deliberately records candidates instead of asserting relationships.
Typed extractors remain the source of canonical graph edges.  The pattern
census makes missed declarations visible with stable line evidence so a
reviewer can inspect only ambiguous or unsupported cases.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Iterable
from urllib.parse import urlsplit

from .source_inventory import iter_source_files


_URL = re.compile(r"(?P<quote>[\"'])(?P<value>(?:https?|wss?)://[^\"']+|//[^\"']+|/(?:api|auth|graphql|events|ws|socket|v[0-9]+)[^\"']*)(?P=quote)", re.I)
_HTTP_CALL_URL = re.compile(
    r"\b(?:fetch|axios(?:\.[A-Za-z]+)?|(?:client|http|api|request|requests?)\.(?:get|post|put|patch|delete|request))\s*"
    r"\(\s*(?P<quote>[\"'])(?P<value>/[^\"']+)(?P=quote)", re.I,
)
_CONFIG = re.compile(
    r"(?:process\.env\.(?P<node>[A-Za-z_][A-Za-z0-9_]*)|import\.meta\.env\.(?P<meta>[A-Za-z_][A-Za-z0-9_]*)|"
    r"System\.getenv\s*\(\s*[\"'](?P<java>[A-Za-z0-9_.-]+)[\"']|"
    r"@Value\s*\(\s*[\"']\$\{(?P<value>[A-Za-z0-9_.-]+)[^}]*\}\s*[\"']|"
    r"\$\{(?P<template>[A-Za-z_][A-Za-z0-9_.-]*)\})"
)
_ENV_CONFIG = re.compile(r"^\s*(?P<env>[A-Za-z_][A-Za-z0-9_]*)\s*=")
_KAFKA = re.compile(
    r"(?:@KafkaListener\b[^\n]*?topics?\s*=\s*[\"'](?P<annotation>[^\"']+)|"
    r"(?:KafkaTemplate|kafkaTemplate)\b[^\n]*?\.(?:send|sendDefault)\s*\(\s*[\"'](?P<send>[^\"']+)|"
    r"\b(?:from|to|toD)\s*\(\s*[\"']kafka:(?P<camel>[^\"']+))",
    re.I,
)
_SQL = re.compile(
    r"\b(?:select\b[\s\S]{0,300}?\bfrom|insert\s+into|update|delete\s+from)\s+[`\"']?(?P<table>[A-Za-z_][\w.$-]*)",
    re.I,
)
_IMPORT = re.compile(
    r"(?:\bimport\s+(?:[\s\S]{0,180}?\s+from\s+)?|\brequire\s*\(|\bSystem\.import\s*\()\s*[\"'](?P<module>[^\"']+)[\"']",
    re.I,
)
_NGINX = re.compile(r"\b(?P<directive>location|proxy_pass|rewrite|upstream)\b\s+(?P<value>[^;{\n]+)", re.I)
_CODE_CONFIG_SUFFIXES = {'.java', '.kt', '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs', '.mts', '.cts',
                         '.py', '.go', '.rs', '.cs', '.kts', '.gradle', '.properties', '.yaml', '.yml',
                         '.toml', '.ini', '.conf', '.j2', '.sql', '.graphql', '.graphqls', '.gql', '.proto',
                         '.html', '.ejs'}


def _is_env_file(path: Path) -> bool:
    return path.name == '.env' or path.name.startswith('.env.')


def _is_import_map(path: Path) -> bool:
    return 'importmap' in re.sub(r'[^a-z0-9]', '', path.stem.lower())


def _safe_value(value: str, *, url: bool = False) -> str:
    value = value.strip()
    if url:
        try:
            parsed = urlsplit(value)
        except ValueError:
            return '<redacted>'
        if parsed.username or parsed.password:
            return '<redacted>'
        value = value.split('#', 1)[0].split('?', 1)[0]
    if re.search(r"(?:password|passwd|secret|token|credential|authorization|client_secret)", value, re.I):
        return '<redacted>'
    return value[:240]


def _line_at(text: str, offset: int) -> int:
    return text.count('\n', 0, max(0, offset)) + 1


def _row(repository: str, workspace: Path, path: Path, line: int, family: str,
         pattern_id: str, value: str, disposition: str = 'CANDIDATE', **extra) -> dict:
    relative = path.relative_to(workspace).as_posix()
    row = {
        'id': 'pattern:' + hashlib.sha256('|'.join((repository, relative, str(line), family, pattern_id, value)).encode()).hexdigest()[:24],
        'repository': repository, 'path': relative, 'line': line, 'family': family,
        'pattern_id': pattern_id, 'value': value, 'disposition': disposition,
        'basis': 'deterministic-search-pattern', 'review_status': 'PENDING',
    }
    row.update(extra)
    return row


def scan_files(workspace: Path, repository: str, paths: Iterable[Path]) -> dict:
    candidates: list[dict] = []
    scanned = 0
    skipped = []
    for path in sorted(paths):
        # Robot suites and large fixture JSON files have their own bounded
        # extractor.  Searching every variable interpolation there creates
        # noise without improving cross-repository identity resolution.
        if path.suffix in {'.robot', '.resource'}:
            skipped.append({'path': path.relative_to(workspace).as_posix(), 'reason': 'SPECIALIZED_TEST_EXTRACTOR'})
            continue
        if path.suffix == '.json' and path.name not in {'package.json', 'tsconfig.json', 'jsconfig.json'} and not _is_import_map(path):
            continue
        if path.suffix not in _CODE_CONFIG_SUFFIXES and path.suffix != '.json' and not _is_env_file(path):
            continue
        try:
            if path.stat().st_size > 2 * 1024 * 1024:
                skipped.append({'path': path.relative_to(workspace).as_posix(), 'reason': 'SOURCE_SIZE_LIMIT'})
                continue
            text = path.read_text(encoding='utf-8', errors='replace')
        except OSError:
            skipped.append({'path': path.relative_to(workspace).as_posix(), 'reason': 'UNREADABLE_SOURCE'})
            continue
        scanned += 1
        lines = text.splitlines()
        file_values: set[tuple[str, str]] = set()
        for number, line in enumerate(lines, 1):
            for match in _URL.finditer(line):
                value = _safe_value(match.group('value'), url=True)
                key = ('HTTP_ENDPOINT', value)
                if key not in file_values:
                    file_values.add(key)
                    candidates.append(_row(repository, workspace, path, number, 'HTTP_ENDPOINT', 'url-literal', value))
            for match in _HTTP_CALL_URL.finditer(line):
                value = _safe_value(match.group('value'), url=True)
                key = ('HTTP_ENDPOINT', value)
                if key not in file_values:
                    file_values.add(key)
                    candidates.append(_row(repository, workspace, path, number, 'HTTP_ENDPOINT', 'http-call-url-literal', value))
            config_matches = _CONFIG.finditer(line) if path.suffix in _CODE_CONFIG_SUFFIXES else ()
            if _is_env_file(path):
                config_matches = _ENV_CONFIG.finditer(line)
            for match in config_matches:
                env_name = match.groupdict().get('env')
                value = env_name or next((match.group(name) for name in ('node', 'meta', 'java', 'value', 'template') if match.group(name)), '')
                value = value if env_name else _safe_value(value)
                key = ('CONFIG_READ', value)
                if key not in file_values:
                    file_values.add(key)
                    candidates.append(_row(repository, workspace, path, number, 'CONFIG_READ', 'configuration-access', value))
            for match in _KAFKA.finditer(line):
                value = next((match.group(name) for name in ('annotation', 'send', 'camel') if match.group(name)), '')
                value = _safe_value(value)
                key = ('MESSAGE_CHANNEL', value)
                if key not in file_values:
                    file_values.add(key)
                    candidates.append(_row(repository, workspace, path, number, 'MESSAGE_CHANNEL', 'kafka-channel', value))
            for match in _SQL.finditer(line):
                value = _safe_value(match.group('table'))
                key = ('DATABASE_TABLE', value)
                if key not in file_values:
                    file_values.add(key)
                    candidates.append(_row(repository, workspace, path, number, 'DATABASE_TABLE', 'sql-table', value))
            for match in _IMPORT.finditer(line):
                module = _safe_value(match.group('module'))
                if module and not module.startswith(('http://', 'https://', '//')):
                    key = ('MODULE_IMPORT', module)
                    if key not in file_values:
                        file_values.add(key)
                        candidates.append(_row(repository, workspace, path, number, 'MODULE_IMPORT', 'module-import', module))
            if path.suffix in {'.conf', '.j2'}:
                for match in _NGINX.finditer(line):
                    raw_value = match.group('value')
                    value = _safe_value(raw_value, url=bool(re.search(r'(?:https?|wss?)://|//', raw_value, re.I)))
                    key = ('GATEWAY_ROUTE', value)
                    if key not in file_values:
                        file_values.add(key)
                        candidates.append(_row(repository, workspace, path, number, 'GATEWAY_ROUTE', 'nginx-directive', value))
        # Re-scan HTTP call syntax over the complete file so a bounded
        # multiline call such as fetch(\n  "/orders"\n) remains discoverable.
        for match in _HTTP_CALL_URL.finditer(text):
            value = _safe_value(match.group('value'), url=True)
            key = ('HTTP_ENDPOINT', value)
            if key not in file_values:
                file_values.add(key)
                candidates.append(_row(repository, workspace, path, _line_at(text, match.start()),
                                       'HTTP_ENDPOINT', 'http-call-url-literal', value))
        if path.suffix in {'.graphql', '.graphqls', '.gql'}:
            schema_line = next((index for index, line in enumerate(lines, 1)
                                if re.search(r'^\s*(?:type|schema|directive|extend)\b', line)), 1)
            candidates.append(_row(repository, workspace, path, schema_line,
                                   'GRAPHQL_SCHEMA', 'graphql-schema-declaration', path.name))
    unique = {row['id']: row for row in candidates}
    return {
        'scanned_files': scanned,
        'skipped_files': sorted(skipped, key=lambda row: row['path']),
        'candidates': sorted(unique.values(), key=lambda row: (row['repository'], row['path'], row['line'], row['family'], row['id'])),
    }


def scan_repository(workspace: Path, repository: str, root: Path) -> dict:
    """Scan the same included source boundary used by the census."""
    return scan_files(workspace, repository, iter_source_files(root, root=root))
