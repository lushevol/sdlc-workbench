// Local test substitute. This does not implement the proprietary toolkit.
if (!customElements.get('sc-icon-card')) {
  customElements.define('sc-icon-card', class extends HTMLElement {});
}
