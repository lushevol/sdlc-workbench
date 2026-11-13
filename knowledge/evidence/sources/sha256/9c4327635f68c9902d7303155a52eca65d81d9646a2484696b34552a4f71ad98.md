# OpenFin

![](https://www.financemagnates.com/wp-content/uploads/2018/02/OpenFin_in_action-1.png?x14075)

***OpenFin is a web runtime and operating environment designed for enterprise app development. Built on web standards, OpenFin dramatically enhances the capabilities of web apps, enabling end-user experience and enterprise controls well beyond what is possible with browsers like Chrome and Edge or with frameworks like Electron and Chromium Embedded Framework.***

> **INFO**
> OpenFin has been rebranded to **Here™**, OpenFin is a fintech company that provides a secure, enterprise-grade runtime environment designed specifically for <u>**desktop**</u> applications in <u>**financial**</u> services industry.

![image-2025-3-14_12-13-31.png](attachments/image-2025-3-14_12-13-31.png)

Relationship with chromium browsers

## Glossary

| Concept Now | Concept (Former) | Capabilities | Description |
| --- | --- | --- | --- |
| Runtime | (OpenFin → Electron → Chromium) | The Runtime component provides the runtime environment in which *Here™ Core apps* and *platforms* are executed. |
| RVM | - [Installing itself and Runtime](https://resources.here.io/docs/core/manage/rvm/how-it-works#installation) - [RVM error reporting](https://resources.here.io/docs/core/manage/data/error-reporting) - [Citrix/VDI installation](https://resources.here.io/docs/core/manage/deployment/vdi-deployment) - [Hosting assets](https://resources.here.io/docs/core/manage/desktops/host-assets) - [Enable HTTPS security features](https://resources.here.io/docs/core/manage/security/https-security) - ~~[Services](https://resources.here.io/docs/core/addenda/deprecated/services)~~ - [Deep linking](https://resources.here.io/docs/core/develop/deep-linking) - [Semantic versioning](https://resources.here.io/docs/core/develop/manifests/semantic-versioning) - Multi-Runtime environments - App Assets & Services - OS-level features such as auto-launch on startup, branded shortcuts, splash screens, and download progress bar - [License tracking](https://resources.here.io/docs/core/manage/data/license-data) | The Runtime Version Manager ([RVM](https://resources.here.io/docs/core/manage/rvm/)) controls the installation and update of the Runtime. It is responsible for launching the Runtime in order to execute Here Core apps. |
| Here™ Core | OpenFin | | ![](https://resources.here.io/docs/core/assets/images/Here-Core-architecture-31da5aaf48ccd44f5c8a0b39f8472c36.png) |
| Here™ Core UI (Components) | OpenFin Workspace | - Browser - Tab - Dynamic Layout - Drag & Drop - Home - Notification Center - Dock - Storefront | entirely agnostic to the frontend frameworks used to deliver your content. Developers are free to build their apps using React, Vue, Angular, or any framework they choose. ![](https://resources.here.io/docs/core/assets/images/here-core-ui-example-a416b0be9987e02a0f266d0f9a637a68.png) |
| Here™ Core Container | OpenFin Container | - Foundation of window and interoperability. | |
| Here™ Core Web | OpenFin Anywhere | | provides a subset of functionality, meaning that content delivered on the desktop can also be provided in a regular web browser such as Chrome, Safari, or Edge. |
| Here™ Core APIs | OpenFin Container APIs | | - written in JavaScript/TypeScript |
| Here™ Core UI APIs | OpenFin Workspace APIs | | - written in JavaScript/TypeScript |
| ** ** Interoperability | - Interop API - FDC3 API - Channel API - Inter-Application Bus (IAB) | |
| ** **Native adapters | - NodeJS: JavaScript is the "default" language of Here Core APIs, but technically, it is provided by an adapter - .NET, for programs written in C# - Java - C++ | |
| ** **Third-party integrations | - [Microsoft 365](https://resources.here.io/docs/core/integrations/microsoft-365/) - [Microsoft Excel](https://resources.here.io/docs/core/integrations/excel/) - [Salesforce](https://resources.here.io/docs/core/integrations/salesforce/) - [ServiceNow](https://resources.here.io/docs/core/integrations/servicenow/) - [Bloomberg](https://resources.here.io/docs/core/integrations/bloomberg) | |

# OpenFin User Journey

# Runtime & RVM Update

TODO

<details>
<summary>Détails</summary>

# OpenFin Instance

</details>

# License

The License in FM is mainly owned by Blade PSS Team. Blade paid 80% of the cost for  1,600 licenses. SPOC: Blade PSS. Prathap Reddy

RVM will reporting License usage frequently.

- **License key**: Unique identifier for your Here™ license
- **Machine ID**: Non-personal, anonymous unique ID for the machine and user account
- **App ID**: URL of the application manifest file
- **Startup URL** or **Platform URL**: (in RVM 7.1 and later) Value used for `startup_app.providerUrl` or `platform.providerUrl` in the application manifest file.
- **Content URL**: (in RVM 7.1/Runtime 26 and later) The URL specified in `window.options` when a window is created via a `fins:` link.
- **App events**: Launch and close time of application (UTC)
- **Runtime environment**: Runtime, RVM, and operating system versions
- **Adapter type and version**: (in RVM 9 or later) If a .NET or Java adapter is used, its type and version
- **Public-facing IP address**: Public facing IP address of the network request as seen by Here™ servers. This is used to estimate the company where the information has been sent from. It is the public IP address attached to the request, or if an LRS is being used, the public IP of the LRS. It is not the end-user desktop IP address.

## Update

Instead of judge env from url, OpenFin now support non-prod license.

![image-2025-5-9_10-40-19.png](attachments/image-2025-5-9_10-40-19.png)

## Unique user API

```
const app = fin.desktop.Application.getCurrent()
   app.registerUser(
    userName, 
    appName, 
    function(){console.log("Success")}, 
    function(err){console.log("Failure")}
)
```

# OpenFin Installer Generator

[https://install.openfin.co/](https://install.openfin.co/)

![image-2025-8-27_13-4-55.png](attachments/image-2025-8-27_13-4-55.png)

# Interoperability

## InterApplication Bus

pub/sub

## Channel

base on IAB, suitable for 2 direction, big data, cross processing. Async msg.

low level data type: Inter-process Communication (IPC) or WebRTC.

## Interop

Contrxt (group) based sharing model, client-> broker -> client.

compatible with FDC3, extends it.

## FDC3

supporting 1.2/2.0

openfin built-in DesktopAgent is interop broker

- every platform auto comes from DA
- every view auto connects to DA

Provide some system channels eg browser color channel.

broadcast context -> addContextHander

raiseIntent -> addIntentHandler

# FDC3

***Financial Desktop Connectivity and Collaboration Consortium***

FDC3 is an <u>**open standard**</u> for applications on financial desktop to interoperate and exchange data with each other.

| Concept | Description | Example |
| --- | --- | --- |
| **[Desktop Agent API](https://fdc3.finos.org/docs/api/spec)** | An API interface for working with a Desktop agent, which acts as launcher and message router (broker) for applications in its domain. | |
| **[Intents](https://fdc3.finos.org/docs/intents/spec)** | A set of verbs that, in conjunction with context data acting as nouns, can be used to put together common cross-application workflows on the financial desktop. | - [StartCall](https://fdc3.finos.org/docs/intents/ref/StartCall) - [StartChat](https://fdc3.finos.org/docs/intents/ref/StartChat) - [StartEmail](https://fdc3.finos.org/docs/intents/ref/StartEmail) - [SendChatMessage](https://fdc3.finos.org/docs/intents/ref/SendChatMessage) - [ViewAnalysis](https://fdc3.finos.org/docs/intents/ref/ViewAnalysis) |
| **[Context Data](https://fdc3.finos.org/docs/context/spec)** | A message format for passing common identifiers and data between apps to create a seamless workflow. | <details> <summary>Détails</summary> { "type": "fdc3.trade", "name": "...", "id": { "myEMS": "12345" }, "product": { "type": "fdc3.product", "id": { "productId": "ABC123" }, "instrument": { "type": "fdc3.instrument", "id": { "ticker": "MSFT" } } } } </details> |
| **[App Directory](https://fdc3.finos.org/docs/app-directory/spec)** | A structured repository of information about apps that can be used in an FDC3-enabled desktop. | - appId, appName, email, version, etc. - intents - context <details> <summary>Détails</summary> { "appId": "my-application", "title": "My Application", "description": "An example application that uses FDC3 and fully describes itself in an AppD record.", "categories": [ "market data", "research", "news" ], "version": "1.0.0", "tooltip": "My example application definition", "lang": "en-US", "icons": [ { "src": "[http://example.domain.com/assets/my-app-icon.png](http://example.domain.com/assets/my-app-icon.png)", "size": "256x256", "type": "image/png" } ], "screenshots": [ { "src": "[http://example.domain.com/assets/my-app-screenshot-1.png](http://example.domain.com/assets/my-app-screenshot-1.png)", "label": "The first screenshot of my example app", "type": "image/png", "size": "800x600" }, { "src": "[http://example.domain.com/assets/my-app-screenshot-2.png](http://example.domain.com/assets/my-app-screenshot-2.png)", "label": "The second screenshot of my example app", "type": "image/png", "size": "800x600" } ], "contactEmail": "fdc3@[finos.org](http://finos.org)", "supportEmail": "fdc3-maintainers@[finos.org](http://finos.org)", "moreInfo": "[http://example.domain.com/](http://example.domain.com/)", "publisher": "Example App, Inc.", "type": "web", "details": { "url": "[http://example.domain.com/app.html](http://example.domain.com/app.html)" }, "hostManifests": { "Finsemble": { "window": { "left": 120, "top": 120, "width": 600, "height": 800, "options": { "minWidth": 75 } }, "foreign": { "components": { "App Launcher": { "launchableByUser": true }, "Window Manager": { "FSBLHeader": true, "persistWindowState": true } } }, "interop": { "autoConnect": true } }, "Glue42": { "type": "window", "details": { "height": 800, "width": 600, "left": 120, "top": 120, "mode": "tab", "allowChannels": true, "loader": { "enabled": true, "hideOnLoad": true } }, "customProperties": { "folder": "FDC3 Toolbox" } }, "Web App Manifest": "[http://example.domain.com/my-app.json](http://example.domain.com/my-app.json)" }, "interop": { "intents": { "listensFor": { "ViewChart": { "contexts": [ "fdc3.instrument" ] }, "myApp.GetPrice": { "contexts": [ "fdc3.instrument" ], "resultType": "myApp.quote" } }, "raises": { "ViewOrders": [ "fdc3.instrument", "fdc3.organization" ], "StartEmail": [ "fdc3.email" ] } }, "userChannels": { "broadcasts": [ "fdc3.instrument", "fdc3.organization" ], "listensFor": [ "fdc3.instrument", "fdc3.organization" ] }, "appChannels": [ { "id": "myApp.quotes,", "description": "Used to share a stream of quotes for currently displayed instrument and may be used to change the currently displayed symbol,", "broadcasts": [ "myApp.quote" ], "listensFor": [ "fdc3.instrument" ] } ] }, "localizedVersions": { "fr-FR": { "title": "Mon application,", "description": "Un exemple d'application qui utilise FDC3 et se décrit entièrement dans un enregistrement AppD." } } } </details> |
| **[Agent Bridging](https://fdc3.finos.org/docs/agent-bridging/spec)** | An [@experimental](https://fdc3.finos.org/docs/fdc3-compliance#experimental-features) API interface for the interconnection of Desktop Agents (DAs) such that apps running under different Desktop Agents can interoperate. | |

![image-2025-3-14_13-1-29.png](attachments/image-2025-3-14_13-1-29.png)

![](https://resources.here.io/docs/core/assets/images/here-core-interop-fdc3-Intent-diagram-75d3c2ebfeaa716db952257f57abab17.png)

# Reference

[https://resources.here.io/docs/core/get-started/terminology](https://resources.here.io/docs/core/get-started/terminology)

[https://resources.here.io/docs/core/get-started/what-is-here-core](https://resources.here.io/docs/core/get-started/what-is-here-core)

OpenFin Installer

[https://install.openfin.co/](https://install.openfin.co/)