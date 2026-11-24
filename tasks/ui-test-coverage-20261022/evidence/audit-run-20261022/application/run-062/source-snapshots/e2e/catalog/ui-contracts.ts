import type { Locator } from '@playwright/test';

export const mfeBaseRevision = '6e34da31961eb6bce4ef6c3daea83a2f7bd48e85';

export interface SourceEvidence {
  readonly repositoryId: 'mfe-base';
  readonly revision: string;
  readonly path: string;
  readonly lines: readonly [number, number];
}

export interface UiContract {
  readonly id: string;
  readonly area: 'portal' | 'login' | 'category';
  readonly componentType: string;
  readonly identity: string;
  readonly identityMethod: 'role-name' | 'placeholder' | 'test-id' | 'id' | 'role' | 'exact-title-descendant' | 'input-value';
  readonly scope: string;
  readonly sources: readonly SourceEvidence[];
  readonly grounding: 'source-inspected';
  readonly runtimeVerification: 'unverified';
}

export interface UiTarget {
  readonly contract: UiContract;
  readonly locator: Locator;
}

export type UiTargets = Readonly<Record<string, UiTarget>>;

const source = (path: string, start: number, end: number): SourceEvidence => ({
  repositoryId: 'mfe-base', revision: mfeBaseRevision, path, lines: [start, end],
});

function contract(
  id: string,
  area: UiContract['area'],
  componentType: string,
  identity: string,
  identityMethod: UiContract['identityMethod'],
  scope: string,
  sources: readonly SourceEvidence[],
): UiContract {
  return { id, area, componentType, identity, identityMethod, scope, sources,
    grounding: 'source-inspected', runtimeVerification: 'unverified' };
}

export function requireIdentifier(value: string, name: string): string {
  if (typeof value !== 'string' || value.trim().length === 0) {
    throw new Error(`${name} must be a nonempty string.`);
  }
  return value;
}

export const sessionUi = {
  dialogName: 'Your session has been expired',
  description: 'Do you want to logout or extend the session?',
  extendButtonName: 'Extend',
  logoutButtonName: 'Logout',
} as const;

export const loginUi = {
  usernamePlaceholder: 'Enter Username',
  passwordPlaceholder: 'Enter Password',
  signInButtonName: 'Sign In',
  ssoLinkName: 'Sign In With SSO',
} as const;

export const portalUi = {
  workspaceListName: 'workspaces',
  addWorkspaceButtonName: 'Add Workspace',
  workspaceName: 'Workspace Name',
  refreshButtonName: 'refresh',
  deleteButtonName: 'delete',
  themeCheckboxName: 'Theme Switch',
  avatarMenuId: 'menu-appbar-avatar',
  logoutMenuItemName: 'Logout',
} as const;

export const categoryUi = {
  createNewButtonName: 'Create New Category',
  closeButtonName: 'Close',
  resetButtonName: 'Reset',
  categoryLabelHeader: 'Category Label',
  ownerHeader: 'Owner',
  verifiedHeader: 'Verified?',
} as const;

const timeoutSource = source('src/components/Timeout/index.tsx', 16, 46);
const loginSource = source('src/pages/Login/index.tsx', 39, 133);
const homeSource = source('src/pages/Home/index.tsx', 56, 108);
const avatarSource = source('src/components/Avatar/index.tsx', 33, 78);
const categorySource = source('src/admin/Category/index.tsx', 14, 27);
const tableSource = source('src/components/Table/index.tsx', 42, 102);

export const uiContracts = {
  sessionDialog: contract('session.dialog', 'portal', 'dialog', sessionUi.dialogName,
    'role-name', 'page', [timeoutSource]),
  sessionExtendButton: contract('session.extend-button', 'portal', 'button', sessionUi.extendButtonName,
    'role-name', 'session.dialog', [timeoutSource]),
  sessionLogoutButton: contract('session.logout-button', 'portal', 'button', sessionUi.logoutButtonName,
    'role-name', 'session.dialog', [timeoutSource]),
} as const;

export function createLoginContracts(prefix: string) {
  requireIdentifier(prefix, 'MFE_APP_PREFIX_STYLE');
  return {
    root: contract('login.root', 'login', 'region', `${prefix}_login`, 'test-id', 'page', [
      loginSource, source('src/pages/Login/common/style.ts', 1, 4),
    ]),
    usernameInput: contract('login.username', 'login', 'textbox', loginUi.usernamePlaceholder,
      'placeholder', 'login.root', [source('src/pages/Login/index.tsx', 53, 74)]),
    passwordInput: contract('login.password', 'login', 'password input', loginUi.passwordPlaceholder,
      'placeholder', 'login.root', [source('src/pages/Login/index.tsx', 80, 102)]),
    signInButton: contract('login.sign-in-button', 'login', 'button', loginUi.signInButtonName,
      'role-name', 'login.root', [source('src/pages/Login/index.tsx', 104, 114)]),
    ssoLink: contract('login.sso-link', 'login', 'link', loginUi.ssoLinkName,
      'role-name', 'login.root', [source('src/pages/Login/index.tsx', 122, 133),
        source('src/components/LoadingButton/index.tsx', 1, 28)]),
  } as const;
}

export function createPortalContracts(prefix: string) {
  requireIdentifier(prefix, 'MFE_APP_PREFIX_STYLE');
  return {
    root: contract('portal.root', 'portal', 'region', `${prefix}_home`, 'test-id', 'page', [
      homeSource, source('src/pages/Home/common/style.ts', 1, 2),
    ]),
    workspaceList: contract('portal.workspaces', 'portal', 'tablist', portalUi.workspaceListName,
      'role-name', 'portal.root', [homeSource]),
    addWorkspaceButton: contract('portal.add-workspace-button', 'portal', 'button', portalUi.addWorkspaceButtonName,
      'role-name', 'portal.workspaces', [homeSource]),
    themeCheckbox: contract('portal.theme-checkbox', 'portal', 'checkbox', portalUi.themeCheckboxName,
      'role-name', 'portal.root', [source('src/components/Switch/index.tsx', 20, 26),
        source('src/components/Switch/common/style.ts', 1, 2)]),
    avatarButton: contract('portal.avatar-button', 'portal', 'button', `${prefix}_avatar_IconButton`,
      'test-id', 'portal.root', [avatarSource, source('src/components/Avatar/common/style.ts', 1, 4)]),
    avatarMenu: contract('portal.avatar-menu', 'portal', 'menu container', portalUi.avatarMenuId,
      'id', 'page', [avatarSource]),
    profileMenuItem: contract('portal.profile-menu-item', 'portal', 'menuitem', `${prefix}_avatar_Profile`,
      'test-id', 'portal.avatar-menu', [avatarSource]),
    logoutMenuItem: contract('portal.logout-menu-item', 'portal', 'menuitem', portalUi.logoutMenuItemName,
      'role-name', 'portal.avatar-menu', [avatarSource]),
  } as const;
}

export function createWorkspaceContracts(workspaceId: string) {
  requireIdentifier(workspaceId, 'workspaceId');
  const scope = `portal.workspace.${workspaceId}`;
  const workspaceSource = source('src/components/TabItem/index.tsx', 39, 76);
  return {
    tab: contract(scope, 'portal', 'tab', `workspaces-tab-${workspaceId}`,
      'test-id', 'portal.workspaces', [source('src/pages/Home/index.tsx', 72, 94),
        source('src/components/TabPanel/index.tsx', 42, 46)]),
    nameInput: contract(`${scope}.name`, 'portal', 'textbox', portalUi.workspaceName,
      'role-name', scope, [workspaceSource]),
    refreshButton: contract(`${scope}.refresh`, 'portal', 'button', portalUi.refreshButtonName,
      'role-name', scope, [workspaceSource]),
    deleteButton: contract(`${scope}.delete`, 'portal', 'button', portalUi.deleteButtonName,
      'role-name', scope, [workspaceSource]),
  } as const;
}

export function createWorkspaceNameContract(name: string): UiContract {
  requireIdentifier(name, 'workspaceName');
  return contract(`portal.workspace-name.${name}`, 'portal', 'tab', name, 'input-value', 'portal.workspaces', [
    source('src/pages/Home/index.tsx', 72, 94), source('src/components/TabItem/index.tsx', 39, 52),
  ]);
}

export function createCategoryContracts(prefix: string) {
  requireIdentifier(prefix, 'MFE_APP_PREFIX_STYLE');
  return {
    root: contract('category.root', 'category', 'region', `${prefix}_category`, 'test-id', 'page', [
      categorySource, source('src/admin/Category/common/style.ts', 1, 4),
    ]),
    createNewButton: contract('category.create-new-button', 'category', 'button', categoryUi.createNewButtonName,
      'role-name', 'category.root', [categorySource, source('src/admin/common/Main/index.tsx', 24, 33)]),
    table: contract('category.table', 'category', 'table container', `${prefix}_simple_table`,
      'test-id', 'category.root', [tableSource, source('src/components/Table/common/style.ts', 1, 4)]),
    grid: contract('category.grid', 'category', 'grid', 'grid', 'role', 'category.table', [tableSource]),
    categoryLabelHeader: contract('category.label-header', 'category', 'columnheader', categoryUi.categoryLabelHeader,
      'role-name', 'category.grid', [source('src/admin/Category/common/useController.tsx', 79, 84)]),
    ownerHeader: contract('category.owner-header', 'category', 'columnheader', categoryUi.ownerHeader,
      'role-name', 'category.grid', [source('src/admin/Category/common/useController.tsx', 85, 90)]),
    verifiedHeader: contract('category.verified-header', 'category', 'columnheader', categoryUi.verifiedHeader,
      'role-name', 'category.grid', [source('src/admin/Category/common/useController.tsx', 91, 99)]),
  } as const;
}

export function createCategoryRecordContracts(recordId: string) {
  requireIdentifier(recordId, 'recordId');
  const actionSource = source('src/admin/common/Actions/index.tsx', 12, 64);
  const scope = 'category.grid';
  return {
    editMenuItem: contract(`category.record.${recordId}.edit`, 'category', 'menuitem', `edit-${recordId}`,
      'test-id', scope, [actionSource, source('src/admin/Category/common/useController.tsx', 47, 53)]),
    auditMenuItem: contract(`category.record.${recordId}.audit`, 'category', 'menuitem', `audit-${recordId}`,
      'test-id', scope, [actionSource, source('src/admin/Category/common/useController.tsx', 47, 53)]),
  } as const;
}

export function createCategoryDetailContracts(mode: 'new' | 'edit' | 'verify' | 'deactivate', recordId: string) {
  requireIdentifier(recordId, 'recordId');
  const id = `category.detail.${mode}.${recordId}`;
  return {
    dialog: contract(id, 'category', 'dialog', `${mode} ID: ${recordId}`, 'exact-title-descendant', 'category.table', [
      source('src/components/Table/index.tsx', 67, 78), source('src/components/TableDetail/index.tsx', 33, 46),
      source('src/components/Dialog/index.tsx', 61, 99),
    ]),
    closeButton: contract(`${id}.close`, 'category', 'button', categoryUi.closeButtonName,
      'role-name', id, [source('src/components/Table/index.tsx', 96, 102),
        source('src/components/Dialog/common/DialogTitle.tsx', 67, 80)]),
    resetButton: contract(`${id}.reset`, 'category', 'button', categoryUi.resetButtonName,
      'role-name', id, [source('src/components/Table/index.tsx', 89, 95)]),
  } as const;
}
