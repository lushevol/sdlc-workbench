import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import test from 'node:test';
import { compileKql, configureKibanaTools, KibanaReader, validateKibanaConfig } from './kibana.js';

const mapping = {
  'logs-app-2026': { mappings: { properties: {
    '@timestamp': { type: 'date' }, message: { type: 'text' },
    'log.level': { type: 'keyword' }, 'http.status_code': { type: 'integer' },
    enabled: { type: 'boolean' },
    service: { properties: { name: { type: 'keyword' } } },
    nested: { type: 'nested', properties: { value: { type: 'keyword' } } },
  } } },
};
const explain = (field, explanation = `Meaning of ${field}`) => ({ field, explanation });
const args = () => ({
  index: 'logs-app-*', kql: 'log.level: error AND http.status_code >= 500',
  start: '2026-11-01T00:00:00Z', end: '2026-11-01T01:00:00Z',
  fieldMapping: { timestamp: explain('@timestamp'), message: explain('message'), level: explain('log.level') },
  fields: [explain('http.status_code')], size: 10,
});
const config = baseUrl => ({
  HTTPS_PROXY: '', kibanaConfig: { baseUrl, apiKey: 'private-fixture-key', indices: ['logs-app-*'], maxRangeHours: 24 },
});

async function fixture(t, handler) {
  const server = createServer(handler);
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  t.after(() => new Promise(resolve => server.close(resolve)));
  const before = process.env.NO_PROXY;
  process.env.NO_PROXY = '127.0.0.1';
  t.after(() => { if (before === undefined) delete process.env.NO_PROXY; else process.env.NO_PROXY = before; });
  return `http://127.0.0.1:${server.address().port}/base/s/operations`;
}

test('Kibana Console reads mapping then generated read-only DSL with auth and explanations', async t => {
  const seen = [];
  const base = await fixture(t, async (request, response) => {
    let body = '';
    for await (const chunk of request) body += chunk;
    seen.push({ url: request.url, method: request.method, headers: request.headers, body });
    response.writeHead(200, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify(seen.length === 1 ? mapping : {
      hits: { total: { value: 12, relation: 'eq' }, hits: [{ fields: { message: ['error'] } }] },
      timed_out: false, _shards: { failed: 0 },
    }));
  });
  const output = await new KibanaReader(config(base)).searchLogs(args());
  assert.equal(seen.length, 2);
  for (const request of seen) {
    assert.equal(request.method, 'POST');
    assert.equal(request.headers.authorization, 'ApiKey private-fixture-key');
    assert.equal(request.headers['kbn-xsrf'], 'workbench-read-only');
    assert.match(request.url, /^\/base\/s\/operations\/api\/console\/proxy\?/);
  }
  const mappingUrl = new URL(seen[0].url, base);
  assert.equal(mappingUrl.searchParams.get('path'), 'logs-app-*/_mapping');
  assert.equal(mappingUrl.searchParams.get('method'), 'GET');
  const searchUrl = new URL(seen[1].url, base);
  assert.equal(searchUrl.searchParams.get('path'), 'logs-app-*/_search');
  assert.equal(searchUrl.searchParams.get('method'), 'POST');
  const query = JSON.parse(seen[1].body);
  assert.deepEqual(query.query.bool.filter[0], { range: { '@timestamp': { gte: args().start, lt: args().end } } });
  assert.deepEqual(query.query.bool.filter[1], { bool: { filter: [
    { term: { 'log.level': 'error' } }, { range: { 'http.status_code': { gte: '500' } } },
  ] } });
  assert.equal(query._source, false);
  assert.equal(query.size, 10);
  assert.deepEqual(query.fields, ['@timestamp', 'message', 'log.level', 'http.status_code']);
  assert.equal(output.fieldExplanations.find(field => field.field === 'log.level').type, 'keyword');
  assert.match(output.explanation, /inclusive start and exclusive end/);
  assert.equal(output.completeness.truncated, true);
  assert.equal(output.completeness.partial, false);
});

test('KQL preserves Boolean precedence, phrase, existence, boolean and keyword wildcard semantics', () => {
  const fields = new Map([
    ['message', { type: 'text' }], ['log.level', { type: 'keyword' }], ['enabled', { type: 'boolean' }],
  ]);
  assert.deepEqual(compileKql('log.level: error OR NOT (message: "lost connection" AND enabled: true)', fields), {
    bool: { should: [
      { term: { 'log.level': 'error' } },
      { bool: { must_not: [{ bool: { filter: [
        { match_phrase: { message: 'lost connection' } }, { term: { enabled: true } },
      ] } }] } },
    ], minimum_should_match: 1 },
  });
  assert.deepEqual(compileKql('log.level: err* AND message: *', fields), {
    bool: { filter: [{ wildcard: { 'log.level': { value: 'err*' } } }, { exists: { field: 'message' } }] },
  });
  assert.deepEqual(compileKql('*', fields), { match_all: {} });
  assert.throws(() => compileKql('message: *error*', fields), /trailing wildcard/);
  assert.throws(() => compileKql('message: error timeout', fields), /unsupported/);
  assert.throws(() => compileKql('log.level: (error OR warn)', fields), /one value/);
  assert.throws(() => compileKql('unknown: value', fields), /mapping and explanation/);
  assert.throws(() => compileKql('message: error AND', fields), /explicit field/);
  assert.throws(() => compileKql('enabled: maybe', fields), /true or false/);
  assert.throws(() => compileKql('message: value\\:other', fields), /unsupported/);
});

test('invalid selectors, time bounds, missing explanations and raw DSL fail before network', async t => {
  let requests = 0;
  const base = await fixture(t, (_request, response) => { requests++; response.end('{}'); });
  const reader = new KibanaReader(config(base));
  for (const index of ['other-*', 'logs-app-*/_delete_by_query', 'logs-app-*?x=1', 'logs-app-*%2f_search', 'logs-app-*,secrets', 'logs-app-*#x']) {
    await assert.rejects(reader.searchLogs({ ...args(), index }));
  }
  await assert.rejects(reader.searchLogs({ ...args(), end: '2026-11-03T00:00:00Z' }), /range/);
  await assert.rejects(reader.searchLogs({ ...args(), end: args().start }), /range/);
  await assert.rejects(reader.searchLogs({ ...args(), fieldMapping: { timestamp: explain('@timestamp'), message: explain('message', ' ') } }));
  await assert.rejects(reader.searchLogs({ ...args(), fieldMapping: undefined }));
  await assert.rejects(reader.searchLogs({ ...args(), query: { script: {} } }));
  await assert.rejects(reader.consoleRead('logs-app-*', '_delete_by_query', {}), /not read-only/);
  assert.equal(requests, 0);
});

test('search rejects unverified, conflicting and nested mappings before any search request', async t => {
  let requests = 0;
  let responseMapping = mapping;
  const base = await fixture(t, (_request, response) => {
    requests++;
    response.writeHead(200, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify(responseMapping));
  });
  const reader = new KibanaReader(config(base));
  await assert.rejects(reader.searchLogs({ ...args(), fields: [explain('nested.value')] }), /nested/);
  await assert.rejects(reader.searchLogs({ ...args(), fields: [explain('unknown')] }), /missing/);
  await assert.rejects(reader.searchLogs({ ...args(), fieldMapping: { ...args().fieldMapping, timestamp: explain('message') } }), /date field/);
  responseMapping = { ...mapping, other: { mappings: { properties: { 'log.level': { type: 'text' } } } } };
  await assert.rejects(reader.searchLogs(args()), /conflicting/);
  responseMapping = { 'logs-app-2026': { mappings: { ...mapping['logs-app-2026'].mappings,
    runtime: { 'log.level': { type: 'keyword', script: { source: 'emit(1)' } } },
  } } };
  await assert.rejects(reader.searchLogs(args()), /conflicting/);
  assert.equal(requests, 5);
});

test('HTTP redirects and errors cannot forward credentials outside configured Kibana', async t => {
  let destinationCalls = 0;
  const destination = await fixture(t, (_request, response) => { destinationCalls++; response.end('{}'); });
  const base = await fixture(t, (_request, response) => {
    response.writeHead(302, { Location: destination }); response.end('private-fixture-key');
  });
  await assert.rejects(new KibanaReader(config(base)).fieldMapping({ index: 'logs-app-*' }), error => {
    assert.doesNotMatch(error.message, /private-fixture-key/); return true;
  });
  assert.equal(destinationCalls, 0);
});

test('Kibana discovery needs no configuration and validation rejects missing or ambiguous auth', async () => {
  const registered = [];
  configureKibanaTools({ tool: (...values) => registered.push(values) }, {});
  assert.deepEqual(registered.map(tool => tool[0]), ['kibana_get_field_mapping', 'kibana_search_logs']);
  const result = await registered[1][3](args());
  assert.equal(result.isError, true);
  assert.equal(result.structuredContent.code, 'KIBANA_INVALID_QUERY');
  assert.throws(() => validateKibanaConfig(config('https://user:password@kibana.example')), /base URL/);
  assert.throws(() => validateKibanaConfig({ kibanaConfig: { ...config('https://kibana.example').kibanaConfig, apiKey: '' } }), /authentication/);
  assert.throws(() => validateKibanaConfig({ kibanaConfig: { ...config('https://kibana.example').kibanaConfig, username: 'user', password: 'pass' } }), /authentication/);
});
