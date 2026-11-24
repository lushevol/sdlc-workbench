import { expect, type Locator } from '@playwright/test';
import { createWorkspaceContracts, portalUi, type UiTargets } from '../catalog/ui-contracts.js';
import { expectActionable, expectUniqueVisible } from './target.js';

export class WorkspaceTab {
  readonly tab: Locator;
  readonly nameInput: Locator;
  readonly refreshButton: Locator;
  readonly deleteButton: Locator;
  readonly targets: UiTargets;

  constructor(private readonly tablist: Locator, readonly workspaceId: string) {
    const contracts = createWorkspaceContracts(workspaceId);
    this.tab = tablist.getByTestId(contracts.tab.identity);
    this.nameInput = this.tab.getByRole('textbox', { name: portalUi.workspaceName, exact: true });
    this.refreshButton = this.tab.getByRole('button', { name: portalUi.refreshButtonName, exact: true });
    this.deleteButton = this.tab.getByRole('button', { name: portalUi.deleteButtonName, exact: true });
    this.targets = {
      tab: { contract: contracts.tab, locator: this.tab },
      nameInput: { contract: contracts.nameInput, locator: this.nameInput },
      refreshButton: { contract: contracts.refreshButton, locator: this.refreshButton },
      deleteButton: { contract: contracts.deleteButton, locator: this.deleteButton },
    };
  }

  async clickTab(): Promise<void> {
    await expectActionable(this.targets.tab, this.tablist);
    await this.tab.click();
  }

  async fillName(value: string): Promise<void> {
    await expectActionable(this.targets.nameInput, this.tab);
    await expect(this.nameInput).toBeEditable();
    await this.nameInput.fill(value);
  }

  async clickRefreshButton(): Promise<void> {
    await expectActionable(this.targets.refreshButton, this.tab);
    await this.refreshButton.click();
  }

  async clickDeleteButton(): Promise<void> {
    await expectActionable(this.targets.deleteButton, this.tab);
    await this.deleteButton.click();
  }

  async expectName(value: string): Promise<void> {
    await expectUniqueVisible(this.nameInput);
    await expect(this.nameInput).toHaveValue(value);
  }

  async expectSelected(): Promise<void> {
    await expectUniqueVisible(this.tab);
    await expect(this.tab).toHaveAttribute('aria-selected', 'true');
  }

  async expectTabAbsent(): Promise<void> {
    await expectUniqueVisible(this.tablist);
    await expect(this.tab).toHaveCount(0);
  }
}
