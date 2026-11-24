from pathlib import Path
from xml.etree import ElementTree as ET
import datetime,hashlib,json,shutil,subprocess,sys
root=Path(__file__).resolve().parents[2];base=Path(__file__).resolve().parent
repo=root/'repos/services/single-ui-bff'
revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
report=repo/'verification/target/surefire-reports/TEST-com.scb.sso.singleuibff.controller.v2.JwtAuthenticationControllerTest.xml'
props={p.get('name'):p.get('value') for p in ET.parse(report).findall('.//property')}
jars=[Path(p) for p in props['java.class.path'].split(':') if p.endswith('.jar')]
replace={'spring-core':'6.1.14','spring-web':'6.1.14','spring-webmvc':'6.1.14','spring-context':'6.1.14','tomcat-embed-core':'10.1.39'}
selected=[]
for p in jars:
 matched=next((name for name in replace if p.name.startswith(name+'-') and p.name[len(name)+1].isdigit()),None)
 if matched:p=p.parent.parent/replace[matched]/(matched+'-'+replace[matched]+'.jar')
 if not p.is_file():raise SystemExit('Missing cached jar: '+p.name)
 selected.append(p)
h2=Path.home()/'.m2/repository/com/h2database/h2/2.4.240/h2-2.4.240.jar';assert h2.is_file();selected.append(h2)
source=base/'source';source.mkdir(exist_ok=True)
manifest=[]
paths=subprocess.check_output(['git','ls-files','src/main/java'],cwd=repo,text=True).splitlines()
for relative in paths:
 p=repo/relative;data=p.read_bytes();exact=subprocess.check_output(['git','show',revision+':'+relative],cwd=repo)
 if data!=exact:raise SystemExit('Worktree differs from exact source: '+relative)
 target=source/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 manifest.append({'path':relative,'sha256':hashlib.sha256(data).hexdigest(),'size_bytes':len(data)})
classes=base/'classes';classes.mkdir(exist_ok=True)
cp=':'.join(map(str,selected));(base/'classpath.txt').write_text(cp)
sources=list(source.rglob('*.java'))+list((base/'runner').rglob('*.java'))
(base/'javac-inputs.txt').write_text('\n'.join(map(str,sources))+'\n')
command=['/opt/homebrew/opt/openjdk@17/bin/javac','--release','17','-encoding','UTF-8','-cp',cp,'-d',str(classes),'@'+str(base/'javac-inputs.txt')]
started=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(command,capture_output=True,text=True)
(base/'build.stdout.txt').write_text(p.stdout);(base/'build.stderr.txt').write_text(p.stderr)
result={'started_at':started,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_revision':revision,'source_count':len(manifest),'source_files':manifest,'runner_sha256':hashlib.sha256(next((base/'runner').rglob('*.java')).read_bytes()).hexdigest(),'dependencies':[{'name':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in selected],'dependency_scope':'Cached public verification dependencies with root-POM Spring/Tomcat overrides; H2 substituted for PostgreSQL; private starters absent','production_runtime_equivalence':'NOT_ESTABLISHED','source_resources':'Not copied; no remote configuration loaded','exit_code':p.returncode,'stderr_sha256':hashlib.sha256(p.stderr.encode()).hexdigest()}
(base/'source-build-manifest.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'exit_code':p.returncode,'source_revision':revision,'source_count':len(manifest),'dependency_count':len(selected),'stderr':p.stderr[-6500:]},indent=2));sys.exit(p.returncode)
