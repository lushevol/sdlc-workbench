---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - This review does not establish current policy, implementation, business execution, or publication approval.
  - The review covers selected ranges and leaves the rest of two contextual pages queued.
---

# CCIL canonical draft review

- **Candidate:** [India CCIL netting](../../../knowledge/records/candidates/settlement/KT-settlement-ccil-netting.md)
- **Candidate SHA-256:** `87816e22088e2dba2a8c9b37916b482b071aacd07101eb7003e7877fb592653b`
- **Semantic reviewer:** `agent:codex`
- **Reviewed at:** `2026-11-15T10:58:33+00:00`
- **Owner:** unknown
- **State:** candidate draft; `verified: []`

## Reviewed source bindings

The eight current collection identities match the Cash plan and selected-view manifest. Four existing manifest identities also bind the cited snapshots. They refer to duplicate source bytes and add no new semantic content.

| Source ID | Original SHA-256 | Selected view SHA-256 | Original line ranges |
| --- | --- | --- | --- |
| `SRC-512ace11dd56f19bf781d531` | `a2ce9ca6a14777d7d688410c3c2c6b19caedf6f8a202f84c4253da78a93736a1` | `a30cc147d3f373220c2380f92149bf188b49d2ff0d8acb4535b4cbbc8ffa1057` | 1–3, 10–32, 34–45, 47–71, 73–113, 132–139, 145–146, 149–150, 152–153, 156 |
| `SRC-5f68d1e47d5b2c04e8639c17` | `e03e964bdf2adc695771ca3e066d3fe899f6823f4ccf6a864e5f53d24010e506` | `4a928a646ead8b2b1bddeb61a607019040076d8608377d7d92063491024330ac` | 1–14 |
| `SRC-d856b444e14a0493cc473bde` | `e03e964bdf2adc695771ca3e066d3fe899f6823f4ccf6a864e5f53d24010e506` | `4a928a646ead8b2b1bddeb61a607019040076d8608377d7d92063491024330ac` | 1–14 |
| `SRC-2ed473c923bd76833481326f` | `246312dc39ff8687020ca048e6b01e19c992164d70b2a8b1c2d720bd83e8135f` | `3bd6866bb77855bcfe904ed87c3c91b61a1886520e6ea325c8f04e654229c511` | 1–8, 10–13 |
| `SRC-17f5cbc4dfeeb07df7397528` | `246312dc39ff8687020ca048e6b01e19c992164d70b2a8b1c2d720bd83e8135f` | `3bd6866bb77855bcfe904ed87c3c91b61a1886520e6ea325c8f04e654229c511` | 1–8, 10–13 |
| `SRC-36e628fbb28fa91eae5735d7` | `3957b43f30b3c7b23f2b189d8f54d4349268db06b3bb48f67d7248d9fcb0550e` | `cbd062966c55534bfc43de88d8f756428cf2e78711d531d7a2614717c04613ed` | 7–8, 10 |
| `SRC-426393fda3ed4becdfc99390` | `88f99202a018ce56e4c173be3026561afc7342bc035ef97eb298491436682e24` | `a3280d65be379b07ead27411e1c1e95a112a37b07cd7ba7af2f74fe31f2caa94` | 3–54, 58–70 |
| `SRC-29e240338779d97eca0bed84` | `55087e09edeb5dfb048c3665eee350c70629cb1efb194c9f7af8361d039c6891` | `55087e09edeb5dfb048c3665eee350c70629cb1efb194c9f7af8361d039c6891` | 1–107 |

| Additional retained identity | Resource | Original SHA-256 |
| --- | --- | --- |
| `SRC-83752d4f8891392fb5d5d81a` | Prior `settlement-netting` identity for the CCIL business case | `e03e964bdf2adc695771ca3e066d3fe899f6823f4ccf6a864e5f53d24010e506` |
| `SRC-a5bac081fa53386d1cebeb7d` | Prior `settlement-netting` identity for the CCIL technical design | `246312dc39ff8687020ca048e6b01e19c992164d70b2a8b1c2d720bd83e8135f` |
| `SRC-47997ab448281d8fdb1ba7a4` | Prior `settlement-netting` identity for the GUI/API page | `88f99202a018ce56e4c173be3026561afc7342bc035ef97eb298491436682e24` |
| `SRC-337472978edf74a738f8a7c4` | `cash-settlement-home-page` `page.md` identity for the GUI/API page | `88f99202a018ce56e4c173be3026561afc7342bc035ef97eb298491436682e24` |

The broad GUI/API and User Actions sources remain queued for full processing. This candidate cites only their relevant selected passages. The Day 2 auto-netting source remains queued for separate cross-lane review.

## Semantic findings

1. **Family and group conflict.** The functional tactical predicate lists family `IRD` and group `IRS`. The technical stamping predicate lists family `IRS` and group `IRD`. These selected lines conflict. The evidence does not establish which proposal is authoritative. See [KDQ-ec45c5ec24](canonical-draft-questions-20261115.md).
2. **Counterparty conflict.** The general backend proposal requires component counterparty FMIDs to match. The CCIL design allows different counterparties for CCIL settlement. It does not define a backend exception or precedence. See [KDQ-c89540196b](canonical-draft-questions-20261115.md).
3. **Status conflict.** The general GUI status list, general backend list, CCIL matrix, and dedicated blotter action differ. The sources do not state one governing status gate or processing order. See [KDQ-7fa8775478](canonical-draft-questions-20261115.md).
4. **Dated IRS scope.** The June and August examples describe expected FMRP flows. They do not state a current general rule for IRS re-netting or settlement-method inheritance. No hub limitation was retained because selected evidence did not support it.
5. **Expected behavior only.** The scenario sheet records expected outcomes. No executable assertions, implementation, deployment, or business execution were inspected.

## Corrections and unresolved owner questions

The candidate removes the unsupported hub-scope statement and replaces it with the limit of the dated examples. It records the supported family/group conflict without choosing a winner. It adds claims `NET-M-031` and `NET-M-032` for counterparty and status conflicts.

The first preparation check identified four retained source identities missing from the candidate. I added those existing manifest entries. They preserve source provenance and leave claim wording unchanged. This review covers the resulting candidate hash above.

The question annex corrects two locator errors. The general GUI gate is at original line 5, and backend validation is at original line 17. Earlier references to lines 3 and 15 pointed to a heading and a blank line. All answer cells remain blank.

Other open questions remain listed in the candidate and the annex. They cover SWIFT treatment, static-data ownership, onboarding controls, staged IRS scope, resultant fields and state, withdrawal scenarios, and lookup failure recovery.

## Checks

- `.venv/bin/ai-sdlc --workspace . validate` returned `VALID` for 22 documents with zero findings.
- A local-link check found 0 broken candidate links among 26 links.
- Question integrity check found 900 unique question IDs and 0 answers.
- No business tests or execution evidence were run or claimed.

The candidate is a source-backed draft. It does not establish an approved rule or publication readiness.

## Derived wiki and source completion

The current-session `llm-wiki-agent` workflow added [the CCIL summary](../../../knowledge/llm-wiki/wiki/summaries/KT-settlement-ccil-netting.md) and one index entry. The summary SHA-256 is `34c2ccd6f588bcfe4492670e1973d31f49afb16780f6670c65a512cc09f0e3ab`. The reviewed receipt is in ignored workspace storage at `.workbench/wiki/ccil-netting-20261115-run01/review.json`.

Both relative aliases point to the canonical candidate. The wiki bridge verified 20 linked canonical sources. Six structural categories and 14 local links in the new summary passed with no findings. The exact CCIL wiki plan replans as `unchanged`.

The Cash collection receipt now records six reviewed CCIL source identities. The result binds source plan `55395eee92d5ec43cd15bf04a925ab777ce90ca48131511d25623346b3de24bf` to the passed prepared and final checkpoints. `sources complete` returned `PARTIAL`, with 432 processing pages and 38 review-held pages remaining in Cash.

The refreshed RATAN plan reports 77 processing pages and three review-held pages. Both collections retain 41 review-held pages in total. Neither the wiki summary nor these receipts approve CCIL policy or publish the candidate.
