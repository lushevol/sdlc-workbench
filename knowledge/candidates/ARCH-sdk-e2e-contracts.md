---
type: Architecture
id: ARCH-sdk-e2e-contracts
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: repos/libraries/single-ui-sdk-starter/pom.xml
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: 757c76776c7530b9dc60f9a3b7d58beb061d52181e3c9ec671ba6a64d4739317
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/pom.xml
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: 88c5d40332aa1cc97a9a90509c1263c5d0911642cd014f26369bca015dd27d67
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: 061a01d18973cf37e7d85dbc6b7af6670dc37bfdc7098cea3c5470a47cda90ec
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/resources/spring.factories
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: 25ebf1ff3d5e42cfa09254e7622dfad05dc74e4075b8bc68d6efd584c9b24823
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/config/AuthConfiguration.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: 48cfea2643775aa3c936e8391a0f2c1bcdba9a540e4b7761848a35906793ecba
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/config/JwtConfiguration.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: 16b26fc91139bf411d7486269ce8cdb6276dbf05de9caf5cc4301e9bb3594e21
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/properties/AuthProperties.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: d41ab828e2295fa4e5d4ccbe87d8a80e54522e0aa9df88f9dd8bfd085d09274f
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/filter/AuthTokenFilter.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: dd0c58c0f226a28ca7eab10d8a7955baa30061c192008dc77b1096b6e574ee9d
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/util/JwtTokenUtil.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: 09d8595302dd702b8f38c298ff9e5a91f6107678ffd61714b540253605bcc161
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/AuthorizationService.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: cc81a872b3565aa58175e6f8630667e776d102e0ebc160d488f4ce0691f5edab
- resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java
  revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
  sha256: 74587cf78a69e0c9b7b3920d510248acd5501dbaa7ac27035b3b9c5fc91bc2d1
- resource: repos/testing/ratan-test-engine/pyproject.toml
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 58810bf51b08a6ecef6c9f914aff1b2c3ced0edaa8d5656f2d28a9a81473893b
- resource: repos/testing/ratan-test-engine/Tests/ratan/workspace/api/__import__.resource
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 97458afc9c089f76e1f07fff8164c81b3b67447f58fb2093576a09e647bb943b
- resource: repos/testing/ratan-test-engine/Tests/ratan/workspace/ui/__import__.resource
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: a8fe3c80eebb9286747d79c518b52466827c994ca279b84a763facdee7ff48d8
- resource: repos/testing/ratan-test-engine/Install/image/robot/Dockerfile
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 1236a477935816bb874bb399f94bfd983fcd12a3ae69814784542b82e94764b3
- resource: repos/testing/ratan-test-engine/Install/image/ui/Dockerfile
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: c70587fd635670997a244684a7dd0e4147150b002fd95cb96d02445be3587008
- resource: repos/testing/ratan-test-engine/rf_agent/server.py
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 58b1c96cd49ab35a5f5d294ec50c4cbb0ef2bdfb995c0740323ad048dbd9b37d
- resource: repos/testing/ratan-test-engine/rf_agent/scanner.py
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: d8aa63e603c7455cbe54ff54f807783dd528a0bea1f051d2f4eaad1efadb8089
- resource: repos/testing/ratan-test-engine/CLAUDE.md#L94-L117
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 40b8262070400476dd29d13dcea323a0d2eff879afcaaa038e428c80a604e40f
- resource: repos/testing/ratan-test-engine/Codeless_v1.57.0.py#L1196-L1244
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: d4117bf5f6b379236ccb782c821a49997db149bb6ec3b87002422b36a097882b
- resource: repos/testing/ratan-test-engine/Codeless_v1.57.0.py#L1254-L1304
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: f503b5bbdd8d904eccdaf821997ed9247c0191dac78cc3f41539fc0c4a800b4a
- resource: repos/testing/ratan-test-engine/GenResults.py#L27-L39
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 80eb3ca34b7e3f462e9fa130d30ad62f49f0a19514fb3d40c11d2694a9e52de6
- resource: repos/testing/ratan-test-engine/GenResults.py#L149-L163
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 54fdbc5daeff83f673742d39aa1a7919c3ddf5ba1ee1d90e9e0ad76c3def6913
- resource: repos/testing/ratan-test-engine/GenResults.py#L188-L205
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 93ee5ed8f1c33b11c8eac26c88aa5e64f65ad1f32395bf53f17dc93e0f980f38
- resource: repos/testing/ratan-test-engine/GenResults.py#L261-L299
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 5c4938bb9ed5dc9d8081ee6350054c7215916f7ff23b32da379987cb038e3907
- resource: repos/testing/ratan-test-engine/GenResults.py#L301-L303
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 68f6d95d4f288379247f8a25e815f94c01abdf792a909d0287e187b5a9c39fc1
- resource: repos/testing/ratan-test-engine/GenResults.py#L309-L331
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: b6f46cc71b2728cd68f5b5809cf0430141954372c52f6bba3bc0e32f6cbace94
- resource: repos/testing/ratan-test-engine/Resources/keywords/commonBiz.resource#L112-L129
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 47098b075583c9fee6e8fec608ad21595e97afe7096700072ec763d1839cd33b
- resource: repos/testing/ratan-test-engine/Resources/keywords/commonBiz.resource#L144-L153
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: 8c0a23c52576d08d03612d79167b6bee7aa51412bfd6dab78358b27ca8a761e6
- resource: repos/testing/ratan-test-engine/Tests/ratan/workspace/ui/UI-E2E-UIFOUNDATION-BUGS.robot#L11-L37
  revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
  sha256: c439b624e3c6eb69a3cca4ea763e3f0a890ba65d0bc24c6b9c4b3f937277d242
- resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java
  revision: 091c9d16c13f285a78463ff0235c21b152844b61
  sha256: c5cb0cb4a7a00663deaaa169837cd607bbaf35f8bf3eda04ffbe951b246d06af
- resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/Constant.java
  revision: 091c9d16c13f285a78463ff0235c21b152844b61
  sha256: 63ddf339505d0971919a513ef088e417bf4fd27d196f912132ebe6788bf1a3ac
- resource: repos/sdk-e2e-initial-local-baselines
  revision: sha256:04ed9c50612ecdd92bb5376e0d3ee543243b9c5fdc07f35b2556ad1b6dd3c841
  sha256: 04ed9c50612ecdd92bb5376e0d3ee543243b9c5fdc07f35b2556ad1b6dd3c841
generated:
  by: agent:codex
  at: '2026-10-14T01:33:53.488111+00:00'
verified: []
scope: Record SDK and test-engine interface declarations at their initial local commits.
components:
- single-ui-auth-sdk supplies a Spring token filter, JWT utilities, and EMS2 entitlement lookup.
- ratan-test-engine supplies Robot suites, generation scripts, result export, and keyword discovery.
- single-ui-bff supplies the related Single UI token format.
interfaces:
- single-ui-sdk-autoconfiguration
- single-ui-sdk-jwt-validation
- single-ui-sdk-request-context
- single-ui-sdk-entitlement-lookup
- ratan-robot-suite-execution
- ratan-excel-robot-generation
- ratan-robot-result-export
- ratan-keyword-mcp
- single-ui-sso-token-family
dependencies:
- The SDK declares Java 17, Spring Boot 4.0.6, java-jwt, Jackson, and an EMS2 host.
- Robot suites need Python dependencies, environment variables, configuration, credentials, keys, and
  reachable services.
- MCP startup needs FastMCP, Robot parsing, and inspected library imports.
decisions:
- Keep all added interface records as candidates pending owner review and execution evidence.
- Keep SDK authentication separate from unproved downstream permission enforcement.
- Keep source assertions separate from passing business execution.
- Bind evidence to local initial commits without claiming original repository history.
contract_candidates:
- id: single-ui-sdk-autoconfiguration
  type: deployment
  provider_repository_ids:
  - single-ui-auth-sdk
  consumer_repository_ids: []
  evidence:
  - resource: repos/libraries/single-ui-sdk-starter/pom.xml
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: 757c76776c7530b9dc60f9a3b7d58beb061d52181e3c9ec671ba6a64d4739317
  - resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/pom.xml
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: 88c5d40332aa1cc97a9a90509c1263c5d0911642cd014f26369bca015dd27d67
  - resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: 061a01d18973cf37e7d85dbc6b7af6670dc37bfdc7098cea3c5470a47cda90ec
  - resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/resources/spring.factories
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: 25ebf1ff3d5e42cfa09254e7622dfad05dc74e4075b8bc68d6efd584c9b24823
  - resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/config/AuthConfiguration.java
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: 48cfea2643775aa3c936e8391a0f2c1bcdba9a540e4b7761848a35906793ecba
  - resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/config/JwtConfiguration.java
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: 16b26fc91139bf411d7486269ce8cdb6276dbf05de9caf5cc4301e9bb3594e21
  observed_declaration:
  - The parent declares Java 17 and Spring Boot 4.0.6.
  - The Maven module identity is com.scb.fmoportal:fmoportal-auth-sdk:2.0.0-SNAPSHOT.
  - Both Spring metadata files name JwtConfiguration and AuthConfiguration.
  - AuthConfiguration enables filter and entitlement beans when fmoportal.auth.enabled is true or absent.
  - JwtConfiguration independently declares JWT utilities and configuration properties.
  consequence: A downstream service needs the SDK dependency and compatible Spring configuration.
  documentation_gap: No consuming service, successful build, or Spring startup result was retained.
  owner: unknown
  next_action: Identify a current consuming service and retain its dependency and startup evidence.
- id: single-ui-sdk-jwt-validation
  type: http
  provider_repository_ids:
  - single-ui-auth-sdk
  consumer_repository_ids: []
  evidence:
  - resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/properties/AuthProperties.java
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: d41ab828e2295fa4e5d4ccbe87d8a80e54522e0aa9df88f9dd8bfd085d09274f
  - resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/filter/AuthTokenFilter.java
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: dd0c58c0f226a28ca7eab10d8a7955baa30061c192008dc77b1096b6e574ee9d
  - resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/util/JwtTokenUtil.java
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: 09d8595302dd702b8f38c298ff9e5a91f6107678ffd61714b540253605bcc161
  - resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java
    revision: 091c9d16c13f285a78463ff0235c21b152844b61
    sha256: c5cb0cb4a7a00663deaaa169837cd607bbaf35f8bf3eda04ffbe951b246d06af
  - resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/Constant.java
    revision: 091c9d16c13f285a78463ff0235c21b152844b61
    sha256: 63ddf339505d0971919a513ef088e417bf4fd27d196f912132ebe6788bf1a3ac
  observed_declaration:
  - The filter reads Single-UI-Authorization and splits its value on Bearer followed by one space.
  - JWT validation uses RSA512 and the configured pub public key.
  - Normal tokens require issuer single-ui-bff and reject an expired optional max_age.
  - Entitlement tokens require issuer single-ui-bff-entitlement and return the entitlements claim as text.
  - Invalid entitlement tokens return null.
  - The BFF declares the same header, RSA512 algorithm, issuer names, and max_age claim.
  consequence: The declared token format supports a candidate relationship between BFF issuance and SDK
    validation.
  documentation_gap: Configured key compatibility and successful token validation remain unproved.
  owner: unknown
  next_action: Compare deployed public keys and retain allowed and rejected token execution results.
  inferred_relationship: Matching source declarations suggest format compatibility. They do not prove
    deployed connectivity.
  related_repository_ids:
  - single-ui-bff
- id: single-ui-sdk-request-context
  type: data
  provider_repository_ids:
  - single-ui-auth-sdk
  consumer_repository_ids: []
  evidence:
  - resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/config/AuthConfiguration.java
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: 48cfea2643775aa3c936e8391a0f2c1bcdba9a540e4b7761848a35906793ecba
  - resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/properties/AuthProperties.java
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: d41ab828e2295fa4e5d4ccbe87d8a80e54522e0aa9df88f9dd8bfd085d09274f
  - resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/filter/AuthTokenFilter.java
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: dd0c58c0f226a28ca7eab10d8a7955baa30061c192008dc77b1096b6e574ee9d
  - resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/util/JwtTokenUtil.java
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: 09d8595302dd702b8f38c298ff9e5a91f6107678ffd61714b540253605bcc161
  observed_declaration:
  - A configured skip header bypasses checks when its incoming request value is nonempty.
  - URL exclusions take precedence. Empty includeUrls protects all remaining URLs.
  - When present, id maps to sessionId and sub maps to userId in the serialized JSON userInfo request attribute.
  - The attribute contains version as string 3 and copies optional oud and entitlements claims.
  - Validation exceptions return HTTP 401 with a JSON message.
  - A final logout URL segment adds an available session ID to the filter instance rejection list.
  consequence: Downstream code must read request attributes and account for configured bypasses and local
    session state.
  documentation_gap: Distributed revocation and downstream action or role enforcement remain unproved.
  owner: unknown
  next_action: Inspect a consuming service, its trusted bypass configuration, and its permission checks.
- id: single-ui-sdk-entitlement-lookup
  type: http
  provider_repository_ids:
  - single-ui-auth-sdk
  consumer_repository_ids: []
  evidence:
  - resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/config/AuthConfiguration.java
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: 48cfea2643775aa3c936e8391a0f2c1bcdba9a540e4b7761848a35906793ecba
  - resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/properties/AuthProperties.java
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: d41ab828e2295fa4e5d4ccbe87d8a80e54522e0aa9df88f9dd8bfd085d09274f
  - resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/filter/AuthTokenFilter.java
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: dd0c58c0f226a28ca7eab10d8a7955baa30061c192008dc77b1096b6e574ee9d
  - resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/AuthorizationService.java
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: cc81a872b3565aa58175e6f8630667e776d102e0ebc160d488f4ce0691f5edab
  - resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: 74587cf78a69e0c9b7b3920d510248acd5501dbaa7ac27035b3b9c5fc91bc2d1
  observed_declaration:
  - AuthorizationService exposes getEntitlements(userId).
  - The implementation gets roles from /ems2/rest/account/%s.
  - It posts a user ID to entity-name list mapping to /ems2/rest/entitlements/entitlementList.
  - Optional entityList configuration filters entity names.
  - The result maps entityName:roleName to subject names and action-name lists.
  - Lookup failures return empty lists or maps. Default connection and read timeouts are 10 and 30 seconds.
  - AuthTokenFilter does not call AuthorizationService.
  consequence: Entitlement lookup supplies data. A downstream caller must apply its permission policy.
  documentation_gap: EMS2 ownership, consuming permission checks, and successful lookup execution remain
    unknown.
  owner: unknown
  next_action: Identify the EMS2 owner and inspect a downstream allow or deny decision.
- id: ratan-robot-suite-execution
  type: deployment
  provider_repository_ids:
  - ratan-test-engine
  consumer_repository_ids: []
  evidence:
  - resource: repos/testing/ratan-test-engine/pyproject.toml
    revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
    sha256: 58810bf51b08a6ecef6c9f914aff1b2c3ced0edaa8d5656f2d28a9a81473893b
  - resource: repos/testing/ratan-test-engine/Tests/ratan/workspace/api/__import__.resource
    revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
    sha256: 97458afc9c089f76e1f07fff8164c81b3b67447f58fb2093576a09e647bb943b
  - resource: repos/testing/ratan-test-engine/Tests/ratan/workspace/ui/__import__.resource
    revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
    sha256: a8fe3c80eebb9286747d79c518b52466827c994ca279b84a763facdee7ff48d8
  - resource: repos/testing/ratan-test-engine/Install/image/robot/Dockerfile
    revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
    sha256: 1236a477935816bb874bb399f94bfd983fcd12a3ae69814784542b82e94764b3
  - resource: repos/testing/ratan-test-engine/Install/image/ui/Dockerfile
    revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
    sha256: c70587fd635670997a244684a7dd0e4147150b002fd95cb96d02445be3587008
  - resource: repos/testing/ratan-test-engine/CLAUDE.md#L94-L117
    revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
    sha256: 40b8262070400476dd29d13dcea323a0d2eff879afcaaa038e428c80a604e40f
  - resource: repos/testing/ratan-test-engine/Tests/ratan/workspace/ui/UI-E2E-UIFOUNDATION-BUGS.robot#L11-L37
    revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
    sha256: c439b624e3c6eb69a3cca4ea763e3f0a890ba65d0bc24c6b9c4b3f937277d242
  observed_declaration:
  - The package declares Python 3.13 or later and Robot Framework 7.2.2.
  - API and UI import resources resolve env_${ENV}_${SECRET}.yaml and decryption key paths.
  - The UI import resource also resolves certificate configuration.
  - Source instructions describe suite paths, tag selection, environment variables, listener use, and
    parallel execution.
  - Both inspected container commands default to robot --dryrun.
  - One inspected UI test asserts a filter item count of at least two.
  consequence: Business execution needs selected suites, dependencies, configuration, credentials, keys,
    and accessible services.
  documentation_gap: Source assertions establish test intent. No retained execution establishes passing
    behavior or complete coverage.
  owner: unknown
  next_action: Identify the suite owner and retain approved scope, assertion review, and execution evidence.
- id: ratan-excel-robot-generation
  type: data
  provider_repository_ids:
  - ratan-test-engine
  consumer_repository_ids: []
  evidence:
  - resource: repos/testing/ratan-test-engine/Codeless_v1.57.0.py#L1196-L1244
    revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
    sha256: d4117bf5f6b379236ccb782c821a49997db149bb6ec3b87002422b36a097882b
  - resource: repos/testing/ratan-test-engine/Codeless_v1.57.0.py#L1254-L1304
    revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
    sha256: f503b5bbdd8d904eccdaf821997ed9247c0191dac78cc3f41539fc0c4a800b4a
  observed_declaration:
  - CLI arguments select a workbook, colon-separated sheet names, and excluded sheet names.
  - The generator reads workbooks below Tests/ratan/cases/api.
  - Sheet selectors beginning with kw_ write API plugin resources. Other selectors write API workspace
    files.
  - Source generation writes output files. Conversion clears existing rbt-api and rbt-ui directory contents.
  - Robot conversion writes suite JSON to files with the .rbt suffix.
  consequence: Generation changes source files and replaces conversion outputs.
  documentation_gap: Workbook semantics and generated outputs remain unreviewed. No generation was executed.
  owner: unknown
  next_action: Review a current workbook and its expected output before running generation.
- id: ratan-robot-result-export
  type: data
  provider_repository_ids:
  - ratan-test-engine
  consumer_repository_ids: []
  evidence:
  - resource: repos/testing/ratan-test-engine/GenResults.py#L27-L39
    revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
    sha256: 80eb3ca34b7e3f462e9fa130d30ad62f49f0a19514fb3d40c11d2694a9e52de6
  - resource: repos/testing/ratan-test-engine/GenResults.py#L149-L163
    revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
    sha256: 54fdbc5daeff83f673742d39aa1a7919c3ddf5ba1ee1d90e9e0ad76c3def6913
  - resource: repos/testing/ratan-test-engine/GenResults.py#L188-L205
    revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
    sha256: 93ee5ed8f1c33b11c8eac26c88aa5e64f65ad1f32395bf53f17dc93e0f980f38
  - resource: repos/testing/ratan-test-engine/GenResults.py#L261-L299
    revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
    sha256: 5c4938bb9ed5dc9d8081ee6350054c7215916f7ff23b32da379987cb038e3907
  - resource: repos/testing/ratan-test-engine/GenResults.py#L301-L303
    revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
    sha256: 68f6d95d4f288379247f8a25e815f94c01abdf792a909d0287e187b5a9c39fc1
  - resource: repos/testing/ratan-test-engine/GenResults.py#L309-L331
    revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
    sha256: b6f46cc71b2728cd68f5b5809cf0430141954372c52f6bba3bc0e32f6cbace94
  observed_declaration:
  - The exporter reads Robot XML through ExecutionResult.
  - CLI inputs select testRunId, xml_path, and xml_files.
  - PASS and SKIP both become exported PASSED.
  - The exported passed count and passrate numerator add passed and skipped counts.
  - close writes result.json. Its normal upload call is commented out.
  - The CLI also removes Report/pabot_results and copies browser screenshots and videos.
  consequence: Exported PASSED cannot distinguish skipped tests from tests with passing assertions.
  documentation_gap: No retained execution was reviewed. Expected business reporting semantics remain
    unknown.
  owner: unknown
  next_action: Review reporting semantics and retain original XML with any execution claim.
- id: ratan-keyword-mcp
  type: data
  provider_repository_ids:
  - ratan-test-engine
  consumer_repository_ids: []
  evidence:
  - resource: repos/testing/ratan-test-engine/rf_agent/server.py
    revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
    sha256: 58b1c96cd49ab35a5f5d294ec50c4cbb0ef2bdfb995c0740323ad048dbd9b37d
  - resource: repos/testing/ratan-test-engine/rf_agent/scanner.py
    revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
    sha256: d8aa63e603c7455cbe54ff54f807783dd528a0bea1f051d2f4eaad1efadb8089
  observed_declaration:
  - The MCP server exposes nine tools over STDIO.
  - Tools search keywords, inspect details, list sources, list source keywords, and return import blocks.
  - Other tools generate skeleton text, report index statistics, refresh the index, and find case examples.
  - Skeleton generation returns text with TODO placeholders. It does not write a case file.
  - Startup builds the keyword index before starting the STDIO server.
  - The scanner parses Robot resources and loads Python or installed libraries through libdoc.
  consequence: Keyword discovery can load Python library code during startup and refresh.
  documentation_gap: Library import side effects, dependencies, and operational results remain unverified.
  owner: unknown
  next_action: Inspect library import behavior before approving an MCP execution configuration.
  tool_names:
  - search_keywords
  - get_keyword_detail
  - list_keyword_sources
  - list_keywords_in_source
  - get_import_block
  - generate_case_skeleton
  - get_index_stats
  - refresh_index
  - find_case_examples
- id: single-ui-sso-token-family
  type: http
  provider_repository_ids:
  - single-ui-bff
  consumer_repository_ids:
  - single-ui-auth-sdk
  - ratan-test-engine
  evidence:
  - resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/filter/AuthTokenFilter.java
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: dd0c58c0f226a28ca7eab10d8a7955baa30061c192008dc77b1096b6e574ee9d
  - resource: repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/util/JwtTokenUtil.java
    revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
    sha256: 09d8595302dd702b8f38c298ff9e5a91f6107678ffd61714b540253605bcc161
  - resource: repos/testing/ratan-test-engine/Resources/keywords/commonBiz.resource#L112-L129
    revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
    sha256: 47098b075583c9fee6e8fec608ad21595e97afe7096700072ec763d1839cd33b
  - resource: repos/testing/ratan-test-engine/Resources/keywords/commonBiz.resource#L144-L153
    revision: 432f898f59fb06414bc14152d6e463a6a1f4eac2
    sha256: 8c0a23c52576d08d03612d79167b6bee7aa51412bfd6dab78358b27ca8a761e6
  - resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java
    revision: 091c9d16c13f285a78463ff0235c21b152844b61
    sha256: c5cb0cb4a7a00663deaaa169837cd607bbaf35f8bf3eda04ffbe951b246d06af
  - resource: repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/Constant.java
    revision: 091c9d16c13f285a78463ff0235c21b152844b61
    sha256: 63ddf339505d0971919a513ef088e417bf4fd27d196f912132ebe6788bf1a3ac
  observed_declaration:
  - The SDK consumes the BFF token format. It does not call the login endpoint.
  - RATAN LOGIN posts supplied credentials and entity names to /api/auth/v2/sso/login.
  - The Robot request expects HTTP 200 and asserts result equals success or Boolean true.
  - The keyword returns the Single-UI-Authorization response header.
  - GET RATAN TOKEN splits supplied username|password values and stores returned tokens as global variables.
  consequence: The existing authentication contract gains separate token-validation and login-keyword
    consumers.
  documentation_gap: Configured key compatibility, deployed routing, and passing login execution remain
    unproved.
  owner: unknown
  next_action: Confirm routing and keys, then retain login and SDK validation execution evidence.
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---
# SDK and E2E interface candidates

## Scope

This candidate records eight new interfaces and an extension to the existing Single UI authentication contract.
The [baseline inventory](../raw/2026-10-14-sdk-e2e-registration/initial-baselines.json) identifies independent local source commits.
Original repository history and business ownership remain unknown.
No source declaration establishes business approval or passing execution.

## Components

- `single-ui-auth-sdk` identifies the supplied Maven authentication library.
- `ratan-test-engine` identifies the supplied Robot Framework project.
- `single-ui-bff` declares the related token producer format.

The SDK lives in the supplied `single-ui-sdk-starter` directory.
Its Maven module is `com.scb.fmoportal:fmoportal-auth-sdk:2.0.0-SNAPSHOT`.
No inspected downstream service establishes SDK adoption.

## Interfaces

The structured interface entries retain exact evidence references, observed declarations, consequences, unknown owners, and next actions.
Four new SDK contracts cover configuration, JWT validation, request attributes, and entitlement lookup.
Four new test contracts cover suite inputs, Excel generation, result export, and keyword MCP tools.
The existing `single-ui-sso-token-family` contract gains SDK token-format consumption and Robot login-keyword consumption.

The SDK filter authenticates tokens and writes the serialized JSON `userInfo` request attribute.
A configured skip header bypasses checks when its incoming request value is nonempty.
URL exclusions also bypass checks.
Logout adds an available session ID to the filter instance rejection list.
Entitlement lookup remains separate from the filter.
Downstream action or role enforcement remains unproved.

The Robot login keyword expects HTTP 200 and asserts `success` or Boolean `true` in the response result.
The inspected UI test asserts at least two filter items.
These assertions establish test intent only.
No retained execution proves their results.

The result exporter maps both `PASS` and `SKIP` to `PASSED`.
Consumers cannot use exported `PASSED` alone to establish executed assertions.
The [result finding](../findings/FND-ratan-skipped-result-status.md) records this evidence limit.
The [SDK finding](../findings/FND-sdk-authorization-enforcement.md) records the permission enforcement gap.

## Dependencies

Spring loading, configured key compatibility, EMS2 responses, and downstream permission checks require separate evidence.
Robot execution needs environment configuration, credentials, keys, dependencies, and reachable services.
Both inspected container defaults use `robot --dryrun`.
Keyword MCP startup can import Python libraries through Robot libdoc.
Excel generation and result export write files and can remove existing generated outputs.

## Decisions

Keep these records as draft candidates.
Keep executable tool registration separate from source interface declarations.
Retain original Robot XML before making behavior claims from exported results.
Retain new source snapshots when implementation changes.
Owner: unknown.
