# TC-RETRY assessment

> **TC-RETRY is NOT_VERIFIED for the candidate.** The passing test asserts the observed logout outcome.
> The supplied intended outcome fails in both selected revisions under equivalent local inputs.

## Scope and authority

The synthetic contract requires retry without logout after rejected renewal. Both revisions must satisfy that rule.
The canonical scenario supplies the Extend trigger and two outcome predicates.
See [requirements](requirements.md#synthetic-intended-behavior) and [TC-RETRY](test-cases.md#tc-retry).

| Binding | Value |
| --- | --- |
| Baseline | `d9417ed17a50516fdca3a85478245cf3bafa40ee` |
| Candidate | `037a1e6c0c2c9d0316fa5882f38417330ec48389` |
| Candidate source SHA-256 | `fecec08e001019b1ff178a147c81591db8a87d262792b967db7dced9a70e1fa9` |
| Baseline source SHA-256 | `64f5ff493e872ca51e2cffeeddb5c9ccd89a69a56f83247fd1c3fe75a9b53e6a` |
| Test SHA-256, both revisions | `b5d44ca80de5049548c7a0eed60df8feed71645024088bfdde1eff5d2325e54c` |
| Environment | Local macOS, Python 3.14.5, unittest, synthetic inputs |

## Assertion chain

`CurrentBehavior.test_rejection_logs_out` imports `renewal_action` directly from `service`.
It calls `renewal_action(refresh_failed=True)`. The omitted `refresh_pending` argument defaults to `False`.
The sole assertion expects `"logout"`. Candidate `service.py` lines 4–5 return that exact value.
See [test](repo/test_characterization.py) line 6 and [implementation](repo/service.py) lines 1–5.

The assertion contradicts both required outcomes. Its passing result establishes the function returned `"logout"` for this input.
The test executes the source function directly. It has no fixtures, mocks, helper calls, or services.
It does not execute the Extend interaction or observe a client session.

## Paired execution

Both exact Git revisions ran the unchanged supplied suite from isolated temporary directories.
Each run passed one test with exit code `0`. The candidate checkout also passed that suite.
Direct function probes then compared the same inputs with the supplied outcomes.
See [retained commands, outputs, hashes, and timing](outputs/actions.json).

| Case | Inputs | Intended action | Baseline observed | Candidate observed | Comparison |
| --- | --- | --- | --- | --- | --- |
| [TC-RETRY](test-cases.md#tc-retry) | `refresh_pending=False, refresh_failed=True` | `retry`, without logout | `logout`, both predicates fail | `logout`, both predicates fail | Unchanged existing failure |
| [TC-PENDING](test-cases.md#tc-pending) | `refresh_pending=True, refresh_failed=False` | `wait`, without logout | `wait`, both predicates pass | `logout`, both predicates fail | Introduced failure |

TC-PENDING supplies context for the only changed branch. Its canonical definition comes from the supplied fixture.
The existing test takes the failure branch and leaves the changed pending branch unexecuted.

## Coverage mappings

The review inventory contains two synthetic cases, four outcome predicates, one existing unit test, and one meaningful source change.
The cases retain their supplied identifiers. No separate AC identifiers or requirement versions were supplied.

### Intended predicates to assertions

| Case and predicates | Definition | Inspected supplied assertion | Supplied execution | Gap |
| --- | --- | --- | --- | --- |
| [TC-RETRY](test-cases.md#tc-retry), action `retry` and no logout | Complete | `assertEqual(..., "logout")`, test line 6 | One test passes on both revisions | Neither required predicate is asserted |
| [TC-PENDING](test-cases.md#tc-pending), action `wait` and no logout | Complete | None | Case absent from supplied suite | Both required predicates lack assertions |

### Intended predicates to implementation

| Case | Change link | Exact implementation | Conformance |
| --- | --- | --- | --- |
| TC-RETRY | UNCHANGED | Both revisions, `service.py` lines 4–5 | Contradictory, returns `logout` |
| TC-PENDING | C1 | Baseline/candidate `service.py` lines 2–3, `wait` → `logout` | Candidate contradicts both required predicates |

### Code change to assertions

| Change | Canonical case | Inspected assertion chain | Matching execution | Gap |
| --- | --- | --- | --- | --- |
| C1, selected revisions, `renewal_action`, pending branch | [TC-PENDING](test-cases.md#tc-pending) | Supplied test sets `refresh_failed=True` with pending false | Suite passes, changed branch unexecuted | No supplied assertion covers C1 |

| Metric | Result | Definition and limit |
| --- | --- | --- |
| Canonical case definitions | 2/2, 100% | Four explicit outcome predicates |
| Required predicates asserted by supplied tests | 0/4, 0% | Test expects the contradictory outcome |
| Cases with all required supplied assertions | 0/2, 0% | Definition existence is counted separately |
| Inspected implementation mapping | 2/2, 100% | Both branches and all four predicates mapped |
| Candidate conforming implementation | 0/2, 0% | Both cases return logout |
| Candidate passing intended function predicates | 0/4, 0% | Paired direct probes, function boundary only |
| Change to canonical definition | 1/1, 100% | C1 maps to TC-PENDING |
| Change to supplied assertions | 0/1, 0% | Pending branch has no assertion |
| Change to passing intended execution | 0/1, 0% | Candidate pending probe fails |
| Behavior change justified by supplied intent | 0/1, 0% | C1 contradicts the pending rule |

## Finding and next action

| Finding | Evidence and consequence | Owner | Next action |
| --- | --- | --- | --- |
| F1, TC-RETRY assertion and implementation gaps | Test line 6 expects logout. Both source revisions return logout. Required retry behavior fails locally. | UNKNOWN | Correct the retry implementation and assert retry without logout under separate authorization. |
| F2, pending regression and assertion gap | C1 changes wait to logout. Equivalent pending probes pass baseline and fail candidate. | UNKNOWN | Restore the intended pending outcome and add matching assertions under separate authorization. |

Confidence is high for the inspected function outcomes and assertion mismatch.
These synthetic results establish function behavior within the retained inputs.
Client session effects, production reachability, real renewal services, acceptance, and deployment suitability remain UNKNOWN.
Source and test hashes match the supplied inputs. The repository worktree remains clean.

## Writing and automated checks

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks covered source hashes, skill hashes, runner results, paired observations, repository cleanliness, JSON, and local report links.
  - Intended behavior failed the local probes.
  - Automated checks do not establish complete writing review.
```
