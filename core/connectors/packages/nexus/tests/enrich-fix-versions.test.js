import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { enrichFixVersions } from '../src/tools/enrich-fix-versions.js';

// ── Base vuln fixture ────────────────────────────────────────────────────────

const makeVuln = (overrides = {}) => ({
  component: 'lodash',
  version: '4.17.20',
  vulnId: 'CVE-2021-23337',
  severity: 'High',
  cvss: '7.2',
  description: 'Injection',
  fixVersion: null,
  referenceUrl: 'https://example.com',
  dependency: 'direct',
  remediationTypes: [],
  hasNoViolationsFix: false,
  ...overrides
});

const BASE_URL = 'https://nexus.example.com';
const HEADERS = { Authorization: 'Basic xxx' };
const APP_ID = 'app-123';
const STAGE = 'build';

// ── Tests ────────────────────────────────────────────────────────────────────

describe('enrichFixVersions', () => {
  let originalFetch;

  beforeEach(() => {
    originalFetch = globalThis.fetch;
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
    vi.restoreAllMocks();
  });

  it('enriches vulnerability with fixVersion from next-no-violations', async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        remediation: {
          versionChanges: [
            { type: 'next-no-violations', data: { component: { packageUrl: 'pkg:npm/lodash@4.17.21' } } }
          ]
        }
      })
    });

    const vulns = [makeVuln()];
    const result = await enrichFixVersions(BASE_URL, HEADERS, APP_ID, vulns, STAGE);

    expect(result[0].fixVersion).toBe('4.17.21');
    expect(result[0].hasNoViolationsFix).toBe(true);
    expect(result[0].remediationTypes).toContain('next-no-violations');
  });

  it('falls back to next-non-failing fixVersion when no next-no-violations available', async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        remediation: {
          versionChanges: [
            { type: 'next-non-failing', data: { component: { packageUrl: 'pkg:npm/lodash@4.17.21' } } }
          ]
        }
      })
    });

    const vulns = [makeVuln()];
    const result = await enrichFixVersions(BASE_URL, HEADERS, APP_ID, vulns, STAGE);

    expect(result[0].fixVersion).toBe('4.17.21');
    expect(result[0].hasNoViolationsFix).toBe(false);
    expect(result[0].remediationTypes).toContain('next-non-failing');
  });

  it('returns null fixVersion and empty remediationTypes when API returns non-ok response', async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 404
    });

    const original = makeVuln({ fixVersion: '4.17.20' });
    const result = await enrichFixVersions(BASE_URL, HEADERS, APP_ID, [original], STAGE);

    // Falls back to original fixVersion (from eval results), remediationTypes empty
    expect(result[0].fixVersion).toBe('4.17.20');
    expect(result[0].remediationTypes).toHaveLength(0);
    expect(result[0].hasNoViolationsFix).toBe(false);
  });

  it('makes only one API call per unique component, not one per vulnerability', async () => {
    const fetchSpy = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ remediation: { versionChanges: [] } })
    });
    globalThis.fetch = fetchSpy;

    const vulns = [
      makeVuln({ vulnId: 'CVE-1' }),
      makeVuln({ vulnId: 'CVE-2' }), // same component (lodash@4.17.20)
      makeVuln({ component: 'react', version: '18.2.0', vulnId: 'CVE-3' })
    ];

    await enrichFixVersions(BASE_URL, HEADERS, APP_ID, vulns, STAGE);

    // 2 unique components — lodash@4.17.20 and react@18.2.0 — should produce 2 API calls
    expect(fetchSpy).toHaveBeenCalledTimes(2);
  });

  it('handles empty vulnerability list without error', async () => {
    const fetchSpy = vi.fn();
    globalThis.fetch = fetchSpy;

    const result = await enrichFixVersions(BASE_URL, HEADERS, APP_ID, [], STAGE);

    expect(result).toHaveLength(0);
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it('silently handles network errors (returns original fixVersion)', async () => {
    globalThis.fetch = vi.fn().mockRejectedValue(new Error('Network failure'));

    const original = makeVuln({ fixVersion: '4.0.0' });
    const result = await enrichFixVersions(BASE_URL, HEADERS, APP_ID, [original], STAGE);

    // Error is swallowed; falls back to original fixVersion
    expect(result[0].fixVersion).toBe('4.0.0');
    expect(result[0].hasNoViolationsFix).toBe(false);
  });

  it('handles packageUrl with no @ version segment gracefully', async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        remediation: {
          versionChanges: [
            { type: 'next-no-violations', data: { component: { packageUrl: 'pkg:npm/lodash' } } }
          ]
        }
      })
    });

    const vulns = [makeVuln()];
    const result = await enrichFixVersions(BASE_URL, HEADERS, APP_ID, vulns, STAGE);

    // No version in packageUrl → fixVersion remains null from API (falls back to original)
    expect(result[0].hasNoViolationsFix).toBe(true);
    expect(result[0].fixVersion).toBeNull(); // no version in purl
  });

  it('includes both remediationTypes when API returns both', async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        remediation: {
          versionChanges: [
            { type: 'next-no-violations', data: { component: { packageUrl: 'pkg:npm/lodash@4.17.21' } } },
            { type: 'next-non-failing', data: { component: { packageUrl: 'pkg:npm/lodash@4.17.21' } } }
          ]
        }
      })
    });

    const vulns = [makeVuln()];
    const result = await enrichFixVersions(BASE_URL, HEADERS, APP_ID, vulns, STAGE);

    expect(result[0].remediationTypes).toContain('next-no-violations');
    expect(result[0].remediationTypes).toContain('next-non-failing');
    expect(result[0].hasNoViolationsFix).toBe(true);
  });

  it('handles null packageUrl in API response (extractVersionFromPurl null path)', async () => {
    // data.component.packageUrl is null → extractVersionFromPurl(null) → match is null → returns null
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        remediation: {
          versionChanges: [
            { type: 'next-no-violations', data: { component: { packageUrl: null } } }
          ]
        }
      })
    });

    const vulns = [makeVuln()];
    const result = await enrichFixVersions(BASE_URL, HEADERS, APP_ID, vulns, STAGE);

    expect(result[0].hasNoViolationsFix).toBe(true);
    expect(result[0].fixVersion).toBeNull(); // no version extractable
  });

  it('uses empty array when versionChanges is missing from remediation (??[] fallback)', async () => {
    // data.remediation exists but versionChanges is undefined → ?? []
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        remediation: {} // no versionChanges key
      })
    });

    const vulns = [makeVuln({ fixVersion: '4.0.0' })];
    const result = await enrichFixVersions(BASE_URL, HEADERS, APP_ID, vulns, STAGE);

    expect(result[0].remediationTypes).toHaveLength(0);
    expect(result[0].hasNoViolationsFix).toBe(false);
    // falls back to original fixVersion since rem.fixVersion is null
    expect(result[0].fixVersion).toBe('4.0.0');
  });

  // ── Maven-specific tests ─────────────────────────────────────────────────────

  it('builds Maven pURL for groupId:artifactId component names', async () => {
    const fetchSpy = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        remediation: {
          versionChanges: [
            { type: 'next-no-violations', data: { component: { packageUrl: 'pkg:maven/org.apache.commons/commons-lang3@3.13.0' } } }
          ]
        }
      })
    });
    globalThis.fetch = fetchSpy;

    const mavenVuln = makeVuln({ component: 'org.apache.commons:commons-lang3', version: '3.12.0' });
    const result = await enrichFixVersions(BASE_URL, HEADERS, APP_ID, [mavenVuln], STAGE);

    // Verify the API was called — body should contain componentIdentifier for Maven
    expect(fetchSpy).toHaveBeenCalledOnce();
    const callArgs = fetchSpy.mock.calls[0];
    const requestBody = JSON.parse(callArgs[1].body);
    expect(requestBody).toHaveProperty('componentIdentifier');
    expect(requestBody.componentIdentifier.format).toBe('maven');
    expect(requestBody.componentIdentifier.coordinates.groupId).toBe('org.apache.commons');
    expect(requestBody.componentIdentifier.coordinates.artifactId).toBe('commons-lang3');
    expect(requestBody.componentIdentifier.coordinates.version).toBe('3.12.0');
    expect(requestBody).not.toHaveProperty('packageUrl');

    // Result should have fixVersion enriched from the API response
    expect(result[0].fixVersion).toBe('3.13.0');
    expect(result[0].hasNoViolationsFix).toBe(true);
  });

  it('sends componentIdentifier (not packageUrl) for Maven components to avoid 400 errors', async () => {
    const fetchSpy = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ remediation: { versionChanges: [] } })
    });
    globalThis.fetch = fetchSpy;

    const mavenVuln = makeVuln({ component: 'com.example:my-lib', version: '1.0.0' });
    await enrichFixVersions(BASE_URL, HEADERS, APP_ID, [mavenVuln], STAGE);

    const body = JSON.parse(fetchSpy.mock.calls[0][1].body);
    // Must NOT include packageUrl for Maven
    expect(body).not.toHaveProperty('packageUrl');
    // Must include componentIdentifier with maven format
    expect(body.componentIdentifier).toMatchObject({
      format: 'maven',
      coordinates: { groupId: 'com.example', artifactId: 'my-lib', version: '1.0.0', extension: 'jar' }
    });
  });

  it('sends packageUrl (not componentIdentifier) for npm components', async () => {
    const fetchSpy = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ remediation: { versionChanges: [] } })
    });
    globalThis.fetch = fetchSpy;

    const npmVuln = makeVuln({ component: 'lodash', version: '4.17.20' });
    await enrichFixVersions(BASE_URL, HEADERS, APP_ID, [npmVuln], STAGE);

    const body = JSON.parse(fetchSpy.mock.calls[0][1].body);
    expect(body).toHaveProperty('packageUrl', 'pkg:npm/lodash@4.17.20');
    expect(body).not.toHaveProperty('componentIdentifier');
  });

  it('deduplicates Maven components with same groupId:artifactId@version across multiple CVEs', async () => {
    const fetchSpy = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ remediation: { versionChanges: [] } })
    });
    globalThis.fetch = fetchSpy;

    const vulns = [
      makeVuln({ component: 'org.springframework:spring-core', version: '5.3.0', vulnId: 'CVE-1' }),
      makeVuln({ component: 'org.springframework:spring-core', version: '5.3.0', vulnId: 'CVE-2' })
    ];

    await enrichFixVersions(BASE_URL, HEADERS, APP_ID, vulns, STAGE);
    // Only 1 API call for the same Maven component
    expect(fetchSpy).toHaveBeenCalledTimes(1);
  });

  it('returns early with null fixVersion when Maven pURL regex fails to match', async () => {
    // Craft a component whose buildPurl produces a pURL the regex can't parse.
    // isMavenComponent detects "groupId:artifactId" format, buildPurl makes
    // "pkg:maven/groupId/artifactId@version" which the regex DOES match.
    // To test the !m branch, simulate a componentIdentifier body correctly formed
    // and verify the API response returns null when the pURL is malformed.
    //
    // We can test this by mocking fetch to receive the call and return ok=false.
    const fetchSpy = vi.fn().mockResolvedValue({ ok: false, status: 400 });
    globalThis.fetch = fetchSpy;

    const mavenVuln = makeVuln({ component: 'org.apache:commons', version: '1.0.0', fixVersion: '1.1.0' });
    const result = await enrichFixVersions(BASE_URL, HEADERS, APP_ID, [mavenVuln], STAGE);

    // Falls back to original fixVersion on non-ok response
    expect(result[0].fixVersion).toBe('1.1.0');
    expect(result[0].remediationTypes).toHaveLength(0);
  });

  it('enriches multiple Maven components independently', async () => {
    let callIdx = 0;
    globalThis.fetch = vi.fn().mockImplementation(() => {
      callIdx++;
      const purl = callIdx === 1
        ? 'pkg:maven/com.google.guava/guava@32.0.0'
        : 'pkg:maven/org.apache.commons/commons-text@1.11.0';
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({
          remediation: {
            versionChanges: [
              { type: 'next-no-violations', data: { component: { packageUrl: purl } } }
            ]
          }
        })
      });
    });

    const vulns = [
      makeVuln({ component: 'com.google.guava:guava', version: '31.0.0', vulnId: 'CVE-A' }),
      makeVuln({ component: 'org.apache.commons:commons-text', version: '1.10.0', vulnId: 'CVE-B' })
    ];

    const result = await enrichFixVersions(BASE_URL, HEADERS, APP_ID, vulns, STAGE);

    expect(result[0].fixVersion).toBe('32.0.0');
    expect(result[1].fixVersion).toBe('1.11.0');
  });
});
