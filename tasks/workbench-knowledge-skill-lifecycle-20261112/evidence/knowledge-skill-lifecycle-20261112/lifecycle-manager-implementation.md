# Knowledge lifecycle manager implementation

Source: [exact user request](lifecycle-manager-request.md#exact-user-input), 12 November 2026.

## Scope and risk

Create one discoverable coordinator that assesses current evidence, selects existing operation skills, and gives concrete next actions.
Affected consumers are agent skill discovery, the shared lifecycle guide, scaffold aliases, and installed workspace packaging.
Reuse existing record states, task documents, receipts, and runtime commands. Add no workflow runner or parallel lifecycle store.
Qualitative risk is moderate: confusing completion, review, publication, wiki freshness, and business verification could recommend an invalid transition.
Keep these dimensions separate and inspect their supporting evidence before recommending a transition.

## Validation

Starting revision: `88bb73bb2b94fae40f2c1bd0ae51c6ea0a38450f`.

| Check | Actual result |
| --- | --- |
| Skill Creator validation | Passed for `manage-knowledge-lifecycle`. |
| Workbench CLI discovery/read | New skill returned successfully. |
| Workspace validation | `VALID`; 15 documents; zero findings. |
| Complete workspace layout and packaging suite | 23 tests passed; zero failures, errors or skips. |
| Local links | Final check: 153 local links across seven inspected files; zero missing targets or anchors. |
| Diff whitespace | Passed. |
| UI metadata and checkout alias | Valid; automatic skill discovery remains enabled. |

Commands:

```sh
.venv/bin/python /Users/lushevol/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/manage-knowledge-lifecycle
.venv/bin/ai-sdlc --workspace . skills manage-knowledge-lifecycle
.venv/bin/ai-sdlc --workspace . validate
.venv/bin/python -m unittest discover -s tests -p test_workspace_layout.py -v
git diff --check
```

Existing packaging checks exercise initialized canonical copies, discovery, aliases, denied-symlink fallback, and source-distribution/wheel resources.
The inventory now includes the new skill. No runtime or package dependency changed.
Independent integration inspection confirmed that current runtime discovery and distribution rules already include the skill and its YAML metadata.

## Behavioral forward checks

Independent read-only evaluation used three synthetic fixtures and the new skill with its linked contracts.
No fixture ran application behavior or changed lifecycle artifacts.

| Case | Observed decision |
| --- | --- |
| Partial collection with current candidates and wiki | One source HOLD keeps full collection coverage partial. The 12 reviewed candidate/wiki scopes remain current. Human review and publication remain separate. |
| Interrupted wiki attempt with concurrent provenance and changed canonical bytes | Automatic restoration is unsafe when provenance differs from both attempt hashes. Preserve semantic edits, reconcile ownership, and perform fresh review of the changed record before completion. Unchanged independent work needs no repeat. |
| New UAT-only answer with a changed source withdrawing a claim | Preserve the answer first; process the changed source and former dependents; reuse the unchanged completed page. Keep UAT 8 seconds separate from published PROD 5 seconds, human review pending, and live behavior unverified. |

The evaluator reported no substantive guidance defect in these three cases.

The independent real portal evaluation reopened source selections, processing receipts, checkpoint hashes, canonical states and wiki bindings.
It found 80 reviewed source outcomes, no queued canonical processing, and one held meeting-minutes page with missing attachments.
The returned answers are in candidate drafts. The next owner action is RATAN review of exact candidate bytes with the applicable ICS policy revision, particularly idle-expiry recovery.
Seven refreshed wiki inputs have current reviewed receipts covering 96 output hashes, with no pending attempts.
Five older linked inputs lack incremental completion receipts; a full structural verification does not supply that missing semantic completion evidence.
The evaluator recommended an explicit selected-ID to receipt-ID comparison before claiming wiki completion.
Added that comparison and an explicit limit on scoped unchanged plans, then repeated the read-only portal assessment.
The evaluator confirmed the guidance correction: only eight of 13 linked inputs have reviewed completion receipts, including the separate Settlement input.
For an entire-wiki completion request, the next action is exact-scope review of the five legacy inputs through `llm-wiki`, reusing the eight completed scopes.
RATAN policy review and publication remain independent owner actions.
No portal record or wiki artifact changed during these evaluations.

The observed decisions satisfy these scenario assertions:

```gherkin
Scenario: Guide a partial collection without repeating completed work
  Given 12 kept pages have current reviewed canonical and wiki completion evidence
  And one page is held for a missing attachment
  And all canonical records remain candidate drafts without required human approval
  When the user asks for status and next actions
  Then the response identifies partial collection coverage and the held page
  And it preserves the 12 completed scopes and pending publication review
  And it names the missing attachment and supported selection as the next source action
  And it makes no lifecycle changes

Scenario: Preserve concurrent provenance during interrupted wiki recovery
  Given one provenance file matches the interrupted attempt's after-image
  And the other file differs from both attempt hashes because another task changed it
  And the canonical record changed after semantic review
  When the user requests continuation of the selected wiki update
  Then the response stops automatic restoration and completion for that record
  And it requires reconciliation that preserves the other task's changes
  And it requires fresh binding and semantic review against current canonical bytes
  And it leaves the independent unchanged record complete

Scenario: Apply a scoped answer and investigate a withdrawn claim
  Given the returned answer specifies an 8-second limit in UAT only
  And a changed page withdraws support from an existing dependent claim
  And another page has unchanged completed input and output hashes
  And the published PROD rule specifies 5 seconds
  When the user requests continued ingestion and candidate wiki maintenance
  Then the response preserves the answer before interpretation
  And it reviews the changed page and former dependents while reusing the unchanged page
  And it keeps the PROD rule and rollout claims separate from the UAT answer
  And it requires scoped candidates, reviewed checkpoints and processing completion evidence
  And it leaves human publication review pending and live behavior unverified
```

These are reasoning assertions over synthetic inputs. They do not establish automatic execution of the procedure.

## Limits

No full runtime suite, native Windows run, live provider compilation, application test or publication ran for this instruction-only change.
Skill validation and packaging do not prove universal agent adherence or business correctness.
The skill coordinates existing operations; it supplies no background monitoring or automatic approval.
Pre-existing portal changes and unrelated `core/release-report/` content remain outside this maintenance scope.
