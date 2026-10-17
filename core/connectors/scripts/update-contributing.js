#!/usr/bin/env node

import { readFileSync, writeFileSync, existsSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const contributingPath = join(root, 'CONTRIBUTING.md');

const STATS_START = '<!-- STATS-START -->';
const STATS_END = '<!-- STATS-END -->';

// Count tools by scanning server.tool( and registerAppTool( calls across all src files
function countTools() {
  const packagesDir = join(root, 'packages');
  let count = 0;
  const pkgs = readdirSync(packagesDir, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name);

  for (const pkg of pkgs) {
    const srcPath = join(packagesDir, pkg, 'src');
    if (!existsSync(srcPath)) continue;
    const files = readdirSync(srcPath, { recursive: true })
      .filter(f => typeof f === 'string' && f.endsWith('.js'));
    for (const file of files) {
      const src = readFileSync(join(srcPath, file), 'utf8');
      const serverTools = src.match(/server\.tool\s*\(/g);
      const appTools = src.match(/registerAppTool\s*\(/g);
      if (serverTools) count += serverTools.length;
      if (appTools) count += appTools.length;
    }
  }
  return count;
}

// Count prompts by scanning UPPER_CASE keys in all packages/*/src/prompts.js files
function countPrompts() {
  const packagesDir = join(root, 'packages');
  let count = 0;
  const pkgs = readdirSync(packagesDir, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name);

  for (const pkg of pkgs) {
    const promptsPath = join(packagesDir, pkg, 'src', 'prompts.js');
    if (!existsSync(promptsPath)) continue;
    const src = readFileSync(promptsPath, 'utf8');
    // Each prompt definition is an UPPER_CASE key followed by { in a *_PROMPTS object
    const matches = src.match(/^\s{2}[A-Z][A-Z0-9_]+\s*:\s*\{/gm);
    if (matches) count += matches.length;
  }
  return count;
}

// Build the stats block content
function buildStatsBlock(toolCount, promptCount) {
  const date = new Date().toISOString().slice(0, 10);
  return [
    STATS_START,
    `> **Auto-generated on ${date} — run \`npm run update-contributing\` to refresh.**`,
    `> - **Tool declarations:** ${toolCount} (total across all packages including standalone; unified server exposes 112 max)`,
    `> - **Prompts:** ${promptCount}`,
    STATS_END
  ].join('\n');
}

// Full initial CONTRIBUTING.md content (written when file doesn't exist)
function buildInitialContent(toolCount, promptCount) {
  const statsBlock = buildStatsBlock(toolCount, promptCount);
  return `# Contributing to SC Node MCP

Thank you for contributing! Please read the guidelines below before raising a pull request.

## How to Contribute

1. Create a feature branch from \`main\`: \`git checkout -b feat/my-change\`
2. Make your changes and write or update tests
3. Run \`npm run pre-pr\` — this refreshes the README install URLs, updates the stats in this file, and runs all tests
4. Raise a pull request with a clear description (the PR template will guide you)

## Adding or Modifying a Tool

- Tool files live in \`packages/*/src/tools/\`
- Register each tool with \`server.tool()\` following the existing pattern
- **You must update [docs/TOOLS_REFERENCE.md](docs/TOOLS_REFERENCE.md)** to document the new or changed tool

## Adding or Modifying a Prompt

- Prompts are distributed across per-package files: \`packages/*/src/prompts.js\`
- Add to the appropriate package's \`prompts.js\` (e.g. \`packages/ado/src/prompts.js\` for ADO prompts)
- Unified-only prompts (context management, upload UI) stay in \`packages/unified/src/prompts.js\`
- **You must update [docs/PROMPTS.md](docs/PROMPTS.md)** to document the new or changed prompt

## Updating Docs

Any change to a tool or prompt that is visible to consumers **must** have a corresponding doc update. The PR checklist in \`.azuredevops/pull_request_template.md\` will remind you.

## Running Tests

\`\`\`bash
npm test               # all packages
npm run test:coverage  # with coverage report
\`\`\`

Coverage threshold is 90% across lines, functions, branches, and statements.

## Before Every PR

\`\`\`bash
npm run pre-pr
\`\`\`

This runs \`update-readme\` (refreshes one-click install badge URLs), \`update-contributing\` (updates the stats block below), and \`npm test\`.

---

## Current Stats

${statsBlock}
`;
}

// Update just the stats block in an existing CONTRIBUTING.md
function updateStats(content, toolCount, promptCount) {
  const startIdx = content.indexOf(STATS_START);
  const endIdx = content.indexOf(STATS_END);
  if (startIdx === -1 || endIdx === -1) {
    // Append stats block if markers are missing (shouldn't normally happen)
    return content.trimEnd() + '\n\n' + buildStatsBlock(toolCount, promptCount) + '\n';
  }
  return (
    content.slice(0, startIdx) +
    buildStatsBlock(toolCount, promptCount) +
    content.slice(endIdx + STATS_END.length)
  );
}

const toolCount = countTools();
const promptCount = countPrompts();

if (existsSync(contributingPath)) {
  const content = readFileSync(contributingPath, 'utf8');
  writeFileSync(contributingPath, updateStats(content, toolCount, promptCount), 'utf8');
  console.log(`✓ CONTRIBUTING.md stats updated (${toolCount} tools, ${promptCount} prompts)`);
} else {
  writeFileSync(contributingPath, buildInitialContent(toolCount, promptCount), 'utf8');
  console.log(`✓ CONTRIBUTING.md created (${toolCount} tools, ${promptCount} prompts)`);
}
