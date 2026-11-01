import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { loadConfig } from './config.js';

test('configuration reads only the selected root and preserves environment precedence', t => {
  const root = mkdtempSync(join(tmpdir(), 'workbench-connectors-config-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  writeFileSync(join(root, '.env'), 'CONFLUENCE_PAT=file-token\nCONFLUENCE_BASE_URL=https://root.example\nCODE_REVIEW_GUIDE_FILE=docs/review.md\nNODE_EXTRA_CA_CERTS=certificates/root.pem\n');
  mkdirSync(join(root, 'nested'));
  writeFileSync(join(root, 'nested', '.env'), 'CONFLUENCE_PAT=nested-token\n');
  const previous = process.env.CONFLUENCE_PAT;
  const previousCertificate = process.env.NODE_EXTRA_CA_CERTS;
  delete process.env.NODE_EXTRA_CA_CERTS;
  process.env.CONFLUENCE_PAT = 'process-token';
  t.after(() => {
    if (previous === undefined) delete process.env.CONFLUENCE_PAT;
    else process.env.CONFLUENCE_PAT = previous;
    if (previousCertificate === undefined) delete process.env.NODE_EXTRA_CA_CERTS;
    else process.env.NODE_EXTRA_CA_CERTS = previousCertificate;
  });

  const config = loadConfig(root);
  assert.equal(config.confluenceConfig.token, 'process-token');
  assert.equal(config.confluenceConfig.baseUrl, 'https://root.example');
  assert.equal(config.codeReviewGuideFile, join(root, 'docs', 'review.md'));
  assert.equal(config.env.NODE_EXTRA_CA_CERTS, join(root, 'certificates', 'root.pem'));
  assert.equal(config.workspaceRoot, root);
});

test('configuration permits a missing root environment file and requires an absolute root', t => {
  const root = mkdtempSync(join(tmpdir(), 'workbench-connectors-empty-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  assert.equal(loadConfig(root).workspaceRoot, root);
  assert.throws(() => loadConfig('relative/path'), /absolute workspace/);
});

test('HTTP_PROXY from the root remains available to web connector tools', t => {
  const root = mkdtempSync(join(tmpdir(), 'workbench-connectors-proxy-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const keys = ['HTTPS_PROXY', 'https_proxy', 'HTTP_PROXY', 'http_proxy'];
  const previous = Object.fromEntries(keys.map(key => [key, process.env[key]]));
  for (const key of keys) delete process.env[key];
  t.after(() => {
    for (const key of keys) {
      if (previous[key] === undefined) delete process.env[key];
      else process.env[key] = previous[key];
    }
  });
  writeFileSync(join(root, '.env'), 'HTTP_PROXY=http://proxy.example:8080\n');
  assert.equal(loadConfig(root).HTTPS_PROXY, 'http://proxy.example:8080');
});

test('data connectors use selected workspace settings and resolve the PostgreSQL CA path', t => {
  const root = mkdtempSync(join(tmpdir(), 'workbench-data-config-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const values = {
    KIBANA_BASE_URL: 'https://kibana.example/s/observability',
    KIBANA_API_KEY: 'fixture-key', KIBANA_ALLOWED_INDICES: 'logs-app-*, logs-audit-*',
    WORKBENCH_PG_HOST: 'db.example', WORKBENCH_PG_DATABASE: 'analytics',
    WORKBENCH_PG_USER: 'reader', WORKBENCH_PG_PASSWORD: 'fixture-password',
    WORKBENCH_PG_CA_FILE: 'certificates/postgresql.pem',
  };
  const previous = { ...process.env };
  for (const key of Object.keys(process.env)) {
    if (key.startsWith('KIBANA_') || key.startsWith('WORKBENCH_PG_')) delete process.env[key];
  }
  t.after(() => {
    for (const key of Object.keys(process.env)) {
      if (key.startsWith('KIBANA_') || key.startsWith('WORKBENCH_PG_')) delete process.env[key];
    }
    for (const [key, value] of Object.entries(previous)) {
      if (key.startsWith('KIBANA_') || key.startsWith('WORKBENCH_PG_')) process.env[key] = value;
    }
  });
  writeFileSync(join(root, '.env'), Object.entries(values).map(([key, value]) => `${key}=${value}`).join('\n'));
  process.env.WORKBENCH_PG_USER = 'process-reader';
  const config = loadConfig(root);
  assert.deepEqual(config.kibanaConfig.indices, ['logs-app-*', 'logs-audit-*']);
  assert.equal(config.kibanaConfig.apiKey, 'fixture-key');
  assert.equal(config.kibanaConfig.maxRangeHours, 24);
  assert.equal(config.postgresqlConfig.user, 'process-reader');
  assert.equal(config.postgresqlConfig.caFile, join(root, 'certificates/postgresql.pem'));
  assert.equal(config.postgresqlConfig.sslMode, 'verify-full');
  assert.equal(config.postgresqlConfig.maxRows, '1000');
  process.env.WORKBENCH_PG_PASSWORD = '';
  assert.equal(loadConfig(root).postgresqlConfig.password, '');
});
