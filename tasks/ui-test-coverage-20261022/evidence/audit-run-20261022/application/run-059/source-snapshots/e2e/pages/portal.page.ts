import { expect, type Locator, type Page } from '@playwright/test';
import { createPortalContracts, createWorkspaceNameContract, portalUi, type UiTargets } from '../catalog/ui-contracts.js';
import { SessionTimeoutDialog } from '../components/session-timeout.dialog.js';
import { WorkspaceTab } from '../components/workspace-tab.component.js';
import { expectActionable, expectUniqueVisible } from '../components/target.js';

export class PortalPage {
  readonly sessionTimeoutDialog: SessionTimeoutDialog;
  readonly root: Locator;
  readonly workspaceList: Locator;
  readonly addWorkspaceButton: Locator;
  readonly themeCheckbox: Locator;
  readonly avatarButton: Locator;
  readonly avatarMenu: Locator;
  readonly profileMenuItem: Locator;
  readonly logoutMenuItem: Locator;
  readonly targets: UiTargets;

  constructor(readonly page: Page, prefix: string) {
    const contracts = createPortalContracts(prefix);
    this.sessionTimeoutDialog = new SessionTimeoutDialog(page);
    this.root = page.getByTestId(contracts.root.identity);
    this.workspaceList = this.root.getByRole('tablist', { name: portalUi.workspaceListName, exact: true });
    this.addWorkspaceButton = this.workspaceList.getByRole('button', { name: portalUi.addWorkspaceButtonName, exact: true });
    this.themeCheckbox = this.root.getByRole('checkbox', { name: portalUi.themeCheckboxName, exact: true });
    this.avatarButton = this.root.getByTestId(contracts.avatarButton.identity);
    this.avatarMenu = page.locator('[id="menu-appbar-avatar"]');
    this.profileMenuItem = this.avatarMenu.getByTestId(contracts.profileMenuItem.identity);
    this.logoutMenuItem = this.avatarMenu.getByRole('menuitem', { name: portalUi.logoutMenuItemName, exact: true });
    this.targets = {
      root: { contract: contracts.root, locator: this.root },
      workspaceList: { contract: contracts.workspaceList, locator: this.workspaceList },
      addWorkspaceButton: { contract: contracts.addWorkspaceButton, locator: this.addWorkspaceButton },
      themeCheckbox: { contract: contracts.themeCheckbox, locator: this.themeCheckbox },
      avatarButton: { contract: contracts.avatarButton, locator: this.avatarButton },
      avatarMenu: { contract: contracts.avatarMenu, locator: this.avatarMenu },
      profileMenuItem: { contract: contracts.profileMenuItem, locator: this.profileMenuItem },
      logoutMenuItem: { contract: contracts.logoutMenuItem, locator: this.logoutMenuItem },
    };
  }

  workspace(workspaceId: string): WorkspaceTab {
    return new WorkspaceTab(this.workspaceList, workspaceId);
  }

  async clickAddWorkspaceButton(): Promise<void> {
    await expectActionable(this.targets.addWorkspaceButton, this.workspaceList);
    await this.addWorkspaceButton.click();
  }

  async setThemeLight(checked: boolean): Promise<void> {
    await expectActionable(this.targets.themeCheckbox, this.root);
    await this.themeCheckbox.setChecked(checked);
  }

  async clickAvatarButton(): Promise<void> {
    await expectActionable(this.targets.avatarButton, this.root);
    await this.avatarButton.click();
  }

  async clickProfileMenuItem(): Promise<void> {
    await expectActionable(this.targets.profileMenuItem, this.avatarMenu);
    await this.profileMenuItem.click();
  }

  async clickLogoutMenuItem(): Promise<void> {
    await expectActionable(this.targets.logoutMenuItem, this.avatarMenu);
    await this.logoutMenuItem.click();
  }

  async expectVisible(): Promise<void> {
    await expectUniqueVisible(this.root);
    await expectUniqueVisible(this.workspaceList);
  }

  async expectWorkspaceTabVisible(name: string): Promise<void> {
    const contract = createWorkspaceNameContract(name);
    await expectUniqueVisible(this.workspaceList);
    await expect.poll(async () => {
      let matchingVisibleTabs = 0;
      for (const tab of await this.workspaceList.getByRole('tab').all()) {
        const input = tab.getByRole('textbox', { name: portalUi.workspaceName, exact: true });
        if (await input.count() === 1 && await input.inputValue() === contract.identity && await tab.isVisible()) {
          matchingVisibleTabs += 1;
        }
      }
      return matchingVisibleTabs;
    }, { message: `One visible workspace tab must have the exact name ${JSON.stringify(name)}.` }).toBe(1);
  }

  async expectThemeLight(checked: boolean): Promise<void> {
    await expectUniqueVisible(this.themeCheckbox);
    await expect(this.themeCheckbox).toBeChecked({ checked });
  }

  async expectAvatarMenuVisible(): Promise<void> {
    await expectUniqueVisible(this.avatarMenu);
    await expectUniqueVisible(this.profileMenuItem);
    await expectUniqueVisible(this.logoutMenuItem);
  }
}
