from pathlib import Path
import subprocess,sys,os,json,datetime
base=Path(__file__).resolve().parent; root=base.parents[1]; prev=root/'.workbench/session-minor-rerun-20261020'; name=sys.argv[1]; env=os.environ.copy()
env.update({'NPM_CONFIG_UPDATE_NOTIFIER':'false','mode':'development','orgName':'fm','devtool':'source-map','isLocal':'true','publicUrl':'','importmap':'/importmaplocal.json','NODE_PATH':str(prev/'mfe/node_modules')})
folder=base/name
if name=='mfe':
 env['port']='8122';cwd=prev/'mfe/source';cmd=['node',str(prev/'mfe/node_modules/webpack/bin/webpack.js'),'serve','--config',str(folder/'webpack.cjs')]
elif name.startswith('root'):
 env['port']='8126' if name=='root-three-minute' else '8121';cwd=root/'repos/ui/mfe-root-config';cmd=['node',str(cwd/'node_modules/webpack/bin/webpack.js'),'serve','--config',str(folder/'webpack.cjs')]
elif name.startswith('bff'):
 old=root/'.workbench/portal-session-real-20261019/local-bff'; fast=root/'.workbench/session-post-change-20261020/bff-fast'; cwd=folder;cp=(str(folder/'classes')+':' if name=='bff-three-minute' else '')+str(fast/'classes')+':'+str(old/'classes')+':'+(old/'classpath.txt').read_text().strip();cmd=['/opt/homebrew/opt/openjdk@17/bin/java','-Djava.net.useSystemProxies=false','-cp',cp,'local.portalsession.LocalSessionApplication','--server.port='+('8127' if name=='bff-three-minute' else '8123')]
else:raise SystemExit(name)
record={'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'cwd':str(cwd),'status':'RUNNING','startup_downloads':False}
with (folder/'runtime.log').open('w') as log:
 process=subprocess.Popen(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT);record['pid']=process.pid;(folder/'runtime.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'service':name,'pid':process.pid}),flush=True);code=process.wait()
record.update({'status':'STOPPED','exit_code':code,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat()});(folder/'runtime.json').write_text(json.dumps(record,indent=2)+'\n');raise SystemExit(code)
