from pathlib import Path
import json, hashlib, collections, datetime, shutil
root=Path.cwd()
out=Path(__file__).parent
sha=lambda b:hashlib.sha256(b).hexdigest()
binding=json.loads((out/'../execution-source-binding.json').read_text())
definitions=out/'../../comprehensive-renewal-20261028/workspace-transport-cases.json'
cases=json.loads(definitions.read_text())['cases']
original=json.loads((out/'attempt1/summary.json').read_text())
runs=[('attempt1/summary.json',original)]
for name in ['rerun-summary-final.json','predicate-rerun-summary.json','closed-tab-rerun-summary.json','loader-proof-summary.json']:
 runs.append((name,json.loads((out/name).read_text())))
rows=[]
for c in cases:
 p=out/c['id']/'result.json'
 r=json.loads(p.read_text())
 matched=[(name,s) for name,s in runs if s['started_at']<=r['started_at']<=s.get('completed_at','9999') and any(x['id']==c['id'] for x in s['cases'])]
 if not matched:raise RuntimeError('No runner binding for '+c['id'])
 run_path,s=matched[-1]
 r['runner_sha256']=s['runner_sha256']
 r['runner_summary']='../'+run_path
 r['definition_json']='../../../comprehensive-renewal-20261028/workspace-transport-cases.json'
 r['definition_json_sha256']=sha(definitions.read_bytes())
 r['execution_mode']='actual-immutable-portal-browser-with-synthetic-modules-and-service-peers' if r.get('setup_complete') else 'blocked-before-complete-browser-setup'
 r['acceptance_limit']='A passing observation does not approve open policy or establish target-deployment suitability.'
 r['executed_source_identity']=[]
 for s in c['sources']:
  if s['path'].startswith('repos/ui/mfe-base/'):
   rel=s['path'].removeprefix('repos/ui/mfe-base/')
   actual=binding['source_hashes'].get(rel)
   r['executed_source_identity'].append({'path':rel,'revision':binding['revision'],'sha256':actual,'canonical_definition_source_sha256':s.get('sha256'),'definition_source_matches':actual==s.get('sha256'),'execution_binding':'../../execution-source-binding.json'})
 if any(not s['definition_source_matches'] for s in r['executed_source_identity']):
  r['definition_source_limit']='Canonical source inventory includes dirty Home bytes. Execution uses the immutable candidate and recorded hashes; it does not execute those dirty bytes.'
 if c['id']=='RN-W015':
  for key in ['observation_before','observation_after']:
   r[key]['descriptor_sha256']=sha(json.dumps(r[key]['descriptors'],sort_keys=True,separators=(',',':')).encode())
 r['execution_class']='executed' if r['status'] in ['PASSED','FAILED'] else 'partial-blocked' if r.get('assertions') else 'blocked-not-executed'
 r['owner']='unknown application, transport, or security owner'
 p.write_text(json.dumps(r,indent=2)+'\n')
 rows.append({'id':c['id'],'status':r['status'],'execution_class':r['execution_class'],'assertions':len(r['assertions']),'failed_assertions':sum(a['status']=='FAILED' for a in r['assertions']),'policy_acceptance':r['business_acceptance'],'result':c['id']+'/result.json','result_sha256':sha(p.read_bytes()),'runner_sha256':r['runner_sha256'],'blocker':r.get('blocker'),'error':r.get('error'),'canonical_definition_source_mismatch':any(not s['definition_source_matches'] for s in r['executed_source_identity'])})
summary={**original,'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'RECONCILED','cases':rows,'counts':dict(collections.Counter(r['status'] for r in rows)),'execution_classes':dict(collections.Counter(r['execution_class'] for r in rows)),'assertion_count':sum(r['assertions'] for r in rows),'failed_assertion_count':sum(r['failed_assertions'] for r in rows),'passing_policy_observations':[r['id'] for r in rows if r['status']=='PASSED' and r['policy_acceptance']=='BLOCKED_POLICY'],'runner_summaries':[{'path':name,'sha256':sha((out/name).read_bytes()),'runner_sha256':s['runner_sha256']} for name,s in runs],'classification_limit':'FAILED requires a retained failing business predicate. Setup, driver, capture, unavailable environment, or missing full predicates remain blocked. Four blocked cases retain partial observations. Five passing cases only verify policy-open observation requirements.','source_definition_limit':'26 canonical definitions cite dirty Home source hash 4c8ad5b55b0e677dd3cfb02e239cdceff795d42e67f33c3397348bd8718b381f. Execution uses immutable candidate Home hash cf5f6312f3fb3524234304e0292e1a82fd63daa99d4442732bc8f6f245144e6a. Each result retains both identities.'}
summary.pop('runner_sha256',None)
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
manifest={'created_at':summary['completed_at'],'files':[{'path':str(p.relative_to(out)),'sha256':sha(p.read_bytes())} for p in sorted(out.rglob('*')) if p.is_file() and p.name!='evidence-manifest.json']}
(out/'evidence-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({k:summary[k] for k in ['counts','execution_classes','assertion_count','failed_assertion_count','passing_policy_observations']},indent=2))
