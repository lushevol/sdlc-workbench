# Goal

1. Ratan can raise intent to open trade ticket in blade
2. (Dual interoperation) Blade can open cashflow blotter in RATAN to query cashflow list by Trade_Id

# Milestone

- [x] Understand OpenFin knowledge, mechanism and FDC3 specification. 2025-05-09
- [x] POC 1: Open Trade Blotter in OpenFin. 2025-05-08
- [x] POC 2: Ratan can raise intent to Blade, Blade handles intent properly. (via Devtool) 2025-05-12
- [x] POC 3: Ratan can raise trade relevant intent to Blade, Blade handle intent and display trade properly. (via GUI) 2025-05-21
- [x] POC 4: Blade can raise intent to Ratan, Ratan handles intent properly. (via Devtool) 2025-05-14
- [ ] ~~POC 5: Blade can raise intent to Ratan, Ratan trades handle intent and react properly. (via GUI) **Pending Blade implementation**~~
- [ ] ~~POC 6: TPT Portal can act as DA, proxy intent to proper app, open and bypass intent.~~
- [ ] ~~POC 7: (Better to Have) App can be opened when not already running.~~
- [x] PTP FDC3 Specification. Intent pattern, context pattern. internal & external.
- [x] Tenant Intent register & discovery.
- [ ] OneFM authentication & authorization.
- [ ] PTP Interop Broker Design. 1. Open tile; 2. Permission control.

# Process

1. Communicated with Blade, got POC present on their local env, got blade installation doc: [Installing OpenFin for Blade / SM Markets (Internal/External)](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3287919844)

2. Complete POC 1:  [fins://fmo-mfe-dev.uk.dev.net:8453/ratan_cashflow_blotter/ratan.fin.json](fins://fmo-mfe-dev.uk.dev.net:8453/ratan_cashflow_blotter/ratan.fin.json)

3. Complete POC 2: Ratan can raise intent to blade.

| Steps | Snapshot | Comment |
| --- | --- | --- |
| Open [Blade](fins://dev-dev1-dtp.apps.dtp-np.ocp.standardchartered.com/openfin.split.app.json) FXO | ![image-2025-5-12_14-9-38.png](attachments/image-2025-5-12_14-9-38.png) | Blade SingleWindow mode not integrated with FDC3, SplitView mode did. |
| Open Ratan Trades via devtool | ![image-2025-5-12_14-11-22.png](attachments/image-2025-5-12_14-11-22.png) ![image-2025-5-12_14-16-46.png](attachments/image-2025-5-12_14-16-46.png) | <details> <summary>Expand Details</summary> ```js fin.Window.create({ name: "trades", url: "https://fmo-mfe-dev.uk.dev.net:8453/?survey=no&container=ratan_container&module=trade_blotter&tile=trade", "fdc3InteropApi": "2.0", }); ``` </details> |
| Raise intent via Ratan devtool | ![image-2025-5-12_14-21-7.png](attachments/image-2025-5-12_14-21-7.png) | <details> <summary>Expand Details</summary> ```js fdc3.raiseIntent('scb.ViewLaunch', { 'type': 'scb.blade.fxo.quote.sales', 'event': { 'value': { 'quoteRequestId': '7v2by6bb944m1pp', 'isReadOnly': false, 'layoutToUse': null } } }); ``` </details> |

Several technical points confirmed:

- One manifest will launch one platform. So if Ratan and Blade use separated manifest, there will be 2 standalone platform.
- If set providerUrl of platform in manifest, platform will render the page in background. Developer should overwrite some Interop Broker api to get intent properly handled. Otherwise no one handle and will show errors.
- If providerUrl not provided in manifest, there will be default provider instead.
- Windows will automatically connect to Interop Broker of platform. Please noted that the platform instance establishing is not shared, one manifest one platform instance. If not provides platform providerUrl will create default platform instance. There will be 2 separate platform even 2 manifest use the same providerUrl.
- The new created windows will connect to platform only when they are created by this platform api. Otherwise windows are belonging to platform who init them.

4. Complete POC 4: Blade can raise intent to Ratan, Ratan handles intent properly. (via Devtool)

| Steps | Snapshot | Comment |
| --- | --- | --- |
| Open [Blade](fins://dev-dev1-dtp.apps.dtp-np.ocp.standardchartered.com/openfin.split.app.json) FXO | ![image-2025-5-12_14-9-38.png](attachments/image-2025-5-12_14-9-38.png) | We implement platform provider in ratan and wrapped blade manifest with it. [fin://fmo-openfin-dev.uk.dev.net:8200/blade.split.app.json](fin://fmo-openfin-dev.uk.dev.net:8200/blade.split.app.json) |
| Open Ratan Cashflow Blotter via devtool | ![image-2025-5-14_10-57-18.png](attachments/image-2025-5-14_10-57-18.png) | <details> <summary>Expand Details</summary> ```js fin.Window.create({ name: "ratan_settlement_cashflow_blotter", url: "https://fmo-mfe-dev.uk.dev.net:8453/?survey=no&container=ratan_container&module=cashflow_blotter_cn&tile=cashflow_cn", "fdc3InteropApi": "2.0", }); ``` </details> |
| Raise intent via GUI | ![image-2025-5-14_10-59-29.png](attachments/image-2025-5-14_10-59-29.png) | <details> <summary>Expand Details</summary> ```js ((function(){ // Create the button element const button = document.createElement('button'); button.id = 'floatingCashflowButton'; button.textContent = 'Open Cashflow'; // Add styles to the button using JavaScript Object.assign(button.style, { position: 'fixed', bottom: '20px', right: '20px', padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)', }); // Add hover effect using JavaScript button.addEventListener('mouseenter', () => { button.style.backgroundColor = '#0056b3'; }); button.addEventListener('mouseleave', () => { button.style.backgroundColor = '#007bff'; }); // Add a click event listener to the button button.addEventListener('click', () => { alert('Button clicked!'); window.fdc3.raiseIntent('scb.ViewLaunch', { 'type': 'scb.fmtpt.ratan_settlement_cashflow_blotter.open.tile', "id": { "cashflowId": "M0094770513" } }); }); // Append the button to the body document.body.appendChild(button); })()); ``` </details> |

# Workflow

**EXPAND: Click here to expand POC Workflow...**

**EXPAND_END**

For more details on FMTPT Broker, please refer to.

## Blade Interoperability Diagram

![image-2025-5-14_11-49-32.png](attachments/image-2025-5-14_11-49-32.png)