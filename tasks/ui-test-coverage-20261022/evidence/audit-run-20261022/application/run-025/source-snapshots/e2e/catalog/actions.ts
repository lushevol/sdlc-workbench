import type { Page } from '@playwright/test';
import { PortalPage } from '../pages/portal.page.js';
import { LoginPage } from '../pages/login.page.js';
import { CategoryAdministrationPage } from '../pages/category-administration.page.js';
import { createCategoryContracts, createPortalContracts, requireIdentifier, uiContracts,
  type UiTarget, type UiContract } from './ui-contracts.js';
import { inspectTarget } from '../components/target.js';

export type Area = UiContract['area'];
export function createPom(page: Page, prefix: string) {
  return { portal: new PortalPage(page, prefix), login: new LoginPage(page, prefix),
    category: new CategoryAdministrationPage(page, prefix) };
}
export type Pom = ReturnType<typeof createPom>;
export type Action = {
  id: string;
  description: string;
  businessIntent: string;
  area: Area;
  target: UiTarget;
  implementation: { path: string; method: string };
  preconditions: string[];
  expectedObservations: string[];
  risk: 'ui-navigation' | 'local-preference' | 'session-state-change';
  verification: 'source-inspected-runtime-unverified';
  execute(): Promise<unknown>;
};

export type ActionDescription = Omit<Action, 'target' | 'execute'> & { target: UiContract };
type ActionMetadata = Omit<Action, 'target' | 'execute' | 'verification'>;
type ActionDefinition = ActionMetadata & {
  describeTarget(prefix: string): UiContract;
  resolveTarget(pom: Pom): UiTarget;
  execute(pom: Pom): Promise<unknown>;
};

const portalContract = (key: keyof ReturnType<typeof createPortalContracts>) =>
  (prefix: string): UiContract => createPortalContracts(prefix)[key];
const categoryContract = (key: keyof ReturnType<typeof createCategoryContracts>) =>
  (prefix: string): UiContract => createCategoryContracts(prefix)[key];

// Descriptions and bound operations share these definitions. Contracts own all UI identity metadata.
const definitions: readonly ActionDefinition[] = [
    { id: 'session.extend', description: 'Click Extend in the expiration dialog.',
      businessIntent: 'Request continuation of the current authenticated session.', area: 'portal',
      describeTarget: () => uiContracts.sessionExtendButton,
      resolveTarget: pom => pom.portal.sessionTimeoutDialog.targets.extendButton!,
      implementation: { path: 'e2e/components/session-timeout.dialog.ts', method: 'SessionTimeoutDialog.clickExtendButton' },
      preconditions: ['The authenticated expiration dialog is visible.', 'Exactly one enabled Extend button exists.'],
      expectedObservations: ['The click completes. Authentication remains unverified until the session-extension flow runs.'],
      risk: 'session-state-change', async execute(pom) {
        await pom.portal.sessionTimeoutDialog.clickExtendButton(); return { clickCompleted: true, sessionValid: null };
      } },
    { id: 'session.logout', description: 'Click Logout in the expiration dialog.',
      businessIntent: 'Request sign-out from the current portal session.', area: 'portal',
      describeTarget: () => uiContracts.sessionLogoutButton,
      resolveTarget: pom => pom.portal.sessionTimeoutDialog.targets.logoutButton!,
      implementation: { path: 'e2e/components/session-timeout.dialog.ts', method: 'SessionTimeoutDialog.clickLogoutButton' },
      preconditions: ['The expiration dialog and one enabled Logout button are visible.'],
      expectedObservations: ['The click completes. Server revocation remains unverified.'], risk: 'session-state-change',
      async execute(pom) {
        await pom.portal.sessionTimeoutDialog.clickLogoutButton(); return { clickCompleted: true, sessionRevoked: null };
      } },
    { id: 'portal.avatar.open', description: 'Open the portal user menu.',
      businessIntent: 'Inspect the available user menu operations.', area: 'portal',
      describeTarget: portalContract('avatarButton'), resolveTarget: pom => pom.portal.targets.avatarButton!,
      implementation: { path: 'e2e/pages/portal.page.ts', method: 'PortalPage.clickAvatarButton' },
      preconditions: ['The portal header and one enabled avatar button are visible.'],
      expectedObservations: ['The portal avatar menu is visible.'], risk: 'ui-navigation',
      async execute(pom) {
        await pom.portal.clickAvatarButton(); await pom.portal.expectAvatarMenuVisible(); return { avatarMenuVisible: true };
      } },
    { id: 'portal.profile.open', description: 'Click the Profile menu item.',
      businessIntent: 'Inspect the current user profile.', area: 'portal',
      describeTarget: portalContract('profileMenuItem'), resolveTarget: pom => pom.portal.targets.profileMenuItem!,
      implementation: { path: 'e2e/pages/portal.page.ts', method: 'PortalPage.clickProfileMenuItem' },
      preconditions: ['The avatar menu and one enabled Profile menu item are visible.'],
      expectedObservations: ['The click completes. Profile contents require a separate assertion.'], risk: 'ui-navigation',
      async execute(pom) { await pom.portal.clickProfileMenuItem(); return { clickCompleted: true }; } },
    ...[true, false].map((light): ActionDefinition => ({ id: light ? 'portal.theme.light' : 'portal.theme.dark',
      description: `Set the portal theme to ${light ? 'light' : 'dark'}.`,
      businessIntent: 'Select the portal appearance.', area: 'portal',
      describeTarget: portalContract('themeCheckbox'), resolveTarget: pom => pom.portal.targets.themeCheckbox!,
      implementation: { path: 'e2e/pages/portal.page.ts', method: 'PortalPage.setThemeLight' },
      preconditions: ['One enabled Theme Switch checkbox is visible.'],
      expectedObservations: [`The Theme Switch checkbox is ${light ? 'checked' : 'unchecked'}.`], risk: 'local-preference',
      async execute(pom) {
        await pom.portal.setThemeLight(light); await pom.portal.expectThemeLight(light); return { themeCheckboxChecked: light };
      } })),
    { id: 'category.create.open', description: 'Open the Create New Category form.',
      businessIntent: 'Inspect the form for a new Category record.', area: 'category',
      describeTarget: categoryContract('createNewButton'), resolveTarget: pom => pom.category.targets.createNewButton!,
      implementation: { path: 'e2e/pages/category-administration.page.ts', method: 'CategoryAdministrationPage.clickCreateNewCategoryButton' },
      preconditions: ['The Category administration area is visible.', 'The user can access Create New Category.'],
      expectedObservations: ['The click completes. No record submission occurs.'], risk: 'ui-navigation',
      async execute(pom) { await pom.category.clickCreateNewCategoryButton(); return { clickCompleted: true, recordCreationVerified: null }; } },
];

function metadata(definition: ActionDefinition): Omit<Action, 'target' | 'execute'> {
  const { describeTarget, resolveTarget, execute, ...description } = definition;
  return { ...description, verification: 'source-inspected-runtime-unverified' };
}

export function describeActions(prefix: string): ActionDescription[] {
  requireIdentifier(prefix, 'MFE_APP_PREFIX_STYLE');
  return definitions.map(definition => ({ ...metadata(definition), target: definition.describeTarget(prefix) }));
}

// Each entry binds a real function. Method strings describe it; they never dispatch code.
export function createActions(pom: Pom): ReadonlyMap<string, Action> {
  return new Map(definitions.map(definition => [definition.id, {
    ...metadata(definition), target: definition.resolveTarget(pom), execute: () => definition.execute(pom),
  }]));
}

export function targetsForArea(pom: Pom, area: Area): UiTarget[] {
  const targets = Object.values(pom[area].targets);
  return area === 'portal' ? [...targets, ...Object.values(pom.portal.sessionTimeoutDialog.targets)] : targets;
}

export async function executeAction(actions: ReadonlyMap<string, Action>, id: string, allowSessionChange: boolean) {
  const action = actions.get(id);
  if (!action) throw new Error(`Unknown action: ${id}`);
  if (action.risk === 'session-state-change' && !allowSessionChange) throw new Error('Session actions require --allow-session-change.');
  const inspection = await inspectTarget(action.target);
  if (!inspection.available) return { action: id, status: 'failed', target: inspection,
    observations: { clickCompleted: false, sessionValid: null } };
  const observations = await action.execute();
  return { action: id, status: 'passed', target: inspection.contract, observations,
    verificationScope: 'Only the named UI observations were asserted.' };
}
