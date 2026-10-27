# Independent audit of the Claude Code and DeepSeek reviews

**Action: Investigate the stale timeout dialog before release.** A focused test confirms the dialog blocks a replacement session in the synthetic flow. The production trigger is unverified. The owner is unknown. See the [probe execution](stale-modal-probe/execution.json) and [assertions](stale-modal-probe/staleModalProbe.test.tsx).

**Action: Verify the deployed renewal-token contract and build settings.** Unsupported token shapes can prevent renewal. Server-mode settings reference a development remote. The production contract and artifact settings are unknown. The owner is unknown. See the [client audit](adversarial-client.json) and [support audit](adversarial-support.json).

The candidate is `e0030f5cf920b715f5831faf7df86cb9789b6d0f`.
The comparison baseline is `f025513f696476a9cc8162681410cbd21e029bcb`.
The provider used Claude Code with `deepseek-v4-flash`, according to the execution metadata.
The provider returned 30 successful CLI executions. One returned tool-call text, not a review.
The other 29 produced usable bounded reviews. Seven additional calls failed.
The full-payload calls failed. See [independent](../independent-execution.json) and [adversarial](../adversarial-execution.json).

Four smaller fragments replaced the failed first segment of `sessionRefresh.test.tsx`.
They reported no confirmed findings. Their limited context cannot establish a full-file review.
Other partial packets have the same cross-file limitation.
These packets do not establish an independent full-branch review.
The [replacement error-handler review](../retry-error-handler-execution.json) covered the earlier unusable tool-call packet.

## Stale dialog after replacement login

The original delayed logout pauses for one second.
A replacement login changes the session epoch during that delay.
The old logout returns without closing the dialog when the epoch changes.
In the focused harness, the replacement token remains valid.
The dialog remains open, Extend is disabled, and Logout is an enabled no-op.
The probe extended [PEND-10](../../../../../repos/ui/mfe-base/src/pages/Home/common/sessionPending.test.tsx) with direct DOM assertions.
It selected one case and skipped 17 unrelated cases.
The probe used a synthetic login button and kept Home mounted.
It does not establish that production users can trigger this sequence.
The [session audit](adversarial-session.json) separates this finding from incorrect provider claims.

## Other material dispositions

- A failed fresh-login request clears refresh credentials before its response. Its active-session UI reachability is unknown. See the [client audit](adversarial-client.json).
- The renewal handler rejects an opaque token or one without `iat`. Production BFF token guarantees are unverified. See the [client audit](adversarial-client.json).
- A direct token dispatcher can preserve refresh credentials and the old epoch. No local non-test caller was found. External consumers remain unknown. See the [support audit](adversarial-support.json).
- Axios config sets a 60-second timeout. A pending acquisition delays Extend and the automatic recovery timer. A wall-clock bound during browser suspension remains unverified. See the [session audit](adversarial-session.json).
- A malformed refresh expiry invokes the final logout fallback. A parsed baseline token without expiry could leave Extend available. The business contract for this difference is unknown. See the [session audit](adversarial-session.json).
- A missed acquisition timer is not replayed after visibility restoration. A lifecycle test expects this behavior. Initial registration within the last 25 seconds needs separate intent evidence. See the [independent session audit](independent-session.json).
- The declared server environment selects a development remote. The production build configuration and overrides are unknown. See the [support audit](adversarial-support.json).
- The `[SR17]` and `[SR05]` test labels each identify multiple cases. Link the exact file and title. The hook-only `[SR05]` asserts the prompt, not completed logout. See the [retry audit](retry-findings.json).
- DEL-20 verifies recovery is available. It does not click Extend or prove recovery completes. See the [retry audit](retry-findings.json).
- A stale completion can clear the pending registry without publishing the loader state. A visible persistent spinner requires further reachability evidence. See the [retry audit](retry-findings.json).
- The provider alleged an unhandled logout promise. The local logout function returns void and catches its HTTP promise failures. See the [independent session audit](independent-session.json).
- The provider alleged a TypeScript parser failure. A selected TypeScript file passed ESLint without fixes. This single-file check does not establish full lint success. See the [support audit](adversarial-support.json).

The [independent support audit](independent-support.json) records remaining support claims.
The [first two test packet audits](independent-tests-1-2.json) record each test claim.
The [fourth and fifth test packet audits](independent-tests-4-5.json) record each test claim.
The [retry audit](retry-findings.json) records the narrowed packet dispositions. Provider output and execution records remain separate from this audit.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
