"""Seed an eligible local catalog and retain an exact-current BFF positive control.

Run only while holding the isolated PostgreSQL mutation window.
No raw access or entitlement token is retained.
"""
from pathlib import Path
from urllib import request
import datetime
import hashlib
import json

ROOT = Path(__file__).resolve().parent
BASE = 'http://127.0.0.1:8090/api/auth'
REVISION = '834b4155232222347220e47139a502ee43a9cbdf'


def post(operation, body):
    req = request.Request(BASE + operation, data=json.dumps(body).encode(), method='POST',
                          headers={'Content-Type': 'application/json'})
    with request.urlopen(req, timeout=15) as response:
        return response.status, dict(response.headers.items()), json.load(response)


common = dict(ems2Role='FMO_ADMIN', active=True, createdAt='2026-10-22T00:00:00Z',
              updatedAt='2026-10-22T00:00:00Z', createdBy='admin-a', updatedBy='admin-a', orderNo=1)
catalog = {
    'categories': [dict(common, applicationCategoryId=1, label='Fixture Auth')],
    'importMaps': [dict(common, importMapId=1, keyName='base', path='http://localhost:8122/base.js')],
    'tiles': [dict(common, applicationTileId=1, title='Fixture Eligible Portal', subtitle='',
                   ems2Entities='FMO PORTAL ADMIN', ems2Subject='', module='admin', tile='category',
                   entryName='Global', filterRule=None, template=True, imageLightTheme='', imageDarkTheme='',
                   emailSupport='support@example.test', applicationCategory={'applicationCategoryId': 1},
                   importMap={'importMapId': 1})],
}
reset_status, _, reset_body = post('/local/fixture/reset', {})
seed_status, _, seed_body = post('/local/fixture/seed', catalog)
login_status, headers, body = post('/v2/sso/login', {'username': 'user-a', 'password': 'FixturePass1!'})
access = next((value for key, value in headers.items() if key.lower() == 'single-ui-authorization'), None)
entitlement = body.get('entitlementsToken')
drawers = body.get('drawers', [])
checks = {
    'resetAccepted': reset_status == 200 and reset_body.get('reset') is True,
    'seedAccepted': seed_status == 200 and seed_body.get('seeded') is True,
    'actualLoginAccepted': login_status == 200 and body.get('result') is True,
    'accessIssued': bool(access),
    'eligibleDrawerPresent': any(tile.get('title') == 'Fixture Eligible Portal'
                                 for drawer in drawers for tile in drawer.get('tiles', [])),
}
result = {
    'recordedAt': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'PASSED' if all(checks.values()) else 'FAILED',
    'sourceRevision': REVISION,
    'checks': checks,
    'catalog': catalog,
    'login': {'httpStatus': login_status, 'result': body.get('result'),
              'entities': body.get('entities'), 'drawers': drawers,
              'accessSha256': hashlib.sha256(access.encode()).hexdigest() if access else None,
              'entitlementSha256': hashlib.sha256(entitlement.encode()).hexdigest() if entitlement else None},
    'limits': ['Synthetic local OUD identity and default controlled EMS2 entity.',
               'Exact current BFF catalog filtering and actual JPA on isolated PostgreSQL.',
               'Isolated Spring Boot3 bootstrap; production Boot4 wiring remains unverified.',
               'API positive control only. Canonical UI assertions run separately.'],
}
output = ROOT / 'auth-local-eligible-control.json'
output.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'checks': checks, 'evidence': str(output)}, indent=2))
if result['status'] != 'PASSED':
    raise SystemExit(1)
