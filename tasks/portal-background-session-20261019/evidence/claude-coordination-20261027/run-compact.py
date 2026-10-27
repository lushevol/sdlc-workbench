"""Execute one bounded packet using the user's authorized provider."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, time

root=Path.cwd();out=Path(__file__).resolve().parent;manifest=json.loads((out/'compact-manifest.json').read_text());name=sys.argv[1]
row=next(item for item in manifest['packets'] if item['name']==name);prompt=out/(name+'-prompt.txt')
assert hashlib.sha256(prompt.read_bytes()).hexdigest()==row['sha256']
head=subprocess.check_output(['git','-C',str(root/'repos/ui/mfe-base'),'rev-parse','HEAD'],text=True).strip();assert head==manifest['candidate']
command=['claude','--print','--model','deepseek-v4-flash','--output-format','json','--tools','','--strict-mcp-config','--mcp-config','{"mcpServers":{}}','--disable-slash-commands','--no-session-persistence','--safe-mode']
environment=dict(os.environ,CLAUDE_CODE_MAX_OUTPUT_TOKENS='4096');execution=out/(name+'-execution.json');response=out/(name+'-response.json');stderr=out/(name+'-stderr.log')
record={'role':row['role'],'name':name,'selected_paths':row['selected_paths'],'status':'RUNNING','started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate':head,'prompt':prompt.name,'prompt_sha256':row['sha256'],'requested_model':'deepseek-v4-flash','command':command,'cwd':'/tmp','tools_disabled':True,'mcp_disabled':True,'authorization':'../user-input-20261027-claude-deepseek-approval.txt'}
execution.write_text(json.dumps(record,indent=2)+'\n');started=time.monotonic()
with prompt.open('rb') as source,response.open('wb') as sink,stderr.open('wb') as error:
    result=subprocess.run(command,stdin=source,stdout=sink,stderr=error,cwd='/tmp',env=environment)
record.update({'ended_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-started,'exit_code':result.returncode,'response':response.name,'response_sha256':hashlib.sha256(response.read_bytes()).hexdigest(),'stderr_sha256':hashlib.sha256(stderr.read_bytes()).hexdigest()})
try:
    body=json.loads(response.read_text());record.update({'success':result.returncode==0 and not body.get('is_error',False),'is_error':body.get('is_error'),'models':list(body.get('modelUsage',{}))})
except (ValueError,OSError) as error:record.update({'success':False,'parse_error':str(error)})
record['status']='COMPLETED' if record['success'] else 'FAILED';execution.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({key:record.get(key) for key in ['name','status','exit_code','models','elapsed_seconds']}));raise SystemExit(0 if record['success'] else 1)
