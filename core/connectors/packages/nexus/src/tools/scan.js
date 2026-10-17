import { z } from 'zod';
import https from 'https';
import http from 'http';
import { urlToHttpOptions } from 'node:url';
import { HttpsProxyAgent } from 'https-proxy-agent';
import { detectProxyFor } from '@sc-node-mcp/core';
import fs from 'fs';
import path from 'path';
import { execSync, exec } from 'child_process';
import { buildJsonReport, writeNexusReport } from './generate-reports.js';
import { enrichFixVersions } from './enrich-fix-versions.js';

// ── HTTP helper ────────────────────────────────────────────────────────────────

async function makeRequest(options, postData = null) {
  const protocol = options.protocol || 'https:';
  const hostname = options.hostname.includes(':') ? `[${options.hostname}]` : options.hostname;
  const host = hostname + (options.port ? `:${options.port}` : '');
  const proxyUrl = await detectProxyFor(`${protocol}//${host}`);
  if (proxyUrl) {
    options.agent = new HttpsProxyAgent(proxyUrl);
  }

  return new Promise((resolve, reject) => {
    const transport = protocol === 'http:' ? http : https;
    const req = transport.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const parsed = data ? JSON.parse(data) : {};
          resolve({ statusCode: res.statusCode, data: parsed, headers: res.headers });
        } catch {
          resolve({ statusCode: res.statusCode, data: data, headers: res.headers });
        }
      });
    });
    req.on('error', reject);
    if (postData) {
      req.write(typeof postData === 'string' ? postData : JSON.stringify(postData));
    }
    req.end();
  });
}

// ── Nexus IQ API calls ─────────────────────────────────────────────────────────

function apiOptions(server, endpoint) {
  const base = new URL(server.includes('://') ? server : `https://${server}`);
  const prefix = base.pathname.replace(/\/+$/, '');
  const endpointPath = endpoint.startsWith(`${prefix}/`) ? endpoint : `${prefix}/${endpoint.replace(/^\/+/, '')}`;
  const target = new URL(URL.canParse(endpoint) ? endpoint : endpointPath, base);
  if (!['http:', 'https:'].includes(target.protocol) || target.origin !== base.origin) {
    throw new Error('Nexus API results must use the configured endpoint origin');
  }
  const { protocol, hostname, port, path } = urlToHttpOptions(target);
  return { protocol, hostname, port, path };
}

async function getInternalAppId(serverHost, authorization, publicId) {
  const options = {
    ...apiOptions(serverHost, `/api/v2/applications?publicId=${encodeURIComponent(publicId)}`),
    method: 'GET',
    headers: { Authorization: authorization, Accept: 'application/json' }
  };

  const response = await makeRequest(options);

  if (
    response.statusCode === 200 &&
    response.data.applications &&
    response.data.applications.length > 0
  ) {
    return response.data.applications[0].id;
  }

  throw new Error(`Application not found: ${publicId} (HTTP ${response.statusCode})`);
}

async function pollForResults(serverHost, authorization, resultsPath, maxAttempts = 30, delayMs = 2000) {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    const options = {
      ...apiOptions(serverHost, resultsPath),
      method: 'GET',
      headers: { Authorization: authorization, Accept: 'application/json' }
    };

    const response = await makeRequest(options);

    if (response.statusCode === 200 && response.data) {
      if (response.data.isError) {
        throw new Error(`Evaluation failed: ${response.data.errorMessage || 'Unknown error'}`);
      }
      if (response.data.results || response.data.components) {
        return response.data;
      }
    }

    if (attempt < maxAttempts) {
      await new Promise((resolve) => setTimeout(resolve, delayMs));
    }
  }

  throw new Error('Timeout waiting for Nexus IQ evaluation results');
}

async function evaluateComponents(serverHost, authorization, internalAppId, components) {
  const options = {
    ...apiOptions(serverHost, `/api/v2/evaluation/applications/${internalAppId}`),
    method: 'POST',
    headers: {
      Authorization: authorization,
      'Content-Type': 'application/json',
      Accept: 'application/json'
    }
  };

  const response = await makeRequest(options, JSON.stringify({ components }));

  if ([200, 201, 202].includes(response.statusCode)) {
    if (response.data.resultsUrl) {
      return await pollForResults(serverHost, authorization, response.data.resultsUrl);
    }
    return response.data;
  }

  throw new Error(`Evaluation failed with status ${response.statusCode}`);
}

// ── Dependency parsing (local package.json / node_modules / yarn.lock) ────────

function parseDependencies(projectPath, deepMode) {
  const packageJsonPath = path.join(projectPath, 'package.json');
  const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
  const prodDeps    = packageJson.dependencies    || {};
  const devDeps     = packageJson.devDependencies || {};
  const devDepNames = new Set(Object.keys(devDeps));

  const directDepsFromJson = deepMode ? { ...prodDeps, ...devDeps } : { ...prodDeps };
  const directDepNames     = new Set(Object.keys(directDepsFromJson));

  const nodeModulesPath = path.join(projectPath, 'node_modules');
  const allInstalled    = new Map(); // pkgName → version

  // ── Pipeline mode: prefer package-lock.json dev:true flags ────────────────
  let prodOnlyPackages = null;
  if (!deepMode) {
    const lockPath = path.join(projectPath, 'package-lock.json');
    if (fs.existsSync(lockPath)) {
      try {
        const lock = JSON.parse(fs.readFileSync(lockPath, 'utf8'));
        if (lock.lockfileVersion >= 2 && lock.packages) {
          prodOnlyPackages = new Map();
          for (const [pkgPath, pkgData] of Object.entries(lock.packages)) {
            if (!pkgPath) continue;
            if (pkgData.dev === true || pkgData.peer === true) continue;
            const segments = pkgPath.replace(/^node_modules\//, '').split('/node_modules/');
            const pkgName  = segments[segments.length - 1];
            const version  = pkgData.version || '0.0.0';
            if (pkgName && !prodOnlyPackages.has(pkgName)) {
              prodOnlyPackages.set(pkgName, version);
            }
          }
        }
      } catch {
        prodOnlyPackages = null;
      }
    }
  }

  if (prodOnlyPackages) {
    for (const [name, version] of prodOnlyPackages) {
      allInstalled.set(name, version);
    }
  } else if (!deepMode && fs.existsSync(nodeModulesPath)) {
    // Yarn project — BFS traversal of production deps only
    function collectProdPackages(startDeps, nmPath) {
      const result  = new Map();
      const queue   = Object.keys(startDeps);
      const visited = new Set();

      while (queue.length > 0) {
        const pkgName = queue.shift();
        if (visited.has(pkgName) || pkgName === 'npm') continue;
        visited.add(pkgName);

        const parts       = pkgName.startsWith('@') ? pkgName.split('/') : [pkgName];
        const pkgJsonPath = path.join(nmPath, ...parts, 'package.json');
        if (!fs.existsSync(pkgJsonPath)) continue;

        try {
          const pkg = JSON.parse(fs.readFileSync(pkgJsonPath, 'utf8'));
          if (pkg.version) result.set(pkgName, pkg.version);
          for (const depName of Object.keys(pkg.dependencies || {})) {
            if (!visited.has(depName)) queue.push(depName);
          }
        } catch { /* ignore malformed package.json */ }
      }

      return result;
    }

    const prodOnly = collectProdPackages(prodDeps, nodeModulesPath);
    for (const [name, version] of prodOnly) {
      allInstalled.set(name, version);
    }
  } else {
    // Deep mode or fallback: walk all node_modules
    if (fs.existsSync(nodeModulesPath)) {
      function scanNodeModules(dir) {
        let entries;
        try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return; }

        for (const entry of entries) {
          if (!entry.isDirectory() || entry.name.startsWith('.') || entry.name === '.bin') continue;

          if (entry.name.startsWith('@')) {
            const scopeDir = path.join(dir, entry.name);
            let scopeEntries;
            try { scopeEntries = fs.readdirSync(scopeDir, { withFileTypes: true }); } catch { continue; }
            for (const se of scopeEntries) {
              if (!se.isDirectory()) continue;
              const pkgName     = `${entry.name}/${se.name}`;
              const pkgJsonPath = path.join(scopeDir, se.name, 'package.json');
              if (fs.existsSync(pkgJsonPath) && !allInstalled.has(pkgName)) {
                try {
                  const pkg = JSON.parse(fs.readFileSync(pkgJsonPath, 'utf8'));
                  if (pkg.version) allInstalled.set(pkgName, pkg.version);
                } catch { /* skip unreadable/malformed package.json */ }
              }
            }
          } else {
            const pkgJsonPath = path.join(dir, entry.name, 'package.json');
            if (fs.existsSync(pkgJsonPath) && !allInstalled.has(entry.name)) {
              try {
                const pkg = JSON.parse(fs.readFileSync(pkgJsonPath, 'utf8'));
                if (pkg.version) allInstalled.set(entry.name, pkg.version);
              } catch { /* skip unreadable/malformed package.json */ }
            }
          }
        }
      }

      scanNodeModules(nodeModulesPath);
    } else {
      // No node_modules — fall back to direct deps from package.json
      for (const [name, spec] of Object.entries(directDepsFromJson)) {
        allInstalled.set(name, spec.replace(/^[\^~>=<*]/, '') || '0.0.0');
      }
    }
  }

  // ── Build Nexus components array ───────────────────────────────────────────
  const components = [];
  for (const [name, version] of allInstalled) {
    const cleanVersion = version.replace(/^[\^~>=<*]/, '') || '0.0.0';
    components.push({
      packageUrl: `pkg:npm/${name}@${cleanVersion}`,
      hash: null,
      componentIdentifier: {
        format: 'npm',
        coordinates: { packageId: name, version: cleanVersion }
      }
    });
  }

  return { components, directDepNames, devDepNames, totalInstalled: allInstalled.size };
}

// ── Vulnerability extraction (mirrors generate-reports.js pipeline filters) ──

const SONATYPE_RE  = /^sonatype-/i;
const FUTURE_CVE_RE = /^CVE-202[56]-/;

/**
 * Extract and normalize vulnerabilities from a raw Nexus IQ API response,
 * applying the same pipeline-aligned filters used in report generation.
 *
 * Filters applied (pipeline mode):
 *   F1 – production deps only (skip pure devDependencies)
 *   F3 – CVSS ≥ 4.0 (Medium and above)
 *   F5 – policy violations gate (skip components with empty policyViolations)
 *   F6 – exclude sonatype-* proprietary IDs (not covered by org policy rules)
 *
 * @param {Object} apiResults       Raw Nexus IQ evaluation response
 * @param {Set}    directDepNames   Names of direct deps (prod only in pipeline mode)
 * @param {Set}    devDepNames      Names of all devDependencies
 * @param {boolean} deepMode        If true, skip pipeline filters
 * @returns {Array} Normalized vulnerability objects
 */
function extractVulnerabilities(apiResults, directDepNames, devDepNames, deepMode) {
  const pipelineMode = !deepMode;

  let evaluatedComponents = [];
  if (apiResults.results)            evaluatedComponents = apiResults.results;
  else if (apiResults.components)    evaluatedComponents = apiResults.components;
  else if (Array.isArray(apiResults)) evaluatedComponents = apiResults;

  // In pipeline mode: packages that are ONLY in devDeps (not also in prod)
  const pureDevDeps = pipelineMode
    ? new Set([...devDepNames].filter(n => !directDepNames.has(n)))
    : new Set();

  const vulnerabilities = [];

  for (const result of evaluatedComponents) {
    const comp   = result.component || result;
    const compId = comp.componentIdentifier || {};
    // Support both npm (packageId) and Maven (groupId:artifactId) coordinate formats
    const pkgName = compId.coordinates?.packageId
      || (compId.coordinates?.groupId && compId.coordinates?.artifactId
        ? `${compId.coordinates.groupId}:${compId.coordinates.artifactId}`
        : null);
    const version = compId.coordinates?.version || '0.0.0';

    if (!pkgName || pkgName === 'npm') continue;

    // F5 – policy violations gate
    if (pipelineMode && result.policyData != null &&
        (result.policyData.policyViolations || []).length === 0) {
      continue;
    }

    // F1 – skip pure dev deps in pipeline mode
    if (pipelineMode && pureDevDeps.has(pkgName)) continue;

    if (!result.securityData?.securityIssues?.length) continue;

    const isDirect = directDepNames.has(pkgName);

    for (const issue of result.securityData.securityIssues) {
      const ref       = issue.reference || '';
      const cveMatch  = ref.match(/(CVE-\d{4}-\d+)/);
      const sonatypeMatch = ref.match(/(sonatype-\d{4}-\d+)/i);
      const vulnId = cveMatch ? cveMatch[1]
        : sonatypeMatch ? sonatypeMatch[1]
        : (ref || 'N/A');

      // F6 – exclude sonatype-* proprietary IDs
      if (pipelineMode && SONATYPE_RE.test(vulnId)) continue;

      const cvss = issue.severity || 0;

      // F3 – skip low/informational (CVSS < 4.0)
      if (pipelineMode && cvss > 0 && cvss < 4.0) continue;

      let severityText = 'Unknown';
      if (cvss >= 9.0)       severityText = 'Critical';
      else if (cvss >= 7.0)  severityText = 'High';
      else if (cvss >= 4.0)  severityText = 'Medium';
      else if (cvss > 0)     severityText = 'Low';

      if (issue.threatCategory) {
        const tc = issue.threatCategory.toLowerCase();
        if (tc === 'critical')  severityText = 'Critical';
        else if (tc === 'severe') severityText = 'High';
        else if (tc === 'moderate') severityText = 'Medium';
      }

      const cveLink = cveMatch
        ? `https://nvd.nist.gov/vuln/detail/${vulnId}`
        : sonatypeMatch
          ? `https://ossindex.sonatype.org/vulnerability/${vulnId}`
          : '';

      vulnerabilities.push({
        component:    pkgName,
        version,
        dependency:   isDirect ? 'direct' : 'transitive',
        vulnId,
        referenceUrl: cveLink,
        cvss,
        description:  issue.threatCategory || issue.title || '',
        severity:     severityText,
        fixVersion:   null   // will be enriched by enrichFixVersions in step 6b
      });
    }
  }

  return vulnerabilities;
}

// ── Browser opener ─────────────────────────────────────────────────────────────

function openInBrowser(htmlPath) {
  try {
    const cmd = process.platform === 'darwin' ? `open "${htmlPath}"`
      : process.platform === 'win32'           ? `start "" "${htmlPath}"`
      : `xdg-open "${htmlPath}"`;
    exec(cmd);
  } catch { /* non-fatal */ }
}

// ── Text summary builder ───────────────────────────────────────────────────────

function buildTextSummary(jsonReport, reportDir) {
  const { summary, vulnerableModules } = jsonReport;
  const sc = summary.severityCounts;
  const totalVulns = sc.Critical + sc.High + sc.Medium + sc.Low;

  const lines = [];
  lines.push('='.repeat(70));
  lines.push('NEXUS IQ VULNERABILITY SCAN RESULTS');
  lines.push('='.repeat(70));
  lines.push(`Application: ${summary.applicationId}`);
  lines.push(`Scan Date:   ${summary.scanDate}`);
  lines.push(`Mode:        ${summary.mode === 'deep' ? 'Deep (all deps incl. devDependencies)' : 'Pipeline-aligned (production deps only, sonatype-* excluded)'}`);
  lines.push('');
  lines.push('-'.repeat(70));
  lines.push('VULNERABILITY SUMMARY');
  lines.push('-'.repeat(70));
  lines.push(`Total Components Analyzed: ${summary.totalComponents}`);
  lines.push(`Vulnerable Components:     ${summary.vulnerableComponents}`);
  lines.push('');

  if (totalVulns > 0) {
    lines.push('Security Vulnerabilities by Severity:');
    if (sc.Critical > 0) lines.push(`  Critical : ${sc.Critical}`);
    if (sc.High     > 0) lines.push(`  High     : ${sc.High}`);
    if (sc.Medium   > 0) lines.push(`  Medium   : ${sc.Medium}`);
    if (sc.Low      > 0) lines.push(`  Low      : ${sc.Low}`);
    lines.push(`  Total    : ${totalVulns}`);
    lines.push('');
  } else {
    lines.push('No security vulnerabilities detected (after pipeline filters)!');
    lines.push('');
  }

  if (vulnerableModules.length > 0) {
    lines.push('-'.repeat(70));
    lines.push('VULNERABLE COMPONENTS');
    lines.push('-'.repeat(70));
    lines.push('');

    for (const [i, mod] of vulnerableModules.entries()) {
      lines.push(`${i + 1}. ${mod.module}@${mod.currentVersion}  [${mod.dependency}]`);
      for (const cve of mod.cves) {
        const badge = cve.isNewCve ? ' [New CVE]' : '';
        lines.push(`   [${cve.severity} ${cve.score}] ${cve.cveId}${badge}  fix: ${cve.fixVersion}`);
      }
      lines.push('');
    }
  }

  lines.push('='.repeat(70));
  lines.push('REPORTS GENERATED');
  lines.push('-'.repeat(70));
  lines.push(`  JSON : ${path.join(reportDir, 'nexus-vulnerability-report.json')}`);
  lines.push(`  MD   : ${path.join(reportDir, 'nexus-vulnerability-report.md')}`);
  lines.push(`  HTML : ${path.join(reportDir, 'nexus-vulnerability-report.html')}  (opened in browser)`);
  lines.push('='.repeat(70));

  return lines.join('\n');
}

// ── Maven dependency parsing ──────────────────────────────────────────────────

/**
 * Parse a Maven/Java project using `mvn dependency:tree`.
 *
 * Pipeline mode: include compile + runtime scopes only.
 * Deep mode:     include all scopes.
 *
 * Components are sent to Nexus IQ using `componentIdentifier` ONLY (no packageUrl).
 * Sending packageUrl alongside componentIdentifier causes a 400 error because the
 * API then expects a `type` coordinate which Maven pURLs don't carry.
 *
 * @param {string}  projectPath  Absolute path to the Maven project root (contains pom.xml)
 * @param {boolean} deepMode     true = all scopes; false = compile + runtime only
 * @returns {{ components, directDepNames, devDepNames, totalInstalled }}
 */
function parseMavenDependencies(projectPath, deepMode) {
  const scanDir  = path.join(projectPath, 'nexus-report', '.nexus-scan');
  if (!fs.existsSync(scanDir)) fs.mkdirSync(scanDir, { recursive: true });
  const treeFile = path.join(scanDir, 'dep-tree.txt');

  // Step 1: mvn dependency:resolve (non-fatal, 2-minute timeout)
  // Fails harmlessly on SC corporate networks where Maven Central is blocked;
  // the subsequent tree step uses the local Maven cache instead.
  try {
    execSync('mvn dependency:resolve', { cwd: projectPath, stdio: 'pipe', timeout: 120000 });
  } catch {
    console.error('[nexus] mvn dependency:resolve failed — continuing with local Maven cache');
  }

  // Step 2: mvn dependency:tree
  try {
    execSync(
      `mvn dependency:tree -DoutputFile="${treeFile}" -DoutputType=text -DappendOutput=false`,
      { cwd: projectPath, stdio: 'pipe', encoding: 'utf8' }
    );
  } catch (e) {
    throw new Error(
      `mvn dependency:tree failed: ${e.message?.split('\n')[0]}\n` +
      'Ensure Maven 3.x is installed and the project compiles cleanly.'
    );
  }

  if (!fs.existsSync(treeFile)) {
    throw new Error('mvn dependency:tree produced no output file. Check Maven project setup.');
  }

  const treeLines      = fs.readFileSync(treeFile, 'utf8').split('\n');
  const coordRe        = /([\w.-]+):([\w.-]+):[^:]+:([\d][\w.-]*):(\w+)/;
  const pipelineScopes = new Set(['compile', 'runtime']);

  const components     = [];
  const directDepNames = new Set();
  const seen           = new Set();

  for (const rawLine of treeLines) {
    const line = rawLine.replace(/^\[INFO\]\s?/, '');
    if (!line.trim()) continue;

    const m = line.match(coordRe);
    if (!m) continue;

    const [, groupId, artifactId, version, scope] = m;

    // Pipeline scope filter (F1 for Maven)
    if (!deepMode && !pipelineScopes.has(scope)) continue;

    const key = `${groupId}:${artifactId}:${version}`;
    if (seen.has(key)) continue;
    seen.add(key);

    // Depth-1 detection: direct dep has "+- " or "\- " with no leading "|  " groups
    const prefixMatch = line.match(/^(\| {2}| {3})*(\+- |\\- )/);
    const depth = prefixMatch ? Math.round((prefixMatch[0].length - 3) / 3) : 0;
    if (depth <= 1) directDepNames.add(`${groupId}:${artifactId}`);

    // Send componentIdentifier ONLY — no packageUrl for Maven (Nexus IQ API requirement)
    components.push({
      componentIdentifier: {
        format: 'maven',
        coordinates: { groupId, artifactId, version, extension: 'jar' }
      }
    });
  }

  if (components.length === 0) {
    throw new Error(
      'No Maven dependencies found after parsing dep-tree output.\n' +
      'Verify the project has <dependencies> in pom.xml and compiles successfully.'
    );
  }

  return {
    components,
    directDepNames,
    devDepNames:    new Set(), // Maven has no devDependencies concept
    totalInstalled: components.length
  };
}

// ── Named exports for testing ─────────────────────────────────────────────────
export { makeRequest, getInternalAppId, pollForResults, evaluateComponents, parseDependencies, parseMavenDependencies, extractVulnerabilities, openInBrowser, buildTextSummary };

// ── MCP tool registration ──────────────────────────────────────────────────────

export function configureScanTools(server, nexusConnectionProvider) {
  server.tool(
    'nexus_scan_vulnerabilities',
    [
      'Scan local npm/Node.js or Maven/Java dependencies for security vulnerabilities using Nexus IQ.',
      'Auto-detects project type from the project directory — reads package.json (npm) or pom.xml (Maven).',
      'Generates reports in JSON, Markdown, and HTML formats and opens the HTML in the browser.',
      '',
      'Choose the scan mode based on the user prompt keyword:',
      '  • Prompt says "Scan" (no "Deep")    → pipeline-aligned mode (default):',
      '    npm: production dependencies only; Maven: compile + runtime scopes only.',
      '    sonatype-* proprietary IDs excluded, CVSS < 4.0 excluded — matches what the ADO pipeline flags.',
      '    Set deepMode=false (or omit).',
      '  • Prompt says "Deep Scan", "full scan", "exhaustive scan", or "include dev dependencies"',
      '    → exhaustive mode: npm ALL deps including devDependencies; Maven: ALL scopes.',
      '    Every CVE and sonatype-* finding reported with NO filtering. Set deepMode=true.',
      '',
      'Fix patterns (the fix step is handled by nexus_fix_vulnerabilities after this tool returns):',
      '  • "Scan and fix"       → run pipeline-aligned scan, then call nexus_fix_vulnerabilities.',
      '  • "Deep Scan and fix" → run exhaustive scan, then call nexus_fix_vulnerabilities.',
    ].join('\n'),
    {
      applicationId: z.string().describe(
        'Nexus IQ application public ID (e.g., ITAM__PROD__my-service). The ADO repo name is always the last __-delimited segment.'
      ),
      projectPath: z.string().optional().describe(
        'Absolute path to the project directory containing package.json or pom.xml (defaults to current working directory).'
      ),
      projectType: z.enum(['npm', 'maven']).optional().describe(
        'Project ecosystem: "npm" for Node.js/package.json, "maven" for Java/pom.xml. '
        + 'Auto-detected when omitted. Required when both package.json and pom.xml are present.'
      ),
      deepMode: z.boolean().optional().describe(
        'Set to true when the user says "Deep Scan", "full scan", "exhaustive scan", or "include dev dependencies". '
        + 'Deep mode scans ALL deps including devDependencies (npm) or all Maven scopes and reports every finding with no filtering. '
        + 'Omit or set false for a normal pipeline-aligned scan (production deps only, sonatype-* and CVSS < 4.0 excluded).'
      )
    },
    async ({ applicationId, projectPath, projectType, deepMode = false }) => {
      try {
        const resolvedPath = projectPath || process.cwd();

        // ── Step 1: detect / validate project type ───────────────────────────
        const hasPkgJson = fs.existsSync(path.join(resolvedPath, 'package.json'));
        const hasPomXml  = fs.existsSync(path.join(resolvedPath, 'pom.xml'));

        let detectedType = projectType;
        if (!detectedType) {
          if (hasPkgJson && !hasPomXml)       detectedType = 'npm';
          else if (hasPomXml && !hasPkgJson)  detectedType = 'maven';
          else if (hasPkgJson && hasPomXml) {
            return {
              content: [{
                type: 'text',
                text:
                  'Both package.json and pom.xml found in: ' + resolvedPath + '\n' +
                  'Please specify which ecosystem to scan by setting projectType to "npm" or "maven".'
              }]
            };
          } else {
            throw new Error(`No package.json or pom.xml found in: ${resolvedPath}`);
          }
        } else {
          if (detectedType === 'npm' && !hasPkgJson) {
            throw new Error(`package.json not found in: ${resolvedPath}`);
          }
          if (detectedType === 'maven' && !hasPomXml) {
            throw new Error(`pom.xml not found in: ${resolvedPath}`);
          }
        }

        // ── Step 2: install / resolve dependencies ───────────────────────────
        if (detectedType === 'npm') {
          const hasYarnLock = fs.existsSync(path.join(resolvedPath, 'yarn.lock'));
          const hasPkgLock  = fs.existsSync(path.join(resolvedPath, 'package-lock.json'));
          const installCmd  = hasYarnLock ? 'yarn install --frozen-lockfile'
            : hasPkgLock ? 'npm ci'
            : 'npm install';
          try {
            execSync(installCmd, { cwd: resolvedPath, stdio: 'pipe' });
          } catch (e) {
            console.error(`[nexus] Install step warning: ${e.message?.split('\n')[0]}`);
          }
        }
        // Maven: dependency:resolve is run inside parseMavenDependencies (non-fatal, 2-min timeout)

        // ── Step 3: get internal application ID ─────────────────────────────
        const connection   = nexusConnectionProvider();
        const { baseUrl, headers } = connection;
        const authorization = headers.Authorization;

        const internalAppId = await getInternalAppId(baseUrl, authorization, applicationId);

        // ── Step 4: parse local dependencies ────────────────────────────────
        const { components, directDepNames, devDepNames, totalInstalled } =
          detectedType === 'maven'
            ? parseMavenDependencies(resolvedPath, deepMode)
            : parseDependencies(resolvedPath, deepMode);

        if (components.length === 0) {
          return {
            content: [{
              type: 'text',
              text: `No components found in ${resolvedPath}. Ensure ${detectedType === 'maven' ? 'pom.xml has <dependencies> and the project compiles' : 'package.json exists and dependencies are installed'}.`
            }]
          };
        }

        // ── Step 5: evaluate via Nexus IQ API ───────────────────────────────
        const apiResults = await evaluateComponents(baseUrl, authorization, internalAppId, components);

        // ── Step 6: extract vulnerabilities with pipeline filters ────────────
        const scanMode = deepMode ? 'deep' : 'pipeline';
        const rawVulnerabilities = extractVulnerabilities(apiResults, directDepNames, devDepNames, deepMode);

        // ── Step 6b: enrich with fix versions from Nexus IQ Remediation API ──
        const vulnerabilities = rawVulnerabilities.length > 0
          ? await enrichFixVersions(baseUrl, headers, internalAppId, rawVulnerabilities, 'build')
          : rawVulnerabilities;

        // ── Step 7: build & write 3-format reports ───────────────────────────
        const repoName = applicationId.split('__').pop() || applicationId;
        const jsonReport = buildJsonReport({
          applicationId,
          branch:                 'local',
          repoName,
          totalComponentsScanned: totalInstalled,
          vulnerabilities,
          scanMode:               'fresh',
          mode:                   scanMode,
          projectType:            detectedType
        });

        const reportDir = writeNexusReport(jsonReport);

        // ── Step 8: open HTML in browser (non-blocking, non-fatal) ───────────
        openInBrowser(path.join(reportDir, 'nexus-vulnerability-report.html'));

        // ── Step 9: return text summary ──────────────────────────────────────
        const textSummary = buildTextSummary(jsonReport, reportDir);
        return { content: [{ type: 'text', text: textSummary }] };
      } catch (error) {
        return {
          content: [{ type: 'text', text: error?.message || String(error) }],
          isError: true
        };
      }
    }
  );
}
