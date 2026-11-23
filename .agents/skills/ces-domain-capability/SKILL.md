---
name: ces-domain-capability
description: Investigate CES entitlement models, effective access, data scope, integration contracts, and EMS2 or EMS3 compatibility. Use for CES domain questions, access differences, and permission verification.
---

# CES domain capability

1. Identify the CES application, entity, environment, and evidence date or revision. Include the provider and affected integration when they matter.
2. Locate applicable decisions, contracts, and source revisions using the [knowledge query workflow](../query-knowledge/SKILL.md).
3. Follow the relevant route below. Distinguish intended access, configured access, and observed enforcement.

| Task | Domain procedure |
| --- | --- |
| Explain an entitlement or access difference | Trace the application and entity to role memberships, effective subject and action permissions, and the applicable data profiles and policies. |
| Review a CES integration or consumer | Inspect provider, adapter, and caller together. Check identity, cardinality, empty and error responses, and where the permission is enforced. |
| Compare EMS2 and CES behavior or review a mixed rollout | Use the [migration compatibility workflow](references/migration-compatibility.md) for static inspection and CES replay for captured responses. |

Keep role names, application identity, functional permissions, and data scope distinct.
Trace the owner and rule for any computed permission or data filter. Report missing policy or evidence as unresolved.
Use the [CES evidence and learning guide](references/capability-learning.md) to interpret replay and capture reusable findings.
Keep tenant-specific access decisions in governed knowledge. Route entitlement or policy changes through [knowledge governance](../govern-knowledge/SKILL.md).
