// Local test substitute. This does not implement the proprietary toolkit.
if (!customElements.get('sc-button')) {
  customElements.define('sc-button', class extends HTMLElement {});
}
