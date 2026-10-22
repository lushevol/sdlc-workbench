import { expect, type Locator, type Page } from '@playwright/test';
import { sessionUi, uiContracts, type UiTargets } from '../catalog/ui-contracts.js';
import { expectActionable, expectUniqueVisible } from './target.js';

export class SessionTimeoutDialog {
  readonly dialog: Locator;
  readonly extendButton: Locator;
  readonly logoutButton: Locator;
  readonly targets: UiTargets;

  constructor(page: Page) {
    this.dialog = page.getByRole('dialog', { name: sessionUi.dialogName, exact: true });
    this.extendButton = this.dialog.getByRole('button', { name: sessionUi.extendButtonName, exact: true });
    this.logoutButton = this.dialog.getByRole('button', { name: sessionUi.logoutButtonName, exact: true });
    this.targets = {
      dialog: { contract: uiContracts.sessionDialog, locator: this.dialog },
      extendButton: { contract: uiContracts.sessionExtendButton, locator: this.extendButton },
      logoutButton: { contract: uiContracts.sessionLogoutButton, locator: this.logoutButton },
    };
  }

  async clickExtendButton(): Promise<void> {
    await expectActionable(this.targets.extendButton, this.dialog);
    await this.extendButton.click();
  }

  async clickLogoutButton(): Promise<void> {
    await expectActionable(this.targets.logoutButton, this.dialog);
    await this.logoutButton.click();
  }

  async expectVisible(): Promise<void> {
    await expectUniqueVisible(this.dialog);
    await expect(this.dialog).toHaveAccessibleDescription(sessionUi.description);
  }

  async expectClosed(): Promise<void> {
    await expect(this.dialog).toBeHidden();
  }

  async expectAbsent(): Promise<void> {
    await expect(this.dialog).toHaveCount(0);
  }
}
