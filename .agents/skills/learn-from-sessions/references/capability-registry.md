# Retrieve and reconcile capabilities

Use this mode when a task needs scoped Workbench rules or produces a supported reusable registry claim.
It reuses existing `learning` operations. Session extraction can proceed without the runtime or native hooks.

## Retrieve at entry

```sh
ai-sdlc --workspace . learning list --query TERMS
ai-sdlc --workspace . learning use CAPABILITY_ID --scope '{"system":"SYSTEM"}'
```

Read linked skills, contracts, exact selectors, and permission requirements before applying a rule.
Keep current sources and tested conditions visible.
Missing selectors cannot establish broader applicability.

## Reconcile at a checkpoint

1. Search for related entries and reuse the existing capability identity.
2. Separate observed facts, derived conclusions, and verification method.
3. Select one supported primary category and the smallest applicable scope.
4. Write a minimized discovery in ignored storage.
5. Submit it through `learning checkpoint --input PATH`.
6. Retain conflicts, candidate decisions, and material limits at handoff.

Use the [learning guide](../../../../docs/CAPABILITY_LEARNING.md#submit-a-discovery) for the exact input contract.
Its categories cover system knowledge, contracts, business rules, workflows, and operational experience.
Preferences remain in their appropriate instruction or task owner unless a supported registry contract applies.
Do not add a parallel preference registry or another learning state machine.

The checkpoint validates references and reconciles the current revision.
It may promote an allowlisted independent result under existing controls.
Other changes retain their required review and approval evidence.
Review and test skill or script changes before registry promotion.
New business intent and entitlement decisions follow canonical knowledge governance.

Use [configure and diagnose](../../../../docs/CAPABILITY_LEARNING.md#configure-and-diagnose) if hooks or the runtime are unavailable.
Record the limit and continue independent authorized work.
