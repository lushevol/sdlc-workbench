| **Entitlement role** | **Location** | **Branches** | **Pre data entitlement changes implementation** |
| --- | --- | --- | --- |
| GBS | IN | All except PK , TZ , BD , LK, NP | IN users are holding GBS profile access, able view all countries cashflow details. |
| GBS | KL | All including PK & Indonesia, except TZ, BD, NP | KL users are holding GBS profile access, able view all countries cashflow details. |
| On shore | Any | Only specific country branch access based on the user domicile. | Eg : LK branch data can be accessed only by users in LK. Other country based users cannot view the same. |
| PSS / Dev | China | Read only access for All branches. | |
| PO | India | Read only access for All branches excluding PK | |
| PO | SG | Read only access for All branches including PK. | |
| On shore | Dubai | Read only access for Egypt and Saudi branches | |

| **Role (X_RATANONE)** | **Expected Countries** | **Profile Names** |
| --- | --- | --- |
| EMS2_ADMIN | (blank) | (blank) |
| FMO_COO | GB | RATAN - UK Onshore User |
| | HK | RATAN - HK Onshore User |
| | Not In PK, TZ, NP, BD | RATAN - Back2Back FMID, RATAN - GBS IN User |
| | Not In TZ, NP, BD | RATAN - GBS KL User |
| | SG | RATAN - SG Onshore User |
| | US | RATAN - US Onshore User |
| FMO_COO_SUP | HK | RATAN - HK Onshore User |
| | SG | RATAN - SG Onshore User |
| | US | RATAN - US Onshore User |
| FMO_KR_OPS | KR | RATAN - KR Onshore User |
| FMO_MO | Not In PK, TZ, NP, BD | RATAN - Back2Back FMID, RATAN - GBS IN User |
| FMO_MO_RO | AE, SA, QA, EG, BH | RATAN - UAE Onshore User |
| | CN | RATAN - CN Onshore User |
| | GB | RATAN - UK Onshore User |
| | HK | RATAN - HK Onshore User |
| | MY | RATAN - MY Onshore User |
| | Not In PK, TZ, NP, BD | RATAN - Back2Back FMID, RATAN - GBS IN User |
| | Not In TZ, NP, BD | RATAN - GBS KL User |
| | SG | RATAN - SG Onshore User |
| | TW | RATAN - TW Onshore User |
| | US | RATAN - US Onshore User |
| | (blank) | (blank) |
| FMO_MO_SUP | Not In PK, TZ, NP, BD | RATAN - Back2Back FMID, RATAN - GBS IN User |
| FMO_MO_TE | All | RATAN - Back2Back FMID, RATAN - ALL ACCESS User |
| | All except PK | RATAN - Back2Back FMID, RATAN - All Access Except PK |
| FMO_MO_TE_SUP | All | RATAN - Back2Back FMID, RATAN - ALL ACCESS User |
| | All except PK | RATAN - Back2Back FMID, RATAN - All Access Except PK |
| FMO_MO_TV | All | RATAN - Back2Back FMID, RATAN - ALL ACCESS User |
| | All except PK | RATAN - Back2Back FMID, RATAN - All Access Except PK |
| | GB | RATAN - UK Onshore User |
| | US | RATAN - US Onshore User |
| FMO_MO_TV_SUP | All | RATAN - Back2Back FMID, RATAN - ALL ACCESS User |
| | All except PK | RATAN - Back2Back FMID, RATAN - All Access Except PK |
| FMO_OPS_BO | Not In PK, TZ, NP, BD | RATAN - Back2Back FMID, RATAN - GBS IN User |
| | Not In TZ, NP, BD | RATAN - GBS KL User |
| | (blank) | RATAN - Clearing Ops |
| FMO_OPS_BOC | Not In PK, TZ, NP, BD | RATAN - Back2Back FMID, RATAN - GBS IN User |
| | Not In TZ, NP, BD | RATAN - GBS KL User |
| FMO_OPS_BOL | Not In PK, TZ, NP, BD | RATAN - Back2Back FMID, RATAN - GBS IN User |
| | Not In TZ, NP, BD | RATAN - GBS KL User |
| | (blank) | RATAN - Clearing Ops |
| FMO_OPS_BOM | Not In PK, TZ, NP, BD | RATAN - Back2Back FMID, RATAN - GBS IN User |
| | Not In TZ, NP, BD | RATAN - GBS KL User |
| | (blank) | RATAN - Back2Back FMID, RATAN - GBS IN User |
| | | RATAN - Clearing Ops |
| FMO_OPS_BOS | Not In TZ, NP, BD | RATAN - GBS KL User |
| | NP | RATAN - NP Onshore User |
| FMO_OPS_INV | Not In PK, TZ, NP, BD | RATAN - Back2Back FMID, RATAN - GBS IN User |
| | Not In TZ, NP, BD | RATAN - GBS KL User |
| | (blank) | RATAN - Back2Back FMID, RATAN - GBS IN User |
| FMO_OPS_MKR | Not In PK, TZ, NP, BD | RATAN - Back2Back FMID, RATAN - GBS IN User |
| | Not In TZ, NP, BD | RATAN - GBS KL User |
| | NP | RATAN - NP Onshore User |
| | (blank) | RATAN - Clearing Ops |
| FMO_OPS_SUP | Not In PK, TZ, NP, BD | RATAN - Back2Back FMID, RATAN - GBS IN User |
| | Not In TZ, NP, BD | RATAN - GBS KL User |
| FMO_RO | AE, SA, QA, EG, BH | RATAN - UAE Onshore User |
| | All | RATAN - Back2Back FMID, RATAN - ALL ACCESS User |
| | All except PK | RATAN - All Access Except PK |
| | BD | RATAN - BD Onshore User |
| | CN | RATAN - CN Onshore User |
| | GB | RATAN - UK Onshore User |
| | JP | RATAN - JP Onshore User |
| | LK | RATAN - LK Onshore User |
| | MY | RATAN - MY Onshore User |
| | Not In PK, TZ, NP, BD | RATAN - Back2Back FMID, RATAN - GBS IN User |
| | Not In TZ, NP, BD | RATAN - GBS KL User |
| | NP | RATAN - NP Onshore User |
| | SG | RATAN - SG Onshore User |
| | TW | RATAN - TW Onshore User |
| | TZ | RATAN - TZ Onshore User |
| | VN | RATAN - VN Onshore User |
| | (blank) | RATAN - Back2Back FMID, RATAN - GBS IN User |
| | | RATAN - Clearing Ops |
| | | RATAN - Prime User |
| | | RATAN - SG Onshore User |
| FMO_STA_CKR | Not In PK, TZ, NP, BD | RATAN - Back2Back FMID, RATAN - GBS IN User |
| | Not In TZ, NP, BD | RATAN - GBS KL User |
| FMO_STA_MKR | Not In PK, TZ, NP, BD | RATAN - Back2Back FMID, RATAN - GBS IN User |
| | Not In TZ, NP, BD | RATAN - GBS KL User |
| KR_PSS_RO | KR | RATAN - KR Onshore User |
| NON_FMO_RO | AE, SA, QA, EG, BH | RATAN - UAE Onshore User |
| | All | RATAN - Back2Back FMID, RATAN - ALL ACCESS User |
| | CN | RATAN - CN Onshore User |
| | DE | RATAN - DE Onshore User |
| | EG | RATAN - EG Onshore User |
| | GB | RATAN - UK Onshore User |
| | ID | RATAN - ID Onshore User |
| | LK | RATAN - LK Onshore User |
| | Not In PK, TZ, NP, BD | RATAN - Back2Back FMID, RATAN - GBS IN User |
| | SG | RATAN - SG Onshore User |
| | ZA | RATAN - ZA Onshore User |
| PSS_RO | All | RATAN - Back2Back FMID, RATAN - ALL ACCESS User |
| | All except PK | RATAN - Back2Back FMID, RATAN - All Access Except PK |
| | (blank) | RATAN - Back2Back FMID, RATAN - ALL ACCESS User |
| (blank) | AE, SA, QA, EG, BH | RATAN - UAE Onshore User |
| | All | RATAN - Back2Back FMID, RATAN - ALL ACCESS User |
| | DE | RATAN - DE Onshore User |
| | GB | RATAN - UK Onshore User |
| | IN | RATAN - IN Onshore User |
| | MY | RATAN - MY Onshore User |
| | Not In PK, TZ, NP, BD | RATAN - Back2Back FMID, RATAN - GBS IN User |
| | Not In TZ, NP, BD | RATAN - GBS KL User |
| | SG | RATAN - SG Onshore User |
| | (blank) | RATAN - Back2Back FMID, RATAN - ALL ACCESS User |
| | | RATAN - SG Onshore User |