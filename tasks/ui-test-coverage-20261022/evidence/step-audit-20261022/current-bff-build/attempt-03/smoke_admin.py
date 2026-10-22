from __future__ import annotations
import base64, hashlib, json, time
from pathlib import Path
from urllib import request, error

BASE = 'http://127.0.0.1:8090/api/auth'
USER = 'user-a'
PASSWORD = 'FixturePass1!'


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


results=[]
def record(name,path,body,headers):
 result,response_headers,payload=call(name,path,body,headers)
 result['data']=payload.get('data');results.append(result)
 return response_headers,payload
headers,login=record('login','/v2/sso/login',{'username':'UI-ADMIN-01','password':PASSWORD},{})
access=headers.get('Single-UI-Authorization');auth={'Single-UI-Authorization':access}
record('create_session','/v2/sso/refreshtoken',{'singleUIAuthorization':access},auth)
ent=login['entitlementsToken']
_,created=record('category_create','/v1/fmo/admin/category/create',{'label':'Current BFF smoke','entitlementsToken':ent},auth)
if created.get('data'):
 id=created['data']['applicationCategoryId']
 record('category_update','/v1/fmo/admin/category/update',{'applicationCategoryId':id,'label':'Updated current BFF smoke','orderNo':7,'mode':'maker','entitlementsToken':ent},auth)
 record('category_list','/v1/fmo/admin/category/data',{'entitlementsToken':ent},auth)
 record('category_audit','/v1/fmo/admin/category/audit',{'applicationCategoryId':id,'entitlementsToken':ent},auth)
checks={'all_requests_accepted':all(x['status']==200 and x['result'] is True for x in results),'create_and_list_audit_executed':len(results)==6}
output={'status':'PASSED' if all(checks.values()) else 'FAILED','source_revision':'834b4155232222347220e47139a502ee43a9cbdf','checks':checks,'results':results,'limits':['Synthetic OUD and EMS2 identities','H2 PostgreSQL mode, not PostgreSQL','Selected exact business source, isolated Spring Boot3 bootstrap, production Boot4 wiring not measured']}
Path(__file__).with_name('smoke-admin-result.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
