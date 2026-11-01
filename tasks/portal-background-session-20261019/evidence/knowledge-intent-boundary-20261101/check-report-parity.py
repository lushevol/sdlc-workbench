"""Check maintained report bindings; this does not establish semantic approval."""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / 'tasks/portal-background-session-20261019'
OUT = Path(__file__).resolve().parent
REPORTS = [TASK / n for n in ('10-release-confidence.md', '10-release-confidence.html', '10-release-confidence-details.html')]
INDEX = TASK / 'evidence/index.md'
STAGE = TASK / '10-knowledge-sync.md'
errors = []

def check(condition, message):
    if not condition:
        errors.append(message)

class Html(HTMLParser):
    def __init__(self, value):
        super().__init__()
        self.links = []
        self.ids = []
        self.feed(value)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])

def anchors(path):
    value = path.read_text(errors='replace')
    ids = set(re.findall(r'\bid=[\"\']([^\"\']+)', value))
    seen = {}
    for heading in re.findall(r'^#{1,6}\s+(.+)$', value, re.M):
        slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        ids.add(slug + (f'-{count}' if count else ''))
    return ids

stage = STAGE.read_text()
canonical = yaml.safe_load(re.search(r'```yaml\n(knowledge_sync:.*?)\n```', stage, re.S).group(1))['knowledge_sync']
check(canonical['operation_status'] == 'PARTIAL', 'canonical operation must remain PARTIAL')
expected = {'required_rows': 4, 'prepared_rows': 4, 'independently_checked_rows': 4, 'reviewed_rows': 2,
            'published_changed_rows': 0, 'supported_no_change_rows': 2, 'synchronized_rows': 2,
            'intended_rule_changes': 0, 'open_gap_rows': 6}
for key, value in expected.items():
    check(canonical[key] == value, f'canonical {key} differs from expected inventory')
expected_views = {p.name for p in REPORTS}
check(set(canonical['required_report_views']) == expected_views, 'canonical required report views differ')
check(set(canonical['reconciled_report_views']) == expected_views, 'canonical report parity not 3/3')

sections = []
link_count = 0
for path in REPORTS:
    value = path.read_text()
    if path.suffix == '.html':
        parsed = Html(value)
        check(len(parsed.ids) == len(set(parsed.ids)), f'duplicate IDs: {path.name}')
        section = re.search(r'<section class="runtime" id="knowledge-sync".*?</details></section>', value, re.S).group()
        sections.append(section)
        check(len(re.findall(r'<tr><td>KS-0[1-4]', section)) == 4, f'four knowledge rows: {path.name}')
        links = parsed.links
    else:
        section = value.split('## Release knowledge synchronization\n', 1)[1].split('\n## ', 1)[0]
        links = re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', value)
    for marker in ['PARTIAL', '2/4', '4/4', '0/2', 'v8 → v9', 'v6 → v7', 'AC-1 through AC-7 remain unchanged',
                   'Existing SDK session intent remains unchanged', 'Intended service responsibilities remain unchanged', 'NOT_PERFORMED',
                   '467-case', '471-unit', 'PROD artifact', 'effective date remain unknown', '09-intent-reality-gaps.md', 'target behavior', 'Intended-rule changes in this session scope: zero',
                   'six gaps and one bounded conformance observation']:
        check(marker in section, f'{path.name}: missing {marker}')
    if canonical['independently_checked_rows'] == 4:
        check('4/4' in section and re.search(r'accuracy review[^.]*4/4', section, re.I), f'{path.name}: accuracy 4/4 missing')
    else:
        check(re.search(r'accuracy review[^.]*PENDING', section, re.I), f'{path.name}: pending accuracy missing')
    check('5/6' in value and 'NOT_RUN' in value and '192/192' in value, f'{path.name}: runtime metrics lost')
    check('NO_GO' in value and '197' in value and '467' in value and '471' in value, f'{path.name}: historical metrics lost')
    for link in links:
        link_count += 1
        parts = urlsplit(unescape(link.strip('<>')))
        if parts.scheme or parts.netloc:
            continue
        target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
        if not target.exists():
            errors.append(f'{path.name}: missing target {link}')
            continue
        fragment = unquote(parts.fragment)
        if re.fullmatch(r'L\d+(?:-L?\d+)?', fragment):
            maximum = max(map(int, re.findall(r'\d+', fragment)))
            check(maximum <= len(target.read_text(errors='replace').splitlines()), f'{path.name}: line outside target {link}')
        elif fragment and target.suffix in ('.md', '.html'):
            check(fragment in anchors(target), f'{path.name}: missing anchor {link}')
check(sections[0] == sections[1], 'HTML knowledge supplement sections differ')

for link in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', INDEX.read_text()):
    link_count += 1
    parts = urlsplit(unescape(link.strip('<>')))
    if parts.scheme or parts.netloc:
        continue
    target = (INDEX.parent / unquote(parts.path)).resolve() if parts.path else INDEX
    check(target.exists(), f'{INDEX.name}: missing target {link}')
    if target.exists() and parts.fragment and target.suffix in ('.md', '.html'):
        check(unquote(parts.fragment) in anchors(target), f'{INDEX.name}: missing anchor {link}')

independent_path = TASK / canonical['independent_review_ref']
independent = json.loads(independent_path.read_text())
check(independent['status'] == 'PASSED_WITH_RECORDED_LIMITS', 'independent semantic review not passed within recorded limits')
check(independent['checks']['gherkin_blocks_byte_identical'] == 7, 'independent review does not preserve all seven criteria')
check(independent['checks']['gap_rows'] == canonical['open_gap_rows'], 'independent gap count differs from canonical summary')
check(independent['checks']['separate_conformance_rows'] == 1, 'bounded conformance observation missing')
concurrency = json.loads((OUT / 'concurrency-review.json').read_text())
check(concurrency['status'] == 'PASSED_WITH_RECORDED_LIMITS', 'supplemental dependency review not passed within recorded limits')
check(concurrency['ks03_disposition']['selected_dependency_meaning_unchanged'], 'selected SDK session meaning changed')
check(concurrency['ks03_disposition']['selected_dependency_applicability_unchanged'], 'selected SDK session applicability changed')
check(not concurrency['ks03_disposition']['whole_document_no_change_claim_valid'], 'SDK global change was not disclosed')
for record in independent['rows']:
    if record['row_id'] == 'KS-03':
        check(record['sha256'] == concurrency['old_reviewed']['sha256'], 'original SDK review identity changed')
        selected = concurrency['current_revalidated']
    else:
        selected = record
    target = ROOT / selected['path']
    check(hashlib.sha256(target.read_bytes()).hexdigest() == selected['sha256'], f'independent final hash mismatch: {selected["path"]}')
    check(selected['governance_state'] == 'candidate' and selected['status'] == 'draft', f'candidate state changed: {selected["path"]}')
    check(selected['human_verification_entries'] == 0, f'human review status unexpectedly changed: {selected["path"]}')
for name, digest in independent['supporting_files'].items():
    check(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, f'independent supporting hash mismatch: {name}')
browser = json.loads((OUT / 'report-browser-checks.json').read_text())
check(browser['status'] == 'PASSED' and len(browser['cases']) == 4, 'browser layout checks not passed')
for source in browser['source_hashes']:
    check(hashlib.sha256((TASK / source['file']).read_bytes()).hexdigest() == source['sha256'], f'browser checked stale HTML: {source["file"]}')

requirement = ROOT / 'knowledge/candidates/requirements/REQ-active-session-renewal.md'
ac_lines = {int(m.group(1)): i for i, line in enumerate(requirement.read_text().splitlines(), 1)
            if (m := re.fullmatch(r'Scenario: AC-(\d+)', line))}
for path in REPORTS:
    value = path.read_text()
    for ac, line in ac_lines.items():
        links = re.findall(r'REQ-active-session-renewal.md#L(\d+)', value)
        if links:
            check(str(line) in links or ac > 4 and path.suffix == '.md', f'{path.name}: AC-{ac} locator missing')
    allowed = set(map(str, ac_lines.values()))
    for line in re.findall(r'REQ-active-session-renewal.md#L(\d+)', value):
        check(line in allowed, f'{path.name}: stale criterion line {line}')

predecessor = TASK / 'evidence/release-knowledge-sync-20261101/predecessors/REQ-active-session-renewal.md'
check(hashlib.sha256(predecessor.read_bytes()).hexdigest() == '3db69ca6827b4afa0eb9f3182f15045f80dac012f9d37004d62144740424c359', 'historical v5 bytes changed')

new_prose = REPORTS[0].read_text().split('## Release knowledge synchronization\n', 1)[1].split('\n## ', 1)[0]
long_sentences = []
for line in new_prose.splitlines():
    if not line or line.startswith(('|', '<')):
        continue
    plain = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line).replace('**', '').replace('`', '')
    for sentence in re.split(r'(?<=[.!?])\s+', plain):
        if len(sentence.split()) > 20:
            long_sentences.append(sentence)
check(not long_sentences, 'new knowledge prose contains a sentence above 20 words')
lint = json.loads((OUT / 'report-artifact-lint.json').read_text())
check(lint['status'] == 'PASSED', 'report artifact lint failed')

result = {
    'status': 'PASSED' if not errors else 'FAILED',
    'checked_at': datetime.now(timezone.utc).isoformat(),
    'scope': 'Intent-only knowledge supplement, independent gap document, and retained historical release bindings',
    'canonical_summary': canonical,
    'checks': {'metric_markers': not errors, 'html_supplement_identical': sections[0] == sections[1],
               'link_count': link_count, 'independent_final_hashes': not any('independent' in e for e in errors),
               'intended_rule_changes': canonical['intended_rule_changes'], 'separate_gap_rows': canonical['open_gap_rows'],
               'knowledge_target_boundary': all('09-intent-reality-gaps.md' in p.read_text() for p in REPORTS),
               'sdk_concurrent_review': concurrency['status'], 'sdk_current_reviewed_version': concurrency['current_revalidated']['version'],
               'desktop_mobile_browser_checks': browser['status'],
               'local_link_targets_and_anchors': not any('target' in e or 'anchor' in e for e in errors), 'current_ac_definition_lines': ac_lines,
               'new_prose_sentence_limit': not long_sentences, 'artifact_lint': lint['status']},
    'errors': errors,
    'writing_review': {'standard': 'ASD-STE100', 'automated_check': 'PASSED' if not errors else 'FAILED',
                       'asd_review': 'PENDING', 'reviewer': None, 'reviewed_at': None,
                       'limitations': ['Automated checks do not check the complete approved dictionary or grammar rules.']},
    'source_hashes': [{'path': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                      for p in REPORTS + [INDEX, STAGE, requirement, TASK / '09-intent-reality-gaps.md', ROOT / 'knowledge/candidates/security/KT-authentication-and-sessions.md']],
    'self_excluded': True,
    'limits': ['Text and link checks do not establish semantic accuracy, publication approval, or application execution.',
               'Historical execution retains its original source scope. No remote UAT or PROD evidence was collected.',
               'Knowledge states intended behavior; source and execution claims are separate task gap evidence.']
}
(OUT / 'report-validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'errors': errors}, indent=2))
sys.exit(bool(errors))
