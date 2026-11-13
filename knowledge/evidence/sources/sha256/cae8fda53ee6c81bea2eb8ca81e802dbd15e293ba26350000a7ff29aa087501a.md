## Murex Products CFI code mapping

The full list of Murex 2.11 Vostro SSI: The top 2 are 'Alert' SSI which are used for all applications, the remaining are Murex 2.11 specific securities.

MXG IRD LN_BR

| ~~SSI+ Security ID~~ | ~~SSI Security Name~~ | ~~Family~~ | ~~Group~~ | ~~Type~~ | ~~CFI Code~~ | ~~Comment~~ |
| --- | --- | --- | --- | --- | --- | --- |
| ~~SCBCRDCDS~~ | ~~MXG CRD CDS~~ | ~~CRD~~ | ~~CDS~~ | | ~~SC****~~ | |
| | | | | | ~~HC****~~ | ~~Credit Default Swap Single Reference Callable~~ ~~Multi Callable Extinguishing Range Accrual (CERA)~~ |
| ~~SCBCRDRTRS~~ | ~~MXG CRD RTRS~~ | ~~CDS~~ | ~~RTRS~~ | | ~~SC****~~ | ~~Not sure about the product~~ |
| ~~SCBIRDBOND~~ | ~~MXG IRD BOND~~ | ~~IRD~~ | ~~BOND~~ | | ~~JR****~~ | |
| ~~SCBIRDCF~~ | ~~MXG IRD CF~~ | ~~IRD~~ | ~~CF~~ | | ~~HR****~~ | ~~IR Derivatives\Swap or Struct Swap\IRS with Capped MTM Conservative Booking~~ ~~IR Derivatives\Swap or Struct Swap\Bullet KO KI Swap, Leveraged In Arrears Swap with KO Cap, Periodic Knock Out Swap, IR Derivatives\Options\Periodic Knock In Floor and Knock Out Cap~~ ~~SR****~~ |
| ~~SCBIRDIRS~~ | ~~MXG IRD IRS~~ | ~~IRD~~ | ~~IRS~~ | | ~~SR****~~ | |
| ~~SCBIRDCS~~ | ~~MXG IRD CS~~ | ~~IRD~~ | ~~CS~~ | | ~~SR****~~ | |
| ~~SCBIRDLNBR~~ | ~~MXG IRD LN_BR~~ | ~~IRD~~ | ~~LN_BR~~ | | ~~DY****~~ | ~~find a way to separate principle and interest for both loan and deposit~~ |
| ~~SCBIRDOPT~~ | ~~MXG IRD OPT~~ | ~~IRD~~ | ~~OPT~~ | ~~OTC~~ | ~~HR****~~ | ~~No identifier for OTC~~ |
| | | ~~CURR~~ | ~~FUT~~ | ~~FUT~~ | ~~FF****~~ | |
| ~~SCBCUFXFX~~ | ~~MXG CURR FXD FXD~~ | ~~CURR~~ | ~~FXD~~ | ~~FXD~~ | ~~JF****~~ | ~~FX Forward~~ |
| | | ~~CURR~~ | ~~FXD~~ | ~~FXD~~ | ~~JF***N~~ | ~~NDF~~ |
| | | ~~CURR~~ | ~~FXD~~ | ~~FXD~~ | ~~IF****~~ | ~~FX Spot~~ |
| ~~SCBCUFXXSW~~ | ~~MXG CURR FXD XSW~~ | ~~CURR~~ | ~~FXD~~ | ~~XSW~~ | ~~SF****~~ | ~~FX Swap~~ |
| ~~SCBCUOPASN~~ | ~~MXG CURR OPT ASN~~ | ~~CURR~~ | ~~OPT~~ | ~~ASN~~ | ~~HF****~~ | |
| | | ~~CURR~~ | ~~OPT~~ | ~~FLEX~~ | ~~HF****~~ | |
| ~~SCBCUOSMP~~ | ~~MXG CURR OPT SMP~~ | ~~CURR~~ | ~~OPT~~ | ~~SMP~~ | ~~HF****~~ | |
| ~~SCBCUOSMP~~ | ~~MXG CURR OPT SMP~~ | ~~SCF~~ | ~~SCF~~ | ~~SCF~~ | ~~MM****~~ | |

Reference:

Equity products CFI code: [BCS Cash Settlements - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/BCS+Cash+Settlements)