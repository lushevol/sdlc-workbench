from pathlib import Path
import subprocess, os, json, hashlib, datetime, tarfile, io
root=Path.cwd(); out=root/'tasks/portal-background-session-20261019/evidence/review-e2e-20261028'; runtime=root/'.workbench/review-e2e-20261028'; runtime.mkdir(parents=True,exist_ok=False)
repo=root/'repos/ui/mfe-base'; rootrepo=root/'repos/ui/mfe-root-config'
sha=lambda b:hashlib.sha256(b).hexdigest()
binding={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline':'f025513f696476a9cc8162681410cbd21e029bcb','candidate':'e0030f5cf920b715f5831faf7df86cb9789b6d0f','source':{},'limits':['Local webpack development build; toolkit substitute; local authentication fixture; no production parity.','Preserve current source checkout including unrelated Home changes.']}
mfe_template=(root/'.workbench/four-checks-e2e-20261027/mfe.webpack.cjs').read_text(); root_template=(root/'.workbench/four-checks-e2e-20261027/root-fast.webpack.cjs').read_text()
for label,port in [('candidate',8142),('baseline',8152)]:
 folder=runtime/label; source=folder/'source';source.mkdir(parents=True)
 archive=subprocess.check_output(['git','-C',str(repo),'archive',binding[label]])
 with tarfile.open(fileobj=io.BytesIO(archive)) as t:t.extractall(source,filter='data')
 (source/'node_modules').symlink_to(repo/'node_modules',target_is_directory=True)
 config=mfe_template.replace(str(root/'.workbench/ut-final-cancellation-20261027/source'),str(source)).replace('port: 8142',f'port: {port}')
 (folder/'mfe.webpack.cjs').write_text(config)
 (folder/'root.webpack.cjs').write_text(root_template.replace('8143',str(port+1)).replace('8142',str(port)))
 binding['source'][label]={'revision':binding[label],'path':str(source.relative_to(root)),'hashes':{str(p.relative_to(source)):sha(p.read_bytes()) for p in sorted((source/'src').rglob('*')) if p.is_file()},'config':{'mfe':sha(config.encode()),'root':sha((folder/'root.webpack.cjs').read_bytes())}}
for p in runtime.glob('*/*.cjs'):(out/(p.parent.name+'-'+p.name)).write_bytes(p.read_bytes())
binding['root_revision']=subprocess.check_output(['git','-C',str(rootrepo),'rev-parse','HEAD'],text=True).strip()
binding['root_status']=subprocess.check_output(['git','-C',str(rootrepo),'status','--short'],text=True).strip()
binding['bff_revision']='85d7cc03eb12710d6facf581987fd4ae24fc9844'
binding['toolkit_hashes']={str(p.relative_to(root)):sha(p.read_bytes()) for p in (root/'.workbench/portal-session-real-20261019/local-mfe/toolkit-mock').rglob('*') if p.is_file()}
(out/'source-binding.json').write_text(json.dumps(binding,indent=2)+'\n')
env=os.environ.copy();env.update({'NPM_CONFIG_UPDATE_NOTIFIER':'false','mode':'development','orgName':'fm','devtool':'source-map','isLocal':'true','publicUrl':'','importmap':'/importmaplocal.json'})
old=root/'.workbench/portal-session-real-20261019/local-bff';fast=root/'.workbench/session-active-cutoff-fix-20261024/bff-fast'; cp=str(fast/'classes')+':'+str(old/'classes')+':'+(old/'classpath.txt').read_text().strip()
commands=[('bff',fast,['/opt/homebrew/opt/openjdk@17/bin/java','-Djava.net.useSystemProxies=false','-cp',cp,'local.portalsession.LocalSessionApplication','--server.port=8091'],None)]
for label,port in [('candidate',8142),('baseline',8152)]:
 folder=runtime/label;source=folder/'source'
 commands.extend([(label+'-mfe',source,['node',str(source/'node_modules/webpack/bin/webpack.js'),'serve','--config',str(folder/'mfe.webpack.cjs')],port),(label+'-root',rootrepo,['node',str(rootrepo/'node_modules/webpack/bin/webpack.js'),'serve','--config',str(folder/'root.webpack.cjs')],port+1)])
records=[]
for name,cwd,cmd,port in commands:
 if port:env['port']=str(port)
 with (out/(name+'.log')).open('w') as stream:p=subprocess.Popen(cmd,cwd=cwd,env=env,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
 records.append({'name':name,'cwd':str(cwd),'argv':cmd,'pid':p.pid,'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owned':True})
(out/'processes.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps([{'name':r['name'],'pid':r['pid']} for r in records]))
