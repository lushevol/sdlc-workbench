import { readFileSync } from 'node:fs';
import { rootCertificates } from 'node:tls';
import { z } from 'zod';

const MAX_RESULT_BYTES = 1024 * 1024;
const name = z.string().min(1).max(256);
const parameter = z.union([z.string().max(65536), z.number().finite(), z.boolean(), z.null()]);
const schemas = {
  postgresql_list_tables: { schema: name.optional() },
  postgresql_describe_table: { schema: name, table: name },
  postgresql_query: {
    sql: z.string().min(1).max(65536),
    parameters: z.array(parameter).max(100).optional(),
    maxRows: z.number().int().min(1).max(10000).optional(),
  },
};

function integer(value, fallback, min, max) {
  const number = value === undefined || value === '' ? fallback : Number(value);
  if (!Number.isInteger(number) || number < min || number > max) throw new Error('Invalid PostgreSQL limit.');
  return number;
}

export function validatePostgresqlConfig(config = {}) {
  if (['host', 'database', 'user', 'password'].some(key => typeof config[key] !== 'string' || !config[key].trim())) {
    throw new Error('PostgreSQL connection settings are incomplete.');
  }
  if (!['verify-full', 'disable'].includes(config.sslMode || 'verify-full')) throw new Error('Invalid PostgreSQL TLS mode.');
  if (config.sslMode === 'disable' && config.caFile) throw new Error('A PostgreSQL CA requires TLS.');
  integer(config.port, 5432, 1, 65535);
  integer(config.statementTimeoutMs, 10000, 1, 60000);
  integer(config.maxRows, 1000, 1, 10000);
}

function settings(config) {
  validatePostgresqlConfig(config);
  return {
    host: config.host, port: integer(config.port, 5432, 1, 65535),
    database: config.database, user: config.user, password: config.password,
    ssl: config.sslMode === 'disable' ? false : {
      rejectUnauthorized: true,
      ...(config.caFile ? { ca: [...rootCertificates, readFileSync(config.caFile, 'utf8')] } : {}),
    },
    application_name: 'ai-sdlc-workbench-read-only',
    connectionTimeoutMillis: 10000,
    // No connection URL is accepted: it could override TLS or session options.
    options: '-c default_transaction_read_only=on',
  };
}

// This guard blocks configuration changes and known side-effect helpers. It is
// not an SQL sandbox: the database role must lack EXECUTE on unsafe UDFs.
export function assertAnalysisSql(sql) {
  if (!/^\s*(SELECT|WITH)\b/i.test(sql) || sql.includes('\0')) throw new Error('Unsupported analysis query.');
  const forbidden = /^(?:set_config|nextval|setval|lo_.*|dblink.*|pg_(?:advisory_.*|try_advisory_.*|notify|sleep.*|terminate_backend|cancel_backend|reload_conf|rotate_logfile|promote|switch_wal|logical_.*|create_.*|drop_.*|replication_.*|replication_origin_.*|write_.*|read_.*|stat_file|ls_.*|import_.*|export_.*|backup_.*|start_backup|stop_backup|wal_replay_.*))$/i;
  for (let i = 0; i < sql.length;) {
    if (sql.startsWith('--', i)) { const end = sql.indexOf('\n', i + 2); i = end < 0 ? sql.length : end + 1; continue; }
    if (sql.startsWith('/*', i)) {
      let depth = 1; i += 2;
      while (i < sql.length && depth) {
        if (sql.startsWith('/*', i)) { depth++; i += 2; }
        else if (sql.startsWith('*/', i)) { depth--; i += 2; }
        else i++;
      }
      continue;
    }
    // Unicode-escaped identifiers can disguise a forbidden function name.
    if (/^[uU]&"/.test(sql.slice(i, i + 3))) throw new Error('Unicode-escaped identifiers are unsupported.');
    if (sql[i] === "'") {
      const escape = /[eE]/.test(sql[i - 1] || '') && !/[A-Za-z_0-9$]/.test(sql[i - 2] || '');
      i++;
      while (i < sql.length) {
        if (escape && sql[i] === '\\') { i += 2; continue; }
        if (sql[i] === "'") { if (sql[i + 1] === "'") { i += 2; continue; } i++; break; }
        i++;
      }
      continue;
    }
    const dollar = sql.slice(i).match(/^\$(?:[A-Za-z_][A-Za-z_0-9]*)?\$/);
    if (dollar) { const end = sql.indexOf(dollar[0], i + dollar[0].length); i = end < 0 ? sql.length : end + dollar[0].length; continue; }
    let token = '';
    if (sql[i] === '"') {
      i++;
      while (i < sql.length) {
        if (sql[i] === '"') { if (sql[i + 1] === '"') { token += '"'; i += 2; continue; } i++; break; }
        token += sql[i++];
      }
    } else {
      const identifier = sql.slice(i).match(/^[A-Za-z_][A-Za-z_0-9$]*/);
      if (identifier) { token = identifier[0]; i += token.length; }
      else { i++; continue; }
    }
    if (forbidden.test(token)) throw new Error('Unsupported analysis function.');
  }
}

function queryDefinition(tool, args, cap) {
  if (tool === 'postgresql_list_tables') return {
    sql: `SELECT table_schema, table_name, table_type FROM information_schema.tables
          WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
            AND ($1::text IS NULL OR table_schema = $1)
          ORDER BY table_schema, table_name`,
    parameters: [args.schema ?? null], cap,
  };
  if (tool === 'postgresql_describe_table') return {
    sql: `SELECT column_name, data_type, udt_schema, udt_name, is_nullable,
                 column_default, ordinal_position
          FROM information_schema.columns WHERE table_schema = $1 AND table_name = $2
          ORDER BY ordinal_position`,
    parameters: [args.schema, args.table], cap,
  };
  // The server parses the wrapped statement. Unsupported commands and multiple
  // statements cannot become top-level transaction-control or mutation commands.
  assertAnalysisSql(args.sql);
  return { sql: args.sql, parameters: args.parameters || [], cap: Math.min(args.maxRows || cap, cap) };
}

/** Execute one bounded query and always discard its read-only transaction. */
export async function readPostgresql(config, tool, input = {}, createClient) {
  const shape = schemas[tool];
  if (!shape) throw new Error('Unknown PostgreSQL tool.');
  const args = z.object(shape).strict().parse(input);
  const cap = integer(config.maxRows, 1000, 1, 10000);
  const definition = queryDefinition(tool, args, cap);
  const clientSettings = settings(config);
  const factory = createClient || (async options => {
    const { Client } = await import('pg');
    return new Client(options);
  });
  const client = await factory(clientSettings);
  let transaction = false;
  try {
    await client.connect();
    await client.query('BEGIN READ ONLY');
    transaction = true;
    const timeout = integer(config.statementTimeoutMs, 10000, 1, 60000);
    await client.query('SET LOCAL standard_conforming_strings = on');
    await client.query(`SET LOCAL statement_timeout = ${timeout}`);
    await client.query(`SET LOCAL lock_timeout = ${Math.min(timeout, 2000)}`);
    await client.query(`SET LOCAL idle_in_transaction_session_timeout = ${Math.max(timeout, 1000)}`);
    const identity = await client.query(`SELECT r.rolsuper, r.rolcreatedb, r.rolcreaterole, r.rolreplication, r.rolbypassrls,
      current_setting('transaction_read_only') AS read_only
      FROM pg_catalog.pg_roles r WHERE r.rolname = current_user`);
    const role = identity.rows[0];
    if (!role || role.read_only !== 'on' || ['rolsuper', 'rolcreatedb', 'rolcreaterole', 'rolreplication', 'rolbypassrls'].some(key => role[key] !== false)) {
      throw new Error('A restricted read-only PostgreSQL role is required.');
    }
    const result = await client.query({
      text: `SELECT * FROM (\n${definition.sql}\n) AS workbench_analysis LIMIT ${definition.cap + 1}`,
      values: definition.parameters,
      queryMode: 'extended',
    });
    // Object rows cannot represent duplicate column names without data loss.
    // Require explicit SQL aliases rather than returning a misleading result.
    if (new Set(result.fields.map(field => field.name)).size !== result.fields.length) {
      throw new Error('Use unique SQL column aliases.');
    }
    const payload = {
      readOnly: true,
      columns: result.fields.map(field => ({ name: field.name, typeOid: field.dataTypeID })),
      rows: result.rows.slice(0, definition.cap),
      rowCount: Math.min(result.rows.length, definition.cap),
      truncated: result.rows.length > definition.cap,
      maxRows: definition.cap,
    };
    if (Buffer.byteLength(JSON.stringify(payload)) > MAX_RESULT_BYTES) throw new Error('The PostgreSQL result exceeds the response limit.');
    return payload;
  } finally {
    if (transaction) await client.query('ROLLBACK').catch(() => {});
    // A fresh connection prevents session state from surviving an analysis call.
    await client.end().catch(() => {});
  }
}

export function configurePostgresqlTools(server, config = {}) {
  const descriptions = {
    postgresql_list_tables: 'List visible PostgreSQL tables and views using a bounded read-only transaction.',
    postgresql_describe_table: 'Read visible column names, types, nullability, and defaults for one PostgreSQL table.',
    postgresql_query: 'Analyze PostgreSQL data with one parameterized SELECT or WITH query. Results are bounded and the transaction is read-only. Use a dedicated SELECT-only role without privileged function grants.',
  };
  for (const [tool, shape] of Object.entries(schemas)) {
    server.tool(tool, descriptions[tool], shape, async args => {
      try {
        const data = await readPostgresql(config, tool, args);
        return { content: [{ type: 'text', text: JSON.stringify(data) }] };
      } catch {
        return { isError: true, content: [{ type: 'text', text: 'The read-only PostgreSQL request failed. Check connection settings, role privileges, query syntax, and limits.' }] };
      }
    });
  }
}
