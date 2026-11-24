import { expect, test } from '@playwright/test';
import { CashflowDialogs, CashflowSsiSection } from '../components/cashflow/dialogs.js';

const base = '/cashflow_blotter_cn/cashflow_cn';
const title = (name: string) => `<header class="MuiDialogTitle-root"><div class="MuiGrid-item">${name}</div>
  <div class="MuiGrid-item"><span role="button" data-testid="test_Dialog-close" onclick="this.closest('[role=dialog]').remove()">Close</span></div></header>`;

test('CF-POM-010: Given a disabled footer Close, When closing a comment dialog, Then the header control closes its own dialog', async ({ page }) => {
  await page.setContent(`<section role="dialog">${title('Hold - 2 cashflows selected')}
    <textarea data-testid="addCommentText"></textarea><button disabled>Close</button>
    <button data-testid="${base}/blotter_menu_action/Hold/submit_btn" onclick="this.dataset.clicked='true'">Submit</button></section>
    <section role="dialog">${title('Manual Settle')}<textarea data-testid="addCommentText">unchanged</textarea></section>`);
  const dialogs = new CashflowDialogs(page);
  const hold = dialogs.comment('Hold');
  await hold.fill(hold.commentInput, 'Synthetic hold reason');
  await hold.click(hold.submitButton);
  await expect(hold.submitButton).toHaveAttribute('data-clicked', 'true');
  await expect(dialogs.comment('Manual Settle').commentInput).toHaveValue('unchanged');
  await hold.close();
  await hold.expectClosed();
  await dialogs.comment('Manual Settle').expectVisible();
});

test('CF-POM-011: Given duplicate generated SSI fields, When editing a Vostro section, Then the Nostro input remains unchanged', async ({ page }) => {
  await page.setContent(`<section id="vostro"><input data-testid="settlementAccount" value="old-vostro"></section>
    <section id="nostro"><input data-testid="settlementAccount" value="old-nostro"></section>`);
  const vostro = new CashflowSsiSection(page, page.locator('#vostro'), 'vostro');
  const nostro = new CashflowSsiSection(page, page.locator('#nostro'), 'nostro');
  await vostro.fill(vostro.formField('settlementAccount'), 'synthetic-account');
  await expect(vostro.formField('settlementAccount')).toHaveValue('synthetic-account');
  await expect(nostro.formField('settlementAccount')).toHaveValue('old-nostro');
});

test('CF-POM-012: Given indexed splitting rows, When editing one child amount, Then adjacent amounts remain unchanged', async ({ page }) => {
  await page.setContent(`<section role="dialog">${title('Split Cashflow Preview')}
    <div data-testid="splittingAmount_Input_0"><input value="20"></div>
    <div data-testid="splittingAmount_Input_1"><input value="30"></div>
    <button data-testid="lookUpSSIBtn_1" onclick="this.dataset.clicked='true'">Look Up SSI</button></section>`);
  const split = new CashflowDialogs(page).splitting();
  await split.fill(split.amountInput(1), '35.50');
  await split.click(split.lookupSsiButton(1));
  await expect(split.amountInput(0)).toHaveValue('20');
  await expect(split.amountInput(1)).toHaveValue('35.50');
  await expect(split.lookupSsiButton(1)).toHaveAttribute('data-clicked', 'true');
  expect(() => split.amountInput(-1)).toThrow('nonnegative row index');
});

test('CF-POM-013: Given the splitting affirmation submit literal, When submitting, Then the source-defined button receives the click', async ({ page }) => {
  await page.setContent(`<section role="dialog">${title('Update Affirmation')}
    <input data-testid="affirmedName"><input data-testid="affirmedEmail"><input data-testid="affirmedAt">
    <button data-testid="CASHFLOW_BLOTTER_SPLITTING_DIALOG_NET_SUBMIT_BTN" onclick="this.dataset.clicked='true'">Submit</button></section>`);
  const affirmation = new CashflowDialogs(page).previewAffirmation('splitting');
  await affirmation.fill(affirmation.affirmation.nameInput, 'Synthetic actor');
  await affirmation.fill(affirmation.affirmation.contactInput, 'actor@example.invalid');
  await affirmation.click(affirmation.submitButton);
  await expect(affirmation.affirmation.nameInput).toHaveValue('Synthetic actor');
  await expect(affirmation.submitButton).toHaveAttribute('data-clicked', 'true');
});

test('CF-POM-016: Given a portalled export dialog, When choosing XLSX, Then its filename and format controls hold the selected values', async ({ page }) => {
  await page.setContent(`<section role="dialog">${title('Export File')}
    <span data-testid="exportFileName"><input></span><span data-testid="exportFileFormat">
    <input role="combobox" aria-controls="export-options"></span>
    <button data-testid="${base}/blotter/export_file_confirm_btn" onclick="this.dataset.clicked='true'">Export</button></section>
    <div id="export-options" role="listbox"><div role="option" data-testid="excel" onclick="this.dataset.selected='true'">XLSX</div></div>`);
  const exportFile = new CashflowDialogs(page).exportFile();
  await exportFile.fill(exportFile.fileNameInput, 'synthetic-cashflows');
  await exportFile.selectFormat('XLSX');
  await exportFile.click(exportFile.exportButton);
  await expect(exportFile.fileNameInput).toHaveValue('synthetic-cashflows');
  await expect(page.getByTestId('excel')).toHaveAttribute('data-selected', 'true');
  await expect(exportFile.exportButton).toHaveAttribute('data-clicked', 'true');
  await exportFile.close();
  await exportFile.expectClosed();
});
