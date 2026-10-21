from pathlib import Path
import datetime, hashlib, io, json, os, subprocess, sys, tempfile, time, zipfile
root=Path('/Users/lushevol/code/github/ratan-release-impact/workbench')
repo=root/'repos/ui/mfe-base'
out=root/'tasks/portal-background-session-20261019/evidence/code-review-refresh-20261021'
old=root/'tasks/portal-background-session-20261019/evidence/baseline-reassessment-20261021'
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
stamp=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
write=lambda p,d: p.write_text(json.dumps(d,indent=2)+'\n')
if sys.argv[1]=='setup':
    sandbox=Path(tempfile.mkdtemp(prefix='mfe-review-refresh-',dir='/private/tmp'))
    inputs=json.loads((out/'inputs.json').read_text())
    entries={}
    for variant,rev in [('suite',inputs['head']),('baseline',inputs['base']),('candidate',inputs['head'])]:
        dest=sandbox/variant;dest.mkdir()
        archive=subprocess.check_output(['git','-C',str(repo),'archive','--format=zip',rev])
        with zipfile.ZipFile(io.BytesIO(archive)) as z:
            for item in z.infolist():
                p=dest/item.filename
                if not p.resolve().is_relative_to(dest.resolve()): raise ValueError('archive path')
                if item.is_dir(): p.mkdir(parents=True,exist_ok=True)
                else:
                    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(item))
        files={str(p.relative_to(dest)):sha(p) for p in dest.rglob('*') if p.is_file()}
        (dest/'node_modules').symlink_to(repo/'node_modules',target_is_directory=True)
        if variant!='suite':
            for source,target in [(old/'lifecycle/diagnostic.test.tsx.snapshot','baselineDiagnostic.test.tsx'),(old/'races/raceComparison.test.tsx','raceComparison.test.tsx')]:
                p=dest/'src/pages/Home/common'/target;p.write_bytes(source.read_bytes())
        entries[variant]={'root':str(dest),'revision':rev,'files_sha256':files}
    record={'recorded_at':stamp(),'method':'Exact git archive zip exports; no source checkout changes. Existing diagnostics copied without edits.','sandbox':str(sandbox),'variants':entries,'diagnostics_sha256':{'baselineDiagnostic.test.tsx':sha(old/'lifecycle/diagnostic.test.tsx.snapshot'),'raceComparison.test.tsx':sha(old/'races/raceComparison.test.tsx')},'runner_sha256':sha(Path(__file__)),'node':subprocess.check_output(['node','--version'],text=True).strip(),'versions':{p:json.loads((repo/'node_modules'/p/'package.json').read_text())['version'] for p in ['jest','typescript','axios','react','react-dom']},'limits':['Installed dependencies shared through symlink; no dependency installation or historical recreation.','JSDOM, fake timers, synthetic credentials, and controlled Axios adapters.','No live browser, provider, or production execution.']}
    write(out/'execution-setup.json',record)
    print(json.dumps({'setup':str(sandbox),'node':record['node'],'versions':record['versions']}))
    sys.exit()
setup=json.loads((out/'execution-setup.json').read_text())
kind,variant=sys.argv[1:3]
case=sys.argv[3] if len(sys.argv)>3 else kind
entry=setup['variants'][variant];dest=Path(entry['root']);run=out/(kind+'-'+variant+'-'+case.lower());run.mkdir(exist_ok=False)
env={'BABEL_ENV':'test'}
cmd=['node',str(dest/'node_modules/jest/bin/jest.js'),'--runInBand','--coverage=false','--ci','--reporters=default','--json','--outputFile='+str(run/'result.json'),'--cacheDirectory='+str(Path(setup['sandbox'])/'cache'/variant)]
if kind=='suite':
    cmd=['node',str(dest/'node_modules/jest/bin/jest.js'),'--maxWorkers=2','--workerIdleMemoryLimit=512MB','--coverage=false','--ci','--forceExit','--reporters=default','--json','--outputFile='+str(run/'result.json'),'--cacheDirectory='+str(Path(setup['sandbox'])/'cache'/variant)]
elif kind=='types': cmd=['node',str(dest/'node_modules/typescript/bin/tsc'),'--noEmit','--incremental','false','--pretty','false']
elif kind=='lifecycle':
    env.update({'REVIEW_VARIANT':variant,'REVIEW_ACTUAL_PATH':str(run/'actual.json')})
    cmd+=['--runTestsByPath','src/pages/Home/common/baselineDiagnostic.test.tsx','--testNamePattern='+case]
elif kind=='races':
    env.update({'COMPARISON_SIDE':variant,'CASE_METRICS_PATH':str(run/'actual.json')})
    pattern={'f02':'F02:','f03-before':'F03: delayed old refresh delivered before-login','f03-after':'F03: delayed old refresh delivered after-login','f03-control':'F03: delayed old refresh delivered after-login'}[case]
    if case=='f03-control': env['NO_NEXT_ACQUISITION']='1'
    cmd+=['--runTestsByPath','src/pages/Home/common/raceComparison.test.tsx','--testNamePattern='+pattern]
else: raise ValueError(kind)
unchanged=lambda:all(sha(dest/p)==s for p,s in entry['files_sha256'].items())
record={'kind':kind,'case':case,'variant':variant,'revision':entry['revision'],'command':cmd,'cwd':str(dest),'environment':env,'started_at':stamp(),'setup_sha256':sha(out/'execution-setup.json'),'source_matches_export_before':unchanged(),'status':'RUNNING'}
write(run/'run.json',record)
start=time.monotonic()
try:
    with (run/'execution.log').open('w') as log:
        result=subprocess.run(cmd,cwd=dest,env={**os.environ,**env},stdout=log,stderr=subprocess.STDOUT,timeout=240)
    record.update({'exit_code':result.returncode,'status':'PASSED' if result.returncode==0 else 'FAILED'})
except subprocess.TimeoutExpired:
    record.update({'exit_code':None,'status':'ERROR','error':'240 second timeout'})
record.update({'completed_at':stamp(),'elapsed_seconds':round(time.monotonic()-start,3),'source_matches_export_after':unchanged()})
if (run/'result.json').exists():
    result=json.loads((run/'result.json').read_text());record['jest_summary']={k:result.get(k) for k in ['success','numTotalTestSuites','numPassedTestSuites','numFailedTestSuites','numTotalTests','numPassedTests','numFailedTests','numPendingTests','numTodoTests']}
if (run/'actual.json').exists():record['actual']=json.loads((run/'actual.json').read_text())
record['artifact_sha256']={p.name:sha(p) for p in run.iterdir() if p.is_file() and p.name!='run.json'}
write(run/'run.json',record)
print(json.dumps({k:record.get(k) for k in ['kind','case','variant','status','exit_code','elapsed_seconds','jest_summary','actual','source_matches_export_after']}))
