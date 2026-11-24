import { execFile } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';
import {
  createCategoryContracts, createCategoryDetailContracts, createCategoryRecordContracts,
  createLoginContracts, createPortalContracts, createWorkspaceContracts, createWorkspaceNameContract,
  uiContracts, type SourceEvidence, type UiContract,
} from '../catalog/ui-contracts.js';

const execFileAsync = promisify(execFile);
const defaultRoot = fileURLToPath(new URL('../../', import.meta.url));

export interface SourceQualityError {
  readonly code: string;
  readonly message: string;
  readonly contractId?: string;
  readonly source?: SourceEvidence;
}

export interface SourceQualityResult {
  readonly status: 'passed' | 'failed';
  readonly contractCount: number;
  readonly sourceCount: number;
  readonly runtimeVerification: 'unverified';
  readonly errors: readonly SourceQualityError[];
}

function currentContracts(): UiContract[] {
  return [
    ...Object.values(uiContracts),
    ...Object.values(createLoginContracts('source-quality')),
    ...Object.values(createPortalContracts('source-quality')),
    ...Object.values(createWorkspaceContracts('source-quality-workspace')),
    createWorkspaceNameContract('Source quality workspace'),
    ...Object.values(createCategoryContracts('source-quality')),
    ...Object.values(createCategoryRecordContracts('source-quality-record')),
    ...(['new', 'edit', 'verify', 'deactivate'] as const).flatMap(mode =>
      Object.values(createCategoryDetailContracts(mode, 'source-quality-record'))),
  ];
}

// This checks retained source definitions. It does not establish runtime uniqueness or business results.
export async function checkSourceContracts(root = defaultRoot): Promise<SourceQualityResult> {
  const contracts = currentContracts();
  const errors: SourceQualityError[] = [];
  const ids = new Set<string>();
  const sources = new Map<string, SourceEvidence>();
  for (const contract of contracts) {
    for (const field of ['id', 'area', 'componentType', 'identity', 'identityMethod', 'scope'] as const) {
      if (typeof contract[field] !== 'string' || contract[field].trim().length === 0) {
        errors.push({ code: 'empty-contract-field', message: `Contract field ${field} must be nonempty.`, contractId: contract.id });
      }
    }
    if (ids.has(contract.id)) {
      errors.push({ code: 'duplicate-contract-id', message: 'Contract IDs must be unique.', contractId: contract.id });
    }
    ids.add(contract.id);
    if (contract.grounding !== 'source-inspected' || contract.runtimeVerification !== 'unverified') {
      errors.push({ code: 'unsupported-verification-claim', message: 'Static contracts must preserve source and runtime evidence limits.', contractId: contract.id });
    }
    if (!Array.isArray(contract.sources) || contract.sources.length === 0) {
      errors.push({ code: 'missing-source', message: 'A contract must cite source evidence.', contractId: contract.id });
    }
    for (const source of contract.sources) {
      if (!/^[a-f0-9]{40}$/.test(source.revision)) {
        errors.push({ code: 'invalid-revision', message: 'Source evidence requires a full Git commit identity.', source, contractId: contract.id });
      }
      if (source.repositoryId !== 'mfe-base') {
        errors.push({ code: 'unsupported-repository', message: 'The source checker supports the inspected mfe-base repository.', source, contractId: contract.id });
      }
      if (source.path.includes('\\') || path.posix.isAbsolute(source.path) ||
          source.path.split('/').some(part => part === '..' || part === '') || source.path.length === 0) {
        errors.push({ code: 'invalid-source-path', message: 'Source paths must remain relative to the registered repository.', source, contractId: contract.id });
        continue;
      }
      sources.set(`${source.repositoryId}:${source.revision}:${source.path}:${source.lines.join('-')}`, source);
    }
  }

  const fileCache = new Map<string, { retained: Buffer; current: Buffer } | null>();
  for (const source of sources.values()) {
    if (!/^[a-f0-9]{40}$/.test(source.revision) || source.repositoryId !== 'mfe-base') continue;
    const fileKey = `${source.repositoryId}:${source.revision}:${source.path}`;
    if (!fileCache.has(fileKey)) {
      try {
        const repository = path.join(root, 'repos', 'ui', 'mfe-base');
        const retained = await execFileAsync('git', ['-C', repository, 'show', `${source.revision}:${source.path}`],
          { encoding: 'buffer', maxBuffer: 4 * 1024 * 1024 });
        const current = await readFile(path.join(repository, source.path));
        fileCache.set(fileKey, { retained: retained.stdout, current });
        if (!retained.stdout.equals(current)) {
          errors.push({ code: 'source-bytes-changed', message: 'Current source bytes differ from the cited Git revision.', source });
        }
      } catch (error) {
        fileCache.set(fileKey, null);
        errors.push({ code: 'source-unavailable', message: error instanceof Error ? error.message : String(error), source });
      }
    }
    const file = fileCache.get(fileKey);
    if (!file) continue;
    const lines = file.retained.toString('utf8').split(/\r?\n/);
    if (lines.at(-1) === '') lines.pop();
    const [start, end] = source.lines;
    if (!Number.isSafeInteger(start) || !Number.isSafeInteger(end) || start < 1 || end < start || end > lines.length) {
      errors.push({ code: 'invalid-source-range', message: 'Source line ranges must identify existing lines.', source });
    } else if (lines.slice(start - 1, end).every(line => line.trim().length === 0)) {
      errors.push({ code: 'empty-source-range', message: 'Source line ranges must contain nonempty content.', source });
    }
  }
  return { status: errors.length === 0 ? 'passed' : 'failed', contractCount: contracts.length,
    sourceCount: sources.size, runtimeVerification: 'unverified', errors };
}
