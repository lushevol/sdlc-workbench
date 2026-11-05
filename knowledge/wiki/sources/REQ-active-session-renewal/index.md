# Active session renewal

Derived navigation. Source state: candidate/draft. This page grants no approval.

[Wiki index](../../index.md)

Canonical record: [REQ-active-session-renewal, version 7](../../../candidates/requirements/REQ-active-session-renewal.md#L2-L7).

## Summary

The requirement defines renewable active portal sessions and recoverable manual renewal.
Its seven criteria record intended behavior; implementation conformance and publication remain separate.
See the canonical [intended scope](../../../candidates/requirements/REQ-active-session-renewal.md#intended-scope).

## Key rules and qualifiers

- Mouse, keyboard, and scroll activity must each support successful renewal under the controlled criterion conditions.
  See [AC-1](../../../candidates/requirements/REQ-active-session-renewal.md#L156-L159), [AC-2](../../../candidates/requirements/REQ-active-session-renewal.md#L163-L166), and [AC-3](../../../candidates/requirements/REQ-active-session-renewal.md#L170-L173).
- Continued eligible activity and successful responses must avoid elapsed-time-only reauthentication across initial refresh-token expiry.
  See [AC-4](../../../candidates/requirements/REQ-active-session-renewal.md#L177-L181).
- A pending manual renewal must keep the expiry prompt open.
  See [AC-5](../../../candidates/requirements/REQ-active-session-renewal.md#L185-L188).
- Successful manual renewal must close the prompt exactly once after completion.
  See [AC-6](../../../candidates/requirements/REQ-active-session-renewal.md#L192-L195).
- Rejected manual renewal must preserve the prompt and permit another attempt.
  See [AC-7](../../../candidates/requirements/REQ-active-session-renewal.md#L199-L202).
- Expired or revoked credentials cannot authorize renewal. Controlled intervals introduce no production timeout setting or proof of indefinite execution.
  See [rationale](../../../candidates/requirements/REQ-active-session-renewal.md#rationale) and [fixture limits](../../../candidates/requirements/REQ-active-session-renewal.md#L205-L207).

## Unresolved questions and limits

- Which session owner will review the candidate before publication?
  See the [next action](../../../candidates/requirements/REQ-active-session-renewal.md#L209-L211).
- Which separate integration evidence covers activity inside cross-origin embedded applications?
  See [review limits](../../../candidates/requirements/REQ-active-session-renewal.md#L104-L108).

Owner: unknown. Next action: obtain the applicable review and preserve the separate integration boundary.

## Connections

- [Authentication and sessions](../KT-authentication-and-sessions/index.md)
- [SDK and entitlements](../KT-sdk-and-entitlements/index.md)

The [authentication topic](../../../candidates/security/KT-authentication-and-sessions.md#intended-session-renewal) links the canonical session criteria.
The [SDK topic](../../../candidates/security/KT-sdk-and-entitlements.md#L516-L517) retains their separate verification boundary.
