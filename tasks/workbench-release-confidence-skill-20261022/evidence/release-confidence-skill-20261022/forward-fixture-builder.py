from pathlib import Path
import hashlib, json, subprocess, sys, tempfile
root = Path(tempfile.mkdtemp(prefix='release-confidence-forward-'))
def git(p, *args):
    return subprocess.check_output(['git', '-C', str(p), *args], text=True).strip()
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, s):
    p.write_text(s, encoding='utf-8')
for name, mode in [('release-a', 'current'), ('release-b', 'stale'), ('release-c', 'failure')]:
    case = root / name
    repo = case / 'repo'
    repo.mkdir(parents=True)
    git(repo, 'init', '-q')
    git(repo, 'config', 'user.name', 'Synthetic Fixture')
    git(repo, 'config', 'user.email', 'fixture@example.invalid')
    write(repo / 'format_cli.py', 'import sys\nprint(sys.argv[1])\n')
    git(repo, 'add', 'format_cli.py')
    git(repo, 'commit', '-qm', 'Baseline')
    base = git(repo, 'rev-parse', 'HEAD')
    write(repo / 'format_cli.py', 'import sys\nprint(sys.argv[1].strip())\n')
    write(repo / 'test_cli.py', '''import subprocess, sys, unittest
from pathlib import Path
TOOL = Path(__file__).with_name('format_cli.py')
class FormatTests(unittest.TestCase):
    def test_trim(self):
        out = subprocess.check_output([sys.executable, str(TOOL), '  alpha  '], text=True)
        self.assertEqual(out, 'alpha\\n')
    def test_empty(self):
        out = subprocess.check_output([sys.executable, str(TOOL), ''], text=True)
        self.assertEqual(out, '\\n')
if __name__ == '__main__': unittest.main(verbosity=2)
''')
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'Trim formatting utility output')
    tested = git(repo, 'rev-parse', 'HEAD')
    proc = subprocess.run([sys.executable, 'test_cli.py'], cwd=repo, text=True, capture_output=True)
    write(case / 'test-output.txt', proc.stdout + proc.stderr)
    run = {'fixture_kind':'synthetic evaluation only', 'command':[sys.executable,'test_cli.py'], 'code_revision':tested,
           'code_sha256':sha(repo / 'format_cli.py'),'test_revision':tested,'test_sha256':sha(repo / 'test_cli.py'),
           'returncode':proc.returncode,'result_file':'test-output.txt','result_sha256':sha(case / 'test-output.txt'),
           'environment':{'python':sys.version,'executable':sys.executable,'mode':'actual local CLI subprocess, no mocks'},
           'assertions':['FormatTests.test_trim','FormatTests.test_empty']}
    if mode in ('stale','failure'):
        body = 'import sys\nprint(sys.argv[1].strip().upper())\n' if mode == 'stale' else 'import sys\nprint(sys.argv[1])\n'
        write(repo / 'format_cli.py', body)
        git(repo, 'add', 'format_cli.py')
        git(repo, 'commit', '-qm', 'Revise candidate formatter')
    head = git(repo, 'rev-parse', 'HEAD')
    if mode == 'failure':
        proc = subprocess.run([sys.executable, 'test_cli.py'], cwd=repo, text=True, capture_output=True)
        write(case / 'candidate-test-output.txt', proc.stdout + proc.stderr)
        run = {'fixture_kind':'synthetic evaluation only','command':[sys.executable,'test_cli.py'],'code_revision':head,
               'code_sha256':sha(repo/'format_cli.py'),'test_revision':head,'test_sha256':sha(repo/'test_cli.py'),
               'returncode':proc.returncode,'result_file':'candidate-test-output.txt','result_sha256':sha(case/'candidate-test-output.txt'),
               'environment':{'python':sys.version,'executable':sys.executable,'mode':'actual local CLI subprocess, no mocks'},
               'assertions':['FormatTests.test_trim','FormatTests.test_empty']}
    (case/'execution.json').write_text(json.dumps(run,indent=2)+'\n')
    write(case/'change-contract.md', '''# Synthetic utility change contract
This is harness maintenance for a standalone formatting CLI.
The fixture defines no real business requirement or approval.
Included behaviors: FMT-01 and FMT-02. No external consumers exist in this synthetic repository.

## FMT-01
Scenario: Trim surrounding whitespace
  Given the CLI input is "  alpha  "
  When the operator runs the formatter
  Then stdout equals "alpha" followed by one newline

## FMT-02
Scenario: Preserve empty input
  Given the CLI input is an empty string
  When the operator runs the formatter
  Then stdout equals one newline

Required checks: direct CLI subprocess assertions for both behaviors.
Requirement implementation, assertion and execution denominators each contain exactly these two behavior versions, version 1.
''')
    write(case/'release-policy.md', '''# Synthetic assessment conditions
This file is synthetic evaluation input. It records no real review or authorization.
Required conditions: both change-contract behaviors conform; the exact immutable deliverable matches inspected source and passing tests.
The deployable deliverable is the single format_cli.py file, with no packaging transformation.
Target runtime: this fixture's recorded Python executable and version. No configuration, data stores, network, or external services apply.
Deployment is an atomic file replacement in the controlled target. Rollback restores the retained baseline file.
Required readiness evidence: current source review, both direct CLI tests, artifact hash, rollback source availability, and smoke command.
No code line coverage threshold applies. No human technical readiness sign-off is required by this synthetic policy.
Actual deployment authorization remains a separate pending human decision.
''')
    artifact = case/'format_cli.py.artifact'
    artifact.write_bytes((repo/'format_cli.py').read_bytes())
    (case/'baseline.py.artifact').write_bytes(subprocess.check_output(['git','-C',str(repo),'show',f'{base}:format_cli.py']))
    scope={'fixture_kind':'synthetic evaluation only','scope':'harness maintenance','release_id':name,'base':base,'candidate':head,
           'repo':'repo','artifact':'format_cli.py.artifact','artifact_sha256':sha(artifact),'artifact_source':'format_cli.py',
           'environment':run['environment'],'target_environment':'synthetic controlled install, same recorded Python runtime',
           'deployment_authorization':None,'owners':'unknown'}
    (case/'release.json').write_text(json.dumps(scope,indent=2)+'\n')
    write(case/'review.md', f'''# Synthetic retained review
Comparison: {base} to {head}; repository repo; range mode.
Inspected paths: format_cli.py and test_cli.py. No excluded changed paths.
Reviewer: synthetic fixture input, not a real human approval.
No actionable defects were reported. Inspect exact source and assertions before accepting this summary.
''')
    write(case/'operations.md', '''# Synthetic operations evidence
Deliverable identity and target runtime are in release.json.
The baseline artifact is retained locally for atomic replacement rollback.
No migration, service, credentials, or cross-repository compatibility boundary applies to this standalone CLI.
Smoke command uses the exact Python executable and the deliverable with "  alpha  ". Expected stdout is "alpha" plus newline.
Operator and production authorization are unknown. No actual PROD action is requested or authorized.
''')
d = root / 'release-d'
import shutil
shutil.copytree(root / 'release-a', d)
(d / 'execution.json').unlink()
(d / 'test-output.txt').unlink()
scope = json.loads((d / 'release.json').read_text())
scope['release_id'] = 'release-d'
(d / 'release.json').write_text(json.dumps(scope, indent=2) + '\n')
(d / 'execution-availability.md').write_text('# Retained execution availability\n\nNo retained test execution result was supplied for this candidate.\nThe test definitions and candidate artifact remain available for inspection.\nThis assessment request authorizes inspection only. No new execution is requested.\n')
manifest={str(p.relative_to(root)):sha(p) for p in sorted(root.rglob('*')) if p.is_file() and '.git' not in p.parts}
(root/'fixture-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(root)
