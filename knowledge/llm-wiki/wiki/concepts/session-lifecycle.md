---
title: "Session lifecycle"
type: concept
tags: [candidate-derived, security]
sources: [wb-candidate-security-kt-authentication-and-sessions, wb-candidate-requirements-req-active-session-renewal, wb-candidate-security-kt-sdk-and-entitlements]
workbench_status: candidate-derived
---

# Session lifecycle

This topic separates identity-provider authentication, Portal session continuity, entitlement retrieval, and application permission. The linked records remain candidate or draft knowledge.

## Core model

- Identity-provider session duration does not select the Portal refresh-token lifetime. [[wb-candidate-security-kt-authentication-and-sessions]]
- Eligible activity and successful renewal are intended to preserve an active session across the initial refresh-token expiry. [[wb-candidate-requirements-req-active-session-renewal]]
- Rejected or revoked credentials must not be renewed; the requested idle-expiry prompt remains available for another permitted attempt. [[wb-candidate-requirements-req-active-session-renewal]]
- Authentication tokens and entitlement tokens have different purposes. Entitlement retrieval does not establish application data permission enforcement. [[wb-candidate-security-kt-sdk-and-entitlements]]

## Open boundaries

Historical duration proposals conflict, and policy authority, applicable timing, Entra persistence, and implementation parity remain unresolved. The candidate requirement supplies target behavior and acceptance criteria, not production configuration or execution evidence. [[wb-candidate-security-kt-authentication-and-sessions]]
