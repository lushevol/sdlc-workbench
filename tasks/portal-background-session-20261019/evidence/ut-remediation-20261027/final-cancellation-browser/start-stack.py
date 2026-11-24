from pathlib import Path
import os,subprocess,json,datetime
root=Path.cwd(); evidence=root/'tasks/portal-background-session-20261019/evidence/ut-remediation-20261027/final-cancellation-browser'; runtime=root/'.workbench/ut-final-cancellation-20261027'
env=os.environ.copy();env.update({'NPM_CONFIG_UPDATE_NOTIFIER':'false','mode':'development','orgName':'fm','devtool':'source-map','isLocal':'true','publicUrl':'','importmap':'/importmaplocal.json'})
records=[]
for name,cwd,config,port in [('mfe',runtime/'source',runtime/'mfe.local.webpack.cjs',8142),('root',root/'repos/ui/mfe-root-config',runtime/'root.webpack.cjs',8143)]:
 env['port']=str(port);cmd=['node',str(cwd/'node_modules/webpack/bin/webpack.js'),'serve','--config',str(config)]
 with (evidence/(name+'.log')).open('w') as stream:
  p=subprocess.Popen(cmd,cwd=cwd,env=env,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
 records.append({'name':name,'pid':p.pid,'cwd':str(cwd),'argv':cmd,'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat()})
(evidence/'started-processes.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps({'started':[{'name':r['name'],'pid':r['pid']} for r in records]}))
