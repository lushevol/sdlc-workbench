import { createHash } from 'node:crypto';
import { readFile, realpath } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = await realpath(fileURLToPath(new URL('../../', import.meta.url)));
const manifests = ['main', 'dialog', 'shared'].map(area => `e2e/traceability/cashflow-${area}-inventory.json`);
const errors = [];
const fingerprints = new Map();
let rangeCount = 0;

for (const manifest of manifests) {
  const inventory = JSON.parse(await readFile(path.join(root, manifest), 'utf8'));
  const sources = new Map();
  function collectSources(value) {
    if (!value || typeof value !== 'object') return;
    if (value.path && value.sha256) sources.set(value.path, value);
    for (const child of Object.values(value)) {
      if (Array.isArray(child)) child.forEach(collectSources);
      else if (child && typeof child === 'object') collectSources(child);
    }
  }
  collectSources(inventory);
  for (const source of sources.values()) {
    try {
      const target = await realpath(path.join(root, source.path));
      if (!target.startsWith(`${root}${path.sep}`)) throw new Error('Source must remain inside the workspace.');
      const bytes = await readFile(target);
      const sha256 = createHash('sha256').update(bytes).digest('hex');
      if (sha256 !== source.sha256) throw new Error('Source hash differs from the inspected bytes.');
      if (fingerprints.has(source.path) && fingerprints.get(source.path) !== sha256) throw new Error('Inventories disagree about source bytes.');
      fingerprints.set(source.path, sha256);
      const lines = bytes.toString('utf8').split(/\r?\n/);
      if (lines.at(-1) === '') lines.pop();
      source.currentLineCount = lines.length;
      if (source.line_count !== undefined && source.line_count !== lines.length) throw new Error('Source line count differs.');
    } catch (error) {
      errors.push({ manifest, source: source.path, message: String(error.message) });
    }
  }
  function inspect(value, inheritedPath) {
    if (!value || typeof value !== 'object') return;
    const sourcePath = value.path ?? (typeof value.source === 'string' ? value.source : value.source?.path) ?? inheritedPath;
    const range = value.lines ?? (value.line ? [value.line, value.line] : undefined);
    if (range && sourcePath) {
      rangeCount++;
      const source = sources.get(sourcePath);
      const [start, end] = range;
      if (!source || !Number.isSafeInteger(start) || !Number.isSafeInteger(end) || start < 1 || end < start || end > source.currentLineCount) {
        errors.push({ manifest, source: sourcePath, lines: range, message: 'Invalid or unavailable source range.' });
      }
    }
    for (const child of Object.values(value)) {
      if (Array.isArray(child)) child.forEach(item => inspect(item, sourcePath));
      else if (child && typeof child === 'object') inspect(child, sourcePath);
    }
  }
  inspect(inventory);
}

console.log(JSON.stringify({ status: errors.length ? 'FAILED' : 'PASSED', manifests: manifests.length,
  sourceFiles: fingerprints.size, sourceRanges: rangeCount, errors,
  runtimeVerification: 'UNVERIFIED',
  limits: ['Checks exact local source bytes and bounded locators only.',
    'Does not establish deployed control coverage, selector compatibility, business behavior, or approval.'] }, null, 2));
process.exitCode = errors.length ? 1 : 0;
