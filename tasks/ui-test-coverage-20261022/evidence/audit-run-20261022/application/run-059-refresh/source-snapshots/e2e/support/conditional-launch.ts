import { readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import ts from 'typescript';
import { expect, type Page } from '@playwright/test';
import { localBase } from './local-app.js';

/** Mount the inspected, otherwise unused hook under the actual shell provider. */
export async function installConditionalLaunch(page: Page) {
  const hookPath = 'repos/ui/mfe-base/src/pages/Home/common/useParameters.ts';
  const utilityPath = 'repos/ui/mfe-base/src/pages/Home/common/util.ts';
  const hookSource = await readFile(hookPath, 'utf8');
  const utilitySource = await readFile(utilityPath, 'utf8');
  const sha256 = (bytes: string) => createHash('sha256').update(bytes).digest('hex');
  const utility = utilitySource.slice(utilitySource.indexOf('export const openTileUtil =')).replace('export const ', 'const ');
  const adapted = hookSource
    .replace(/import React from "react";/, '')
    .replace(/import \{ useContext \} from "\.\.\/\.\.\/\.\.\/hooks\/provider";/, 'const { useContext } = base.Provider;')
    .replace(/import \{ findTileConfig \} from "\.\.\/\.\.\/\.\.\/utils\/drawer";/, 'const { findTileConfig } = base.ChannelUtil;')
    .replace(/import \{ uuidv4, validateTile \} from "\.\.\/\.\.\/\.\.\/utils\/common";/, 'const { uuidv4, validateTile } = base.CommonUtil;')
    .replace(/import \{ Container \} from "\.\.\/\.\.\/\.\.\/hooks\/model\/workspaces";/, '')
    .replace(/import useDispatcher from "\.\.\/\.\.\/\.\.\/hooks\/dispathcer";/, 'const useDispatcher = base.Dispatcher.default;')
    .replace(/import useAnalytics from "\.\.\/\.\.\/\.\.\/analytics";/, 'const useAnalytics = base.Analytics.default;')
    .replace(/import \{ getHooksBase \} from "\.\.\/\.\.\/\.\.\/hooks\/HooksBase";/, 'const getHooksBase = base.Hooks.getHooks;')
    .replace(/import \{ openTileUtil \} from "\.\/util";/, utility)
    .replace('process.env.orgName', '"fm"')
    .replace('export default useParameters;', '');
  const javascript = ts.transpileModule(adapted, { compilerOptions: { target: ts.ScriptTarget.ES2020, module: ts.ModuleKind.None } }).outputText;
  if (/\bimport\s/.test(javascript)) throw new Error('The conditional hook retains an unresolved import.');
  const body = `System.register(['react','@fm/base'],function(exports){var React,base;return{setters:[function(v){React=v.default||v;},function(v){base=v;}],execute:function(){${javascript}\nexports('default',function ConditionalUrlLaunch(){useParameters();return React.createElement('section',{'data-testid':'conditional-launch-mounted'},'Conditional useParameters source integration');});}};});`;
  await page.route('**/importmap*.json', async route => {
    const response = await route.fetch(); const map = await response.json();
    await route.fulfill({ response, json: { ...map, imports: { ...map.imports,
      '@fm/test_container': `${localBase}/audit-fixtures/test-container.js`,
      '@fm/url-launch-fixture': `${localBase}/audit-fixtures/url-integration.js` } } });
  });
  await page.route('**/audit-fixtures/url-integration.js', route => route.fulfill({ status: 200,
    contentType: 'application/javascript', body }));
  return { hookPath, hookSource, hookSha256: sha256(hookSource), utilityPath,
    utilitySource, utilitySha256: sha256(utilitySource), generatedSystemJs: body, generatedSha256: sha256(body),
    compiler: `TypeScript ${ts.version}`, importAdapters: ['Actual base.Provider.useContext', 'Actual base.ChannelUtil.findTileConfig',
      'Actual base.CommonUtil.uuidv4 and validateTile', 'Actual base.Dispatcher.default', 'Actual base.Analytics.default',
      'Actual base.Hooks.getHooks for the delayed store read', 'Exact openTileUtil source'],
    limit: 'Production Home does not mount useParameters. This explicitly mounted source integration is conditional characterization.' };
}

export async function installFdc3Fixture(page: Page): Promise<void> {
  await page.addInitScript(() => {
    const target = window as unknown as { fin: unknown; fdc3: unknown; __auditFdc3: {
      listeners: Record<string, (context: unknown) => unknown>; deliveries: unknown[]; unsubscriptions: string[] } };
    target.__auditFdc3 = { listeners: {}, deliveries: [], unsubscriptions: [] };
    // The bundled legacy adapter eagerly calls desktop.main. Keep that native startup dormant.
    // Home uses the explicit window.fdc3 provider below for the tested listener.
    target.fin = { desktop: { main: () => undefined } };
    target.fdc3 = { addIntentListener: async (intent: string, callback: (context: unknown) => unknown) => {
      target.__auditFdc3.listeners[intent] = callback;
      return { unsubscribe: () => { delete target.__auditFdc3.listeners[intent]; target.__auditFdc3.unsubscriptions.push(intent); } };
    } };
  });
}

export async function deliverFdc3(page: Page, context: unknown): Promise<void> {
  await expect.poll(() => page.evaluate(() => Boolean((window as unknown as { __auditFdc3: { listeners: Record<string, unknown> } }).__auditFdc3.listeners['scb.ViewLaunch']))).toBe(true);
  await page.evaluate(context => {
    const fixture = (window as unknown as { __auditFdc3: {
      listeners: Record<string, (context: unknown) => void>; deliveries: unknown[] } }).__auditFdc3;
    fixture.deliveries.push({ intent: 'scb.ViewLaunch', context });
    fixture.listeners['scb.ViewLaunch'](context);
  }, context);
}
