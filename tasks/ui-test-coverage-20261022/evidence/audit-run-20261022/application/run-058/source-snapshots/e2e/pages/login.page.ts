import { expect, type Locator, type Page } from '@playwright/test';
import { createLoginContracts, loginUi, type UiTargets } from '../catalog/ui-contracts.js';
import { expectActionable, expectUniqueVisible } from '../components/target.js';

export class LoginPage {
  readonly root: Locator;
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly signInButton: Locator;
  readonly ssoLink: Locator;
  readonly targets: UiTargets;

  constructor(readonly page: Page, prefix: string) {
    const contracts = createLoginContracts(prefix);
    this.root = page.getByTestId(contracts.root.identity);
    this.usernameInput = this.root.getByPlaceholder(loginUi.usernamePlaceholder, { exact: true });
    this.passwordInput = this.root.getByPlaceholder(loginUi.passwordPlaceholder, { exact: true });
    this.signInButton = this.root.getByRole('button', { name: loginUi.signInButtonName, exact: true });
    this.ssoLink = this.root.getByRole('link', { name: loginUi.ssoLinkName, exact: true });
    this.targets = {
      root: { contract: contracts.root, locator: this.root },
      usernameInput: { contract: contracts.usernameInput, locator: this.usernameInput },
      passwordInput: { contract: contracts.passwordInput, locator: this.passwordInput },
      signInButton: { contract: contracts.signInButton, locator: this.signInButton },
      ssoLink: { contract: contracts.ssoLink, locator: this.ssoLink },
    };
  }

  async fillUsername(value: string): Promise<void> {
    await expectActionable(this.targets.usernameInput, this.root);
    await expect(this.usernameInput).toBeEditable();
    await this.usernameInput.fill(value);
  }

  async fillPassword(value: string): Promise<void> {
    await expectActionable(this.targets.passwordInput, this.root);
    await expect(this.passwordInput).toBeEditable();
    await this.passwordInput.fill(value);
  }

  async clickSignInButton(): Promise<void> {
    await expectActionable(this.targets.signInButton, this.root);
    await this.signInButton.click();
  }

  async clickSsoLink(): Promise<void> {
    await expectActionable(this.targets.ssoLink, this.root);
    await this.ssoLink.click();
  }

  async expectVisible(): Promise<void> {
    await expectUniqueVisible(this.root);
    await expectUniqueVisible(this.ssoLink);
  }

  async expectPasswordMasked(): Promise<void> {
    await expectUniqueVisible(this.passwordInput);
    await expect(this.passwordInput).toHaveAttribute('type', 'password');
  }

  async expectUsernameValue(value: string): Promise<void> {
    await expectUniqueVisible(this.usernameInput);
    await expect(this.usernameInput).toHaveValue(value);
  }

  async expectPasswordValue(value: string): Promise<void> {
    await expectUniqueVisible(this.passwordInput);
    await expect(this.passwordInput).toHaveValue(value);
  }
}
