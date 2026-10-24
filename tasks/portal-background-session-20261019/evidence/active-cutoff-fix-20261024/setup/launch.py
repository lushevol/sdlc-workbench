from pathlib import Path
import subprocess,sys,os,json,datetime
base=Path(__file__).resolve().parent;root=base.parents[1];name=sys.argv[1];env=os.environ.copy()
env.update({'NPM_CONFIG_UPDATE_NOTIFIER':'false','mode':'development','orgName':'fm','devtool':'source-map','isLocal':'true','publicUrl':'','importmap':'/importmaplocal.json'})
folder=base/name
if name=='mfe':
 env['port']='8102';cwd=folder/'source';cmd=['node',str(folder/'node_modules/webpack/bin/webpack.js'),'serve','--config',str(folder/'mfe.local.webpack.cjs')]
elif name.startswith('root-'):
 env['port']='8101' if name=='root-natural' else '8103';cwd=root/'repos/ui/mfe-root-config';cmd=['node',str(cwd/'node_modules/webpack/bin/webpack.js'),'serve','--config',str(folder/'root.webpack.cjs')]
elif name=='bff-fast':
 old=root/'.workbench/portal-session-real-20261019/local-bff';cwd=folder;cp=str(folder/'classes')+':'+str(old/'classes')+':'+(old/'classpath.txt').read_text().strip();cmd=['/opt/homebrew/opt/openjdk@17/bin/java','-Djava.net.useSystemProxies=false','-cp',cp,'local.portalsession.LocalSessionApplication','--server.port=8091']
else:raise SystemExit(name)
record={'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'cwd':str(cwd),'environment_overrides':{k:env[k] for k in ['mode','orgName','devtool','isLocal','publicUrl','importmap']},'status':'RUNNING','startup_downloads':False}
with (folder/'runtime.log').open('w') as log:
 process=subprocess.Popen(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT);record['pid']=process.pid;(folder/'runtime.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'service':name,'pid':process.pid}),flush=True);code=process.wait()
record.update({'status':'STOPPED','exit_code':code,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat()});(folder/'runtime.json').write_text(json.dumps(record,indent=2)+'\n');raise SystemExit(code)
