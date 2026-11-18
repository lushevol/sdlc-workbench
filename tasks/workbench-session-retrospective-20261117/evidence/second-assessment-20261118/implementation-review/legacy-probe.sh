.venv/bin/python - <<'PY'
import hashlib
import json
import subprocess
from tests.test_incremental_ingestion import IncrementalIngestionTests

case = IncrementalIngestionTests()
case.setUp()
try:
    case.page()
    case.refresh()
    case.select()
    plan, plan_path = case.plan()
    case.complete(plan, plan_path, case.result())
    receipt_path = case.root / 'evidence/knowledge/processing/docs.json'
    receipt = json.loads(receipt_path.read_text())
    receipt['receipts']['page.md']['review'].pop('source_to_output')
    receipt_path.write_text(json.dumps(receipt))
    before = receipt_path.read_bytes()
    replanned = case.plan()[0]
    assert [item['path'] for item in replanned['process_queue']] == ['page.md']
    assert 'source_to_output_accounting_missing' in replanned['process_queue'][0]['reasons']
    assert before == receipt_path.read_bytes()
    print(json.dumps({'legacy_without_accounting': 'PASSED', 'receipt_unchanged': True, 'queue_count': 1}))
finally:
    case.doCleanups()

paths = ['.agents/skills/manage-knowledge-lifecycle', '.agents/skills/ingest-knowledge', '.agents/skills/resolve-knowledge-questions', '.agents/skills/review-knowledge-claims', '.agents/skills/evaluate-knowledge-retrieval', '.agents/skills/evaluate-harness', '.claude/skills/evaluate-harness', 'scaffold.json', 'README.md', 'docs/KNOWLEDGE_LIFECYCLE.md', 'docs/QUESTION_RECONCILIATION.md', 'core/ingestion/incremental.py', 'tests/test_incremental_ingestion.py', 'tests/test_source_preparation_cli.py', 'tests/test_knowledge_layout.py', 'tests/test_workspace_layout.py']
patch = subprocess.check_output(['git', 'diff', '--binary', 'a8a38ee49', 'HEAD', '--', *paths])
print(json.dumps({'comparison': 'a8a38ee49a67d99b517f2aac41a421a7300df2f4..eda18511447612d69caef037c8087147d31e1c9f', 'selected_diff_sha256': hashlib.sha256(patch).hexdigest(), 'paths_changed_since_f5b1b072b': subprocess.check_output(['git','diff','--name-only','f5b1b072b','HEAD','--',*paths], text=True).splitlines()}))
PY
