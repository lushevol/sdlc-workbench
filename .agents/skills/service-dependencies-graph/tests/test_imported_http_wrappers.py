"""Imported HTTP wrappers retain inspected transport and URL evidence."""
import json
from pathlib import Path
import runpy
import tempfile
import unittest

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
web = load_tool('extract_web_interfaces')


class ImportedHttpWrapperTests(unittest.TestCase):
    def fixture(self, directory, *, helper=None, client=None, wrapper=None):
        workspace = Path(directory)
        repository = workspace / 'repos/web'
        repository.mkdir(parents=True)
        (repository / 'client.ts').write_text(client or '''import transport from "axios";
const service = transport.create({headers: {Authorization: "DO_NOT_RETAIN_SECRET"}});
export default service;''')
        (repository / 'endpoint.ts').write_text(helper or '''export const getEndpoint = (path: string) => {
return `/api${path}`;
};''')
        (repository / 'wrapper.ts').write_text(wrapper or '''import service from "./client";
import {getEndpoint} from "./endpoint";
const send = <T = unknown>(path: string, data: T) => {
return service.post<T>(getEndpoint(path), data);
};
export {send as postService};''')
        return workspace, repository

    def extract(self, workspace, repository, content):
        source = repository / 'consumer.ts'
        source.write_text(content)
        binding = web.static_http_imports(source, content, repository, workspace)
        return binding, web.extract_interfaces(content, external_http_bindings=binding)

    def test_named_alias_wrapper_composes_prefix_with_supporting_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace, repository = self.fixture(directory)
            binding, result = self.extract(workspace, repository, '''import {postService as send} from "./wrapper";
send("/auth/v2/sso/login?token=DO_NOT_RETAIN_QUERY", {password: "DO_NOT_RETAIN_PASSWORD"});''')
            operation, = result['operations']
            self.assertEqual((operation['method'], operation['path']),
                             ('POST', '/api/auth/v2/sso/login?token=%7Bvalue%7D'))
            self.assertEqual(operation['assertion_status'], 'CONFIRMED')
            self.assertEqual({row['path'] for row in operation['supporting_evidence']}, {
                'repos/web/consumer.ts', 'repos/web/wrapper.ts', 'repos/web/client.ts', 'repos/web/endpoint.ts'})
            self.assertNotIn('DO_NOT_RETAIN', json.dumps((binding, result)))

    def test_imported_client_with_prefix_helper_handles_direct_typed_call(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace, repository = self.fixture(directory)
            _, result = self.extract(workspace, repository, '''import service from "./client";
import {getEndpoint as endpoint} from "./endpoint";
service.post<Response>(endpoint("/auth/v2/sso/refreshtoken"), {});''')
            operation, = result['operations']
            self.assertEqual(operation['path'], '/api/auth/v2/sso/refreshtoken')
            self.assertEqual(operation['method'], 'POST')
            self.assertEqual(len(operation['supporting_evidence']), 5)

    def test_literal_base_url_keeps_external_authority_and_base_path(self):
        for consumer in ('''import {postService} from "./wrapper";
postService("/auth/v2/sso/login", {});''', '''import service from "./client";
import {getEndpoint} from "./endpoint";
service.post(getEndpoint("/auth/v2/sso/login"), {});'''):
            with self.subTest(consumer=consumer), tempfile.TemporaryDirectory() as directory:
                workspace, repository = self.fixture(directory, client='''import axios from "axios";
const service = axios.create({baseURL: "https://outside.example/backend/"});
export default service;''')
                _, result = self.extract(workspace, repository, consumer)
                operation, = result['operations']
                self.assertEqual(operation['path'], 'https://outside.example/backend/api/auth/v2/sso/login')
                self.assertEqual(operation['assertion_status'], 'CONFIRMED')

    def test_absolute_request_authority_overrides_literal_base_url(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace, repository = self.fixture(directory, client='''import axios from "axios";
const service = axios.create({baseURL: "https://base.example"});
export default service;''', wrapper='''import service from "./client";
export const postService = (path: string, data: unknown) => service.post(path, data);''')
            _, result = self.extract(workspace, repository, '''import {postService} from "./wrapper";
postService("https://outside.example/token", {});''')
            operation, = result['operations']
            self.assertEqual(operation['path'], 'https://outside.example/token')

    def test_unknown_client_routing_retains_diagnostics_without_provider_join_inputs(self):
        clients = [
            'const service = axios.create(runtimeConfig);',
            'const service = axios.create({...runtimeConfig});',
            'const service = axios.create({baseURL: runtimeBaseURL});',
            'const service = axios.create({adapter: customAdapter});',
            'const service = axios.create({baseURL: "https://user:DO_NOT_RETAIN@outside.example"});',
            'const config = {}; const service = axios.create(config); config.baseURL = runtimeBaseURL;',
            'const config = {}; config.baseURL = runtimeBaseURL; const service = axios.create(config);',
            'const config = {}; const other = config; other.baseURL = runtimeBaseURL; const service = axios.create(config);',
            'const service = axios.create({}); service.defaults.baseURL = runtimeBaseURL;',
            'const service = axios.create({}); const alias = service; alias.defaults.baseURL = runtimeBaseURL;',
            'const service = axios.create({}); configureClient(service);',
            'const service = axios.create({}); service.interceptors.request.use(runtimeHandler);',
            'const service = axios.create({}); service.interceptors.request.use(request => {request.url = "/other"; return request;});',
            'const service = axios.create({}); service.interceptors.request.use(request => {request.method = "GET"; return request;});',
            'const service = axios.create({}); service.interceptors.request.use(request => {const alias = request; alias.url = "/other"; return request;});',
            'const service = axios.create({}); service.interceptors.request.use(request => {changeRequest(request); return request;});',
        ]
        for client in clients:
            with self.subTest(client=client), tempfile.TemporaryDirectory() as directory:
                workspace, repository = self.fixture(directory, client='import axios from "axios"; ' + client + '\nexport default service;')
                binding, result = self.extract(workspace, repository, '''import {postService} from "./wrapper";
postService("/auth/v2/sso/login", {});''')
                self.assertTrue(binding['wrappers']['postService']['routing_limit'])
                self.assertEqual(result['operations'], [])
                self.assertIn('UNRESOLVED_WEB_CLIENT_ROUTING', {row['code'] for row in result['diagnostics']})
                self.assertNotIn('DO_NOT_RETAIN', json.dumps((binding, result)))

    def test_imported_header_interceptor_retains_inspected_source_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace, repository = self.fixture(directory, client='''import axios from "axios";
import {requestHandler} from "./request.handler";
const config = {headers: {Accept: "application/json"}, timeout: 60000};
const service = axios.create(config);
service.interceptors.request.use(requestHandler);
export default service;''')
            handler = repository / 'request.handler.ts'
            handler.write_text('''export const requestHandler = (request: any) => {
if (request.url?.includes("/auth/")) { request.headers["Authorization"] = "DO_NOT_RETAIN_SECRET"; }
notifyLoading({loading: true});
return request;
};''')
            binding, result = self.extract(workspace, repository, '''import {postService} from "./wrapper";
postService("/auth/v2/sso/login", {});''')
            operation, = result['operations']
            self.assertEqual(operation['path'], '/api/auth/v2/sso/login')
            self.assertFalse(binding['wrappers']['postService'].get('routing_limit'))
            self.assertTrue(any(row['path'] == 'repos/web/request.handler.ts' and row['line'] == 1
                                for row in operation['supporting_evidence']))
            self.assertNotIn('DO_NOT_RETAIN', json.dumps((binding, result)))
            handler.write_text('''export const requestHandler = (request: any) => {
request.baseURL = "https://outside.example"; return request;
};''')
            _, result = self.extract(workspace, repository, '''import {postService} from "./wrapper";
postService("/auth/v2/sso/login", {});''')
            self.assertEqual(result['operations'], [])
            self.assertIn('UNRESOLVED_WEB_CLIENT_ROUTING', {row['code'] for row in result['diagnostics']})

    def test_request_configuration_overrides_and_unknown_configuration_are_distinct(self):
        consumers = [
            ('{baseURL: "https://outside.example"}', 'https://outside.example/api/auth/v2/sso/login'),
            ('{headers: {Accept: "application/json"}}', '/api/auth/v2/sso/login'),
            ('runtimeConfig', None),
            ('{...runtimeConfig}', None),
            ('{[runtimeField]: "https://outside.example"}', None),
            ('{baseURL: runtimeBaseURL}', None),
        ]
        for config, expected in consumers:
            for direct in (False, True):
                with self.subTest(config=config, direct=direct), tempfile.TemporaryDirectory() as directory:
                    workspace, repository = self.fixture(directory, wrapper='''import service from "./client";
import {getEndpoint} from "./endpoint";
export const postService = (path: string, data: unknown, config?: unknown) => service.post(getEndpoint(path), data, config);''')
                    consumer = (f'''import service from "./client";
service.post("/api/auth/v2/sso/login", {{}}, {config});''' if direct else f'''import {{postService}} from "./wrapper";
postService("/auth/v2/sso/login", {{}}, {config});''')
                    _, result = self.extract(workspace, repository, consumer)
                    if expected is None:
                        self.assertEqual(result['operations'], [])
                        self.assertIn('UNRESOLVED_WEB_CLIENT_ROUTING', {row['code'] for row in result['diagnostics']})
                    else:
                        operation, = result['operations']
                        self.assertEqual(operation['path'], expected)

    def test_dynamic_helper_and_uninspected_client_do_not_invent_routes(self):
        for change in ({'helper': '''export const getEndpoint = (path: string) => {
return `${runtimePrefix}${path}`;
};'''}, {'client': '''const service = new Map(); export default service;'''}):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as directory:
                workspace, repository = self.fixture(directory, **change)
                binding, result = self.extract(workspace, repository, '''import {postService} from "./wrapper";
postService("/auth/v2/sso/login", {});''')
                self.assertEqual(binding['wrappers'], {})
                self.assertEqual(result['operations'], [])

    def test_conditional_wrapper_cannot_establish_single_forwarding_method(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace, repository = self.fixture(directory, wrapper='''import service from "./client";
export const postService = (path: string, data: unknown) => {
if (flag) return service.post(path, data);
return service.get(path);
};''')
            binding, result = self.extract(workspace, repository, '''import {postService} from "./wrapper";
postService("/auth/v2/sso/login", {});''')
            self.assertEqual(binding['wrappers'], {})
            self.assertEqual(result['operations'], [])

    def test_parameter_shadowing_does_not_reuse_imported_wrapper(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace, repository = self.fixture(directory)
            _, result = self.extract(workspace, repository, '''import {postService} from "./wrapper";
postService("/auth/v2/sso/login", {});
function example(postService: (path: string) => unknown) {
postService("/unrelated");
}''')
            self.assertEqual([(row['method'], row['path']) for row in result['operations']],
                             [('POST', '/api/auth/v2/sso/login')])

    def test_wrapper_parameters_cannot_impersonate_imported_client_or_helper(self):
        for extra in ('service', 'getEndpoint'):
            with self.subTest(extra=extra), tempfile.TemporaryDirectory() as directory:
                workspace, repository = self.fixture(directory, wrapper='''import service from "./client";
import {getEndpoint} from "./endpoint";
export const postService = (path: string, ''' + extra + ''': unknown) => {
return service.post(getEndpoint(path));
};''')
                binding, result = self.extract(workspace, repository, '''import {postService} from "./wrapper";
postService("/auth/v2/sso/login", {});''')
                self.assertEqual(binding['wrappers'], {})
                self.assertEqual(result['operations'], [])

    def test_type_only_import_and_ambiguous_module_are_not_bindings(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace, repository = self.fixture(directory)
            binding, result = self.extract(workspace, repository, '''import type {postService} from "./wrapper";
postService("/auth/v2/sso/login", {});''')
            self.assertEqual(binding['wrappers'], {})
            self.assertEqual(result['operations'], [])
            (repository / 'wrapper.tsx').write_text((repository / 'wrapper.ts').read_text())
            binding, _ = self.extract(workspace, repository, '''import {postService} from "./wrapper";''')
            self.assertEqual(binding['wrappers'], {})


if __name__ == '__main__':
    unittest.main()
