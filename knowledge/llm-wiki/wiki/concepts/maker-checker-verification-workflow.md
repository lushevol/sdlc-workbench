---
type: "Concept"
sources: ["summaries/KT-release-operations.md", "summaries/KT-admin-and-onboarding.md"]
description: "Two-person review that verifies an un-verified admin record before activation."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Maker-checker verification workflow

## Definition

A maker-checker verification workflow separates the user who creates or changes a record from the user who approves it.
In the [[entities/fmo-post-trade-portal]] admin module, the maker prepares the record and the checker verifies it before activation.
The workflow gives a second-person control over catalog changes.

## Scope in the admin module

The workflow applies to the three admin functions described in the user manual: Module Mapping, Drawer Category, and Tile Configuration.
These functions maintain the application catalog.
See [[concepts/admin-catalog-configuration]].

## Record states

Creation or modification produces an `un-verified` record.
A different user checks the record and verifies it.
Activation is possible after verification.
Deactivation of a verified record returns it to `un-verified` state.
Each admin function keeps its own audit history, and users can view record-specific history.

The supplied text does not fully specify these behaviors:

- Rollback of an activated record.
- Propagation of an activation to running tiles.
- Handling of concurrent edits by two makers.
- Expiry or withdrawal of a pending verification.

## Required roles and entitlements

The manual lists `FMO PORTAL ADMIN` entitlements for the import-map, category, and tile functions.
The manual requires that the checker is a different user from the maker.
These statements describe prerequisites.
They do not show that any current operator holds the entitlements or that enforcement passes.
See [[concepts/ems2-entitlement-provisioning]] and [[entities/ems2]].

## Relation to tenant boundaries

The admin overview proposes tenant-maintained configuration with tenant-specific roles. The manual lists shared admin subjects and a different-user check.
The user-stated rule allows a portal administrator to read audit history and configuration across tenants. It separately prohibits any tile reference to metadata from another tile.
Which cross-tenant writes and verification actions makers and checkers may perform remains open. [ADMIN-CROSS-TENANT-READ-AC-001](../../../candidates/operations/KT-admin-and-onboarding.md#admin-cross-tenant-read-ac-001) · [ADMIN-TILE-METADATA-AC-001](../../../candidates/operations/KT-admin-and-onboarding.md#admin-tile-metadata-ac-001)

## Relation to tile authorization

Verification controls who may change catalog records.
It does not decide which end users can see or launch a tile.
Tile visibility depends on EMS2 entities and portal-entry requirements.
See [[concepts/portal-entry-and-tile-authorization]] and [[concepts/portal-tile-workspace-model]].

A record can be verified and active while its tile remains unavailable to a user who lacks the required entity entitlement.
The two controls act at different layers.

## Relation to release controls

The overview proposes self-service configuration to reduce repeated production change requests.
The manual describes record review and audit history.
Neither document establishes an approved production governance policy.
The applicable release, approval, rollback, and emergency-change rules remain undefined.

A verified record alone does not prove that a production change control was satisfied.

## Evidence status

The workflow description comes from a procedural manual whose source revision and current applicability are unconfirmed.
The manual also depends on screenshots that are absent from the retained copy.
Detailed visual steps cannot be reconstructed from the available material.
See [[summaries/KT-admin-and-onboarding]].

Owner: unknown.
Next action: obtain the current manual revision and a release record that confirms maker-checker enforcement in the target environment.

## Open questions

1. How does the portal map role checks to record ownership across tenants?
2. Can one user hold both maker and checker entitlements, and is the different-user rule enforced by the service or by convention?
3. Which audit fields record the checker identity, the verification time, and the reason for rejection?
4. Which release controls apply when a verified record changes production behavior?

## Related pages

- [[concepts/admin-catalog-configuration]] — the catalog functions that use this workflow.
- [[concepts/ems2-entitlement-provisioning]] — how roles and entitlements are created.
- [[concepts/portal-entry-and-tile-authorization]] — runtime visibility control for end users.
- [[concepts/application-ownership]] — which team is responsible for a given record.
- [[entities/portal-team]] — the team named in the empty-subject clarification.
- [[summaries/KT-admin-and-onboarding]] — source summary.


See also: [[summaries/KT-release-operations]]
