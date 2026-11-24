from pathlib import Path
import datetime, hashlib, json, os, subprocess

root = Path.cwd()
runtime = root / '.workbench/four-checks-ac4-20261027'
evidence = Path(__file__).parent / 'ac4-browser'
evidence.mkdir(exist_ok=True)
source = root / '.workbench/ut-final-cancellation-20261027/source'
environment = dict(os.environ, NPM_CONFIG_UPDATE_NOTIFIER='false', mode='development', orgName='fm', devtool='source-map', isLocal='true', publicUrl='', importmap='/importmaplocal.json')
records = []
for name, cwd, config, port in [('mfe', source, runtime/'mfe.webpack.cjs', 8152), ('root', root/'repos/ui/mfe-root-config', runtime/'root.webpack.cjs', 8153)]:
    environment['port'] = str(port)
    command = ['node', str(cwd/'node_modules/webpack/bin/webpack.js'), 'serve', '--config', str(config)]
    with (evidence/(name+'.log')).open('w') as stream:
        process = subprocess.Popen(command, cwd=cwd, env=environment, stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
    records.append({'name':name, 'pid':process.pid, 'cwd':str(cwd), 'command':command, 'config_sha256':hashlib.sha256(config.read_bytes()).hexdigest(), 'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat()})
    (evidence/(name+'.webpack.cjs.snapshot')).write_bytes(config.read_bytes())
(evidence/'started-processes.json').write_text(json.dumps(records, indent=2)+'\n')
print(json.dumps([{'name':r['name'],'pid':r['pid']} for r in records]))
