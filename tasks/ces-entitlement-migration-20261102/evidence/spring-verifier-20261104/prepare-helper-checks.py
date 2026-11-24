"""Focused preparation-boundary checks. No dependency acquisition or application execution."""
import argparse
import datetime
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / 'tasks/ces-entitlement-migration-20261102/spring-verifier/prepare-sdks.py'
OUT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('task_prepare_sdks', SOURCE)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
results = []

def check(name, operation):
    operation()
    results.append({'case': name, 'status': 'PASSED'})

def rejects(value):
    try:
        helper.positive_seconds(value)
    except argparse.ArgumentTypeError:
        return
    raise AssertionError('invalid command deadline accepted')

check('minimum command deadline', lambda: helper.positive_seconds('1') == 1 or (_ for _ in ()).throw(AssertionError()))
check('maximum command deadline', lambda: helper.positive_seconds('86400') == 86400 or (_ for _ in ()).throw(AssertionError()))
for value in ('0', '86401', 'abc'):
    check('reject invalid deadline ' + value, lambda value=value: rejects(value))
with tempfile.TemporaryDirectory() as directory:
    temporary = Path(directory)
    def archive_case(name, symlink=False):
        payload = io.BytesIO()
        with tarfile.open(fileobj=payload, mode='w') as archive:
            member = tarfile.TarInfo(name)
            if symlink:
                member.type = tarfile.SYMTYPE
                member.linkname = '../escape'
                archive.addfile(member)
            else:
                member.size = 1
                archive.addfile(member, io.BytesIO(b'x'))
        try:
            helper.extract_archive(payload.getvalue(), temporary / 'export')
        except helper.PreparationError:
            return
        raise AssertionError('unsafe archive path accepted')
    for name in ('../escape', '/escape'):
        check('reject archive ' + name, lambda name=name: archive_case(name))
    check('reject archive symlink', lambda: archive_case('link', True))
    def valid_archive():
        payload=io.BytesIO()
        with tarfile.open(fileobj=payload, mode='w') as archive:
            member=tarfile.TarInfo('src/file.txt');member.size=1;archive.addfile(member,io.BytesIO(b'x'))
        helper.extract_archive(payload.getvalue(), temporary / 'valid')
        assert (temporary / 'valid/src/file.txt').read_bytes() == b'x'
    check('extract ordinary source file', valid_archive)
    def deadline():
        result=helper.run_build([sys.executable,'-c','import time; time.sleep(20)'],temporary,dict(os.environ),temporary/'timeout.log',1)
        assert result == 124
        assert 'PREPARATION_TIMEOUT' in (temporary/'timeout.log').read_text()
    check('terminate timed out build process', deadline)
    def overwrite():
        destination=temporary/'existing';destination.mkdir();(destination/'ems2-sdk.jar').write_bytes(b'preserved')
        options=argparse.Namespace(output=destination)
        try:helper.prepare(options,dict(os.environ),{})
        except helper.PreparationError:pass
        else:raise AssertionError('existing SDK artifact overwritten')
        assert (destination/'ems2-sdk.jar').read_bytes() == b'preserved'
    check('refuse existing SDK artifact overwrite', overwrite)
command=[sys.executable,str(SOURCE),'--sdk-repo',str(ROOT/'repos/libraries/single-ui-sdk-starter'),'--java-home','/opt/homebrew/opt/openjdk@17','--check']
readiness=subprocess.run(command,capture_output=True,text=True,timeout=20)
assert readiness.returncode == 0, readiness.stderr
diagnosis=json.loads(readiness.stdout)
assert diagnosis['java_major'] >= 17 and diagnosis['status'] == 'READY'
results.append({'case':'read-only local prerequisite diagnosis','status':'PASSED','diagnosis':diagnosis})
report={'status':'PASSED','finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'checks':results,'limits':['No Maven dependency acquisition, SDK build, verifier build, or live company request executed by these checks.','Windows command behavior remains inspected only.']}
(OUT/'prepare-helper-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'checks':len(results)},indent=2))
