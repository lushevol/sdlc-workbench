"""Validate modified task documents and newly added local links."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess
import urllib.parse

root = Path.cwd()
output = Path(__file__).parent
documents = [
    'tasks/portal-background-session-20261019/06-test-cases.md',
    'tasks/portal-background-session-20261019/09-delivery-coverage-20261026.md',
    'tasks/portal-background-session-20261019/10-delivery-confidence-20261026.md',
    'tasks/portal-background-session-20261019/evidence/index.md',
]
lint = subprocess.run([str(root/'.venv/bin/ai-sdlc'), 'lint', *documents[:3]], capture_output=True, text=True)
workspace = subprocess.run([str(root/'.venv/bin/ai-sdlc'), '--workspace', str(root), 'validate'], capture_output=True, text=True)
diff_check = subprocess.run(['git', 'diff', 'HEAD', '--check', '--', *documents], capture_output=True, text=True)
errors = []
checked = 0
for name in documents:
    diff = subprocess.check_output(['git', 'diff', 'HEAD', '--unified=0', '--', name], text=True)
    added = [line[1:] for line in diff.splitlines() if line.startswith('+') and not line.startswith('+++')]
    for line in added:
        for target in re.findall(r'\]\(([^)]+)\)', line):
            if target.startswith(('http:', 'https:', 'mailto:')):
                continue
            raw, _, anchor = target.partition('#')
            file = ((root/name).parent/urllib.parse.unquote(raw)) if raw else root/name
            checked += 1
            if not file.exists():
                errors.append({'document':name, 'target':target, 'reason':'missing path'})
                continue
            if not anchor or file.is_dir():
                continue
            if re.fullmatch(r'L\d+(?:-L\d+)?', anchor):
                number = int(re.match(r'L(\d+)', anchor).group(1))
                if number > len(file.read_text(errors='replace').splitlines()):
                    errors.append({'document':name, 'target':target, 'reason':'line beyond end'})
            elif file.suffix == '.md':
                text = file.read_text(errors='replace')
                anchors = set(re.findall(r'<a\s+id=["\']([^"\']+)', text))
                for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
                    heading = re.sub(r'<[^>]*>', '', heading).lower()
                    anchors.add(re.sub(r'[^\w\- ]', '', heading).replace(' ', '-'))
                if urllib.parse.unquote(anchor) not in anchors:
                    errors.append({'document':name, 'target':target, 'reason':'anchor missing'})
record = {
    'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'documents':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in documents},
    'artifact_lint':json.loads(lint.stdout) if lint.stdout else {'error':lint.stderr},
    'artifact_lint_exit_code':lint.returncode,
    'workspace_validation':json.loads(workspace.stdout) if workspace.stdout else {'error':workspace.stderr},
    'workspace_validation_exit_code':workspace.returncode,
    'diff_check_exit_code':diff_check.returncode,
    'diff_check_output':diff_check.stdout + diff_check.stderr,
    'new_local_links_checked':checked,
    'link_errors':errors,
    'limitations':['Only links in added diff lines are checked.', 'The link checker does not verify semantic authority.', 'Automated checks do not check the complete ASD-STE100 dictionary or grammar rules.'],
    'writing_review':{'standard':'ASD-STE100', 'automated_check':'PASSED' if not (lint.returncode or workspace.returncode or diff_check.returncode or errors) else 'FAILED', 'asd_review':'PENDING', 'reviewer':None, 'reviewed_at':None},
}
(output/'document-validation.json').write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps({'lint':lint.returncode, 'workspace':workspace.returncode, 'diff_check':diff_check.returncode, 'links':checked, 'link_errors':errors}))
raise SystemExit(1 if lint.returncode or workspace.returncode or diff_check.returncode or errors else 0)
