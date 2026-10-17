#!/usr/bin/env node
/**
 * post-build.js
 *
 * Patches each package's package.json after `yarn build` so that
 * `main`, `bin`, `exports`, and `files` all point to `dist/` instead of `src/`.
 *
 * Run via: node scripts/post-build.js  (or `yarn post-build` at the root)
 *
 * The script is idempotent — paths already referencing `dist/` are left unchanged.
 * Private packages (e.g. shared-tests) are skipped automatically.
 */

import { readFileSync, writeFileSync, readdirSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const packagesDir = join(__dirname, '..', 'packages');

/**
 * Replace leading `src/` or `./src/` with `dist/` / `./dist/`.
 * Leaves any string that already references dist/ untouched.
 */
function srcToDist(value) {
  if (typeof value !== 'string') return value;
  return value
    .replace(/^src\//, 'dist/')
    .replace(/^\.\/src\//, './dist/');
}

function patchStringField(pkg, field) {
  const patched = srcToDist(pkg[field]);
  if (patched !== pkg[field]) { pkg[field] = patched; return true; }
  return false;
}

function patchObjectField(pkg, field) {
  if (!pkg[field]) return false;
  let changed = false;
  for (const key of Object.keys(pkg[field])) {
    const patched = srcToDist(pkg[field][key]);
    if (patched !== pkg[field][key]) { pkg[field][key] = patched; changed = true; }
  }
  return changed;
}

function patchFilesField(pkg) {
  if (!pkg.files) return false;
  // Replace src/**/* → dist/**/* and deduplicate (handles ado-upload-app
  // which ships both src/**/* and dist/**/* before the patch).
  const patched = [...new Set(pkg.files.map(f => f.replace(/^src\//, 'dist/')))];
  if (JSON.stringify(patched) === JSON.stringify(pkg.files)) return false;
  pkg.files = patched;
  return true;
}

function patchPackageJson(pkgPath) {
  const pkg = JSON.parse(readFileSync(pkgPath, 'utf8'));

  const changed = [
    pkg.main ? patchStringField(pkg, 'main') : false,
    patchObjectField(pkg, 'bin'),
    patchObjectField(pkg, 'exports'),
    patchFilesField(pkg),
  ].some(Boolean);

  if (changed) {
    writeFileSync(pkgPath, JSON.stringify(pkg, null, 2) + '\n');
    console.log(`✓ Patched  ${pkgPath}`);
  } else {
    console.log(`  Skipped  ${pkgPath} (no src/ paths to replace)`);
  }
}

const packages = readdirSync(packagesDir).filter(name => {
  try { statSync(join(packagesDir, name, 'package.json')); return true; }
  catch { return false; }
});

for (const name of packages) {
  const pkgPath = join(packagesDir, name, 'package.json');
  const pkg = JSON.parse(readFileSync(pkgPath, 'utf8'));
  if (!pkg.private) {
    patchPackageJson(pkgPath);
  }
}
