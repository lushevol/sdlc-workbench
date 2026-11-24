"""Run the existing isolated portal composition at new loopback-only ports."""
from pathlib import Path
import datetime, hashlib, io, json, os, subprocess, tarfile

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
binding = json.loads((OUT / 'execution-source-binding.json').read_text())
runtime = Path(binding['runtime'])
source = Path(binding['source'])
rootrepo = ROOT / 'repos/ui/mfe-root-config'
root_revision = subprocess.check_output(['git', '-C', str(rootrepo), 'rev-parse', 'HEAD'], text=True).strip()
root_source = runtime / 'root-source'
if not root_source.exists():
    root_source.mkdir()
    with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git', '-C', str(rootrepo), 'archive', root_revision]))) as stream:
        stream.extractall(root_source, filter='data')
    (root_source / 'node_modules').symlink_to(rootrepo / 'node_modules', target_is_directory=True)
mfe_config = (ROOT / '.workbench/four-checks-e2e-20261027/mfe.webpack.cjs').read_text().replace(str(ROOT / '.workbench/ut-final-cancellation-20261027/source'), str(source)).replace('8142', '8342').replace("require('webpack')", "require(" + json.dumps(str(source / 'node_modules/webpack')) + ")")
root_config = (ROOT / '.workbench/four-checks-e2e-20261027/root-fast.webpack.cjs').read_text().replace(str(rootrepo), str(root_source)).replace('8142', '8342').replace('8143', '8343').replace('8091', '8291')
(OUT / 'mfe.webpack.cjs').write_text(mfe_config)
(OUT / 'root.webpack.cjs').write_text(root_config)
old = ROOT / '.workbench/portal-session-real-20261019/local-bff'
fast = ROOT / '.workbench/session-active-cutoff-fix-20261024/bff-fast'
cp = str(fast / 'classes') + ':' + str(old / 'classes') + ':' + (old / 'classpath.txt').read_text().strip()
env = os.environ.copy()
env.update({'NPM_CONFIG_UPDATE_NOTIFIER': 'false', 'mode': 'development', 'orgName': 'fm', 'devtool': 'source-map', 'isLocal': 'true', 'publicUrl': '', 'importmap': '/importmaplocal.json'})
commands = [
    ('bff', fast, ['/opt/homebrew/opt/openjdk@17/bin/java', '-Djava.net.useSystemProxies=false', '-cp', cp, 'local.portalsession.LocalSessionApplication', '--server.port=8291', '--server.address=127.0.0.1'], None),
    ('mfe', source, ['node', str(source / 'node_modules/webpack/bin/webpack.js'), 'serve', '--config', str(OUT / 'mfe.webpack.cjs')], '8342'),
    ('root', root_source, ['node', str(root_source / 'node_modules/webpack/bin/webpack.js'), 'serve', '--config', str(OUT / 'root.webpack.cjs')], '8343')
]
records = []
for name, cwd, cmd, port in commands:
    current = env.copy()
    if port:
        current['port'] = port
    with (runtime / (name + '.log')).open('w') as log:
        process = subprocess.Popen(cmd, cwd=cwd, env=current, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    records.append({'name': name, 'pid': process.pid, 'owned': True, 'argv': cmd, 'cwd': str(cwd), 'log': str(runtime / (name + '.log'))})
binding['root_revision'] = root_revision
binding['root_source'] = str(root_source)
binding['ports'] = {'bff': 8291, 'mfe': 8342, 'root': 8343}
binding['bff_class_sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for base in [fast / 'classes', old / 'classes'] for p in sorted(base.rglob('*.class'))}
(OUT / 'execution-source-binding.json').write_text(json.dumps(binding, indent=2) + '\n')
(OUT / 'local-processes.json').write_text(json.dumps(records, indent=2) + '\n')
print(json.dumps([{'name': r['name'], 'pid': r['pid']} for r in records]))
