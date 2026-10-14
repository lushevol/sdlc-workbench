---
type: Architecture
id: ARCH-single-ui-contracts
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: repos/ui/mfe-base/src/root.tsx
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: d633a6d2dc60da8ed031bab323fb658f016d85a26fd10b4f2f302cefd0b048a1
- resource: repos/ui/mfe-root-config/src/root.ts
  revision: 83091d85beff5306ca0cd643955d8ea6ed0a2d93
  sha256: 25f2b952a39292a0e73caf4c2bea373fa0bdaa5972f00ee60b7a41cb302a2dab
- resource: repos/ui/mfe-root-config/src/microfrontend-layout.html
  revision: 83091d85beff5306ca0cd643955d8ea6ed0a2d93
  sha256: f0a62a6fd9c2baa28c182076f0e36622afa6bb4f76712b4da358f72b6b2ff421
- resource: repos/ui/mfe-root-config/src/index.ejs#L36-L36
  revision: 83091d85beff5306ca0cd643955d8ea6ed0a2d93
  sha256: ec96d54a396565ac57d6dfec282f6d0a2262853fa418621039d06411ea4644aa
- resource: repos/ui/mfe-base/src/pages/Home/common/Container.tsx
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: c724d38617a9e452f2e002f1866ce7e9999cd8f5a37689f9510097c43870d5c4
- resource: repos/ui/mfe-base/src/hooks/model/workspaces.ts
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: f98dccdeb3991f68e86d9f51c7fdca6b107fd828bb01818d95b35c99c1fcc322
- resource: repos/ui/mfe-base/src/hooks/service/index.ts
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: dad8c0cc23240d926a5e73fa83e1fc6830c8134046e59defcf61990e9b38989e
- resource: repos/ui/mfe-base/src/hooks/service/config.ts
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: f3856b594a5930ee9f66e28e91e4a345873850f501b8768315a8e7c9ae889266
- resource: repos/ui/mfe-base/src/hooks/service/util/getEndpoint.ts
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: 4fad93acd98fcd34e3ed5bc3f0d1bdfb5a59d8dd1c7a9e7f62354a702e47c102
- resource: repos/ui/mfe-base/src/services/index.ts
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: c71ea8dd0481fb8074073dbc2dccf7e03878768ba722b652e14ff11e855e64ab
- resource: repos/ui/mfe-base/src/hooks/service/util/success.request.handler.ts
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: 4b85639d4bf4c0b588b9c9a774a105ef74c11ea2b109092425b4a85ca87195cd
- resource: repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: 7917609f4cb9f0ef995d7846a910c91430972bb16e96f5320f5b55ed4362ba31
- resource: repos/ui/mfe-base/src/utils/login.ts
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: e95c437c5cadb7ebb2ca450c6f2df85bcf3f60194d9ef54095fdbf7934eaa7de
- resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java
  revision: 091c9d16c13f285a78463ff0235c21b152844b61
  sha256: b71df7273263aa8c17b8ea58e9e727008b108ec51ffdc70e266207ed07efad4a
- resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/Constant.java
  revision: 091c9d16c13f285a78463ff0235c21b152844b61
  sha256: 63ddf339505d0971919a513ef088e417bf4fd27d196f912132ebe6788bf1a3ac
- resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/response/ResponseOfAuthenticate.java
  revision: 091c9d16c13f285a78463ff0235c21b152844b61
  sha256: 9e88f065b94c1e5edad70e027db3f43921c50283eb51c69edc152f0000a67bf4
- resource: repos/ui/mfe-base/src/admin/ImportMap/services/useServices.ts
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: c039fd03f8f5c51a386ba10d527f3beae7bb28681ae3cfdd1db1b1a81e8bdfca
- resource: repos/ui/mfe-base/src/admin/common/services/useAdminRequest.ts
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: 538f31a915c9f0955c692a9dac1dead28686fd99c5844744caccce4dfaf5e267
- resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java
  revision: 091c9d16c13f285a78463ff0235c21b152844b61
  sha256: 17e4241303c4e1efaec0dd3f4623d4d823bb232e87a882b7214e48fa1c3c13d0
- resource: repos/ui/mfe-root-config/src/index.ejs#L21-L24
  revision: 83091d85beff5306ca0cd643955d8ea6ed0a2d93
  sha256: e0aa5801888d199becb69fa7cbaca1b09ffde3b598de8ab46d3d9b1d0084f23c
- resource: repos/ui/mfe-base/src/admin/Category/services/useServices.ts
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: 58b53dc7a14c9f9d2709ddcae26efef7b64d6a308b84515899e3cef72273539a
- resource: repos/ui/mfe-base/src/admin/Tile/services/useServices.ts
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: 44327e6dcd4548266e9781977beae8e0d35ac06fb69af55701650e3377953092
- resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java
  revision: 091c9d16c13f285a78463ff0235c21b152844b61
  sha256: cf5c2266952bb6684f2600ecb268c8120d1efbbf5220d8fadf528c9f8a5b91b3
- resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java
  revision: 091c9d16c13f285a78463ff0235c21b152844b61
  sha256: 6b2d0c45025fc32495f48c2a49380cc297e24e9a6eaa6b6da742b2d47f42084b
- resource: repos/ui/mfe-base/src/analytics/index.ts
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: a620b4ad660ed47d1df4a9a9a4d6b0582988f5c20964f3ead4383771fe99c368
- resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/AnalyticsController.java
  revision: 091c9d16c13f285a78463ff0235c21b152844b61
  sha256: cd34671c3226b7ca43eb1569042f4fa48070803fe3e23e24aaf08d0cedd2a40d
- resource: repos/ui/mfe-root-config/nginx/mfe.conf#L785-L807
  revision: 83091d85beff5306ca0cd643955d8ea6ed0a2d93
  sha256: 768d57d1f09ef8d58ce813dff5028df34bb40ca138aa73220a21fd2d426ccbea
generated:
  by: agent:codex
  at: '2026-10-14T01:06:51.080147+00:00'
verified: []
scope: Record current interface declarations across single-ui-bff, mfe-base, and mfe-root-config
  source snapshots.
components:
- single-ui-bff declares authentication, import map, category, tile, and analytics
  HTTP providers.
- mfe-base declares the base application, shared client services, and dynamic container
  host.
- mfe-root-config declares application loading, an import map loader, and proxy routes.
interfaces:
- single-ui-base-module
- single-ui-container-props
- single-ui-shared-http
- single-ui-sso-token-family
- single-ui-importmap-admin
- single-ui-active-importmap
- single-ui-category-tile-admin
- single-ui-analytics-proxy
dependencies:
- The root source imports single-spa and single-spa-layout.
- The base source imports React, single-spa-react, and Axios.
- The provider source imports Spring HTTP and controller interfaces.
- The proxy names ratan_backend_api_gateway. Its implementation is outside the inspected
  source scope.
decisions:
- Keep these interfaces as knowledge candidates until owner review and routing gaps
  are resolved.
- Bind contract sources to new local initial commits without claiming original repository
  history.
- Do not infer approved business requirements or passing business behavior from source
  declarations.
contract_candidates:
- id: single-ui-base-module
  type: ui
  provider_repository_ids:
  - mfe-base
  consumer_repository_ids:
  - mfe-root-config
  source_paths:
  - repos/ui/mfe-base/src/root.tsx
  - repos/ui/mfe-root-config/src/root.ts
  - repos/ui/mfe-root-config/src/microfrontend-layout.html
  - repos/ui/mfe-root-config/src/index.ejs#L36-L36
  evidence:
  - resource: repos/ui/mfe-base/src/root.tsx
    revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
    sha256: d633a6d2dc60da8ed031bab323fb658f016d85a26fd10b4f2f302cefd0b048a1
  - resource: repos/ui/mfe-root-config/src/root.ts
    revision: 83091d85beff5306ca0cd643955d8ea6ed0a2d93
    sha256: 25f2b952a39292a0e73caf4c2bea373fa0bdaa5972f00ee60b7a41cb302a2dab
  - resource: repos/ui/mfe-root-config/src/microfrontend-layout.html
    revision: 83091d85beff5306ca0cd643955d8ea6ed0a2d93
    sha256: f0a62a6fd9c2baa28c182076f0e36622afa6bb4f76712b4da358f72b6b2ff421
  - resource: repos/ui/mfe-root-config/src/index.ejs#L36-L36
    revision: 83091d85beff5306ca0cd643955d8ea6ed0a2d93
    sha256: ec96d54a396565ac57d6dfec282f6d0a2262853fa418621039d06411ea4644aa
  observed_declaration:
  - The root imports application names through SystemJS and registers the default
    @fm/base application.
  - The root supplies publicUrl and version properties to each application.
  - The base exports bootstrap, mount, unmount, shared services, hooks, utilities,
    and UI components.
  documentation_gap: The active module mapping and deployed lifecycle results remain
    unknown.
  owner: unknown
  next_action: Confirm the deployed @fm/base mapping and retain lifecycle execution
    evidence.
- id: single-ui-container-props
  type: ui
  provider_repository_ids: []
  consumer_repository_ids:
  - mfe-base
  source_paths:
  - repos/ui/mfe-base/src/pages/Home/common/Container.tsx
  - repos/ui/mfe-base/src/hooks/model/workspaces.ts
  evidence:
  - resource: repos/ui/mfe-base/src/pages/Home/common/Container.tsx
    revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
    sha256: c724d38617a9e452f2e002f1866ce7e9999cd8f5a37689f9510097c43870d5c4
  - resource: repos/ui/mfe-base/src/hooks/model/workspaces.ts
    revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
    sha256: f98dccdeb3991f68e86d9f51c7fdca6b107fd828bb01818d95b35c99c1fcc322
  observed_declaration:
  - The base loads props.container through System.import and expects a React component.
  - The base passes module, tile, parameters, panelId, and tabId properties.
  - The @fm/base container selects the internal admin module.
  documentation_gap: Loaded container providers and their accepted property contracts
    remain unidentified.
  owner: unknown
  next_action: Identify each current container provider and compare its declared properties.
  inferred_relationship: External container components must accept the properties
    supplied by the base host.
- id: single-ui-shared-http
  type: http
  provider_repository_ids:
  - mfe-base
  consumer_repository_ids:
  - mfe-base
  source_paths:
  - repos/ui/mfe-base/src/root.tsx
  - repos/ui/mfe-base/src/hooks/service/index.ts
  - repos/ui/mfe-base/src/hooks/service/config.ts
  - repos/ui/mfe-base/src/hooks/service/util/getEndpoint.ts
  evidence:
  - resource: repos/ui/mfe-base/src/root.tsx
    revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
    sha256: d633a6d2dc60da8ed031bab323fb658f016d85a26fd10b4f2f302cefd0b048a1
  - resource: repos/ui/mfe-base/src/hooks/service/index.ts
    revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
    sha256: dad8c0cc23240d926a5e73fa83e1fc6830c8134046e59defcf61990e9b38989e
  - resource: repos/ui/mfe-base/src/hooks/service/config.ts
    revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
    sha256: f3856b594a5930ee9f66e28e91e4a345873850f501b8768315a8e7c9ae889266
  - resource: repos/ui/mfe-base/src/hooks/service/util/getEndpoint.ts
    revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
    sha256: 4fad93acd98fcd34e3ed5bc3f0d1bdfb5a59d8dd1c7a9e7f62354a702e47c102
  observed_declaration:
  - The Service export supplies GET, POST, PUT, PATCH, and DELETE clients.
  - The endpoint helper prepends /api to each supplied path.
  - The Axios configuration declares JSON headers and a 60000 ms timeout.
  documentation_gap: Exported helpers have internal consumers. External consumers
    and timeout execution results remain unknown.
  owner: unknown
  next_action: Record current external consumers before changing shared HTTP behavior.
- id: single-ui-sso-token-family
  type: http
  provider_repository_ids:
  - single-ui-bff
  consumer_repository_ids:
  - mfe-base
  source_paths:
  - repos/ui/mfe-base/src/services/index.ts
  - repos/ui/mfe-base/src/hooks/service/index.ts
  - repos/ui/mfe-base/src/hooks/service/util/success.request.handler.ts
  - repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts
  - repos/ui/mfe-base/src/utils/login.ts
  - repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java
  - repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/Constant.java
  - repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/response/ResponseOfAuthenticate.java
  evidence:
  - resource: repos/ui/mfe-base/src/services/index.ts
    revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
    sha256: c71ea8dd0481fb8074073dbc2dccf7e03878768ba722b652e14ff11e855e64ab
  - resource: repos/ui/mfe-base/src/hooks/service/index.ts
    revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
    sha256: dad8c0cc23240d926a5e73fa83e1fc6830c8134046e59defcf61990e9b38989e
  - resource: repos/ui/mfe-base/src/hooks/service/util/success.request.handler.ts
    revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
    sha256: 4b85639d4bf4c0b588b9c9a774a105ef74c11ea2b109092425b4a85ca87195cd
  - resource: repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts
    revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
    sha256: 7917609f4cb9f0ef995d7846a910c91430972bb16e96f5320f5b55ed4362ba31
  - resource: repos/ui/mfe-base/src/utils/login.ts
    revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
    sha256: e95c437c5cadb7ebb2ca450c6f2df85bcf3f60194d9ef54095fdbf7934eaa7de
  - resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java
    revision: 091c9d16c13f285a78463ff0235c21b152844b61
    sha256: b71df7273263aa8c17b8ea58e9e727008b108ec51ffdc70e266207ed07efad4a
  - resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/Constant.java
    revision: 091c9d16c13f285a78463ff0235c21b152844b61
    sha256: 63ddf339505d0971919a513ef088e417bf4fd27d196f912132ebe6788bf1a3ac
  - resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/response/ResponseOfAuthenticate.java
    revision: 091c9d16c13f285a78463ff0235c21b152844b61
    sha256: 9e88f065b94c1e5edad70e027db3f43921c50283eb51c69edc152f0000a67bf4
  observed_declaration:
  - The base declares POST /api/auth/v2/sso/login and /api/auth/v3/sso/login calls.
  - The provider declares v2/sso/login and v3/sso/login mappings.
  - Both sources declare validation, logout, refresh token, and relogin interfaces.
  - Session requests use singleUIAuthorization bodies. Relogin uses the Single-UI-Refresh
    header.
  - The provider declares Bearer-prefixed Single-UI-Authorization and Single-UI-Refresh
    response headers.
  - The base consumes token headers, userInfo, entities, drawers, and entitlementsToken
    response fields.
  documentation_gap: Matching declarations support compatibility. Gateway routing
    and retained authentication execution remain unresolved.
  owner: unknown
  next_action: Confirm gateway rewrites and retain approved authentication scenario
    results.
  inferred_relationship: The client and provider declarations describe compatible
    authentication interfaces after prefix removal.
- id: single-ui-importmap-admin
  type: http
  provider_repository_ids:
  - single-ui-bff
  consumer_repository_ids:
  - mfe-base
  source_paths:
  - repos/ui/mfe-base/src/admin/ImportMap/services/useServices.ts
  - repos/ui/mfe-base/src/admin/common/services/useAdminRequest.ts
  - repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java
  evidence:
  - resource: repos/ui/mfe-base/src/admin/ImportMap/services/useServices.ts
    revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
    sha256: c039fd03f8f5c51a386ba10d527f3beae7bb28681ae3cfdd1db1b1a81e8bdfca
  - resource: repos/ui/mfe-base/src/admin/common/services/useAdminRequest.ts
    revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
    sha256: 538f31a915c9f0955c692a9dac1dead28686fd99c5844744caccce4dfaf5e267
  - resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java
    revision: 091c9d16c13f285a78463ff0235c21b152844b61
    sha256: 17e4241303c4e1efaec0dd3f4623d4d823bb232e87a882b7214e48fa1c3c13d0
  observed_declaration:
  - The client declares POST /api/auth/v1/fmo/admin/importmap/{data,audit,update,create}.
  - The provider declares matching v1/fmo/admin/importmap mappings.
  - Update requests use maker, checker, or deactivate modes and include entitlementsToken.
  - The client reads the data field from the provider response envelope.
  documentation_gap: Matching route suffixes do not establish deployed connectivity
    or successful administrative authorization.
  owner: unknown
  next_action: Confirm routing and retain reviewed administrative request and response
    examples.
- id: single-ui-active-importmap
  type: data
  provider_repository_ids:
  - single-ui-bff
  consumer_repository_ids: []
  source_paths:
  - repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java
  - repos/ui/mfe-root-config/src/index.ejs#L21-L24
  evidence:
  - resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java
    revision: 091c9d16c13f285a78463ff0235c21b152844b61
    sha256: 17e4241303c4e1efaec0dd3f4623d4d823bb232e87a882b7214e48fa1c3c13d0
  - resource: repos/ui/mfe-root-config/src/index.ejs#L21-L24
    revision: 83091d85beff5306ca0cd643955d8ea6ed0a2d93
    sha256: e0aa5801888d199becb69fa7cbaca1b09ffde3b598de8ab46d3d9b1d0084f23c
  observed_declaration:
  - The provider declares GET v1/fmo/admin/importmap/active and returns an imports
    object from active records.
  - The provider prefixes other keys with @fm/ and preserves single-spa, react, and
    react-dom keys.
  - The root template loads a SystemJS import map from its publicUrl and importmap
    parameters.
  documentation_gap: The retained template does not identify the configured import
    map URL or its active provider.
  owner: unknown
  next_action: Inspect the deployed importmap parameter and retain the retrieved import
    map bytes.
  potential_consumer_repository_ids:
  - mfe-root-config
  inferred_relationship: The provider output has the imports shape expected by the
    root loader. Deployment use remains unproved.
- id: single-ui-category-tile-admin
  type: http
  provider_repository_ids:
  - single-ui-bff
  consumer_repository_ids:
  - mfe-base
  source_paths:
  - repos/ui/mfe-base/src/admin/Category/services/useServices.ts
  - repos/ui/mfe-base/src/admin/Tile/services/useServices.ts
  - repos/ui/mfe-base/src/admin/common/services/useAdminRequest.ts
  - repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java
  - repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java
  evidence:
  - resource: repos/ui/mfe-base/src/admin/Category/services/useServices.ts
    revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
    sha256: 58b53dc7a14c9f9d2709ddcae26efef7b64d6a308b84515899e3cef72273539a
  - resource: repos/ui/mfe-base/src/admin/Tile/services/useServices.ts
    revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
    sha256: 44327e6dcd4548266e9781977beae8e0d35ac06fb69af55701650e3377953092
  - resource: repos/ui/mfe-base/src/admin/common/services/useAdminRequest.ts
    revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
    sha256: 538f31a915c9f0955c692a9dac1dead28686fd99c5844744caccce4dfaf5e267
  - resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java
    revision: 091c9d16c13f285a78463ff0235c21b152844b61
    sha256: cf5c2266952bb6684f2600ecb268c8120d1efbbf5220d8fadf528c9f8a5b91b3
  - resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java
    revision: 091c9d16c13f285a78463ff0235c21b152844b61
    sha256: 6b2d0c45025fc32495f48c2a49380cc297e24e9a6eaa6b6da742b2d47f42084b
  observed_declaration:
  - The client declares POST /api/auth/v1/fmo/admin/category/{data,audit,update,create}.
  - The client declares POST /api/auth/v1/fmo/admin/tile/{data,audit,update,create}.
  - The provider declares matching category and tile route families.
  - Update requests use maker, checker, or deactivate modes and include entitlementsToken.
  - The shared client consumes the response data field and supplies request cancellation
    signals.
  documentation_gap: Matching administrative declarations do not prove authorization,
    review separation, or successful storage changes.
  owner: unknown
  next_action: Confirm routing and retain separate maker and checker execution evidence.
- id: single-ui-analytics-proxy
  type: http
  provider_repository_ids:
  - single-ui-bff
  consumer_repository_ids:
  - mfe-base
  source_paths:
  - repos/ui/mfe-base/src/analytics/index.ts
  - repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/AnalyticsController.java
  - repos/ui/mfe-root-config/nginx/mfe.conf#L785-L807
  evidence:
  - resource: repos/ui/mfe-base/src/analytics/index.ts
    revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
    sha256: a620b4ad660ed47d1df4a9a9a4d6b0582988f5c20964f3ead4383771fe99c368
  - resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/AnalyticsController.java
    revision: 091c9d16c13f285a78463ff0235c21b152844b61
    sha256: cd34671c3226b7ca43eb1569042f4fa48070803fe3e23e24aaf08d0cedd2a40d
  - resource: repos/ui/mfe-root-config/nginx/mfe.conf#L785-L807
    revision: 83091d85beff5306ca0cd643955d8ea6ed0a2d93
    sha256: 768d57d1f09ef8d58ce813dff5028df34bb40ca138aa73220a21fd2d426ccbea
  observed_declaration:
  - The base declares POST /api/analytics/v1/fmo/print with singleUIAuthorization,
    key, and event fields.
  - The provider declares POST v1/fmo/print and returns a result field.
  - The proxy removes /api/auth/ and /api/analytics/ prefixes and targets ratan_backend_api_gateway.
  - Direct single_ui_bff proxy directives are comments in the retained configuration.
  documentation_gap: The gateway implementation and active deployment configuration
    remain unavailable. Direct browser connectivity remains unproved.
  owner: unknown
  next_action: Retain gateway route evidence and one reviewed analytics execution
    result.
  intermediary_repository_ids:
  - mfe-root-config
  inferred_relationship: The client and provider suffixes match after the declared
    proxy rewrite. Gateway forwarding remains unresolved.
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
local_initial_baselines:
  single-ui-bff: 091c9d16c13f285a78463ff0235c21b152844b61
  mfe-base: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  mfe-root-config: 83091d85beff5306ca0cd643955d8ea6ed0a2d93
source_origin_limit: These commits start the supplied copies. Original repository
  history remains unavailable.
---
# Single UI interface candidates

## Scope

This record describes retained source declarations for three registered repository identities.
Each source revision identifies a new local initial Git commit.
Original repository history and deployed connectivity remain unknown.
No business execution was performed for this record.
The `verified` list is empty.

## Components

- `single-ui-bff` declares HTTP providers for authentication, import maps, categories, tiles, and analytics.
- `mfe-base` declares application lifecycles, shared clients, and a dynamic container host.
- `mfe-root-config` declares the application loader, import map loader, and proxy routes.

## Interfaces

### Base module

Fact: The root registers `@fm/base` through single-spa.
Fact: The base exports lifecycles, shared services, hooks, utilities, and UI components.
Evidence: [base exports](../raw/2026-10-14-initial-repositories/mfe-base/src/root.tsx.snapshot) and [root registration](../raw/2026-10-14-initial-repositories/mfe-root-config/src/root.ts.snapshot).
Consequence: Module changes can affect the root loader and shared API consumers.
Owner: Unknown.
Next action: Confirm the deployed module mapping and retain lifecycle execution evidence.

### Dynamic container properties

Fact: The base loads the named container and passes `module`, `tile`, `parameters`, `panelId`, and `tabId`.
Evidence: [container host](../raw/2026-10-14-initial-repositories/mfe-base/src/pages/Home/common/Container.tsx.snapshot).
Inference: External container components must accept the supplied properties.
Consequence: Incompatible properties can prevent a container from displaying its intended content.
Owner: Unknown.
Next action: Identify providers and compare their declared properties.

### Shared HTTP clients

Fact: The shared service prefixes paths with `/api` and declares a 60000 ms timeout.
Evidence: [endpoint helper](../raw/2026-10-14-initial-repositories/mfe-base/src/hooks/service/util/getEndpoint.ts.snapshot) and [Axios configuration](../raw/2026-10-14-initial-repositories/mfe-base/src/hooks/service/config.ts.snapshot).
Limit: Source inspection does not establish observed timeout behavior.
Consequence: Helper changes can affect internal callers and unknown external consumers.
Owner: Unknown.
Next action: Identify current consumers before changing shared HTTP behavior.

### SSO and token family

Fact: Client and provider sources declare matching login, validation, logout, refresh token, and relogin suffixes.
Evidence: [SSO client](../raw/2026-10-14-initial-repositories/mfe-base/src/services/index.ts.snapshot) and [authentication provider](../raw/2026-10-14-initial-repositories/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java.snapshot).
Inference: The declarations describe compatible interfaces after prefix removal.
Consequence: Header, body, or response changes can affect session handling.
Owner: Unknown.
Next action: Confirm routing and retain approved authentication scenario results.

### Import map administration

Fact: Client and provider sources declare import map data, audit, update, and create routes.
Evidence: [admin client](../raw/2026-10-14-initial-repositories/mfe-base/src/admin/ImportMap/services/useServices.ts.snapshot) and [import map provider](../raw/2026-10-14-initial-repositories/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java.snapshot).
Limit: Matching declarations do not establish successful administrative authorization.
Consequence: Route or envelope changes can prevent import map administration.
Owner: Unknown.
Next action: Retain reviewed administrative request and response examples.

### Active import map provider

Fact: The provider returns active records inside an `imports` object.
Fact: The root loads an import map from configured template parameters.
Evidence: [active provider](../raw/2026-10-14-initial-repositories/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java.snapshot) and [import map loader](../raw/2026-10-14-initial-repositories/mfe-root-config/src/index.ejs.L21-L24.snapshot).
Consequence: Unresolved configuration prevents a confirmed relationship between the provider and loader.
Owner: Unknown.
Next action: Inspect deployed parameters and retain the retrieved import map bytes.

### Category and tile administration

Fact: Client and provider sources declare category and tile data, audit, update, and create routes.
Evidence: [category client](../raw/2026-10-14-initial-repositories/mfe-base/src/admin/Category/services/useServices.ts.snapshot) and [tile client](../raw/2026-10-14-initial-repositories/mfe-base/src/admin/Tile/services/useServices.ts.snapshot).
Limit: Source declarations do not prove review separation or successful storage changes.
Consequence: Route, mode, or envelope changes can affect category and tile administration.
Owner: Unknown.
Next action: Retain separate maker and checker execution evidence.

### Analytics and proxy mediation

Fact: Client `/api/analytics/v1/fmo/print` and provider `v1/fmo/print` declarations have matching suffixes.
Evidence: [analytics client](../raw/2026-10-14-initial-repositories/mfe-base/src/analytics/index.ts.snapshot) and [analytics provider](../raw/2026-10-14-initial-repositories/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/AnalyticsController.java.snapshot).
Fact: The [proxy declaration](../raw/2026-10-14-initial-repositories/mfe-root-config/nginx/mfe.conf.L785-L807.snapshot) targets `ratan_backend_api_gateway` after prefix removal.
Consequence: Missing gateway evidence prevents a confirmed route from the browser to the provider.
Owner: Unknown.
Next action: Retain gateway route evidence and one reviewed analytics execution result.

## Dependencies

The inspected sources declare SystemJS, single-spa, React, Axios, and Spring controller interfaces.
The root proxy names `ratan_backend_api_gateway`.
The gateway implementation and active deployment configuration remain outside this evidence set.
Matching source declarations establish candidate compatibility only.

## Decisions

Keep these interfaces as candidates until owner review and routing gaps are resolved.
Record no approved business requirements or verified behavior from these declarations.
Keep initial local commits distinct from unavailable original repository history.
Owner: Unknown.
Next action: Assign repository owners and review the retained declarations before promotion.
