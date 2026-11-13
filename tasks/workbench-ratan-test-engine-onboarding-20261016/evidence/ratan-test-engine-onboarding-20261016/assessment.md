---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Ratan test engine onboarding assessment

- Repository ID: `ratan-test-engine`
- Source revision: `432f898f59fb06414bc14152d6e463a6a1f4eac2`
- Assessment date: `2026-10-16`
- Assessment mode: `assess`
- Dependency profile: `external-dependencies/1`
- Evidence register: [claims.json](claims.json)
- Check provenance: [provenance.json](provenance.json)
- Knowledge state: candidate documentation; human review remains pending.

## Purpose and ownership

The repository converts Excel case definitions into Robot Framework suites and keyword resources. (`PUR-001`, `GEN-001`, `GEN-002`)
It contains API suites, UI helpers, report tools, and an MCP keyword server. (`MCP-001`, `UI-001`, `OBS-001`, `TEST-001`)
These observations establish implementation responsibilities within this checkout.
They do not establish approved requirements or deployed service identities.
The current implementation and approval owners remain unknown. (`GAP-001`)

## Critical dependency summary

| Dependency and workflow | Consequence | Evidence and limit | Owner | Next action |
| --- | --- | --- | --- | --- |
| `D03-PRIVATE-CONFIG`: business suites | Missing environment settings or keys can prevent suite loading. | Inferred from imports; private values remain excluded. | unknown | Provision approved private inputs before integration execution. |
| `D15-PYTHON`: setup | Dependency routes can create different environments. | Conflicting Robot and Browser declarations; generator imports pandas. | unknown | Select a reproducible profile and resolve missing dependencies. |
| `D01-MCP`, `D02-LIBRARIES`: discovery | Startup can load executable Python libraries. | Observed library loading; import effects remain unverified. | unknown | Use static parsing for default agent discovery. |
| `D04-GENERATOR`: generation | RBT conversion removes existing destination files. | Observed source behavior; generator was not executed. | unknown | Generate in an isolated copy and review the differences. |
| `D11-MINIO`: uploads | Import can initiate an external upload attempt. | Inferred from an unconditional module-scope `main()` call. | unknown | Exclude uploader modules from automatic imports. |
| `D06-KAFKA`, `D07-KAFKA-HTTP`, `D08-POSTGRES`: integration | Execution can publish messages or change database state. | Observed write calls; deployed permissions remain unknown. | unknown | Confirm environment ownership and permitted operations. |
| `D10-TRUST`, `D16-AUTH`: credentials | Missing trust inputs can block authenticated workflows. | Observed credential mechanisms; effective grants remain unknown. | unknown | Confirm test identities and secure credential provisioning. |
| `D12-ADO`: report publication | The optional uploader has a syntax failure. | Static parsing failed; no upload executed. | unknown | Repair syntax before enabling this publication route. |

## Deployables and components

| Component | Responsibility | Source entrypoints | Evidence | Status |
| --- | --- | --- | --- | --- |
| Codeless generator | Read workbook sheets and generate Robot and RBT files. | `Codeless_v1.57.0.py` | `GEN-001`–`GEN-004` | observed |
| Robot suites and plugins | Exercise configured external application workflows. | `Tests/ratan/workspace/api/`, `Tests/ratan/plugin/api/` | `TEST-001`, `CFG-001` | observed within selected files |
| Shared keyword resources | Provide HTTP, identity, SQL, messaging, trust, and browser helpers. | `Resources/keywords/` | `API-001`, `AUTH-001`, `DATA-001`, `MSG-001`, `TRUST-001`, `UI-001` | observed within selected files |
| MCP server | Return keyword information and case skeletons over STDIO. | `rf_agent/server.py`, `rf_agent/scanner.py` | `MCP-001`–`MCP-004` | observed |
| Local result generation | Convert execution output into result JSON. | `GenResults.py`, `Resources/data/config/RunListener.py` | `OBS-001`, `OBS-002` | observed |
| Optional upload scripts | Publish selected files or report payloads. | `upload_folder_to_minio.py`, `upload_reports_to_ADO.py` | `STORE-001`–`STORE-003`, `OBS-003` | observed source declarations |

The MCP server is a local process interface.
No source evidence establishes a separately deployed repository service.
No cross-repository runtime relationship was verified.

## Interfaces and dependency details

The evidence register contains each relationship's attributes, claim references, status, and limits.
Unknown permissions remain unknown even when a protocol or caller is observed.

| Dependency | Operation and activation | Configuration and failure limits | Evidence |
| --- | --- | --- | --- |
| `D01-MCP` | Nine registered tools; entrypoint builds the index before STDIO startup. | Client authentication, authorization, and permitted callers remain unknown. | `MCP-001`, `MCP-002` |
| `D02-LIBRARIES` | Scanner uses `LibraryDocumentation` for local and installed Python libraries. | Loading errors are caught; module initialization effects remain unverified. | `MCP-003` |
| `D03-PRIVATE-CONFIG` | Suite imports load environment YAML, certificate references, and decryption keys. | `ENV` and `SECRET` select private inputs; their contents were excluded. | `CFG-001`, `CFG-002` |
| `D04-GENERATOR` | Manual invocation reads Excel sheets, writes Robot files, and converts API/UI RBT directories. | Defaults select `case_debug`; conversion clears destination files. | `GEN-001`–`GEN-003` |
| `D05-HTTP` | A conversion helper discovers a URL and sends `POST /v1/modelling/scbml/indexed`. | Effective server permissions, timeouts, retries, and deployment routing remain unknown. | `API-001`, `NET-001` |
| `D06-KAFKA` | Helpers create producers, produce caller messages, and flush. | `KAFKA_HOSTS` and `KAFKA_PORT` bind brokers; ACLs and delivery guarantees remain unknown. | `MSG-001` |
| `D07-KAFKA-HTTP` | Helper sends `POST /topic/${topic}/data` through a configured gateway. | Compression is conditional; gateway permissions and broker routing remain unknown. | `MSG-002` |
| `D08-POSTGRES` | Helper refreshes RATAN credentials, connects, and executes caller SQL. | Database selector expands settings; teardown disconnects; deployed grants remain unknown. | `DATA-001` |
| `D09-MYSQL` | Helper connects, queries caller SQL, converts date fields, and disconnects. | `mysql_*` settings select the datasource; ownership and transaction guarantees remain unknown. | `DATA-002` |
| `D10-TRUST` | Enabled refresh writes a temporary key, authenticates, and retrieves database credentials. | Environment branches select credential paths; login disables certificate verification; provisioning remains unknown. | `TRUST-001` |
| `D11-MINIO` | Module-scope `main()` activates recursive selection and object uploads. | Bucket permissions, retention, and production bindings remain unknown. | `STORE-001`–`STORE-003` |
| `D12-ADO` | Source declares two HTTP POST calls for case and result payloads. | Calls disable TLS verification; syntax failure prevents a passing local parse check. | `OBS-003`, `GAP-003` |
| `D13-DISCOVERY` | Helper requests `GET /eureka/apps` and selects an instance URL. | `ENV` and `forceDev` affect routing; private DNS and network controls remain unknown. | `NET-001`, `API-001` |
| `D14-BROWSER` | Helper creates a browser context and opens the supplied page URL. | Context ignores HTTPS errors; browser assets and deployment access remain unverified. | `UI-001` |
| `D15-PYTHON` | Project manifest requires Python 3.13; another delivery path uses Python 3.10. | Robot/Browser declarations differ; direct pandas and fastmcp declarations are absent. | `PKG-001`–`PKG-003`, `GEN-004`, `DEL-001` |
| `D16-AUTH` | Login sends credentials and extracts `Single-UI-Authorization`; caller saves tokens globally. | Payload entity names do not establish server authorization or effective grants. | `AUTH-001`, `AUTH-002` |
| `D17-GRPC` | Helper invokes `grpcurl` with a proto file, selected method, and token headers. | The command uses `-insecure`; deadlines, streaming, and remote permissions remain unknown. | `API-002` |

GenResults and RunListener currently generate local result JSON without invoking their commented MinIO upload calls. (`OBS-001`, `OBS-002`)
This distinction limits documentation claims about automatic report upload.
Package declarations for Redis do not establish an active Redis connection. (`PKG-001`)

## Dependency family coverage

The inventory enumerated 1,769 nonignored files without enumeration or category truncation.
The scanner found no test candidates because its filename rules did not identify the Robot suite layout.
Manual review inspected one suite's assertions and selected common helpers.
This review does not establish exhaustive suite, contract, or dependency coverage.

| Family | Disposition | Inspected scope and limits |
| --- | --- | --- |
| `api` | inspected | MCP, conversion HTTP, Kafka HTTP, and gRPC helpers; target server controls remain unavailable. |
| `messaging` | inspected | Direct Kafka producers; broker bindings and ACLs remain unresolved. |
| `managed-events` | not-observed | Selected entrypoints and common helpers; dynamic libraries can add relationships. |
| `data` | inspected | PostgreSQL and MySQL helpers; datasource values and deployed grants remain unavailable. |
| `identity` | inspected | Ratan login and token assignment; server authorization remains unknown. |
| `trust` | inspected | HashiCorp credential refresh and certificate references; secret contents remain excluded. |
| `configuration` | inspected | API/UI variable imports; private settings and key files remain excluded. |
| `storage` | inspected | Generator files and MinIO uploads; object permissions and retention remain unknown. |
| `network` | inspected | Eureka discovery; VPN, DNS, gateway, and deployment controls remain unavailable. |
| `platform` | not-observed | Selected helpers and delivery manifests; deployment environments remain unavailable. |
| `scheduling` | not-observed | Selected entrypoints and common helpers; no reviewed external scheduler binding was found. |
| `observability` | inspected | Local result generation and optional ADO uploads; external delivery remains unverified. |
| `frontend` | inspected | Browser context and navigation helpers; remote module dependencies remain unknown. |
| `business-provider` | not-observed | Selected entrypoints and helpers; business payloads and external providers remain outside this assessment. |
| `delivery` | inspected | Python manifests, container input, and dynamic library loading; full installation remains unverified here. |
| `other` | not-observed | No additional family was identified within the selected source scope. |

`not-observed` describes this review scope.
It does not establish production absence.
The original inventory excludes ignored key directories, reports, Git internals, and other omitted paths.
The tracked provenance retains those exclusions without machine paths.

## Readiness

| Dimension | Status | Evidence | Gap and next action |
| --- | --- | --- | --- |
| Repository identity | ready | Exact Git revision and inventory metadata | Preserve the assessed baseline when implementation changes. |
| Purpose and ownership | partial | `PUR-001`, `GEN-001`, `GAP-001` | Confirm the current implementation and approval owners. |
| Agent instructions | partial | `PUR-001`, `MCP-001`, `MCP-003` | Add native navigation and explicit offline versus integration commands. |
| Build and tests | partial | `PKG-001`–`PKG-003`, `TEST-001` | Resolve dependency gaps and retain authorized execution evidence. |
| Interface contracts | partial | `API-001`, `API-002`, `MSG-001` | Confirm peer contracts, endpoint bindings, and permissions. |
| Functional mapping | partial | `GEN-001`, `MCP-001`, `TEST-001` | Extend mapping only for the requested workflow. |
| Dependency visibility | partial | `D01-MCP`–`D17-GRPC` | Resolve private configuration, dynamic imports, and deployed controls. |
| Evidence governance | partial | Exact source citations and helper result | Candidate documentation still requires human review before publication. |

These ratings describe the baseline revision.
The parent adoption task records its later implementation and execution results separately.

## Findings

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| `F01`, P0: business execution inputs remain unavailable. | `CFG-001`, `CFG-002`, `DATA-001`, `MSG-001` | Business execution cannot establish a controlled environment from this evidence. | unknown | Confirm private inputs, environment ownership, and write permissions. |
| `F02`, P1: setup routes disagree. | `PKG-002`, `PKG-003`, `GEN-004`, `DEL-001` | Setup can omit required imports or select different runtime versions. | unknown | Define and validate one reproducible local setup profile. |
| `F03`, P1: MCP discovery loads executable libraries. | `MCP-002`, `MCP-003` | Keyword discovery can execute module initialization. | unknown | Make default discovery static; keep dynamic introspection explicit. |
| `F04`, P1: uploader import has side effects. | `STORE-002`, `STORE-003` | Automatic imports can initiate uploads. | unknown | Exclude uploaders from automatic discovery and isolate explicit upload commands. |
| `F05`, P1: default generation replaces RBT files. | `GEN-002`, `GEN-003` | An unreviewed run can replace generated assets. | unknown | Generate within an isolated copy and review destination differences. |
| `F06`, P1: automatic upload documentation conflicts with source. | `OBS-001`, `OBS-002`, `OBS-004` | Operators can expect report uploads that these close methods do not perform. | unknown | Document local result generation and separate upload entrypoints. |
| `F07`, P1: optional ADO uploader has invalid syntax. | Retained static parse failure; `GAP-003` | This upload route cannot start under the checked interpreter. | unknown | Repair syntax and retain a focused regression before activation. |
| `F08`, P1: source handles sensitive material unsafely. | `SEC-001`, `TRUST-001` | Literal authorization and key logging can expose sensitive material. | unknown | Move authorization into private inputs and remove key logging. |
| `F09`, P1: effective remote permissions remain unknown. | `AUTH-001`, `API-001`, `DATA-001`, `MSG-001` | Source calls do not establish authorized access to the selected environment. | unknown | Obtain owner review for the requested integration workflow. |

### Candidate acceptance criteria

These criteria describe adoption checks.
They do not record business approval.

```gherkin
Scenario: Discover repository assets without private configuration
  Given the checkout has no private environment YAML or key files
  When an agent runs the default offline discovery command
  Then the command lists the selected source assets
  And the command performs zero remote requests and zero business suite executions

Scenario: Identify external execution requirements
  Given an agent selects a business integration suite
  When the agent reads the repository execution guide
  Then the guide names its private configuration requirements
  And the guide states its external write operations and unresolved permissions

Scenario: Retain exact onboarding evidence
  Given the checkout remains at the assessed revision
  When the evidence helper checks the original staging report
  Then all cited bytes match their committed source blobs
  And each dependency family has exactly one coverage disposition
```

## Checks and execution limits

| Check | Actual result | Limit |
| --- | --- | --- |
| Static filename inventory | PASSED | Enumerated 1,769 files; source and test classification needed manual supplementation. |
| Original evidence helper | PASSED | 38 claims and 17 dependency records passed the exact-byte and structure checks. |
| Family coverage structure | PASSED | All 16 family keys are present; structure does not establish exhaustive discovery. |
| Optional uploader syntax | FAILED | `ast.parse` failed at `upload_reports_to_ADO.py:77` under Python 3.14.5. |
| Target build and business tests | NOT RUN | This assessment used static inspection only. |
| Remote services and uploads | NOT RUN | Connectivity, remote grants, and behavior remain unknown. |
| Catalog validation | NOT RUN | The parent adoption task owns catalog changes and validation. |
| Portable bundle checks | PASSED | JSON parsing, citation hashes, local links, and machine-path checks. |
| ASD writing review | PENDING | Automated checks do not establish complete ASD-STE100 compliance. |

Evidence validation checks source bytes and report structure.
It does not establish semantic truth, effective permissions, runtime behavior, or approval.
This bundle contains no raw source snapshot, credentials, customer data, or trading payloads.
