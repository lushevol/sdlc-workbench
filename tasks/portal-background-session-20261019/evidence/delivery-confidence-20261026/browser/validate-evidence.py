from pathlib import Path
import hashlib,json,datetime,re,subprocess
root=Path.cwd();base=root/'tasks/portal-background-session-20261019/evidence/delivery-confidence-20261026/browser';checks=[];errors=[];json_count=0;artifact_count=0
for p in base.rglob('*.json'):
 try:json.loads(p.read_text());json_count+=1
 except Exception as e:errors.append({'path':str(p.relative_to(base)),'error':str(e)})
for p in base.glob('*/*/case-summary.json'):
 d=json.loads(p.read_text())
 if d['status']=='RUNNING':errors.append({'path':str(p.relative_to(base)),'error':'Case remains RUNNING.'})
 for rel,digest in d.get('artifacts',{}).items():
  target=p.parent/rel;artifact_count+=1
  if not target.exists() or hashlib.sha256(target.read_bytes()).hexdigest()!=digest:errors.append({'path':str(target.relative_to(base)),'error':'Artifact hash mismatch or missing.'})
checks.append({'id':'json-and-artifact-integrity','status':'PASSED' if not errors else 'FAILED','json_count':json_count,'artifact_count':artifact_count})
for name in ['served-source-binding.json','test-commit-binding.json']:
 d=json.loads((base/name).read_text());passed=all(x['status']=='PASSED' for x in d['refs'].values()) if 'refs' in d else d['status']=='PASSED';checks.append({'id':name,'status':'PASSED' if passed else 'FAILED'})
 d_error=None if passed else {'path':name,'error':'Binding failed.'}
 if d_error:errors.append(d_error)
source=(root/'.workbench/session-post-change-20261020/bff-fast/runner/local/portalsession/LocalSessionApplication.java').read_text();sensitive=[]
for field in ['USER','PASSWORD']:
 match=re.search(r'public static final String '+field+r'="([^"]+)"',source)
 if match:sensitive.append(match.group(1))
text_files=0;secret_paths=[]
for p in base.rglob('*'):
 if not p.is_file() or p.suffix not in ['.json','.txt','.py','.mjs','.cjs','.snapshot']:continue
 text_files+=1;s=p.read_text(errors='replace')
 if any(value and value in s for value in sensitive) or re.search(r'eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}',s):secret_paths.append(str(p.relative_to(base)))
checks.append({'id':'credential-and-token-retention','status':'PASSED' if not secret_paths else 'FAILED','text_files_checked':text_files,'matches':secret_paths})
if secret_paths:errors.append({'error':'Potential sensitive data retained.','paths':secret_paths})
r={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASSED' if not errors else 'FAILED','checks':checks,'errors':errors,'limits':['Checks establish file integrity and known credential exclusion. They do not establish passing business predicates or complete ASD review.']}
(base/'validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
