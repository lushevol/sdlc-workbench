# Knowledge skill decomposition verification

Source: [exact user request and implementation authorization](user-input.md#exact-user-input), 12 November 2026.
Follow-up: [lifecycle manager request](lifecycle-manager-request.md#exact-user-input), 12 November 2026; handled in its linked implementation review.
Branch: `codex/knowledge-skill-lifecycle-20261112`.
Starting revision: `0d1c539ea8cf74f6072904f428302bc932c44e1c`.

## Outcome and scope

Six major-step parents now coordinate 17 reusable operation skills.
The [lifecycle guide](../../KNOWLEDGE_LIFECYCLE.md) records ownership, storage, invalidation, and the workflow diagram.
Each operation identifies its inputs, checkable results, and stopping conditions.
Source filtering, canonical governance, and wiki freshness retain separate completion boundaries.

Existing source commands, policy paths, schemas, validators, hashing, and wiki engine implementations remain the tool layer.
Wiki finalization coordinates paired provenance, reviewed bytes, verification, and safe interrupted recovery.
Native source-owning transactions remain restricted on canonical aliases.

The change covers skills, shared guidance, discovery aliases, distribution manifests, and existing packaging-test inventories.
Qualitative risk is moderate: a missed procedural safeguard could allow misleading publication or stale wiki claims.
The work preserves unrelated `core/release-report/` content outside this commit.

## Deterministic checks

Environment: macOS arm64, Python 3.14.5, existing project virtual environment.

| Check | Actual outcome |
| --- | --- |
| Skill Creator validation | All 23 changed/new entrypoints passed. The two recovery-related skills passed again after refinement. |
| Local Markdown links | Targets and anchors passed across 35 changed/new Markdown files before this verification record. |
| Workspace validation | `VALID`; 14 canonical documents; zero findings. |
| Complete runtime suite | 937 tests; zero failures, errors, skips, or expected failures. |
| Source distribution and wheel round trip | Existing packaging tests passed, including unchanged upstream file inventories and workspace initialization. |
| Final wheel build | Passed with existing dependencies and no build isolation or downloads. |
| Fresh installation probe | Installed the built wheel outside this checkout; discovered/read all 37 canonical skills and aliases. |
| Fresh workspace validation | `VALID`; zero business documents; lifecycle guide present. |
| Diff whitespace | Passed. |

Complete-suite command:

```sh
WORKBENCH_CONNECTOR_INTEGRATION=1 .venv/bin/python -m unittest discover -s tests -v
```

Final build command:

```sh
.venv/bin/python -m pip wheel . --no-deps --no-build-isolation --wheel-dir dist
```

Final wheel SHA-256: `549b5835706e68ca8cb03064ac5c2781a10c6b2ebfcb5fc3183ee3de0031a673`.
The installation probe imported the installed package, initialized an empty workspace, read all aliases, and invoked CLI validation.
It used a temporary directory outside this checkout and existing dependencies.

## Failed attempt and correction

The first sandboxed suite reported 930 tests, one failure, 36 errors, and two optional skips.
Controlled HTTP fixtures failed to bind localhost because the sandbox denied socket access.
The packaging test also found the new lifecycle guide missing from the source distribution.
The wheel-from-source-distribution error was `No such file or directory: .../unpacked/docs/KNOWLEDGE_LIFECYCLE.md`.

Added the guide to [MANIFEST.in](../../../MANIFEST.in), alongside its scaffold registration.
Repeated the complete suite with local fixture access and existing optional Node integration enabled.
The final 937-test run passed without narrowing tests or weakening assertions.

## Independent skill forward checks

An independent reader used the current skills and supplied scenario evidence.
These are reasoning checks of agent procedures. They are not live business or wiki compilation results.

```gherkin
Scenario: Answer a PROD question when a newer UAT proposal appears in a stale wiki
  Given a published PROD rule states 15 minutes
  And a newer UAT candidate proposes 30 minutes
  And the wiki binding is stale
  And PROD execution evidence is unavailable
  When the agent answers through query-knowledge without update authorization
  Then the answer identifies 15 minutes as documented PROD intent
  And the answer identifies actual PROD enforcement as unverified
  And the agent performs no record or wiki writes

Scenario: Reuse a supported no-change release synchronization
  Given a published rule denies access when permission is missing
  And a code fix restores that rule with retained passing UAT assertions
  And no intent source changed
  When the agent classifies the release change
  Then canonical intended meaning remains unchanged
  And actual conformance evidence stays in the independent gap record
  And a retry requires matching operation identity, fingerprints, and base hashes
  And row completion does not establish whole-release completion or PROD execution

Scenario: Resume an interrupted ADE wiki update after source bytes changed
  Given reviewed source bytes and current source bytes have different hashes
  And only one provenance file advanced
  And paired before-images exist
  When the agent uses finalize-wiki-update
  Then the agent stops completion and preserves semantic edits
  And recovery requires proof that both current provenance files belong to the attempt
  And unrelated provenance changes remain protected
  And both intended after-image hashes are recorded before either replacement
  And fresh binding and semantic review precede another completion attempt
```

All three scenario decisions matched their supplied evidence boundaries.
The independent reader found an interrupted-recovery ownership and ordering ambiguity.
Refined the binding receipt and finalization instructions, then repeated that scenario review.
The reader reported no remaining actionable gap in the current procedure.

## Limits

No native Windows installation or live model compilation ran.
Scenario checks do not establish universal agent adherence or business behavior.
ADE concurrency exclusion remains procedural. Two provenance writes remain non-atomic, with explicit stop and recovery requirements.
No domain records, retained source snapshots, immutable governance events, or active wiki state changed.

## Writing review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
