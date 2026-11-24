"""Verify matrix identity extraction and bounded private HTTP acquisition."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import ssl
import tempfile
import threading
import unittest
from unittest.mock import patch
from xml.sax.saxutils import escape
from zipfile import ZipFile

from ai_sdlc_workbench.entitlement_sources import (
    JsonHttpClient, SourceError, load_root_env, read_http_example, read_matrix,
)


def matrix(path, users='0012; srv.one', extra_assignment=False):
    """Build the supported sparse Excel source format without Excel packages."""
    sheets = {
        "Application": {1: {"A": "ITAM_ID", "C": "APPNAME"}, 2: {"A": 123, "C": "APP"}},
        "Feature": {1: {"A": "FEATURENAME"}, 2: {"A": "FEATURE"}},
        "Entitlement": {1: {"A": "ENTITLEMENTNAME", "D": "APPLICATIONNAME"}, 2: {"A": "ROLE", "D": "APP"}},
        "EntitlementFeatureAction": {1: {"A": "ENTITLEMENTNAME", "B": "APPLICATIONNAME", "C": "FEATURENAME", "D": "ACTIONNAME"},
                                    2: {"A": "ROLE", "B": "APP", "C": "FEATURE", "D": "View"}},
        "UserEntitlement": {1: {"A": "USERNAME", "B": "ENTITLEMENTNAME", "E": "APPNAME"},
                            2: {"H": "PRESENT_IN"}, 3: {"A": users, "B": "ROLE", "E": "APP"}},
    }
    if extra_assignment:
        sheets["UserEntitlement"][4] = {"A": 9007199254740993, "B": "UNDEFINED", "E": "APP"}
    ns = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    rel = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    with ZipFile(path, 'w') as archive:
        archive.writestr('xl/workbook.xml', f'<workbook xmlns="{ns}" xmlns:r="{rel}"><sheets>' + ''.join(
            f'<sheet name="{name}" sheetId="{i}" r:id="rId{i}"/>' for i, name in enumerate(sheets, 1)) + '</sheets></workbook>')
        archive.writestr('xl/_rels/workbook.xml.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + ''.join(
            f'<Relationship Id="rId{i}" Target="worksheets/sheet{i}.xml"/>' for i in range(1, 6)) + '</Relationships>')
        archive.writestr('xl/sharedStrings.xml', f'<sst xmlns="{ns}"><si><r><t>RO</t></r><r><t>LE</t></r></si></sst>')
        for index, rows in enumerate(sheets.values(), 1):
            xml = []
            for row_num, cells in rows.items():
                values = []
                for column, value in cells.items():
                    ref = f'{column}{row_num}'
                    if value == 'ROLE':
                        values.append(f'<c r="{ref}" t="s"><v>0</v></c>')
                    elif isinstance(value, int):
                        values.append(f'<c r="{ref}"><v>{value}</v></c>')
                    else:
                        values.append(f'<c r="{ref}" t="inlineStr"><is><t>{escape(value)}</t></is></c>')
                xml.append(f'<row r="{row_num}">' + ''.join(values) + '</row>')
            archive.writestr(f'xl/worksheets/sheet{index}.xml', f'<worksheet xmlns="{ns}"><sheetData>' + ''.join(xml) + '</sheetData></worksheet>')


class MatrixSourceTests(unittest.TestCase):
    def test_shared_rich_inline_sparse_cells_and_multiple_identities(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'matrix.xlsx'
            matrix(path, users='0012; srv.one\n0034', extra_assignment=True)
            value = read_matrix(path)
        self.assertEqual(value['app'], 'APP')
        self.assertEqual(value['itam_id'], '123')
        self.assertEqual(value['users'], ['0012', '0034', '9007199254740993', 'srv.one'])
        self.assertEqual(value['grants'], [['APP', 'ROLE', 'FEATURE', 'View']])
        self.assertEqual(value['missing_profile_definitions'], [['APP', 'UNDEFINED']])
        self.assertEqual(value['missing_profile_grants'], [['APP', 'UNDEFINED']])

    def test_json_array_identity_cell_expands_without_losing_leading_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'matrix.xlsx'
            matrix(path, users='["0012", "srv.one", "0012"]')
            self.assertEqual(read_matrix(path)['users'], ['0012', 'srv.one'])

    def test_invalid_identity_array_fails_instead_of_becoming_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'matrix.xlsx'; matrix(path, users='[broken')
            with self.assertRaises(SourceError) as caught:
                read_matrix(path)
            self.assertEqual(caught.exception.code, 'INVALID_MATRIX_IDENTITIES')

    def test_collection_omits_credentials_and_preserves_explicit_empty_array(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'request.yml'
            path.write_text('''http:
  method: GET
  url: https://example.invalid/catalog
  headers:
    - name: Authorization
      value: Bearer PRIVATE_SENTINEL
examples:
  - request:
      url: https://example.invalid/catalog
    response:
      status: 200
      body:
        type: json
        data: '[]'
''')
            value = read_http_example(path)
        self.assertEqual(value['response'], [])
        self.assertNotIn('PRIVATE_SENTINEL', repr(value))
        self.assertNotIn('headers', value)

    def test_root_environment_respects_process_empty_override(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, '.env').write_text('export VALUE="file value"\nTOKEN=private\n')
            with patch.dict(os.environ, {'TOKEN': ''}, clear=True):
                value = load_root_env(directory)
        self.assertEqual(value['VALUE'], 'file value')
        self.assertEqual(value['TOKEN'], '')


class Handler(BaseHTTPRequestHandler):
    calls = []

    def do_GET(self):
        type(self).calls.append((self.path, self.headers.get('Authorization')))
        if self.path == '/401':
            self.send_response(401); self.end_headers(); self.wfile.write(b'PRIVATE_SERVER_BODY')
        elif self.path == '/redirect':
            self.send_response(302); self.send_header('Location', '/success'); self.end_headers()
        elif self.path == '/invalid':
            self.send_response(200); self.end_headers(); self.wfile.write(b'not JSON PRIVATE_SERVER_BODY')
        elif self.path == '/large':
            self.send_response(200); self.end_headers(); self.wfile.write(b'[' + b' ' * 1000 + b']')
        else:
            self.send_response(200); self.send_header('Content-Type', 'application/json'); self.end_headers()
            self.wfile.write(b'{"users": ["a", "b"]}')

    def log_message(self, *args):
        pass


class HttpSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True); cls.thread.start()
        cls.base = 'http://127.0.0.1:' + str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join()

    def setUp(self):
        Handler.calls = []

    def test_http_requires_explicit_loopback_exception(self):
        for url in (self.base, 'http://example.invalid/users'):
            with self.assertRaises(SourceError) as caught:
                JsonHttpClient({}, allow_http=False).request('GET', url)
            self.assertEqual(caught.exception.code, 'HTTPS_REQUIRED')
        with self.assertRaises(SourceError):
            JsonHttpClient({}, allow_http=True).request('GET', 'http://example.invalid/users')

    def test_success_retains_json_and_redacts_query_values(self):
        value = JsonHttpClient({'TOKEN': 'PRIVATE_SENTINEL'}, retries=0, allow_http=True).request(
            'GET', self.base + '/success?token=PRIVATE_QUERY', token_env='TOKEN')
        self.assertEqual(value['data'], {'users': ['a', 'b']})
        self.assertEqual(value['status'], 200)
        self.assertIn('token=REDACTED', value['url'])
        self.assertNotIn('PRIVATE', repr(value))
        self.assertEqual(Handler.calls[0][1], 'Bearer PRIVATE_SENTINEL')

    def test_401_never_becomes_empty_permissions_or_leaks_response(self):
        with self.assertRaises(SourceError) as caught:
            JsonHttpClient({}, retries=0, allow_http=True).request('GET', self.base + '/401')
        self.assertEqual(caught.exception.status, 401)
        self.assertEqual(caught.exception.code, 'HTTP_ERROR')
        self.assertNotIn('PRIVATE', str(caught.exception))

    def test_redirect_cannot_forward_a_credential(self):
        with self.assertRaises(SourceError) as caught:
            JsonHttpClient({'TOKEN': 'PRIVATE_SENTINEL'}, retries=0, allow_http=True).request(
                'GET', self.base + '/redirect', token_env='TOKEN')
        self.assertEqual(caught.exception.status, 302)
        self.assertEqual([path for path, _ in Handler.calls], ['/redirect'])

    def test_malformed_and_oversized_bodies_are_explicit_errors(self):
        client = JsonHttpClient({}, retries=0, allow_http=True, max_response_bytes=100)
        for path, code in (('/invalid', 'INVALID_JSON_RESPONSE'), ('/large', 'RESPONSE_TOO_LARGE')):
            with self.assertRaises(SourceError) as caught:
                client.request('GET', self.base + path)
            self.assertEqual(caught.exception.code, code)

    def test_default_tls_context_keeps_certificate_verification(self):
        factory = ssl.create_default_context
        created = []
        def create(**kwargs):
            context = factory(**kwargs)
            created.append(context)
            return context
        with patch('ai_sdlc_workbench.entitlement_sources.ssl.create_default_context', side_effect=create):
            JsonHttpClient({}, retries=0, allow_http=True).request('GET', self.base + '/success')
        self.assertEqual(len(created), 1)
        context = created[0]
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(context.check_hostname)

    def test_missing_credentials_prevent_acquisition(self):
        with self.assertRaises(SourceError) as caught:
            JsonHttpClient({}, retries=0, allow_http=True).request('GET', self.base, token_env='MISSING')
        self.assertEqual(caught.exception.code, 'MISSING_CREDENTIAL')
        self.assertEqual(Handler.calls, [])


if __name__ == '__main__':
    unittest.main()
