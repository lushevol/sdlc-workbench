# Registry proposal contracts

ADE's central registries are source-of-truth **after review**. Never overwrite them during initial onboarding.

## Responsibilities

- `registry/repositories.yaml`: checkout location, Git origin/revision, source stacks, build/test entry points, governance owner and association to deployables. **One entry per source repository**.
- `registry/services.yaml`: logical deployable boundaries, endpoints, published/consumed contracts, transports and dependency edges. **Not one-to-one with repositories**.
- `registry/capabilities.yaml`: stable business capability identifiers, participating services/components, requirements and test references. **Capabilities may span repositories**.
- `components.proposed.yaml`: reusable per-repository functional components, responsibilities, entrypoint/path patterns and evidence IDs. May ultimately belong in ADE's curated knowledge rather than in the source repo.

## YAML example — proposals only

`repositories.proposed.yaml`:

```yaml
schema_version: '1.0'
repositories:
  - id: settlement-service
    path: repos/settlement-service
    revision: REPLACE_WITH_SCANNED_SHA
    type: backend
    languages: [java]
    service_ids: [settlement-api]
    build_manifest: pom.xml
    owner: review_required
    status: proposed
```

`services.proposed.yaml`:

```yaml
schema_version: '1.0'
services:
  - id: settlement-api
    repository_id: settlement-service
    kind: spring-boot-service
    provides:
      - id: settlement-graphql
        transport: graphql
        contract_path: src/main/resources/schema/settlement.graphqls
        evidence_ids: [INT-001]
    consumes: []
    status: proposed
```

`capabilities.proposed.yaml`:

```yaml
schema_version: '1.0'
capabilities:
  - id: settlement-exception-management
    description: Manage settlement exceptions
    implemented_by:
      - repository_id: settlement-service
        component_id: exception-api
        evidence_ids: [CMP-001]
    requirements: [] # unknown until mapped to governed requirements
    tests: []        # unknown until mapped to actual tests
    status: proposed
```

`components.proposed.yaml`:

```yaml
schema_version: '1.0'
repository_id: settlement-service
components:
  - id: exception-api
    business_function: Settlement exception processing
    responsibility: Handle exception queries and actions
    entrypoints: [src/main/java/example/ExceptionController.java]
    path_patterns: [src/main/java/example/exception/**]
    contracts: [settlement-graphql]
    tests: []
    evidence_ids: [CMP-001, INT-001]
    status: proposed
```

The examples illustrate relationships, **not actual findings**. IDs/paths must be adapted to repository evidence. Never copy fictional IDs into approved registries. For cross-repository edges require a second-repository corroboration or an authoritative contract and label the edge `candidate` until then.
