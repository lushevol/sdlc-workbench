"""Stop only this execution's three recorded local stack processes after identity checks."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import signal
import subprocess
import time

folder=Path(__file__).resolve().parent
processes=json.loads((folder/'local-processes.json').read_text())
records=[]
for item in processes:
    pid=item['pid']
    result=subprocess.run(['ps','-p',str(pid),'-o','command='],text=True,capture_output=True)
    command=result.stdout.strip()
    expected=('local.portalsession.LocalSessionApplication' in command and '--server.port=8291' in command) if item['name']=='bff' else item['argv'][-1] in command
    identity_basis='Recorded argv'
    if command and not expected and item['name'] in ['mfe','root']:
        cwd_output=subprocess.run(['/usr/sbin/lsof','-a','-p',str(pid),'-d','cwd','-Fn'],text=True,capture_output=True).stdout.splitlines()
        directories=[line[1:] for line in cwd_output if line.startswith('n')]
        expected=command=='webpack' and len(directories)==1 and Path(directories[0]).resolve()==Path(item['cwd']).resolve()
        identity_basis='Recorded owned PID, webpack process title, and canonical unique runtime cwd'
    record={'name':item['name'],'pid':pid,'owned':item['owned'],'command_sha256':hashlib.sha256(command.encode()).hexdigest(),
            'identity_matches':expected,'identity_basis':identity_basis,'was_running':bool(command),'stopped':False}
    if command and item['owned'] and expected:
        os.kill(pid,signal.SIGTERM)
        record['signal']='SIGTERM'
    elif command:
        record['reason']='Identity differs; process preserved.'
    records.append(record)
time.sleep(1)
for record in records:
    result=subprocess.run(['ps','-p',str(record['pid']),'-o','command='],text=True,capture_output=True)
    record['stopped']=not bool(result.stdout.strip())
output={'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'processes':records,
        'application_changes':False,'source_snapshots_preserved':True,
        'limit':'Only recorded, identity-matching owned local processes received SIGTERM.'}
(folder/'execution-cleanup.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'stopped':[r['name'] for r in records if r['stopped']],
                  'preserved':[r['name'] for r in records if not r['stopped']]}))
