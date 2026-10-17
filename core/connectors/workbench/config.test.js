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
