from contextlib import redirect_stdout, redirect_stderr
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import types

REPO = Path('/Users/lushevol/code/github/ratan-release-impact/workbench')
EVIDENCE = Path('/tmp/runtime-accounting-review-20261117')
sys.path.insert(0, str(REPO))
import ai_sdlc_workbench.ingestion

def pinned_module(name, path):
    raw = subprocess.check_output(['git', 'show', 'bf0f10a09:' + path], cwd=REPO)
    module = types.ModuleType(name)
    module.__package__ = name.rsplit('.', 1)[0]
    module.__file__ = str(REPO / path)
    sys.modules[name] = module
    exec(compile(raw, module.__file__, 'exec'), module.__dict__)
    (EVIDENCE / ('candidate-' + Path(path).name)).write_bytes(raw)
    return module

candidate = pinned_module('ai_sdlc_workbench.ingestion.incremental', 'core/ingestion/incremental.py')
cli = pinned_module('ai_sdlc_workbench.cli', 'core/cli.py')
test_module = pinned_module('tests.test_incremental_ingestion', 'tests/test_incremental_ingestion.py')
IncrementalIngestionTests = test_module.IncrementalIngestionTests
from ai_sdlc_workbench.models import WorkbenchError

base_raw = subprocess.check_output(['git', 'show', 'bf0f10a09^:core/ingestion/incremental.py'], cwd=REPO)
(EVIDENCE / 'baseline-incremental.py').write_bytes(base_raw)
base = types.ModuleType('ai_sdlc_workbench.ingestion.audit_baseline_incremental')
base.__package__ = 'ai_sdlc_workbench.ingestion'
exec(compile(base_raw, str(EVIDENCE / 'baseline-incremental.py'), 'exec'), base.__dict__)

observations = {}

def save(name, value):
    (EVIDENCE / (name + '.json')).write_text(json.dumps(value, indent=2) + '\n')
    observations[name] = value

def fixture(name):
    case = IncrementalIngestionTests('test_supported_no_change_is_idempotent_and_skips_unchanged_semantic_work')
    case.setUp()
    original_root = case.root
    case.root = (EVIDENCE / name / 'workspace').resolve()
    if case.root.exists():
        shutil.rmtree(case.root)
    shutil.copytree(original_root, case.root)
    case.raw = case.root / 'evidence/knowledge/incoming/docs'
    case.policy = case.root / '.agents/skills/ingest-knowledge/assets/source-filter.yaml'
    return case

def prepare(case):
    case.page()
    case.refresh()
    case.select()

def complete(module, case, plan, plan_path, result):
    results_path = case.save({'schema_version': 1, 'source_id': 'docs', 'plan_id': plan['plan_id'], 'results': [result]}, 'completion')
    try:
        result = module.complete_sources(case.root, 'docs', plan_path, results_path)
        return {'return': result}
    except Exception as error:
        return {'exception': type(error).__name__, 'message': str(error)}

# Case 1. Explicit existing-coverage citations are accepted without any path binding.
case = fixture('unbound-target')
prepare(case)
plan, path = case.plan()
result = case.result(source_to_output=[{'source_range': 'L1', 'disposition': 'existing_coverage',
    'target': 'knowledge/candidates/does-not-exist.md#request-validation',
    'reason': 'The declared canonical section supplies coverage.'}])
completed = complete(candidate, case, plan, path, result)
next_plan = candidate.plan_sources(case.root, 'docs')
assert completed['return']['status'] == 'COMPLETED'
assert next_plan['counts']['unchanged'] == 1 and not next_plan['process_queue']
save('unbound-target', {'completion': completed, 'target_exists': False, 'next_counts': next_plan['counts'],
     'next_process_queue': next_plan['process_queue']})
case.doCleanups()

# Case 2. Changes and deletion of a real cited target leave the declaring source skipped.
case = fixture('target-staleness')
case.page()
case.page('other.md', 'The system must deny invalid requests.\n')
case.refresh()
case.select()
case.select('other.md')
record = case.record(source='other.md')
plan, path = case.plan()
first = case.result(source_to_output=[{'source_range': 'L1', 'disposition': 'existing_coverage',
    'target': record + '#request-validation', 'reason': 'This existing canonical section preserves the clause.'}])
second = case.result(path='other.md', outputs=[record])
completed = case.complete(plan, path, first, second)
assert completed['status'] == 'COMPLETED'
receipt = json.loads((case.root / 'evidence/knowledge/processing/docs.json').read_text())['receipts']['page.md']
assert receipt['outputs'] == {} and receipt['input']['dependencies'] == {}
(EVIDENCE / 'target-staleness-original.md').write_bytes((case.root / record).read_bytes())
(case.root / record).write_text((case.root / record).read_text() + '\nA changed condition.\n')
(EVIDENCE / 'target-staleness-changed.md').write_bytes((case.root / record).read_bytes())
changed = candidate.plan_sources(case.root, 'docs')
assert [item['path'] for item in changed['process_queue']] == ['other.md']
(case.root / record).unlink()
deleted = candidate.plan_sources(case.root, 'docs')
assert [item['path'] for item in deleted['process_queue']] == ['other.md']
save('target-staleness', {'completion': completed, 'declaring_source_receipt': receipt,
    'changed_target_process_paths': [item['path'] for item in changed['process_queue']],
    'deleted_target_process_paths': [item['path'] for item in deleted['process_queue']],
    'deleted_target_counts': deleted['counts']})
case.doCleanups()

# Case 3. Existing documented review-note shape regresses for no_change.
doc = (REPO / '.agents/skills/ingest-knowledge/references/source-preparation.md').read_text()
section = doc.split('## Record canonical processing completion', 1)[1]
sample = json.loads(re.search(r'```json\n(.*?)\n```', section, re.S).group(1))['results'][0]
results = {}
for label, module in [('base', base), ('candidate', candidate)]:
    case = fixture('documented-review-' + label)
    prepare(case)
    plan = module.plan_sources(case.root, 'docs')
    plan_path = case.save(plan, 'source-plan')
    result = deepcopy(sample)
    result.update(path='page.md', disposition='no_change', outputs=[])
    result.pop('checkpoint')
    result['review'].update(actor='agent:fixture', reviewed_at='2026-11-12T00:00:00Z',
        note='L1 is context/redundancy and adds no canonical intent, within the selected request-validation scope.')
    results[label] = complete(module, case, plan, plan_path, result)
    case.doCleanups()
assert results['base']['return']['status'] == 'COMPLETED'
assert results['candidate']['exception'] == 'WorkbenchError'
save('documented-review', results)

# Case 4. Legacy missing accounting requeues cleanly, while null review crashes the public CLI.
case = fixture('legacy-review')
prepare(case)
plan = base.plan_sources(case.root, 'docs')
path = case.save(plan, 'source-plan')
legacy_result = case.result()
legacy_result['review'].pop('source_to_output')
assert 'return' in complete(base, case, plan, path, legacy_result)
legacy_plan = candidate.plan_sources(case.root, 'docs')
assert 'source_to_output_accounting_missing' in legacy_plan['process_queue'][0]['reasons']
receipt_path = case.root / 'evidence/knowledge/processing/docs.json'
receipt = json.loads(receipt_path.read_text())
receipt['receipts']['page.md']['review'] = None
receipt_path.write_text(json.dumps(receipt))
results = {'legacy_missing_accounting_queue': legacy_plan['process_queue']}
for label, module in [('base', base), ('candidate', candidate)]:
    try:
        module.plan_sources(case.root, 'docs')
        results[label] = {'unexpected_success': True}
    except Exception as error:
        results[label] = {'exception': type(error).__name__, 'message': str(error)}
stdout, stderr = io.StringIO(), io.StringIO()
with redirect_stdout(stdout), redirect_stderr(stderr):
    try:
        code = cli.main(['--workspace', str(case.root), 'sources', 'plan', '--source', 'docs'])
        cli_result = {'exit_code': code}
    except Exception as error:
        cli_result = {'exception': type(error).__name__, 'message': str(error)}
results['candidate_cli'] = {**cli_result, 'stdout': stdout.getvalue(), 'stderr': stderr.getvalue()}
assert results['base']['exception'] == 'WorkbenchError'
assert results['candidate']['exception'] == 'TypeError'
assert results['candidate_cli']['exception'] == 'TypeError'
save('legacy-review', results)
case.doCleanups()

# Case 5. A JSON-compatible array in the new disposition field bypasses structured errors.
case = fixture('malformed-accounting')
prepare(case)
plan, path = case.plan()
result = case.result(source_to_output=[{'source_range': 'L1', 'disposition': [],
    'target': 'none', 'reason': 'Invalid input should produce a supported validation error.'}])
results = complete(candidate, case, plan, path, result)
assert results['exception'] == 'TypeError'
save('malformed-accounting', results)
case.doCleanups()

save('summary', observations.copy())
print(json.dumps(observations, indent=2))
