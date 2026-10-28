import { readFileSync } from 'node:fs';
import path from 'node:path';
import { requireIdentifier } from '../catalog/ui-contracts.js';
import { sha256 } from './results.js';

export class TargetConfigurationError extends Error { override name = 'TargetConfigurationError'; }
export type TargetOptions = {
  environment?: string; environmentsFile?: string; url?: string; prefix?: string; storageState?: string;
};
export type Target = {
  name: string; targetUrl: string; prefix: string; area: 'login' | 'portal' | 'category';
  storageState?: string; workspaceName?: string; refreshCredentialSha256?: string; configurationSha256: string;
};

function object(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}
function readJson(file: string, description: string): unknown {
  try { return JSON.parse(readFileSync(file, 'utf8')); }
  catch { throw new TargetConfigurationError(`Cannot read valid JSON for ${description}.`); }
}
function text(value: unknown, description: string): string {
  if (typeof value !== 'string' || !value.trim()) throw new TargetConfigurationError(`${description} must be a nonempty string.`);
  return value;
}
function targetUrl(value: unknown): string {
  const raw = text(value, 'targetUrl');
  let url: URL;
  try { url = new URL(raw); }
  catch { throw new TargetConfigurationError('targetUrl must be an absolute HTTP(S) URL.'); }
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password)
    throw new TargetConfigurationError('targetUrl must use HTTP(S) without embedded credentials.');
  return url.href;
}

export function loadTarget(options: TargetOptions = {}, env: NodeJS.ProcessEnv = process.env): Target | undefined {
  const name = options.environment ?? env.E2E_ENVIRONMENT;
  const file = options.environmentsFile ?? env.E2E_ENVIRONMENTS_FILE;
  let profile: Record<string, unknown>;
  let directory = process.cwd();
  if (name !== undefined) {
    if (!/^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$/.test(name)) throw new TargetConfigurationError('Use a simple environment name.');
    if (options.url !== undefined || options.prefix !== undefined || options.storageState !== undefined)
      throw new TargetConfigurationError('Choose a named environment or direct URL options; profile overrides are ambiguous.');
    const profilesPath = path.resolve(file ?? '.workbench/e2e-environments.json');
    const catalog = readJson(profilesPath, 'environment profiles');
    if (!object(catalog) || Object.keys(catalog).some(key => !['schemaVersion', 'environments'].includes(key)) ||
      (catalog.schemaVersion !== undefined && catalog.schemaVersion !== 1) || !object(catalog.environments))
      throw new TargetConfigurationError('Use schemaVersion 1 and an environments mapping.');
    if (!Object.hasOwn(catalog.environments, name) || !object(catalog.environments[name]))
      throw new TargetConfigurationError('The selected environment has no profile.');
    profile = catalog.environments[name];
    directory = path.dirname(profilesPath);
  } else {
    if (file !== undefined) throw new TargetConfigurationError('An environments file requires an environment name.');
    if (options.url === undefined) {
      if (options.storageState !== undefined) throw new TargetConfigurationError('Saved authentication state requires a target.');
      return undefined;
    }
    profile = { targetUrl: options.url, prefix: options.prefix, area: 'portal', storageState: options.storageState };
  }
  if (Object.keys(profile).some(key => !['targetUrl', 'prefix', 'area', 'storageState', 'workspaceName', 'refreshCredentialSha256'].includes(key)))
    throw new TargetConfigurationError('The target profile contains unsupported fields.');
  const url = targetUrl(profile.targetUrl);
  const prefix = text(profile.prefix, 'prefix');
  try { requireIdentifier(prefix, 'prefix'); }
  catch { throw new TargetConfigurationError('The profile prefix is not a supported UI identifier.'); }
  const area = profile.area ?? 'login';
  if (typeof area !== 'string' || !['login', 'portal', 'category'].includes(area))
    throw new TargetConfigurationError('area must be login, portal, or category.');
  const target: Target = { name: name ?? 'direct-url', targetUrl: url, prefix, area: area as Target['area'],
    configurationSha256: sha256(JSON.stringify(profile)) };
  if (profile.storageState !== undefined) {
    target.storageState = path.resolve(directory, text(profile.storageState, 'storageState'));
    const state = readJson(target.storageState, 'saved authentication state');
    if (!object(state) || !Array.isArray(state.cookies) || !Array.isArray(state.origins))
      throw new TargetConfigurationError('storageState must contain Playwright cookies and origins arrays.');
  }
  if (profile.workspaceName !== undefined) target.workspaceName = text(profile.workspaceName, 'workspaceName');
  if (profile.refreshCredentialSha256 !== undefined) {
    const hash = text(profile.refreshCredentialSha256, 'refreshCredentialSha256');
    if (!/^[a-fA-F0-9]{64}$/.test(hash)) throw new TargetConfigurationError('refreshCredentialSha256 must be a SHA-256 fingerprint.');
    target.refreshCredentialSha256 = hash.toLowerCase();
  }
  return target;
}

export function targetSummary(target: Target) {
  const url = new URL(target.targetUrl);
  return { environment: target.name, targetUrl: `${url.origin}${url.pathname}`, prefix: target.prefix, area: target.area,
    configurationSha256: target.configurationSha256,
    storageStateSha256: target.storageState ? sha256(readFileSync(target.storageState, 'utf8')) : null };
}

export function rejectEnvironmentForFixtures(env: NodeJS.ProcessEnv = process.env): void {
  if (env.E2E_ENVIRONMENT !== undefined || env.E2E_ENVIRONMENTS_FILE !== undefined)
    throw new TargetConfigurationError('Named targets use e2e:remote. Fixture and local audit suites use their isolated configuration.');
}
