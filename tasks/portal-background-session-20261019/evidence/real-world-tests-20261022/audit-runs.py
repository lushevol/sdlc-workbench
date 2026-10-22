"""Audit retained native-run evidence without connecting to any browser or service."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import re


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', required=True, type=Path)
    parser.add_argument('--test-repo', required=True, type=Path)
    parser.add_argument('--private-fixture-source', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--runs', required=True, nargs='+')
    args = parser.parse_args()
    stage = args.stage.resolve()
    driver_root = args.test_repo.resolve() / 'Tests/ratan/plugin/ui/session/real-world'
    private = re.findall(r'\b(?:USER|PASSWORD)\s*=\s*"([^"]+)"', args.private_fixture_source.read_text())
    if len(private) != 2:
        raise ValueError('Expected two private fixture bindings.')
    private_bytes = [value.encode() for value in private]
    jwt_pattern = re.compile(rb'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+')
    findings = []
    results = []
    for run_id in args.runs:
        run = stage / run_id
        result_file = run / 'result.json'
        result = json.loads(result_file.read_text())
        assertions = result['assertions']
        failed = [item['id'] for item in assertions if item['passed'] is not True]
        manifest_name = next((name for name in ('artifact-manifest.redacted-v2.json',
                            'artifact-manifest.redacted.json', 'artifact-manifest.json')
                              if (run / name).exists()), None)
        manifest = json.loads((run / manifest_name).read_text())
        manifest_checks = []
        for item in manifest:
            retained = run / item['path']
            matched = retained.is_file() and digest(retained.read_bytes()) == item['sha256']
            manifest_checks.append(matched)
            if not matched:
                findings.append({'run': run_id, 'kind': 'manifest-mismatch', 'path': item['path']})
        drivers = []
        for item in result['driverSources']:
            retained = run / item['retained']
            current = driver_root / item['module']
            row = {'module': item['module'], 'sha256': item['sha256'],
                   'snapshotMatches': digest(retained.read_bytes()) == item['sha256'],
                   'currentSourceMatches': digest(current.read_bytes()) == item['sha256']}
            drivers.append(row)
            if not row['snapshotMatches']:
                findings.append({'run': run_id, 'kind': 'driver-snapshot-mismatch', 'module': item['module']})
        checks = {'artifactManifestMatches': all(manifest_checks),
                  'driverSnapshotsMatch': all(item['snapshotMatches'] for item in drivers),
                  'nativeDefaultContext': result['nativeBrowser']['nativeDefaultContext'] is True,
                  'nativeNoDefaults': result['nativeBrowser']['noDefaults'] is True,
                  'nativeBrowserClosed': result['nativeBrowser']['status'] == 'CLOSED',
                  'timerDelaysUnchanged': result['timerDelaysChanged'] is False}
        negative = result['caseId'] == 'RW-CONFIG-PREFLIGHT' and result['status'] == 'FAILED'
        if negative:
            timing = result['timing']['access']
            checks.update({'expectedFailureOnly': failed == ['preflight-access-issued-lifetime'],
                           'actual28800Expected900': timing['lifetimeSeconds'] == 28800
                           and timing['expectedLifetimeSeconds'] == 900,
                           'measurementNeverStarted': not (run / 'measurement-start.json').exists()})
        else:
            checks['recordedStatusMatchesAssertions'] = bool(assertions) and result['status'] == ('FAILED' if failed else 'PASSED')
        if result['caseId'] == 'RW-BLOTTER-HIDDEN-30M':
            measurement = result['measurement']
            checks['fullThirtyMinutes'] = min(measurement['actualWallMs'], measurement['actualMonotonicMs']) >= 1800000
            required = ['native-hidden', 'trusted-input', 'same-document', 'real-clock', 'fixed-expiry',
                        'no-early-timeout', 'returned-component', 'final-access-timer', 'final-refresh-timer']
            checks['requiredHiddenAssertionsRetained'] = all(any(item['id'] == key for item in assertions) for key in required)
        stack_file = stage / (run_id + '-stack') / 'stack-result.json'
        stack = json.loads(stack_file.read_text())
        checks['ownedServicesStopped'] = stack.get('servicesStopped') is True and all(
            item['status'] == 'STOPPED' for item in stack['services'])
        for name, passed in checks.items():
            if not passed:
                findings.append({'run': run_id, 'kind': 'predicate-failed', 'predicate': name})
        results.append({'runId': run_id, 'caseId': result['caseId'], 'recordedStatus': result['status'],
                        'resultSha256': digest(result_file.read_bytes()), 'assertions': len(assertions),
                        'passedAssertions': len(assertions) - len(failed), 'failedAssertionIds': failed,
                        'classification': 'EXPECTED_MISMATCH_DETECTED' if negative else result['status'],
                        'checks': checks, 'drivers': drivers, 'artifactManifest': manifest_name,
                        'artifactCount': len(manifest), 'measurement': result.get('measurement')})
    scanned = 0
    for file in stage.rglob('*'):
        if not file.is_file():
            continue
        scanned += 1
        data = file.read_bytes()
        if any(value in data for value in private_bytes):
            findings.append({'kind': 'private-fixture-value', 'path': str(file.relative_to(stage))})
        if jwt_pattern.search(data):
            findings.append({'kind': 'raw-jwt-pattern', 'path': str(file.relative_to(stage))})
    record = {'recordedAt': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'status': 'FAILED' if findings else 'PASSED', 'results': results, 'findings': findings,
              'standard': 'ASD-STE100', 'automated_check': 'FAILED' if findings else 'PASSED',
              'asd_review': 'PENDING', 'reviewer': None, 'reviewed_at': None,
              'scriptSha256': digest(Path(__file__).read_bytes()), 'scannedFiles': scanned,
              'privateValuesPrintedOrRetained': False,
              'limitations': ['Automated checks do not check the complete approved dictionary or grammar rules.',
                         'This audit reads retained evidence. It does not repeat browser execution.',
                         'An integrity audit can pass while a recorded browser case fails. Assertion outcomes remain separate.',
                         'Credential scanning checks known fixture bytes and a JWT pattern. It cannot prove complete secret absence.',
                         'Current-source mismatches remain explicit. Use the exact tested revision for affected claims.',
                         'Screenshots require separate visual review. Local execution does not establish UAT parity.']}
    with args.output.open('x') as stream:
        json.dump(record, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'status': record['status'], 'results': len(results), 'findings': len(findings),
                      'output': str(args.output)}))
    return bool(findings)


if __name__ == '__main__':
    raise SystemExit(main())
