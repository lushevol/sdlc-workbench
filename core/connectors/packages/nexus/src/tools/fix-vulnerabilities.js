import { z } from 'zod';
import { readFileSync, writeFileSync, existsSync, mkdirSync, copyFileSync } from 'fs';
import { join } from 'path';
import { appendFixSummary } from './generate-reports.js';

// ── Package manager detection ─────────────────────────────────────────────────

/**
 * Detect the package manager in use for a project root.
 * @param {string} projectRoot
 * @returns {'yarn'|'npm'}
 */
function detectPackageManager(projectRoot) {
  return existsSync(join(projectRoot, 'yarn.lock')) ? 'yarn' : 'npm';
}

// ── Package.json manipulation ─────────────────────────────────────────────────

/**
 * Read, parse, and return package.json from a directory. Throws on failure.
 */
function readPackageJson(projectRoot) {
  return JSON.parse(readFileSync(join(projectRoot, 'package.json'), 'utf8'));
}

/**
 * Write a modified package.json back to disk.
 */
function writePackageJson(projectRoot, pkg) {
  writeFileSync(join(projectRoot, 'package.json'), JSON.stringify(pkg, null, 2) + '\n', 'utf8');
}

// ── Shell helpers ────────────────────────────────────────────────────────────

import { execSync } from 'child_process';

// ── Maven pom.xml helpers ─────────────────────────────────────────────────────

/**
 * Update the <version> of a dependency in pom.xml.
 * Finds the <dependency> block matching groupId:artifactId and replaces its
 * <version> tag. Returns true if changed, false if not found (e.g. uses a
 * ${property} version — those need manual update).
 */
function updatePomVersion(pomPath, groupId, artifactId, newVersion) {
  let pomText = readFileSync(pomPath, 'utf8');
  const depBlockRe = /(<dependency>[\s\S]*?<\/dependency>)/g;
  let changed = false;
  pomText = pomText.replace(depBlockRe, block => {
    if (
      block.includes(`<groupId>${groupId}</groupId>`) &&
      block.includes(`<artifactId>${artifactId}</artifactId>`)
    ) {
      const updated = block.replace(/<version>[^<]*<\/version>/, `<version>${newVersion}</version>`);
      if (updated !== block) { changed = true; return updated; }
    }
    return block;
  });
  if (changed) writeFileSync(pomPath, pomText, 'utf8');
  return changed;
}

/**
 * Add or update a <dependencyManagement> entry in pom.xml to force a specific
 * version of a transitive dependency.
 * @param {string} pomPath
 * @param {string} groupArtifact  "groupId:artifactId"
 * @param {string} fixVersion
 * @returns {boolean}
 */
function addPomDependencyManagement(pomPath, groupArtifact, fixVersion) {
  const [groupId, artifactId] = groupArtifact.split(':');
  if (!groupId || !artifactId) return false;

  let pomText = readFileSync(pomPath, 'utf8');
  const depBlock = `
      <dependency>
        <groupId>${groupId}</groupId>
        <artifactId>${artifactId}</artifactId>
        <version>${fixVersion}</version>
      </dependency>`;

  if (pomText.includes('<dependencyManagement>')) {
    // Append into existing <dependencyManagement><dependencies>
    pomText = pomText.replace(
      /(<dependencyManagement>[\s\S]*?<dependencies>)([\s\S]*?)(<\/dependencies>[\s\S]*?<\/dependencyManagement>)/,
      (_, open, body, close) => `${open}${body}${depBlock}\n    ${close}`
    );
  } else {
    // Inject a new <dependencyManagement> block before </project>
    const dmSection = `\n  <dependencyManagement>\n    <dependencies>${depBlock}\n    </dependencies>\n  </dependencyManagement>\n`;
    pomText = pomText.replace('</project>', `${dmSection}</project>`);
  }

  writeFileSync(pomPath, pomText, 'utf8');
  return true;
}

/**
 * Find which direct dependency (listed in pom.xml) pulls in a given transitive
 * artifact, by re-running `mvn dependency:tree` and tracing the parent chain.
 * Returns "groupId:artifactId" of the direct parent, or null if not found.
 */
function findMavenParentDep(transitiveGroupArtifact, projectRoot) {
  const [tGroupId, tArtifactId] = transitiveGroupArtifact.split(':');
  if (!tGroupId || !tArtifactId) return null;

  try {
    const treeOutput = execSync('mvn dependency:tree -DoutputType=text', {
      cwd: projectRoot, stdio: 'pipe', encoding: 'utf8', timeout: 60000
    });

    const lines = treeOutput.split('\n');
    const coordRe = /([\w.-]+):([\w.-]+):[^:]+:([\d][\w.-]*):(\w+)/;

    let lastDirect = null;

    for (const rawLine of lines) {
      const line = rawLine.replace(/^\[INFO\]\s?/, '');
      const m = line.match(coordRe);
      if (!m) continue;
      const [, groupId, artifactId] = m;

      const prefixMatch = line.match(/^(\| {2}| {3})*(\+- |\\- )/);
      const depth = prefixMatch ? Math.round((prefixMatch[0].length - 3) / 3) : 0;

      if (depth <= 1) {
        lastDirect = `${groupId}:${artifactId}`;
      } else if (groupId === tGroupId && artifactId === tArtifactId) {
        return lastDirect;
      }
    }
  } catch { /* non-fatal */ }
  return null;
}

// ── Maven direct-dep fix (Phase A) ───────────────────────────────────────────

function fixMavenDirectDependencies(directVulns, projectRoot) {
  const pomPath = join(projectRoot, 'pom.xml');
  const fixed = [];
  const updates = new Map();

  for (const v of directVulns) {
    if (!v.fixVersion || v.fixVersion === 'Check CVE' || updates.has(v.module)) continue;
    const [groupId, artifactId] = v.module.split(':');
    if (!groupId || !artifactId) continue;
    updates.set(v.module, { groupId, artifactId, fixVersion: v.fixVersion, vuln: v });
  }

  if (updates.size === 0) return [];

  for (const [key, { groupId, artifactId, fixVersion, vuln }] of updates) {
    const updated = updatePomVersion(pomPath, groupId, artifactId, fixVersion);
    if (updated) {
      fixed.push({
        module: key,
        cveId: vuln.cveId,
        severity: vuln.severity,
        dependency: 'direct',
        fixMethod: 'pom.xml update',
        oldVersion: vuln.currentVersion,
        newVersion: fixVersion
      });
    }
  }

  if (fixed.length > 0) {
    tryRunCmd('mvn dependency:resolve -q', projectRoot);
  }
  return fixed;
}

// ── Maven dependencyManagement (Phase B3) ────────────────────────────────────

function applyMavenDependencyManagement(remainingVulns, projectRoot) {
  const pomPath = join(projectRoot, 'pom.xml');
  const fixed = [];

  for (const v of remainingVulns) {
    if (!v.fixVersion || v.fixVersion === 'Check CVE') continue;
    const added = addPomDependencyManagement(pomPath, v.module, v.fixVersion);
    if (added) {
      fixed.push({
        module: v.module,
        cveId: v.cveId,
        severity: v.severity,
        dependency: 'transitive',
        fixMethod: 'dependencyManagement',
        oldVersion: v.currentVersion,
        newVersion: v.fixVersion
      });
    }
  }

  if (fixed.length > 0) {
    tryRunCmd('mvn dependency:resolve -q', projectRoot);
  }
  return fixed;
}

// ── Semver helpers ────────────────────────────────────────────────────────────

/**
 * Simple semver ≥ comparison (a >= b). Handles x.y.z format.
 */
function semverGte(a, b) {
  const parse = v => (v || '').replace(/^[^0-9]*/, '').split('.').map(n => parseInt(n) || 0);
  const pa = parse(a);
  const pb = parse(b);
  for (let i = 0; i < Math.max(pa.length, pb.length); i++) {
    const diff = (pa[i] || 0) - (pb[i] || 0);
    if (diff > 0) return true;
    if (diff < 0) return false;
  }
  return true;
}

/**
 * Read the installed version of a package from node_modules.
 * @param {string} pkgName
 * @param {string} projectRoot
 * @returns {string|null}
 */
function getInstalledVersion(pkgName, projectRoot) {
  const pkgPath = join(projectRoot, 'node_modules', pkgName, 'package.json');
  if (!existsSync(pkgPath)) return null;
  try {
    return JSON.parse(readFileSync(pkgPath, 'utf8')).version || null;
  } catch { return null; }
}

/**
 * Get the latest published version of an npm package via `npm view`.
 * @param {string} pkgName
 * @param {string} projectRoot
 * @returns {string|null}
 */
function getLatestNpmVersion(pkgName, projectRoot) {
  const { stdout, success } = tryRunCmd(`npm view ${pkgName} version`, projectRoot);
  return success ? stdout.trim() : null;
}

/**
 * Backup package.json to nexus-report/package.json.backup.
 * @param {string} projectRoot
 */
function backupPackageJson(projectRoot) {
  try {
    const src = join(projectRoot, 'package.json');
    const dest = join(projectRoot, 'nexus-report', 'package.json.backup');
    mkdirSync(join(projectRoot, 'nexus-report'), { recursive: true });
    copyFileSync(src, dest);
  } catch { /* non-fatal */ }
}

/**
 * Open the HTML report in the default browser (non-fatal).
 * @param {string} htmlPath
 */
async function openInBrowser(htmlPath) {
  try {
    const { exec } = await import('child_process');
    const cmd = process.platform === 'darwin'
      ? `open "${htmlPath}"`
      : process.platform === 'win32'
        ? `start "" "${htmlPath}"`
        : `xdg-open "${htmlPath}"`;
    exec(cmd);
  } catch { /* non-fatal */ }
}

/**
 * Run a shell command synchronously; returns stdout string. Throws on failure.
 * @param {string} cmd
 * @param {string} cwd
 * @returns {string}
 */
function runCmd(cmd, cwd) {
  return execSync(cmd, { cwd, stdio: ['pipe', 'pipe', 'pipe'], timeout: 180000, encoding: 'utf8' });
}

/**
 * Run a shell command; returns { stdout, success, error }.
 */
function tryRunCmd(cmd, cwd) {
  try {
    const stdout = runCmd(cmd, cwd);
    return { stdout, success: true, error: null };
  } catch (err) {
    return { stdout: err.stdout || '', success: false, error: err.message || String(err) };
  }
}

// ── Direct dependency fixes (Phase A) ────────────────────────────────────────

/**
 * Fix direct dependency vulnerabilities by updating versions in package.json.
 * @param {Array} directVulns - vulnerabilities where dependency === 'direct' and fixVersion exists
 * @param {string} projectRoot
 * @param {'yarn'|'npm'} pm
 * @returns {Array} fixed module records
 */
function fixDirectDependencies(directVulns, projectRoot, pm) {
  const pkg = readPackageJson(projectRoot);
  const fixed = [];
  const updates = new Map();

  for (const v of directVulns) {
    if (!v.fixVersion || updates.has(v.module)) continue;
    const depType = (pkg.dependencies || {})[v.module] ? 'dependencies'
      : (pkg.devDependencies || {})[v.module] ? 'devDependencies'
      : null;
    if (!depType) continue;

    const oldVersion = pkg[depType][v.module];
    const newVersion = `^${v.fixVersion}`;
    pkg[depType][v.module] = newVersion;
    updates.set(v.module, { oldVersion, fixVersion: v.fixVersion, depType });
  }

  if (updates.size === 0) return [];
  writePackageJson(projectRoot, pkg);

  const installCmd = pm === 'yarn' ? 'yarn install' : 'npm install';
  tryRunCmd(installCmd, projectRoot);

  for (const v of directVulns) {
    if (!updates.has(v.module)) continue;
    const { oldVersion, fixVersion } = updates.get(v.module);
    if (fixed.some(f => f.module === v.module && f.cveId === v.cveId)) continue;
    fixed.push({
      module: v.module,
      cveId: v.cveId,
      severity: v.severity,
      dependency: 'direct',
      fixMethod: 'package.json update',
      oldVersion,
      newVersion: fixVersion
    });
  }

  return fixed;
}

// ── Yarn upgrade (Phase B1) ───────────────────────────────────────────────────

/**
 * Run yarn upgrade to resolve transitive vulnerabilities via ^ range.
 * Handles the "Outdated lockfile" error by running yarn install first and retrying.
 * @param {string} projectRoot
 * @returns {{ fixed: string[], log: string }}
 */
function runYarnUpgrade(projectRoot) {
  let result = tryRunCmd('yarn upgrade', projectRoot);

  if (!result.success && result.error && result.error.includes('Outdated lockfile')) {
    tryRunCmd('yarn install', projectRoot);
    result = tryRunCmd('yarn upgrade', projectRoot);
  }

  return { success: result.success, log: result.success ? result.stdout : result.error };
}

// ── Parent dependency analysis (Phase B2) ────────────────────────────────────

/**
 * Identify the direct parent dependency of each transitive package using
 * 'yarn why' (yarn) or 'npm ls' (npm).
 * @param {string} pkgName
 * @param {string} projectRoot
 * @param {'yarn'|'npm'} pm
 * @returns {string|null} parent direct dep name, or null if not found
 */
function findParentDep(pkgName, projectRoot, pm) {
  const cmd = pm === 'yarn' ? `yarn why ${pkgName}` : `npm ls ${pkgName}`;
  const { stdout, success } = tryRunCmd(cmd, projectRoot);
  if (!success) return null;

  // yarn why output: "This module exists because X depends on it."
  // npm ls output: tree with dep chain
  // Try to extract first mentioned direct parent from the cwd package.json deps
  try {
    const pkg = readPackageJson(projectRoot);
    const directDeps = new Set([
      ...Object.keys(pkg.dependencies || {}),
      ...Object.keys(pkg.devDependencies || {})
    ]);

    // Search for the first direct dep name mentioned in the output
    for (const dep of directDeps) {
      if (stdout.includes(dep) && dep !== pkgName) return dep;
    }
  } catch (_) { /* ignore */ }

  return null;
}

// ── Resolutions / overrides (Phase B3) ───────────────────────────────────────

/**
 * Add yarn resolutions (or npm overrides) to package.json for remaining transitive vulns.
 * @param {Array} remainingVulns
 * @param {string} projectRoot
 * @param {'yarn'|'npm'} pm
 * @returns {Array} fixed records
 */
function applyResolutions(remainingVulns, projectRoot, pm) {
  const pkg = readPackageJson(projectRoot);
  const fixed = [];
  const proposed = new Map();

  for (const v of remainingVulns) {
    if (!v.fixVersion || proposed.has(v.module)) continue;
    proposed.set(v.module, { fixVersion: v.fixVersion, vuln: v });
  }

  if (proposed.size === 0) return [];

  if (pm === 'yarn') {
    pkg.resolutions = pkg.resolutions || {};
    for (const [name, { fixVersion }] of proposed) {
      pkg.resolutions[name] = fixVersion;
    }
  } else {
    pkg.overrides = pkg.overrides || {};
    for (const [name, { fixVersion }] of proposed) {
      pkg.overrides[name] = fixVersion;
    }
  }

  writePackageJson(projectRoot, pkg);
  const installCmd = pm === 'yarn' ? 'yarn install' : 'npm install';
  tryRunCmd(installCmd, projectRoot);

  for (const [name, { vuln }] of proposed) {
    fixed.push({
      module: name,
      cveId: vuln.cveId,
      severity: vuln.severity,
      dependency: 'transitive',
      fixMethod: 'resolution',
      oldVersion: vuln.currentVersion,
      newVersion: vuln.fixVersion
    });
  }

  return fixed;
}

// ── Tool registration ────────────────────────────────────────────────────────

// ── Named exports for testing ─────────────────────────────────────────────────
export { semverGte, getInstalledVersion, getLatestNpmVersion, backupPackageJson, tryRunCmd, openInBrowser, updatePomVersion, addPomDependencyManagement, findMavenParentDep };

/**
 * Register the nexus_fix_vulnerabilities tool on the MCP server.
 * @param {Object} server - MCP server instance
 */
export function configureFixTools(server) {
  server.tool(
    'nexus_fix_vulnerabilities',
    [
      'Automatically remediate vulnerabilities found by nexus_scan_vulnerabilities.',
      'Reads the existing nexus-report/nexus-vulnerability-report.json from the current working directory.',
      'Supports both npm/Node.js and Maven/Java projects — project type is read from the scan report.',
      'npm fix workflow:',
      '  Phase A — Direct dependencies: bumps versions in package.json and runs install.',
      '  Phase B1 — Yarn upgrade: runs "yarn upgrade" (or npm install) to resolve transitive deps via ^ range.',
      '  Phase B2 — Parent upgrade: identifies and optionally upgrades parent direct deps. Requires approveParentUpgrades=true.',
      '  Phase B3 — Resolutions/overrides: force-pins remaining transitive deps. Requires approveResolutions=true.',
      'Maven fix workflow:',
      '  Phase A — Direct dependencies: updates <version> tags in pom.xml.',
      '  Phase B1 — Skipped (no range-upgrade equivalent for Maven).',
      '  Phase B2 — Parent upgrade: runs mvn versions:use-latest-releases for identified parent deps. Requires approveParentUpgrades=true.',
      '  Phase B3 — dependencyManagement: adds <dependencyManagement> entries to force transitive versions. Requires approveResolutions=true.',
      '  Phase C — Appends a fix summary section to the existing scan reports.',
      'Run without approval flags first to see what would be proposed, then re-call with approvals to apply.'
    ].join(' '),
    {
      applicationId: z.string().describe(
        'Nexus IQ public application ID that was previously scanned (used for display only).'
      ),
      approveParentUpgrades: z.boolean().optional().default(false).describe(
        'Set true to approve and apply Phase B2 — npm: upgrading parent direct dependencies; Maven: running mvn versions:use-latest-releases.'
      ),
      approveResolutions: z.boolean().optional().default(false).describe(
        'Set true to approve and apply Phase B3 — npm: adding resolutions/overrides in package.json; Maven: adding <dependencyManagement> entries in pom.xml.'
      )
    },
    async ({ applicationId, approveParentUpgrades, approveResolutions }) => {
      try {
        const projectRoot = process.cwd();
        const reportPath = join(projectRoot, 'nexus-report', 'nexus-vulnerability-report.json');

        if (!existsSync(reportPath)) {
          return {
            content: [{ type: 'text', text: `No scan report found at ${reportPath}. Run nexus_scan_vulnerabilities first.` }],
            isError: true
          };
        }

        let report;
        try {
          report = JSON.parse(readFileSync(reportPath, 'utf8'));
        } catch (err) {
          return {
            content: [{ type: 'text', text: `Failed to read scan report: ${err.message}` }],
            isError: true
          };
        }

        const allVulnerabilities = report.allVulnerabilities || [];
        if (allVulnerabilities.length === 0) {
          return {
            content: [{ type: 'text', text: '✅ No vulnerabilities to fix — scan report is clean.' }]
          };
        }

        // ── Detect project type from report or CWD ───────────────────────────
        const reportedType = report.summary?.projectType || null;
        const isMaven = reportedType === 'maven'
          || (!reportedType && existsSync(join(projectRoot, 'pom.xml')) && !existsSync(join(projectRoot, 'package.json')));

        const pm = isMaven ? null : detectPackageManager(projectRoot);
        const fixedModules = [];
        const remainingModules = [];
        const lines = [
          `🔧 Starting vulnerability fix workflow for ${applicationId}`,
          `Project type: ${isMaven ? '☕ Maven (Java)' : `📦 npm (${pm})`}`,
          ``
        ];

        // Back up the project file before any modifications
        if (isMaven) {
          try {
            const pomSrc = join(projectRoot, 'pom.xml');
            const pomDest = join(projectRoot, 'nexus-report', 'pom.xml.backup');
            mkdirSync(join(projectRoot, 'nexus-report'), { recursive: true });
            copyFileSync(pomSrc, pomDest);
          } catch { /* non-fatal */ }
        } else {
          backupPackageJson(projectRoot);
        }

        // ── Phase A: Fix direct dependencies ─────────────────────────────────
        const directFixable = allVulnerabilities.filter(
          v => v.dependency === 'direct' && v.fixVersion && v.canAutoFix
        );

        if (isMaven) {
          // Maven Phase A: update <version> tags in pom.xml
          if (directFixable.length > 0) {
            lines.push(`📦 Phase A — Fixing ${directFixable.length} direct dependency/ies in pom.xml...`);
            try {
              const fixed = fixMavenDirectDependencies(directFixable, projectRoot);
              fixedModules.push(...fixed);
              lines.push(`  ✅ Fixed ${fixed.length} direct dependency/ies via pom.xml update`);
              for (const f of fixed) {
                lines.push(`     ${f.module}: ${f.oldVersion} → ${f.newVersion} (${f.cveId})`);
              }
              const unfixed = directFixable.filter(v => !fixed.some(f => f.module === v.module));
              for (const v of unfixed) {
                lines.push(`  ⚠️  ${v.module}: version tag not found directly in pom.xml (may use a \${property} — update manually)`);
              }
            } catch (err) {
              lines.push(`  ⚠️  Phase A partially failed: ${err.message}`);
            }
          } else {
            lines.push(`📦 Phase A — No fixable direct dependencies found.`);
          }
        } else {
          if (directFixable.length > 0) {
            lines.push(`📦 Phase A — Fixing ${directFixable.length} direct dependency vulnerability/ies...`);
            try {
              const fixed = fixDirectDependencies(directFixable, projectRoot, pm);
              fixedModules.push(...fixed);
              lines.push(`  ✅ Fixed ${fixed.length} direct dependency/ies via package.json update`);
              for (const f of fixed) {
                lines.push(`     ${f.module}: ${f.oldVersion} → ${f.newVersion} (${f.cveId})`);
              }
            } catch (err) {
              lines.push(`  ⚠️  Phase A partially failed: ${err.message}`);
            }
          } else {
            lines.push(`📦 Phase A — No fixable direct dependencies found.`);
          }
        }
        lines.push('');

        // Determine remaining transitive vulnerabilities
        const fixedModuleNames = new Set(fixedModules.map(f => f.module));
        const transitiveVulns = allVulnerabilities.filter(
          v => v.dependency === 'transitive' && v.fixVersion
        );

        // ── Phase B1 ──────────────────────────────────────────────────────────
        const b1FixedNames = new Set();
        if (isMaven) {
          // Maven: no range-upgrade equivalent
          lines.push(`⏭️  Phase B1 — Skipped (Maven manages versions explicitly; no range-upgrade equivalent).`);
        } else if (transitiveVulns.length > 0) {
          if (pm === 'yarn') {
            lines.push(`🔄 Phase B1 — Running yarn upgrade for transitive vulnerabilities...`);

            // Capture pre-upgrade installed versions to compare after
            const preUpgradeVersions = new Map();
            for (const v of transitiveVulns) {
              const ver = getInstalledVersion(v.module, projectRoot);
              if (ver) preUpgradeVersions.set(v.module, ver);
            }

            const { success, log } = runYarnUpgrade(projectRoot);
            if (success) {
              lines.push(`  ✅ yarn upgrade completed.`);

              // Detect which transitive vulns were resolved by checking installed versions
              for (const v of transitiveVulns) {
                if (!v.fixVersion) continue;
                const installedVer = getInstalledVersion(v.module, projectRoot);
                if (installedVer && semverGte(installedVer, v.fixVersion)) {
                  b1FixedNames.add(v.module);
                  fixedModuleNames.add(v.module);
                  if (!fixedModules.some(f => f.module === v.module && f.fixMethod === 'yarn upgrade')) {
                    fixedModules.push({
                      module: v.module,
                      cveId: v.cveId,
                      severity: v.severity,
                      dependency: 'transitive',
                      fixMethod: 'yarn upgrade',
                      oldVersion: preUpgradeVersions.get(v.module) || v.currentVersion,
                      newVersion: installedVer
                    });
                  }
                }
              }

              if (b1FixedNames.size > 0) {
                lines.push(`  ✅ The following transitive vulnerabilities were resolved by yarn upgrade:`);
                lines.push(`  | Module | Old Version | New Version | CVE(s) Fixed |`);
                lines.push(`  |--------|-------------|-------------|--------------|`);
                for (const v of transitiveVulns) {
                  if (!b1FixedNames.has(v.module)) continue;
                  const f = fixedModules.find(m => m.module === v.module && m.fixMethod === 'yarn upgrade');
                  lines.push(`  | ${v.module} | ${f?.oldVersion || ''} | ${f?.newVersion || ''} | ${v.cveId} |`);
                }
              }
              const stillUnresolved = transitiveVulns.filter(v => !b1FixedNames.has(v.module));
              if (stillUnresolved.length > 0) {
                lines.push(`  ⚠️  The following transitive vulnerabilities remain unresolved after yarn upgrade:`);
                lines.push(`  | Module | Current Version | CVE(s) | Reason |`);
                lines.push(`  |--------|----------------|--------|--------|`);
                for (const v of stillUnresolved) {
                  lines.push(`  | ${v.module} | ${v.currentVersion} | ${v.cveId} | Outside ^ range |`);
                }
              }
            } else {
              lines.push(`  ⚠️  yarn upgrade failed: ${log}`);
            }
          } else {
            lines.push(`⏭️  Phase B1 — Skipping yarn upgrade (project uses npm). Proceeding to parent dependency upgrade check.`);
          }
        } // end npm B1
        lines.push('');

        // Re-check remaining after B1 — account for yarn upgrade fixes
        const b2Remaining = transitiveVulns.filter(v => !fixedModuleNames.has(v.module));

        // ── Phase B2: Parent dependency upgrades ──────────────────────────────
        if (b2Remaining.length > 0) {
          lines.push(`🔍 Phase B2 — Analysing parent dependencies for ${b2Remaining.length} remaining transitive vulnerability/ies...`);
          const parentProposals = [];
          const b2SkippedReasons = [];

          if (isMaven) {
            // Maven B2: use mvn versions:use-latest-releases on identified parent dep
            for (const v of b2Remaining) {
              const parent = findMavenParentDep(v.module, projectRoot);
              if (parent) {
                parentProposals.push({ transitivePkg: v.module, cveId: v.cveId, parent, vuln: v });
              } else {
                b2SkippedReasons.push({ module: v.module, cveId: v.cveId, reason: 'Could not identify a parent direct dependency from mvn dependency:tree' });
              }
            }

            if (parentProposals.length > 0) {
              lines.push(`🔐 Phase B2 — Maven parent dependency upgrades proposed:`);
              lines.push(`  | Transitive Pkg | CVE(s) | Parent Dependency |`);
              lines.push(`  |----------------|--------|-------------------|`);
              for (const p of parentProposals) {
                lines.push(`  | ${p.transitivePkg} | ${p.cveId} | ${p.parent} |`);
              }
              lines.push('');

              if (!approveParentUpgrades) {
                lines.push(`  ⏸️  Phase B2 not applied — set approveParentUpgrades=true to run mvn versions:use-latest-releases on these parents.`);
                for (const p of parentProposals) {
                  remainingModules.push({ module: p.transitivePkg, cveId: p.cveId, severity: p.vuln.severity, dependency: 'transitive', reason: `Parent upgrade pending approval (parent: ${p.parent})` });
                }
              } else {
                lines.push(`  ✅ approveParentUpgrades=true — running mvn versions:use-latest-releases...`);
                const done = new Set();
                for (const p of parentProposals) {
                  if (done.has(p.parent)) continue;
                  done.add(p.parent);
                  const { success, error } = tryRunCmd(`mvn versions:use-latest-releases -Dincludes="${p.parent}" -q`, projectRoot);
                  if (success) {
                    fixedModules.push({ module: p.transitivePkg, cveId: p.cveId, severity: p.vuln.severity, dependency: 'transitive', fixMethod: 'parent upgrade', oldVersion: p.vuln.currentVersion, newVersion: 'latest' });
                    fixedModuleNames.add(p.transitivePkg);
                    lines.push(`     ✅ ${p.parent} upgraded (fixes ${p.transitivePkg} ${p.cveId})`);
                  } else {
                    lines.push(`     ⚠️  mvn versions:use-latest-releases failed for ${p.parent}: ${error?.split('\n')[0]}`);
                    remainingModules.push({ module: p.transitivePkg, cveId: p.cveId, severity: p.vuln.severity, dependency: 'transitive', reason: `mvn versions:use-latest-releases failed for ${p.parent}` });
                  }
                }
              }
            } else {
              lines.push(`⏭️  Phase B2 — No parent dependency upgrade paths identified for any remaining transitive vulnerability.`);
              if (b2SkippedReasons.length > 0) {
                lines.push(`  Reasons:`);
                for (const s of b2SkippedReasons) {
                  lines.push(`    - ${s.module}: ${s.reason}`);
                  remainingModules.push({ module: s.module, cveId: s.cveId, severity: b2Remaining.find(v => v.module === s.module)?.severity || '', dependency: 'transitive', reason: s.reason });
                }
              }
            }
          } else {
            // npm B2: find npm parent dep and upgrade it
            for (const v of b2Remaining) {
              const parent = findParentDep(v.module, projectRoot, pm);
            if (parent) {
              const parentCurrentVersion = (() => {
                try { return JSON.parse(readFileSync(join(projectRoot, 'package.json'), 'utf8'))[
                  ((JSON.parse(readFileSync(join(projectRoot, 'package.json'), 'utf8')).dependencies || {})[parent] ? 'dependencies' : 'devDependencies')
                ]?.[parent] || 'unknown'; } catch { return 'unknown'; }
              })();
              const latestParentVersion = getLatestNpmVersion(parent, projectRoot);
              const proposed = latestParentVersion ? `^${latestParentVersion}` : 'latest';
              parentProposals.push({ transitivePkg: v.module, cveId: v.cveId, parent, parentCurrentVersion, proposedVersion: proposed, vuln: v });
            } else {
              const isDirectDep = (() => {
                try {
                  const p = JSON.parse(readFileSync(join(projectRoot, 'package.json'), 'utf8'));
                  return !!(p.dependencies || {})[v.module] || !!(p.devDependencies || {})[v.module];
                } catch { return false; }
              })();
              const reason = isDirectDep
                ? `"${v.module}" is itself a direct dependency`
                : `Could not identify a parent direct dependency via ${pm === 'yarn' ? 'yarn why' : 'npm ls'}`;
              b2SkippedReasons.push({ module: v.module, cveId: v.cveId, reason });
            }
          }

          if (parentProposals.length > 0) {
            lines.push(`🔐 Phase B2 — Parent dependency upgrades proposed:`);
            lines.push(`  | Transitive Pkg | CVE(s) | Parent Dependency | Current Version | Proposed Version |`);
            lines.push(`  |----------------|--------|-------------------|-----------------|------------------|`);
            for (const p of parentProposals) {
              lines.push(`  | ${p.transitivePkg} | ${p.cveId} | ${p.parent} | ${p.parentCurrentVersion} | ${p.proposedVersion} |`);
            }
            lines.push('');

            if (b2SkippedReasons.length > 0) {
              lines.push(`  ℹ️  Skipped (no parent upgrade path found):`);
              for (const s of b2SkippedReasons) {
                lines.push(`     - ${s.module} (${s.cveId}): ${s.reason}`);
                remainingModules.push({ module: s.module, cveId: s.cveId, severity: b2Remaining.find(v => v.module === s.module)?.severity || '', dependency: 'transitive', reason: s.reason });
              }
              lines.push('');
            }

            if (!approveParentUpgrades) {
              lines.push(`  ⏸️  Phase B2 not applied — set approveParentUpgrades=true to apply these upgrades.`);
              for (const p of parentProposals) {
                remainingModules.push({
                  module: p.transitivePkg,
                  cveId: p.cveId,
                  severity: p.vuln.severity,
                  dependency: 'transitive',
                  reason: `Parent upgrade pending approval (parent: ${p.parent} → ${p.proposedVersion})`
                });
              }
            } else {
              lines.push(`  ✅ approveParentUpgrades=true — applying parent upgrades...`);
              const pkg = readPackageJson(projectRoot);
              for (const p of parentProposals) {
                const depType = (pkg.dependencies || {})[p.parent] ? 'dependencies'
                  : (pkg.devDependencies || {})[p.parent] ? 'devDependencies'
                  : null;
                if (!depType) continue;
                const oldVersion = pkg[depType][p.parent];
                pkg[depType][p.parent] = p.proposedVersion;
                fixedModules.push({
                  module: p.transitivePkg,
                  cveId: p.cveId,
                  severity: p.vuln.severity,
                  dependency: 'transitive',
                  fixMethod: 'parent upgrade',
                  oldVersion,
                  newVersion: p.proposedVersion
                });
                fixedModuleNames.add(p.transitivePkg);
                lines.push(`     ${p.parent}: ${oldVersion} → ${p.proposedVersion} (fixes ${p.transitivePkg} ${p.cveId})`);
              }
              writePackageJson(projectRoot, pkg);
              const installCmd = pm === 'yarn' ? 'yarn install' : 'npm install';
              tryRunCmd(installCmd, projectRoot);
            }
          } else {
            lines.push(`⏭️  Phase B2 — No parent dependency upgrade paths identified for any remaining transitive vulnerability.`);
            if (b2SkippedReasons.length > 0) {
              lines.push(`  Reasons:`);
              for (const s of b2SkippedReasons) {
                lines.push(`    - ${s.module}: ${s.reason}`);
                remainingModules.push({ module: s.module, cveId: s.cveId, severity: b2Remaining.find(v => v.module === s.module)?.severity || '', dependency: 'transitive', reason: s.reason });
              }
            }
          }
          } // end else (npm B2)
        } // end if (b2Remaining.length > 0)
        lines.push('');

        // ── Phase B3 ──────────────────────────────────────────────────────────
        const b3Remaining = b2Remaining.filter(v => !fixedModuleNames.has(v.module));

        if (b3Remaining.length > 0) {
          if (isMaven) {
            lines.push(`🔐 Phase B3 — <dependencyManagement> entries proposed for remaining transitive vulnerabilities:`);
          } else {
            lines.push(`🔐 Phase B3 — Resolutions/overrides proposed for remaining transitive vulnerabilities:`);
          }
          lines.push(`  | Transitive Pkg | Current Version | Proposed Fix Version |`);
          lines.push(`  |----------------|-----------------|----------------------|`);
          for (const v of b3Remaining) {
            lines.push(`  | ${v.module} | ${v.currentVersion} | ${v.fixVersion} |`);
          }
          lines.push('');

          if (!approveResolutions) {
            const pendingLabel = isMaven ? '<dependencyManagement> entries' : 'resolutions/overrides';
            lines.push(`  ⏸️  Phase B3 not applied — set approveResolutions=true to add ${pendingLabel}.`);
            for (const v of b3Remaining) {
              if (!remainingModules.some(r => r.module === v.module && r.cveId === v.cveId)) {
                remainingModules.push({
                  module: v.module,
                  cveId: v.cveId,
                  severity: v.severity,
                  dependency: 'transitive',
                  reason: isMaven ? 'dependencyManagement pending approval' : 'Resolutions pending approval'
                });
              }
            }
          } else if (isMaven) {
            lines.push(`  ✅ approveResolutions=true — adding <dependencyManagement> entries...`);
            try {
              const fixed = applyMavenDependencyManagement(b3Remaining, projectRoot);
              fixedModules.push(...fixed);
              for (const f of fixed) fixedModuleNames.add(f.module);
              lines.push(`  ✅ Added ${fixed.length} <dependencyManagement> entry/ies to pom.xml`);
              for (const f of fixed) lines.push(`     ${f.module}: pinned to ${f.newVersion} (${f.cveId})`);
            } catch (err) {
              lines.push(`  ⚠️  Phase B3 failed: ${err.message}`);
              for (const v of b3Remaining) {
                remainingModules.push({ module: v.module, cveId: v.cveId, severity: v.severity, dependency: 'transitive', reason: `dependencyManagement failed: ${err.message}` });
              }
            }
          } else {
            lines.push(`  ✅ approveResolutions=true — applying resolutions...`);
            try {
              const fixed = applyResolutions(b3Remaining, projectRoot, pm);
              fixedModules.push(...fixed);
              for (const f of fixed) fixedModuleNames.add(f.module);
              lines.push(`  ✅ Added ${fixed.length} resolution(s) to package.json`);
              for (const f of fixed) lines.push(`     ${f.module}: pinned to ${f.newVersion} (${f.cveId})`);
            } catch (err) {
              lines.push(`  ⚠️  Phase B3 failed: ${err.message}`);
              for (const v of b3Remaining) {
                remainingModules.push({
                  module: v.module,
                  cveId: v.cveId,
                  severity: v.severity,
                  dependency: 'transitive',
                  reason: `Resolution failed: ${err.message}`
                });
              }
            }
          }
        }
        lines.push('');

        // Track truly unresolvable direct vulns (no fixVersion)
        const unfixableDirect = allVulnerabilities.filter(
          v => v.dependency === 'direct' && !v.fixVersion && !fixedModuleNames.has(v.module)
        );
        for (const v of unfixableDirect) {
          remainingModules.push({
            module: v.module,
            cveId: v.cveId || v.vulnId,
            severity: v.severity,
            dependency: 'direct',
            reason: 'No fix version available'
          });
        }

        // Track truly unresolvable transitive vulns (no fixVersion at all)
        const unfixableTransitive = allVulnerabilities.filter(
          v => v.dependency === 'transitive' && !v.fixVersion && !fixedModuleNames.has(v.module)
        );
        for (const v of unfixableTransitive) {
          if (!remainingModules.some(r => r.module === v.module && r.cveId === v.cveId)) {
            remainingModules.push({
              module: v.module,
              cveId: v.cveId || v.vulnId,
              severity: v.severity,
              dependency: 'transitive',
              reason: 'No fix version available'
            });
          }
        }

        // ── Phase C: Append fix report ─────────────────────────────────────────
        const fixSummary = {
          fixDate: new Date().toLocaleString(),
          totalOriginal: allVulnerabilities.length,
          totalFixed: fixedModules.length,
          totalRemaining: remainingModules.length,
          byMethod: {
            packageJsonUpdate: fixedModules.filter(f => f.fixMethod === 'package.json update').length,
            pomUpdate:         fixedModules.filter(f => f.fixMethod === 'pom.xml update').length,
            yarnUpgrade:       fixedModules.filter(f => f.fixMethod === 'yarn upgrade').length,
            parentUpgrade:     fixedModules.filter(f => f.fixMethod === 'parent upgrade').length,
            resolution:        fixedModules.filter(f => f.fixMethod === 'resolution').length,
            dependencyManagement: fixedModules.filter(f => f.fixMethod === 'dependencyManagement').length
          },
          fixedModules,
          remainingModules
        };

        try {
          appendFixSummary(fixSummary);
          lines.push(`📄 Fix summary appended to nexus-report/ files.`);
        } catch (_) {
          lines.push(`⚠️  Could not append fix summary to reports.`);
        }

        lines.push('');
        lines.push('✅ Vulnerability Fix Summary');
        lines.push('════════════════════════════════════════');
        lines.push(`Direct Dependencies Fixed:     ${fixSummary.byMethod.packageJsonUpdate + fixSummary.byMethod.pomUpdate}`);
        lines.push(`Transitive (yarn upgrade):     ${fixSummary.byMethod.yarnUpgrade}`);
        lines.push(`Transitive (parent upgrade):   ${fixSummary.byMethod.parentUpgrade}`);
        lines.push(`Transitive (resolutions/DM):   ${fixSummary.byMethod.resolution + fixSummary.byMethod.dependencyManagement}`);
        lines.push(`Remaining Unresolved:          ${fixSummary.totalRemaining}`);
        lines.push('════════════════════════════════════════');

        if (remainingModules.length > 0) {
          lines.push('');
          lines.push('⏭️  Re-run nexus_scan_vulnerabilities to verify fixes and check remaining vulnerabilities.');
        }

        // Open HTML report in default browser
        const htmlReportPath = join(projectRoot, 'nexus-report', 'nexus-vulnerability-report.html');
        await openInBrowser(htmlReportPath);
        lines.push('');
        lines.push(`✅ Fix report appended to scan report. Opening nexus-vulnerability-report.html...`);

        return { content: [{ type: 'text', text: lines.join('\n') }] };
      } catch (error) {
        return {
          content: [{ type: 'text', text: error?.message || String(error) }],
          isError: true
        };
      }
    }
  );
}
