import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { Client } from 'pg';
import { assertAnalysisSql, configurePostgresqlTools, readPostgresql, validatePostgresqlConfig } from './postgresql.js';

const config = { host: 'localhost', database: 'analysis', user: 'reader', password: 'must-not-appear', sslMode: 'disable', maxRows: '2' };
const restricted = { rolsuper: false, rolcreatedb: false, rolcreaterole: false, rolreplication: false, rolbypassrls: false, read_only: 'on' };

function mockClient({ role = restricted, result, fail = '' } = {}) {
  const seen = [];
  const client = {
    connect: async () => { seen.push('CONNECT'); },
    query: async query => {
      seen.push(query);
      if (query === fail) throw new Error('must-not-appear');
      if (typeof query === 'string' && query.startsWith('SELECT r.rolsuper')) return { rows: [role] };
      if (typeof query === 'object') {
        if (fail === 'query') throw new Error('must-not-appear');
        return result || { fields: [{ name: 'id', dataTypeID: 23 }], rows: [{ id: 1 }, { id: 2 }, { id: 3 }] };
      }
      return { rows: [] };
    },
    end: async () => { seen.push('END'); },
  };
  return { client, seen };
}

test('PostgreSQL query uses read-only transaction, extended protocol, parameters, bounded rows, and rollback', async () => {
  const { client, seen } = mockClient();
  let options;
  const data = await readPostgresql(config, 'postgresql_query', { sql: 'SELECT $1::int AS id', parameters: [8] }, async value => { options = value; return client; });
  assert.equal(options.options, '-c default_transaction_read_only=on');
  assert.equal(options.ssl, false);
  assert.deepEqual(data.rows, [{ id: 1 }, { id: 2 }]);
  assert.equal(data.truncated, true);
  assert.equal(data.maxRows, 2);
  assert.equal(seen[1], 'BEGIN READ ONLY');
  assert.ok(seen.includes('SET LOCAL statement_timeout = 10000'));
  assert.ok(seen.includes('SET LOCAL lock_timeout = 2000'));
  const query = seen.find(value => typeof value === 'object');
  assert.equal(query.queryMode, 'extended');
  assert.deepEqual(query.values, [8]);
  assert.match(query.text, /LIMIT 3$/);
  assert.deepEqual(seen.slice(-2), ['ROLLBACK', 'END']);
});

test('PostgreSQL rejects privileged roles and rolls back failed reads', async () => {
  for (const role of [{ ...restricted, rolsuper: true }, { ...restricted, rolbypassrls: true }, { ...restricted, read_only: 'off' }]) {
    const { client, seen } = mockClient({ role });
    await assert.rejects(readPostgresql(config, 'postgresql_query', { sql: 'SELECT 1' }, async () => client));
    assert.equal(seen.some(value => typeof value === 'object'), false);
    assert.deepEqual(seen.slice(-2), ['ROLLBACK', 'END']);
  }
  const { client, seen } = mockClient({ fail: 'query' });
  await assert.rejects(readPostgresql(config, 'postgresql_query', { sql: 'SELECT 1' }, async () => client));
  assert.deepEqual(seen.slice(-2), ['ROLLBACK', 'END']);
});

test('PostgreSQL rejects mutation commands, configuration functions, and oversized arguments before connecting', async () => {
  const queries = [
    'DELETE FROM accounts', 'BEGIN', 'COPY accounts TO STDOUT', 'EXPLAIN ANALYZE DELETE FROM accounts',
    "SELECT set_config('statement_timeout', '0', true)",
    "SELECT pg_catalog.\"set_config\"('transaction_read_only', 'off', true)",
    "SELECT U&\"set_\\0063onfig\"('statement_timeout','0',true)",
    "SELECT pg_notify('topic', 'data')", 'SELECT public.dblink_exec($$UPDATE data SET id=1$$)',
    "SELECT '\\', set_config('statement_timeout','0',true)",
    'SELECT pg_advisory_lock(1)', 'SELECT nextval(\'sequence\')',
  ];
  for (const sql of queries) await assert.rejects(readPostgresql(config, 'postgresql_query', { sql }, async () => { throw new Error('MUST NOT CONNECT'); }));
  assert.doesNotThrow(() => assertAnalysisSql("SELECT 'set_config', $$pg_notify$$ /* set_config */ AS description"));
  assert.doesNotThrow(() => assertAnalysisSql("SELECT E'escaped\\\'set_config' AS description"));
  await assert.rejects(readPostgresql(config, 'postgresql_query', { sql: 'SELECT 1', parameters: Array(101).fill(1) }));
  await assert.rejects(readPostgresql(config, 'postgresql_query', { sql: `SELECT '${'a'.repeat(65536)}'` }));
});

test('PostgreSQL metadata uses bound identifiers and response errors remain redacted', async () => {
  const { client, seen } = mockClient();
  await readPostgresql(config, 'postgresql_describe_table', { schema: 'public', table: "t'; DELETE FROM t; --" }, async () => client);
  const query = seen.find(value => typeof value === 'object');
  assert.deepEqual(query.values, ['public', "t'; DELETE FROM t; --"]);
  assert.doesNotMatch(query.text, /DELETE/);
  const handlers = {};
  configurePostgresqlTools({ tool: (name, _description, _shape, handler) => { handlers[name] = handler; } }, {});
  const error = await handlers.postgresql_query({ sql: 'SELECT 1' });
  assert.equal(error.isError, true);
  assert.doesNotMatch(JSON.stringify(error), /must-not-appear/);
});

test('PostgreSQL TLS verifies certificates by default and invalid limits fail', async () => {
  const { client } = mockClient();
  let settings;
  await readPostgresql({ ...config, sslMode: undefined }, 'postgresql_query', { sql: 'SELECT 1' }, async value => { settings = value; return client; });
  assert.equal(settings.ssl.rejectUnauthorized, true);
  for (const change of [{ sslMode: 'require' }, { maxRows: '10001' }, { port: 'no' }, { statementTimeoutMs: '0' }, { sslMode: 'disable', caFile: '/tmp/ca' }]) {
    assert.throws(() => validatePostgresqlConfig({ ...config, ...change }));
  }
  const huge = mockClient({ result: { fields: [], rows: [{ data: 'x'.repeat(1024 * 1024) }] } });
  await assert.rejects(readPostgresql(config, 'postgresql_query', { sql: 'SELECT data' }, async () => huge.client));
  assert.deepEqual(huge.seen.slice(-2), ['ROLLBACK', 'END']);
  const ambiguous = mockClient({ result: { fields: [{ name: 'id' }, { name: 'id' }], rows: [{ id: 2 }] } });
  await assert.rejects(readPostgresql(config, 'postgresql_query', { sql: 'SELECT 1 AS id, 2 AS id' }, async () => ambiguous.client));
  assert.deepEqual(ambiguous.seen.slice(-2), ['ROLLBACK', 'END']);
});

test('real PostgreSQL fixture proves reads, row caps, mutation denial, and no persistent transaction state', async t => {
  try { execFileSync('initdb', ['--version'], { stdio: 'ignore' }); }
  catch { t.skip('PostgreSQL initdb is unavailable; controlled database execution did not run.'); return; }
  const root = mkdtempSync(join(tmpdir(), 'workbench-pg-'));
  const data = join(root, 'data');
  const socket = root;
  const port = 5432;
  let started = false;
  t.after(() => {
    if (started) execFileSync('pg_ctl', ['-D', data, '-m', 'immediate', '-w', 'stop'], { stdio: 'ignore' });
    rmSync(root, { recursive: true, force: true });
  });
  execFileSync('initdb', ['-D', data, '-A', 'trust', '--no-locale', '--encoding=UTF8'], { stdio: 'ignore' });
  // An isolated Unix socket avoids contacting or binding an existing database.
  execFileSync('pg_ctl', ['-D', data, '-l', join(root, 'server.log'), '-o', `-F -k ${socket} -h '' -p ${port}`, '-w', 'start'], { stdio: 'ignore' });
  started = true;
  const admin = new Client({ host: socket, port, database: 'postgres', user: process.env.USER, ssl: false });
  await admin.connect();
  t.after(() => admin.end());
  await admin.query(`CREATE ROLE workbench_reader LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;
    CREATE TABLE public.workbench_probe (id integer PRIMARY KEY, label text);
    INSERT INTO public.workbench_probe VALUES (1, 'one'), (2, 'two'), (3, 'three');
    GRANT USAGE ON SCHEMA public TO workbench_reader;
    GRANT SELECT ON public.workbench_probe TO workbench_reader;`);
  const cfg = { ...config, host: socket, port, database: 'postgres', user: 'workbench_reader', statementTimeoutMs: 300 };
  const version = (await admin.query('SELECT version() AS version')).rows[0].version;
  t.diagnostic(version);
  const tables = await readPostgresql(cfg, 'postgresql_list_tables', { schema: 'public' });
  assert.ok(tables.rows.some(row => row.table_name === 'workbench_probe'));
  const columns = await readPostgresql(cfg, 'postgresql_describe_table', { schema: 'public', table: 'workbench_probe' });
  assert.deepEqual(columns.rows.map(row => row.column_name), ['id', 'label']);
  const rows = await readPostgresql(cfg, 'postgresql_query', { sql: 'SELECT * FROM public.workbench_probe WHERE id >= $1 ORDER BY id', parameters: [1] });
  assert.deepEqual(rows.rows, [{ id: 1, label: 'one' }, { id: 2, label: 'two' }]);
  assert.equal(rows.truncated, true);
  for (const sql of [
    'SELECT 1); ROLLBACK; DELETE FROM public.workbench_probe; SELECT (1',
    'WITH removed AS (DELETE FROM public.workbench_probe RETURNING *) SELECT * FROM removed',
    'SELECT 1 INTO public.workbench_created',
  ]) await assert.rejects(readPostgresql(cfg, 'postgresql_query', { sql }));
  // Temporarily grant UPDATE to prove transaction enforcement independently of grants.
  await admin.query('GRANT UPDATE, DELETE ON public.workbench_probe TO workbench_reader');
  await assert.rejects(readPostgresql(cfg, 'postgresql_query', { sql: 'WITH changed AS (UPDATE public.workbench_probe SET label = \'changed\' RETURNING *) SELECT * FROM changed' }));
  // A SECURITY DEFINER function cannot bypass the transaction's read-only state.
  await admin.query(`CREATE FUNCTION public.workbench_write_probe() RETURNS int LANGUAGE plpgsql SECURITY DEFINER AS $$ BEGIN DELETE FROM public.workbench_probe; RETURN 1; END $$`);
  await assert.rejects(readPostgresql(cfg, 'postgresql_query', { sql: 'SELECT public.workbench_write_probe()' }));
  assert.equal((await admin.query('SELECT count(*)::int AS count FROM public.workbench_probe')).rows[0].count, 3);
  assert.equal((await admin.query("SELECT to_regclass('public.workbench_created') AS table_name")).rows[0].table_name, null);
  await assert.rejects(readPostgresql({ ...cfg, user: process.env.USER }, 'postgresql_query', { sql: 'SELECT 1' }));
  const state = await readPostgresql(cfg, 'postgresql_query', { sql: "SELECT current_setting('transaction_read_only') AS read_only" });
  assert.equal(state.rows[0].read_only, 'on');
  // A recursive computation reaches the server-side timeout without unsafe functions.
  await assert.rejects(readPostgresql(cfg, 'postgresql_query', { sql: 'WITH RECURSIVE endless(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM endless) SELECT sum(n) FROM endless' }));
  t.diagnostic('Assertions: parameterized read; metadata; cap and truncation; multi-statement escape denied; DML/DDL denied; SECURITY DEFINER write denied; table unchanged; superuser denied; server timeout enforced.');
  assert.ok(readFileSync(join(root, 'server.log'), 'utf8').length > 0);
});
