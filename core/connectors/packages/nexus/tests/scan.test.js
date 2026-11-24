import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { EventEmitter } from 'node:events';
import {
  configureScanTools,
  makeRequest,
  getInternalAppId,
  pollForResults,
  evaluateComponents,
  parseDependencies,
  parseMavenDependencies,
  extractVulnerabilities,
  buildTextSummary,
  openInBrowser
} from '../src/tools/scan.js';
import { createMockServer } from '@sc-node-mcp/shared-tests/helpers/mockServer';

// ── Mock node built-ins ───────────────────────────────────────────────────────

vi.mock('child_process', () => ({
  execSync: vi.fn(),
  exec: vi.fn()
}));

vi.mock('https', () => {
  const makeRequestMock = vi.fn();
  return {
    default: { request: makeRequestMock },
    request: makeRequestMock
  };
});

vi.mock('http', () => {
  const request = vi.fn();
  return { default: { request }, request };
});

vi.mock('../src/tools/generate-reports.js', () => ({
  buildJsonReport: vi.fn((opts) => ({
    summary: {
      applicationId: opts.applicationId,
      scanDate: new Date().toLocaleString(),
      mode: opts.mode || 'pipeline',
      scanMode: opts.scanMode || 'fresh',
      totalComponents: opts.totalComponentsScanned,
      vulnerableComponents: 0,
      totalVulnerabilities: 0,
      severityCounts: { Critical: 0, High: 0, Medium: 0, Low: 0 }
    },
    vulnerableModules: [],
    allVulnerabilities: []
  })),
  writeNexusReport: vi.fn(() => '/tmp/nexus-report')
}));

// ── Helpers ───────────────────────────────────────────────────────────────────

function makeMockConnection() {
  return () => ({
    baseUrl: 'https://sonatypenexus.global.standardchartered.com',
    headers: {
      Authorization: 'Basic dXNlcjpwYXNz',
      'Content-Type': 'application/json',
      Accept: 'application/json'
    }
  });
}

function mockJsonResponse(transport, data) {
  transport.request.mockImplementation((_options, callback) => {
    const response = new EventEmitter();
    response.statusCode = 200;
    response.headers = {};
    const request = new EventEmitter();
    request.write = vi.fn();
    request.end = () => {
      callback(response);
      response.emit('data', JSON.stringify(data));
      response.emit('end');
    };
    return request;
  });
}

// ── makeRequest ───────────────────────────────────────────────────────────────

describe('makeRequest', () => {
  afterEach(() => { vi.restoreAllMocks(); vi.unstubAllEnvs(); });

  it('honors NO_PROXY for a configured endpoint port', async () => {
    const https = await import('https');
    mockJsonResponse(https, { ok: true });
    vi.stubEnv('HTTPS_PROXY', 'http://proxy.example:8080');
    vi.stubEnv('NO_PROXY', 'nexus.example.com:8443');
    await makeRequest({ hostname: 'nexus.example.com', port: '8443', path: '/api', method: 'GET' });
    expect(https.request.mock.lastCall[0].agent).toBeUndefined();
    expect(process.env.HTTPS_PROXY).toBe('http://proxy.example:8080');
  });

  it('uses the configured proxy when NO_PROXY does not match the endpoint port', async () => {
    const https = await import('https');
    mockJsonResponse(https, { ok: true });
    vi.stubEnv('HTTPS_PROXY', 'http://proxy.example:8080');
    vi.stubEnv('NO_PROXY', 'nexus.example.com:8444');
    await makeRequest({ hostname: 'nexus.example.com', port: '8443', path: '/api', method: 'GET' });
    expect(https.request.mock.lastCall[0].agent).toBeDefined();
  });

  it('resolves with parsed JSON body and statusCode', async () => {
    const https = await import('https');
    https.request.mockImplementation((_opts, callback) => {
      const res = new EventEmitter();
      res.statusCode = 200;
      res.headers = {};
      const req = new EventEmitter();
      req.write = vi.fn();
      req.end = () => {
        callback(res);
        res.emit('data', JSON.stringify({ ok: true }));
        res.emit('end');
      };
      return req;
    });

    const result = await makeRequest({ hostname: 'nexus.example.com', path: '/api', method: 'GET', headers: {} });
    expect(result.statusCode).toBe(200);
    expect(result.data).toEqual({ ok: true });
  });

  it('falls back to raw text when body is not valid JSON', async () => {
    const https = await import('https');
    https.request.mockImplementation((_opts, callback) => {
      const res = new EventEmitter();
      res.statusCode = 200;
      res.headers = {};
      const req = new EventEmitter();
      req.write = vi.fn();
      req.end = () => {
        callback(res);
        res.emit('data', 'NOT_JSON{{');
        res.emit('end');
      };
      return req;
    });

    const result = await makeRequest({ hostname: 'nexus.example.com', path: '/api', method: 'GET', headers: {} });
    expect(result.data).toBe('NOT_JSON{{');
  });

  it('writes string postData directly', async () => {
    const https = await import('https');
    const writeSpy = vi.fn();
    https.request.mockImplementation((_opts, callback) => {
      const res = new EventEmitter();
      res.statusCode = 200;
      res.headers = {};
      const req = new EventEmitter();
      req.write = writeSpy;
      req.end = () => { callback(res); res.emit('data', '{}'); res.emit('end'); };
      return req;
    });

    await makeRequest({ hostname: 'nexus.example.com', path: '/api', method: 'POST', headers: {} }, 'raw-string');
    expect(writeSpy).toHaveBeenCalledWith('raw-string');
  });

  it('stringifies object postData', async () => {
    const https = await import('https');
    const writeSpy = vi.fn();
    https.request.mockImplementation((_opts, callback) => {
      const res = new EventEmitter();
      res.statusCode = 200;
      res.headers = {};
      const req = new EventEmitter();
      req.write = writeSpy;
      req.end = () => { callback(res); res.emit('data', '{}'); res.emit('end'); };
      return req;
    });

    await makeRequest({ hostname: 'nexus.example.com', path: '/api', method: 'POST', headers: {} }, { foo: 'bar' });
    expect(writeSpy).toHaveBeenCalledWith(JSON.stringify({ foo: 'bar' }));
  });

  it('rejects when the request emits an error', async () => {
    const https = await import('https');
    https.request.mockImplementation(() => {
      const req = new EventEmitter();
      req.write = vi.fn();
      req.end = () => { req.emit('error', new Error('ECONNREFUSED')); };
      return req;
    });

    await expect(makeRequest({ hostname: 'nexus.example.com', path: '/api', method: 'GET', headers: {} }))
      .rejects.toThrow('ECONNREFUSED');
  });
});

// ── getInternalAppId ──────────────────────────────────────────────────────────

describe('getInternalAppId', () => {
  afterEach(() => { vi.restoreAllMocks(); });

  it('preserves a configured endpoint port and base path', async () => {
    const https = await import('https');
    mockJsonResponse(https, { applications: [{ id: 'internal-abc' }] });
    expect(await getInternalAppId('https://nexus.example.com:8443/nexus', 'Basic xxx', 'MY_APP'))
      .toBe('internal-abc');
    expect(https.request.mock.lastCall[0]).toMatchObject({
      protocol: 'https:', hostname: 'nexus.example.com', port: 8443,
      path: '/nexus/api/v2/applications?publicId=MY_APP'
    });
  });

  it('uses HTTP for an explicitly configured HTTP endpoint', async () => {
    const http = await import('http');
    mockJsonResponse(http, { applications: [{ id: 'internal-http' }] });
    expect(await getInternalAppId('http://nexus.example.com:8080/nexus', 'Basic xxx', 'MY_APP'))
      .toBe('internal-http');
    expect(http.request.mock.lastCall[0]).toMatchObject({
      protocol: 'http:', hostname: 'nexus.example.com', port: 8080,
      path: '/nexus/api/v2/applications?publicId=MY_APP'
    });
  });

  it('returns internalId when application is found', async () => {
    const https = await import('https');
    https.request.mockImplementation((_opts, callback) => {
      const res = new EventEmitter();
      res.statusCode = 200;
      res.headers = {};
      const req = new EventEmitter();
      req.write = vi.fn();
      req.end = () => {
        callback(res);
        res.emit('data', JSON.stringify({ applications: [{ id: 'internal-abc' }] }));
        res.emit('end');
      };
      return req;
    });

    const id = await getInternalAppId('nexus.example.com', 'Basic xxx', 'MY_APP');
    expect(id).toBe('internal-abc');
  });

  it('throws when applications array is empty', async () => {
    const https = await import('https');
    https.request.mockImplementation((_opts, callback) => {
      const res = new EventEmitter();
      res.statusCode = 200;
      res.headers = {};
      const req = new EventEmitter();
      req.write = vi.fn();
      req.end = () => {
        callback(res);
        res.emit('data', JSON.stringify({ applications: [] }));
        res.emit('end');
      };
      return req;
    });

    await expect(getInternalAppId('nexus.example.com', 'Basic xxx', 'MISSING'))
      .rejects.toThrow(/not found/i);
  });

  it('throws when status code is non-200', async () => {
    const https = await import('https');
    https.request.mockImplementation((_opts, callback) => {
      const res = new EventEmitter();
      res.statusCode = 404;
      res.headers = {};
      const req = new EventEmitter();
      req.write = vi.fn();
      req.end = () => { callback(res); res.emit('data', '{}'); res.emit('end'); };
      return req;
    });

    await expect(getInternalAppId('nexus.example.com', 'Basic xxx', 'NOT_FOUND'))
      .rejects.toThrow(/404/);
  });
});

// ── pollForResults ────────────────────────────────────────────────────────────

describe('pollForResults', () => {
  afterEach(() => { vi.restoreAllMocks(); });

  it.each(['/api/results', '/nexus/api/results', 'https://nexus.example.com:8443/nexus/api/results'])(
    'keeps the configured endpoint for results path %s', async (resultsPath) => {
      const https = await import('https');
      mockJsonResponse(https, { results: [] });
      await pollForResults('https://nexus.example.com:8443/nexus', 'Basic xxx', resultsPath);
      expect(https.request.mock.lastCall[0]).toMatchObject({
        hostname: 'nexus.example.com', port: 8443, path: '/nexus/api/results'
      });
    }
  );

  it('rejects a results URL on another origin before sending credentials', async () => {
    const https = await import('https');
    https.request.mockClear();
    await expect(pollForResults('https://nexus.example.com', 'Basic xxx', 'https://other.example/results'))
      .rejects.toThrow('configured endpoint origin');
    expect(https.request).not.toHaveBeenCalled();
  });

  it('returns results immediately on first success', async () => {
    const https = await import('https');
    https.request.mockImplementation((_opts, callback) => {
      const res = new EventEmitter();
      res.statusCode = 200;
      res.headers = {};
      const req = new EventEmitter();
      req.write = vi.fn();
      req.end = () => {
        callback(res);
        res.emit('data', JSON.stringify({ results: [{ component: 'a' }] }));
        res.emit('end');
      };
      return req;
    });

    const data = await pollForResults('nexus.example.com', 'Basic xxx', '/api/results', 3, 0);
    expect(data.results).toHaveLength(1);
  });

  it('throws when evaluation isError flag is set', async () => {
    const https = await import('https');
    https.request.mockImplementation((_opts, callback) => {
      const res = new EventEmitter();
      res.statusCode = 200;
      res.headers = {};
      const req = new EventEmitter();
      req.write = vi.fn();
      req.end = () => {
        callback(res);
        res.emit('data', JSON.stringify({ isError: true, errorMessage: 'Scan failed' }));
        res.emit('end');
      };
      return req;
    });

    await expect(pollForResults('nexus.example.com', 'Basic xxx', '/api/results', 1, 0))
      .rejects.toThrow('Scan failed');
  });

  it('throws timeout error when maxAttempts exceeded without results', async () => {
    const https = await import('https');
    https.request.mockImplementation((_opts, callback) => {
      const res = new EventEmitter();
      res.statusCode = 202;
      res.headers = {};
      const req = new EventEmitter();
      req.write = vi.fn();
      req.end = () => { callback(res); res.emit('data', '{}'); res.emit('end'); };
      return req;
    });

    await expect(pollForResults('nexus.example.com', 'Basic xxx', '/api/results', 1, 0))
      .rejects.toThrow(/timeout/i);
  });

  it('prepends slash to resultsPath when missing', async () => {
    const https = await import('https');
    let capturedPath;
    https.request.mockImplementation((opts, callback) => {
      capturedPath = opts.path;
      const res = new EventEmitter();
      res.statusCode = 200;
      res.headers = {};
      const req = new EventEmitter();
      req.write = vi.fn();
      req.end = () => {
        callback(res);
        res.emit('data', JSON.stringify({ components: [] }));
        res.emit('end');
      };
      return req;
    });

    await pollForResults('nexus.example.com', 'Basic xxx', 'api/results/no-slash', 1, 0);
    expect(capturedPath).toBe('/api/results/no-slash');
  });
});

// ── evaluateComponents ────────────────────────────────────────────────────────

describe('evaluateComponents', () => {
  afterEach(() => { vi.restoreAllMocks(); });

  it('chains to pollForResults when 202 response contains resultsUrl', async () => {
    const https = await import('https');
    let callCount = 0;
    https.request.mockImplementation((_opts, callback) => {
      callCount += 1;
      const res = new EventEmitter();
      res.statusCode = callCount === 1 ? 202 : 200;
      res.headers = {};
      const req = new EventEmitter();
      req.write = vi.fn();
      req.end = () => {
        callback(res);
        if (callCount === 1) {
          res.emit('data', JSON.stringify({ resultsUrl: '/api/v2/evaluation/results/abc' }));
        } else {
          res.emit('data', JSON.stringify({ results: [{ component: 'lodash' }] }));
        }
        res.emit('end');
      };
      return req;
    });

    const result = await evaluateComponents('nexus.example.com', 'Basic xxx', 'app-id', []);
    expect(result.results).toHaveLength(1);
    expect(callCount).toBe(2);
  });

  it('returns data directly when 200 with no resultsUrl', async () => {
    const https = await import('https');
    https.request.mockImplementation((_opts, callback) => {
      const res = new EventEmitter();
      res.statusCode = 200;
      res.headers = {};
      const req = new EventEmitter();
      req.write = vi.fn();
      req.end = () => {
        callback(res);
        res.emit('data', JSON.stringify({ components: [{ id: 'x' }] }));
        res.emit('end');
      };
      return req;
    });

    const result = await evaluateComponents('nexus.example.com', 'Basic xxx', 'app-id', []);
    expect(result.components).toHaveLength(1);
  });

  it('throws when status is 500', async () => {
    const https = await import('https');
    https.request.mockImplementation((_opts, callback) => {
      const res = new EventEmitter();
      res.statusCode = 500;
      res.headers = {};
      const req = new EventEmitter();
      req.write = vi.fn();
      req.end = () => { callback(res); res.emit('data', '{}'); res.emit('end'); };
      return req;
    });

    await expect(evaluateComponents('nexus.example.com', 'Basic xxx', 'app-id', []))
      .rejects.toThrow(/500/);
  });
});

// ── parseDependencies ─────────────────────────────────────────────────────────

describe('parseDependencies', () => {
  let tmpDir;
  let realFs;

  beforeEach(async () => {
    realFs = await import('fs');
    const os = await import('os');
    const path = await import('path');
    tmpDir = realFs.mkdtempSync(path.join(os.tmpdir(), 'nexus-parse-'));
  });

  afterEach(async () => {
    const realFs2 = await import('fs');
    realFs2.rmSync(tmpDir, { recursive: true, force: true });
    vi.restoreAllMocks();
  });

  it('returns components from prod deps only when no lockfile (pipeline mode)', async () => {
    const path = await import('path');
    realFs.writeFileSync(
      path.join(tmpDir, 'package.json'),
      JSON.stringify({ dependencies: { lodash: '^4.17.21' }, devDependencies: { jest: '^27.0.0' } })
    );

    const { components, directDepNames, devDepNames } = parseDependencies(tmpDir, false);
    // No node_modules & no lockfiles → falls back to direct deps from package.json
    expect(components.some(c => c.packageUrl.startsWith('pkg:npm/lodash@'))).toBe(true);
    expect(directDepNames.has('lodash')).toBe(true);
    expect(devDepNames.has('jest')).toBe(true);
  });

  it('returns all deps (prod + dev) in deep mode', async () => {
    const path = await import('path');
    realFs.writeFileSync(
      path.join(tmpDir, 'package.json'),
      JSON.stringify({ dependencies: { lodash: '^4.17.21' }, devDependencies: { jest: '^27.0.0' } })
    );

    const { components } = parseDependencies(tmpDir, true);
    // deep mode: jest from devDeps should also appear
    // (falls back to direct deps when no node_modules)
    const names = components.map(c => c.packageUrl);
    expect(names.some(n => n.includes('lodash'))).toBe(true);
    expect(names.some(n => n.includes('jest'))).toBe(true);
  });

  it('reads installed versions from node_modules (deep mode)', async () => {
    const path = await import('path');
    realFs.writeFileSync(
      path.join(tmpDir, 'package.json'),
      JSON.stringify({ dependencies: { lodash: '^4.17.21' } })
    );

    // Create mock node_modules/lodash/package.json
    const nmPath = path.join(tmpDir, 'node_modules', 'lodash');
    realFs.mkdirSync(nmPath, { recursive: true });
    realFs.writeFileSync(path.join(nmPath, 'package.json'), JSON.stringify({ name: 'lodash', version: '4.17.21' }));

    const { components } = parseDependencies(tmpDir, true);
    expect(components[0].packageUrl).toBe('pkg:npm/lodash@4.17.21');
  });

  it('handles scoped packages in node_modules (deep mode)', async () => {
    const path = await import('path');
    realFs.writeFileSync(
      path.join(tmpDir, 'package.json'),
      JSON.stringify({ dependencies: { '@babel/core': '^7.0.0' } })
    );

    const nmPath = path.join(tmpDir, 'node_modules', '@babel', 'core');
    realFs.mkdirSync(nmPath, { recursive: true });
    realFs.writeFileSync(path.join(nmPath, 'package.json'), JSON.stringify({ name: '@babel/core', version: '7.21.0' }));

    const { components } = parseDependencies(tmpDir, true);
    expect(components[0].packageUrl).toBe('pkg:npm/@babel/core@7.21.0');
  });

  it('uses lockfile v2 packages map for prod-only filtering', async () => {
    const path = await import('path');
    realFs.writeFileSync(
      path.join(tmpDir, 'package.json'),
      JSON.stringify({ dependencies: { lodash: '^4.17.21' }, devDependencies: { jest: '^27.0.0' } })
    );

    const lock = {
      lockfileVersion: 2,
      packages: {
        '': {},
        'node_modules/lodash': { version: '4.17.21' },
        'node_modules/jest': { version: '27.0.0', dev: true }
      }
    };
    realFs.writeFileSync(path.join(tmpDir, 'package-lock.json'), JSON.stringify(lock));

    const { components } = parseDependencies(tmpDir, false);
    const names = components.map(c => c.packageUrl);
    // lodash should be included (prod); jest should be excluded (dev: true)
    expect(names.some(n => n.includes('lodash'))).toBe(true);
    expect(names.some(n => n.includes('jest'))).toBe(false);
  });

  it('falls back gracefully when lockfile JSON is malformed', async () => {
    const path = await import('path');
    realFs.writeFileSync(
      path.join(tmpDir, 'package.json'),
      JSON.stringify({ dependencies: { lodash: '^4.17.21' } })
    );
    realFs.writeFileSync(path.join(tmpDir, 'package-lock.json'), 'INVALID{{JSON');

    // Should not throw, falls back to alternative strategy
    expect(() => parseDependencies(tmpDir, false)).not.toThrow();
  });

  it('uses BFS traversal for yarn project (no lockfile v2)', async () => {
    const path = await import('path');
    realFs.writeFileSync(
      path.join(tmpDir, 'package.json'),
      JSON.stringify({ dependencies: { lodash: '^4.17.0' } })
    );

    // Simulate node_modules/lodash with its own dep
    const nmLodash = path.join(tmpDir, 'node_modules', 'lodash');
    realFs.mkdirSync(nmLodash, { recursive: true });
    realFs.writeFileSync(path.join(nmLodash, 'package.json'), JSON.stringify({ name: 'lodash', version: '4.17.21', dependencies: {} }));

    const { components } = parseDependencies(tmpDir, false);
    // BFS should pick up lodash
    expect(components[0].packageUrl).toBe('pkg:npm/lodash@4.17.21');
  });
});

// ── extractVulnerabilities ────────────────────────────────────────────────────

describe('extractVulnerabilities', () => {
  const directNames = new Set(['lodash']);
  const devNames = new Set(['jest']);

  function makeApiResult(overrides = {}) {
    return {
      component: {
        componentIdentifier: {
          coordinates: { packageId: 'lodash', version: '4.17.20' }
        }
      },
      policyData: { policyViolations: [{ policyName: 'Security' }] },
      securityData: {
        securityIssues: [{
          reference: 'CVE-2021-23337',
          severity: 7.2,
          threatCategory: 'severe',
          title: 'Prototype pollution'
        }]
      },
      ...overrides
    };
  }

  it('extracts a CVE from a direct dependency', () => {
    const apiResults = { results: [makeApiResult()] };
    const vulns = extractVulnerabilities(apiResults, directNames, devNames, false);
    expect(vulns).toHaveLength(1);
    expect(vulns[0].component).toBe('lodash');
    expect(vulns[0].vulnId).toBe('CVE-2021-23337');
    expect(vulns[0].dependency).toBe('direct');
  });

  it('F1 – skips pure dev dependencies in pipeline mode', () => {
    const pureDevResult = {
      component: {
        componentIdentifier: { coordinates: { packageId: 'jest', version: '27.0.0' } }
      },
      policyData: { policyViolations: [{ policyName: 'Security' }] },
      securityData: { securityIssues: [{ reference: 'CVE-2022-99999', severity: 5.0 }] }
    };
    // jest is in devNames but not in directNames (prod)
    const directNoProd = new Set(); // jest not in prod deps
    const devWithJest = new Set(['jest']);
    const vulns = extractVulnerabilities({ results: [pureDevResult] }, directNoProd, devWithJest, false);
    expect(vulns).toHaveLength(0);
  });

  it('F3 – skips CVSS < 4.0 in pipeline mode', () => {
    const lowResult = makeApiResult();
    lowResult.securityData.securityIssues[0].severity = 2.0;
    const vulns = extractVulnerabilities({ results: [lowResult] }, directNames, devNames, false);
    expect(vulns).toHaveLength(0);
  });

  it('F5 – skips components with empty policyViolations in pipeline mode', () => {
    const noPolicyResult = makeApiResult();
    noPolicyResult.policyData = { policyViolations: [] };
    const vulns = extractVulnerabilities({ results: [noPolicyResult] }, directNames, devNames, false);
    expect(vulns).toHaveLength(0);
  });

  it('F6 – skips sonatype-* vulnerability IDs in pipeline mode', () => {
    const sonatypeResult = makeApiResult();
    sonatypeResult.securityData.securityIssues[0].reference = 'sonatype-2021-0001';
    const vulns = extractVulnerabilities({ results: [sonatypeResult] }, directNames, devNames, false);
    expect(vulns).toHaveLength(0);
  });

  it('deep mode: includes dev deps and low CVSS findings', () => {
    const devResult = {
      component: { componentIdentifier: { coordinates: { packageId: 'jest', version: '27.0.0' } } },
      securityData: { securityIssues: [{ reference: 'CVE-2022-99999', severity: 1.0 }] }
    };
    const vulns = extractVulnerabilities({ results: [devResult] }, new Set(), new Set(['jest']), true);
    expect(vulns).toHaveLength(1);
    expect(vulns[0].component).toBe('jest');
  });

  it('extracts sonatype-* IDs in deep mode', () => {
    const result = makeApiResult();
    result.securityData.securityIssues[0].reference = 'sonatype-2021-0001';
    const vulns = extractVulnerabilities({ results: [result] }, directNames, devNames, true);
    expect(vulns).toHaveLength(1);
    expect(vulns[0].vulnId).toBe('sonatype-2021-0001');
  });

  it('marks transitive dependencies correctly', () => {
    const transitiveResult = {
      component: { componentIdentifier: { coordinates: { packageId: 'minimist', version: '1.2.5' } } },
      policyData: { policyViolations: [{ policyName: 'Security' }] },
      securityData: { securityIssues: [{ reference: 'CVE-2021-44906', severity: 7.5 }] }
    };
    const vulns = extractVulnerabilities({ results: [transitiveResult] }, directNames, devNames, false);
    expect(vulns).toHaveLength(1);
    expect(vulns[0].dependency).toBe('transitive');
  });

  it('handles components array instead of results array', () => {
    const apiResults = { components: [makeApiResult()] };
    const vulns = extractVulnerabilities(apiResults, directNames, devNames, false);
    expect(vulns).toHaveLength(1);
  });

  it('handles plain array as apiResults', () => {
    const vulns = extractVulnerabilities([makeApiResult()], directNames, devNames, false);
    expect(vulns).toHaveLength(1);
  });

  it('skips components with no securityIssues', () => {
    const noSecResult = makeApiResult();
    noSecResult.securityData = {};
    const vulns = extractVulnerabilities({ results: [noSecResult] }, directNames, devNames, false);
    expect(vulns).toHaveLength(0);
  });

  it('maps Critical threatCategory to Critical severity', () => {
    const critResult = makeApiResult();
    critResult.securityData.securityIssues[0].threatCategory = 'critical';
    critResult.securityData.securityIssues[0].severity = 9.5;
    const vulns = extractVulnerabilities({ results: [critResult] }, directNames, devNames, false);
    expect(vulns[0].severity).toBe('Critical');
  });
});

// ── buildTextSummary ──────────────────────────────────────────────────────────

describe('buildTextSummary', () => {
  it('includes application ID in output', () => {
    const report = {
      summary: {
        applicationId: 'TEST__PROD__my-app',
        scanDate: '1/1/2025',
        mode: 'pipeline',
        totalComponents: 100,
        vulnerableComponents: 2,
        severityCounts: { Critical: 0, High: 1, Medium: 1, Low: 0 }
      },
      vulnerableModules: []
    };
    const text = buildTextSummary(report, '/some/dir');
    expect(text).toContain('TEST__PROD__my-app');
  });

  it('shows no vulnerabilities message when total is zero', () => {
    const report = {
      summary: {
        applicationId: 'TEST',
        scanDate: '1/1/2025',
        mode: 'pipeline',
        totalComponents: 50,
        vulnerableComponents: 0,
        severityCounts: { Critical: 0, High: 0, Medium: 0, Low: 0 }
      },
      vulnerableModules: []
    };
    const text = buildTextSummary(report, '/some/dir');
    expect(text).toContain('No security vulnerabilities');
  });

  it('lists vulnerable modules with CVE details', () => {
    const report = {
      summary: {
        applicationId: 'TEST',
        scanDate: '1/1/2025',
        mode: 'deep',
        totalComponents: 50,
        vulnerableComponents: 1,
        severityCounts: { Critical: 1, High: 0, Medium: 0, Low: 0 }
      },
      vulnerableModules: [{
        module: 'lodash',
        currentVersion: '4.17.20',
        dependency: 'direct',
        cves: [{ severity: 'Critical', score: '9.8', cveId: 'CVE-2021-99999', isNewCve: false, fixVersion: '4.17.21' }]
      }]
    };
    const text = buildTextSummary(report, '/reports');
    expect(text).toContain('lodash');
    expect(text).toContain('CVE-2021-99999');
    expect(text).toContain('Critical');
  });

  it('shows [New CVE] badge when isNewCve is true', () => {
    const report = {
      summary: {
        applicationId: 'TEST',
        scanDate: '1/1/2025',
        mode: 'pipeline',
        totalComponents: 10,
        vulnerableComponents: 1,
        severityCounts: { Critical: 0, High: 1, Medium: 0, Low: 0 }
      },
      vulnerableModules: [{
        module: 'some-pkg',
        currentVersion: '1.0.0',
        dependency: 'direct',
        cves: [{ severity: 'High', score: '7.5', cveId: 'CVE-2026-12345', isNewCve: true, fixVersion: '1.0.1' }]
      }]
    };
    const text = buildTextSummary(report, '/reports');
    expect(text).toContain('[New CVE]');
  });

  it('shows Low count when sc.Low > 0', () => {
    const report = {
      summary: {
        applicationId: 'TEST',
        scanDate: '1/1/2025',
        mode: 'pipeline',
        totalComponents: 10,
        vulnerableComponents: 1,
        severityCounts: { Critical: 0, High: 0, Medium: 0, Low: 2 }
      },
      vulnerableModules: [{
        module: 'some-pkg',
        currentVersion: '1.0.0',
        dependency: 'direct',
        cves: [{ severity: 'Low', score: '2.0', cveId: 'CVE-2020-1234', isNewCve: false, fixVersion: null }]
      }]
    };
    const text = buildTextSummary(report, '/reports');
    expect(text).toContain('Low');
    expect(text).toContain('2');
  });
});

// ── openInBrowser ─────────────────────────────────────────────────────────────

describe('openInBrowser', () => {
  afterEach(() => { vi.restoreAllMocks(); });

  it('does not throw on darwin', () => {
    vi.stubGlobal('process', { ...process, platform: 'darwin' });
    expect(() => openInBrowser('/tmp/report.html')).not.toThrow();
  });

  it('does not throw on win32', () => {
    vi.stubGlobal('process', { ...process, platform: 'win32' });
    expect(() => openInBrowser('/tmp/report.html')).not.toThrow();
  });

  it('does not throw on linux', () => {
    vi.stubGlobal('process', { ...process, platform: 'linux' });
    expect(() => openInBrowser('/tmp/report.html')).not.toThrow();
  });
});

// ── configureScanTools ────────────────────────────────────────────────────────

describe('configureScanTools', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = createMockServer();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('registers nexus_scan_vulnerabilities on the server', () => {
    configureScanTools(mockServer, makeMockConnection());
    const names = mockServer.getRegisteredTools().map((t) => t.name);
    expect(names).toContain('nexus_scan_vulnerabilities');
  });

  it('tool schema requires applicationId', () => {
    configureScanTools(mockServer, makeMockConnection());
    const tool = mockServer.getTool('nexus_scan_vulnerabilities');
    expect(tool.schema).toHaveProperty('applicationId');
  });

  it('tool schema has optional projectPath and deepMode', () => {
    configureScanTools(mockServer, makeMockConnection());
    const tool = mockServer.getTool('nexus_scan_vulnerabilities');
    expect(tool.schema).toHaveProperty('projectPath');
    expect(tool.schema).toHaveProperty('deepMode');
  });

  it('returns isError when package.json is not found at projectPath', async () => {
    configureScanTools(mockServer, makeMockConnection());
    const response = await mockServer.invokeTool('nexus_scan_vulnerabilities', {
      applicationId: 'TEST__PROD__my-service',
      projectPath: '/nonexistent/path/xyz123'
    });
    expect(response.isError).toBe(true);
    expect(response.content[0].text).toMatch(/No package\.json or pom\.xml found in/i);
  });

  it('returns isError when Nexus app lookup fails', async () => {
    const https = await import('https');
    const { EventEmitter } = await import('events');

    https.request.mockImplementation((_opts, callback) => {
      const res = new EventEmitter();
      res.statusCode = 404;
      res.headers = {};

      const req = new EventEmitter();
      req.end = () => {
        callback(res);
        res.emit('data', JSON.stringify({ applications: [] }));
        res.emit('end');
      };
      req.write = vi.fn();
      return req;
    });

    const { execSync } = await import('child_process');
    execSync.mockImplementation(() => {});

    // Use a temp dir that has a minimal package.json
    const os = await import('os');
    const fs = await import('fs');
    const p  = await import('path');
    const tmpDir = fs.mkdtempSync(p.join(os.tmpdir(), 'nexus-test-'));
    fs.writeFileSync(p.join(tmpDir, 'package.json'), JSON.stringify({ dependencies: {} }));

    configureScanTools(mockServer, makeMockConnection());
    const response = await mockServer.invokeTool('nexus_scan_vulnerabilities', {
      applicationId: 'NOT_FOUND',
      projectPath: tmpDir
    });

    expect(response.isError).toBe(true);
    expect(response.content[0].text).toMatch(/not found|404/i);

    fs.rmSync(tmpDir, { recursive: true });
  });

  it('returns success with text summary when scan completes (no vulnerabilities)', async () => {
    const https = await import('https');
    const { EventEmitter } = await import('events');
    const { execSync } = await import('child_process');
    const fs = await import('fs');
    const os = await import('os');
    const p = await import('path');

    execSync.mockImplementation(() => '');

    let callCount = 0;
    https.request.mockImplementation((_opts, callback) => {
      callCount += 1;
      const res = new EventEmitter();
      res.statusCode = 200;
      res.headers = {};
      const req = new EventEmitter();
      req.write = vi.fn();
      req.end = () => {
        callback(res);
        if (callCount === 1) {
          // getInternalAppId
          res.emit('data', JSON.stringify({ applications: [{ id: 'internal-123' }] }));
        } else if (callCount === 2) {
          // evaluateComponents
          res.emit('data', JSON.stringify({ components: [] }));
        }
        res.emit('end');
      };
      return req;
    });

    const tmpDir = fs.mkdtempSync(p.join(os.tmpdir(), 'nexus-full-'));
    fs.writeFileSync(p.join(tmpDir, 'package.json'), JSON.stringify({ dependencies: { lodash: '^4.17.21' } }));

    configureScanTools(mockServer, makeMockConnection());
    const response = await mockServer.invokeTool('nexus_scan_vulnerabilities', {
      applicationId: 'TEST__PROD__app',
      projectPath: tmpDir
    });

    // Should get a result (text summary from mocked buildTextSummary)
    expect(response.isError).toBeUndefined();
    expect(response.content).toBeDefined();

    fs.rmSync(tmpDir, { recursive: true });
  });

  it('returns no-components message when parseDependencies returns empty', async () => {
    const https = await import('https');
    const { EventEmitter } = await import('events');
    const { execSync } = await import('child_process');
    const fs = await import('fs');
    const os = await import('os');
    const p = await import('path');

    execSync.mockImplementation(() => '');
    https.request.mockImplementation((_opts, callback) => {
      const res = new EventEmitter();
      res.statusCode = 200;
      res.headers = {};
      const req = new EventEmitter();
      req.write = vi.fn();
      req.end = () => {
        callback(res);
        res.emit('data', JSON.stringify({ applications: [{ id: 'internal-123' }] }));
        res.emit('end');
      };
      return req;
    });

    const tmpDir = fs.mkdtempSync(p.join(os.tmpdir(), 'nexus-empty-'));
    // package.json with NO dependencies → components will be empty
    fs.writeFileSync(p.join(tmpDir, 'package.json'), JSON.stringify({}));

    configureScanTools(mockServer, makeMockConnection());
    const response = await mockServer.invokeTool('nexus_scan_vulnerabilities', {
      applicationId: 'TEST__PROD__app',
      projectPath: tmpDir
    });

    expect(response.isError).toBeUndefined();
    expect(response.content[0].text).toContain('No components found');

    fs.rmSync(tmpDir, { recursive: true });
  });
});

// ── Additional parseDependencies edge cases ───────────────────────────────────

describe('parseDependencies — edge cases', () => {
  let tmpDir;
  let realFs;

  beforeEach(async () => {
    realFs = await import('fs');
    const os = await import('os');
    const path = await import('path');
    tmpDir = realFs.mkdtempSync(path.join(os.tmpdir(), 'nexus-parse2-'));
  });

  afterEach(async () => {
    const realFs2 = await import('fs');
    realFs2.rmSync(tmpDir, { recursive: true, force: true });
    vi.restoreAllMocks();
  });

  it('skips "npm" package name during BFS traversal', async () => {
    const path = await import('path');
    realFs.writeFileSync(
      path.join(tmpDir, 'package.json'),
      JSON.stringify({ dependencies: { npm: '^8.0.0', lodash: '^4.17.0' } })
    );
    // npm in node_modules as a dep (BFS should skip it)
    const nmLodash = path.join(tmpDir, 'node_modules', 'lodash');
    realFs.mkdirSync(nmLodash, { recursive: true });
    realFs.writeFileSync(path.join(nmLodash, 'package.json'), JSON.stringify({ name: 'lodash', version: '4.17.21', dependencies: {} }));

    const { components } = parseDependencies(tmpDir, false);
    const names = components.map(c => c.packageUrl);
    expect(names.some(n => n.includes('lodash'))).toBe(true);
    // 'npm' should be excluded from BFS
    expect(names.some(n => n.startsWith('pkg:npm/npm@'))).toBe(false);
  });

  it('handles missing package.json in node_modules (existsSync returns false for dep)', async () => {
    const path = await import('path');
    realFs.writeFileSync(
      path.join(tmpDir, 'package.json'),
      JSON.stringify({ dependencies: { lodash: '^4.17.0', 'missing-pkg': '^1.0.0' } })
    );
    // Only lodash exists in node_modules, missing-pkg does not
    const nmLodash = path.join(tmpDir, 'node_modules', 'lodash');
    realFs.mkdirSync(nmLodash, { recursive: true });
    realFs.writeFileSync(path.join(nmLodash, 'package.json'), JSON.stringify({ name: 'lodash', version: '4.17.21' }));

    const { components } = parseDependencies(tmpDir, false);
    expect(components.some(c => c.packageUrl.includes('lodash'))).toBe(true);
    // missing-pkg skipped (existsSync returns false in BFS)
    expect(components.some(c => c.packageUrl.includes('missing-pkg'))).toBe(false);
  });

  it('handles malformed package.json in node_modules during BFS (catch ignores it)', async () => {
    const path = await import('path');
    realFs.writeFileSync(
      path.join(tmpDir, 'package.json'),
      JSON.stringify({ dependencies: { lodash: '^4.17.0' } })
    );
    const nmLodash = path.join(tmpDir, 'node_modules', 'lodash');
    realFs.mkdirSync(nmLodash, { recursive: true });
    realFs.writeFileSync(path.join(nmLodash, 'package.json'), 'INVALID JSON{'); // malformed

    // Should not throw; malformed pkg.json is silently skipped
    expect(() => parseDependencies(tmpDir, false)).not.toThrow();
  });

  it('uses "0.0.0" when dep version spec becomes empty after stripping prefix chars', async () => {
    const path = await import('path');
    // '*' after stripping becomes '' → fallback '0.0.0'
    realFs.writeFileSync(
      path.join(tmpDir, 'package.json'),
      JSON.stringify({ dependencies: { 'some-pkg': '*' } })
    );

    const { components } = parseDependencies(tmpDir, false);
    const comp = components.find(c => c.packageUrl.includes('some-pkg'));
    expect(comp.packageUrl).toBe('pkg:npm/some-pkg@0.0.0');
  });

  it('uses lockfile v1 (without packages) — falls through to BFS', async () => {
    const path = await import('path');
    realFs.writeFileSync(
      path.join(tmpDir, 'package.json'),
      JSON.stringify({ dependencies: { lodash: '^4.17.0' } })
    );
    // lockfileVersion 1 has no 'packages' field
    realFs.writeFileSync(path.join(tmpDir, 'package-lock.json'), JSON.stringify({ lockfileVersion: 1, dependencies: {} }));

    const nmLodash = path.join(tmpDir, 'node_modules', 'lodash');
    realFs.mkdirSync(nmLodash, { recursive: true });
    realFs.writeFileSync(path.join(nmLodash, 'package.json'), JSON.stringify({ name: 'lodash', version: '4.17.21' }));

    const { components } = parseDependencies(tmpDir, false);
    expect(components.some(c => c.packageUrl.includes('lodash'))).toBe(true);
  });
});

// ── Additional extractVulnerabilities edge cases ──────────────────────────────

describe('extractVulnerabilities — edge cases', () => {
  const directNames = new Set(['lodash']);
  const devNames = new Set(['jest']);

  it('skips component where pkgName is "npm"', () => {
    const result = {
      component: { componentIdentifier: { coordinates: { packageId: 'npm', version: '8.0.0' } } },
      policyData: { policyViolations: [{ policyName: 'Security' }] },
      securityData: { securityIssues: [{ reference: 'CVE-2022-1', severity: 5.0 }] }
    };
    const vulns = extractVulnerabilities({ results: [result] }, directNames, devNames, false);
    expect(vulns).toHaveLength(0);
  });

  it('uses "0.0.0" when coordinates version is missing', () => {
    const result = {
      component: { componentIdentifier: { coordinates: { packageId: 'lodash' } } }, // no version
      policyData: { policyViolations: [{ policyName: 'Security' }] },
      securityData: { securityIssues: [{ reference: 'CVE-2021-99', severity: 5.0 }] }
    };
    const vulns = extractVulnerabilities({ results: [result] }, directNames, devNames, false);
    expect(vulns[0].version).toBe('0.0.0');
  });

  it('uses "N/A" when reference is empty and no CVE/sonatype match', () => {
    const result = {
      component: { componentIdentifier: { coordinates: { packageId: 'lodash', version: '4.17.20' } } },
      policyData: { policyViolations: [{ policyName: 'Security' }] },
      securityData: { securityIssues: [{ reference: '', severity: 5.0, threatCategory: 'moderate' }] }
    };
    const vulns = extractVulnerabilities({ results: [result] }, directNames, devNames, false);
    expect(vulns[0].vulnId).toBe('N/A');
  });

  it('sets severity to "Unknown" when cvss is 0 and no threatCategory', () => {
    const result = {
      component: { componentIdentifier: { coordinates: { packageId: 'lodash', version: '4.17.20' } } },
      securityData: { securityIssues: [{ reference: 'CVE-2021-1', severity: 0 }] }
    };
    // deep mode to skip F3/F5 filters
    const vulns = extractVulnerabilities({ results: [result] }, directNames, devNames, true);
    expect(vulns[0].severity).toBe('Unknown');
  });

  it('generates sonatype reference URL for sonatype issue IDs in deep mode', () => {
    const result = {
      component: { componentIdentifier: { coordinates: { packageId: 'lodash', version: '4.17.20' } } },
      securityData: { securityIssues: [{ reference: 'sonatype-2021-0001', severity: 5.0 }] }
    };
    const vulns = extractVulnerabilities({ results: [result] }, directNames, devNames, true);
    expect(vulns[0].referenceUrl).toContain('ossindex.sonatype.org');
  });

  it('skips component when policyData.policyViolations is null (treated as empty)', () => {
    const result = {
      component: { componentIdentifier: { coordinates: { packageId: 'lodash', version: '4.17.20' } } },
      policyData: { policyViolations: null },
      securityData: { securityIssues: [{ reference: 'CVE-2021-1', severity: 5.0 }] }
    };
    // null policyViolations treated same as empty → skip
    const vulns = extractVulnerabilities({ results: [result] }, directNames, devNames, false);
    expect(vulns).toHaveLength(0);
  });

  it('maps severity "moderate" threatCategory to Medium', () => {
    const result = {
      component: { componentIdentifier: { coordinates: { packageId: 'lodash', version: '4.17.20' } } },
      policyData: { policyViolations: [{ policyName: 'Security' }] },
      securityData: { securityIssues: [{ reference: 'CVE-2021-1', severity: 5.0, threatCategory: 'moderate' }] }
    };
    const vulns = extractVulnerabilities({ results: [result] }, directNames, devNames, false);
    expect(vulns[0].severity).toBe('Medium');
  });

  it('sets severity based on CVSS score when no threatCategory (cvss 4-7 → Medium)', () => {
    const result = {
      component: { componentIdentifier: { coordinates: { packageId: 'lodash', version: '4.17.20' } } },
      policyData: { policyViolations: [{ policyName: 'Security' }] },
      securityData: { securityIssues: [{ reference: 'CVE-2021-1', severity: 5.5 }] } // no threatCategory
    };
    const vulns = extractVulnerabilities({ results: [result] }, directNames, devNames, false);
    expect(vulns[0].severity).toBe('Medium');
  });
});

// ── Additional configureScanTools branch coverage ─────────────────────────────

describe('configureScanTools — additional branch coverage', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = createMockServer();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('uses process.cwd() when projectPath is not provided (and no package.json there → isError)', async () => {
    // Spy on process.cwd() to return a path with no package.json
    const cwdSpy = vi.spyOn(process, 'cwd').mockReturnValue('/nonexistent/cwd-no-pkg');

    configureScanTools(mockServer, makeMockConnection());
    const response = await mockServer.invokeTool('nexus_scan_vulnerabilities', {
      applicationId: 'TEST__PROD__app'
      // no projectPath — falls back to process.cwd()
    });

    expect(response.isError).toBe(true);
    expect(response.content[0].text).toMatch(/No package\.json or pom\.xml found in/i);

    cwdSpy.mockRestore();
  });

  it('uses npm ci install when package-lock.json exists (hasPkgLock=true)', async () => {
    const https = await import('https');
    const { execSync } = await import('child_process');
    const fs = await import('fs');
    const os = await import('os');
    const p = await import('path');

    const calledCommands = [];
    execSync.mockImplementation((cmd) => { calledCommands.push(cmd); return ''; });

    let callCount = 0;
    https.request.mockImplementation((_opts, callback) => {
      callCount += 1;
      const res = new EventEmitter();
      res.statusCode = 200;
      res.headers = {};
      const req = new EventEmitter();
      req.write = vi.fn();
      req.end = () => {
        callback(res);
        if (callCount === 1) {
          res.emit('data', JSON.stringify({ applications: [{ id: 'internal-123' }] }));
        } else {
          res.emit('data', JSON.stringify({ components: [] }));
        }
        res.emit('end');
      };
      return req;
    });

    const tmpDir = fs.mkdtempSync(p.join(os.tmpdir(), 'nexus-pkglock-'));
    fs.writeFileSync(p.join(tmpDir, 'package.json'), JSON.stringify({ dependencies: { lodash: '^4.17.21' } }));
    // Add package-lock.json but NOT yarn.lock → hasPkgLock=true, hasYarnLock=false → npm ci
    fs.writeFileSync(p.join(tmpDir, 'package-lock.json'), JSON.stringify({ lockfileVersion: 1, dependencies: {} }));

    configureScanTools(mockServer, makeMockConnection());
    await mockServer.invokeTool('nexus_scan_vulnerabilities', {
      applicationId: 'TEST__PROD__app',
      projectPath: tmpDir
    });

    expect(calledCommands[0]).toBe('npm ci');

    fs.rmSync(tmpDir, { recursive: true });
  });

  it('proceeds non-fatally when execSync install step throws (install error logged)', async () => {
    const https = await import('https');
    const { execSync } = await import('child_process');
    const fs = await import('fs');
    const os = await import('os');
    const p = await import('path');

    // execSync throws on the first call (install step)
    execSync.mockImplementationOnce(() => { throw new Error('install failed'); });
    execSync.mockImplementation(() => '');

    let callCount = 0;
    https.request.mockImplementation((_opts, callback) => {
      callCount += 1;
      const res = new EventEmitter();
      res.statusCode = 200;
      res.headers = {};
      const req = new EventEmitter();
      req.write = vi.fn();
      req.end = () => {
        callback(res);
        if (callCount === 1) {
          res.emit('data', JSON.stringify({ applications: [{ id: 'internal-xyz' }] }));
        } else {
          res.emit('data', JSON.stringify({ components: [] }));
        }
        res.emit('end');
      };
      return req;
    });

    const tmpDir = fs.mkdtempSync(p.join(os.tmpdir(), 'nexus-installerr-'));
    fs.writeFileSync(p.join(tmpDir, 'package.json'), JSON.stringify({ dependencies: {} }));

    configureScanTools(mockServer, makeMockConnection());
    const response = await mockServer.invokeTool('nexus_scan_vulnerabilities', {
      applicationId: 'TEST__PROD__app',
      projectPath: tmpDir
    });

    // Should NOT be an error — install failure is non-fatal
    expect(response.isError).toBeUndefined();

    fs.rmSync(tmpDir, { recursive: true });
  });

  it('uses deep scan mode when deepMode=true is provided', async () => {
    const https = await import('https');
    const { execSync } = await import('child_process');
    const fs = await import('fs');
    const os = await import('os');
    const p = await import('path');

    execSync.mockImplementation(() => '');

    let callCount = 0;
    https.request.mockImplementation((_opts, callback) => {
      callCount += 1;
      const res = new EventEmitter();
      res.statusCode = 200;
      res.headers = {};
      const req = new EventEmitter();
      req.write = vi.fn();
      req.end = () => {
        callback(res);
        if (callCount === 1) {
          res.emit('data', JSON.stringify({ applications: [{ id: 'internal-deep' }] }));
        } else {
          res.emit('data', JSON.stringify({ components: [] }));
        }
        res.emit('end');
      };
      return req;
    });

    const tmpDir = fs.mkdtempSync(p.join(os.tmpdir(), 'nexus-deep-'));
    fs.writeFileSync(p.join(tmpDir, 'package.json'), JSON.stringify({ dependencies: { lodash: '^4.17.21' } }));

    configureScanTools(mockServer, makeMockConnection());
    const response = await mockServer.invokeTool('nexus_scan_vulnerabilities', {
      applicationId: 'TEST__PROD__app',
      projectPath: tmpDir,
      deepMode: true
    });

    expect(response.isError).toBeUndefined();
    expect(response.content).toBeDefined();
    // deep mode summary should mention Deep
    expect(response.content[0].text).toMatch(/deep/i);

    fs.rmSync(tmpDir, { recursive: true });
  });
});

// ── parseMavenDependencies ────────────────────────────────────────────────────

describe('parseMavenDependencies', () => {
  afterEach(() => { vi.restoreAllMocks(); });

  it('parses direct and transitive compile-scope Maven deps from dep-tree output', async () => {
    const { execSync } = await import('child_process');
    const fs = await import('fs');
    const os = await import('os');
    const p  = await import('path');

    const treeContent = [
      '[INFO] com.example:my-service:jar:1.0.0:',
      '[INFO] +- org.apache.commons:commons-lang3:jar:3.12.0:compile',
      '[INFO] +- com.google.guava:guava:jar:31.0.0:compile',
      '[INFO] |  \\- com.google.errorprone:error_prone_annotations:jar:2.18.0:compile',
      '[INFO] \\- junit:junit:jar:4.13.2:test',
      ''
    ].join('\n');

    execSync.mockImplementation((cmd) => {
      if (cmd.includes('dependency:resolve')) return '';
      if (cmd.includes('dependency:tree')) return '';
    });

    const tmpDir = fs.mkdtempSync(p.join(os.tmpdir(), 'nexus-maven-'));
    const scanDir = p.join(tmpDir, 'nexus-report', '.nexus-scan');
    fs.mkdirSync(scanDir, { recursive: true });
    fs.writeFileSync(p.join(scanDir, 'dep-tree.txt'), treeContent);

    const result = parseMavenDependencies(tmpDir, false);

    // Pipeline mode: compile scope included, test excluded
    const names = result.components.map(c => c.componentIdentifier.coordinates.artifactId);
    expect(names).toContain('commons-lang3');
    expect(names).toContain('guava');
    expect(names).toContain('error_prone_annotations');
    expect(names).not.toContain('junit');

    // Direct deps at depth 1
    expect(result.directDepNames.has('org.apache.commons:commons-lang3')).toBe(true);
    expect(result.directDepNames.has('com.google.guava:guava')).toBe(true);

    // No devDependencies in Maven
    expect(result.devDepNames.size).toBe(0);
    expect(result.totalInstalled).toBe(result.components.length);

    // Components use componentIdentifier (no packageUrl)
    for (const c of result.components) {
      expect(c).toHaveProperty('componentIdentifier');
      expect(c.componentIdentifier.format).toBe('maven');
      expect(c).not.toHaveProperty('packageUrl');
    }

    fs.rmSync(tmpDir, { recursive: true });
  });

  it('deep mode includes all scopes including test scope', async () => {
    const { execSync } = await import('child_process');
    const fs = await import('fs');
    const os = await import('os');
    const p  = await import('path');

    const treeContent = [
      '[INFO] com.example:my-service:jar:1.0.0:',
      '[INFO] +- org.springframework:spring-core:jar:5.3.0:compile',
      '[INFO] \\- junit:junit:jar:4.13.2:test',
      ''
    ].join('\n');

    execSync.mockImplementation(() => '');

    const tmpDir = fs.mkdtempSync(p.join(os.tmpdir(), 'nexus-maven-deep-'));
    const scanDir = p.join(tmpDir, 'nexus-report', '.nexus-scan');
    fs.mkdirSync(scanDir, { recursive: true });
    fs.writeFileSync(p.join(scanDir, 'dep-tree.txt'), treeContent);

    const result = parseMavenDependencies(tmpDir, true); // deepMode=true

    const names = result.components.map(c => c.componentIdentifier.coordinates.artifactId);
    expect(names).toContain('spring-core');
    expect(names).toContain('junit'); // included in deep mode

    fs.rmSync(tmpDir, { recursive: true });
  });

  it('throws when mvn dependency:tree fails', async () => {
    const { execSync } = await import('child_process');
    const fs = await import('fs');
    const os = await import('os');
    const p  = await import('path');

    execSync.mockImplementation((cmd) => {
      if (cmd.includes('dependency:resolve')) return '';
      if (cmd.includes('dependency:tree')) throw new Error('BUILD FAILURE');
    });

    const tmpDir = fs.mkdtempSync(p.join(os.tmpdir(), 'nexus-maven-fail-'));
    fs.mkdirSync(p.join(tmpDir, 'nexus-report', '.nexus-scan'), { recursive: true });

    expect(() => parseMavenDependencies(tmpDir, false)).toThrow('mvn dependency:tree failed');

    fs.rmSync(tmpDir, { recursive: true });
  });

  it('throws when tree output has no valid dependency lines (no components)', async () => {
    const { execSync } = await import('child_process');
    const fs = await import('fs');
    const os = await import('os');
    const p  = await import('path');

    execSync.mockImplementation(() => '');

    const tmpDir = fs.mkdtempSync(p.join(os.tmpdir(), 'nexus-maven-empty-'));
    const scanDir = p.join(tmpDir, 'nexus-report', '.nexus-scan');
    fs.mkdirSync(scanDir, { recursive: true });
    // Write a tree file with only the root artifact (no dependencies)
    fs.writeFileSync(p.join(scanDir, 'dep-tree.txt'), '[INFO] com.example:my-service:jar:1.0.0:\n');

    expect(() => parseMavenDependencies(tmpDir, false)).toThrow('No Maven dependencies found');

    fs.rmSync(tmpDir, { recursive: true });
  });

  it('continues non-fatally when mvn dependency:resolve fails', async () => {
    const { execSync } = await import('child_process');
    const fs = await import('fs');
    const os = await import('os');
    const p  = await import('path');

    execSync.mockImplementation((cmd) => {
      if (cmd.includes('dependency:resolve')) throw new Error('Network timeout');
      return ''; // dependency:tree succeeds
    });

    const treeContent = '[INFO] +- org.apache.commons:commons-lang3:jar:3.12.0:compile\n';
    const tmpDir = fs.mkdtempSync(p.join(os.tmpdir(), 'nexus-maven-resolve-'));
    const scanDir = p.join(tmpDir, 'nexus-report', '.nexus-scan');
    fs.mkdirSync(scanDir, { recursive: true });
    fs.writeFileSync(p.join(scanDir, 'dep-tree.txt'), treeContent);

    // Should NOT throw even though resolve failed
    const result = parseMavenDependencies(tmpDir, false);
    expect(result.components.length).toBeGreaterThan(0);

    fs.rmSync(tmpDir, { recursive: true });
  });

  it('throws when dep-tree.txt file is not produced by mvn dependency:tree', async () => {
    const { execSync } = await import('child_process');
    const fs = await import('fs');
    const os = await import('os');
    const p  = await import('path');

    execSync.mockImplementation(() => ''); // both mvn commands succeed but no file written

    const tmpDir = fs.mkdtempSync(p.join(os.tmpdir(), 'nexus-maven-nofile-'));
    // Do NOT create the scan dir or tree file

    expect(() => parseMavenDependencies(tmpDir, false)).toThrow('mvn dependency:tree produced no output file');

    fs.rmSync(tmpDir, { recursive: true });
  });

  it('deduplicates identical groupId:artifactId:version entries', async () => {
    const { execSync } = await import('child_process');
    const fs = await import('fs');
    const os = await import('os');
    const p  = await import('path');

    // Same artifact appears twice (e.g. from different paths in tree)
    const treeContent = [
      '[INFO] +- org.apache.commons:commons-lang3:jar:3.12.0:compile',
      '[INFO] +- org.apache.commons:commons-lang3:jar:3.12.0:compile',
      ''
    ].join('\n');

    execSync.mockImplementation(() => '');

    const tmpDir = fs.mkdtempSync(p.join(os.tmpdir(), 'nexus-maven-dedup-'));
    const scanDir = p.join(tmpDir, 'nexus-report', '.nexus-scan');
    fs.mkdirSync(scanDir, { recursive: true });
    fs.writeFileSync(p.join(scanDir, 'dep-tree.txt'), treeContent);

    const result = parseMavenDependencies(tmpDir, false);
    expect(result.components).toHaveLength(1); // deduped

    fs.rmSync(tmpDir, { recursive: true });
  });
});

// ── Maven project type detection in configureScanTools ───────────────────────

describe('configureScanTools — Maven project type', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = createMockServer();
  });

  afterEach(() => { vi.restoreAllMocks(); });

  it('returns error when both package.json and pom.xml exist and projectType not specified', async () => {
    const fs = await import('fs');
    const os = await import('os');
    const p  = await import('path');

    const tmpDir = fs.mkdtempSync(p.join(os.tmpdir(), 'nexus-both-'));
    fs.writeFileSync(p.join(tmpDir, 'package.json'), JSON.stringify({ dependencies: {} }));
    fs.writeFileSync(p.join(tmpDir, 'pom.xml'), '<project></project>');

    configureScanTools(mockServer, makeMockConnection());
    const response = await mockServer.invokeTool('nexus_scan_vulnerabilities', {
      applicationId: 'TEST__PROD__app',
      projectPath: tmpDir
    });

    expect(response.isError).toBeUndefined();
    expect(response.content[0].text).toMatch(/Both package\.json and pom\.xml found/i);
    expect(response.content[0].text).toMatch(/projectType/i);

    fs.rmSync(tmpDir, { recursive: true });
  });

  it('returns isError when projectType=maven but pom.xml is missing', async () => {
    const fs = await import('fs');
    const os = await import('os');
    const p  = await import('path');

    const tmpDir = fs.mkdtempSync(p.join(os.tmpdir(), 'nexus-nomvn-'));
    fs.writeFileSync(p.join(tmpDir, 'package.json'), JSON.stringify({ dependencies: {} }));
    // No pom.xml

    configureScanTools(mockServer, makeMockConnection());
    const response = await mockServer.invokeTool('nexus_scan_vulnerabilities', {
      applicationId: 'TEST__PROD__app',
      projectPath: tmpDir,
      projectType: 'maven'
    });

    expect(response.isError).toBe(true);
    expect(response.content[0].text).toMatch(/pom\.xml not found/i);

    fs.rmSync(tmpDir, { recursive: true });
  });

  it('returns isError when projectType=npm but package.json is missing', async () => {
    const fs = await import('fs');
    const os = await import('os');
    const p  = await import('path');

    const tmpDir = fs.mkdtempSync(p.join(os.tmpdir(), 'nexus-nonpm-'));
    fs.writeFileSync(p.join(tmpDir, 'pom.xml'), '<project></project>');
    // No package.json

    configureScanTools(mockServer, makeMockConnection());
    const response = await mockServer.invokeTool('nexus_scan_vulnerabilities', {
      applicationId: 'TEST__PROD__app',
      projectPath: tmpDir,
      projectType: 'npm'
    });

    expect(response.isError).toBe(true);
    expect(response.content[0].text).toMatch(/package\.json not found/i);

    fs.rmSync(tmpDir, { recursive: true });
  });

  it('auto-detects Maven when only pom.xml is present', async () => {
    const https = await import('https');
    const { execSync } = await import('child_process');
    const fs = await import('fs');
    const os = await import('os');
    const p  = await import('path');
    const { EventEmitter: EE } = await import('events');

    execSync.mockImplementation(() => '');

    let callCount = 0;
    https.request.mockImplementation((_opts, callback) => {
      callCount++;
      const res = new EE();
      res.statusCode = 200;
      res.headers = {};
      const req = new EE();
      req.write = vi.fn();
      req.end = () => {
        callback(res);
        if (callCount === 1) {
          res.emit('data', JSON.stringify({ applications: [{ id: 'internal-mvn' }] }));
        } else {
          res.emit('data', JSON.stringify({ components: [] }));
        }
        res.emit('end');
      };
      return req;
    });

    const treeContent = '[INFO] +- org.apache.commons:commons-lang3:jar:3.12.0:compile\n';
    const tmpDir = fs.mkdtempSync(p.join(os.tmpdir(), 'nexus-mvn-auto-'));
    const scanDir = p.join(tmpDir, 'nexus-report', '.nexus-scan');
    fs.mkdirSync(scanDir, { recursive: true });
    fs.writeFileSync(p.join(tmpDir, 'pom.xml'), '<project></project>');
    fs.writeFileSync(p.join(scanDir, 'dep-tree.txt'), treeContent);

    configureScanTools(mockServer, makeMockConnection());
    const response = await mockServer.invokeTool('nexus_scan_vulnerabilities', {
      applicationId: 'TEST__PROD__app',
      projectPath: tmpDir
    });

    // Should succeed (not return isError for missing package.json)
    expect(response.isError).toBeUndefined();
    expect(response.content).toBeDefined();

    fs.rmSync(tmpDir, { recursive: true });
  });
});
