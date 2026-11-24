from pathlib import Path
import os, re, subprocess, sys, json, datetime
root=Path.cwd();base=root/'.workbench/session-active-cutoff-fix-20261024'
source=(root/'.workbench/session-post-change-20261020/bff-fast/runner/local/portalsession/LocalSessionApplication.java').read_text()
env=os.environ.copy()
for field,key in [('USER','SESSION_E2E_USERNAME'),('PASSWORD','SESSION_E2E_PASSWORD')]:
 env[key]=re.search(r'public static final String '+field+r'="([^"]+)"',source).group(1)
modes=sys.argv[1:] or ['cross']
if modes != ['cross']: raise SystemExit('Only the original cross counterfactual is configured.')
for mode in modes:
 identity='baseline-'+mode+'-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S')
 profile='baseline-fast'
 print(json.dumps({'starting':mode,'id':identity,'profile':profile}),flush=True)
 log=base/(identity+'.log')
 with log.open('w') as out:
  run=subprocess.run(['node',str(base/'browser-runner.mjs'),mode,profile,identity],env=env,stdout=out,stderr=subprocess.STDOUT)
 evidence=base/'native'/identity/'run.json'
 record=json.loads(evidence.read_text()) if evidence.exists() else {}
 # Retain each completed case before another native browser starts.
 subprocess.run([
  sys.executable,
  str(root/'tasks/portal-background-session-20261019/evidence/active-cutoff-fix-20261024/compare-results.py'),
  '--record-mode',mode,'--run',str(evidence),
  '--evidence-root',str(root/'tasks/portal-background-session-20261019/evidence/active-cutoff-fix-20261024/counterfactual'),
 ],check=True)
 print(json.dumps({'finished':mode,'status':record.get('status'),'exit_code':run.returncode,'error':record.get('error'),'evidence':str(evidence)}),flush=True)
