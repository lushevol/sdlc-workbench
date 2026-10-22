from pathlib import Path
import datetime,json,os,subprocess,time,urllib.request
base=Path(__file__).resolve().parent
cp=str(base/'classes')+':'+(base/'classpath.txt').read_text()
command=['/opt/homebrew/opt/openjdk@17/bin/java','-Djava.net.useSystemProxies=false','-cp',cp,'local.portalsession.LocalSessionApplication']
env={'PATH':'/opt/homebrew/opt/openjdk@17/bin:/usr/bin:/bin','JAVA_HOME':'/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home','LANG':'en_US.UTF-8'}
with (base/'runtime.stdout.log').open('ab') as out,(base/'runtime.stderr.log').open('ab') as err:
 process=subprocess.Popen(command,cwd=base,env=env,stdin=subprocess.DEVNULL,stdout=out,stderr=err,start_new_session=True)
result={'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':process.pid,'listen':'127.0.0.1:8090','context_path':'/api/auth','source_revision':'834b4155232222347220e47139a502ee43a9cbdf','clock':'REAL_WALL_CLOCK','effective_timeouts':{'access_minutes':1,'refresh_minutes':2,'refresh_extra_seconds':24,'absolute_minutes':60},'substitutes':['synthetic OUD identity','actual category/tile/importmap services and JPA repositories','fixed local EMS2 admin role entitlements','no-op analytics','disposable PostgreSQL18.4 with all11currentmigrationfilesappliedunchanged','isolated Spring bootstrap without private starters'],'real_paths':['JwtAuthenticationController','JwtTokenUtil RSA generation and verification','SessionServiceImplementation','Actual admincontrollers/services/JPA repositories with PostgreSQL migrations'],'private_keys':'generated only in process memory','log_policy':'request route/timing/status and issued-token hashes/claims; no raw tokens or private keys'}
for i in range(50):
 if process.poll() is not None:result.update(status='EXITED',exit_code=process.returncode);break
 try:
  with urllib.request.urlopen('http://127.0.0.1:8090/api/auth/local/health',timeout=1) as response:
   result.update(status='READY',health=json.load(response));break
 except Exception:time.sleep(.5)
else:result['status']='STARTUP_NOT_READY'
(base/'runtime-start.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
