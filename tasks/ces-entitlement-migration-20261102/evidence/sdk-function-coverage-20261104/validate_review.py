"""Check review links, source identity, counts, and preserved intake hashes."""
from pathlib import Path
import ast, hashlib, json, re, subprocess
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
STAGE = ROOT / 'tasks/ces-entitlement-migration-20261102/10-change-review-sdk-function-coverage.md'
REPO = ROOT / 'repos/libraries/single-ui-sdk-starter'
HEAD = 'fd9a157e260850b6d9efa10da3223950ea61133a'
errors = []
checks = {}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def anchors(path):
    text = path.read_text()
    result = set(re.findall(r'<a\s+id="([^"]+)"', text))
    for line in text.splitlines():
        if re.match(r'^#{1,6}\s', line):
            title = re.sub(r'^#+\s+', '', line).strip().lower()
            title = re.sub(r'[^\w\- ]', '', title)
            result.add(title.replace(' ', '-'))
    return result

links = 0
for path in [STAGE, OUT / 'api-parity.md']:
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        if re.match(r'^[a-z][a-z0-9+.-]*:', target):
            continue
        target = unquote(target.strip('<>'))
        location, _, anchor = target.partition('#')
        resolved = (path.parent / location).resolve() if location else path
        links += 1
        if not resolved.exists():
            errors.append(f'missing link: {path.name} -> {target}')
        elif anchor and resolved.suffix == '.md' and anchor not in anchors(resolved):
            errors.append(f'missing anchor: {path.name} -> {target}')
checks['markdown_links'] = links
json_count = 0
for path in OUT.rglob('*.json'):
    try:
        json.loads(path.read_text()); json_count += 1
    except Exception as error:
        errors.append(f'{path.name}: {error}')
checks['parsed_json'] = json_count
for path in OUT.glob('*.py'):
    ast.parse(path.read_text(), filename=str(path))
checks['python_syntax'] = 'PASSED'
context = json.loads((OUT / 'review-context.json').read_text())
final_context = json.loads((OUT / 'final-review-context.json').read_text())
if context['fingerprint'] != final_context['fingerprint']:
    errors.append('Review fingerprint changed')
checks['context_fingerprint'] = context['fingerprint']
inputs = json.loads((OUT / 'candidate-module-test-run/inputs.json').read_text())
for source in inputs['files']:
    exact = subprocess.check_output(['git', '-C', str(REPO), 'show', HEAD + ':' + source['path']])
    if hashlib.sha256(exact).hexdigest() != source['sha256']:
        errors.append('candidate source mismatch: ' + source['path'])
checks['candidate_source_bindings'] = len(inputs['files'])
result = json.loads((OUT / 'candidate-module-test-run/result.json').read_text())
if result['counts'] != dict(tests=44, failures=0, errors=0, skipped=0) or result['exit_code'] != 0 or result['source_changes']:
    errors.append('Current full unit suite did not pass unchanged')
checks['fresh_test_counts'] = result['counts']
for source in json.loads((OUT / 'api-inventory.json').read_text()):
    if sha(ROOT / source['file']) != source['sha256']:
        errors.append('API source changed: ' + source['file'])
checks['api_file_bindings'] = len(json.loads((OUT / 'api-inventory.json').read_text()))
binding = json.loads((OUT / 'retained-execution-binding.json').read_text())
for source in binding['other_sources']:
    if sha(ROOT / source['path']) != source['sha256']:
        errors.append('Preserved source changed: ' + source['path'])
checks['preserved_sources'] = len(binding['other_sources'])
api = json.loads((OUT / 'api-parity.json').read_text())
summary = api['prod_summary']
if (summary['matched_grant_rows'], summary['missing_grant_rows'], summary['distinct_entity_role_subject_action_tuples']) != (60, 0, 59):
    errors.append('API counts differ from report')
checks['prod_snapshot_counts'] = summary
if not json.loads((OUT / 'artifact-lint.json').read_text())['valid']:
    errors.append('Artifact lint failed')
if not json.loads((OUT / 'workspace-validation.json').read_text())['valid']:
    errors.append('Workspace validation failed')
checks['artifact_lint'] = 'PASSED_WITH_PENDING_OWNER_AND_REVIEW_WARNINGS'
checks['workspace_validation'] = 'PASSED'
excluded_raw_logs = ':(glob,exclude)tasks/ces-entitlement-migration-20261102/evidence/sdk-function-coverage-20261104/**/*.log'
status = subprocess.run(['git', 'diff', '--cached', '--check', '--', '.', excluded_raw_logs], cwd=ROOT, capture_output=True, text=True)
if status.returncode:
    errors.append(status.stdout + status.stderr)
checks['staged_authored_diff_check'] = 'PASSED' if status.returncode == 0 else 'FAILED'
checks['raw_log_whitespace'] = 'Preserved exact Maven log bytes, including trailing spaces; excluded from authored-file whitespace checks.'
checks['fresh_execution_scope'] = 'All 44 tests in the sole declared SDK module; explicit compilation/test goals; parent has no tests. Full packaging lifecycle not rerun successfully.'
report = dict(status='PASSED' if not errors else 'FAILED', checks=checks, errors=errors, limitations=['Automated checks do not establish complete ASD-STE100 compliance.', 'Mock unit tests and snapshot equality do not establish live migration parity.'])
(OUT / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
raise SystemExit(bool(errors))
