import { describe, it, expect, vi, beforeEach } from 'vitest';
import {
  buildJsonReport,
  formatMarkdown,
  formatHtml,
  writeNexusReport,
  appendFixSummary,
  mapCvssToSeverity,
  mapThreatCategory
} from '../src/tools/generate-reports.js';

// Mock fs to avoid writing to disk
vi.mock('fs', () => ({
  writeFileSync: vi.fn(),
  mkdirSync: vi.fn(),
  readFileSync: vi.fn(),
  existsSync: vi.fn(() => true)
}));

import { writeFileSync, mkdirSync, readFileSync, existsSync } from 'fs';

// ── Fixtures ─────────────────────────────────────────────────────────────────

const makeVuln = (overrides = {}) => ({
  component: 'lodash',
  version: '4.17.20',
  vulnId: 'CVE-2021-23337',
  severity: 'High',
  cvss: '7.2',
  description: 'severe',
  fixVersion: '4.17.21',
  referenceUrl: 'https://nvd.nist.gov/vuln/detail/CVE-2021-23337',
  dependency: 'direct',
  remediationTypes: ['next-no-violations'],
  hasNoViolationsFix: true,
  ...overrides
});

const BASE_REPORT_OPTS = {
  applicationId: '51855__DCDAQPR__test-repo',
  branch: 'develop',
  repoName: 'test-repo',
  totalComponentsScanned: 10,
  summary: { Critical: 0, High: 1, Medium: 0, Low: 0, total: 1 },
  vulnerabilities: [makeVuln()],
  scanMode: 'fresh',
  mode: 'pipeline'
};

// ── mapCvssToSeverity ─────────────────────────────────────────────────────────

describe('mapCvssToSeverity', () => {
  it('maps ≥9.0 to Critical', () => expect(mapCvssToSeverity(9.0)).toBe('Critical'));
  it('maps ≥7.0 to High', () => expect(mapCvssToSeverity(7.0)).toBe('High'));
  it('maps ≥4.0 to Medium', () => expect(mapCvssToSeverity(4.0)).toBe('Medium'));
  it('maps >0 to Low', () => expect(mapCvssToSeverity(0.1)).toBe('Low'));
  it('maps 0 to None', () => expect(mapCvssToSeverity(0)).toBe('None'));
  it('maps 9.8 to Critical', () => expect(mapCvssToSeverity(9.8)).toBe('Critical'));
});

// ── mapThreatCategory ────────────────────────────────────────────────────────

describe('mapThreatCategory', () => {
  it('maps "critical" to Critical', () => expect(mapThreatCategory('critical')).toBe('Critical'));
  it('maps "severe" to High', () => expect(mapThreatCategory('severe')).toBe('High'));
  it('maps "moderate" to Medium', () => expect(mapThreatCategory('moderate')).toBe('Medium'));
  it('maps anything else to Low', () => expect(mapThreatCategory('minor')).toBe('Low'));
  it('maps empty string to Low', () => expect(mapThreatCategory('')).toBe('Low'));
});

// ── buildJsonReport ──────────────────────────────────────────────────────────

describe('buildJsonReport', () => {
  it('returns the correct summary shape', () => {
    const report = buildJsonReport(BASE_REPORT_OPTS);
    expect(report.summary.applicationId).toBe('51855__DCDAQPR__test-repo');
    expect(report.summary.branch).toBe('develop');
    expect(report.summary.repoName).toBe('test-repo');
    expect(report.summary.totalComponents).toBe(10);
    expect(report.summary.totalVulnerabilities).toBe(1);
    expect(report.summary.vulnerableComponents).toBe(1);
    expect(report.summary.mode).toBe('pipeline');
    expect(report.summary.scanMode).toBe('fresh');
    expect(report.summary.scanDate).toBeDefined();
  });

  it('includes vulnerableModules grouped by component', () => {
    const vulns = [
      makeVuln({ vulnId: 'CVE-1' }),
      makeVuln({ vulnId: 'CVE-2' }) // same component
    ];
    const report = buildJsonReport({ ...BASE_REPORT_OPTS, vulnerabilities: vulns });
    expect(report.vulnerableModules).toHaveLength(1); // grouped
    expect(report.vulnerableModules[0].cveCount).toBe(2);
    expect(report.vulnerableModules[0].cves).toHaveLength(2);
  });

  it('includes allVulnerabilities as a flat array', () => {
    const vulns = [makeVuln({ vulnId: 'CVE-1' }), makeVuln({ vulnId: 'CVE-2' })];
    const report = buildJsonReport({ ...BASE_REPORT_OPTS, vulnerabilities: vulns });
    expect(report.allVulnerabilities).toHaveLength(2);
    expect(report.allVulnerabilities[0].cveId).toBe('CVE-1');
    expect(report.allVulnerabilities[1].cveId).toBe('CVE-2');
  });

  it('sets canAutoFix=true for direct deps with a fixVersion', () => {
    const report = buildJsonReport(BASE_REPORT_OPTS);
    expect(report.vulnerableModules[0].cves[0].canAutoFix).toBe(true);
  });

  it('sets canAutoFix=false for transitive deps', () => {
    const opts = { ...BASE_REPORT_OPTS, vulnerabilities: [makeVuln({ dependency: 'transitive' })] };
    const report = buildJsonReport(opts);
    expect(report.vulnerableModules[0].cves[0].canAutoFix).toBe(false);
  });

  it('marks isNewCve=true for CVE-2025-* references', () => {
    const opts = {
      ...BASE_REPORT_OPTS,
      vulnerabilities: [makeVuln({ vulnId: 'CVE-2025-12345' })]
    };
    const report = buildJsonReport(opts);
    expect(report.vulnerableModules[0].cves[0].isNewCve).toBe(true);
  });

  it('marks isNewCve=false for older CVEs', () => {
    const report = buildJsonReport(BASE_REPORT_OPTS);
    expect(report.vulnerableModules[0].cves[0].isNewCve).toBe(false);
  });

  it('sets dependency=direct for packages in package.json.dependencies', () => {
    const report = buildJsonReport(BASE_REPORT_OPTS);
    expect(report.vulnerableModules[0].dependency).toBe('direct');
    expect(report.vulnerableModules[0].modulePath).toBe('lodash');
  });

  it('sets dependency=transitive and (transitive) path prefix for non-direct packages', () => {
    const opts = { ...BASE_REPORT_OPTS, vulnerabilities: [makeVuln({ dependency: 'transitive' })] };
    const report = buildJsonReport(opts);
    expect(report.vulnerableModules[0].dependency).toBe('transitive');
    expect(report.vulnerableModules[0].modulePath).toContain('(transitive)');
  });

  it('returns cves[0].fixVersion as bare version string (not ≥-prefixed)', () => {
    const report = buildJsonReport(BASE_REPORT_OPTS);
    expect(report.vulnerableModules[0].cves[0].fixVersion).toBe('4.17.21');
  });

  it('returns "Check CVE" when fixVersion is null', () => {
    const opts = { ...BASE_REPORT_OPTS, vulnerabilities: [makeVuln({ fixVersion: null })] };
    const report = buildJsonReport(opts);
    expect(report.vulnerableModules[0].cves[0].fixVersion).toBe('Check CVE');
  });

  it('sorts vulnerableModules by highestScore descending', () => {
    const opts = {
      ...BASE_REPORT_OPTS,
      vulnerabilities: [
        makeVuln({ component: 'low-pkg', version: '1.0', vulnId: 'CVE-LOW', cvss: '4.5', severity: 'Medium' }),
        makeVuln({ component: 'high-pkg', version: '2.0', vulnId: 'CVE-HIGH', cvss: '9.8', severity: 'Critical' })
      ]
    };
    const report = buildJsonReport(opts);
    expect(report.vulnerableModules[0].module).toBe('high-pkg');
    expect(report.vulnerableModules[1].module).toBe('low-pkg');
  });
});

// ── formatMarkdown ────────────────────────────────────────────────────────────

describe('formatMarkdown', () => {
  it('includes the application ID in the output', () => {
    const report = buildJsonReport(BASE_REPORT_OPTS);
    const md = formatMarkdown(report);
    expect(md).toContain('51855__DCDAQPR__test-repo');
  });

  it('contains a Severity Summary table', () => {
    const report = buildJsonReport(BASE_REPORT_OPTS);
    const md = formatMarkdown(report);
    expect(md).toContain('| Severity | Count |');
  });

  it('contains a Vulnerability Details table header', () => {
    const report = buildJsonReport(BASE_REPORT_OPTS);
    const md = formatMarkdown(report);
    expect(md).toContain('| Module | Current Version');
  });

  it('includes the CVE ID as a link in the table', () => {
    const report = buildJsonReport(BASE_REPORT_OPTS);
    const md = formatMarkdown(report);
    expect(md).toContain('[CVE-2021-23337]');
  });

  it('adds [New CVE] badge for 2025+ CVEs', () => {
    const opts = { ...BASE_REPORT_OPTS, vulnerabilities: [makeVuln({ vulnId: 'CVE-2025-99999' })] };
    const report = buildJsonReport(opts);
    const md = formatMarkdown(report);
    expect(md).toContain('[New CVE]');
  });

  it('includes Pipeline-Aligned note for pipeline mode', () => {
    const report = buildJsonReport(BASE_REPORT_OPTS);
    const md = formatMarkdown(report);
    expect(md).toContain('Pipeline-aligned mode');
  });

  it('includes Deep scan note for deep mode', () => {
    const report = buildJsonReport({ ...BASE_REPORT_OPTS, mode: 'deep' });
    const md = formatMarkdown(report);
    expect(md).toContain('Deep scan mode');
  });
});

// ── formatHtml ────────────────────────────────────────────────────────────────

describe('formatHtml', () => {
  it('produces valid HTML with a title', () => {
    const report = buildJsonReport(BASE_REPORT_OPTS);
    const html = formatHtml(report);
    expect(html).toContain('<!DOCTYPE html>');
    expect(html).toContain('Nexus IQ Vulnerability Report');
  });

  it('includes the application metadata', () => {
    const report = buildJsonReport(BASE_REPORT_OPTS);
    const html = formatHtml(report);
    expect(html).toContain('51855__DCDAQPR__test-repo');
    expect(html).toContain('test-repo');
    expect(html).toContain('develop');
  });

  it('renders no-vulnerabilities block when list is empty', () => {
    const opts = { ...BASE_REPORT_OPTS, vulnerabilities: [], summary: { Critical: 0, High: 0, Medium: 0, Low: 0, total: 0 } };
    const report = buildJsonReport(opts);
    const html = formatHtml(report);
    expect(html).toContain('No Vulnerabilities Found');
  });

  it('renders [New CVE] badge span for 2025+ CVEs', () => {
    const opts = { ...BASE_REPORT_OPTS, vulnerabilities: [makeVuln({ vulnId: 'CVE-2026-1234' })] };
    const report = buildJsonReport(opts);
    const html = formatHtml(report);
    expect(html).toContain('badge-new-cve');
    expect(html).toContain('New CVE');
  });

  it('renders direct/transitive dependency badges', () => {
    const opts = {
      ...BASE_REPORT_OPTS,
      vulnerabilities: [
        makeVuln({ dependency: 'direct' }),
        makeVuln({ component: 'axios', version: '0.21.0', vulnId: 'CVE-X', dependency: 'transitive' })
      ]
    };
    const report = buildJsonReport(opts);
    const html = formatHtml(report);
    expect(html).toContain('badge-direct');
    expect(html).toContain('badge-transitive');
  });
});

// ── writeNexusReport ─────────────────────────────────────────────────────────

describe('writeNexusReport', () => {
  beforeEach(() => {
    vi.mocked(mkdirSync).mockClear();
    vi.mocked(writeFileSync).mockClear();
  });

  it('creates the nexus-report directory', () => {
    const report = buildJsonReport(BASE_REPORT_OPTS);
    writeNexusReport(report);
    expect(mkdirSync).toHaveBeenCalledWith(expect.stringContaining('nexus-report'), { recursive: true });
  });

  it('writes JSON, MD, and HTML files', () => {
    const report = buildJsonReport(BASE_REPORT_OPTS);
    writeNexusReport(report);
    const paths = vi.mocked(writeFileSync).mock.calls.map(c => c[0]);
    expect(paths.some(p => p.endsWith('nexus-vulnerability-report.json'))).toBe(true);
    expect(paths.some(p => p.endsWith('nexus-vulnerability-report.md'))).toBe(true);
    expect(paths.some(p => p.endsWith('nexus-vulnerability-report.html'))).toBe(true);
  });

  it('returns the report directory path', () => {
    const report = buildJsonReport(BASE_REPORT_OPTS);
    const dir = writeNexusReport(report);
    expect(dir).toContain('nexus-report');
  });
});

// ── appendFixSummary ─────────────────────────────────────────────────────────

describe('appendFixSummary', () => {
  const FIX_SUMMARY = {
    fixDate: '1/1/2025',
    totalOriginal: 3,
    totalFixed: 2,
    totalRemaining: 1,
    byMethod: { packageJsonUpdate: 1, yarnUpgrade: 1, parentUpgrade: 0, resolution: 0 },
    fixedModules: [
      { module: 'lodash', cveId: 'CVE-2021-23337', severity: 'High', dependency: 'direct', fixMethod: 'package.json update', oldVersion: '4.17.20', newVersion: '4.17.21' }
    ],
    remainingModules: [
      { module: 'some-dep', cveId: 'CVE-X', severity: 'Medium', dependency: 'transitive', reason: 'No fix available' }
    ]
  };

  beforeEach(() => {
    vi.mocked(writeFileSync).mockClear();
    vi.mocked(readFileSync)
      .mockReturnValueOnce(JSON.stringify({ summary: {}, vulnerableModules: [] })) // JSON parse
      .mockReturnValueOnce('# Existing Report\n') // md content
      .mockReturnValueOnce('<html><body>existing</body></html>'); // html content
  });

  it('merges fixSummary key into existing JSON report', () => {
    appendFixSummary(FIX_SUMMARY);
    const jsonCall = vi.mocked(writeFileSync).mock.calls.find(c => c[0].endsWith('.json'));
    expect(jsonCall).toBeDefined();
    const written = JSON.parse(jsonCall[1]);
    expect(written.fixSummary.totalFixed).toBe(2);
    expect(written.fixSummary.totalRemaining).toBe(1);
  });

  it('appends ## Fix Report section to markdown file', () => {
    appendFixSummary(FIX_SUMMARY);
    const mdCall = vi.mocked(writeFileSync).mock.calls.find(c => c[0].endsWith('.md'));
    expect(mdCall).toBeDefined();
    expect(mdCall[1]).toContain('## Fix Report');
    expect(mdCall[1]).toContain('lodash');
    expect(mdCall[1]).toContain('package.json update');
  });

  it('injects fix section into HTML before </body>', () => {
    appendFixSummary(FIX_SUMMARY);
    const htmlCall = vi.mocked(writeFileSync).mock.calls.find(c => c[0].endsWith('.html'));
    expect(htmlCall).toBeDefined();
    expect(htmlCall[1]).toContain('<h2>🔧 Fix Report</h2>');
    expect(htmlCall[1]).not.toContain('</body>\n</body>'); // not double-appended
  });

  it('handles corrupt JSON gracefully (does not throw)', () => {
    vi.mocked(readFileSync).mockReset();
    vi.mocked(readFileSync)
      .mockReturnValueOnce('INVALID JSON{{{{') // corrupt JSON
      .mockReturnValueOnce('# Report\n')
      .mockReturnValueOnce('<body></body>');

    expect(() => appendFixSummary(FIX_SUMMARY)).not.toThrow();
  });

  it('skips writing files that do not exist (existsSync=false)', () => {
    vi.mocked(writeFileSync).mockClear();
    vi.mocked(existsSync).mockReturnValue(false);

    expect(() => appendFixSummary(FIX_SUMMARY)).not.toThrow();
    // No writes should have occurred (files don't exist)
    expect(vi.mocked(writeFileSync)).not.toHaveBeenCalled();

    // Restore for subsequent tests
    vi.mocked(existsSync).mockReturnValue(true);
  });

  it('renders all fix method badge classes in HTML', () => {
    const fixSummaryAllMethods = {
      ...FIX_SUMMARY,
      fixedModules: [
        { module: 'a', cveId: 'CVE-1', severity: 'High', dependency: 'direct', fixMethod: 'yarn upgrade', oldVersion: '1.0', newVersion: '1.1' },
        { module: 'b', cveId: 'CVE-2', severity: 'High', dependency: 'transitive', fixMethod: 'parent upgrade', oldVersion: '2.0', newVersion: '2.1' },
        { module: 'c', cveId: 'CVE-3', severity: 'Medium', dependency: 'transitive', fixMethod: 'resolution', oldVersion: '3.0', newVersion: '3.1' }
      ]
    };
    vi.mocked(readFileSync).mockReset();
    vi.mocked(readFileSync)
      .mockReturnValueOnce(JSON.stringify({}))
      .mockReturnValueOnce('# Report\n')
      .mockReturnValueOnce('<body></body>');

    appendFixSummary(fixSummaryAllMethods);
    const htmlCall = vi.mocked(writeFileSync).mock.calls.find(c => c[0].endsWith('.html'));
    expect(htmlCall[1]).toContain('badge-fix-yarn');
    expect(htmlCall[1]).toContain('badge-fix-parent');
    expect(htmlCall[1]).toContain('badge-fix-resolution');
  });
});

// ── Additional branch-coverage tests ─────────────────────────────────────────

describe('buildJsonReport — edge cases', () => {
  it('uses default scanMode="fresh" when scanMode is null', () => {
    const report = buildJsonReport({ ...BASE_REPORT_OPTS, scanMode: null });
    expect(report.summary.scanMode).toBe('fresh');
  });

  it('uses default mode="pipeline" when mode is null', () => {
    const report = buildJsonReport({ ...BASE_REPORT_OPTS, mode: null });
    expect(report.summary.mode).toBe('pipeline');
  });

  it('uses "transitive" dependency when vuln.dependency is falsy', () => {
    const opts = { ...BASE_REPORT_OPTS, vulnerabilities: [makeVuln({ dependency: undefined })] };
    const report = buildJsonReport(opts);
    expect(report.vulnerableModules[0].dependency).toBe('transitive');
    expect(report.allVulnerabilities[0].dependency).toBe('transitive');
  });

  it('isFutureCve returns false for vulnId with no CVE year match (null cveId)', () => {
    const opts = { ...BASE_REPORT_OPTS, vulnerabilities: [makeVuln({ vulnId: null })] };
    const report = buildJsonReport(opts);
    // vulnId null → isFutureCve(null) → false
    expect(report.vulnerableModules[0].cves[0].isNewCve).toBe(false);
  });

  it('updates highestScore when second CVE for same module has higher score', () => {
    const vulns = [
      makeVuln({ vulnId: 'CVE-LOW', cvss: '4.5', description: 'moderate' }),
      makeVuln({ vulnId: 'CVE-HIGH', cvss: '9.8', description: 'critical' }) // same lodash component
    ];
    const report = buildJsonReport({ ...BASE_REPORT_OPTS, vulnerabilities: vulns });
    // highestScore should be updated to 9.8 on the second CVE addition
    expect(parseFloat(report.vulnerableModules[0].highestScore)).toBe(9.8);
  });
});

describe('formatMarkdown — branch coverage', () => {
  it('renders multiple CVEs per module (i>0 loop iterations)', () => {
    const vulns = [
      makeVuln({ vulnId: 'CVE-1' }),
      makeVuln({ vulnId: 'CVE-2' }) // same component
    ];
    const report = buildJsonReport({ ...BASE_REPORT_OPTS, vulnerabilities: vulns });
    const md = formatMarkdown(report);
    expect(md).toContain('CVE-1');
    expect(md).toContain('CVE-2');
  });

  it('skips zero-count severity rows in summary table', () => {
    const report = buildJsonReport(BASE_REPORT_OPTS); // has High=1, rest=0
    const md = formatMarkdown(report);
    expect(md).not.toMatch(/\| Low\s*\|\s*0\s*\|/);
  });
});

describe('formatHtml — branch coverage', () => {
  it('renders deep scan mode label in HTML header', () => {
    const report = buildJsonReport({ ...BASE_REPORT_OPTS, mode: 'deep' });
    const html = formatHtml(report);
    expect(html).toContain('Deep Scan');
    expect(html).toContain('Deep scan mode');
  });

  it('renders multiple CVEs per module in HTML (i>0 loop iterations)', () => {
    const vulns = [
      makeVuln({ vulnId: 'CVE-A' }),
      makeVuln({ vulnId: 'CVE-B' }) // same component
    ];
    const report = buildJsonReport({ ...BASE_REPORT_OPTS, vulnerabilities: vulns });
    const html = formatHtml(report);
    expect(html).toContain('CVE-A');
    expect(html).toContain('CVE-B');
  });

  it('renders badge for medium severity', () => {
    const opts = {
      ...BASE_REPORT_OPTS,
      vulnerabilities: [makeVuln({ cvss: '5.5', severity: 'Medium', description: 'moderate' })]
    };
    const report = buildJsonReport(opts);
    const html = formatHtml(report);
    expect(html).toContain('badge-medium');
  });
});

describe('appendFixSummary — edge cases', () => {
  beforeEach(() => {
    vi.mocked(writeFileSync).mockClear();
    vi.mocked(existsSync).mockReturnValue(true);
  });

  it('renders resolution fix method badge in HTML', () => {
    const resolutionSummary = {
      fixDate: '1/1/2025',
      totalOriginal: 1,
      totalFixed: 1,
      totalRemaining: 0,
      byMethod: { packageJsonUpdate: 0, yarnUpgrade: 0, parentUpgrade: 0, resolution: 1 },
      fixedModules: [
        { module: 'minimist', cveId: 'CVE-1', severity: 'High', dependency: 'transitive', fixMethod: 'resolution', oldVersion: '1.2.5', newVersion: '1.2.6' }
      ],
      remainingModules: []
    };
    vi.mocked(readFileSync)
      .mockReturnValueOnce(JSON.stringify({}))
      .mockReturnValueOnce('# Report\n')
      .mockReturnValueOnce('<body></body>');

    appendFixSummary(resolutionSummary);
    const htmlCall = vi.mocked(writeFileSync).mock.calls.find(c => c[0].endsWith('.html'));
    expect(htmlCall[1]).toContain('badge-fix-resolution');
  });

  it('handles null fixedModules and remainingModules gracefully (|| [] fallback)', () => {
    const summaryWithNulls = {
      fixDate: '1/1/2025',
      totalOriginal: 0,
      totalFixed: 0,
      totalRemaining: 0,
      byMethod: { packageJsonUpdate: 0, yarnUpgrade: 0, parentUpgrade: 0, resolution: 0 },
      fixedModules: null,
      remainingModules: null
    };
    vi.mocked(readFileSync)
      .mockReturnValueOnce(JSON.stringify({}))
      .mockReturnValueOnce('# Report\n')
      .mockReturnValueOnce('<body></body>');

    expect(() => appendFixSummary(summaryWithNulls)).not.toThrow();
  });
});

// ── Additional branch coverage ─────────────────────────────────────────────────

describe('formatMarkdown — additional branches', () => {
  it('uses "transitive" depLabel when mod.dependency is not "direct"', () => {
    const opts = { ...BASE_REPORT_OPTS, vulnerabilities: [makeVuln({ dependency: 'transitive' })] };
    const report = buildJsonReport(opts);
    const md = formatMarkdown(report);
    expect(md).toContain('transitive');
  });

  it('renders [New CVE] badge for second CVE in a multi-CVE module', () => {
    const opts = {
      ...BASE_REPORT_OPTS,
      vulnerabilities: [
        makeVuln({ vulnId: 'CVE-2021-1', cvss: '7.5' }),
        makeVuln({ vulnId: 'CVE-2025-99999', cvss: '6.0' }) // same component, 2nd CVE has isNewCve=true
      ]
    };
    const report = buildJsonReport(opts);
    const md = formatMarkdown(report);
    // The second CVE (i=1 loop) should get the [New CVE] badge
    expect(md).toContain('[New CVE]');
  });
});

describe('formatHtml — additional branches', () => {
  it('uses empty string for badge class when highestSeverity is null', () => {
    // Build manually a report where highestSeverity is null/empty
    const report = {
      summary: {
        applicationId: 'test',
        scanDate: '1/1/2025',
        mode: 'pipeline',
        totalComponents: 1,
        vulnerableComponents: 1,
        totalVulnerabilities: 1,
        severityCounts: { Critical: 0, High: 0, Medium: 1, Low: 0 }
      },
      vulnerableModules: [{
        module: 'pkg',
        currentVersion: '1.0.0',
        dependency: 'direct',
        modulePath: 'pkg',
        highestSeverity: null,  // null severity → (sev || '') in badgeClass
        highestScore: '5.0',
        cveCount: 1,
        cves: [{ cveId: 'CVE-2021-1', cveLink: 'https://example.com', severity: 'Medium', score: '5.0', fixVersion: '1.0.1', isNewCve: false }]
      }]
    };
    const html = formatHtml(report);
    expect(html).toContain('badge-'); // class generated without crashing
  });

  it('renders [New CVE] badge for second CVE in a multi-CVE module (HTML)', () => {
    const opts = {
      ...BASE_REPORT_OPTS,
      vulnerabilities: [
        makeVuln({ vulnId: 'CVE-2021-1', cvss: '7.5' }),
        makeVuln({ vulnId: 'CVE-2025-99999', cvss: '6.0' })
      ]
    };
    const report = buildJsonReport(opts);
    const html = formatHtml(report);
    // Second CVE row (i=1 loop in HTML template) should contain New CVE badge
    expect(html).toContain('badge-new-cve');
  });
});
