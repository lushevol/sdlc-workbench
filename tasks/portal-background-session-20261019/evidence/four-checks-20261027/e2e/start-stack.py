from pathlib import Path
import subprocess,os,json,datetime
root=Path.cwd();runtime=root/'.workbench/four-checks-e2e-20261027';out=root/'tasks/portal-background-session-20261019/evidence/four-checks-20261027/e2e';source=root/'.workbench/ut-final-cancellation-20261027/source';rootrepo=root/'repos/ui/mfe-root-config';old=root/'.workbench/portal-session-real-20261019/local-bff';fast=root/'.workbench/session-active-cutoff-fix-20261024/bff-fast'
env=os.environ.copy();env.update({'NPM_CONFIG_UPDATE_NOTIFIER':'false','mode':'development','orgName':'fm','devtool':'source-map','isLocal':'true','publicUrl':'','importmap':'/importmaplocal.json'})
cp=str(fast/'classes')+':'+str(old/'classes')+':'+(old/'classpath.txt').read_text().strip()
commands=[('bff-fast',fast,['/opt/homebrew/opt/openjdk@17/bin/java','-Djava.net.useSystemProxies=false','-cp',cp,'local.portalsession.LocalSessionApplication','--server.port=8091'],None),('mfe',source,['node',str(source/'node_modules/webpack/bin/webpack.js'),'serve','--config',str(runtime/'mfe.webpack.cjs')],8142),('root-fast',rootrepo,['node',str(rootrepo/'node_modules/webpack/bin/webpack.js'),'serve','--config',str(runtime/'root-fast.webpack.cjs')],8143),('root-natural',rootrepo,['node',str(rootrepo/'node_modules/webpack/bin/webpack.js'),'serve','--config',str(runtime/'root-natural.webpack.cjs')],8141)]
records=[]
for name,cwd,cmd,port in commands:
 if port:env['port']=str(port)
 with (out/(name+'-authorized.log')).open('w') as stream:p=subprocess.Popen(cmd,cwd=cwd,env=env,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
 records.append({'name':name,'cwd':str(cwd),'argv':cmd,'pid':p.pid,'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owned':True})
(out/'started-processes-authorized.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps([{'name':r['name'],'pid':r['pid']} for r in records]))
