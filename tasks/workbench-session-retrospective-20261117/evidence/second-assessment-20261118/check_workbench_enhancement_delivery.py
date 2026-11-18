from pathlib import Path
import hashlib,json,re,subprocess
root=Path('/Users/lushevol/code/github/ratan-release-impact/workbench')
task=root/'tasks/workbench-session-retrospective-20261117'
changed=subprocess.check_output(['git','diff','--name-only','a8a38ee49..cad633b99','--','.agents/skills','docs','README.md','tests/README.md'],cwd=root,text=True).splitlines()
files=[root/x for x in changed if x.endswith('.md')]
files += [task/x for x in ('01-maintenance.md','06-optimization-plan.md','07-requirements-and-skills.md')]
errors=[];links=0
for p in files:
    fenced=False
    for n,line in enumerate(p.read_text().splitlines(),1):
        if line.startswith('```'):
            fenced=not fenced
            continue
        if fenced:continue
        for ref in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)',line):
            if re.match(r'\w+://',ref):continue
            links+=1
            path,_,anchor=ref.partition('#')
            target=(p.parent/path).resolve() if path else p
            if not target.exists():
                errors.append(f'{p.relative_to(root)}:{n}: missing {ref}')
                continue
            if not anchor or target.suffix!='.md':continue
            headings=[];inside=False
            for text in target.read_text().splitlines():
                if text.startswith('```'):
                    inside=not inside
                    continue
                if inside or not re.match(r'^#{1,6} ',text):continue
                title=re.sub(r'^#{1,6}\s+','',text).lower()
                headings.append(re.sub(r'[^\w\- ]','',title).replace(' ','-'))
            if anchor not in headings:errors.append(f'{p.relative_to(root)}:{n}: missing anchor {ref}')
        if fenced:continue
    if fenced:errors.append(f'{p.relative_to(root)}: unclosed code fence')
index=json.loads((task/'evidence/behavioral-trials/index.json').read_text())
bindings=0
for t in index['trials']+index.get('extra_trials',[]):
    r=root/t['retained_root']
    manifest=json.loads((r/'evaluation-input.json').read_text())
    assert hashlib.sha256((r/'evaluation-input.json').read_bytes()).hexdigest()==t['input_sha256']
    assert hashlib.sha256((r/'assessment.json').read_bytes()).hexdigest()==t['assessment_sha256']
    for relative,digest in manifest['input_files_sha256'].items():
        assert hashlib.sha256((r/relative).read_bytes()).hexdigest()==digest,(r,relative)
        bindings+=1
    for x in json.loads((r/'skill-source-bindings.json').read_text())['skill_inputs']:
        assert hashlib.sha256((root/x['retained_payload']).read_bytes()).hexdigest()==x['sha256']
        bindings+=1
    assessment=json.loads((r/'assessment.json').read_text())
    response=assessment.get('response_path','outputs/response.md')
    for name in (response,'outputs/actions.json'):
        actual=r/'artifacts/modified-inputs'/name if name in manifest['input_files_sha256'] else r/name
        assert actual.is_file(),(r,name)
    actual_response=r/'artifacts/modified-inputs'/response if response in manifest['input_files_sha256'] else r/response
    if 'response_sha256' in assessment:assert hashlib.sha256(actual_response.read_bytes()).hexdigest()==assessment['response_sha256']
schedule=json.loads((task/'evidence/behavioral-trials/operator/schedule.json').read_text())
g=schedule.get('reader_generated_draft',{})
generator_bindings=0
if g.get('status')=='COMPLETED':
    r=task/'evidence/behavioral-trials/reader-draft-generation'
    m=json.loads((r/'evaluation-input.json').read_text())
    assert hashlib.sha256((r/'evaluation-input.json').read_bytes()).hexdigest()==g['input_sha256']
    for relative,digest in m['input_files_sha256'].items():
        assert hashlib.sha256((r/relative).read_bytes()).hexdigest()==digest
        generator_bindings+=1
    for x in json.loads((r/'skill-source-bindings.json').read_text())['skill_inputs']:
        assert hashlib.sha256((root/x['retained_payload']).read_bytes()).hexdigest()==x['sha256']
        generator_bindings+=1
    for name,key in [('outputs/response.md','response_sha256'),('outputs/actions.json','actions_sha256')]:
        assert hashlib.sha256((r/name).read_bytes()).hexdigest()==g[key]
for x in index['operator_snapshots']:
    assert hashlib.sha256((task/'evidence/behavioral-trials'/x['path']).read_bytes()).hexdigest()==x['sha256']
import sys
if '--complete' in sys.argv:
    assert index['retained']==index['scheduled']==40
    assert index['extra_trials_retained']==2
    assert {t['case_id'] for t in index['extra_trials']}=={'current-results','source-dispositions'}
    assert index['reader_draft_status']=='COMPLETED'
    required=[x for x in schedule['trials'] if x.get('required',True)]
    assert len({x['case_id'] for x in required})==13
    assert all(x['status']=='ASSESSED' for x in required)
    assert len(index['optional_not_executed'])==10
    for t in index['trials']+index.get('extra_trials',[]):
        a=json.loads((root/t['retained_root']/'assessment.json').read_text())
        assert a['scope_integrity']['outcome']=='PASSED',t['id']
        if t['variant'] in ('candidate','installed'):
            assert not a['material_candidate_failure'],t['id']
result={'status':'PASSED' if not errors else 'FAILED','authored_markdown_files':len(files),'local_links_checked':links,'errors':errors,'retained_trials':index['retained'],'extra_trials':index['extra_trials_retained'],'required_trials':index['scheduled'],'optional_not_executed':len(index['optional_not_executed']),'hash_bindings_checked':bindings,'generator_hash_bindings_checked':generator_bindings,'limits':['Automated link and byte checks do not establish complete ASD writing review.','Semantic outcomes require the retained independent assessments.']}
print(json.dumps(result,indent=2))
if __name__=='__main__':
    import sys
    if '--save' in sys.argv:(task/'evidence/final-delivery-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    raise SystemExit(bool(errors))
