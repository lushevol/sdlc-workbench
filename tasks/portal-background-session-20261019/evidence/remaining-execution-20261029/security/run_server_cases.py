"""Run additional isolated BFF/SDK cases with exact committed classes and retained assertions."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, tempfile

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
runtime = Path(tempfile.mkdtemp(prefix='remaining-security-'))
classes = runtime/'classes'; classes.mkdir()
bff=ROOT/'repos/services/single-ui-bff'
sdk=ROOT/'repos/libraries/single-ui-sdk-starter'
dep=ROOT/'.workbench/current-bff-audit'
jars=[Path(x) for x in (dep/'classpath.txt').read_text().strip().split(':') if x.endswith('.jar')]
cp=str(dep/'classes')+':'+':'.join(map(str,jars))
bff_paths=['controller/v2/JwtAuthenticationController.java','util/JwtTokenUtil.java','service/v1/implementation/SessionServiceImplementation.java','service/v2/authorization/TileAuthorizationService.java']
sdk_paths=['filter/AuthTokenFilter.java','filter/ResponseOfError.java','properties/AuthProperties.java','util/JWTSessionData.java','util/JwtTokenUtil.java','exception/JwtException.java']
rows=[]; sources=[]
for repo,prefix,paths in [(bff,'src/main/java/com/scb/sso/singleuibff',bff_paths),(sdk,'single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth',sdk_paths)]:
    rev=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
    for rel in paths:
        full=prefix+'/'+rel; data=subprocess.check_output(['git','-C',str(repo),'show',rev+':'+full]); source=runtime/full; source.parent.mkdir(parents=True,exist_ok=True);source.write_bytes(data);sources.append(source)
        rows.append({'repository':str(repo.relative_to(ROOT)),'revision':rev,'path':full,'sha256':hashlib.sha256(data).hexdigest()})
record={'started_at':datetime.now(timezone.utc).isoformat(),'sources':rows,'runtime':str(runtime),'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'probe_sha256':hashlib.sha256((OUT/'RemainingSecurityProbe.java').read_bytes()).hexdigest(),'java':'OpenJDK17','dependencies':[{'name':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in jars]}
cmd=['/opt/homebrew/opt/openjdk@17/bin/javac','--release','17','-cp',cp,'-d',str(classes),*map(str,sources),str(OUT/'RemainingSecurityProbe.java')]
run=subprocess.run(cmd,capture_output=True,text=True);(OUT/'compile.log').write_text(run.stdout+run.stderr);record['compile_exit']=run.returncode
if not run.returncode:
    ext=classes/'mockito-extensions/org.mockito.plugins.MockMaker';ext.parent.mkdir(parents=True);ext.write_text('mock-maker-subclass\n')
    run=subprocess.run(['/opt/homebrew/opt/openjdk@17/bin/java','-cp',str(classes)+':'+cp,'RemainingSecurityProbe',str(OUT)],capture_output=True,text=True,timeout=90)
    (OUT/'server-run.log').write_text(run.stdout+run.stderr);record['execution_exit']=run.returncode
record['completed_at']=datetime.now(timezone.utc).isoformat();record['cases']=[json.loads(p.read_text()) for p in sorted(OUT.glob('rn-s*/result.json'))]
record['passed']=sum(c['status']=='PASSED' for c in record['cases']);record['failed']=sum(c['status']=='FAILED' for c in record['cases']);record['case_count']=len(record['cases']);record['status']='COMPLETED_WITH_FAILURES' if record['failed'] else 'COMPLETED'
if record['compile_exit'] or record.get('execution_exit',1):record['status']='RUNNER_ERROR'
(OUT/'server-execution.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:record.get(k) for k in ['status','compile_exit','execution_exit','passed','failed','case_count']},indent=2))
raise SystemExit(record['compile_exit'] or record.get('execution_exit',1))
