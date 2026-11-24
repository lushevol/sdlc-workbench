Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Junying Jiang @Yunzhe Ta | 2026-01-19 | @Daiqi Wang @Yunzhe Ta @LiPing Gao | 2026-09-29 | |

### Description:

Describe the background and purpose of the flow.

> **INFO**
> CDUPS call Ratan for trade stamping **via api **
>
> CDUPS send trade confirmation event to RATAN for BCS trade
>
> CDU-IS to subscribe Trade messages from RATAN for confirmation
>
> **Trade confirmation:**
>
> MUREX trade (booked in Murex) confirmation happened in **CDUPS,** CDUPS send trade confirmation event to TDS3, RATAN sync trade state (cashflow STP condition) from TDS3
> BCS trade (booked in EDrisque) confirmation happened in **CDUPS**, CDUPS send trade confirmation event to RATAN (inbound, outbound),TDS3 has no such data
> FMRP trade (booked in Blade) confirmation in **CDUPS**, CDUPS call stella api, stella will update trade status and send trade xml to RATAN via tds3
>
>
>
> **From RATAN-CDUPS OLA:**
>
> | **Flow / Interface** | **Integration Type** | **Business Purpose** | **Provider -> Consumer** | **Data Direction** | **Protocol / Format** | **Interface / Endpoint** | **Method** | **Queue / Topic** | **Frequency** | **Control Requirement** |
> | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
> | Flow 1 | Message Flow (EDMi) | Display Confirmation Status (Conf. Status) in the RATAN Trade Blotter | CDUPS -> RATANONE (via FM-EDMi) | CDUPS -> FM-EDMi -> RATANONE | JMS-JSON | EDMi path to be confirmed and added in OLA | N/A | q-51358-ratanone-cdu-cofstatus-ratan | Realtime (event-driven) | Provides confirmation status data consumed by RATAN Trade Blotter. |
> | Flow 2 | API Integration | Trade SSI stamping enrichment | 51358-RATAN -> 51512-CDUPS (consumer calls RATAN endpoint) | CDUPS -> RATAN | HTTPS + JSON | https://fmo-shell.gdc.standardchartered.com:8453/api/v1/stampings/trade/enrich | POST | N/A | Realtime (triggered by CDUPS) | Mandatory request fields: trackingId, tradeId, productType, message. Optional fields: isScbml, cfiCode. |

### E2E Data Flow:

Describe the end to end  flow.

> You may want to use a panel to highlight different Flow details for different purpose
> 1. Stamping: CDUPS call Ratan API for trade SSI stamping
> 2. CDUPS →Solace →Ratan (trade confirmation)
> 3. Ratan →Solace →CDUPS (trade info)

### Connection details:

### Interface Specification:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Interface team contact:

### OLA:

BPMS OLA location, no change required

[RATAN - OLA - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/RATAN+-+OLA)

### Other Useful Docs:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Known Issues:

### Troubleshooting Steps:

Describe whom and where to check if any interface related issue. Click to edit the macro and add or change labels.