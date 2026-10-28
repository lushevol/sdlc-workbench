"""Compile exact BFF classes and run isolated controller assertions without network access."""
from pathlib import Path
import hashlib,json,subprocess,datetime
root=Path(__file__).resolve().parents[4]
out=Path(__file__).resolve().parent
scratch=root/'.workbench/security-renewal-20261028'; classes=scratch/'classes'; classes.mkdir(parents=True,exist_ok=True)
repo=root/'repos/services/single-ui-bff'; depdir=root/'.workbench/current-bff-audit'
jars=[Path(p) for p in (depdir/'classpath.txt').read_text().strip().split(':') if p.endswith('.jar')]
cp=str(depdir/'classes')+':'+':'.join(str(p) for p in jars)
paths=['controller/v2/JwtAuthenticationController.java','util/JwtTokenUtil.java','service/v1/implementation/SessionServiceImplementation.java','service/v2/authorization/TileAuthorizationService.java']
sources=[repo/'src/main/java/com/scb/sso/singleuibff'/p for p in paths]; probe=out/'SecurityLogoutProbe.java'; source_rows=[]
rev=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
assert rev=='19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a',rev
for p in sources:
 rel=p.relative_to(repo).as_posix(); data=p.read_bytes(); assert data==subprocess.check_output(['git','-C',str(repo),'show',rev+':'+rel]); source_rows.append({'path':rel,'revision':rev,'sha256':hashlib.sha256(data).hexdigest()})
cmd=['/opt/homebrew/opt/openjdk@17/bin/javac','--release','17','-cp',cp,'-d',str(classes),*[str(p) for p in sources],str(probe)]
record={'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':source_rows,'probe_sha256':hashlib.sha256(probe.read_bytes()).hexdigest(),'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'java':'OpenJDK 17','limits':['Actual JWT controller, RSA verification and session service. Mocked repository and entitlement dependencies. Servlet mocks. No HTTP, browser, production services or target evidence.']}
p=subprocess.run(cmd,capture_output=True,text=True); (out/'security-probe-compile.txt').write_text(p.stdout+p.stderr); record['compile_exit']=p.returncode
if p.returncode==0:
 ext=classes/'mockito-extensions/org.mockito.plugins.MockMaker'; ext.parent.mkdir(parents=True,exist_ok=True); ext.write_text('mock-maker-subclass\n')
 q=subprocess.run(['/opt/homebrew/opt/openjdk@17/bin/java','-cp',str(classes)+':'+cp,'SecurityLogoutProbe',str(out)],capture_output=True,text=True,timeout=45); record['execution_exit']=q.returncode; record['mockito_maker']='subclass'; (out/'security-probe-output.txt').write_text(q.stdout+q.stderr)
 record['compiled_hashes']={str(p.relative_to(scratch)):hashlib.sha256(p.read_bytes()).hexdigest() for p in classes.rglob('*.class')}
 record['dependencies']=[{'name':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in jars]
 cases=[json.loads(p.read_text()) for p in sorted(out.glob('*-credential-case.json'))]+[json.loads((out/p).read_text()) for p in ('valid-logout-case.json','expired-logout-case.json')]
 record['cases']=cases; record['passed']=sum(bool(x.get('assertions_passed',x.get('security_assertion_passed'))) for x in cases); record['failed']=len(cases)-record['passed']; record['case_count']=len(cases)
 record['initial_attempt']='security-probe-execution-initial.json'
record['status']='FAILED' if record.get('compile_exit') or record.get('execution_exit') or record.get('failed',1) else 'PASSED'
record['finished_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(out/'security-probe-execution.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:record.get(k) for k in ('status','compile_exit','execution_exit','case_count','passed','failed')},indent=2))
raise SystemExit(record.get('compile_exit',1) or record.get('execution_exit',1) or int(record.get('failed',1)>0))
