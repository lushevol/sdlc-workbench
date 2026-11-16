# Legacy entitlement and tenant-routing catalog context

This document retains selected historical catalog meaning and its current-policy limits.
Current source authority, deployment and conformance remain unverified.

## Legacy CES catalog meaning

The catalog describes CES as the strategic data-entitlement service and calls it the former EMS3.
It describes API checks using FMAA authentication, resilience, selective enablement and caching.
Its need-to-know rule limits visible cashflows to allowed entities according to user profile and location.

Data Policy links rules to HR profiles and automatically inherits them for new users. Policy Owner or COO manages it.
Data Profile links rules to roles and is assigned by an EMS3 operator. Role describes permitted business activities.
The catalog gives Data Profile a general precedence over Data Policy.

Its example permits a GB-user Korea-trading override outside Korea trading hours through a Data Profile.
It describes CES data entitlement for RATAN and BCS cashflow blotters, while menu/button function entitlement uses EMS2.
These are undated historical catalog claims. Current policy precedence and applicability remain unresolved under KDQ-75b4b1db97.

[Selected catalog lines 13–30](<../../../knowledge/evidence/sources/sha256/5ba48d46d997950c8070a86b613ca85146082b7a982e04beb6806df88cb81add.md#L13-L30>)
[Selected catalog lines 36–40](<../../../knowledge/evidence/sources/sha256/5ba48d46d997950c8070a86b613ca85146082b7a982e04beb6806df88cb81add.md#L36-L40>)

## Legacy EMS2 and FMAA catalog meaning

The catalog describes EMS2 management of user entities.
At login, RATAN retrieves subjects under X_RATANONE to control visible blotters and right-click operation permissions.
For another application connecting to RATAN, the catalog describes FMAA authentication and an issued access token.

These describe the historical caller baseline. Current migration requirements preserve supported permission meaning and distinguish system-specific identifiers.

[Selected catalog lines 9–30](<../../../knowledge/evidence/sources/sha256/39cb89d5a608a849658f754d4e22f9dd54f831b2399744205159cab373b4b864.md#L9-L30>)

## Legacy tenant SDK and forwarding catalog meaning

The catalog assigns tenant entitlement-list retrieval to the RATAN SDK and EMS2.
It routes tenant frontend requests through RATAN Nginx to the tenant backend.
These are historical integration responsibilities. They select no universal current entitlement provider or invented role mapping.

[Selected catalog lines 9–11](<../../../knowledge/evidence/sources/sha256/b7213ecfa70d8c7503a6c72c4a2c84b40d3bdd1b923f73a2073610fb28d60189.md#L9-L11>)
[Selected catalog lines 24–29](<../../../knowledge/evidence/sources/sha256/b7213ecfa70d8c7503a6c72c4a2c84b40d3bdd1b923f73a2073610fb28d60189.md#L24-L29>)

## Current-priority handling

The user requested preservation of the SDK contract where possible, with version 3.0.0 and caller-supplied FMAA tokens.
The current SDK record also distinguishes the X_RATANONE-to-RATAN_ENTITLEMENT_RULE name correspondence from identifier and role equivalence.
Existing permission-provider and compatibility decisions remain scoped to their original user clarifications.
[SDK implementation clarification](../../../knowledge/evidence/sources/user-clarifications/single-ui-sdk-ces-migration-20261101/user-clarification-implementation.md)
[Name-equivalence clarification](../../ces-entitlement-migration-20261102/evidence/user-input-20261030-field-equivalence.txt)

KDQ-75b4b1db97 asks whether the historical Data Profile precedence and EMS2 menu/button split apply outside the clarified migration.
Its owner remains unknown. Its answer remains pending in the single central question document.
This retained source context supplies historical meaning while that applicability decision remains open.
[Central question document](canonical-draft-questions-20261115.md)

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
  - Historical catalog claims do not establish current accepted policy.
```
