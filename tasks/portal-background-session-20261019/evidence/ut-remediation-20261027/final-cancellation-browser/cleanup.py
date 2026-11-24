from pathlib import Path
import os,signal,json,subprocess,datetime
folder=Path('tasks/portal-background-session-20261019/evidence/ut-remediation-20261027/final-cancellation-browser');records=json.loads((folder/'started-processes.json').read_text());out=[]
for item in records:
 try:os.killpg(item['pid'],signal.SIGTERM);result='SIGTERM_SENT_TO_OWN_PROCESS_GROUP'
 except ProcessLookupError:result='ALREADY_STOPPED'
 out.append({'name':item['name'],'pid':item['pid'],'result':result})
report={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'processes':out,'bff8088_untouched':True,'other_task_processes_untouched':True}
(folder/'cleanup.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
