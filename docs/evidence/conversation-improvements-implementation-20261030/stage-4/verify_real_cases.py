"""Retain each controlled prerequisite verification before starting the next case."""
from datetime import datetime, timezone
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import subprocess
import threading

from ai_sdlc_workbench.test_preflight import plan_test_execution, preflight_test_execution

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / 'repos/ui/mfe-root-config/src/root.ts'
ASSET = ROOT / '.workbench/portal-session-real-20261019/frontend/root-config-build/config.js'
SOURCE_MAP = ASSET.with_suffix('.js.map')
BUILD_RESULT = ROOT / '.workbench/portal-session-real-20261019/frontend/mfe-root-config-build-result.json'
STACK = ROOT / '.workbench/ui-audit-stack-attempt03.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path):
    return path.relative_to(ROOT).as_posix()


def save(name, data):
    payload = {'case_id': name, 'recorded_at': datetime.now(timezone.utc).isoformat(), **data}
    (HERE / f'{name}.json').write_text(json.dumps(payload, indent=2) + '\n')
    print(json.dumps({'case_id': name, 'assertions_passed': data.get('assertions_passed')}), flush=True)


def declaration(name, checks):
    path = HERE / f'{name}-checks.json'
    path.write_text(json.dumps({'schema_version': 1, **checks}, indent=2) + '\n')
    return relative(path)


def plan(checks):
    return plan_test_execution(ROOT, runner='playwright', suite='e2e:test',
                               output_dir=relative(HERE / 'not-created-run-output'), checks_file=checks)


def retain(name, expected, result, assertions, **extra):
    passed = all(assertions.values())
    save(name, {'expected': expected, 'result': result, 'assertions': assertions,
                'assertions_passed': passed, 'product_behavior': 'NOT_EXECUTED', **extra})
    if not passed:
        raise AssertionError(f'{name} failed; evidence already retained')


def main():
    stack = json.loads(STACK.read_text())
    bindings = [{'label': entry['label'], 'path': entry['path'], 'expected_sha256': entry['sha256'],
                 'actual_sha256': sha(Path(entry['path']))} for entry in stack['sourceBindings']]
    services = [{'id': f'prepared-{index + 1}', 'url': url} for index, url in enumerate(stack['readyUrls'])]
    current = plan(declaration('stopped-session-services', {'services': services}))
    result = preflight_test_execution(current, ROOT, probe_services=True)
    service_rows = [row for row in result['checks'] if row['id'].startswith('service:')]
    retain('PF-REAL-001', 'Diagnose all five stopped prepared services without a product failure.', result, {
        'five_stopped_services': len(service_rows) == 5 and all(row['status'] == 'FAILED' for row in service_rows),
        'browser_asset_present': any(row['id'] == 'browser-asset' and row['status'] == 'READY' for row in result['checks']),
        'retained_stack_bindings_match': all(row['expected_sha256'] == row['actual_sha256'] for row in bindings),
        'build_identity_unknown': result['build_identity'] == 'UNKNOWN',
        'no_suite_execution': result['suite_executed'] is False,
        'no_run_output_created': not Path(current['output_dir']).exists(),
    }, stack={'path': relative(STACK), 'sha256': sha(STACK), 'source_bindings': bindings,
              'limits': stack['limits']})

    source_map = json.loads(SOURCE_MAP.read_text())
    position = source_map['sources'].index('webpack://root-config/./src/root.ts')
    embedded = source_map['sourcesContent'][position].encode()
    revision = subprocess.run(['git', '-C', str(SOURCE.parent.parent), 'rev-parse', 'HEAD'],
                              check=True, capture_output=True, text=True).stdout.strip()
    manifest = {'schema_version': 1, 'sources': [
        {'path': relative(SOURCE), 'sha256': sha(SOURCE), 'revision': revision},
        {'path': relative(SOURCE_MAP), 'sha256': sha(SOURCE_MAP), 'revision': None},
        {'path': relative(BUILD_RESULT), 'sha256': sha(BUILD_RESULT), 'revision': None}],
        'artifacts': [{'path': relative(ASSET), 'sha256': sha(ASSET)}]}
    manifest_path = HERE / 'retained-root-asset-source-manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    requests = []
    asset_bytes = ASSET.read_bytes()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            requests.append(self.path)
            if self.path == '/redirect':
                self.send_response(302)
                self.send_header('Location', '/matching')
                self.end_headers()
                return
            body = asset_bytes if self.path == '/matching' else asset_bytes + b'\n/* controlled mismatch */'
            if self.path == '/oversized':
                body = b'x' * (1024 * 1024 + 1)
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    server.daemon_threads = True
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f'http://127.0.0.1:{server.server_port}'
    asset = {'id': 'retained-root-config', 'url': base + '/matching', 'artifact_path': relative(ASSET),
             'source_manifest': relative(manifest_path), 'source_manifest_sha256': sha(manifest_path)}
    common_limits = ['Controlled loopback HTTP fixture serves an actual retained built frontend asset.',
                     'The fixture is not an application runtime or deployed environment.',
                     'Matching bytes prove only the declared artifact and source fingerprint scope.',
                     'No browser, credentials, application login, or business suite was executed.']
    try:
        current = plan(declaration('matching-asset', {'served_assets': [asset]}))
        result = preflight_test_execution(current, ROOT, probe_services=True)
        retain('PF-REAL-002', 'Match retained served bytes against the source-bound artifact.', result, {
            'identity_matched': result['build_identity'] == 'MATCHED',
            'preflight_ready': result['status'] == 'READY',
            'asset_bytes_match': result['served_assets'][0]['actual_sha256'] == sha(ASSET),
            'embedded_root_source_matches': embedded == SOURCE.read_bytes(),
            'no_suite_execution': result['suite_executed'] is False,
        }, source_map_embedded_source={'name': source_map['sources'][position],
              'sha256': hashlib.sha256(embedded).hexdigest()}, limits=common_limits)

        mismatch = {**asset, 'url': base + '/mismatch'}
        result = preflight_test_execution(plan(declaration('mismatched-asset', {'served_assets': [mismatch]})), ROOT, probe_services=True)
        retain('PF-REAL-003', 'Reject altered served bytes without changing the retained artifact.', result, {
            'identity_mismatched': result['build_identity'] == 'MISMATCH',
            'preflight_incomplete': result['status'] == 'INCOMPLETE',
            'local_artifact_unchanged': sha(ASSET) == manifest['artifacts'][0]['sha256'],
            'asset_hashes_differ': result['served_assets'][0]['actual_sha256'] != result['served_assets'][0]['expected_sha256'],
        }, limits=common_limits)

        result = preflight_test_execution(plan(declaration('no-fingerprint', {'services': [{'id': 'reachable', 'url': base + '/matching'}]})), ROOT, probe_services=True)
        retain('PF-REAL-004', 'Keep served build identity unknown when no fingerprint is declared.', result, {
            'service_reachable': any(row['id'] == 'service:reachable' and row['status'] == 'READY' for row in result['checks']),
            'identity_unknown': result['build_identity'] == 'UNKNOWN',
            'unknown_blocks_ready': result['status'] == 'INCOMPLETE',
        }, limits=common_limits)

        before = len(requests)
        invalid = {**asset, 'source_manifest_sha256': '0' * 64}
        result = preflight_test_execution(plan(declaration('invalid-manifest-binding', {'served_assets': [invalid]})), ROOT, probe_services=True)
        retain('PF-REAL-005', 'Reject an invalid manifest binding before requesting the asset.', result, {
            'binding_rejected': result['served_assets'][0]['status'] == 'INVALID_BINDING',
            'no_asset_request': len(requests) == before,
            'identity_unknown': result['build_identity'] == 'UNKNOWN',
        }, limits=common_limits)

        before = len(requests)
        result = preflight_test_execution(plan(declaration('redirect-refused', {'services': [{'id': 'redirect', 'url': base + '/redirect'}]})), ROOT, probe_services=True)
        retain('PF-REAL-006', 'Refuse readiness redirects and retain a specific setup failure.', result, {
            'redirect_setup_failed': any(row['id'] == 'service:redirect' and row['status'] == 'FAILED' for row in result['checks']),
            'redirect_target_not_requested': requests[before:] == ['/redirect'],
        }, limits=common_limits)

        result = preflight_test_execution(plan(declaration('oversized-response', {'services': [{'id': 'oversized', 'url': base + '/oversized'}]})), ROOT, probe_services=True)
        retain('PF-REAL-007', 'Reject a service response above one MiB without retaining its body.', result, {
            'oversized_setup_failed': any(row['id'] == 'service:oversized' and row['status'] == 'FAILED' for row in result['checks']),
            'response_body_not_retained': 'xxxxxxxxxx' not in json.dumps(result),
        }, limits=common_limits)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)

    save('verification-receipt', {'assertions_passed': True,
        'command': '.venv/bin/python docs/evidence/conversation-improvements-implementation-20261030/stage-4/verify_real_cases.py',
        'cases': [f'PF-REAL-{number:03}' for number in range(1, 8)],
        'source_identities': [{'path': name, 'sha256': sha(ROOT / name)} for name in [
            'core/test_preflight.py', 'tests/test_test_preflight.py', relative(Path(__file__))]],
        'suite_executed': False, 'product_behavior': 'NOT_EXECUTED', 'request_paths': requests})


if __name__ == '__main__':
    main()
