from __future__ import annotations
import base64, hashlib, json, time
from pathlib import Path
from urllib import request, error

BASE = 'http://127.0.0.1:8089/api/auth'
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
result, login_headers, _ = call('login', '/v2/sso/login', {'username': USER, 'password': PASSWORD})
results.append(result)
access_header=login_headers.get('Single-UI-Authorization')
assert access_header
result, fixtures, _ = call('issue_expired_fixture', '/local/fixture/expired-access', {'singleUIAuthorization': access_header})
results.append(result)
expired=fixtures.get('Single-UI-Authorization'); refresh=fixtures.get('Single-UI-Refresh')
assert expired and refresh
result, _, _ = call('refresh_with_expired_access', '/v2/sso/refreshtoken', {'singleUIAuthorization': expired})
results.append(result)
result, _, _ = call('extend_with_expired_access', '/v2/sso/extend', {'singleUIAuthorization': expired})
results.append(result)
result, _, _ = call('relogin_with_valid_refresh', '/v2/sso/relogin', {}, {'Single-UI-Refresh': refresh})
results.append(result)
checks={
 'expired_fixture_past_exp':results[1]['Single-UI-Authorization']['claims']['exp'] < time.time(),
 'refresh_rejected_with_expired_access':results[2]['status']==401 and 'TOKEN_INVALID_EXPIRED' in results[2]['errorMessage'],
 'extend_rejected_with_expired_access':results[3]['status']==401 and 'TOKEN_INVALID_EXPIRED' in results[3]['errorMessage'],
 'valid_refresh_accepted_for_relogin':results[4]['status']==200 and results[4]['result'] is True,
}
output={'status':'PASSED' if all(checks.values()) else 'FAILED','base':BASE,
 'fixture_limit':'Access expiry was explicitly set one minute in the past. Normal controller timeouts remain15/225/60 minutes.',
 'results':results,'checks':checks}
Path(__file__).with_name('expired-result.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
if output['status']!='PASSED':raise SystemExit(1)
