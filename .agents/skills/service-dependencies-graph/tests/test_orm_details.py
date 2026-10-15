"""Check ORM mapping identities and source-backed SQL column references."""
from pathlib import Path
import runpy
import tempfile
import unittest

load_tool = runpy.run_path(str(Path(__file__).with_name('_support.py')))['load_tool']
orm = load_tool('extract_orm_details')
Graph = load_tool('build_graph').Graph


class OrmDetailsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.repo = self.workspace / 'repos/service'
        self.repo.mkdir(parents=True)

    def write(self, path, content):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')

    def entity(self, name='Order', annotation='@Table(name="orders", schema="sales")', package='example', fields=None):
        self.write('src/main/java/' + package.replace('.', '/') + '/' + name + '.java',
                   f'package {package}; import jakarta.persistence.*;\n@Entity {annotation} class {name} {{\n' +
                   (fields or '@Column(name="order_id") Long id; @Column(nullable=false) String label;') + '\n}')

    def repository(self, body=''):
        self.write('src/main/java/example/OrderRepo.java', '''package example;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
interface OrderRepo extends JpaRepository<Order, Long> {
''' + body + '\n}')

    def test_explicit_and_logical_columns_keep_schema_and_repository_evidence(self):
        self.entity()
        self.repository('Order findByLabel(String label);')
        graph = Graph(self.workspace)
        stats = orm.add_to_graph(graph, self.repo, 'repo:service', {})
        self.assertEqual(stats['entities'], 1)
        self.assertEqual(stats['column_mappings'], 2)
        self.assertEqual(stats['repositories'], 1)
        nodes = list(graph.nodes.values())
        table = next(n for n in nodes if n['type'] == 'TABLE')
        self.assertEqual(table['properties']['schema'], 'sales')
        self.assertEqual(table['properties']['physical_name'], 'orders')
        columns = [n for n in nodes if n['type'] == 'COLUMN']
        self.assertEqual({n['name'] for n in columns}, {'order_id', 'label'})
        self.assertIsNone(next(n for n in columns if n['name'] == 'label')['properties']['physical_name'])
        edges = list(graph.edges.values())
        self.assertFalse({'READS', 'WRITES'} & {e['relationship'] for e in edges})
        binding = next(e for e in edges if e['relationship'] == 'USES_ENTITY')
        self.assertEqual(binding['properties']['declared_operations'], ['findByLabel'])
        self.assertEqual(len(binding['evidence']), 2)
        evidence = list(graph.evidence.values())
        self.assertTrue(any(e['declaration'] == '@Column(name="order_id")' and e['line'] == 3 for e in evidence))

    def test_schema_only_mapping_retains_logical_identity_and_static_import_constant(self):
        self.write('src/main/java/example/Names.java', 'package example; class Names { public static final String SCHEMA = "sales"; }')
        self.write('src/main/java/example/Order.java', '''package example;
import jakarta.persistence.*;
import static example.Names.SCHEMA;
@Entity @Table(schema=SCHEMA) class Order { @Column(name="order_id") Long id; }
''')
        result = orm.extract(self.repo)
        self.assertEqual(result['entities'][0]['schema'], 'sales')
        self.assertIsNone(result['entities'][0]['table'])
        graph = Graph(self.workspace)
        orm.add_to_graph(graph, self.repo, 'repo:service', {})
        table = next(n for n in graph.nodes.values() if n['type'] == 'TABLE')
        self.assertEqual(table['name'], 'example.Order')
        self.assertNotEqual(table['name'], 'order')
        self.assertIsNone(table['properties']['physical_name'])
        edge = next(e for e in graph.edges.values() if e['relationship'] == 'MAPS_TO_TABLE')
        self.assertEqual(edge['resolution_status'], 'UNRESOLVED')

    def test_dynamic_and_ambiguous_constants_are_unresolved(self):
        self.write('src/main/java/a/Names.java', 'package a; public interface Names { String TABLE="first"; }')
        self.write('src/main/java/b/Names.java', 'package b; public interface Names { String TABLE="second"; }')
        self.write('src/main/java/example/Order.java', '''package example; import jakarta.persistence.*;
import static a.Names.*; import static b.Names.*;
@Entity @Table(name=TABLE, schema=System.getenv("SCHEMA")) class Order {
@Column(name=System.getenv("COLUMN")) Long id;
}''')
        result = orm.extract(self.repo)
        self.assertIsNone(result['entities'][0]['table'])
        self.assertIsNone(result['entities'][0]['schema'])
        self.assertIsNone(result['entities'][0]['columns'][0]['name'])
        self.assertTrue({'UNRESOLVED_ORM_TABLE_NAME', 'UNRESOLVED_ORM_SCHEMA', 'UNRESOLVED_ORM_COLUMN_NAME'} <=
                        {d['code'] for d in result['diagnostics']})

    def test_unrelated_annotations_comments_and_test_source_do_not_create_entities(self):
        self.write('src/main/java/Fake.java', '''import unrelated.Entity; import unrelated.Table;
@Entity @Table(name="fake") class Fake {}
// @jakarta.persistence.Entity class Comment {}
class Text { String fake="@Entity @Table(name=\\"fake\\")"; }
''')
        self.write('src/test/java/Order.java', 'import jakarta.persistence.*; @Entity class Order {}')
        self.assertEqual(orm.extract(self.repo)['entities'], [])

    def test_duplicate_simple_entity_names_do_not_bind_repository_arbitrarily(self):
        self.entity(package='a')
        self.entity(package='b')
        self.write('src/main/java/example/OrderRepo.java', '''package example;
import a.*; import b.*; import org.springframework.data.jpa.repository.JpaRepository;
interface OrderRepo extends JpaRepository<Order,Long> {}''')
        result = orm.extract(self.repo)
        self.assertIsNone(result['repositories'][0]['entity'])
        self.assertEqual(len(result['repositories'][0]['candidate_entities']), 2)
        self.assertIn('UNRESOLVED_ORM_REPOSITORY_ENTITY', {d['code'] for d in result['diagnostics']})

    def test_schema_and_repository_scope_prevent_column_identity_collisions(self):
        self.entity('Order', '@Table(name="orders",schema="sales")')
        self.entity('Other', '@Table(name="orders",schema="audit")')
        graph = Graph(self.workspace)
        orm.add_to_graph(graph, self.repo, 'repo:service', {})
        first = {n['id'] for n in graph.nodes.values() if n['type'] == 'COLUMN'}
        self.assertEqual(len(first), 4)
        orm.add_to_graph(graph, self.repo, 'repo:another-service', {})
        all_columns = {n['id'] for n in graph.nodes.values() if n['type'] == 'COLUMN'}
        self.assertEqual(len(all_columns), 8)

    def test_reuse_existing_unqualified_table_does_not_erase_runtime_metadata(self):
        self.entity()
        self.repository('@Query(value="SELECT id FROM orders", nativeQuery=true) Object list();')
        graph = Graph(self.workspace)
        path = (self.repo / 'src/main/java/example/OrderRepo.java').relative_to(self.workspace).as_posix()
        ev = graph.add_evidence('repo:service', path, 4, 'orders', 'database-runtime')
        graph.add_node('table:service:orders', 'TABLE', 'orders', 'repo:service', dimensions=('RUNTIME',),
                       component_kind=None, functional_role='Existing runtime reference', business_meaning='Existing reference',
                       source_paths=(path,), evidence=(ev,), properties={'access': 'READ', 'client': 'NATIVE_QUERY'})
        orm.add_to_graph(graph, self.repo, 'repo:service', {})
        table = graph.nodes['table:service:orders']
        self.assertEqual(table['properties']['access'], 'READ')
        self.assertNotIn('mapping_only', table['properties'])
        self.assertTrue(table['properties']['has_mapping_detail'])
        references = [e for e in graph.edges.values() if e['relationship'] == 'REFERENCES_COLUMN']
        column = graph.nodes[references[0]['target']]
        self.assertEqual(column['properties']['table'], 'table:service:orders')

    def test_native_sql_columns_retain_alias_roles_and_wildcard_limit(self):
        self.entity()
        self.repository('''@Query(value="SELECT o.order_id, c.name, o.* FROM sales.orders o JOIN crm.customers c ON o.customer_id=c.id WHERE o.status=:status ORDER BY o.order_id", nativeQuery=true)
Object report();''')
        result = orm.extract(self.repo)
        query = result['queries'][0]
        columns = {(c['table']['schema'], c['table']['name'], c['name'], c['role']) for c in query['columns']}
        self.assertIn(('sales', 'orders', 'order_id', 'PROJECTION'), columns)
        self.assertIn(('crm', 'customers', 'name', 'PROJECTION'), columns)
        self.assertIn(('sales', 'orders', 'customer_id', 'PREDICATE'), columns)
        self.assertIn(('sales', 'orders', 'status', 'PREDICATE'), columns)
        self.assertNotIn('status', {c['name'] for c in query['columns'] if c['role'] == 'PROJECTION'})
        self.assertIn('SQL_WILDCARD_COLUMN_SET', query['limits'])

    def test_sql_insert_update_delete_and_unqualified_ambiguity(self):
        insert = orm.sql_columns('INSERT INTO sales.orders (id, amount) VALUES (:id, :amount)')
        self.assertEqual({(c['name'], c['role']) for c in insert['columns']}, {('id', 'INSERT'), ('amount', 'INSERT')})
        update = orm.sql_columns('UPDATE sales.orders SET amount=:amount WHERE id=:id')
        self.assertEqual({(c['name'], c['role']) for c in update['columns']}, {('amount', 'ASSIGNMENT'), ('id', 'PREDICATE')})
        delete = orm.sql_columns('DELETE FROM sales.orders WHERE id=?')
        self.assertEqual([(c['name'], c['role']) for c in delete['columns']], [('id', 'PREDICATE')])
        ambiguous = orm.sql_columns('SELECT id FROM orders o JOIN customers c ON o.customer_id=c.id')
        self.assertIn('AMBIGUOUS_SQL_COLUMN', ambiguous['limits'])
        self.assertFalse(any(c['name'] == 'id' and c['role'] == 'PROJECTION' for c in ambiguous['columns']))

    def test_dynamic_native_query_and_nested_sql_have_explicit_limits(self):
        self.entity()
        self.repository('''@Query(value=makeSql(), nativeQuery=true) Object dynamic();
@Query(value="SELECT id FROM orders WHERE id IN (SELECT id FROM other)", nativeQuery=true) Object nested();
@Query("select o from Order o") Object jpql();''')
        result = orm.extract(self.repo)
        self.assertEqual(len(result['queries']), 1)
        self.assertEqual(result['queries'][0]['columns'], [])
        self.assertIn('UNSUPPORTED_COMPLEX_SQL', result['queries'][0]['limits'])
        self.assertIn('UNRESOLVED_SQL_EXPRESSION', {d['code'] for d in result['diagnostics']})

    def test_nested_module_paths_remain_repository_relative(self):
        self.write('pom.xml', '<project><modules><module>nested</module></modules></project>')
        self.write('nested/pom.xml', '<project/>')
        self.write('nested/src/main/java/Order.java', 'import jakarta.persistence.*; @Entity @Table(name="orders") class Order { @Column(name="id") Long id; }')
        self.assertEqual(orm.extract(self.repo)['entities'][0]['path'], 'nested/src/main/java/Order.java')

    def test_sql_labels_functions_and_qualified_names_are_not_false_columns(self):
        query = orm.sql_columns('SELECT sales.orders.id identity, count(*) AS total FROM sales.orders WHERE status=\'ACTIVE\'')
        self.assertEqual({(c['name'], c['role']) for c in query['columns']}, {('id', 'PROJECTION'), ('status', 'PREDICATE')})
        self.assertEqual(query['limits'], [])
        ambiguous = orm.sql_columns('SELECT orders.id FROM sales.orders JOIN audit.orders ON sales.orders.id=audit.orders.id')
        self.assertIn('AMBIGUOUS_SQL_COLUMN', ambiguous['limits'])
        self.assertFalse(any(c['role'] == 'PROJECTION' for c in ambiguous['columns']))
        function = orm.sql_columns('SELECT value FROM generate_series(1, 10)')
        self.assertEqual(function['tables'], [])
        self.assertIn('UNSUPPORTED_SQL_TABLE_EXPRESSION', function['limits'])

    def test_typed_jdbc_literals_are_retained_dynamic_and_shadowed_receivers_are_not_guessed(self):
        self.write('src/main/java/Client.java', '''import org.springframework.jdbc.core.JdbcTemplate;
class Client { JdbcTemplate jdbc;
Object read() { return jdbc.queryForList("SELECT id FROM sales.orders WHERE status=?", "ACTIVE"); }
void write() { jdbc.update("UPDATE sales.orders SET amount=? WHERE id=?", 1, 2); }
Object dynamic(String sql) { return jdbc.queryForList(sql); }
Object shadow(Object jdbc) { return jdbc.queryForList("SELECT fake FROM fake"); }
}''')
        self.write('src/main/java/Fake.java', '''class Fake { Object jdbc;
Object read() { return jdbc.queryForList("SELECT fake FROM fake"); } }''')
        result = orm.extract(self.repo)
        self.assertEqual(len(result['queries']), 2)
        self.assertEqual({q['client'] for q in result['queries']}, {'JDBC_TEMPLATE'})
        self.assertTrue({'UNRESOLVED_SQL_EXPRESSION', 'AMBIGUOUS_JDBC_RECEIVER'} <= {d['code'] for d in result['diagnostics']})
        self.assertFalse(any(c['name'] == 'fake' for q in result['queries'] for c in q['columns']))

    def test_runtime_mapper_xml_is_separate_from_migrations_and_dynamic_mapper_sql(self):
        self.write('src/main/resources/mappers/Orders.xml', '''<mapper namespace="example.Orders">
<select id="find">SELECT o.id FROM sales.orders o WHERE o.status=#{status}</select>
<update id="change">UPDATE sales.orders SET status=#{status} WHERE id=#{id}</update>
<select id="dynamic">SELECT id FROM ${table}</select>
<select id="conditional">SELECT id FROM sales.orders <where><if test="x">id=#{x}</if></where></select>
</mapper>''')
        self.write('src/main/resources/db/migration/V1.sql', 'SELECT false_positive FROM migration_only;')
        result = orm.extract(self.repo)
        self.assertEqual(len(result['queries']), 2)
        self.assertEqual({q['mapper_statement'] for q in result['queries']}, {'find', 'change'})
        self.assertEqual(sum(d['code'] == 'UNRESOLVED_MYBATIS_SQL' for d in result['diagnostics']), 2)
        self.assertFalse(any(c['name'] == 'false_positive' for q in result['queries'] for c in q['columns']))


if __name__ == '__main__':
    unittest.main()
