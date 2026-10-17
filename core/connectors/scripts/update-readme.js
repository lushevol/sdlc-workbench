#!/usr/bin/env node

import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { stableUrl, insidersUrl, stableBadgeUrl, insidersBadgeUrl, teamsChannelBadgeUrl, teamsChannelUrl, adoPipelineUrl, adoPipelineBadgeUrl, generateGranularTable } from './create-install-url.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

const START_MARKER = '<!-- ONE-CLICK-INSTALL-START -->';
const END_MARKER = '<!-- ONE-CLICK-INSTALL-END -->';

const newBadgeBlock = [
  START_MARKER,
  `[![Pipeline](${adoPipelineBadgeUrl})](${adoPipelineUrl})`,
  '',
  `[![Install with NPX in VS Code](${stableBadgeUrl})](${stableUrl})`,
  '',
  `[![Install with NPX in VS Code Insiders](${insidersBadgeUrl})](${insidersUrl})`,
  '',
  `[![Teams Channel](${teamsChannelBadgeUrl})](${teamsChannelUrl})`,
  END_MARKER
].join('\n');

const filesToUpdate = [
  join(__dirname, '..', 'README.md'),
  join(__dirname, '..', 'CONSUMER_GUIDE.md'),
  join(__dirname, '..', 'packages', 'unified', 'README.md'),
];

const GRANULAR_START_MARKER = '<!-- GRANULAR-INSTALL-START -->';
const GRANULAR_END_MARKER = '<!-- GRANULAR-INSTALL-END -->';

const newGranularBlock = `${GRANULAR_START_MARKER}\n${generateGranularTable()}\n${GRANULAR_END_MARKER}`;

const granularFilesToUpdate = [
  join(__dirname, '..', 'README.md'),
  join(__dirname, '..', 'CONSUMER_GUIDE.md'),
];

for (const filePath of filesToUpdate) {
  const content = readFileSync(filePath, 'utf8');
  const startIdx = content.indexOf(START_MARKER);
  const endIdx = content.indexOf(END_MARKER);

  if (startIdx === -1 || endIdx === -1) {
    console.error(`ERROR: Could not find ONE-CLICK-INSTALL markers in ${filePath}`);
    process.exit(1);
  }

  const updated = content.slice(0, startIdx) + newBadgeBlock + content.slice(endIdx + END_MARKER.length);
  writeFileSync(filePath, updated, 'utf8');
  console.log(`✓ ${filePath.split('/').slice(-2).join('/')} install URLs updated`);
}

for (const filePath of granularFilesToUpdate) {
  const content = readFileSync(filePath, 'utf8');
  const startIdx = content.indexOf(GRANULAR_START_MARKER);
  const endIdx = content.indexOf(GRANULAR_END_MARKER);

  if (startIdx === -1 || endIdx === -1) {
    console.error(`ERROR: Could not find GRANULAR-INSTALL markers in ${filePath}`);
    process.exit(1);
  }

  const updated = content.slice(0, startIdx) + newGranularBlock + content.slice(endIdx + GRANULAR_END_MARKER.length);
  writeFileSync(filePath, updated, 'utf8');
  console.log(`✓ ${filePath.split('/').slice(-2).join('/')} granular install table updated`);
}
