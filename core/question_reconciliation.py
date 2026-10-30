"""Check answer propagation references without deciding business meaning or publishing knowledge."""
from __future__ import annotations
import hashlib
from pathlib import Path
import re
import yaml
from .assurance import _read, local_path
from .models import WorkbenchError

_ANSWERED = {'ANSWERED', 'ANSWERED_FROM_EVIDENCE', 'RESOLVED'}

def reconcile_questions(manifest: dict, root: str | Path) -> dict:
    """Reconcile selected stable question IDs against hash-bound living documents and consumers."""
    root = Path(root).resolve()
    if not isinstance(manifest, dict) or type(manifest.get('schema_version')) is not int or manifest['schema_version'] != 1 or not isinstance(manifest.get('questions'), list):
        raise WorkbenchError('Select a question manifest with schema_version 1 and a questions array.')
    findings, rows, entries = [], [], {}
    def finding(code, identifier, detail):
        findings.append({'code': code, 'question_id': identifier, 'detail': detail, 'owner': 'unknown',
                         'next_action': 'Review the linked answer and its consuming knowledge record.'})
    def read(reference):
        if not isinstance(reference, dict) or not isinstance(reference.get('path'), str) or not re.fullmatch(r'[a-f0-9]{64}', str(reference.get('sha256', ''))):
            raise WorkbenchError('Every question and consumer needs a retained path and SHA-256.')
        raw = _read(local_path(root, reference['path']))
        try:
            text = raw.decode('utf-8')
        except UnicodeError:
            raise WorkbenchError('Question and consumer documents must contain UTF-8 text.') from None
        return text, hashlib.sha256(raw).hexdigest() == reference['sha256']
    for entry in manifest['questions']:
        if not isinstance(entry, dict) or not isinstance(entry.get('id'), str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:-]*', entry['id']):
            raise WorkbenchError('Each question needs a stable ID.')
        identifier = entry['id']
        if identifier in entries:
            finding('DUPLICATE_ENTRY_POINT', identifier, 'The manifest declares the same question more than once.')
        entries[identifier] = entry
        text, current = read(entry.get('document'))
        sections = list(re.finditer(r'^(#{1,6})\s+`?' + re.escape(identifier) + r'`?\s*$', text, re.M))
        row = {'id': identifier, 'document': entry['document'], 'freshness': 'CURRENT' if current else 'STALE', 'status': 'UNKNOWN', 'consumers': []}
        if not current:
            finding('STALE_ANSWER_SOURCE', identifier, 'The living document differs from its recorded hash.')
        if len(sections) != 1:
            finding('DUPLICATE_QUESTION_ID' if sections else 'QUESTION_NOT_FOUND', identifier, 'The living document must define this question exactly once.')
            rows.append(row)
            continue
        start = sections[0].end()
        level = len(sections[0].group(1))
        following = re.search(r'^#{1,' + str(level) + r'}\s+', text[start:], re.M)
        section = text[start:start + following.start()] if following else text[start:]
        status = re.search(r'Status:\s*`?([A-Z_]+)', section)
        row['status'] = status.group(1) if status else 'UNKNOWN'
        answer_hash = hashlib.sha256(section.encode('utf-8')).hexdigest()
        row['answer_sha256'] = answer_hash
        links = re.findall(r'\[[^\]]+\]\(([^)]+)\)', section)
        row['answer_source_references'] = links
        if row['status'] in _ANSWERED and not links:
            finding('ANSWER_SOURCE_MISSING', identifier, 'The resolved answer has no supporting source reference.')
        consumers = entry.get('consumers', [])
        if not isinstance(consumers, list):
            raise WorkbenchError('Question consumers must be an array.')
        if row['status'] in _ANSWERED and not consumers:
            finding('CONSUMER_SCOPE_UNKNOWN', identifier, 'No consuming knowledge inventory is declared.')
        for consumer in consumers:
            content, consumer_current = read(consumer)
            header = re.match(r'^---\s*\n(.*?)\n---', content, re.S)
            try:
                metadata = yaml.safe_load(header.group(1)) if header else {}
            except yaml.YAMLError:
                raise WorkbenchError('Correct malformed consumer YAML metadata before reconciliation.') from None
            metadata = metadata if isinstance(metadata, dict) else {}
            version_matches = 'version' in consumer and metadata.get('version') == consumer['version']
            applied = consumer.get('applied_answer_sha256') == answer_hash
            anchor = identifier.lower()
            reference_present = False
            for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', content):
                path, separator, fragment = target.strip('<>').partition('#')
                if separator and fragment == anchor and ':' not in path:
                    resolved = (root / consumer['path']).parent / path
                    reference_present |= resolved.resolve() == (root / entry['document']['path']).resolve()
            # Hashes and references are declarations. They cannot establish semantic agreement.
            propagated = current and consumer_current and version_matches and applied and reference_present
            state = {'path': consumer['path'], 'expected_version': consumer.get('version'), 'observed_version': metadata.get('version'),
                     'freshness': 'CURRENT' if consumer_current else 'STALE', 'answer_reference_present': reference_present,
                     'applied_answer_hash_matches': applied, 'propagation_reference_complete': propagated}
            row['consumers'].append(state)
            if not consumer_current or not version_matches:
                finding('CONSUMER_VERSION_STALE', identifier, 'The consuming knowledge bytes or version differ from the declaration.')
            if row['status'] in _ANSWERED and not propagated:
                finding('ANSWER_PROPAGATION_MISSING', identifier, 'The consuming knowledge lacks a current answer hash, source reference, or version binding.')
        rows.append(row)
    return {'schema_version': 1, 'status': 'ACTION_REQUIRED' if findings else 'REFERENCES_COMPLETE', 'questions': rows, 'findings': findings,
            'verification': 'NOT_VERIFIED', 'limitations': ['This check detects reference drift. It cannot establish semantic consistency or business approval.',
                'Publication, source authority, and human knowledge review remain separate.', 'Only declared questions and consumers are checked.']}
