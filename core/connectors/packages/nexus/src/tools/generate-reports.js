import { writeFileSync, mkdirSync, readFileSync, existsSync } from 'fs';
import { join } from 'path';

// ── Severity helpers ─────────────────────────────────────────────────────────

/**
 * Map a numeric CVSS score to a severity text label.
 * @param {number} score
 * @returns {string}
 */
export function mapCvssToSeverity(score) {
  if (score >= 9.0) return 'Critical';
  if (score >= 7.0) return 'High';
  if (score >= 4.0) return 'Medium';
  if (score > 0) return 'Low';
  return 'None';
}

/**
 * Map Nexus threatCategory string to a display severity label.
 * @param {string} description
 * @returns {string}
 */
export function mapThreatCategory(description) {
  const d = (description || '').toLowerCase();
  if (d === 'critical') return 'Critical';
  if (d === 'severe') return 'High';
  if (d === 'moderate') return 'Medium';
  return 'Low';
}

// ── CVE / New-CVE helpers ────────────────────────────────────────────────────

/**
 * Returns true if the CVE ID is from 2025 or later.
 * @param {string} cveId
 * @returns {boolean}
 */
function isFutureCve(cveId) {
  const match = (cveId || '').match(/^CVE-(\d{4})-/);
  return match ? parseInt(match[1], 10) >= 2025 : false;
}

/**
 * Returns true if the vuln ID looks like a Sonatype proprietary ID.
 * @param {string} vulnId
 * @returns {boolean}
 */
function isSonatypeId(vulnId) {
  return (vulnId || '').toLowerCase().startsWith('sonatype-');
}

// ── Vulnerable-modules builder ───────────────────────────────────────────────

/**
 * Group a flat vulnerability list by component+version into vulnerableModules format.
 * @param {Array} vulnerabilities
 * @returns {Array}
 */
function buildVulnerableModules(vulnerabilities) {
  const moduleMap = new Map();

  for (const v of vulnerabilities) {
    const key = `${v.component}@${v.version}`;
    if (!moduleMap.has(key)) {
      moduleMap.set(key, {
        module: v.component,
        currentVersion: v.version,
        dependency: v.dependency || 'transitive',
        modulePath: v.dependency === 'direct' ? v.component : `(transitive) → ${v.component}`,
        highestSeverity: v.severity,
        highestScore: String(v.cvss),
        cveCount: 0,
        cves: []
      });
    }

    const mod = moduleMap.get(key);
    mod.cves.push({
      cveId: v.vulnId,
      cveLink: v.referenceUrl,
      severity: mapThreatCategory(v.description),
      score: String(v.cvss),
      fixVersion: v.fixVersion || 'Check CVE',
      description: v.description,
      canAutoFix: v.dependency === 'direct' && !!v.fixVersion,
      isNewCve: isFutureCve(v.vulnId)
    });
    mod.cveCount += 1;

    if (parseFloat(v.cvss) > parseFloat(mod.highestScore)) {
      mod.highestScore = String(v.cvss);
      mod.highestSeverity = v.severity;
    }
  }

  return Array.from(moduleMap.values()).sort(
    (a, b) => parseFloat(b.highestScore) - parseFloat(a.highestScore)
  );
}

/**
 * Build the flat allVulnerabilities array (one entry per CVE, not per module).
 * @param {Array} vulnerabilities
 * @returns {Array}
 */
function buildAllVulnerabilities(vulnerabilities) {
  return vulnerabilities.map(v => ({
    module: v.component,
    currentVersion: v.version,
    fixVersion: v.fixVersion || null,
    cveId: v.vulnId,
    severity: v.severity,
    score: String(v.cvss),
    dependency: v.dependency || 'transitive',
    canAutoFix: v.dependency === 'direct' && !!v.fixVersion,
    isNewCve: isFutureCve(v.vulnId)
  }));
}

// ── Report builder ───────────────────────────────────────────────────────────

/**
 * Build the full JSON report object.
 * @param {Object} opts
 * @param {string} opts.applicationId
 * @param {string} opts.branch
 * @param {string} opts.repoName
 * @param {number} opts.totalComponentsScanned
 * @param {Object} opts.summary - { Critical, High, Medium, Low, total }
 * @param {Array}  opts.vulnerabilities - enriched flat vulnerability list
 * @param {string} opts.scanMode - 'fresh' | 'existing'
 * @param {string} opts.mode - 'pipeline' | 'deep'
 * @param {string} [opts.projectType] - 'npm' | 'maven'
 * @returns {Object}
 */
export function buildJsonReport({ applicationId, branch, repoName, totalComponentsScanned, summary, vulnerabilities, scanMode, mode, projectType }) {
  const vulnerableModules = buildVulnerableModules(vulnerabilities);
  const allVulns = buildAllVulnerabilities(vulnerabilities);

  const severityCounts = { Critical: 0, High: 0, Medium: 0, Low: 0 };
  for (const v of vulnerabilities) {
    const cat = mapThreatCategory(v.description);
    severityCounts[cat] = (severityCounts[cat] || 0) + 1;
  }

  return {
    summary: {
      applicationId,
      branch,
      repoName,
      scanDate: new Date().toLocaleString(),
      scanMode: scanMode || 'fresh',
      mode: mode || 'pipeline',
      projectType: projectType || 'npm',
      totalComponents: totalComponentsScanned,
      vulnerableComponents: vulnerableModules.length,
      totalVulnerabilities: vulnerabilities.length,
      severityCounts
    },
    vulnerableModules,
    allVulnerabilities: allVulns
  };
}

// ── Markdown formatter ───────────────────────────────────────────────────────

/**
 * Format the report as a Markdown string.
 * @param {Object} report
 * @returns {string}
 */
export function formatMarkdown(report) {
  const { summary, vulnerableModules } = report;
  const modeNote = summary.mode === 'pipeline'
    ? '\n> ℹ️  **Pipeline-aligned mode:** informational and dev-only findings excluded.\n'
    : '\n> ℹ️  **Deep scan mode:** all findings including devDependencies are reported.\n';

  const lines = [
    '# Nexus IQ Vulnerability Report',
    '',
    `**Application:** ${summary.applicationId}`,
    `**Repository:** ${summary.repoName}`,
    `**Branch:** ${summary.branch}`,
    `**Scan Date:** ${summary.scanDate}`,
    `**Scan Mode:** ${summary.mode === 'deep' ? 'Deep Scan' : 'Pipeline-Aligned'}`,
    `**Total Components Scanned:** ${summary.totalComponents}`,
    `**Vulnerable Components:** ${summary.vulnerableComponents}`,
    `**Total Vulnerabilities:** ${summary.totalVulnerabilities}`,
    modeNote,
    '---',
    '',
    '## Summary',
    '',
    '| Severity | Count |',
    '|----------|-------|',
  ];

  for (const [sev, count] of Object.entries(summary.severityCounts)) {
    if (count > 0) lines.push(`| ${sev} | ${count} |`);
  }

  lines.push(
    '',
    '---',
    '',
    '## Vulnerability Details',
    '',
    '> **Note:** Click on the CVE links to view detailed vulnerability information and recommended fix versions.',
    '',
    '| Module | Current Version | CVE / ID | Score | Fix Version | Highest Severity | Dependency | Module Path |',
    '|--------|----------------|----------|-------|-------------|------------------|------------|-------------|'
  );

  for (const mod of vulnerableModules) {
    const depLabel = mod.dependency === 'direct' ? 'direct' : 'transitive';
    const first = mod.cves[0];
    const newCveBadge = first.isNewCve ? ' `[New CVE]`' : '';
    lines.push(
      `| **${mod.module}** | ${mod.currentVersion} | [${first.cveId}](${first.cveLink})${newCveBadge} | ${first.score} | ${first.fixVersion} | ${mod.highestSeverity} | ${depLabel} | \`${mod.modulePath}\` |`
    );
    for (let i = 1; i < mod.cves.length; i++) {
      const cve = mod.cves[i];
      const newBadge = cve.isNewCve ? ' `[New CVE]`' : '';
      lines.push(`| | | [${cve.cveId}](${cve.cveLink})${newBadge} | ${cve.score} | ${cve.fixVersion} | | | |`);
    }
  }

  lines.push(
    '',
    '---',
    '',
    '## Recommendations',
    '',
    '1. Review and update vulnerable dependencies',
    '2. For direct dependencies, update `package.json`',
    '3. For transitive dependencies, update parent packages or add `resolutions`/`overrides`',
    '4. Test thoroughly after updates',
    '5. Re-run scan to verify fixes'
  );

  return lines.join('\n');
}

// ── HTML formatter ───────────────────────────────────────────────────────────

/**
 * Format the report as an HTML string.
 * @param {Object} report
 * @returns {string}
 */
export function formatHtml(report) {
  const { summary, vulnerableModules } = report;
  const badgeClass = (sev) => `badge-${(sev || '').toLowerCase()}`;
  const modeLabel = summary.mode === 'deep' ? 'Deep Scan' : 'Pipeline-Aligned';
  const modeNote = summary.mode === 'pipeline'
    ? '<p style="background:#e3f2fd;padding:12px;border-radius:4px;border-left:4px solid #2196f3;margin:15px 0;"><strong>ℹ️  Pipeline-aligned mode:</strong> informational and dev-only findings excluded.</p>'
    : '<p style="background:#fce4ec;padding:12px;border-radius:4px;border-left:4px solid #e91e63;margin:15px 0;"><strong>ℹ️  Deep scan mode:</strong> all findings including devDependencies are reported.</p>';

  const tableRows = vulnerableModules.map(mod => {
    const rowspan = mod.cves.length;
    const firstCve = mod.cves[0];
    const depBadge = `<span class="badge badge-${mod.dependency === 'direct' ? 'direct' : 'transitive'}">${mod.dependency}</span>`;
    let html = `<tr>
                    <td rowspan="${rowspan}" style="vertical-align:middle;"><strong>${mod.module}</strong></td>
                    <td rowspan="${rowspan}" style="vertical-align:middle;">${mod.currentVersion}</td>
                    <td style="white-space:nowrap;"><a href="${firstCve.cveLink}" target="_blank" rel="noopener">${firstCve.cveId}</a>${firstCve.isNewCve ? ' <span class="badge badge-new-cve">New CVE</span>' : ''}</td>
                    <td style="text-align:center;">${firstCve.score}</td>
                    <td style="white-space:nowrap;">${firstCve.fixVersion}</td>
                    <td rowspan="${rowspan}" style="vertical-align:middle;text-align:center;"><span class="badge ${badgeClass(mod.highestSeverity)}">${mod.highestSeverity}</span></td>
                    <td rowspan="${rowspan}" style="vertical-align:middle;text-align:center;">${depBadge}</td>
                    <td rowspan="${rowspan}" style="vertical-align:middle;"><code>${mod.modulePath}</code></td>
                </tr>`;
    for (let i = 1; i < mod.cves.length; i++) {
      const cve = mod.cves[i];
      html += `\n                <tr>
                    <td style="white-space:nowrap;"><a href="${cve.cveLink}" target="_blank" rel="noopener">${cve.cveId}</a>${cve.isNewCve ? ' <span class="badge badge-new-cve">New CVE</span>' : ''}</td>
                    <td style="text-align:center;">${cve.score}</td>
                    <td style="white-space:nowrap;">${cve.fixVersion}</td>
                </tr>`;
    }
    return html;
  }).join('\n');

  const summaryCards = Object.entries(summary.severityCounts)
    .map(([sev, count]) => `<div class="summary-card ${sev.toLowerCase()}">
                <h3>${count}</h3>
                <p>${sev}</p>
            </div>`).join('\n            ');

  const noVulns = vulnerableModules.length === 0
    ? `<div class="no-vulnerabilities"><h3>✅ No Vulnerabilities Found</h3><p>All scanned components are clean.</p></div>`
    : `<table>
            <thead>
                <tr>
                    <th>Module</th><th>Current Version</th><th>CVE / ID</th><th>Score</th>
                    <th>Fix Version</th><th>Highest Severity</th><th>Dependency</th><th>Module Path</th>
                </tr>
            </thead>
            <tbody>
                ${tableRows}
            </tbody>
        </table>`;

  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus IQ Vulnerability Report</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; padding: 20px; }
        .container { max-width: 1400px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; margin-bottom: 20px; font-size: 2.5em; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; margin-bottom: 15px; font-size: 1.8em; }
        .metadata { background: #ecf0f1; padding: 20px; border-radius: 6px; margin-bottom: 30px; }
        .metadata p { margin: 5px 0; font-size: 0.95em; }
        .metadata strong { color: #2c3e50; }
        .summary-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 20px 0; }
        .summary-card { padding: 20px; border-radius: 6px; text-align: center; color: white; }
        .summary-card h3 { font-size: 2em; margin-bottom: 5px; }
        .summary-card p { font-size: 0.9em; opacity: 0.9; }
        .critical { background: #c0392b; } .high { background: #e67e22; } .medium { background: #f39c12; } .low { background: #95a5a6; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 0.9em; background: white; }
        thead { background: #34495e; color: white; }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }
        th { font-weight: 600; text-transform: uppercase; font-size: 0.85em; letter-spacing: 0.5px; }
        tbody tr:hover { background: #f8f9fa; }
        .badge { display: inline-block; padding: 4px 10px; border-radius: 4px; font-size: 0.85em; font-weight: 600; color: white; }
        .badge-critical { background: #c0392b; } .badge-high { background: #e67e22; } .badge-medium { background: #f39c12; } .badge-low { background: #95a5a6; }
        .badge-direct { background: #27ae60; } .badge-transitive { background: #3498db; } .badge-new-cve { background: #9b59b6; font-size: 0.75em; }
        a { color: #3498db; text-decoration: none; } a:hover { text-decoration: underline; }
        .no-vulnerabilities { text-align: center; padding: 40px; background: #d5f4e6; border-radius: 6px; margin: 20px 0; }
        .no-vulnerabilities h3 { color: #27ae60; font-size: 1.5em; margin-bottom: 10px; }
        .timestamp { text-align: center; color: #7f8c8d; margin-top: 30px; font-size: 0.9em; }
        .fix-fixed-row { border-left: 4px solid #27ae60; }
        .fix-remaining-row { border-left: 4px solid #c0392b; }
        .badge-fix-pkg { background: #27ae60; } .badge-fix-yarn { background: #1abc9c; }
        .badge-fix-parent { background: #3498db; } .badge-fix-resolution { background: #e67e22; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Nexus IQ Vulnerability Report</h1>
        <div class="metadata">
            <p><strong>Application:</strong> ${summary.applicationId}</p>
            <p><strong>Repository:</strong> ${summary.repoName}</p>
            <p><strong>Branch:</strong> ${summary.branch}</p>
            <p><strong>Scan Date:</strong> ${summary.scanDate}</p>
            <p><strong>Scan Mode:</strong> ${modeLabel}</p>
            <p><strong>Total Components Scanned:</strong> ${summary.totalComponents}</p>
            <p><strong>Vulnerable Components:</strong> ${summary.vulnerableComponents}</p>
            <p><strong>Total Vulnerabilities:</strong> ${summary.totalVulnerabilities}</p>
        </div>
        <h2>📊 Severity Summary</h2>
        <div class="summary-cards">
            ${summaryCards}
        </div>
        <h2>🔍 Vulnerability Details</h2>
        ${modeNote}
        <p style="background: #e3f2fd; padding: 12px; border-radius: 4px; border-left: 4px solid #2196f3; margin: 15px 0;">
            <strong>💡 Note:</strong> Click on the CVE links to view detailed vulnerability information. <strong>New CVE</strong> badges indicate findings published in 2025 or later.
        </p>
        ${noVulns}
        <p class="timestamp">Report generated: ${summary.scanDate}</p>
    </div>
</body>
</html>`;
}

// ── Report writer ────────────────────────────────────────────────────────────

/**
 * Write the full vulnerability report to nexus-report/ (JSON + MD + HTML).
 * @param {Object} jsonReport
 * @returns {string} Path to the report directory
 */
export function writeNexusReport(jsonReport) {
  const reportDir = join(process.cwd(), 'nexus-report');
  mkdirSync(reportDir, { recursive: true });
  writeFileSync(join(reportDir, 'nexus-vulnerability-report.json'), JSON.stringify(jsonReport, null, 2), 'utf8');
  writeFileSync(join(reportDir, 'nexus-vulnerability-report.md'), formatMarkdown(jsonReport), 'utf8');
  writeFileSync(join(reportDir, 'nexus-vulnerability-report.html'), formatHtml(jsonReport), 'utf8');
  return reportDir;
}

// ── Fix report appender ──────────────────────────────────────────────────────

/**
 * Format the fix summary as a Markdown section to append.
 * @param {Object} fixSummary
 * @returns {string}
 */
function formatFixSectionMarkdown(fixSummary) {
  const lines = [
    '',
    '---',
    '',
    '## Fix Report',
    '',
    `**Fix Date:** ${fixSummary.fixDate}`,
    `**Original Vulnerabilities:** ${fixSummary.totalOriginal}`,
    `**Fixed:** ${fixSummary.totalFixed}`,
    `**Remaining:** ${fixSummary.totalRemaining}`,
    '',
    '### Fixed Vulnerabilities',
    '',
    '| Module | CVE(s) | Severity | Dependency Type | Fix Method | Old Version | New Version |',
    '|--------|--------|----------|-----------------|------------|-------------|-------------|',
  ];

  for (const f of fixSummary.fixedModules || []) {
    lines.push(`| ${f.module} | ${f.cveId} | ${f.severity} | ${f.dependency} | ${f.fixMethod} | ${f.oldVersion} | ${f.newVersion} |`);
  }

  lines.push(
    '',
    '### Fix Method Legend',
    '',
    '| Method | Description |',
    '|--------|-------------|',
    '| package.json update | Direct dependency version bumped in package.json |',
    '| yarn upgrade | Resolved automatically via `yarn upgrade` |',
    '| parent upgrade | Parent direct dependency upgraded |',
    '| resolution | Forced version via `resolutions`/`overrides` in package.json |',
    '',
    '### Remaining Unresolved Vulnerabilities',
    '',
    '| Module | CVE(s) | Severity | Dependency Type | Reason |',
    '|--------|--------|----------|-----------------|--------|',
  );

  for (const r of fixSummary.remainingModules || []) {
    lines.push(`| ${r.module} | ${r.cveId} | ${r.severity} | ${r.dependency} | ${r.reason} |`);
  }

  lines.push(
    '',
    '### Recommendations',
    '',
    '- Re-run Nexus scan to verify all fixes are effective',
    '- Review remaining unresolved vulnerabilities manually',
    '- Consider updating lock file and committing changes'
  );

  return lines.join('\n');
}

/**
 * Format the fix summary as an HTML section to inject before </body>.
 * @param {Object} fixSummary
 * @returns {string}
 */
function formatFixSectionHtml(fixSummary) {
  const fixMethodBadgeClass = (method) => {
    if (method === 'package.json update') return 'badge-fix-pkg';
    if (method === 'yarn upgrade') return 'badge-fix-yarn';
    if (method === 'parent upgrade') return 'badge-fix-parent';
    if (method === 'resolution') return 'badge-fix-resolution';
    return 'badge-transitive';
  };

  const fixedRows = (fixSummary.fixedModules || []).map(f =>
    `<tr class="fix-fixed-row"><td>${f.module}</td><td>${f.cveId}</td><td>${f.severity}</td><td>${f.dependency}</td><td><span class="badge ${fixMethodBadgeClass(f.fixMethod)}">${f.fixMethod}</span></td><td>${f.oldVersion}</td><td>${f.newVersion}</td></tr>`
  ).join('\n');

  const remainingRows = (fixSummary.remainingModules || []).map(r =>
    `<tr class="fix-remaining-row"><td>${r.module}</td><td>${r.cveId}</td><td>${r.severity}</td><td>${r.dependency}</td><td>${r.reason}</td></tr>`
  ).join('\n');

  return `
    <hr>
    <h2>🔧 Fix Report</h2>
    <div class="metadata">
        <p><strong>Fix Date:</strong> ${fixSummary.fixDate}</p>
        <p><strong>Original Vulnerabilities:</strong> ${fixSummary.totalOriginal}</p>
        <p><strong>Fixed:</strong> ${fixSummary.totalFixed}</p>
        <p><strong>Remaining:</strong> ${fixSummary.totalRemaining}</p>
    </div>
    <h3>Fixed Vulnerabilities</h3>
    <table>
        <thead><tr><th>Module</th><th>CVE(s)</th><th>Severity</th><th>Dependency Type</th><th>Fix Method</th><th>Old Version</th><th>New Version</th></tr></thead>
        <tbody>${fixedRows}</tbody>
    </table>
    <h3>Remaining Unresolved</h3>
    <table>
        <thead><tr><th>Module</th><th>CVE(s)</th><th>Severity</th><th>Dependency Type</th><th>Reason</th></tr></thead>
        <tbody>${remainingRows}</tbody>
    </table>`;
}

/**
 * Append a fix summary section to the existing report files in nexus-report/.
 * Modifies JSON, MD, and HTML reports in place.
 * @param {Object} fixSummary
 */
export function appendFixSummary(fixSummary) {
  const reportDir = join(process.cwd(), 'nexus-report');
  const jsonPath = join(reportDir, 'nexus-vulnerability-report.json');
  const mdPath = join(reportDir, 'nexus-vulnerability-report.md');
  const htmlPath = join(reportDir, 'nexus-vulnerability-report.html');

  // JSON — merge fixSummary key
  if (existsSync(jsonPath)) {
    try {
      const json = JSON.parse(readFileSync(jsonPath, 'utf8'));
      json.fixSummary = fixSummary;
      writeFileSync(jsonPath, JSON.stringify(json, null, 2), 'utf8');
    } catch (_) {
      // Non-fatal — report file may be corrupted; write a standalone fix summary instead
    }
  }

  // Markdown — append section
  if (existsSync(mdPath)) {
    const mdContent = readFileSync(mdPath, 'utf8');
    writeFileSync(mdPath, mdContent + formatFixSectionMarkdown(fixSummary), 'utf8');
  }

  // HTML — inject before </body>
  if (existsSync(htmlPath)) {
    const htmlContent = readFileSync(htmlPath, 'utf8');
    writeFileSync(htmlPath, htmlContent.replace('</body>', formatFixSectionHtml(fixSummary) + '\n</body>'), 'utf8');
  }
}
