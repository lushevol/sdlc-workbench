Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Yunzhe Ta @Junying Jiang | 2026-01-21 | @Yunzhe Ta @Pengpeng Li | 2026-01-21 | |

### Description:

FM-BPMS-LMS extracts/receives the cashflow data from RATAN for Liquidity management

As a system may have a data feed for multiple countries, please list here the countries in scope for this OLA data feed:

| Source System | Data Feed | Countries in scope |
| --- | --- | --- |
| Stella | Accumulator / Decumulator, TRS - Equity Swaps, OTC Options, Structured Product, SCF | HK,UK,SG, Jersey* *Note: Jersey entity will not flow to SAIL-LMS |
| FMRP | CURR | FXD-FXD ,CURR | FXD-XSW, CURR | OPT-SMP, CURR | OPT-ASN, COM | SWAP, CRD | RTRS, CRD | CDS, SCF | SCF-SCF, IRD | CF, IRD | IRS, IRD | CS, IRD | LN_BR, IRD | BOND | CN,IN,SG,UK,DE, HK, DUBAI,NEWYORK, DIFC *Note: Egypt,Malaysia, Nepal, Saudi, South Africa, Taipei, OBU-Taipei, Bangkok, SCS HK, MAURITIUS, JAKARTA, MANILA, TOKYO, JOBURG, PHILIP FCU should not flow to SAIL-LMS |
| LOANIQ | XQTXXX - term loan XQRXXX - revolving loan XQXXXX – default loan | UK, SG and HK |

### E2E Data Flow:

Ratan --(Solace)-->LMS

### Connection details:

### Interface Specification:

- [LMS Feed - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/LMS+Feed)
- [https://confluence.global.standardchartered.com/display/FMEDMI/BCS+-+Sophis+Decom+-+Service+Specs](https://confluence.global.standardchartered.com/display/FMEDMI/BCS+-+Sophis+Decom+-+Service+Specs)

### Interface team contact:

### OLA:

BPMS OLA location, no change required

[RATAN - OLA - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/RATAN+-+OLA)

### Other Useful Docs:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Known Issues:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Troubleshooting Steps:

Describe whom and where to check if any interface related issue. Click to edit the macro and add or change labels.