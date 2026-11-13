"""Retain the real declared consumer drift case without changing domain knowledge."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from ai_sdlc_workbench.question_reconciliation import reconcile_questions
root=Path.cwd();base=Path(__file__).resolve().parent
manifest=json.loads((base/'questions-manifest.json').read_text());result=reconcile_questions(manifest,root)
(base/'questions-result.json').write_text(json.dumps(result,indent=2)+'\n')
checks={'resolved_status_retained':result['questions'][0]['status']=='ANSWERED_FROM_EVIDENCE','missing_propagation_found':any(r['code']=='ANSWER_PROPAGATION_MISSING' for r in result['findings']),'candidate_version_1':result['questions'][0]['consumers'][0]['observed_version']==1,'answer_has_three_sources':len(result['questions'][0]['answer_source_references'])==3,'business_not_verified':result['verification']=='NOT_VERIFIED','sources_unchanged':all(hashlib.sha256((root/p['path']).read_bytes()).hexdigest()==p['sha256'] for p in [manifest['questions'][0]['document'],*manifest['questions'][0]['consumers']])}
receipt={'case_id':'QUESTIONS-EMS3','status':'PASSED' if all(checks.values()) else 'FAILED','checked_at':datetime.now(timezone.utc).isoformat(),'checks':checks,'files':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [root/'core/question_reconciliation.py',root/'tests/test_question_reconciliation.py',Path(__file__).resolve()]},'limits':['Actual stale EMS3 claim remains unchanged in candidate knowledge. Human review and governed publication remain separate.','This check identifies missing references; semantic conflict was confirmed by source inspection.']}
(base/'questions-case.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status']);assert all(checks.values())
