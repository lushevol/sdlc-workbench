import datetime, hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).parent
schedule=json.loads((ROOT/'schedule.json').read_text())
case_id=sys.argv[1]
results=[]
for trial in schedule['trials']+schedule.get('extra_trials',[]):
    if trial['case_id']!=case_id or trial['status']!='PREPARED':continue
    root=Path(trial['root'])
    manifest_path=root/'evaluation-input.json'
    assert hashlib.sha256(manifest_path.read_bytes()).hexdigest()==trial['input_sha256']
    manifest=json.loads(manifest_path.read_text())
    for relative,digest in manifest['input_files_sha256'].items():
        assert hashlib.sha256((root/relative).read_bytes()).hexdigest()==digest,(trial['id'],relative)
    for path,digest in manifest['skill_inputs_sha256'].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,(trial['id'],path)
    results.append({'trial_id':trial['id'],'manifest_sha256':trial['input_sha256'],'input_bindings':len(manifest['input_files_sha256']),'skill_bindings':len(manifest['skill_inputs_sha256']),'status':'PASSED'})
assert results,case_id
receipt={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'case_id':case_id,'trials':results}
(ROOT/('preflight-'+case_id+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
