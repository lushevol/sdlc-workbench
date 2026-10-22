"""Run explicitly configured local services until interrupted, then stop owned groups.

Only existing dependencies and prepared source wrappers are used. Raw service logs
remain in the ignored configured runtime directory. Durable output excludes secrets.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import os
import signal
import socket
import subprocess
import time
import urllib.request


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    config_path = Path(args.config).resolve()
    config = json.loads(config_path.read_text())
    evidence = Path(args.output).resolve()
    evidence.mkdir(parents=True, exist_ok=False)
    runtime = Path(config['runtimeDirectory']).resolve()
    runtime.mkdir(parents=True, exist_ok=False)
    record = {'startedAt': utc(), 'status': 'STARTING', 'services': [],
              'configurationSha256': digest(config_path.read_bytes()),
              'launcherSha256': digest(Path(__file__).read_bytes()),
              'runtimeDirectory': str(runtime), 'startupDownloads': False,
              'credentialsRetained': False, 'limits': config.get('limits', [])}
    services = []
    stop_requested = False

    def save():
        temporary = evidence / 'stack-lifecycle.json.tmp'
        temporary.write_text(json.dumps(record, indent=2) + '\n')
        temporary.replace(evidence / 'stack-lifecycle.json')

    def stopped(signum, frame):
        nonlocal stop_requested
        stop_requested = True

    signal.signal(signal.SIGTERM, stopped)
    signal.signal(signal.SIGINT, stopped)
    try:
        # Validate every port before starting any process. Never reuse shared servers.
        for service in config['services']:
            for port in service.get('ports', []):
                if port == 8018:
                    raise ValueError('Port 8018 is outside audit scope.')
                with socket.socket() as connection:
                    if connection.connect_ex(('127.0.0.1', port)) == 0:
                        raise ValueError('Port already in use: ' + str(port))
        env = os.environ.copy()
        env.update(config.get('environment', {}))
        for service in config['services']:
            local_env = env.copy()
            local_env.update(service.get('environment', {}))
            log_path = runtime / (service['name'] + '.log')
            with log_path.open('x') as log:
                process = subprocess.Popen(service['command'], cwd=service['cwd'], env=local_env,
                                           stdin=subprocess.DEVNULL, stdout=log,
                                           stderr=subprocess.STDOUT, start_new_session=True)
            services.append((service, process, log_path))
            record['services'].append({'name': service['name'], 'pid': process.pid,
                                       'processGroup': process.pid,
                                       'ports': service.get('ports', []), 'status': 'STARTING'})
            save()
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        deadline = time.monotonic() + config.get('startupTimeoutSeconds', 120)
        pending = list(config['readyUrls'])
        ready = []
        while pending and time.monotonic() < deadline and not stop_requested:
            if any(process.poll() is not None for _, process, _ in services):
                raise RuntimeError('A configured service exited before readiness.')
            remaining = []
            for url in pending:
                try:
                    with opener.open(url, timeout=2) as response:
                        if response.status == 200:
                            ready.append({'url': url, 'status': response.status, 'capturedAt': utc()})
                        else:
                            remaining.append(url)
                except Exception:
                    remaining.append(url)
            pending = remaining
            if pending:
                time.sleep(0.5)
        record['readyUrls'] = ready
        record['pendingUrls'] = pending
        if stop_requested:
            raise InterruptedError('Local stack interrupted before readiness.')
        if pending:
            raise RuntimeError('Configured services did not become ready.')
        record['status'] = 'RUNNING'
        record['readyAt'] = utc()
        for service in record['services']:
            service['status'] = 'RUNNING'
        save()
        print(json.dumps({'status': 'RUNNING', 'evidence': str(evidence), 'launcherPid': os.getpid()}), flush=True)
        while not stop_requested:
            if any(process.poll() is not None for _, process, _ in services):
                raise RuntimeError('A configured service exited during browser execution.')
            time.sleep(0.5)
        record['status'] = 'STOPPED'
    except Exception as error:
        record['status'] = 'INTERRUPTED' if isinstance(error, InterruptedError) else 'START_OR_RUNTIME_FAILED'
        record['errorType'] = type(error).__name__
        record['error'] = str(error) if isinstance(error, (ValueError, RuntimeError, InterruptedError)) else 'Local stack operation failed.'
    finally:
        for service, process, log_path in reversed(services):
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait(timeout=4)
            row = next(row for row in record['services'] if row['name'] == service['name'])
            row.update({'status': 'STOPPED', 'exitCode': process.returncode})
            data = log_path.read_bytes()
            lines = data.decode(errors='replace').splitlines()
            compile_messages = [line for line in lines if 'compiled successfully' in line or 'compiled with' in line]
            errors = []
            if any('EPERM' in line or 'Operation not permitted' in line for line in lines):
                errors.append('LOCALHOST_LISTEN_DENIED')
            # Raw response bodies, headers, credentials, SQL and token values are excluded.
            metadata = {'rawLogSha256': digest(data), 'rawLogBytes': len(data),
                        'rawLogRetained': False, 'compileMessages': compile_messages,
                        'classifiedErrors': errors,
                        'limit': 'Raw logs remain in the ignored runtime directory.'}
            (evidence / (service['name'] + '-log-metadata.json')).write_text(json.dumps(metadata, indent=2) + '\n')
        record['servicesStopped'] = True
        record['finishedAt'] = utc()
        save()
        print(json.dumps({'status': record['status'], 'servicesStopped': True, 'evidence': str(evidence)}), flush=True)
    return 0 if record['status'] == 'STOPPED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
