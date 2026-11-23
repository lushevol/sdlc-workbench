# CES integration

Use this library to inspect CES interfaces, entitlement assignments, effective access, and scoped data restrictions.
The same maintained files serve Workbench discovery and standalone copies.
All commands read local evidence. Documented routes and captured origins grant no execution permission.

## Contracts

| View | Contract and examples | Evidence scope |
| --- | --- | --- |
| Application catalog | [OpenAPI subset](Contracts/openapi.yaml), [contract guide](Contracts/README.md) | Retained UAT GET exchanges; application identity comes from the request |
| Effective user | [OpenAPI subset](Contracts/openapi.yaml), [contract guide](Contracts/README.md) | Retained UAT GET exchanges; match request and response identity |
| Assigned roles | [OpenAPI subset](Contracts/openapi.yaml), [contract guide](Contracts/README.md) | Supplied SDK body fixture; HTTP result and capture time remain unknown |

## Workflows

- [Inspect, attribute, compare, and reconcile captures](Workflows/inspect-captures.md).
- [Check a sourced functional profile value and provisioning evidence](Workflows/functional-profile.md).
- [Variable definitions](Workflows/variables.md) and [safe template](Workflows/variables.example.json).
- [Offline inspector](Workflows/tools/inspect_ces.py). Requires Python 3.10 or newer and the standard library.

## Knowledge

- [Access concepts, policy interpretation, and ownership](Knowledge/domain-model.md).
- [Scoped domain facts and limitations](Knowledge/domain-facts.md).
- [Exact source identities, hashes, revisions, and locators](Knowledge/sources.json).

## Material limits

Captured schemas describe observed shapes and inspector requirements, not service-wide guarantees.
Assigned roles preserve attribution; flattened effective grants do not recover that attribution.
Data-policy precedence, complete pagination, authorization errors, and live provisioning need scoped evidence.
The functional-profile wire location and empty value remain unresolved.
Offline matches do not establish deployed enforcement, business acceptance, or entitlement-change authorization.

In Workbench, canonical business intent remains in `knowledge/records/`. Original captures remain in their owning tasks.
Copy this skill folder to use the library outside Workbench. Its internal links and tools remain local.
