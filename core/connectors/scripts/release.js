#!/usr/bin/env node
/**
 * Custom release script.
 *
 * Usage:
 *   npm run release -- [--work-item=<ADO work item ID>] [--yes]
 *
 * Flags:
 *   --work-item=<id>   ADO work item ID. When provided, skips auto-detection
 *                      and confirmation entirely (non-interactive, backward-compatible).
 *   --yes              Non-interactive mode. Skips all prompts. Requires either
 *                      --work-item=<id> OR a detectable #<id> in the last 3 commits.
 *
 * What it does:
 *  1. Determines the ADO work item ID:
 *     - If --work-item=<id> is passed, use it directly (non-interactive)
 *     - Otherwise, scans the last 3 commits for a #<id> reference
 *     - Prompts to confirm or override the detected ID (unless --yes)
 *     - If no ID is found and not --yes, prompts interactively
 *  2. Previews which packages have pending changes (via `lerna changed`)
 *     - If no packages have changes, exits cleanly
 *     - Prompts to confirm the list before proceeding (unless --yes)
 *  3. Reads all package versions before bumping (snapshot)
 *  4. Runs `npm run docs` to regenerate README.md / CONTRIBUTING.md
 *  5. Runs `lerna version --no-git-tag-version` to bump package.json files
 *     and CHANGELOG.md entries without creating a git commit or tag
 *  6. Detects which packages were bumped (diff vs snapshot)
 *  7. Stages all changes via `git add -A`
 *  8. Creates ONE commit:  chore(release): #<id> - publish
 *  9. Creates per-package git tags to replicate lerna's normal behaviour
 */

import { execSync } from 'node:child_process';
import { readFileSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createInterface } from 'node:readline';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function run(cmd, opts = {}) {
  console.log(`\n> ${cmd}`);
  execSync(cmd, { cwd: root, stdio: 'inherit', ...opts });
}

function readPackageVersions() {
  const packagesDir = join(root, 'packages');
  const dirs = readdirSync(packagesDir, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name);

  const versions = {};
  for (const dir of dirs) {
    const pkgPath = join(packagesDir, dir, 'package.json');
    try {
      const pkg = JSON.parse(readFileSync(pkgPath, 'utf8'));
      if (pkg.name && pkg.version) {
        versions[pkg.name] = pkg.version;
      }
    } catch {
      // skip packages without package.json
    }
  }
  return versions;
}

function promptUser(question) {
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => {
    rl.question(question, answer => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

function detectWorkItemFromGit() {
  try {
    const log = execSync('git log --oneline -3 --no-decorate', { cwd: root, encoding: 'utf8' });
    for (const line of log.split('\n')) {
      const match = line.match(/\B#(\d+)\b/);
      if (match) return match[1];
    }
  } catch {
    // git log failed — ignore
  }
  return null;
}

function getChangedPackages() {
  try {
    const output = execSync('npx lerna changed', {
      cwd: root,
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe'],
    });
    return output
      .split('\n')
      .map(l => l.trim())
      .filter(l => l && !l.startsWith('info') && !l.startsWith('warn'));
  } catch (err) {
    // lerna changed exits non-zero when no packages have pending changes — that is expected
    const stderr = (err.stderr || '').toString();
    const stdout = (err.stdout || '').toString().trim();
    if (!stdout || stderr.includes('No changed packages found')) return [];
    throw new Error(`Failed to get changed packages: ${stderr || err.message}`);
  }
}

// ---------------------------------------------------------------------------
// Step 1: Determine work item ID
// ---------------------------------------------------------------------------
async function resolveWorkItemId(workItemArg, yesMode) {
  if (workItemArg) {
    const id = workItemArg.split('=')[1].trim();
    if (!id) {
      console.error('Error: --work-item value cannot be empty.\n');
      process.exit(1);
    }
    console.log(`\n🔖  Using work item: #${id}`);
    return id;
  }

  const detected = detectWorkItemFromGit();

  if (detected) {
    return resolveDetectedWorkItem(detected, yesMode);
  }

  // Nothing found in commits
  if (yesMode) {
    console.error('Error: Could not auto-detect a work item ID from the last 3 commits.\n');
    console.error('       In --yes mode, pass --work-item=<id> or ensure the last commit contains #<id>.\n');
    process.exit(1);
  }
  console.log('\n⚠️   No work item ID found in the last 3 commits.');
  return promptForWorkItem();
}

async function resolveDetectedWorkItem(detected, yesMode) {
  console.log(`\n🔍  Detected work item from recent commits: #${detected}`);
  if (yesMode) {
    console.log('    (--yes mode: using detected work item automatically)');
    return detected;
  }
  const answer = await promptUser('    Use this work item? [Y/n]: ');
  if (answer === '' || answer.toLowerCase() === 'y') return detected;
  return promptForWorkItem();
}

async function promptForWorkItem() {
  const entered = await promptUser('    Enter work item ID: ');
  if (!entered) {
    console.error('Error: work item ID cannot be empty.\n');
    process.exit(1);
  }
  return entered;
}

// ---------------------------------------------------------------------------
// Step 2: Preview and confirm packages to bump
// ---------------------------------------------------------------------------
async function previewAndConfirmPackages(yesMode) {
  console.log('\n🔎  Checking which packages have pending changes...');
  const changedPackages = getChangedPackages();

  if (changedPackages.length === 0) {
    console.log('\n⚠️   No packages have pending changes. Nothing to release. Exiting.');
    process.exit(0);
  }

  console.log('\n📦  Packages to be bumped:');
  for (const pkg of changedPackages) {
    console.log(`   ${pkg}`);
  }

  if (!yesMode) {
    const proceed = await promptUser('\n    Proceed with bumping these packages? [Y/n]: ');
    if (proceed.toLowerCase() === 'n') {
      console.log('\n⛔  Release cancelled.\n');
      process.exit(0);
    }
  }
}

// ---------------------------------------------------------------------------
// Steps 3–9: Version bump, commit, and tag
// ---------------------------------------------------------------------------
function bumpAndCommit(workItemId) {
  // 3. Snapshot versions before bump
  console.log('\n📸  Snapshotting current package versions...');
  const before = readPackageVersions();

  // 4. Generate docs (updates README.md / CONTRIBUTING.md)
  console.log('\n📝  Generating documentation...');
  run('npm run docs');

  // 5. Bump versions without committing
  //    --no-git-tag-version  → no commit, no tag (bypasses dirty-tree check)
  //    --conventional-commits → uses conventional commits to determine bump type
  //    --yes                  → skip interactive prompt
  console.log('\n🔖  Bumping versions (no commit / no tag)...');
  run('npx lerna version --no-git-tag-version --conventional-commits --yes');

  // 6. Detect bumped packages
  const after = readPackageVersions();
  const bumped = Object.entries(after)
    .filter(([name, newVer]) => before[name] !== newVer)
    .map(([name, newVer]) => ({ name, oldVersion: before[name], newVersion: newVer }));

  if (bumped.length === 0) {
    console.log('\n⚠️   No packages were bumped — nothing to commit. Exiting.');
    process.exit(0);
  }

  console.log('\n📦  Bumped packages:');
  for (const { name, oldVersion, newVersion } of bumped) {
    console.log(`   ${name}: ${oldVersion} → ${newVersion}`);
  }

  // 7. Stage all changes
  console.log('\n📂  Staging all changes...');
  run('git add -A');

  // 8. Create single release commit
  //    Subject: chore(release): #<id> - publish
  //    Body: one line per bumped package
  const packageLines = bumped.map(({ name, newVersion }) => ` - ${name}@${newVersion}`).join('\n');
  const commitMessage = `chore(release): #${workItemId} - publish\n\n${packageLines}\n`;

  console.log('\n✅  Creating release commit...');
  console.log('\n> git commit -F -');
  execSync('git commit -F -', { cwd: root, stdio: ['pipe', 'inherit', 'inherit'], input: commitMessage });

  // 9. Create per-package git tags
  console.log('\n🏷️   Creating git tags...');
  for (const { name, newVersion } of bumped) {
    const tag = `${name}@${newVersion}`;
    run(`git tag "${tag}"`);
    console.log(`   Tagged: ${tag}`);
  }

  console.log('\n🎉  Release commit created successfully!');
  console.log(`    Commit: chore(release): #${workItemId} - publish`);
  console.log(`    Packages bumped: ${bumped.length}`);
  console.log('\n    Run `git push --follow-tags` when ready to push.\n');
}

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------
const args = process.argv.slice(2);
const workItemArg = args.find(a => a.startsWith('--work-item='));
const yesMode = args.includes('--yes');

try {
  const workItemId = await resolveWorkItemId(workItemArg, yesMode);
  await previewAndConfirmPackages(yesMode);
  bumpAndCommit(workItemId);
} catch (err) {
  console.error('\n❌  Release failed:', err.message || err);
  process.exit(1);
}
