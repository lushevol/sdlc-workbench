---
name: entitlement-compatibility-scan
description: Scan UI, shared-library, BFF, authentication, and SDK repositories for EMS2-to-CES entitlement compatibility gaps when upper-layer source changes must remain zero.
---

# Entitlement Compatibility Scan

Use this skill to audit one or more repositories before an EMS2-to-CES migration. The target contract is usually: upper applications keep their existing APIs and source, while lower layers add CES support.

Keep the result evidence-backed and repository-relative. Do not edit target source, weaken checks, or infer a business policy from a compatibility request. This skill performs static inspection unless the user separately authorizes a controlled runtime probe.

## Workflow

1. Record each repository path, Git revision, checkout status, source roots, test roots, and the old and new entitlement samples. State missing snapshots and dynamic boundaries.
2. Run the deterministic inventory helper:

   ```sh
   python3 <skill-root>/scripts/scan_entitlement_compat.py \
     <repo-or-repo>... --output <task-dir>/evidence/entitlement-scan.json
   ```

   The helper finds high-recall candidates. It does not prove that a match is reachable or incompatible.
3. Inspect every candidate in context. Read callers, imports, DTOs, mappers, route configuration, tests, and the lower-layer adapter that supplies the value. Search for the same symbol across all selected repositories.
4. Compare the old contract with the CES shape. Check role cardinality, application identity, subjects and actions, data profiles and policies, ownership fields, tile routing, empty grants, and admin identity.
5. Classify each finding with one primary category from [finding-categories.md](references/finding-categories.md) and one disposition:
   - `compatible`: the existing contract survives with the supplied data.
   - `lower-layer-preservable`: a lower-layer additive projection can preserve it without upper source changes.
   - `hard-incompatibility`: the old API cannot represent valid CES behavior without a policy or upper change.
   - `conditional`: it breaks only when a stated configuration, role combination, or provider conflict occurs.
   - `latent`: the code is present but no reachable production caller was found in the inspected snapshot.
   - `verification-gap`: the behavior may work, but tests or runtime evidence do not cover the CES boundary.
6. Write one finding per behavior. Include the exact file and line, old assumption, CES evidence, user or system consequence, lower-layer preservation option, owner, next action, and evidence limit. Use the template in [report-template.md](references/report-template.md).

## Compatibility rules

- Treat `roleList` as a multi-value membership list. Never join it with commas to satisfy a scalar `role`, `roleName`, `assignee`, `moduleOwner`, or data-profile field.
- Treat `applicationId` and `applicationName` as identity metadata. They do not replace legacy `subject:action` permission keys.
- Preserve the complete legacy permission projection when zero upper changes are required. Check exact subject and action names, including maker/checker actions.
- Flag direct reads of `user.entitlements`, JWT claims, `X_RATANONE`, `roleName`, or `getUser().role` because they can bypass a container or BFF compatibility adapter.
- Flag role-owned views and filters separately from creator-owned items. A lower layer cannot invent the owner for a multi-role CES user.
- Check tile-level EMS2/CES routing. A global EMS3-only switch cannot support a partial rollout that leaves other tiles on EMS2.
- Check CES `data_profiles` and `data_policies` separately from functional roles. Do not infer a data profile from an entitlement name.
- Check empty valid CES assignments. Empty grants should produce an empty deny projection, not an authentication failure, unless the source contract defines the response as malformed.
- Check legacy admin identity and token validation separately. CES entity identity cannot silently replace `FMO PORTAL ADMIN:<role>`.
- Treat module-level permission constants and cached user decisions as lifecycle risks when entitlements can arrive or change after module evaluation.
- Treat an absent match as `not-observed`, never as proof that a dependency or incompatibility does not exist.

## Evidence and limits

Use exact revisions where available. Separate observed source facts, inferred consequences, unresolved policy, and unavailable runtime evidence. Tests with only EMS2 fixtures do not prove CES compatibility. A passing static scan or unit suite does not establish live CES parity, production reachability, or release approval.

The helper intentionally excludes common generated and dependency directories. Record those exclusions and any inventory truncation in the report. Use `rg` or direct source inspection when a repository uses generated imports, dynamic routing, or unsupported file types.
