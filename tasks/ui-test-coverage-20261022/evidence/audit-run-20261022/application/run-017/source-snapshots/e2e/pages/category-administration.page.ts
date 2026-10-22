import { type Locator, type Page } from '@playwright/test';
import { categoryUi, createCategoryContracts, type UiTargets } from '../catalog/ui-contracts.js';
import { CategoryRecordActions } from '../components/category-record-actions.component.js';
import { CategoryDetailDialog } from '../components/category-detail.dialog.js';
import { expectActionable, expectUniqueVisible } from '../components/target.js';

export class CategoryAdministrationPage {
  readonly root: Locator;
  readonly createNewButton: Locator;
  readonly table: Locator;
  readonly grid: Locator;
  readonly categoryLabelHeader: Locator;
  readonly ownerHeader: Locator;
  readonly verifiedHeader: Locator;
  readonly targets: UiTargets;

  constructor(readonly page: Page, prefix: string) {
    const contracts = createCategoryContracts(prefix);
    this.root = page.getByTestId(contracts.root.identity);
    this.createNewButton = this.root.getByRole('button', { name: categoryUi.createNewButtonName, exact: true });
    this.table = this.root.getByTestId(contracts.table.identity);
    this.grid = this.table.getByRole('grid');
    this.categoryLabelHeader = this.grid.getByRole('columnheader', { name: categoryUi.categoryLabelHeader, exact: true });
    this.ownerHeader = this.grid.getByRole('columnheader', { name: categoryUi.ownerHeader, exact: true });
    this.verifiedHeader = this.grid.getByRole('columnheader', { name: categoryUi.verifiedHeader, exact: true });
    this.targets = {
      root: { contract: contracts.root, locator: this.root },
      createNewButton: { contract: contracts.createNewButton, locator: this.createNewButton },
      table: { contract: contracts.table, locator: this.table },
      grid: { contract: contracts.grid, locator: this.grid },
      categoryLabelHeader: { contract: contracts.categoryLabelHeader, locator: this.categoryLabelHeader },
      ownerHeader: { contract: contracts.ownerHeader, locator: this.ownerHeader },
      verifiedHeader: { contract: contracts.verifiedHeader, locator: this.verifiedHeader },
    };
  }

  recordActions(recordId: string): CategoryRecordActions {
    return new CategoryRecordActions(this.grid, recordId);
  }

  detailDialog(mode: 'new' | 'edit' | 'verify' | 'deactivate', recordId: string): CategoryDetailDialog {
    return new CategoryDetailDialog(this.table, mode, recordId);
  }

  async clickCreateNewCategoryButton(): Promise<void> {
    await expectActionable(this.targets.createNewButton, this.root);
    await this.createNewButton.click();
  }

  async expectVisible(): Promise<void> {
    await expectUniqueVisible(this.root);
    await expectUniqueVisible(this.grid);
  }

  async expectCoreColumnHeaders(): Promise<void> {
    await expectUniqueVisible(this.grid);
    for (const header of [this.categoryLabelHeader, this.ownerHeader, this.verifiedHeader]) {
      await expectUniqueVisible(header);
    }
  }
}
