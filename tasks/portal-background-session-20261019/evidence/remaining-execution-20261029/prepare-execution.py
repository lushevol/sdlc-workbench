"""Prepare an immutable local source snapshot; preserve the business worktree."""
from pathlib import Path
import datetime, hashlib, io, json, subprocess, tarfile, tempfile

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
REPO = ROOT / 'repos/ui/mfe-base'
REVISION = '66c6411ade58e4d134e381c2baee8ad3f76a8dbf'
runtime = Path(tempfile.mkdtemp(prefix='comprehensive-renewal-'))
source = runtime / 'source'
source.mkdir()
archive = subprocess.check_output(['git', '-C', str(REPO), 'archive', REVISION])
with tarfile.open(fileobj=io.BytesIO(archive)) as stream:
    stream.extractall(source, filter='data')
(source / 'node_modules').symlink_to(REPO / 'node_modules', target_is_directory=True)
sha = lambda data: hashlib.sha256(data).hexdigest()
binding = {
    'created_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'repository': 'mfe-base', 'revision': REVISION, 'runtime': str(runtime),
    'source': str(source), 'archive_sha256': sha(archive),
    'dirty_worktree_excluded': subprocess.check_output(['git', '-C', str(REPO), 'status', '--short'], text=True),
    'source_hashes': {str(p.relative_to(source)): sha(p.read_bytes()) for p in sorted((source / 'src').rglob('*')) if p.is_file()},
    'limits': ['Immutable committed source only; dirty worktree excluded.', 'Dependency installation reused from the existing checkout; no downloads.']
}
(OUT / 'execution-source-binding.json').write_text(json.dumps(binding, indent=2) + '\n')
print(json.dumps({'revision': REVISION, 'source': str(source)}))
