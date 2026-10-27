"""Execute one explicitly approved source-only Claude Code/DeepSeek review."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

root = Path.cwd()
out = Path(__file__).resolve().parent
prepared = root/'tasks/portal-background-session-20261019/evidence/renewed-review-20261027/claude'
manifest = json.loads((prepared/'prepared-payloads.json').read_text())
role = sys.argv[1]
assert role in ('independent', 'adversarial')
prompt = prepared/(role+'-prompt.txt')
digest = hashlib.sha256(prompt.read_bytes()).hexdigest()
assert digest == manifest['payloads'][prompt.name]['sha256']
head = subprocess.check_output(['git', '-C', str(root/'repos/ui/mfe-base'), 'rev-parse', 'HEAD'], text=True).strip()
assert head == manifest['candidate']
command = ['claude', '--print', '--model', 'deepseek-v4-flash', '--output-format', 'json', '--tools', '', '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}', '--disable-slash-commands', '--no-session-persistence', '--safe-mode']
environment = dict(os.environ, CLAUDE_CODE_MAX_OUTPUT_TOKENS='4096')
execution = out/(role+'-execution.json')
response = out/(role+'-response.json')
stderr = out/(role+'-stderr.log')
record = {'role':role, 'status':'RUNNING', 'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'candidate':head, 'prompt':str(prompt), 'prompt_sha256':digest, 'requested_model':'deepseek-v4-flash', 'command':command, 'cwd':'/tmp', 'tools_disabled':True, 'mcp_disabled':True, 'user_authorization':'../user-input-20261027-claude-deepseek-approval.txt'}
execution.write_text(json.dumps(record, indent=2)+'\n')
started = time.monotonic()
with prompt.open('rb') as source, response.open('wb') as sink, stderr.open('wb') as error:
    result = subprocess.run(command, stdin=source, stdout=sink, stderr=error, cwd='/tmp', env=environment)
record.update({'ended_at':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'elapsed_seconds':time.monotonic()-started, 'exit_code':result.returncode, 'response':response.name, 'response_sha256':hashlib.sha256(response.read_bytes()).hexdigest(), 'stderr_sha256':hashlib.sha256(stderr.read_bytes()).hexdigest()})
try:
    body = json.loads(response.read_text())
    record.update({'success':result.returncode == 0 and not body.get('is_error', False), 'is_error':body.get('is_error'), 'models':list(body.get('modelUsage', {})), 'subtype':body.get('subtype')})
except (ValueError, OSError) as error:
    record.update({'success':False, 'parse_error':str(error)})
record['status'] = 'COMPLETED' if record['success'] else 'FAILED'
execution.write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps({key:record.get(key) for key in ['role','status','exit_code','models','elapsed_seconds']}))
raise SystemExit(0 if record['success'] else 1)
