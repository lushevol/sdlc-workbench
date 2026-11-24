**Problem statement**: SABRE rollout its strategic trade format **uber** to replace SCBML, as a result of this, the downstream of sabre who is relying on SCBML are being requested to upgrade, CDU is one of downstream, while CDUPS is also relying on SSI stamping service where offered by RATAN for its client document generation, so upgrade SSI service to accommodate the new requirement is become mandatory.

**MOM:**

1. Given trade and cashflow stamping must be sitting together, Reiterate the necessity of having central SSI stamping service and all are aligned.
2. [@Ghorpade, Amol](mailto:Amol.Ghorpade@sc.com) [@Ahamed, Fayaz](mailto:Fayaz.Ahamed@sc.com) confirmed that the notification on vostro refresh is required for CDUPS based on confirmation client (ad-hoc, call based) request. 1. SSI Vostro refresh (not publish to CDUPS) 2. Ratan Nostro refresh (not publish to CDUPS) 3. Settlement Ops ad-hoc SSI stamping (not publish to CDUPS, may required only on CDUPS call based) 4. Fixing Notice - will response to CDUPS with latest cashflow SSI stamping result, prior to general SSI stamping result 5. Trade event - CDUPS will make a call again. 6. There maybe scenario that post trade SSI stamping, cashflow SSI stamp with different SSI, so CDUPS would query the latest cashflow SSI on call basis. 7. Trade SSI query will use request date/trade date??? to be compared with SSI effective date @Amol Ashok Ghorpade
3. [@Ghorpade, Amol](mailto:Amol.Ghorpade@sc.com) [@Ahamed, Fayaz](mailto:Fayaz.Ahamed@sc.com) confirmed that the exception handling between CDUPS and RATAN is required.
4. All agreed that upgraded SSI stamping service should accept the trade id and version that can unique identified a uber message from TL instead of pass the uber message as parameter which too heavy .
5. SSI stamping service to response a post stamped uber message to CDU
6. The protocol of response stamped message to CDUPS can be via solace given the size of message could be large, to be further assessed along with the new solution.

# Business Requirement and Cases

## Vostro and Nostro Stamping

| | Trade ID | Currency | Cashflow ID | Payment Date | SSI ID | Comment |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | T1 | USD | C1 | Jan 01 2025 | 123 | |
| 2 | T1 | USD | C2 | Feb 01 2025 | 123 | |
| 3 | T1 | USD | C3 | Mar 01 2025 | 456 | |
| 4 | T1 | USD | C4 | Apr 01 2025 | 456 | |
| 5 | T1 | USD | C5 | May 01 2025 | 456 | |
| 6 | T1 | USD | C6 | Jun 01 2025 | 789 | |

## Vostro and Nostro Stamping

| | Event | Action | Comment |
| --- | --- | --- | --- |
| 1 | Trade T1 Booked | Ratan would extract T1's parameter according to production template. | Product Template: Buy currency will have Nostro Sell currency will have Vostro and Nostro |
| 2 | | SSI stamping service would stamp Vostro an Nostro according to T1's parameter, and generate response with Vostro and Nostro / exceptions as extension | |
| 3 | | SSI stamping service send the response to CDUPS through solace. | |
| 4 | Cashflow (C1...Cn)Materialized in T1 | C1 would query trade SSI stamping result for T1 with latest major version. | |

## Vostro Refresh

| | Event | Action |
| --- | --- | --- |
| 1 | Vostro Refresh | Vostro refresh notification sends from SSI+ |
| 2 | | RATAN identify impacted trade (T2) |
| 3 | | SSI stamping service would re-stamp Vostro an Nostro, and generate response with Vostro and Nostro / exceptions as extension |
| 4 | Vostro Refresh impact on cashflow | Cashflow (C1...Cn) with the same trade ID T2 would re-stamp Vostro an Nostro with T1 and latest major version. |
| 5 | CDUPS Query | SSI stamping service send the response to CDUPS with latest stamping result. |

## Nostro Refresh

| | Event | Action |
| --- | --- | --- |
| 1 | Nostro Refresh | Nostro refresh notification sends from Nostro static |
| 2 | | RATAN identify impacted trade (T2) |
| 3 | | SSI stamping service would re-stamp Nostro, and generate response with Vostro and Nostro / exceptions as extension |
| 4 | Nostro Refresh impact on cashflow | Cashflow (C1...Cn) with the same trade ID T2 would re-stamp Nostro with T1 and latest major version. |
| 5 | CDUPS Query | SSI stamping service send the response to CDUPS with latest stamping result. |

## Adhoc SSI/Multi Vostro/Missing Vostro/Missing Nostro

| | Event | Action |
| --- | --- | --- |
| 1 | Adhoc SSI/Multi Vostro/Missing Vostro/Missing Nostro | Settlement Ops user performed adhoc SSI on C1 and approved. |
| 2 | | SSI stamping service would re-stamp Vostro an Nostro on corresponding T1, and generate response with Vostro and Nostro as extension |
| 3 | CDUPS Query | SSI stamping service send the response to CDUPS with latest stamping result. |

Solution 1

Solution 2