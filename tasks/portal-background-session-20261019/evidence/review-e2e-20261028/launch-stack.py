from pathlib import Path
import subprocess,os,json,datetime
root=Path.cwd();out=root/'tasks/portal-background-session-20261019/evidence/review-e2e-20261028'
previous=json.loads((out/'processes.json').read_text());env=os.environ.copy();env.update({'NPM_CONFIG_UPDATE_NOTIFIER':'false','mode':'development','orgName':'fm','devtool':'source-map','isLocal':'true','publicUrl':'','importmap':'/importmaplocal.json'})
records=[]
for r in previous:
 port={'candidate-mfe':8142,'candidate-root':8143,'baseline-mfe':8152,'baseline-root':8153}.get(r['name'])
 if port:env['port']=str(port)
 with (out/(r['name']+'-attempt2.log')).open('w') as f:p=subprocess.Popen(r['argv'],cwd=r['cwd'],env=env,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
 records.append({**r,'pid':p.pid,'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat()})
(out/'processes-attempt2.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps([{'name':r['name'],'pid':r['pid']} for r in records]))
