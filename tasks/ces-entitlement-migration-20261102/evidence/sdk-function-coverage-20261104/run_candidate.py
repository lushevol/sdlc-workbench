"""Run the exact candidate offline in an isolated export. No source edits or network calls."""
from pathlib import Path
import datetime, hashlib, io, json, os, shutil, subprocess, sys, tarfile, tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[4]
EVIDENCE = Path(__file__).resolve().parent
REPO = ROOT / 'repos/libraries/single-ui-sdk-starter'
HEAD = 'fd9a157e260850b6d9efa10da3223950ea61133a'
BASE = 'b0aa82005e7f14202f85f5ef583f25e42da9eeb3'
MODULE_TESTS = '--module-test-goals' in sys.argv
QUALIFIED = '--qualified-test-goals' in sys.argv or MODULE_TESTS
TEST_GOALS = '--test-goals' in sys.argv or QUALIFIED
RUN = EVIDENCE / ('candidate-module-test-run' if MODULE_TESTS else 'candidate-qualified-test-run' if QUALIFIED else 'candidate-test-run' if TEST_GOALS else 'candidate-run')
RUN.mkdir(exist_ok=False)
TEMP = Path(tempfile.mkdtemp(prefix='sdk-coverage-20261104-', dir='/private/tmp'))
SOURCE = TEMP / 'source'
SOURCE.mkdir()
archive = subprocess.check_output(['git', '-C', str(REPO), 'archive', HEAD])
with tarfile.open(fileobj=io.BytesIO(archive)) as tree:
    tree.extractall(SOURCE, filter='data')
files = [{'path': str(p.relative_to(SOURCE)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(SOURCE.rglob('*')) if p.is_file()]
for row in files:
    exact = subprocess.check_output(['git', '-C', str(REPO), 'show', HEAD + ':' + row['path']])
    assert hashlib.sha256(exact).hexdigest() == row['sha256']
settings = TEMP / 'settings.xml'
settings.write_text('<settings xmlns="http://maven.apache.org/SETTINGS/1.2.0"/>\n')
cache = TEMP / 'repository'
subprocess.run(['/bin/cp', '-cR', str(Path.home() / '.m2/repository'), str(cache)], check=True)
reports = RUN / 'surefire-reports'
reports.mkdir()
target = SOURCE / 'single-ui-sdk-starter/target'
target.mkdir()
(target / 'surefire-reports').symlink_to(reports, target_is_directory=True)
command = ['/opt/homebrew/bin/mvn', '-B', '-o', '-s', str(settings), '-Dmaven.repo.local=' + str(cache), '-Dformatter.skip=true']
if MODULE_TESTS:
    command += ['-pl', 'single-ui-sdk-starter']
if QUALIFIED:
    command += ['org.apache.maven.plugins:maven-resources-plugin:3.3.1:resources', 'org.apache.maven.plugins:maven-compiler-plugin:3.8.0:compile', 'org.apache.maven.plugins:maven-resources-plugin:3.3.1:testResources', 'org.apache.maven.plugins:maven-compiler-plugin:3.8.0:testCompile', 'org.apache.maven.plugins:maven-surefire-plugin:3.5.5:test']
else:
    command += (['resources:resources', 'compiler:compile', 'resources:testResources', 'compiler:testCompile', 'surefire:test'] if TEST_GOALS else ['verify'])
inputs = {'head': HEAD, 'base': BASE, 'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'source_directory': str(SOURCE), 'command': command, 'JAVA_HOME': '/opt/homebrew/opt/openjdk@17', 'files': files, 'mode': 'all compilation and test goals; packaging plugins not invoked' if TEST_GOALS else 'complete verify lifecycle', 'network': 'offline; existing local Maven cache copied into temporary storage', 'limits': ['Mock CES and local fixtures only; no live CES, FMAA, or deployed consumer.', 'Full declared reactor; formatter disabled to preserve source bytes.']}
(RUN / 'inputs.json').write_text(json.dumps(inputs, indent=2) + '\n')
env = dict(os.environ, JAVA_HOME='/opt/homebrew/opt/openjdk@17')
with (RUN / 'maven.log').open('w') as output:
    try:
        result = subprocess.run(command, cwd=SOURCE, env=env, stdout=output, stderr=subprocess.STDOUT, timeout=180)
        code = result.returncode
    except subprocess.TimeoutExpired:
        code = 124
cases = []
counts = dict(tests=0, failures=0, errors=0, skipped=0)
for p in sorted(reports.glob('TEST-*.xml')):
    suite = ET.parse(p).getroot()
    for key in counts:
        counts[key] += int(suite.get(key, '0'))
    for case in suite.findall('testcase'):
        status = next((tag.upper() for tag in ['failure', 'error', 'skipped'] if case.find(tag) is not None), 'PASSED')
        cases.append({'class': case.get('classname'), 'method': case.get('name'), 'result': status, 'evidence': str(p.relative_to(EVIDENCE))})
changed = [r['path'] for r in files if hashlib.sha256((SOURCE / r['path']).read_bytes()).hexdigest() != r['sha256']]
summary = {'head': HEAD, 'base': BASE, 'finished_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'exit_code': code, 'counts': counts, 'cases': cases, 'source_changes': changed, 'log_sha256': hashlib.sha256((RUN / 'maven.log').read_bytes()).hexdigest(), 'status': 'PASSED_CONTROLLED_SCOPE' if code == 0 and counts['tests'] > 0 and sum(counts[x] for x in ['failures', 'errors', 'skipped']) == 0 and not changed else 'INCOMPLETE_OR_FAILED', 'limits': inputs['limits']}
(RUN / 'result.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({k: summary[k] for k in ['status', 'exit_code', 'counts', 'source_changes']}, indent=2))
print('Isolated source: ' + str(SOURCE))
