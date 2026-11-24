from __future__ import annotations
import base64, hashlib, json, time
from pathlib import Path
from urllib import request, error

BASE = 'http://127.0.0.1:8088/api/auth'
USER = 'session-local'
PASSWORD = 'LocalOnly-Session-20261019'


def token_info(raw: str | None):
    if not raw:
        return None
    token = raw.split(' ', 1)[1] if ' ' in raw else raw
    parts = token.split('.')
    claims = {}
    if len(parts) == 3:
        try:
            payload = parts[1] + '=' * (-len(parts[1]) % 4)
            decoded = json.loads(base64.urlsafe_b64decode(payload.encode()).decode())
            for key in ('iss', 'sub', 'id', 'iat', 'exp', 'auth_time', 'max_age'):
                if key in decoded:
                    claims[key] = decoded[key]
        except Exception as exc:
            claims = {'decode_error': type(exc).__name__}
    return {'sha256': hashlib.sha256(token.encode()).hexdigest(), 'claims': claims}


def call(name: str, path: str, body=None, headers=None):
    data = None if body is None else json.dumps(body).encode()
    req = request.Request(BASE + path, data=data, method='POST' if body is not None else 'GET')
    if body is not None:
        req.add_header('Content-Type', 'application/json')
    for key, value in (headers or {}).items():
        req.add_header(key, value)
    try:
        with request.urlopen(req, timeout=10) as response:
            status = response.status
            response_headers = dict(response.headers.items())
            payload = json.loads(response.read().decode() or '{}')
    except error.HTTPError as exc:
        status = exc.code
        response_headers = dict(exc.headers.items())
        try:
            payload = json.loads(exc.read().decode() or '{}')
        except Exception:
            payload = {}
    result = {
        'name': name,
        'status': status,
        'result': payload.get('result') if isinstance(payload, dict) else None,
        'errorMessage': payload.get('errorMessage') if isinstance(payload, dict) else None,
        'body_keys': sorted(payload.keys()) if isinstance(payload, dict) else [],
    }
    for header in ('Single-UI-Authorization', 'Single-UI-Refresh'):
        if header in response_headers:
            result[header] = token_info(response_headers[header])
    return result, response_headers, payload

results = []

result, _, _ = call('bad_login', '/v2/sso/login', {'username': USER, 'password': 'wrong'})
results.append(result)

result, login_headers, _ = call('login', '/v2/sso/login', {'username': USER, 'password': PASSWORD})
results.append(result)
access_header = login_headers.get('Single-UI-Authorization')
if not access_header:
    raise SystemExit(json.dumps({'status': 'FAILED', 'results': results}, indent=2))
access = access_header.split(' ', 1)[1]
auth = {'Single-UI-Authorization': access_header}

result, refresh_headers, _ = call('refresh_token', '/v2/sso/refreshtoken', {'singleUIAuthorization': access_header}, auth)
results.append(result)
refresh_header = refresh_headers.get('Single-UI-Refresh')
if not refresh_header:
    raise SystemExit(json.dumps({'status': 'FAILED', 'results': results}, indent=2))
refresh = refresh_header.split(' ', 1)[1]

result, extend_headers, _ = call('extend', '/v2/sso/extend', {'singleUIAuthorization': access_header}, auth)
results.append(result)

result, relogin_headers, _ = call('relogin', '/v2/sso/relogin', {}, {'Single-UI-Refresh': refresh_header})
results.append(result)

result, _, _ = call('logout', '/v2/sso/logout', {'singleUIAuthorization': access_header}, auth)
results.append(result)

result, _, _ = call('refresh_after_logout', '/v2/sso/refreshtoken', {'singleUIAuthorization': access_header}, auth)
results.append(result)

result, _, _ = call('extend_after_logout', '/v2/sso/extend', {'singleUIAuthorization': access_header}, auth)
results.append(result)

checks = {
    'bad_login_rejected': results[0]['status'] == 400 and results[0]['result'] is False,
    'login_issued_access': results[1]['status'] == 200 and bool(results[1].get('Single-UI-Authorization')),
    'refresh_issued_refresh': results[2]['status'] == 200 and bool(results[2].get('Single-UI-Refresh')),
    'extend_accepted': results[3]['status'] == 200 and results[3]['result'] is True,
    'relogin_accepted': results[4]['status'] == 200 and results[4]['result'] is True,
    'logout_accepted': results[5]['status'] == 200 and results[5]['result'] is True,
    'refresh_rejected_after_logout': results[6]['status'] == 401 and results[6]['result'] is False,
    'extend_rejected_after_logout': results[7]['status'] == 401 and results[7]['result'] is False,
}
output = {'status': 'PASSED' if all(checks.values()) else 'FAILED', 'base': BASE, 'results': results, 'checks': checks}
path = Path(__file__).with_name('smoke-result.json')
path.write_text(json.dumps(output, indent=2) + '\n')
print(json.dumps(output, indent=2))
if output['status'] != 'PASSED':
    raise SystemExit(1)
