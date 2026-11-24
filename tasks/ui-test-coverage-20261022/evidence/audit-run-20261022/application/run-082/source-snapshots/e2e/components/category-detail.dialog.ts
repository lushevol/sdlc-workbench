import { expect, type Locator } from '@playwright/test';
import { categoryUi, createCategoryDetailContracts, type UiTargets } from '../catalog/ui-contracts.js';
import { expectActionable, expectUniqueVisible } from './target.js';

export class CategoryDetailDialog {
  readonly dialog: Locator;
  readonly closeButton: Locator;
  readonly resetButton: Locator;
  readonly targets: UiTargets;

  constructor(table: Locator, mode: 'new' | 'edit' | 'verify' | 'deactivate', recordId: string) {
    const contracts = createCategoryDetailContracts(mode, recordId);
    this.dialog = table.getByRole('dialog').filter({
      has: table.page().getByText(contracts.dialog.identity, { exact: true }),
    });
    // The header also has a disabled "Close" chip. Target the enabled footer button explicitly.
    this.closeButton = this.dialog.getByRole('button', { name: categoryUi.closeButtonName, exact: true })
      .and(this.dialog.locator('button'));
    this.resetButton = this.dialog.getByRole('button', { name: categoryUi.resetButtonName, exact: true });
    this.targets = {
      dialog: { contract: contracts.dialog, locator: this.dialog },
      closeButton: { contract: contracts.closeButton, locator: this.closeButton },
      resetButton: { contract: contracts.resetButton, locator: this.resetButton },
    };
  }

  async clickCloseButton(): Promise<void> {
    await expectActionable(this.targets.closeButton, this.dialog);
    await this.closeButton.click();
  }

  async clickResetButton(): Promise<void> {
    await expectActionable(this.targets.resetButton, this.dialog);
    await this.resetButton.click();
  }

  async expectVisible(): Promise<void> {
    await expectUniqueVisible(this.dialog);
  }

  async expectClosed(): Promise<void> {
    await expect(this.dialog).toBeHidden();
  }
}
