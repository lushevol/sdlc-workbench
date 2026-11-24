# Function entitlement discussion answers

- Source: User answers to asynchronous questions in the current Codex conversation.
- Date: 2026-11-17, Asia/Singapore.

## FUNC-Q1 exact question and answer

Question: For one account, can multiple X_RATANONE functional profiles be valid simultaneously?

Exact answer: Exactly one functional profile per account

## FUNC-Q2 exact question and answer

Question: For case 6, should we verify only that function_entitlement never contains the wrong account-type profile, or also verify CES rejects the assignment?

Exact answer: Also verify CES rejects incompatible assignments

## Effect and limits

One assigned functional profile is allowed. An account without one still requires the agreed empty value.
Tests must verify both incompatible assignment directions and retain the original functional value after rejection.
The answers authorize case definitions. No provisioning or live execution has occurred.

## FUNC-Q3 and FUNC-Q4 exact question and answer

Question: What update boundary should cases use: the first API read after CES confirms the assignment change, or a documented propagation delay? Also, does “general account” include Generic, System, and Service accounts?

Exact answer: both, and yes.

Interpretation: cover the first read after CES confirms the change and the documented propagation limit.
General accounts include Generic, System, and Service accounts.
The maximum delay and its exact clock origin remain unknown.
Immediate correctness and deadline conformance require separate reported results.
Later correctness cannot erase an incorrect immediate read.
