---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
---

# Proposed guidance additions

> **These changes are drafts awaiting human confirmation.**
> The target files remain unchanged by this review.
> Owner: user. Next action: approve, reject, or revise the candidate IDs below.

## C06: Preserve recent-session coverage

Target: `.agents/skills/learn-from-sessions/references/history-scan.md`.
Proposed addition:

> Discover accessible chat histories for the requested project and time window before scanning all retained task evidence.
> Read message pages; thread titles and retrieval summaries alone do not establish reviewed conversation content.
> The scanner's duration filters session inputs; default task evidence can include older context.
> Default tasks precede explicit session paths and can exhaust the scan budget.
> When truncated, report missing coverage and use a separate review root with explicit selected paths.
> Keep chat timestamps distinct from file modification dates, and disclose partially inspected message pages.

This uses existing discovery tools and the existing scanner.
No new transcript collector or runtime option is proposed.
The review reproduced truncation, then inventoried seven selected records without truncation.

## C07: Protect authored assets during cleanup

Target: `tasks/README.md#evidence-priorities-and-cleanup`.
Proposed addition:

> Inventory authored, editable project assets separately from generated task evidence before selecting deletion candidates.
> A diagram or source document can have a human consumer without an active runtime importer.
> Confirm its intended retention and recovery location before deleting its last maintained copy.
> After restoration, compare exact bytes with the selected source revision and applicable cleanup hashes.
> Keep historical content labels separate from current architecture authority.

Proposed helper: `verify_restored_assets.py` beside this draft.
Possible final target: `.agents/skills/learn-from-sessions/scripts/verify_restored_assets.py`.
If approved, link it from the restoration guidance.
It verifies existing files against Git blobs; it performs no restoration or cleanup.
XML checks establish parseability only, not visual correctness.

## C08: Check the installed result after skill changes

Target: `.agents/skills/learn-from-sessions/references/workbench-promotion.md`.
Proposed addition:

> After moving or adopting a skill, inventory its entry point, helpers, references, metadata, aliases, and active consumers.
> Prepare the complete replacement before retiring the old entry point.
> Validate the installed wheel in an empty workspace outside the checkout.
> Compare shipped source bytes and check that retired folders are absent.
> Permit responsibility guides under `core/`; reject runtime modules, project task history, package manifests, and runtime tests.
> Resolve both paths before comparing installation locations on systems with temporary-directory aliases.
> Preserve meaningful probe failures and distinguish corrected test assumptions from product defects.

This extends the existing promotion reference rather than adding another packaging skill.
Evidence comes from session-learning consolidation, settings implementation, graph delivery, and Requirement Grill adoption.
The proposal adds focused checks; it does not require repeating every historical test for documentation edits.
