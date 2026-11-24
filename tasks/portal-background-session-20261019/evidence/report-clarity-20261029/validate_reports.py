"""Check authored reports, local references, source identity, and evidence reconciliation."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import datetime
import hashlib
import html
import json
import re
import subprocess

HERE=Path(__file__).resolve().parent
TASK=HERE.parent.parent
ROOT=TASK.parent.parent
RUN=TASK/'evidence/remaining-execution-20261029'
OLD=TASK/'evidence/release-report-execution-20261029'
DOCUMENTS=[TASK/n for n in ['08-test-execution-renewal.md','09-renewal-coverage.md',
                           '10-release-confidence.md','10-release-confidence.html','evidence/index.md']]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def slug(text):
    text=re.sub('<[^>]*>','',text)
    return re.sub(r'[^\w\- ]','',text.lower()).replace(' ','-')


def main():
    errors=[];commands=[];checked=0;referenced=set()
    for doc in DOCUMENTS:
        body=doc.read_text()
        links=re.findall(r'\]\(([^)\s]+)(?:\s+"[^"]*")?\)',body)
        links+=re.findall(r'(?:href|src)=["\']([^"\']+)["\']',body)
        for raw in links:
            raw=html.unescape(raw.strip('<>'))
            parsed=urlsplit(raw)
            if parsed.scheme or raw.startswith('//'):
                continue
            target=(doc.parent/unquote(parsed.path)).resolve() if parsed.path else doc
            checked+=1
            if not target.is_file():
                errors.append({'type':'missing-link-target','document':str(doc.relative_to(ROOT)),'link':raw})
                continue
            referenced.add(target)
            fragment=unquote(parsed.fragment)
            if not fragment:continue
            text=target.read_text(errors='replace')
            line=re.fullmatch(r'L(\d+)(?:-L?(\d+))?',fragment)
            if line:
                first,last=int(line[1]),int(line[2] or line[1])
                if not 1<=first<=last<=len(text.splitlines()):
                    errors.append({'type':'invalid-line-locator','link':raw})
            elif target.suffix.lower() in ['.md','.html']:
                anchors=set(re.findall(r'id=["\']([^"\']+)["\']',text))
                anchors.update(slug(m) for m in re.findall(r'^#{1,6}\s+(.+?)\s*#*$',text,re.M))
                if fragment not in anchors:
                    errors.append({'type':'missing-anchor','document':str(doc.relative_to(ROOT)),'link':raw})
    for doc in DOCUMENTS[:3]:
        args=[str(ROOT/'.venv/bin/ai-sdlc'),'lint',str(doc.relative_to(ROOT))]
        p=subprocess.run(args,cwd=ROOT,text=True,capture_output=True)
        result=json.loads(p.stdout) if p.stdout.strip().startswith('{') else p.stdout+p.stderr
        commands.append({'command':args,'exit_code':p.returncode,'result':result})
        if p.returncode:errors.append({'type':'artifact-lint','path':str(doc),'exit_code':p.returncode})
    for args in [[str(ROOT/'.venv/bin/ai-sdlc'),'--workspace',str(ROOT),'validate'],['git','diff','--check']]:
        p=subprocess.run(args,cwd=ROOT,text=True,capture_output=True)
        result=json.loads(p.stdout) if p.stdout.strip().startswith('{') else p.stdout+p.stderr
        commands.append({'command':args,'exit_code':p.returncode,'result':result})
        if p.returncode:errors.append({'type':'command','command':args,'exit_code':p.returncode})
    audit=json.loads((HERE/'execution-reason-audit.json').read_text())
    criteria=json.loads((HERE/'ac-explanation-audit.json').read_text())['criteria']
    from collections import Counter
    if Counter(r['status'] for r in audit['rows'])!={'FAILED':15,'PARTIALLY_EXECUTED':199,'BLOCKED':71}:
        errors.append({'type':'explanation-count-mismatch'})
    if len(criteria)!=7:errors.append({'type':'criterion-count-mismatch'})
    binding=json.loads((RUN/'execution-source-binding.json').read_text())
    source=Path(binding['source']);mismatches=[]
    for name,expected in binding['source_hashes'].items():
        f=source/name
        if not f.is_file() or sha(f)!=expected:mismatches.append(name)
    if mismatches:errors.append({'type':'immutable-source-mismatch','paths':mismatches})
    freshness={}
    for name,location,expected in [
        ('frontend','repos/ui/mfe-base','66c6411ade58e4d134e381c2baee8ad3f76a8dbf'),
        ('bff','repos/services/single-ui-bff','19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a'),
        ('sdk','repos/libraries/single-ui-sdk-starter','b0aa82005e7f14202f85f5ef583f25e42da9eeb3')]:
        actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT/location,text=True).strip()
        freshness[name]={'expected':expected,'head':actual}
        if actual!=expected:errors.append({'type':'candidate-head-mismatch','repository':name})
    for file,expected in [
        (TASK/'06-test-cases.md','5622dab3b635113ff0137fbf66489f385bbcb11dc4444ec0070f7203d19a7037'),
        (ROOT/'knowledge/candidates/requirements/REQ-active-session-renewal.md','3db69ca6827b4afa0eb9f3182f15045f80dac012f9d37004d62144740424c359')]:
        if sha(file)!=expected:errors.append({'type':'definition-hash-mismatch','path':str(file.relative_to(ROOT))})
    inv=json.loads((RUN/'aggregate/final-inventory.json').read_text())
    for r in inv['rows']:
        if not r.get('result') or sha(TASK/r['result'])!=r['result_sha256']:
            errors.append({'type':'result-hash-mismatch','id':r['id']})
    impact=json.loads((OLD/'failure-impacts.json').read_text())
    md=(TASK/'10-release-confidence.md').read_text()
    for f in impact['cases']:
        if f['case_id'] not in md:errors.append({'type':'missing-failure-row','id':f['case_id']})
    # Check fixture credentials privately. Only a zero/nonzero result is retained.
    fixture=ROOT/'.workbench/portal-session-real-20261019/local-bff/runner/local/portalsession/LocalSessionApplication.java'
    credentials=[]
    if fixture.exists():
        fixture_text=fixture.read_text()
        for field in ['PASSWORD']:
            match=re.search(r'public static final String '+field+r'="([^"]+)"',fixture_text)
            if match:credentials.append(match[1].encode())
    secret_matches=[]
    for base in [RUN,HERE]:
        for f in base.rglob('*'):
            if f.is_file() and f.suffix in ['.json','.log','.mjs','.py','.java','.md','.html']:
                data=f.read_bytes()
                if any(value in data for value in credentials):secret_matches.append(str(f.relative_to(ROOT)))
    if secret_matches:errors.append({'type':'fixture-credential-retained','paths':secret_matches})
    source_files=[]
    for base in [RUN,HERE]:
        for f in sorted(base.rglob('*')):
            if f.is_file() and '__pycache__' not in f.parts and f.name not in ['source-manifest.json','validation.json']:
                source_files.append({'path':str(f.relative_to(ROOT)),'sha256':sha(f),'bytes':f.stat().st_size})
    source_files.extend({'path':str(f.relative_to(ROOT)),'sha256':sha(f),'bytes':f.stat().st_size} for f in DOCUMENTS)
    existing={f['path'] for f in source_files}
    for f in sorted(referenced):
        if f in [HERE/'validation.json',HERE/'source-manifest.json']:
            continue
        name=str(f.relative_to(ROOT))
        if name not in existing:
            source_files.append({'path':name,'sha256':sha(f),'bytes':f.stat().st_size})
            existing.add(name)
    (HERE/'source-manifest.json').write_text(json.dumps({'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'files':source_files,'limits':['Hashes bind retained bytes. They do not establish source authority, business acceptance, or deployment identity.']},indent=2)+'\n')
    qa=json.loads((HERE/'html-qa.json').read_text()) if (HERE/'html-qa.json').exists() else {'status':'NOT_RUN'}
    if qa['status']!='PASSED' or qa.get('visual_review')!='PASSED':errors.append({'type':'html-qa-incomplete'})
    data={'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASSED' if not errors else 'FAILED',
          'scope':'Presentation clarification: 285 execution reasons, seven criterion explanations, and plain file coverage wording. No new case execution.',
          'commands':commands,'links':{'checked':checked,'errors':[x for x in errors if 'link' in x.get('type','') or 'anchor' in x.get('type','')]},
          'immutable_source':{'files_checked':len(binding['source_hashes']),'mismatches':mismatches},
          'candidate_freshness':freshness,
          'inventory':{'total':inv['total'],'counts':inv['counts'],'result_hashes_checked':len(inv['rows'])},
          'failure_impacts':{'rows':len(impact['cases']),'all_current_failed_cases_covered':not impact['missing_current_failures']},
          'fixture_credentials':{'password_values_retained':bool(secret_matches),'matching_files':len(secret_matches),
                                 'synthetic_principal_identity':'Retained where account ownership is an asserted predicate.'},
          'html_qa':qa,'source_manifest_sha256':sha(HERE/'source-manifest.json'),
          'writing_review':{'standard':'ASD-STE100','automated_check':'PASSED' if not errors else 'FAILED',
                            'asd_review':'PENDING','reviewer':None,'reviewed_at':None,
                            'limitations':['Automated checks do not check the complete approved dictionary or grammar rules.']},
          'errors':errors,'limits':['Automated validation does not establish business correctness, human acceptance, or release authorization.']}
    (HERE/'validation.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'status':data['status'],'links_checked':checked,'source_files_checked':len(binding['source_hashes']),
                      'result_hashes_checked':len(inv['rows']),'errors':errors},indent=2))
    raise SystemExit(bool(errors))


if __name__=='__main__':
    main()
