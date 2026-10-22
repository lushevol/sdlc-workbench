from pathlib import Path
import datetime,hashlib,json,subprocess,urllib.request
root=Path.cwd();out=root/'tasks/ui-test-coverage-20261022/evidence/screenshot-review-20261022/environment';base=root/'.workbench/current-bff-audit'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
prior=root/'tasks/ui-test-coverage-20261022/evidence/step-audit-20261022/current-bff-build/final-runtime/manifest.json';old=json.loads(prior.read_text());config=json.loads((out/'stack-config-02.json').read_text());lifecycle=json.loads((out/'launch-02/stack-lifecycle.json').read_text())
compiled=[];errors=[]
for item in old['compiledClasses']:
 p=base/'classes'/item['path'];actual=sha(p);compiled.append({**item,'currentSha256':actual,'matches':actual==item['sha256']})
 if actual!=item['sha256']:errors.append(str(p))
libs=[];cp=[Path(p) for p in (base/'classpath.txt').read_text().split(':') if p.strip()];oldlib={p['name']:p for p in old['classpathLibraries']}
for p in cp:
 actual=sha(p);expected=oldlib[p.name]['sha256'];libs.append({'path':str(p),'name':p.name,'sha256':actual,'matches':actual==expected})
 if actual!=expected:errors.append(str(p))
processes=[]
for service in lifecycle['services']:
 r=subprocess.run(['ps','-p',str(service['pid']),'-o','pid=','-o','pgid=','-o','command='],capture_output=True,text=True)
 processes.append({'service':service['name'],'expectedPid':service['pid'],'exitCode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 if r.returncode:errors.append('missing process '+service['name'])
http=[];opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
for url in config['readyUrls']:
 with opener.open(url,timeout=5) as r:
  data=r.read();item={'url':url,'status':r.status,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
  if url.endswith('/health'):item['health']=json.loads(data)
  http.append(item)
manifest={'recordedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASSED' if not errors else 'FAILED','launcherPid':21980,'ownedServices':processes,'http':http,'priorRuntimeManifest':{'path':str(prior.relative_to(root)),'sha256':sha(prior)},'compiledClassCount':len(compiled),'compiledClasses':compiled,'classpathLibraryCount':len(libs),'classpathLibraries':libs,'currentBffSourceRevision':'834b4155232222347220e47139a502ee43a9cbdf','runtimeLimits':{'frontend':'Actual prepared MFE and controlled tenant responses. Prior toolkit and dependency substitutions remain.','bff8090':'Current compiled BFF with PostgreSQL; SpringBoot3 isolated bootstrap, controlled OUD/EMS2, no production wiring equivalence.','bff8129':'Prior session fixture BFF with shortened timeouts and H2. It is separate from current BFF8090.','database':'Copied prior stopped disposable PostgreSQL data. No new migration or business source changes.'},'errors':errors}
(out/'readiness.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps({k:manifest[k] for k in ['status','compiledClassCount','classpathLibraryCount','errors']}))
