import assert from 'node:assert/strict';
import { copyFileSync, mkdtempSync, mkdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import test, { type TestContext } from 'node:test';
import { loadTarget, rejectEnvironmentForFixtures, targetSummary } from '../support/environment.js';

function inputs(t: TestContext, environments: Record<string, unknown>, schemaVersion: number | null = 1) {
  const directory = mkdtempSync(path.join(tmpdir(), 'e2e-environment-'));
  t.after(() => rmSync(directory, { recursive: true, force: true }));
  const file = path.join(directory, 'environments.json');
  const contents = `${JSON.stringify({ ...(schemaVersion === null ? {} : { schemaVersion }), environments }, null, 2)}\n`;
  writeFileSync(file, contents);
  return { directory, file, contents };
}

const nonprod = { targetUrl: 'https://nonprod.example.test/portal/', prefix: 'NonprodPortal' };
const production = { targetUrl: 'https://prod.example.test/portal/', prefix: 'ProductionPortal', area: 'portal' };

test('Given no target selection, When loading configuration, Then no target or implicit local URL is returned', () => {
  assert.equal(loadTarget({}, {}), undefined);
});

test('Given two environment profiles, When selecting each name, Then its URL and prefix remain paired', t => {
  const { file } = inputs(t, { nonprod, production });
  const selectedNonprod = loadTarget({ environment: 'nonprod', environmentsFile: file }, {});
  const selectedProduction = loadTarget({ environment: 'production', environmentsFile: file }, {});
  assert.equal(selectedNonprod?.name, 'nonprod');
  assert.equal(selectedNonprod?.targetUrl, nonprod.targetUrl);
  assert.equal(selectedNonprod?.prefix, nonprod.prefix);
  assert.equal(selectedNonprod?.area, 'login');
  assert.equal(selectedProduction?.name, 'production');
  assert.equal(selectedProduction?.targetUrl, production.targetUrl);
  assert.equal(selectedProduction?.prefix, production.prefix);
  assert.equal(selectedProduction?.area, 'portal');
});

test('Given environment variables, When loading configuration, Then the named file and profile select the target', t => {
  const { file } = inputs(t, { nonprod });
  const selected = loadTarget({}, { E2E_ENVIRONMENT: 'nonprod', E2E_ENVIRONMENTS_FILE: file });
  assert.equal(selected?.targetUrl, nonprod.targetUrl);
  assert.equal(selected?.name, 'nonprod');
});

test('Given the default workspace profile file, When only a name is selected, Then that workspace supplies the target', t => {
  const { directory, file } = inputs(t, { nonprod });
  const workspace = path.join(directory, '.workbench');
  mkdirSync(workspace);
  copyFileSync(file, path.join(workspace, 'e2e-environments.json'));
  const previousDirectory = process.cwd();
  try {
    process.chdir(directory);
    assert.equal(loadTarget({ environment: 'nonprod' }, {})?.targetUrl, nonprod.targetUrl);
  } finally {
    process.chdir(previousDirectory);
  }
});

test('Given explicit profile options, When process defaults differ, Then explicit options determine the selected profile', t => {
  const { file } = inputs(t, { nonprod, production });
  const selected = loadTarget({ environment: 'nonprod', environmentsFile: file }, {
    E2E_ENVIRONMENT: 'production', E2E_ENVIRONMENTS_FILE: path.join(path.dirname(file), 'missing-default.json'),
  });
  assert.equal(selected?.targetUrl, nonprod.targetUrl);
});

test('Given a selected profile, When its target configuration changes, Then retained configuration identity changes', t => {
  const { file } = inputs(t, { nonprod });
  const options = { environment: 'nonprod', environmentsFile: file };
  const first = loadTarget(options, {})?.configurationSha256;
  assert.match(first ?? '', /^[a-f0-9]{64}$/);
  assert.equal(loadTarget(options, {})?.configurationSha256, first);
  writeFileSync(file, JSON.stringify({ environments: { nonprod: { ...nonprod, targetUrl: 'https://changed.example.test/' } } }));
  assert.notEqual(loadTarget(options, {})?.configurationSha256, first);
});

test('Given an existing relative storage file, When loading its profile, Then the path resolves from the profile directory', t => {
  const { directory, file } = inputs(t, { production: { ...production, storageState: 'private/auth.json' } });
  const state = path.join(directory, 'private/auth.json');
  mkdirSync(path.dirname(state));
  writeFileSync(state, JSON.stringify({ cookies: [], origins: [] }));
  const selected = loadTarget({ environment: 'production', environmentsFile: file }, {});
  assert.equal(selected?.storageState, state);
});

test('Given a nonexistent storage file, When loading its profile, Then setup fails before browser execution', t => {
  const { file } = inputs(t, { production: { ...production, storageState: 'missing-auth.json' } });
  assert.throws(() => loadTarget({ environment: 'production', environmentsFile: file }, {}));
});

test('Given a configured workspace and refresh fingerprint, When resolving a profile, Then both assertion inputs are retained', t => {
  const fingerprint = 'a'.repeat(64);
  const { file } = inputs(t, { production: { ...production, workspaceName: 'Read Only Workspace', refreshCredentialSha256: fingerprint } });
  const selected = loadTarget({ environment: 'production', environmentsFile: file }, {});
  assert.equal(selected?.workspaceName, 'Read Only Workspace');
  assert.equal(selected?.refreshCredentialSha256, fingerprint);
});

test('Given an uppercase refresh fingerprint, When resolving a profile, Then session assertions receive normalized hexadecimal', t => {
  const { file } = inputs(t, { production: { ...production, refreshCredentialSha256: 'A'.repeat(64) } });
  const selected = loadTarget({ environment: 'production', environmentsFile: file }, {});
  assert.equal(selected?.refreshCredentialSha256, 'a'.repeat(64));
});

test('Given an unknown environment name, When resolving a target, Then another profile is never selected as fallback', t => {
  const { file } = inputs(t, { production });
  assert.throws(() => loadTarget({ environment: 'nonprod', environmentsFile: file }, {}));
});

test('Given a file without an environment name, When resolving a target, Then ambiguous selection fails', t => {
  const { file } = inputs(t, { production });
  assert.throws(() => loadTarget({ environmentsFile: file }, {}));
  assert.throws(() => loadTarget({}, { E2E_ENVIRONMENTS_FILE: file }));
});

test('Given a named profile, When URL or authentication overrides are supplied, Then mixed target configuration fails', t => {
  const { file } = inputs(t, { production });
  const overrides = [{ url: nonprod.targetUrl }, { prefix: nonprod.prefix }, { storageState: 'other-auth.json' }];
  for (const override of overrides) {
    assert.throws(() => loadTarget({ environment: 'production', environmentsFile: file, ...override }, {}));
  }
});

test('Given an explicit URL and prefix, When resolving a direct target, Then existing direct target selection remains supported', () => {
  const selected = loadTarget({ url: nonprod.targetUrl, prefix: nonprod.prefix }, {});
  assert.equal(selected?.targetUrl, nonprod.targetUrl);
  assert.equal(selected?.prefix, nonprod.prefix);
  assert.equal(selected?.area, 'portal');
});

test('Given an explicit URL without a prefix, When resolving the target, Then setup fails', () => {
  assert.throws(() => loadTarget({ url: nonprod.targetUrl }, {}));
});

test('Given unsupported or credential-bearing URLs, When resolving targets, Then URL validation rejects them', t => {
  const urls = ['file:///tmp/portal.html', 'ftp://example.test/', 'javascript:alert(1)', 'https://user:password@example.test/'];
  for (const targetUrl of urls) {
    const { file } = inputs(t, { nonprod: { ...nonprod, targetUrl } });
    assert.throws(() => loadTarget({ environment: 'nonprod', environmentsFile: file }, {}));
    assert.throws(() => loadTarget({ url: targetUrl, prefix: nonprod.prefix }, {}));
  }
});

test('Given unsupported profile values, When resolving a target, Then invalid configuration never reaches browser setup', t => {
  const invalidProfiles = [
    { ...nonprod, prefix: '' },
    { prefix: nonprod.prefix },
    { ...nonprod, area: 'unknown-area' },
    { ...nonprod, area: ['login'] },
    { ...nonprod, password: 'private-value' },
    { ...nonprod, refreshCredentialSha256: 'not-a-sha256' },
  ];
  for (const profile of invalidProfiles) {
    const { file } = inputs(t, { nonprod: profile });
    assert.throws(() => loadTarget({ environment: 'nonprod', environmentsFile: file }, {}));
  }
});

test('Given an unsupported schema version, When resolving its profile, Then the loader rejects the document', t => {
  const { file } = inputs(t, { nonprod }, 2);
  assert.throws(() => loadTarget({ environment: 'nonprod', environmentsFile: file }, {}));
});

test('Given the optional schema version is absent, When resolving its profile, Then supported configuration still loads', t => {
  const { file } = inputs(t, { nonprod }, null);
  assert.equal(loadTarget({ environment: 'nonprod', environmentsFile: file }, {})?.targetUrl, nonprod.targetUrl);
});

test('Given sensitive query, fragment, and storage values, When summarizing a target, Then retained metadata excludes those values', t => {
  const { directory, file } = inputs(t, {
    production: { ...production, targetUrl: `${production.targetUrl}?code=private-query#private-fragment`, storageState: 'private-state.json' },
  });
  const privateState = path.join(directory, 'private-state.json');
  writeFileSync(privateState, JSON.stringify({ cookies: [{ name: 'session', value: 'private-cookie-value',
    domain: 'prod.example.test', path: '/', expires: -1, httpOnly: true, secure: true, sameSite: 'Lax' }], origins: [] }));
  const selected = loadTarget({ environment: 'production', environmentsFile: file }, {});
  assert.ok(selected);
  const summary = JSON.stringify(targetSummary(selected));
  assert.ok(summary.includes('prod.example.test'));
  assert.ok(summary.includes('production'));
  assert.ok(summary.includes(selected.configurationSha256));
  for (const value of ['private-query', 'private-fragment', 'private-state.json', 'private-cookie-value', privateState]) {
    assert.ok(!summary.includes(value), `Target summary must exclude ${value}`);
  }
});

test('Given synthetic fixture execution, When an environment selector is present, Then fixture execution rejects the remote target', () => {
  assert.doesNotThrow(() => rejectEnvironmentForFixtures({}));
  assert.throws(() => rejectEnvironmentForFixtures({ E2E_ENVIRONMENT: 'production' }));
  assert.throws(() => rejectEnvironmentForFixtures({ E2E_ENVIRONMENTS_FILE: 'private-environments.json' }));
});
