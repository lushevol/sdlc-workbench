# Source-reported performance observations

These observations belong to task evidence. They do not define canonical business intent.

The SLA capacity page labels daily volume as current: Trade 158,263; Settlement GDC 173,610; ISO Korea 3,898; total 335,771. It reports concurrent users changing from 89 to 103 per minute and total users from 386 to 545. No measurement period, collection method, approval, or retained execution output was inspected. Peak volume is separately labeled an assumption; it remains qualified in the intent candidate.

[Reported volumes and user counts](../../../knowledge/evidence/sources/sha256/51ee793f59a1db606970bf6df3627151d7b09f2a48da68a6c291a64e99f3f273.md#L15-L23)

The architecture test plan reports six VMs and two database nodes, with business and infrastructure services sharing resources across two data centers. It describes resource shortage and difficult fault isolation. It also states that six VMs have been added, services reorganized, and configuration adjusted. These are source-reported implementation or risk observations. No deployed topology, resource telemetry, incident, change execution, or performance result was inspected.

[Reported topology, changes, and risks](../../../knowledge/evidence/sources/sha256/981637c57f4daa20684d179fcd28eac041f9e315a06b7b0a22c53395b0673f03.md#L11-L17)

Owner: unknown. Next action: bind dated environment, build, configuration, topology and measurement evidence before using these observations operationally.

standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations: Original and selected-view hashes remain bound by the prior performance review. Source reports do not prove current runtime or execution.
