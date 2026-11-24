"""High-recall dependency-shaped source search.

This pass deliberately records candidates instead of asserting relationships.
Typed extractors remain the source of canonical graph edges.  The pattern
census makes missed declarations visible with stable line evidence so a
reviewer can inspect only ambiguous or unsupported cases.
"""
from __future__ import annotations

from bisect import bisect_right
import hashlib
import re
from pathlib import Path
from typing import Iterable
from urllib.parse import urlsplit

from .dependency_patterns import PATTERNS
from .discovery_sources import MAX_TEXT_BYTES, decode_discovery_text, discovery_inventory


_URL = re.compile(r"(?P<quote>[\"'`])(?P<value>(?:https?|wss?)://[^\"'`]+|//[^\"'`]+|/(?:api|auth|graphql|events|ws|socket|v[0-9]+)[^\"'`]*)(?P=quote)", re.I)
_HTTP_CALL_URL = re.compile(
    r"\b(?:fetch|axios(?:\.[A-Za-z]+)?|(?:client|http|api|request|requests?)\.(?:get|post|put|patch|delete|request))\s*"
    r"\(\s*(?P<quote>[\"'`])(?P<value>/[^\"'`]+)(?P=quote)", re.I,
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
_ABS_URL = re.compile(r'(?P<value>(?:https?|wss?|grpcs?|tcp|tcps|mqtts?|amqps?|ldaps?|rediss?|smfs?|solace|sftp|ftp|s3|file|jdbc:[a-z]+)://[^\s\"\'`<>\])}]+)', re.I)
_CONFIG_DECLARATION = re.compile(
    r'^[ \t]*[\"\']?(?P<value>[A-Za-z_][\w.\[\]-]*(?:url|uri|host|port|address|endpoint|broker|topic|queue|channel|destination|server|service|bootstrap|vpn|connection|provider|jndi|binding)[\w.\[\]-]*|(?:urls?|uris?|hosts?|ports?|addresses|endpoints?|brokers?|topics?|queues?|channels?|destinations?|servers?|services?|vpn|connections?|providers?|jndi|bindings?|listeners?|upstreams?|ingress|routes?))[\"\']?\s*[:=]', re.I | re.M)
_CONFIG_API = re.compile(
    r'(?:\b(?:getProperty|getRequiredProperty|getenv|GetEnvironmentVariable|config\.get|os\.getenv|os\.environ\.get|env|value)\s*\(\s*[\"\'](?P<value>[A-Za-z_][\w.-]*)[\"\']|\b(?:os\.environ|process\.env)\s*\[\s*[\"\'](?P<index>[A-Za-z_][\w.-]*)[\"\']|(?P<annotation>@ConfigurationProperties)\b)', re.I)
_SENSITIVE = r'(?:pass(?:word|wd|phrase)?|pwd|secret|token|credential|authorization|authentication|api[_-]?key|access[_-]?key|private[_-]?key|client[_-]?secret|sasl\.jaas\.config)'
_QUOTED = r'"""[\s\S]*?"""|' + "'''[\\s\\S]*?'''|" + r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|`(?:\\.|[^`\\])*`'
_SECRET_ASSIGNMENT = re.compile(
    r'(?P<label>\b[\w.-]*' + _SENSITIVE + r'[\w.-]*[\"\']?\s*(?::|=|,)\s*)(?P<value>' + _QUOTED + r'|[^\r\n]*)', re.I)
_SECRET_CALL = re.compile(
    r'(?P<label>\b(?:set|with)[\w]*' + _SENSITIVE + r'[\w]*\s*\(\s*)(?P<value>' + _QUOTED + r'|[^)\r\n]*)', re.I)
_SECRET_BLOCK = re.compile(
    r'(?P<label>^[ \t]*[\w.-]*' + _SENSITIVE + r'[\w.-]*\s*:\s*[|>][+-]?[ \t]*\r?\n)(?P<value>(?:[ \t]+[^\r\n]*(?:\r?\n|$))+)', re.I | re.M)
_CREDENTIAL_CALL = re.compile(
    r'\b(?:createSession|createConnection|getConnection|connect|simple_bind_s|bind|login|authenticate|withBasicAuth|basicAuthentication|setCredentials|PasswordAuthentication|UsernamePasswordCredentials|PasswordCredentials|NetworkCredential|BasicAWSCredentials|AwsBasicCredentials\.create)\s*\(', re.I)
_PRIVATE_KEY = re.compile(r'-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----[\s\S]*?(?:-----END [A-Z0-9 ]*PRIVATE KEY-----|\Z)', re.I)
_XML_SECRET = re.compile(r'(<(?:[\w.-]+:)?' + _SENSITIVE + r'\b[^>]*>)[\s\S]*?(</[^>]+>)', re.I)
_BEARER = re.compile(r'\b(?:Bearer|Basic)\s+[A-Za-z0-9_+/=.\-]+', re.I)
_JWT = re.compile(r'\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b')
_CLI_SECRET = re.compile(
    r'(?P<label>(?<![\w-])--(?:password|passwd|token|auth-token|access-token|api-key|apikey|secret|client-secret|access-key|secret-key|private-key|credential|user|proxy-user)(?:\s*=\s*|\s+)(?:\\\r?\n[ \t]*)*)(?P<value>' + _QUOTED + r'|[^\s\\]+)', re.I)
_AUTH_COMMAND = re.compile(r'\b(?:curl|wget|(?:docker|podman)\s+login)\b(?:\\\r?\n|[^\r\n])*', re.I)
_CLI_SHORT_SECRET = re.compile(r'(?P<label>(?<![\w-])-[upU](?:\s*=\s*|\s+|(?=[^\s-]))(?:\\\r?\n[ \t]*)*)(?P<value>' + _QUOTED + r'|[^\s\\]+)')


def _is_env_file(path: Path) -> bool:
    return path.name == '.env' or path.name.startswith('.env.')


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
    value = _safe_snippet(value)
    return value.replace('\r', ' ').replace('\n', ' ')[:240]


def _preserve_lines_redaction(value: str) -> str:
    return '\n'.join('<redacted>' if line else '' for line in value.split('\n'))


def _safe_snippet(text: str) -> str:
    """Sanitize the full file before selecting context, including multiline secrets."""
    text = _PRIVATE_KEY.sub(lambda match: _preserve_lines_redaction(match.group()), text)
    text = _XML_SECRET.sub(lambda match: match.group(1) + _preserve_lines_redaction(
        match.group()[len(match.group(1)):-len(match.group(2))]) + match.group(2), text)
    text = _SECRET_BLOCK.sub(lambda match: match.group('label') + _preserve_lines_redaction(match.group('value')), text)
    # Positional authentication arguments have no trustworthy parameter names.
    replacements = []
    for call in _CREDENTIAL_CALL.finditer(text):
        cursor, depth, quote = call.end(), 1, None
        while cursor < len(text) and cursor - call.end() < 4096 and depth:
            character = text[cursor]
            if quote:
                if character == '\\':
                    cursor += 2
                    continue
                if character == quote:
                    quote = None
            elif character in {'"', "'", '`'}:
                quote = character
            elif character == '(':
                depth += 1
            elif character == ')':
                depth -= 1
            cursor += 1
        for literal in re.finditer(_QUOTED, text[call.end():cursor]):
            start, end = call.end() + literal.start(), call.end() + literal.end()
            value = literal.group()[1:-1]
            if text[end:cursor].lstrip().startswith(':') or _ABS_URL.fullmatch(value):
                continue
            replacements.append((start, end))
    nonoverlapping = []
    for start, end in sorted(set(replacements), key=lambda span: (span[0], -span[1])):
        if not nonoverlapping or start >= nonoverlapping[-1][1]:
            nonoverlapping.append((start, end))
    for start, end in reversed(nonoverlapping):
        text = text[:start] + _preserve_lines_redaction(text[start:end]) + text[end:]
    text = _SECRET_ASSIGNMENT.sub(lambda match: match.group('label') + _preserve_lines_redaction(match.group('value')), text)
    text = _SECRET_CALL.sub(lambda match: match.group('label') + _preserve_lines_redaction(match.group('value')), text)
    text = _CLI_SECRET.sub(lambda match: match.group('label') + _preserve_lines_redaction(match.group('value')), text)
    text = _AUTH_COMMAND.sub(lambda command: _CLI_SHORT_SECRET.sub(
        lambda match: match.group('label') + _preserve_lines_redaction(match.group('value')), command.group()), text)
    text = _BEARER.sub('<redacted>', _JWT.sub('<redacted>', text))

    def url(match):
        value = match.group('value').split('?', 1)[0].split('#', 1)[0]
        return re.sub(r'(?<=//)[^/@\s]+@', '<redacted>@', value)

    text = _ABS_URL.sub(url, text)
    return re.sub(r'(?<!:)//[^\s/\"\']+@[^\s\"\'<>]+',
                  lambda match: re.sub(r'(?<=//)[^/@\s]+@', '<redacted>@', match.group()).split('?', 1)[0].split('#', 1)[0], text)


def _protocols(value: str) -> tuple[str, ...]:
    scheme = value.lower().split(':', 1)[0]
    if scheme in {'http', 'https'}:
        return ('HTTP',)
    if scheme in {'ws', 'wss'}:
        return ('WEBSOCKET',)
    if scheme in {'smf', 'smfs', 'solace'}:
        return ('SOLACE',)
    return (scheme.upper(),) if scheme in {'grpc', 'grpcs', 'tcp', 'tcps', 'mqtt', 'mqtts', 'amqp', 'amqps', 'ldap', 'ldaps', 'redis', 'rediss', 'sftp', 'ftp', 's3', 'jdbc', 'file', 'jms', 'kafka', 'rabbitmq', 'activemq', 'ibmmq'} else ()


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


def scan_files(workspace: Path, repository: str, paths: Iterable[Path], *, expected_sha256: dict | None = None) -> dict:
    candidates: list[dict] = []
    scanned = 0
    skipped = []
    for path in sorted(paths):
        try:
            with path.open('rb') as source:
                raw = source.read(MAX_TEXT_BYTES + 1)
            if len(raw) > MAX_TEXT_BYTES:
                raise ValueError('SOURCE_SIZE_LIMIT')
            text = decode_discovery_text(raw)[0]
        except (OSError, ValueError, UnicodeError) as error:
            if expected_sha256 is not None:
                raise ValueError('DISCOVERY_SOURCE_CHANGED: ' + path.relative_to(workspace).as_posix()) from error
            reason = str(error) if str(error) in {'SOURCE_SIZE_LIMIT', 'BINARY_FILE'} else 'UNREADABLE_SOURCE'
            skipped.append({'path': path.relative_to(workspace).as_posix(), 'reason': reason})
            continue
        source_sha256 = hashlib.sha256(raw).hexdigest()
        if expected_sha256 is not None and (path.is_symlink() or expected_sha256.get(path) != source_sha256):
            raise ValueError('DISCOVERY_SOURCE_CHANGED: ' + path.relative_to(workspace).as_posix())
        scanned += 1
        safe_lines = _safe_snippet(text).split('\n')
        line_starts = [0, *(match.end() for match in re.finditer('\n', text))]
        file_values: dict[tuple[str, str], dict] = {}
        occurrence_keys: dict[tuple[str, str], set] = {}
        snippets = {}
        has_graphql_context = bool(re.search(r'\b(?:ApolloClient|ApolloProvider|graphql|gql|urql|react-apollo)\b|@apollo/client', text, re.I))
        has_solace_context = bool(re.search(r'\b(?:com\.solacesystems|com\.solace\.messaging|solace\.messaging|solclientjs|solace-pubsubplus|solace-messaging)\b', text))

        def record(match, family, pattern_id, value, roles=(), protocols=(), *, url=False):
            start, end = match.span()
            start += len(match.group()) - len(match.group().lstrip())
            start_line, end_line = bisect_right(line_starts, start), bisect_right(line_starts, max(start, end - 1))
            value = (value if family in {'CONFIG_READ', 'CONFIG_DECLARATION'} and re.fullmatch(r'[A-Za-z_][\w.@\[\]-]*', value)
                     else _safe_value(value, url=url))
            if not value:
                return
            if family in {'CALL_HINT', 'MESSAGE_OPERATION'}:
                operation = value.rsplit('.', 1)[-1].lower()
                if operation.startswith(('send', 'publish', 'createproducer')):
                    roles = (*roles, 'producer')
                elif operation.startswith(('subscribe', 'consume', 'receive', 'createconsumer', 'addsubscription')):
                    roles = (*roles, 'subscriber')
            key = (family, value)
            row = file_values.get(key)
            if row is None:
                row = _row(repository, workspace, path, start_line, family, pattern_id, value,
                           source_sha256=source_sha256, role_hints=[], protocol_hints=[], occurrences=[])
                file_values[key] = row
                occurrence_keys[key] = set()
                candidates.append(row)
            first = max(1, start_line - 1)
            last = min(len(safe_lines), max(end_line + 1, start_line), first + 7)
            if (first, last) not in snippets:
                snippets[first, last] = '\n'.join(line[:400] for line in safe_lines[first - 1:last])[:1600]
            occurrence_key = (start, end, pattern_id, tuple(roles), tuple(protocols))
            if occurrence_key in occurrence_keys[key]:
                return
            occurrence_keys[key].add(occurrence_key)
            occurrence = {
                'start_line': start_line, 'end_line': end_line,
                'start_column': start - line_starts[start_line - 1] + 1,
                'end_column': end - line_starts[bisect_right(line_starts, end) - 1] + 1,
                'pattern_id': pattern_id, 'role_hints': list(roles), 'protocol_hints': list(protocols),
                'snippet_start_line': first, 'snippet_end_line': last, 'snippet': snippets[first, last],
            }
            # Different recognizers may find one declaration. Preserve each distinct occurrence and its hints.
            row['occurrences'].append(occurrence)
            row['role_hints'] = sorted(set(row['role_hints']) | set(roles))
            row['protocol_hints'] = sorted(set(row['protocol_hints']) | set(protocols))
            row['occurrence_count'] = len(row['occurrences'])

        for match in _URL.finditer(text):
            record(match, 'HTTP_ENDPOINT', 'url-literal', match.group('value'), ('dependency',),
                   _protocols(match.group('value')) or ('HTTP',), url=True)
        for match in _HTTP_CALL_URL.finditer(text):
            record(match, 'HTTP_ENDPOINT', 'http-call-url-literal', match.group('value'), ('consumer',), ('HTTP',), url=True)
        for match in _ABS_URL.finditer(text):
            value = match.group('value')
            family = 'HTTP_ENDPOINT' if value.lower().startswith(('http:', 'https:', 'ws:', 'wss:')) else 'NETWORK_ENDPOINT'
            record(match, family, 'unquoted-network-url', value, ('dependency',), _protocols(value), url=True)
        for match in _CONFIG.finditer(text):
            value = next((value for value in match.groupdict().values() if value), '')
            record(match, 'CONFIG_READ', 'configuration-access', value, ('configuration',))
        for match in re.finditer(_ENV_CONFIG.pattern, text, re.M):
            # Configuration names remain useful even when their values are credentials.
            value = match.group('env')
            if value.isupper() or _is_env_file(path):
                record(match, 'CONFIG_READ', 'configuration-access', value, ('configuration',))
        for match in _CONFIG_API.finditer(text):
            value = next((value for value in match.groupdict().values() if value), '')
            record(match, 'CONFIG_READ', 'configuration-api', value, ('configuration',))
        for match in _CONFIG_DECLARATION.finditer(text):
            record(match, 'CONFIG_DECLARATION', 'configuration-declaration', match.group('value'), ('configuration',))
        for match in _KAFKA.finditer(text):
            value = next((value for value in match.groupdict().values() if value), '')
            record(match, 'MESSAGE_CHANNEL', 'kafka-channel', value, ('consumer',), ('KAFKA',))
        for match in _SQL.finditer(text):
            record(match, 'DATABASE_TABLE', 'sql-table', match.group('table'), ('consumer',), ('SQL',))
        for match in _IMPORT.finditer(text):
            module = match.group('module')
            if not module.startswith(('http://', 'https://', '//')):
                record(match, 'MODULE_IMPORT', 'module-import', module, ('dependency',))
        for match in _NGINX.finditer(text):
            value = match.group('value')
            record(match, 'GATEWAY_ROUTE', 'nginx-directive', value, ('configuration', 'provider'),
                   ('HTTP',), url=bool(re.search(r'(?:https?|wss?)://|//', value, re.I)))
        for family, pattern_id, pattern, roles, protocols in PATTERNS:
            for match in pattern.finditer(text):
                value = next((value for value in match.groupdict().values() if value), match.group())
                if family == 'GRAPHQL_SCHEMA':
                    value = path.name
                if (family == 'GRAPHQL_CLIENT' and value in {'useQuery', 'useLazyQuery', 'useMutation', 'useSubscription'}
                        and not has_graphql_context):
                    continue
                hints = _protocols(value) or protocols
                if pattern_id == 'solace-operation' and not has_solace_context:
                    hints = ()
                record(match, family, pattern_id, value, roles, hints,
                       url=family in {'HTTP_ENDPOINT', 'MESSAGE_CHANNEL'})
        for row in file_values.values():
            row['occurrences'].sort(key=lambda occurrence: (occurrence['start_line'], occurrence['start_column'], occurrence['pattern_id']))
    unique = {row['id']: row for row in candidates}
    return {
        'scanned_files': scanned,
        'skipped_files': sorted(skipped, key=lambda row: row['path']),
        'candidates': sorted(unique.values(), key=lambda row: (row['repository'], row['path'], row['line'], row['family'], row['id'])),
    }


def scan_repository(workspace: Path, repository: str, root: Path) -> dict:
    """Search the broad text inventory independently of typed-extractor layouts."""
    inventory = discovery_inventory(root)
    sources = {root / row['path']: row['sha256'] for row in inventory['files'] if row['status'] == 'SCANNED'}
    result = scan_files(workspace, repository, sources, expected_sha256=sources)
    result['skipped_files'].extend({'path': (root / row['path']).relative_to(workspace).as_posix(), 'reason': row['reason']}
                                   for row in inventory['files'] if row['status'] == 'SKIPPED')
    result['skipped_files'].sort(key=lambda row: row['path'])
    result['file_inventory'] = inventory
    result['discovery_sha256'] = inventory['content_sha256']
    return result
