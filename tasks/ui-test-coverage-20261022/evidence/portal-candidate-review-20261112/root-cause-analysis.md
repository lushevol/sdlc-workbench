# Root-cause analysis: MFE Base session timing evidence

## Conclusion

The 15-second text was removed for the right reason in the canonical requirement, then removed too broadly from the MFE Base derived page. The canonical correction retired unsupported fixed acceptance fixtures. It did not retire the dated implementation and test facts that produced those fixtures. This was a classification and review-boundary failure, not an application-code change.

The current MFE Base page retains the evidence in a separately labelled section. The candidate requirement remains free of a fixed activity cadence or renewal interval.

## What changed and why

The prior requirement (v8) put `100 ms`, `15 seconds`, and `30 seconds` into AC-1 through AC-3. The retained intent sources say to keep refresh-token renewal for mouse, keyboard, and scroll activity and to renew during continuous activity; they do not select those numbers as product policy. The 12 November answer supplies the 15-minute idle ceiling and 60-minute absolute ceiling. `corrections.json` therefore changed the candidate to v9 and replaced the fixtures with the renewal-due condition and the access/absolute deadlines.

Commit `a84f49f7a` propagated that policy correction into six policy or navigation pages, including `wiki/entities/mfe-base.md`. That propagation was valid for the policy summaries. It was incomplete for MFE Base because that entity page also carried implementation context. The retained source review still shows a five-second trailing debounce in `useController.ts:60-79`; the retained activity helper still emits every 100 ms for a 15-second observation window in `activity.cjs:12-38`; and the retained execution records zero renewal during continuous mouse movement. Those facts describe implementation and test observation. They do not define a required product interval.

Commit `c43fe92ea` restored those facts under `Retained implementation evidence` in MFE Base, with source hashes and a link to the independent gap record. It did not change the candidate requirement or application code.

## Why the review missed it

The correction was reviewed as a canonical-policy change. The recorded wiki review checked seven changed outputs against v9 and reported zero unqualified removed timing claims. Its closure search covered derived wiki output and deliberately treated the saved exploration as historical. It did not inventory retained implementation sources or require a mapping for each removed implementation/test fact.

The bridge did not yet require a `claim_review` for changed outputs, so the prior completion record carried canonical-consistency notes without a claim-level retention map. That allowed a policy-consistency review to stand in for an evidence-retention review.

The failure chain was:

1. A test fixture was correctly rejected as target policy.
2. The same numeric facts were treated as invalid everywhere, without classifying their implementation/test meaning.
3. A shared entity page was treated as a policy-only dependent even though it contained source and execution context.
4. The review checked current canonical fidelity, but not claim-level loss across retained evidence.
5. Provenance was advanced through the old transition path before the claim-loss guard existed.

## Similar findings

No second unqualified timing-evidence omission remains in the current wiki. The other policy pages correctly omit the old fixtures, and the saved exploration retains them with an explicit historical qualification.

The same evidence-classification failure appeared in earlier generated pages and was corrected in the legacy wiki review:

| Finding | Earlier error | Current status |
| --- | --- | --- |
| `CES-WIKI-02` · `wiki/entities/ems3.md` | Expanded reported Auth Server delegation into a portal-wide no-evaluation model. | Corrected; BFF evidence and portal decisions are separate. |
| `CES-WIKI-03` · `wiki/concepts/machine-to-machine-authentication.md` | Turned historical 17-year/7-day token validity examples into rotation and ownership inferences. | Corrected; values remain historical evidence only. |
| `IE-003` · `wiki/entities/graphql.md` | Called documented experiments measured transport patterns without retained execution. | Corrected; experiment descriptions and execution limits are separate. |
| `IE-004` · `wiki/entities/apache-jmeter.md` | Said workload evidence was unavailable even though the UAT summary supplied workload facts. | Corrected; summary facts are retained and artifacts remain unavailable. |
| `CROSS-01` · `wiki/concepts/identity-provider-delegation.md` | Made FMAA universal and omitted the separate initial bulk-insert path. | Corrected; recurring upload and initial bulk insert are qualified separately. |

These are related semantic overstatement or evidence-loss cases, not additional current MFE timing deletions. Their durable records are in `tasks/ui-test-coverage-20261022/evidence/portal-wiki-legacy-review-20261112/`.

## Prevention controls

1. **Classify claims before editing.** Every changed or removed claim must be labelled `intent`, `implementation`, `test`, `execution`, `deployment`, `approval`, or `unknown`. A policy correction may remove an `intent` fixture while preserving an implementation or test claim.
2. **Require a retention map.** For every removed numeric or behavioural fact, the review record must state its disposition (`preserved`, `superseded`, or `withdrawn`) and cite the exact evidence. An implementation or test fact is not withdrawn merely because it is absent from policy.
3. **Review all former dependents.** Reopen entity pages, concepts, summaries, index entries, and saved explorations that depended on the changed source. Do not classify a page as policy-only from its filename or type.
4. **Use the bridge transition.** Compile, review, and finalize through `wiki.py review`; do not edit `source-manifest.json` or `.openkb/hashes.json` to record semantic completion. The bridge's changed-output claim guard must be the completion gate.
5. **Search evidence as well as wiki output.** Closure checks must inspect the retained source snapshots, gap records, case definitions, and execution results named by the affected topic. A zero match in derived pages cannot prove that a fact was safely retired.
6. **Keep a regression assertion for consequential boundaries.** The portal test asserts that v9 has no fixed AC-1–AC-3 cadence while MFE Base still exposes the five-second debounce, 15-second observation window, and measured outcome as qualified evidence.

## Completion and limits

The MFE page, candidate requirement, gap record, and retained source hashes are now consistent for this scope. The regression assertion and lifecycle guidance provide prevention coverage for this failure mode. No ICS source question was reopened, no publication approval was invented, and no application runtime was changed or executed by this review.
