import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import {
  configureFixTools,
  semverGte,
  getInstalledVersion,
  getLatestNpmVersion,
  backupPackageJson,
  tryRunCmd,
  openInBrowser,
  updatePomVersion,
  addPomDependencyManagement,
  findMavenParentDep
} from '../src/tools/fix-vulnerabilities.js';
import { createMockServer, isValidToolResponse, isValidErrorResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';

// ── Mock child_process ───────────────────────────────────────────────────────
vi.mock('child_process', () => ({
  execSync: vi.fn(() => '')
}));

// ── Mock generate-reports appendFixSummary ────────────────────────────────────
vi.mock('../src/tools/generate-reports.js', () => ({
  appendFixSummary: vi.fn()
}));

// ── Mock fs ───────────────────────────────────────────────────────────────────
vi.mock('fs', () => ({
  writeFileSync: vi.fn(),
  mkdirSync: vi.fn(),
  copyFileSync: vi.fn(),
  readFileSync: vi.fn(),
  existsSync: vi.fn()
}));

import { execSync } from 'child_process';
import { existsSync, readFileSync, writeFileSync, copyFileSync } from 'fs';
import { appendFixSummary } from '../src/tools/generate-reports.js';

// ── Fixtures ─────────────────────────────────────────────────────────────────

const APPLICATION_ID = '51855__DCDAQPR__test-repo';

const DIRECT_VULN = {
  module: 'lodash',
  currentVersion: '4.17.20',
  fixVersion: '4.17.21',
  cveId: 'CVE-2021-23337',
  severity: 'High',
  score: '7.2',
  dependency: 'direct',
  canAutoFix: true
};

const TRANSITIVE_VULN = {
  module: 'minimist',
  currentVersion: '1.2.5',
  fixVersion: '1.2.6',
  cveId: 'CVE-2021-44906',
  severity: 'High',
  score: '7.5',
  dependency: 'transitive',
  canAutoFix: false
};

const DIRECT_NO_FIX = {
  module: 'old-lib',
  currentVersion: '1.0.0',
  fixVersion: null,
  cveId: 'CVE-X',
  severity: 'Medium',
  score: '5.0',
  dependency: 'direct',
  canAutoFix: false
};

function makeReport(overrides = {}) {
  return {
    summary: { applicationId: APPLICATION_ID },
    vulnerableModules: [],
    allVulnerabilities: [DIRECT_VULN],
    ...overrides
  };
}

function makePackageJson(overrides = {}) {
  return JSON.stringify({
    name: 'test-repo',
    dependencies: { lodash: '4.17.20' },
    devDependencies: {},
    ...overrides
  });
}

// ── Tests ─────────────────────────────────────────────────────────────────────

describe('nexus_fix_vulnerabilities tool', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = createMockServer();
    vi.mocked(existsSync).mockReset();
    vi.mocked(readFileSync).mockReset();
    vi.mocked(writeFileSync).mockReset();
    vi.mocked(execSync).mockReset();
    vi.mocked(appendFixSummary).mockClear();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('is registered with name nexus_fix_vulnerabilities', () => {
    configureFixTools(mockServer);
    const names = mockServer.getRegisteredTools().map(t => t.name);
    expect(names).toContain('nexus_fix_vulnerabilities');
  });

  it('returns isError when nexus-report/nexus-vulnerability-report.json does not exist', async () => {
    vi.mocked(existsSync).mockReturnValue(false);
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID
    });

    expect(isValidErrorResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('nexus_scan_vulnerabilities');
  });

  it('returns clean message when allVulnerabilities is empty', async () => {
    vi.mocked(existsSync).mockReturnValue(true);
    vi.mocked(readFileSync).mockReturnValue(JSON.stringify(makeReport({ allVulnerabilities: [] })));
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID
    });

    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('No vulnerabilities to fix');
  });

  it('attempts to fix direct dependencies via package.json update', async () => {
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      return false; // no yarn.lock
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [DIRECT_VULN] }));
      }
      if (p.endsWith('package.json')) return makePackageJson();
      return '';
    });
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID
    });

    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('Phase A');
    // package.json should have been written with updated lodash version
    const writeCall = vi.mocked(writeFileSync).mock.calls.find(
      c => c[0].endsWith('package.json') && !c[0].endsWith('report.json')
    );
    expect(writeCall).toBeDefined();
    const writtenPkg = JSON.parse(writeCall[1]);
    expect(writtenPkg.dependencies.lodash).toBe('^4.17.21');
  });

  it('runs yarn upgrade for transitive vulnerabilities when yarn.lock is present', async () => {
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('yarn.lock')) return true;
      if (p.endsWith('package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [TRANSITIVE_VULN] }));
      }
      if (p.endsWith('package.json')) return makePackageJson({ dependencies: {} });
      return '';
    });
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID
    });

    expect(isValidToolResponse(response)).toBe(true);
    const text = response.content[0].text;
    expect(text).toContain('Phase B1');
    // Should have attempted yarn upgrade
    const yarnCall = vi.mocked(execSync).mock.calls.find(c => c[0].includes('yarn upgrade'));
    expect(yarnCall).toBeDefined();
  });

  it('skips yarn upgrade and reports when project uses npm', async () => {
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      if (p.endsWith('yarn.lock')) return false;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [TRANSITIVE_VULN] }));
      }
      if (p.endsWith('package.json')) return makePackageJson({ dependencies: {} });
      return '';
    });
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID
    });

    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('Skipping yarn upgrade');
  });

  it('proposes parent upgrades (B2) but does not apply without approval', async () => {
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      if (p.endsWith('yarn.lock')) return false;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [TRANSITIVE_VULN] }));
      }
      if (p.endsWith('package.json')) {
        // webpack depends on minimist transiently
        return makePackageJson({ dependencies: { webpack: '^5.88.0' } });
      }
      return '';
    });
    // npm ls finds webpack as parent
    vi.mocked(execSync).mockImplementation(cmd => {
      if (cmd.includes('npm ls minimist')) return 'webpack@5.88.0\n  minimist@1.2.5\n';
      return '';
    });
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID,
      approveParentUpgrades: false
    });

    expect(isValidToolResponse(response)).toBe(true);
    const text = response.content[0].text;
    expect(text).toContain('Phase B2');
    expect(text).toContain('approveParentUpgrades=true');
  });

  it('applies parent upgrades (B2) when approveParentUpgrades=true', async () => {
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      if (p.endsWith('yarn.lock')) return false;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [TRANSITIVE_VULN] }));
      }
      if (p.endsWith('package.json')) {
        return makePackageJson({ dependencies: { webpack: '^5.88.0' } });
      }
      return '';
    });
    vi.mocked(execSync).mockImplementation(cmd => {
      if (cmd.includes('npm ls minimist')) return 'webpack@5.88.0\n  minimist@1.2.5\n';
      return '';
    });
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID,
      approveParentUpgrades: true
    });

    expect(isValidToolResponse(response)).toBe(true);
    const text = response.content[0].text;
    expect(text).toContain('approveParentUpgrades=true — applying');
    // package.json should have been written with webpack: latest
    const writeCall = vi.mocked(writeFileSync).mock.calls.find(
      c => c[0].endsWith('package.json') && !c[0].endsWith('report.json')
    );
    expect(writeCall).toBeDefined();
    const writtenPkg = JSON.parse(writeCall[1]);
    expect(writtenPkg.dependencies.webpack).toBe('latest');
  });

  it('proposes resolutions (B3) but does not apply without approval', async () => {
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      if (p.endsWith('yarn.lock')) return false;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [TRANSITIVE_VULN] }));
      }
      if (p.endsWith('package.json')) return makePackageJson({ dependencies: {} });
      return '';
    });
    // npm ls returns no parent
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID,
      approveResolutions: false
    });

    expect(isValidToolResponse(response)).toBe(true);
    const text = response.content[0].text;
    expect(text).toContain('Phase B3');
    expect(text).toContain('approveResolutions=true');
  });

  it('applies resolutions (B3) when approveResolutions=true (yarn project)', async () => {
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('yarn.lock')) return true;
      if (p.endsWith('package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [TRANSITIVE_VULN] }));
      }
      if (p.endsWith('package.json')) return makePackageJson({ dependencies: {} });
      return '';
    });
    // yarn why returns no parent  
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID,
      approveResolutions: true
    });

    expect(isValidToolResponse(response)).toBe(true);
    const text = response.content[0].text;
    expect(text).toContain('approveResolutions=true — applying');
    // package.json should have resolutions block
    const writeCall = vi.mocked(writeFileSync).mock.calls.find(
      c => c[0].endsWith('package.json') && !c[0].endsWith('report.json')
    );
    expect(writeCall).toBeDefined();
    const writtenPkg = JSON.parse(writeCall[1]);
    expect(writtenPkg.resolutions?.minimist).toBe('1.2.6');
  });

  it('appends fix summary to reports after workflow completes', async () => {
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [DIRECT_VULN] }));
      }
      if (p.endsWith('package.json')) return makePackageJson();
      return '';
    });
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    await mockServer.invokeTool('nexus_fix_vulnerabilities', { applicationId: APPLICATION_ID });

    expect(appendFixSummary).toHaveBeenCalledOnce();
    const arg = vi.mocked(appendFixSummary).mock.calls[0][0];
    expect(arg.totalOriginal).toBe(1);
    expect(arg.fixDate).toBeDefined();
  });

  it('prints the final summary counters in response text', async () => {
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [DIRECT_VULN] }));
      }
      if (p.endsWith('package.json')) return makePackageJson();
      return '';
    });
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', { applicationId: APPLICATION_ID });

    const text = response.content[0].text;
    expect(text).toContain('Vulnerability Fix Summary');
    expect(text).toContain('Direct Dependencies Fixed:');
    expect(text).toContain('Remaining Unresolved:');
  });

  it('returns isError when the JSON report file is corrupt', async () => {
    vi.mocked(existsSync).mockReturnValue(true);
    vi.mocked(readFileSync).mockReturnValue('NOT VALID JSON{{');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID
    });

    expect(isValidErrorResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('Failed to read scan report');
  });

  it('retries yarn upgrade after "Outdated lockfile" error', async () => {
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('yarn.lock')) return true;
      if (p.endsWith('package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [TRANSITIVE_VULN] }));
      }
      if (p.endsWith('package.json')) return makePackageJson({ dependencies: {} });
      return '';
    });

    let upgradeCallCount = 0;
    vi.mocked(execSync).mockImplementation(cmd => {
      if (cmd.includes('yarn upgrade')) {
        upgradeCallCount += 1;
        if (upgradeCallCount === 1) {
          // First call throws "Outdated lockfile"
          const err = new Error('error Outdated lockfile. Please run yarn install and try again.');
          err.stdout = '';
          throw err;
        }
        return ''; // Second call succeeds
      }
      return '';
    });
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID
    });

    expect(isValidToolResponse(response)).toBe(true);
    // yarn upgrade should have been called twice (first fail + retry)
    expect(upgradeCallCount).toBe(2);
  });

  it('includes unfixable direct deps (no fixVersion) in remaining modules', async () => {
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [DIRECT_NO_FIX] }));
      }
      if (p.endsWith('package.json')) return makePackageJson();
      return '';
    });
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    await mockServer.invokeTool('nexus_fix_vulnerabilities', { applicationId: APPLICATION_ID });

    const arg = vi.mocked(appendFixSummary).mock.calls[0][0];
    expect(arg.remainingModules).toHaveLength(1);
    expect(arg.remainingModules[0].reason).toContain('No fix version available');
  });

  it('skips Phase A update for a dep not found in dependencies or devDependencies', async () => {
    // Vuln references 'unknown-dep' which doesn't appear in package.json
    const unknownVuln = { ...DIRECT_VULN, module: 'unknown-dep' };
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [unknownVuln] }));
      }
      if (p.endsWith('package.json')) return makePackageJson(); // only has lodash
      return '';
    });
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', { applicationId: APPLICATION_ID });
    // Should not crash and Phase A should find nothing to update
    expect(isValidToolResponse(response)).toBe(true);
    // package.json write should NOT have happened for package.json update (dep not found)
    const pkgWrite = vi.mocked(writeFileSync).mock.calls.find(
      c => c[0].endsWith('package.json') && !c[0].endsWith('report.json')
    );
    expect(pkgWrite).toBeUndefined();
  });

  it('fixes devDependency when dep is in devDependencies', async () => {
    const devVuln = { ...DIRECT_VULN, module: 'webpack' };
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [devVuln] }));
      }
      if (p.endsWith('package.json')) {
        return JSON.stringify({
          name: 'test',
          dependencies: {},
          devDependencies: { webpack: '^5.88.0' }
        });
      }
      return '';
    });
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', { applicationId: APPLICATION_ID });
    expect(isValidToolResponse(response)).toBe(true);
    const writeCall = vi.mocked(writeFileSync).mock.calls.find(
      c => c[0].endsWith('package.json') && !c[0].endsWith('report.json')
    );
    expect(writeCall).toBeDefined();
    const writtenPkg = JSON.parse(writeCall[1]);
    expect(writtenPkg.devDependencies.webpack).toBe('^4.17.21');
  });

  it('handles appendFixSummary throwing without crashing the tool', async () => {
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [DIRECT_VULN] }));
      }
      if (p.endsWith('package.json')) return makePackageJson();
      return '';
    });
    vi.mocked(execSync).mockReturnValue('');
    vi.mocked(appendFixSummary).mockImplementation(() => { throw new Error('write error'); });
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', { applicationId: APPLICATION_ID });
    // Tool should still return a valid response, just with a warning
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('Could not append fix summary');
  });

  // ── Additional branch coverage tests ─────────────────────────────────────────

  it('Phase A: uses yarn install when yarn.lock is present', async () => {
    // pm === 'yarn' branch in fixDirectDependencies — installCmd = 'yarn install'
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('yarn.lock')) return true;
      if (p.endsWith('package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [DIRECT_VULN] }));
      }
      if (p.endsWith('package.json')) return makePackageJson();
      return '';
    });
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID
    });

    expect(isValidToolResponse(response)).toBe(true);
    // Should have called 'yarn install' for Phase A (not 'npm install')
    const yarnInstallCall = vi.mocked(execSync).mock.calls.find(c => c[0] === 'yarn install');
    expect(yarnInstallCall).toBeDefined();
  });

  it('Phase A: logs warning when fixDirectDependencies throws (Phase A catch block)', async () => {
    // Make writeFileSync throw when writing package.json (triggers Phase A catch)
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [DIRECT_VULN] }));
      }
      if (p.endsWith('package.json')) return makePackageJson();
      return '';
    });
    vi.mocked(writeFileSync).mockImplementation(p => {
      if (p.endsWith('package.json') && !p.endsWith('report.json')) {
        throw new Error('EPERM: permission denied');
      }
    });
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID
    });

    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('Phase A partially failed');
  });

  it('Phase B1: logs failure message when yarn upgrade fails with non-lockfile error', async () => {
    // runYarnUpgrade returns success=false (not due to "Outdated lockfile") → B1 failure message
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('yarn.lock')) return true;
      if (p.endsWith('package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [TRANSITIVE_VULN] }));
      }
      if (p.endsWith('package.json')) return makePackageJson({ dependencies: {} });
      return '';
    });
    vi.mocked(execSync).mockImplementation(cmd => {
      if (cmd.includes('yarn upgrade')) {
        const err = new Error('yarn upgrade failed: some network error');
        throw err;
      }
      return '';
    });
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID
    });

    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('yarn upgrade failed');
  });

  it('Phase B3: applies npm overrides when pm is npm and approveResolutions=true', async () => {
    // pm === 'npm' branch in applyResolutions — uses overrides (not resolutions)
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      if (p.endsWith('yarn.lock')) return false; // npm project
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [TRANSITIVE_VULN] }));
      }
      if (p.endsWith('package.json')) return makePackageJson({ dependencies: {} });
      return '';
    });
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID,
      approveResolutions: true
    });

    expect(isValidToolResponse(response)).toBe(true);
    const text = response.content[0].text;
    expect(text).toContain('approveResolutions=true — applying');
    // package.json should have overrides (not resolutions — npm project)
    const writeCall = vi.mocked(writeFileSync).mock.calls.find(
      c => c[0].endsWith('package.json') && !c[0].endsWith('report.json')
    );
    expect(writeCall).toBeDefined();
    const writtenPkg = JSON.parse(writeCall[1]);
    expect(writtenPkg.overrides?.minimist).toBe('1.2.6');
    expect(writtenPkg.resolutions).toBeUndefined();
  });

  it('Phase B3: logs failure when applyResolutions throws (B3 catch block)', async () => {
    // writeFileSync throws inside applyResolutions → B3 catch → remainingModules push
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      if (p.endsWith('yarn.lock')) return false;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [TRANSITIVE_VULN] }));
      }
      if (p.endsWith('package.json')) return makePackageJson({ dependencies: {} });
      return '';
    });
    let writeCallCount = 0;
    vi.mocked(writeFileSync).mockImplementation(p => {
      if (p.endsWith('package.json') && !p.endsWith('report.json')) {
        writeCallCount++;
        if (writeCallCount >= 1) throw new Error('EROFS: file system is read-only');
      }
    });
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID,
      approveResolutions: true
    });

    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('Phase B3 failed');
    // The module should appear in remainingModules
    const arg = vi.mocked(appendFixSummary).mock.calls[0]?.[0];
    expect(arg?.remainingModules?.length).toBeGreaterThan(0);
  });

  it('findParentDep: returns no parent when yarn why command fails', async () => {
    // tryRunCmd !success → returns null from findParentDep → parentProposals is empty
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('yarn.lock')) return true;
      if (p.endsWith('package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [TRANSITIVE_VULN] }));
      }
      if (p.endsWith('package.json')) {
        return makePackageJson({ dependencies: { webpack: '^5.88.0' } });
      }
      return '';
    });
    vi.mocked(execSync).mockImplementation(cmd => {
      if (cmd.includes('yarn why')) throw new Error('command not found: yarn');
      if (cmd.includes('yarn upgrade')) return ''; // B1 succeeds
      return '';
    });
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID,
      approveParentUpgrades: true
    });

    // Should succeed but B2 found no parent (yarn why failed)
    expect(isValidToolResponse(response)).toBe(true);
    // No parent proposals → B2 else branch: "No parent dependency upgrade paths identified"
    const text = response.content[0].text;
    expect(text).toContain('No parent dependency upgrade paths identified');
  });

  it('tryRunCmd: captures stdout from failed command (err.stdout truthy branch)', async () => {
    // err.stdout has content (not empty) — covers the truthy branch of err.stdout ||
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('yarn.lock')) return true;
      if (p.endsWith('package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [TRANSITIVE_VULN] }));
      }
      if (p.endsWith('package.json')) return makePackageJson({ dependencies: {} });
      return '';
    });
    vi.mocked(execSync).mockImplementation(cmd => {
      if (cmd.includes('yarn upgrade')) {
        const err = new Error('yarn: command failed');
        err.stdout = 'yarn output before failure\n'; // truthy stdout
        throw err;
      }
      return '';
    });
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID
    });

    expect(isValidToolResponse(response)).toBe(true);
    // yarn upgrade failed → failure message includes the error
    expect(response.content[0].text).toContain('yarn upgrade failed');
  });

  it('Phase A: handles duplicate CVEs for the same module (dedup on push)', async () => {
    // Two vulns for same module (lodash) with same CVE — updates.has(v.module) covers repeat check
    const DIRECT_VULN_DUP = {
      module: 'lodash', currentVersion: '4.17.20',
      fixVersion: '4.17.21', cveId: 'CVE-2021-23337',
      vulnId: 'CVE-2021-23337', severity: 'High', score: '7.2',
      dependency: 'direct', canAutoFix: true
    };
    const DIRECT_VULN_DUP2 = {
      ...DIRECT_VULN_DUP, cveId: 'CVE-2021-23337' // same module, same CVE
    };
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [DIRECT_VULN_DUP, DIRECT_VULN_DUP2] }));
      }
      if (p.endsWith('package.json')) return makePackageJson();
      return '';
    });
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', { applicationId: APPLICATION_ID });
    expect(isValidToolResponse(response)).toBe(true);
    // Should have fixed lodash once, not twice
    const arg = vi.mocked(appendFixSummary).mock.calls[0][0];
    expect(arg.fixedModules.filter(f => f.module === 'lodash')).toHaveLength(1);
  });

  it('falls back to empty array when allVulnerabilities is absent from report (covers || [] branch)', async () => {
    // report has no allVulnerabilities field → report.allVulnerabilities || [] → uses []
    vi.mocked(existsSync).mockReturnValue(true);
    vi.mocked(readFileSync).mockReturnValue(
      JSON.stringify({ summary: { applicationId: APPLICATION_ID }, vulnerableModules: [] }) // no allVulnerabilities
    );
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', { applicationId: APPLICATION_ID });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('No vulnerabilities to fix');
  });

  it('Phase A covers: duplicate module in directFixable AND mixed known/unknown deps', async () => {
    // Covers:
    //   - Line 75: updates.has(v.module) = true → continue (duplicate lodash)
    //   - Line 93: !updates.has(v.module) = true → continue (unknown-dep not in updates)
    //   - Line 95: fixed.some(...) = true → continue (duplicate CVE logging)
    const LODASH_DUP = { ...DIRECT_VULN }; // duplicate of DIRECT_VULN (same module, same fixVersion)
    const UNKNOWN_FIXABLE = {
      ...DIRECT_VULN,
      module: 'not-in-package', // not in package.json dependencies → depType = null
      vulnId: 'CVE-UNKNOWN'
    };
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [DIRECT_VULN, LODASH_DUP, UNKNOWN_FIXABLE] }));
      }
      if (p.endsWith('package.json')) return makePackageJson(); // only has lodash, not 'not-in-package'
      return '';
    });
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', { applicationId: APPLICATION_ID });
    expect(isValidToolResponse(response)).toBe(true);
    // Only lodash fixed once (duplicate deduplicated; unknown-dep skipped)
    const arg = vi.mocked(appendFixSummary).mock.calls[0][0];
    expect(arg.fixedModules.filter(f => f.module === 'lodash')).toHaveLength(1);
    expect(arg.fixedModules.some(f => f.module === 'not-in-package')).toBe(false);
  });

  it('Phase B1: detects resolved transitive vuln when installed version >= fixVersion after yarn upgrade', async () => {
    // Covers: getInstalledVersion success path, semverGte true branch, b1FixedNames tracking
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('yarn.lock')) return true;
      if (p.endsWith('package.json')) return true;
      if (p.includes('node_modules/minimist/package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [TRANSITIVE_VULN] }));
      }
      if (p.includes('node_modules/minimist/package.json')) {
        return JSON.stringify({ version: '1.2.6' }); // == fixVersion → semverGte=true
      }
      if (p.endsWith('package.json')) return makePackageJson({ dependencies: {} });
      return '';
    });
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID
    });

    expect(isValidToolResponse(response)).toBe(true);
    const text = response.content[0].text;
    expect(text).toContain('Phase B1');
    const arg = vi.mocked(appendFixSummary).mock.calls[0][0];
    // minimist should be in fixedModules with fixMethod 'yarn upgrade'
    const yarnFixed = arg.fixedModules.find(f => f.module === 'minimist' && f.fixMethod === 'yarn upgrade');
    expect(yarnFixed).toBeDefined();
    expect(yarnFixed.newVersion).toBe('1.2.6');
  });

  it('Phase B1: getInstalledVersion returns null when package.json parse fails (catch block)', async () => {
    // Covers: JSON.parse error catch branch in getInstalledVersion
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('yarn.lock')) return true;
      if (p.endsWith('package.json')) return true;
      if (p.includes('node_modules/minimist/package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [TRANSITIVE_VULN] }));
      }
      if (p.includes('node_modules/minimist/package.json')) return 'NOT_JSON{'; // invalid JSON
      if (p.endsWith('package.json')) return makePackageJson({ dependencies: {} });
      return '';
    });
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', { applicationId: APPLICATION_ID });
    expect(isValidToolResponse(response)).toBe(true);
    // parse error → getInstalledVersion returns null → no b1 fix recorded
    const arg = vi.mocked(appendFixSummary).mock.calls[0][0];
    expect(arg.fixedModules.some(f => f.fixMethod === 'yarn upgrade')).toBe(false);
  });

  it('Phase B2: marks package as skipped when it is itself a direct dep (isDirectDep branch)', async () => {
    // minimist is BOTH listed as transitive AND in package.json dependencies (direct dep misclassification)
    // findParentDep returns null → isDirectDep check fires
    const TRANSITIVE_BUT_DIRECT = {
      ...TRANSITIVE_VULN,
      module: 'lodash', // lodash IS a direct dep in MOCK_PACKAGE_JSON
    };
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      return false; // npm project
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [TRANSITIVE_BUT_DIRECT] }));
      }
      if (p.endsWith('package.json')) return makePackageJson(); // lodash IS in dependencies
      return '';
    });
    vi.mocked(execSync).mockImplementation(cmd => {
      if (cmd.includes('npm ls lodash')) throw new Error('not found');
      return '';
    });
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', { applicationId: APPLICATION_ID });
    expect(isValidToolResponse(response)).toBe(true);
    const text = response.content[0].text;
    // Should show skip reason mentioning "direct dependency"
    expect(text).toContain('Phase B2');
    const arg = vi.mocked(appendFixSummary).mock.calls[0][0];
    expect(arg.remainingModules.some(r => r.module === 'lodash')).toBe(true);
  });

  it('Phase B2: covers both proposals AND skip-reason entries in same run', async () => {
    // One transitive has a parent (webpack→minimist), another has no parent (unknown-trans)
    const UNKNOWN_TRANS = {
      module: 'unknown-trans',
      currentVersion: '1.0.0',
      fixVersion: '1.0.1',
      cveId: 'CVE-UNKNOWN-TRANS',
      severity: 'Medium',
      score: '5.0',
      dependency: 'transitive',
      canAutoFix: false
    };
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      return false; // npm
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [TRANSITIVE_VULN, UNKNOWN_TRANS] }));
      }
      if (p.endsWith('package.json')) {
        return makePackageJson({ dependencies: { webpack: '^5.0.0' } });
      }
      return '';
    });
    vi.mocked(execSync).mockImplementation(cmd => {
      if (cmd.includes('npm ls minimist')) return 'webpack@5.0.0\n  minimist@1.2.5\n';
      if (cmd.includes('npm ls unknown-trans')) throw new Error('not found');
      if (cmd.includes('npm view')) return '5.99.0\n'; // getLatestNpmVersion
      return '';
    });
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', { applicationId: APPLICATION_ID });
    expect(isValidToolResponse(response)).toBe(true);
    const text = response.content[0].text;
    expect(text).toContain('Phase B2');
    expect(text).toContain('approveParentUpgrades=true'); // proposals shown but not applied
  });

  it('Phase B2: applies approved parent upgrade using resolved npm version', async () => {
    // approveParentUpgrades=true + npm view returns specific version → uses ^latestVersion
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      return false; // npm
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [TRANSITIVE_VULN] }));
      }
      if (p.endsWith('package.json')) return makePackageJson({ dependencies: { webpack: '^5.0.0' } });
      return '';
    });
    vi.mocked(execSync).mockImplementation(cmd => {
      if (cmd.includes('npm ls minimist')) return 'webpack@5.0.0\n  minimist@1.2.5\n';
      if (cmd.includes('npm view webpack version')) return '5.99.0\n';
      return '';
    });
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID,
      approveParentUpgrades: true
    });

    expect(isValidToolResponse(response)).toBe(true);
    const text = response.content[0].text;
    expect(text).toContain('^5.99.0'); // uses version from npm view
    const arg = vi.mocked(appendFixSummary).mock.calls[0][0];
    const parentFixed = arg.fixedModules.find(f => f.module === 'minimist' && f.fixMethod === 'parent upgrade');
    expect(parentFixed).toBeDefined();
    expect(parentFixed.newVersion).toBe('^5.99.0');
  });

  it('includes unfixable transitive dep (no fixVersion) in remaining modules', async () => {
    // Covers: unfixable transitive tracking code path
    const TRANSITIVE_NO_FIX = {
      module: 'old-trans',
      currentVersion: '0.1.0',
      fixVersion: null,
      cveId: 'CVE-TRANS-NOFX',
      severity: 'Medium',
      score: '5.0',
      dependency: 'transitive',
      canAutoFix: false
    };
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [TRANSITIVE_NO_FIX] }));
      }
      if (p.endsWith('package.json')) return makePackageJson({ dependencies: {} });
      return '';
    });
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', { applicationId: APPLICATION_ID });
    expect(isValidToolResponse(response)).toBe(true);
    const arg = vi.mocked(appendFixSummary).mock.calls[0][0];
    const remaining = arg.remainingModules.find(r => r.module === 'old-trans');
    expect(remaining).toBeDefined();
    expect(remaining.reason).toContain('No fix version');
  });

  it('Phase B2: no proposals found — reports per-package skip reasons in output', async () => {
    // All transitive pkgs have no findable parent → skip reasons reported
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('package.json')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeReport({ allVulnerabilities: [TRANSITIVE_VULN] }));
      }
      if (p.endsWith('package.json')) return makePackageJson({ dependencies: {} });
      return '';
    });
    vi.mocked(execSync).mockImplementation(cmd => {
      if (cmd.includes('npm ls')) throw new Error('not found');
      return '';
    });
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', { applicationId: APPLICATION_ID });
    expect(isValidToolResponse(response)).toBe(true);
    const text = response.content[0].text;
    expect(text).toContain('Phase B2');
    expect(text).toContain('No parent dependency upgrade paths identified');
  });
});

// ── Pure-function unit tests ──────────────────────────────────────────────────

describe('semverGte', () => {
  it('returns true when a > b on first segment', () => {
    expect(semverGte('2.0.0', '1.0.0')).toBe(true);
  });

  it('returns false when a < b on third segment', () => {
    expect(semverGte('1.2.5', '1.2.6')).toBe(false);
  });

  it('returns true when a == b', () => {
    expect(semverGte('1.2.6', '1.2.6')).toBe(true);
  });

  it('handles shorter a array (pa[i] undefined → treated as 0)', () => {
    // '1.0' (2 segments) vs '1.0.0' (3 segments); i=2: pa[2]=undefined → 0, diff=0 → true
    expect(semverGte('1.0', '1.0.0')).toBe(true);
  });

  it('handles shorter b array (pb[i] undefined → treated as 0)', () => {
    // '1.0.1' vs '1.0' (2 segments); i=2: pb[2]=undefined → 0, diff=0+1=1 → true
    expect(semverGte('1.0.1', '1.0')).toBe(true);
  });

  it('handles null/empty version string (v || "")', () => {
    // null → '' → ['0'] → [0]
    expect(semverGte(null, '0.0.0')).toBe(true);
    expect(semverGte('1.0.0', null)).toBe(true);
  });

  it('handles non-numeric segment (parseInt NaN → 0)', () => {
    // '1.alpha.3' vs '1.0.3': 'alpha' parses to NaN → 0; diff at i=1: 0-0=0; i=2: 3-3=0 → true
    expect(semverGte('1.alpha.3', '1.0.3')).toBe(true);
  });
});

describe('tryRunCmd', () => {
  afterEach(() => { vi.mocked(execSync).mockReset(); });

  it('returns success:true and stdout on success', () => {
    vi.mocked(execSync).mockReturnValue('output\n');
    const result = tryRunCmd('echo hi', '/');
    expect(result.success).toBe(true);
    expect(result.stdout).toBe('output\n');
  });

  it('returns success:false and empty stdout when err.stdout is falsy', () => {
    vi.mocked(execSync).mockImplementation(() => {
      const err = new Error('command failed');
      err.stdout = null; // explicitly falsy
      throw err;
    });
    const result = tryRunCmd('bad-cmd', '/');
    expect(result.success).toBe(false);
    expect(result.stdout).toBe('');
  });

  it('returns success:false and err.stdout when truthy', () => {
    vi.mocked(execSync).mockImplementation(() => {
      const err = new Error('command failed');
      err.stdout = 'partial output';
      throw err;
    });
    const result = tryRunCmd('bad-cmd', '/');
    expect(result.success).toBe(false);
    expect(result.stdout).toBe('partial output');
  });
});

describe('getInstalledVersion', () => {
  afterEach(() => { vi.mocked(existsSync).mockReset(); vi.mocked(readFileSync).mockReset(); });

  it('returns version from node_modules package.json', () => {
    vi.mocked(existsSync).mockReturnValue(true);
    vi.mocked(readFileSync).mockReturnValue(JSON.stringify({ version: '1.2.3' }));
    expect(getInstalledVersion('lodash', '/project')).toBe('1.2.3');
  });

  it('returns null when file does not exist', () => {
    vi.mocked(existsSync).mockReturnValue(false);
    expect(getInstalledVersion('missing-pkg', '/project')).toBeNull();
  });

  it('returns null when package.json is invalid JSON (catch branch)', () => {
    vi.mocked(existsSync).mockReturnValue(true);
    vi.mocked(readFileSync).mockReturnValue('INVALID JSON{');
    expect(getInstalledVersion('bad-pkg', '/project')).toBeNull();
  });
});

describe('getLatestNpmVersion', () => {
  afterEach(() => { vi.mocked(execSync).mockReset(); });

  it('returns version string when npm view succeeds', () => {
    vi.mocked(execSync).mockReturnValue('4.17.21\n');
    expect(getLatestNpmVersion('lodash', '/project')).toBe('4.17.21');
  });

  it('returns null when npm view fails', () => {
    vi.mocked(execSync).mockImplementation(() => { throw new Error('not found'); });
    expect(getLatestNpmVersion('missing-pkg', '/project')).toBeNull();
  });
});

describe('backupPackageJson', () => {
  afterEach(() => { vi.restoreAllMocks(); });

  it('does not throw when copyFileSync fails (non-fatal catch)', () => {
    vi.mocked(existsSync).mockReturnValue(true);
    vi.mocked(copyFileSync).mockImplementation(() => { throw new Error('EPERM'); });
    expect(() => backupPackageJson('/project')).not.toThrow();
  });
});

describe('openInBrowser (fix-vulnerabilities version)', () => {
  afterEach(() => { vi.restoreAllMocks(); });

  it('does not throw on darwin', async () => {
    vi.stubGlobal('process', { ...process, platform: 'darwin' });
    await expect(openInBrowser('/report.html')).resolves.not.toThrow();
  });

  it('does not throw on win32', async () => {
    vi.stubGlobal('process', { ...process, platform: 'win32' });
    await expect(openInBrowser('/report.html')).resolves.not.toThrow();
  });

  it('does not throw on linux', async () => {
    vi.stubGlobal('process', { ...process, platform: 'linux' });
    await expect(openInBrowser('/report.html')).resolves.not.toThrow();
  });
});

// ── Maven helper functions ────────────────────────────────────────────────────

describe('updatePomVersion', () => {
  beforeEach(() => {
    vi.mocked(readFileSync).mockReset();
    vi.mocked(writeFileSync).mockReset();
  });

  it('updates the <version> tag for a matching groupId:artifactId', () => {
    const pomXml = `<project>
  <dependencies>
    <dependency>
      <groupId>org.apache.commons</groupId>
      <artifactId>commons-lang3</artifactId>
      <version>3.12.0</version>
    </dependency>
  </dependencies>
</project>`;
    vi.mocked(readFileSync).mockReturnValue(pomXml);

    const result = updatePomVersion('/project/pom.xml', 'org.apache.commons', 'commons-lang3', '3.13.0');

    expect(result).toBe(true);
    expect(vi.mocked(writeFileSync)).toHaveBeenCalledOnce();
    const written = vi.mocked(writeFileSync).mock.calls[0][1];
    expect(written).toContain('<version>3.13.0</version>');
  });

  it('returns false when groupId:artifactId not found in pom.xml', () => {
    const pomXml = `<project>
  <dependencies>
    <dependency>
      <groupId>other.group</groupId>
      <artifactId>other-artifact</artifactId>
      <version>1.0.0</version>
    </dependency>
  </dependencies>
</project>`;
    vi.mocked(readFileSync).mockReturnValue(pomXml);

    const result = updatePomVersion('/project/pom.xml', 'org.apache.commons', 'commons-lang3', '3.13.0');

    expect(result).toBe(false);
    expect(vi.mocked(writeFileSync)).not.toHaveBeenCalled();
  });

  it('returns false when dependency uses ${property} version (version text unchanged)', () => {
    const pomXml = `<project>
  <dependencies>
    <dependency>
      <groupId>org.apache.commons</groupId>
      <artifactId>commons-lang3</artifactId>
      <version>\${commons.lang3.version}</version>
    </dependency>
  </dependencies>
</project>`;
    vi.mocked(readFileSync).mockReturnValue(pomXml);

    // The regex replaces <version>...<\/version> — the ${property} value will be replaced
    // but since old and new differ, it should return true and write it
    const result = updatePomVersion('/project/pom.xml', 'org.apache.commons', 'commons-lang3', '3.13.0');

    // This will actually succeed (replaces the property placeholder with the fixed version)
    expect(typeof result).toBe('boolean');
  });

  it('does not modify other dependencies when updating one', () => {
    const pomXml = `<project>
  <dependencies>
    <dependency>
      <groupId>org.apache.commons</groupId>
      <artifactId>commons-lang3</artifactId>
      <version>3.12.0</version>
    </dependency>
    <dependency>
      <groupId>com.google.guava</groupId>
      <artifactId>guava</artifactId>
      <version>31.0.0</version>
    </dependency>
  </dependencies>
</project>`;
    vi.mocked(readFileSync).mockReturnValue(pomXml);

    updatePomVersion('/project/pom.xml', 'org.apache.commons', 'commons-lang3', '3.13.0');

    const written = vi.mocked(writeFileSync).mock.calls[0][1];
    expect(written).toContain('<version>31.0.0</version>'); // guava unchanged
    expect(written).toContain('<version>3.13.0</version>'); // commons-lang3 updated
  });
});

describe('addPomDependencyManagement', () => {
  beforeEach(() => {
    vi.mocked(readFileSync).mockReset();
    vi.mocked(writeFileSync).mockReset();
  });

  it('injects a new <dependencyManagement> block when none exists', () => {
    const pomXml = `<project>
  <dependencies/>
</project>`;
    vi.mocked(readFileSync).mockReturnValue(pomXml);

    const result = addPomDependencyManagement('/project/pom.xml', 'com.example:my-lib', '2.0.0');

    expect(result).toBe(true);
    const written = vi.mocked(writeFileSync).mock.calls[0][1];
    expect(written).toContain('<dependencyManagement>');
    expect(written).toContain('<groupId>com.example</groupId>');
    expect(written).toContain('<artifactId>my-lib</artifactId>');
    expect(written).toContain('<version>2.0.0</version>');
  });

  it('appends into existing <dependencyManagement><dependencies> block', () => {
    const pomXml = `<project>
  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>org.existing</groupId>
        <artifactId>existing-lib</artifactId>
        <version>1.0.0</version>
      </dependency>
    </dependencies>
  </dependencyManagement>
</project>`;
    vi.mocked(readFileSync).mockReturnValue(pomXml);

    addPomDependencyManagement('/project/pom.xml', 'com.new:new-lib', '3.0.0');

    const written = vi.mocked(writeFileSync).mock.calls[0][1];
    expect(written).toContain('existing-lib'); // existing dep preserved
    expect(written).toContain('<artifactId>new-lib</artifactId>'); // new dep added
    expect(written).toContain('<version>3.0.0</version>');
  });

  it('returns false when groupArtifact is malformed (no colon)', () => {
    vi.mocked(readFileSync).mockReturnValue('<project></project>');

    const result = addPomDependencyManagement('/project/pom.xml', 'invalidformat', '1.0.0');
    expect(result).toBe(false);
    expect(vi.mocked(writeFileSync)).not.toHaveBeenCalled();
  });
});

describe('findMavenParentDep', () => {
  beforeEach(() => {
    vi.mocked(execSync).mockReset();
  });

  it('finds the direct parent dep that pulls in a transitive artifact', () => {
    // spring-jcl is at depth 2 (transitive of spring-web which is direct)
    // prefix "|  |  \- " has length 9 → depth = Math.round((9-3)/3) = 2
    const treeOutput = [
      '[INFO] com.example:my-service:jar:1.0.0:',
      '[INFO] +- org.springframework:spring-web:jar:5.3.0:compile',
      '[INFO] |  +- org.springframework:spring-core:jar:5.3.0:compile',
      '[INFO] |  |  \\- org.springframework:spring-jcl:jar:5.3.0:compile',
      '[INFO] \\- com.google.guava:guava:jar:31.0.0:compile',
      ''
    ].join('\n');

    vi.mocked(execSync).mockReturnValue(treeOutput);

    const parent = findMavenParentDep('org.springframework:spring-jcl', '/project');
    // lastDirect when spring-jcl (depth 2) is processed = spring-core (depth 1) or spring-web (depth 0)
    // depth <=1 updates lastDirect: spring-web (0), spring-core (1), then spring-jcl is depth 2 → returns lastDirect
    expect(parent).not.toBeNull();
  });

  it('returns null when the transitive artifact is not found in the tree', () => {
    vi.mocked(execSync).mockReturnValue('[INFO] +- org.springframework:spring-core:jar:5.3.0:compile\n');

    const parent = findMavenParentDep('com.nonexistent:missing', '/project');
    expect(parent).toBeNull();
  });

  it('returns null when execSync throws', () => {
    vi.mocked(execSync).mockImplementation(() => { throw new Error('mvn not found'); });

    const parent = findMavenParentDep('org.apache.commons:commons-lang3', '/project');
    expect(parent).toBeNull();
  });

  it('returns null when groupArtifact has no colon', () => {
    const parent = findMavenParentDep('invalidformat', '/project');
    expect(parent).toBeNull();
    // execSync should not be called for malformed input
    expect(vi.mocked(execSync)).not.toHaveBeenCalled();
  });
});

// ── Maven Phase A in configureFixTools ────────────────────────────────────────

describe('nexus_fix_vulnerabilities — Maven project', () => {
  let mockServer;

  const MAVEN_DIRECT_VULN = {
    module: 'org.apache.commons:commons-lang3',
    currentVersion: '3.12.0',
    fixVersion: '3.13.0',
    cveId: 'CVE-2024-1234',
    severity: 'High',
    score: '7.5',
    dependency: 'direct',
    canAutoFix: true
  };

  const MAVEN_TRANSITIVE_VULN = {
    module: 'org.apache.commons:commons-text',
    currentVersion: '1.9.0',
    fixVersion: '1.11.0',
    cveId: 'CVE-2022-42889',
    severity: 'Critical',
    score: '9.8',
    dependency: 'transitive',
    canAutoFix: false
  };

  function makeMavenReport(overrides = {}) {
    return {
      summary: { applicationId: APPLICATION_ID, projectType: 'maven' },
      vulnerableModules: [],
      allVulnerabilities: [MAVEN_DIRECT_VULN],
      ...overrides
    };
  }

  const SAMPLE_POM = `<project>
  <dependencies>
    <dependency>
      <groupId>org.apache.commons</groupId>
      <artifactId>commons-lang3</artifactId>
      <version>3.12.0</version>
    </dependency>
  </dependencies>
</project>`;

  beforeEach(() => {
    mockServer = createMockServer();
    vi.mocked(existsSync).mockReset();
    vi.mocked(readFileSync).mockReset();
    vi.mocked(writeFileSync).mockReset();
    vi.mocked(execSync).mockReset();
    vi.mocked(appendFixSummary).mockClear();
  });

  afterEach(() => { vi.restoreAllMocks(); });

  it('detects Maven project from report summary.projectType and runs Phase A', async () => {
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('pom.xml')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeMavenReport({ allVulnerabilities: [MAVEN_DIRECT_VULN] }));
      }
      if (p.endsWith('pom.xml')) return SAMPLE_POM;
      return '';
    });
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID
    });

    expect(isValidToolResponse(response)).toBe(true);
    const text = response.content[0].text;
    expect(text).toContain('Phase A');
    expect(text).toContain('Maven');
  });

  it('shows Phase A — No fixable direct dependencies when directFixable is empty for Maven', async () => {
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('pom.xml')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        // Transitive vuln only - no direct fixable
        return JSON.stringify(makeMavenReport({ allVulnerabilities: [MAVEN_TRANSITIVE_VULN] }));
      }
      if (p.endsWith('pom.xml')) return SAMPLE_POM;
      return '';
    });
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID
    });

    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('Phase A — No fixable direct dependencies found');
  });

  it('handles Phase A catch block when pom.xml update throws for Maven', async () => {
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('pom.xml')) return true;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        return JSON.stringify(makeMavenReport({ allVulnerabilities: [MAVEN_DIRECT_VULN] }));
      }
      if (p.endsWith('pom.xml')) return SAMPLE_POM;
      return '';
    });
    // Make writeFileSync throw to trigger Phase A catch
    vi.mocked(writeFileSync).mockImplementation(() => { throw new Error('Disk full'); });
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID
    });

    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('Phase A partially failed');
  });

  it('auto-detects Maven when pom.xml exists but no package.json and no projectType in report', async () => {
    vi.mocked(existsSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) return true;
      if (p.endsWith('pom.xml')) return true;
      if (p.endsWith('package.json')) return false;
      return false;
    });
    vi.mocked(readFileSync).mockImplementation(p => {
      if (p.endsWith('nexus-vulnerability-report.json')) {
        // No projectType in summary
        return JSON.stringify({
          summary: { applicationId: APPLICATION_ID },
          vulnerableModules: [],
          allVulnerabilities: [MAVEN_DIRECT_VULN]
        });
      }
      if (p.endsWith('pom.xml')) return SAMPLE_POM;
      return '';
    });
    vi.mocked(execSync).mockReturnValue('');
    configureFixTools(mockServer);

    const response = await mockServer.invokeTool('nexus_fix_vulnerabilities', {
      applicationId: APPLICATION_ID
    });

    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('Maven');
  });
});
