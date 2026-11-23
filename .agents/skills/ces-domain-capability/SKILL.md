---
name: ces-domain-capability
description: Explain CES entitlements and data scope, inspect API contracts and paired captures, reconcile access views, compare snapshots, and check sourced functional profile values. Use for CES integration and entitlement investigations.
---

# CES domain capability

Start at the [CES domain index](README.md). It links Contracts, Workflows, and Knowledge within this standalone folder.
The Workbench source checkout also exposes this library at `knowledge/integrations/ces/` through a directory link.
Scope each investigation to the application, principal, environment, and observation time or source revision.
Use the applicable policy and exact capture before making a claim about an account or resource.
Collect task inputs in a local copy of the [variable template](Workflows/variables.example.json).
Read the [variable guide](Workflows/variables.md) for bindings and keep private values outside this library.

| Task | Read |
| --- | --- |
| Explain assignments, feature actions, or record visibility | [Domain model](Knowledge/domain-model.md) and [source-bound facts](Knowledge/domain-facts.md) |
| Select an endpoint, schema, or paired case | [Contract guide](Contracts/README.md) and [OpenAPI subset](Contracts/openapi.yaml) |
| Inspect grants, reconcile three views, or compare captures | [Capture workflows and tools](Workflows/inspect-captures.md) |
| Check a sourced profile value or provisioning evidence | [Functional profile workflow](Workflows/functional-profile.md) |
| Verify provenance, uncertainty, or failure lessons | [Source register](Knowledge/sources.json) and workflow failure sections |

Run `Workflows/tools/inspect_ces.py` with Python 3.10 or newer. It reads local JSON and prints aggregate results.
Use the retained response examples through the [capture workflow](Workflows/inspect-captures.md#commands-and-outputs).
Report whether the evidence establishes a definition, an assignment, an effective feature action, or observed enforcement.
Resolve policy interpretation through the applicable approved source and its owner.
