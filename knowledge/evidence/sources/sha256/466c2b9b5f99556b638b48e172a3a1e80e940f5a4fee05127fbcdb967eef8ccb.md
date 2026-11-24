Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Yunzhe Ta @Junying Jiang | 2026-01-21 | @Yunzhe Ta @Fengke Wu | 2026-01-21 | |

### Description:

FXU call Ratan API to query cashflow status

FXU send utilize request(FullUtilize) for accounting to Ratan via solace.

Product: SPOT/Forward/SWAP

### E2E Data Flow:

FXU call Ratan API to query cashflow status

API Call: MX-FXCASH(FXU) -> Ratan API

Product: SPOT/Forward/SWAP

Message format: JSON

To consume utilization request and response: FXU→ Solace Topic1 → Solace Queue1 → RATANONE→ Solace Topic2- Solace Queue2 ->FXU

### Connection details:

### Interface Specification:

[FXU Tech Detail Design - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/FXU+Tech+Detail+Design)

### Interface team contact:

### OLA:

BPMS OLA location, no change required

[RATAN - OLA - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/RATAN+-+OLA)

### Other Useful Docs:

[FXU Tech Detail Design - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/FXU+Tech+Detail+Design)

[FXU Technical Design - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/FXU+Technical+Design#FXUTechnicalDesign-FXURequest/Response)

### Known Issues:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Troubleshooting Steps:

Describe whom and where to check if any interface related issue. Click to edit the macro and add or change labels.