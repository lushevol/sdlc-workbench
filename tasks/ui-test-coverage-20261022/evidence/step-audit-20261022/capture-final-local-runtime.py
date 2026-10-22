"""Retain a fresh final isolated BFF runtime snapshot without modifying business state."""
from pathlib import Path
from urllib import request
import datetime
import gzip
import hashlib
import json
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[3]
BASE = WORKSPACE / '.workbench/current-bff-audit'
TARGET = ROOT / 'current-bff-build/final-runtime'
TARGET.mkdir(parents=True, exist_ok=False)


def digest(data):
    return hashlib.sha256(data).hexdigest()


copied = []
for name in ['build_local.py', 'start_local.py', 'build.stdout.txt', 'build.stderr.txt',
             'source-build-manifest.json', 'migration-manifest.json', 'migration-execution.json',
             'runtime-start.json', 'postgres-initialize.sql']:
    source = BASE / name
    shutil.copyfile(source, TARGET / name)
    copied.append({'path': name, 'sha256': digest(source.read_bytes()), 'bytes': source.stat().st_size})
source = BASE / 'runner/local/portalsession/LocalSessionApplication.java'
shutil.copyfile(source, TARGET / source.name)
copied.append({'path': source.name, 'sha256': digest(source.read_bytes()), 'bytes': source.stat().st_size})
for name in ['runtime.stdout.log', 'runtime.stderr.log', 'postgres.log']:
    data = (BASE / name).read_bytes()
    (TARGET / (name + '.gz')).write_bytes(gzip.compress(data, mtime=0))
    copied.append({'path': name + '.gz', 'uncompressedSha256': digest(data), 'uncompressedBytes': len(data),
                   'sha256': digest((TARGET / (name + '.gz')).read_bytes())})
classes = [{'path': str(p.relative_to(BASE / 'classes')), 'sha256': digest(p.read_bytes()), 'bytes': p.stat().st_size}
           for p in sorted((BASE / 'classes').rglob('*')) if p.is_file()]
classpath = (BASE / 'classpath.txt').read_text().strip().split(':')
libraries = [{'name': Path(raw).name, 'sha256': digest(Path(raw).read_bytes()), 'bytes': Path(raw).stat().st_size}
             for raw in classpath if Path(raw).is_file()]
with request.urlopen('http://127.0.0.1:8090/api/auth/local/health', timeout=5) as response:
    health = {'status': response.status, 'body': json.load(response)}
commands = [
    ['lsof', '-nP', '-iTCP:8090', '-sTCP:LISTEN'],
    ['lsof', '-nP', '-iTCP:54390', '-sTCP:LISTEN'],
    ['/opt/homebrew/bin/pg_ctl', '-D', str(BASE / 'pg-data'), 'status'],
]
process_checks = []
for command in commands:
    result = subprocess.run(command, text=True, capture_output=True)
    process_checks.append({'command': command, 'exitCode': result.returncode,
                           'stdout': result.stdout, 'stderr': result.stderr})
result = {
    'recordedAt': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'sourceRevision': '834b4155232222347220e47139a502ee43a9cbdf',
    'status': 'PASSED' if health['body'].get('status') == 'UP' and all(p['exitCode'] == 0 for p in process_checks) else 'FAILED',
    'health': health, 'processChecks': process_checks, 'files': copied,
    'compiledClassCount': len(classes), 'compiledClasses': classes,
    'classpathLibraryCount': len(libraries), 'classpathLibraries': libraries,
    'limits': ['Local synthetic identities, controlled EMS2, and analytics boundary.',
               'Exact business source and migrations use isolated Spring Boot3 configuration.',
               'Production Boot4 and private starter configuration remain unverified.',
               'Snapshot is read-only provenance. Individual case evidence establishes asserted outcomes.'],
}
(TARGET / 'manifest.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ['recordedAt', 'status', 'compiledClassCount', 'classpathLibraryCount']}, indent=2))
