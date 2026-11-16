# Portal reported observations

This document retains reported observations with their original qualifications.
The source documents supply historical evidence.
Current execution and deployment require independent evidence.

## May 2023 reported rendering measurements

The draft reports login FCP 0.8 seconds and LCP 1.3 seconds.
It reports home FCP 0.9 seconds and LCP 1.3 seconds.
The underlying screenshots and measurement captures are absent from this supplied copy.
These reported values cannot establish present performance or capacity.
[May 2023 document, result tables, lines 230–256](<../../../knowledge/evidence/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/MFE Performance Monitoring/FMO Post Trade Portal Frontend Performance Testing May 2023/page.md#L230>)

## Reported UAT throughput workload and results

The UAT throughput page describes 500 users, a 250-second ramp-up, and five iterations.
It reports 17,500 successful requests and a maximum response time of 2,023 milliseconds.
That maximum concerns `/api/auth/v2/sso/validate` in the reported test.
The source links a JMeter plan and result archive that are absent from this supplied copy.
The summary alone does not establish current production capacity or verified business behavior.
[UAT throughput, workload and result summary, lines 11–42](<../../../knowledge/evidence/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Throughput Testing in UAT/page.md#L11>)

## Reported OpenFin POC compatibility observations

### Compatibility observations

The technical issue page reports that two FDC3 libraries did not exchange broadcast messages in its POC.
It reports intent errors with one library and successful intent handling with the other.
Its workaround uses `fdc3-2.1` for broadcast and `openfin-fdc3` for intents.
These are reported POC observations, without current reproduction or a supported compatibility guarantee.
The referenced screenshots and source archives are absent from this supplied copy.
[Technical issue, observations and workaround, lines 1–29](<../../../knowledge/evidence/sources/confluence/FM TPT UI Guild/OpenFin/5. Technical Issue/page.md#L1>)
[Getting Started, source archives, lines 30–36](<../../../knowledge/evidence/sources/confluence/FM TPT UI Guild/OpenFin/2. Getting Started/page.md#L30>)

## Retained SQL configuration observations

### Historical persistence relationships

The Flyway page configures a schema-history table and enables migration baselining from version zero.
Its SQL defines import-map records with unique keys and categories with unique labels.
Tile records reference both category and import-map records through foreign keys.
Separate import-map, category, and tile audit tables preserve the design's change-history vocabulary.
These relationships describe retained SQL, rather than a confirmed deployed schema or executed migration.
[Flyway configuration and schema, lines 16–24, 77–220](<../../../knowledge/evidence/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Flywaydb/page.md>)

## Retained firewall register context

The retained firewall register supplies operational connectivity context for tenant onboarding.
Its addresses and contact details remain in the original material.
Current network approvals and reachability were not verified.
[Firewall operational register, lines 1–8](<../../../knowledge/evidence/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Firewall Configurations/page.md>)

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
  - Verbatim historical quotations retain their original wording.
```
