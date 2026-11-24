"""Probe baseline and candidate dependency overrides using the cached Boot-managed closure."""
from pathlib import Path
import subprocess, tempfile, json, hashlib, datetime
ROOT=Path(__file__).resolve().parents[3]
REPO=ROOT/'repos/services/single-ui-bff'
CACHE=Path.home()/'.m2/repository'
JDK=Path('/opt/homebrew/opt/openjdk@17/bin')
OUT=Path(__file__).with_name('bff-dependencies.json')

def jar(path,version,name=None):
    return CACHE/path/version/f'{name or path.rsplit("/",1)[1]}-{version}.jar'

def hashfile(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def execute(name,source,basejars,candidatejars):
    record={'case':name,'source':source,'runs':[]}
    with tempfile.TemporaryDirectory(prefix='bff-dependencies-') as tmp:
        tmp=Path(tmp); f=tmp/'Probe.java';f.write_text(source)
        compile=subprocess.run([str(JDK/'javac'),'--release','17','-cp',':'.join(map(str,basejars)),'-d',str(tmp),str(f)],capture_output=True,text=True)
        record['compilation']={'exit':compile.returncode,'output':compile.stdout+compile.stderr}
        if compile.returncode: return record
        for side,jars in [('baseline',basejars),('candidate',candidatejars)]:
            result=subprocess.run([str(JDK/'java'),'-cp',str(tmp)+':'+':'.join(map(str,jars)),'Probe'],capture_output=True,text=True,timeout=30)
            record['runs'].append({'side':side,'exit':result.returncode,'output':result.stdout+result.stderr,'dependencies':[{'path':str(p),'sha256':hashfile(p)} for p in jars]})
    return record

jackson=lambda v:[jar('com/fasterxml/jackson/core/jackson-databind',v),jar('com/fasterxml/jackson/core/jackson-core','2.17.2'),jar('com/fasterxml/jackson/core/jackson-annotations','2.17.2')]
validator=lambda v:[jar('org/hibernate/validator/hibernate-validator',v),jar('jakarta/validation/jakarta.validation-api','3.0.2'),jar('org/jboss/logging/jboss-logging','3.5.3.Final'),jar('com/fasterxml/classmate','1.7.0')]
result={'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'repository':str(REPO),'base':subprocess.check_output(['git','rev-parse','main'],cwd=REPO,text=True).strip(),'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),'pom_sha256':hashfile(REPO/'pom.xml'),'boot_dependency_bom':{'path':str(CACHE/'org/springframework/boot/spring-boot-dependencies/3.3.4/spring-boot-dependencies-3.3.4.pom'),'sha256':hashfile(CACHE/'org/springframework/boot/spring-boot-dependencies/3.3.4/spring-boot-dependencies-3.3.4.pom')},'jdk':subprocess.check_output([str(JDK/'java'),'-version'],stderr=subprocess.STDOUT,text=True),'cases':[],'limits':['Standalone dependency integration probes. Actual BFF service and corporate starter are not started.','Baseline uses Spring Boot 3.3.4 managed versions. Candidate overrides only the two direct dependencies in the committed POM.','Validator comparison substitutes cached 8.0.2.Final for the Boot-managed 8.0.1.Final baseline. Jackson baseline is exact.', 'Real cached dependency bytes; no fabricated classes, downloads, live calls, or credentials. Java 17 executes release-17 probe bytecode.']}
for args in [('jackson-read', 'import com.fasterxml.jackson.databind.ObjectMapper; import java.util.Map; public class Probe { public static void main(String[] args) throws Exception { Object value=new ObjectMapper().readValue("{}", Map.class); if (!value.toString().equals("{}")) throw new AssertionError(value); System.out.println("JSON_READ_OK "+value); }}',jackson('2.17.2'),jackson('2.21.8')),('validator-start', 'import jakarta.validation.Validation; import org.hibernate.validator.messageinterpolation.ParameterMessageInterpolator; public class Probe { public static void main(String[] args) { try (var factory=Validation.byDefaultProvider().configure().messageInterpolator(new ParameterMessageInterpolator()).buildValidatorFactory()) { if (factory.getValidator()==null) throw new AssertionError(); System.out.println("VALIDATOR_START_OK"); } }}',validator('8.0.2.Final'),validator('9.0.2.Final'))]:
    case=execute(*args)
    signature='JsonSerializeAs' if case['case']=='jackson-read' else 'getMessageLogger'
    case['assertions']={'baseline_exit_zero':len(case['runs'])==2 and case['runs'][0]['exit']==0,'candidate_exit_nonzero':len(case['runs'])==2 and case['runs'][1]['exit']!=0,'candidate_contains_expected_linkage_error':len(case['runs'])==2 and signature in case['runs'][1]['output']}
    case['status']='CONFIRMED' if all(case['assertions'].values()) else 'NOT_CONFIRMED'
    result['cases'].append(case)
    result['finished_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    OUT.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps([{'case':c['case'],'compilation':c['compilation'],'runs':[{'side':r['side'],'exit':r['exit'],'output':r['output']} for r in c['runs']]} for c in result['cases']],indent=2))
