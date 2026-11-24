## 1. Background

Due to the current policy situation in Indonesia, service data has been deployed in Indonesia.

- Opening Indonesia tiles loads its own container.js and cashflow-blotter.js, mfe-rules, nostro-static.js.
- Indonesia go-live will use independent CR processes and independent deployment pipelines. Indonesian features may differ from GDC.

## 2. Object

Exception to Indonesia-related UI packages are deployed to Indonesian servers.

And gdc and id tiles do not affect each other.

##

# 3. Blocks

| Option | Blocks | Solutions | | |
| --- | --- | --- | --- | --- |
| duplicate repo | sync code from GDC to Id repo (how to maintain later) | git remote + merge feature code | git remote add source-repo <repo url> git fetch source-repo git checkout feature/xxxx git merge --no-ff --allow-unrelated-histories source-repo/main | ![image-2026-6-23_14-37-48.png](attachments/image-2026-6-23_14-37-48.png) |
| git cherry-pick | git remote add source-repo <repo URL> git fetch source-repo git log source-repo/branch-name git cherry-pick <commit-hash> | ![image-2026-6-23_15-26-46.png](attachments/image-2026-6-23_15-26-46.png) |
| single repo | Ratan container dependencies at runtime @fm/ratan_container @fm/idns_ratan_container | when build webpack to switch import which one container | 1.package.json build: "cross-env REGION=ID concurrently npm:build:*", 2.webpack.config.js ``` const region = (process.env.REGION || "GDC").toUpperCase(); const containerPackage = region === "ID" ? "@fm/idns_ratan_container" : "@fm/ratan_container"; // single-spa default externals may externalize @fm/* first. // Put remap external in front so @fm/ratan_container can be rewritten by REGION. const defaultExternals = Array.isArray(defaultConfig.externals) ? defaultConfig.externals : [defaultConfig.externals].filter(Boolean); const remapContainerExternal = ({ request }, callback) => { if (request === "@fm/ratan_container") { return callback(null, containerPackage); } return callback(); }; defaultConfig.externals = [remapContainerExternal, ...defaultExternals]; ``` | ![image-2026-6-24_13-58-28.png](attachments/image-2026-6-24_13-58-28.png) ![image-2026-6-25_23-52-22.png](attachments/image-2026-6-25_23-52-22.png) ![image-2026-6-25_23-51-39.png](attachments/image-2026-6-25_23-51-39.png) |
| single repo | api prefix | env variable | | |
| duplicate/signle repo | global style | normal less→ mudule.less ant less→ module + :global(.ant-xxx) ag-grid less--delete | | |
| window.xxxx | | | |
| document.body | | | |
| Storage / Session / IndexedDB | env variable | | |

# ID bussiness

1. Trade blotter - cashflow details button support redirect to GDC and ID based on trade booking entity
2. ID blotters - booking entity fmid in drop down list should only include ID
3. Global rule real-time sync up from GDC to ID
4. Dashboard[ID] status cards support open Cashflow Blotter[ID]/Grouping Blotter[ID]