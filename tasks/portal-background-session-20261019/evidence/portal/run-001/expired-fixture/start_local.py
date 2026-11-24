from pathlib import Path
import datetime,json,os,subprocess,time,urllib.request
base=Path(__file__).resolve().parent
cp=str(base/'classes')+':'+(base/'classpath.txt').read_text()
command=['/opt/homebrew/opt/openjdk@17/bin/java','-Djava.net.useSystemProxies=false','-cp',cp,'local.portalsession.LocalSessionApplication']
env={'PATH':'/opt/homebrew/opt/openjdk@17/bin:/usr/bin:/bin','JAVA_HOME':'/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home','LANG':'en_US.UTF-8'}
with (base/'runtime.stdout.log').open('ab') as out,(base/'runtime.stderr.log').open('ab') as err:
 process=subprocess.Popen(command,cwd=base,env=env,stdin=subprocess.DEVNULL,stdout=out,stderr=err,start_new_session=True)
result={'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':process.pid,'listen':'127.0.0.1:8089','context_path':'/api/auth','source_revision':'85d7cc03eb12710d6facf581987fd4ae24fc9844','clock':'REAL_WALL_CLOCK','effective_timeouts':{'access_minutes':15,'refresh_minutes':225,'refresh_extra_seconds':24,'absolute_minutes':60},'substitutes':['synthetic OUD identity','fixed empty application catalog','fixed local EMS2 entitlements','no-op analytics','isolated H2 memory database instead of PostgreSQL','isolated Spring bootstrap without private starters'],'real_paths':['JwtAuthenticationController','JwtTokenUtil RSA generation and verification','SessionServiceImplementation','ApplicationSessionRepo with real JPA/H2'],'private_keys':'generated only in process memory','log_policy':'request route/timing/status and issued-token hashes/claims; no raw tokens or private keys'}
for i in range(50):
 if process.poll() is not None:result.update(status='EXITED',exit_code=process.returncode);break
 try:
  with urllib.request.urlopen('http://127.0.0.1:8089/api/auth/local/health',timeout=1) as response:
   result.update(status='READY',health=json.load(response));break
 except Exception:time.sleep(.5)
else:result['status']='STARTUP_NOT_READY'
(base/'runtime-start.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
