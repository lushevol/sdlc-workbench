"""Protect exact source-module joins, exported symbols, aliases, and limits."""
from copy import deepcopy
from pathlib import Path
import runpy
import tempfile
import unittest

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
Graph = load_tool('build_graph').Graph
add_to_graph = load_tool('extract_web_structure').add_to_graph


class WebStructureTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='web-structure-')
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.repo = self.workspace / 'repos' / 'ui'
        self.repo.mkdir(parents=True)
        self.graph = Graph(self.workspace)
        self.repository = self.graph.add_repository(self.repo, 'WEB', True)

    def write(self, path, source):
        destination = self.repo / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(source)
        return destination

    def edges(self, relationship):
        return [edge for edge in self.graph.edges.values() if edge['relationship'] == relationship]

    def nodes(self, kind):
        return [node for node in self.graph.nodes.values() if node.get('component_kind') == kind]

    def test_relative_barrels_default_and_named_exports_reuse_exact_component(self):
        provider = self.write('src/provider.ts', 'export const alpha = () => 1; export default function Main() { return alpha(); }')
        self.write('src/barrel/index.ts', 'export {alpha as renamed, default} from "../provider";')
        self.write('src/side.ts', 'console.log("loaded");')
        self.write('src/consumer.ts', 'import Main, {renamed as used} from "./barrel"; import * as helpers from "./barrel"; import "./side";')
        ev = self.graph.add_evidence(self.repository, provider.relative_to(self.workspace).as_posix(), 1,
                                     'Existing detail', 'fixture')
        self.graph.add_node('detail:provider', 'COMPONENT', 'Provider detail', self.repository,
                            dimensions=('RUNTIME',), component_kind='REACT_COMPONENT', functional_role='Fixture component',
                            business_meaning='Fixture component', source_paths=(provider.relative_to(self.workspace).as_posix(),), evidence=(ev,))
        self.graph.add_edge('detail:provider', 'detail:provider', 'USES_COMPONENT', 'RUNTIME', (ev,), assertion_status='INFERRED')
        before = deepcopy(self.edges('USES_COMPONENT'))
        result = add_to_graph(self.graph, self.repo, self.repository)
        self.assertEqual(self.edges('USES_COMPONENT'), before)
        self.assertEqual(len(self.edges('IMPORTS_SOURCE')), 3)  # Repeated imports merge by canonical endpoints.
        self.assertTrue(any(edge['target'] == 'detail:provider' for edge in self.edges('IMPORTS_SOURCE')))
        imported = [edge for edge in self.edges('IMPORTS_SYMBOL')
                    if self.graph.nodes[edge['source']]['source_paths'] == ['repos/ui/src/consumer.ts']]
        self.assertEqual({self.graph.nodes[edge['target']]['name'] for edge in imported}, {'alpha', 'Main'})
        for edge in imported:
            self.assertEqual(edge['resolution_status'], 'RESOLVED')
            self.assertEqual(edge['properties']['resolution_rule'], 'exact-exported-value-binding')
            self.assertGreaterEqual(len(edge['evidence']), 2)
        self.assertEqual(result['statistics']['resolved_source_imports'], 4)
        self.assertEqual(result['statistics']['exported_symbols'], 2)

    def test_jsonc_inherited_tsconfig_paths_and_base_url_resolve_exact_sources(self):
        self.write('config/base.json', '{ /* base aliases */ "compilerOptions": { "baseUrl": "..", "paths": {"@shared/*": ["src/shared/*"],}, }, }')
        self.write('tsconfig.json', '{"extends": "./config/base.json"}')
        self.write('src/shared/format/index.ts', 'export function format() { return "ok"; }')
        self.write('src/app.ts', 'import {format} from "@shared/format"; import {format as another} from "src/shared/format";')
        result = add_to_graph(self.graph, self.repo, self.repository)
        self.assertEqual(result['statistics']['resolved_source_imports'], 2)
        self.assertEqual(result['statistics']['resolved_symbol_imports'], 2)
        self.assertEqual(len(self.edges('IMPORTS_SYMBOL')), 1)
        self.assertEqual(set(self.edges('IMPORTS_SYMBOL')[0]['properties']['bindings']), {'format', 'another'})
        self.assertEqual(set(self.edges('IMPORTS_SOURCE')[0]['properties']['modules']), {'@shared/format', 'src/shared/format'})

    def test_ambiguous_paths_and_barrel_symbols_never_select_a_provider(self):
        self.write('src/dupe.ts', 'export const dupe = 1;')
        self.write('src/dupe.tsx', 'export const dupe = 2;')
        self.write('src/a.ts', 'export const value = 1;')
        self.write('src/b.ts', 'export const value = 2;')
        self.write('src/barrel.ts', 'export * from "./a"; export * from "./b";')
        self.write('src/app.ts', 'import {dupe} from "./dupe"; import {value, absent} from "./barrel";')
        result = add_to_graph(self.graph, self.repo, self.repository)
        codes = {item['code'] for item in self.graph.diagnostics.values()}
        self.assertIn('AMBIGUOUS_WEB_SOURCE_IMPORT', codes)
        self.assertIn('AMBIGUOUS_WEB_SYMBOL_IMPORT', codes)
        self.assertIn('UNRESOLVED_WEB_SYMBOL_IMPORT', codes)
        app_imports = [edge for edge in self.edges('IMPORTS_SOURCE')
                       if self.graph.nodes[edge['source']]['source_paths'] == ['repos/ui/src/app.ts']]
        self.assertEqual(len(app_imports), 1)
        self.assertEqual(self.graph.nodes[app_imports[0]['target']]['name'], 'barrel.ts')
        self.assertFalse(any(self.graph.nodes[edge['source']]['source_paths'] == ['repos/ui/src/app.ts']
                             for edge in self.edges('IMPORTS_SYMBOL')))
        self.assertTrue(any(row.get('reason') == 'AMBIGUOUS_WEB_SOURCE_IMPORT' and len(row['candidate_paths']) == 2
                            for row in result['ledger']))

    def test_type_only_imports_tests_declarations_and_packages_do_not_create_value_edges(self):
        self.write('src/provider.ts', 'export interface TypeOnly { name: string }; export const value = 1;')
        self.write('src/app.ts', 'import type {value as TypeValue} from "./provider"; import {type TypeOnly, value} from "./provider"; import React from "react";')
        self.write('src/app.test.ts', 'import {value} from "./provider";')
        self.write('src/types.d.ts', 'import {value} from "./provider";')
        self.write('tests/main.ts', 'import {value} from "../src/provider";')
        result = add_to_graph(self.graph, self.repo, self.repository)
        self.assertEqual(result['statistics']['source_files'], 2)
        self.assertEqual(len(self.edges('IMPORTS_SOURCE')), 1)
        self.assertEqual({node['name'] for node in self.nodes('EXPORTED_SYMBOL')}, {'value'})
        self.assertEqual(self.edges('IMPORTS_SYMBOL')[0]['properties']['symbols'], ['value'])
        reasons = {row.get('reason') for row in result['ledger']}
        self.assertIn('TYPE_ONLY_IMPORT', reasons)
        self.assertIn('PACKAGE_IMPORT_HANDLED_SEPARATELY', reasons)
        self.assertIn('TYPE_DECLARATION_OR_TEST', reasons)

    def test_reexported_local_import_bindings_and_cycles_keep_exact_identity(self):
        self.write('src/provider.ts', 'const inner = () => 1; export {inner as value};')
        self.write('src/wrapper.ts', 'import {value as local} from "./provider"; export {local as wrapped};')
        self.write('src/first.ts', 'export * from "./second";')
        self.write('src/second.ts', 'export * from "./first";')
        self.write('src/app.ts', 'import {wrapped} from "./wrapper"; import {missing} from "./first";')
        result = add_to_graph(self.graph, self.repo, self.repository)
        self.assertEqual({node['name'] for node in self.nodes('EXPORTED_SYMBOL')}, {'inner'})
        self.assertTrue(any(item.get('reason') == 'UNRESOLVED_WEB_SYMBOL_IMPORT' for item in result['ledger']))
        target = next(edge['target'] for edge in self.edges('IMPORTS_SYMBOL'))
        self.assertTrue(all(edge['target'] == target for edge in self.edges('IMPORTS_SYMBOL')))

    def test_outside_repository_sources_and_dynamic_specifiers_remain_unresolved(self):
        outside = self.workspace / 'repos' / 'outside.ts'
        outside.write_text('export const value = 1;')
        self.write('src/app.ts', 'import {value} from "../../outside"; import bad from "./target?secret=fixture";')
        result = add_to_graph(self.graph, self.repo, self.repository)
        self.assertFalse(self.edges('IMPORTS_SOURCE'))
        self.assertFalse(any('outside.ts' in node['source_paths'] for node in self.graph.nodes.values()))
        self.assertEqual(sum(row['disposition'] == 'UNRESOLVED' for row in result['ledger']), 2)
        retained = str(self.graph.diagnostics) + str(self.graph.evidence) + str(result['ledger'])
        self.assertNotIn('secret=fixture', retained)

    def test_dynamic_import_and_commonjs_syntax_are_visible_limits(self):
        self.write('src/provider.ts', 'export const value = 1;')
        self.write('src/app.ts', 'const lazy = import("./provider"); const old = require("./provider");')
        result = add_to_graph(self.graph, self.repo, self.repository)
        self.assertFalse(self.edges('IMPORTS_SOURCE'))
        self.assertEqual({row['reason'] for row in result['ledger'] if row['disposition'] == 'UNRESOLVED'},
                         {'DYNAMIC_IMPORT_SYNTAX', 'COMMONJS_REQUIRE_SYNTAX'})

    def test_exact_type_only_exports_do_not_become_runtime_imports(self):
        self.write('src/types.ts', 'export interface User { name: string }; export type Identifier = string;')
        self.write('src/barrel.ts', 'export {User} from "./types"; export type {Identifier} from "./types";')
        self.write('src/app.ts', 'import {User, Identifier} from "./barrel";')
        result = add_to_graph(self.graph, self.repo, self.repository)
        self.assertFalse(self.edges('IMPORTS_SOURCE'))
        self.assertFalse(self.edges('IMPORTS_SYMBOL'))
        self.assertFalse(self.nodes('EXPORTED_SYMBOL'))
        self.assertTrue(any(row.get('reason') == 'TYPE_ONLY_EXPORTED_BINDINGS' for row in result['ledger']))
        self.assertFalse(any(item['code'] == 'UNRESOLVED_WEB_SYMBOL_IMPORT' for item in self.graph.diagnostics.values()))


if __name__ == '__main__':
    unittest.main()
