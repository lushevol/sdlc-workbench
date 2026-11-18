"""Discover Single-SPA composition from source without architecture instructions."""
import json
from pathlib import Path
import runpy
import tempfile
import unittest

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
builder = load_tool('build_graph')
extractor = load_tool('extract_single_spa_layout')
resolver = load_tool('resolve_repository_relationships')


SOURCE = '''import {registerApplication as register} from "single-spa";
import {constructRoutes as makeRoutes, constructApplications as makeApps} from "single-spa-layout";
import layout from "./layout.html";
const root = () => {
  const routes = makeRoutes(layout);
  const applications = makeApps({routes, loadApp({name}) { return System.import(name); }});
  applications.forEach(app => {
    app.customProps = {publicUrl: "/"};
    register(app);
  });
};
root();
'''


class SingleSpaLayoutTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / 'repos/ui/entry'
        (self.repo / 'src').mkdir(parents=True)
        (self.repo / 'package.json').write_text(json.dumps({'name': '@example/entry'}))
        self.source = self.repo / 'src/root.ts'
        self.source.write_text(SOURCE)
        self.layout = self.repo / 'src/layout.html'
        self.layout.write_text('<single-spa-router>\n<route default>\n<application name="@example/shell"></application>\n</route>\n</single-spa-router>')

    def graph(self, providers=('@example/shell',)):
        graph = builder.Graph(self.root)
        for name, package in [('entry', '@example/entry'), *[(f'provider-{index}', package) for index, package in enumerate(providers)]]:
            repo = self.root / 'repos/ui' / name
            repo.mkdir(parents=True, exist_ok=True)
            (repo / 'package.json').write_text(json.dumps({'name': package}))
            repository = graph.add_repository(repo, 'WEB', True)
            builder.extract_web(graph, repo, repository, True)
        extractor.add_to_graph(graph, self.repo, 'repo:entry')
        resolver.resolve(graph)
        return graph

    def test_seedless_layout_registration_resolves_exact_package_with_all_source_evidence(self):
        graph = self.graph()
        edge = next(row for row in graph.edges.values() if row['source'] == 'application:entry'
                    and row['target'] == 'application:provider-0' and row['relationship'] == 'LOADS_REMOTE')
        self.assertEqual(edge['resolution_status'], 'RESOLVED')
        self.assertEqual(edge['properties']['resolution_rule'], 'declared-module-identity')
        sources = [graph.evidence[key] for key in edge['evidence']]
        self.assertTrue(any(row['path'].endswith('layout.html') and row['line'] == 3 for row in sources))
        self.assertTrue(any(row['path'].endswith('provider-0/package.json') for row in sources))
        self.assertEqual({row['line'] for row in sources if row['extractor'] == 'single-spa-layout' and row['path'].endswith('root.ts')}, {5, 6, 9})

    def test_unknown_and_duplicate_packages_remain_unresolved_or_ambiguous(self):
        graph = self.graph(providers=())
        edge = next(row for row in graph.edges.values() if row['relationship'] == 'LOADS_REMOTE')
        self.assertEqual(edge['resolution_status'], 'UNRESOLVED')
        graph = self.graph(providers=('@example/shell', '@example/shell'))
        edge = next(row for row in graph.edges.values() if row['relationship'] == 'LOADS_REMOTE')
        self.assertEqual(edge['resolution_status'], 'AMBIGUOUS')
        self.assertFalse(any(row['target'].startswith('application:provider') for row in graph.edges.values()
                             if row['relationship'] == 'LOADS_REMOTE'))

    def test_layout_names_require_proven_loading_and_registration(self):
        cases = [SOURCE.replace('System.import(name)', 'otherLoader(name)'),
                 SOURCE.replace('register(app);', 'otherRegistration(app);'),
                 SOURCE.replace('makeRoutes(layout)', 'makeRoutes(runtimeLayout)'),
                 SOURCE.replace('  const routes = makeRoutes(layout);', '  const other = () => { const routes = makeRoutes(layout); };'),
                 SOURCE.replace('makeRoutes(layout)', 'makeRoutes(layout)').replace('register(app);', 'app.name = "@example/other"; register(app);'),
                 SOURCE.replace('const root = () => {', 'const root = (makeRoutes) => {'),
                 SOURCE.replace('const root = () => {', 'const System = customLoader; const root = () => {')]
        for source in cases:
            with self.subTest(source=source):
                self.source.write_text(source)
                result = extractor.extract(self.repo)
                self.assertEqual(result['registrations'], [])

    def test_dynamic_names_comments_and_unbound_html_do_not_create_dependencies(self):
        self.layout.write_text('''<application name="@example/outside"></application>
<single-spa-router>
<!-- <application name="@example/comment"></application> -->
<application name="${runtimeModule}"></application>
<application name="@example/shell" />
</single-spa-router>''')
        result = extractor.extract(self.repo)
        self.assertEqual([row['module'] for row in result['registrations']], ['@example/shell'])
        self.assertEqual(result['diagnostics'][0]['code'], 'UNRESOLVED_SINGLE_SPA_LAYOUT')

    def test_escaping_layout_and_unrelated_framework_names_cannot_create_dependencies(self):
        (self.root / 'outside.html').write_text('<single-spa-router><application name="@example/shell" /></single-spa-router>')
        self.source.write_text(SOURCE.replace('./layout.html', '../../../../outside.html'))
        self.assertEqual(extractor.extract(self.repo)['registrations'], [])
        self.source.write_text(SOURCE.replace('"single-spa-layout"', '"custom-layout"'))
        self.assertEqual(extractor.extract(self.repo)['registrations'], [])

    def test_direct_foreach_registration_and_explicit_routes_property_are_supported(self):
        self.source.write_text(SOURCE.replace('{routes, loadApp', '{routes: routes, loadApp').replace('applications.forEach(app => {\n    app.customProps = {publicUrl: "/"};\n    register(app);\n  });', 'applications.forEach(register);'))
        self.assertEqual([row['module'] for row in extractor.extract(self.repo)['registrations']], ['@example/shell'])

    def test_catch_destructuring_and_assignment_shadows_do_not_bind_framework_calls(self):
        cases = [SOURCE.replace('const root = () => {', 'const root = () => { try {} catch (register) {').replace('\n};', '\n}};'),
                 SOURCE.replace('const root = () => {', 'const root = () => { try {} catch (System) {').replace('\n};', '\n}};'),
                 SOURCE.replace('const root = () => {', 'const root = () => { const {register} = custom;'),
                 SOURCE.replace('  const routes', '  System = custom;\n  const routes'),
                 SOURCE.replace('  const routes', '  System["im" + "port"] = custom;\n  const routes'),
                 SOURCE.replace('  const routes', '  Object.assign(System, {import: custom});\n  const routes'),
                 SOURCE.replace('  const routes', '  register = custom;\n  const routes')]
        for source in cases:
            with self.subTest(source=source):
                self.source.write_text(source)
                result = extractor.extract(self.repo)
                self.assertEqual(result['registrations'], [])
                self.assertTrue(any(row['code'] == 'UNRESOLVED_SINGLE_SPA_LAYOUT' for row in result['diagnostics']))

    def test_unknown_application_mutations_and_escapes_stay_unresolved(self):
        mutations = ['app["na" + "me"] = "@example/other";',
                     'Object.assign(app, {name: "@example/other"});',
                     'changeApplication(app);', 'const alias = app; alias.name = "@example/other";',
                     'app.setName("@example/other");', 'delete app.name;',
                     'app.loadApp = other;', 'Reflect.set(app, "name", "@example/other");']
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.source.write_text(SOURCE.replace('    register(app);', '    ' + mutation + '\n    register(app);'))
                result = extractor.extract(self.repo)
                self.assertEqual(result['registrations'], [])
                self.assertTrue(result['diagnostics'])

    def test_route_and_application_collection_mutations_or_aliases_stay_unresolved(self):
        mutations = ['routes = custom;', 'routes["na" + "me"] = custom;', 'routes.push(custom);',
                     'Object.assign(routes, custom);', 'const alias = routes;',
                     'applications.splice(0);', 'Object.assign(applications, custom);', 'const alias = applications;']
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.source.write_text(SOURCE.replace('  applications.forEach', '  ' + mutation + '\n  applications.forEach'))
                result = extractor.extract(self.repo)
                self.assertEqual(result['registrations'], [])
                self.assertTrue(result['diagnostics'])

    def test_options_spread_computed_and_unknown_loader_overrides_stay_unresolved(self):
        overrides = ['...runtimeOptions', '["load" + "App"]: otherLoader',
                     '[runtimeKey]: runtimeValue', '"load\\u0041pp": otherLoader', 'loadApp',
                     '["load" + "App"]({name}) { return otherLoader(name); }',
                     '"load\\u0041pp"({name}) { return otherLoader(name); }',
                     'get routes() { return runtimeRoutes; }',
                     'routes() { return runtimeRoutes; }',
                     'set routes(value) { runtimeRoutes = value; }',
                     'set loadApp({name}) { return System.import(name); }',
                     '*loadApp({name}) { return System.import(name); }',
                     'loadApp: function*({name}) { return System.import(name); }']
        for override in overrides:
            with self.subTest(override=override):
                self.source.write_text(SOURCE.replace('return System.import(name); }});',
                                                      'return System.import(name); }, ' + override + '});'))
                result = extractor.extract(self.repo)
                self.assertEqual(result['registrations'], [])
                self.assertTrue(any(row['code'] == 'UNRESOLVED_SINGLE_SPA_LAYOUT' for row in result['diagnostics']))


if __name__ == '__main__':
    unittest.main()
