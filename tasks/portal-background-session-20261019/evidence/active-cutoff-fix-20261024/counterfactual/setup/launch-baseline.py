from pathlib import Path
import datetime
import json
import os
import subprocess
import sys

base = Path(__file__).resolve().parent
root = base.parents[1]
name = sys.argv[1]
env = os.environ.copy()
env.update({'NPM_CONFIG_UPDATE_NOTIFIER': 'false', 'mode': 'development',
            'orgName': 'fm', 'devtool': 'source-map', 'isLocal': 'true',
            'publicUrl': '', 'importmap': '/importmaplocal.json'})
if name == 'mfe':
    folder = base / 'baseline-mfe'
    cwd = folder / 'source'
    env['port'] = '8112'
    cmd = ['node', str(folder / 'node_modules/webpack/bin/webpack.js'),
           'serve', '--config', str(folder / 'mfe.local.webpack.cjs')]
elif name == 'root-fast':
    folder = base / 'baseline-root-fast'
    cwd = root / 'repos/ui/mfe-root-config'
    env['port'] = '8113'
    cmd = ['node', str(cwd / 'node_modules/webpack/bin/webpack.js'),
           'serve', '--config', str(folder / 'root.webpack.cjs')]
else:
    raise SystemExit(name)
record = {'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'command': cmd, 'cwd': str(cwd), 'status': 'RUNNING',
          'environment_overrides': {k: env[k] for k in
              ['port', 'mode', 'orgName', 'devtool', 'isLocal', 'publicUrl', 'importmap']},
          'startup_downloads': False}
with (folder / 'runtime.log').open('w') as log:
    process = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT)
    record['pid'] = process.pid
    (folder / 'runtime.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'service': 'baseline-' + name, 'pid': process.pid}), flush=True)
    code = process.wait()
record.update({'status': 'STOPPED', 'exit_code': code,
               'finished_at': datetime.datetime.now(datetime.timezone.utc).isoformat()})
(folder / 'runtime.json').write_text(json.dumps(record, indent=2) + '\n')
raise SystemExit(code)
