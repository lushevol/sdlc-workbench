---
name: ces-domain-capability
description: Explain CES entitlements and data scope, inspect CES response contracts, and compare effective access across captured snapshots. Use for CES access questions, contract checks, and entitlement investigations.
---

# CES domain capability

Scope each investigation to the CES application, principal, environment, and observation time or source revision.
Use the applicable policy and exact capture before making a claim about an account or resource.
Collect task inputs in a local copy of the [variable template](assets/variables.example.json). Read the [variable guide](references/variables.md) for bindings.

| Task | Read |
| --- | --- |
| Explain entitlement assignments, feature actions, or record visibility | [CES domain model](references/domain-model.md) |
| Select a catalog, effective-user, or assigned-role response | [CES response contracts](references/contracts.md) |
| Trace effective access or compare two captures | [CES workflows and commands](references/workflows.md) |
| Check a functional profile value or review provisioning evidence | [Functional profile checks](references/functional-profile.md) |

Run `scripts/inspect_ces.py` with Python 3.10 or newer. The script reads local JSON and prints aggregate results.
Use the included synthetic examples to check the command from any copy of the skill folder.
Report whether the evidence establishes a definition, an assignment, an effective feature action, or observed enforcement.
Resolve policy interpretation through the applicable approved source and its owner.
