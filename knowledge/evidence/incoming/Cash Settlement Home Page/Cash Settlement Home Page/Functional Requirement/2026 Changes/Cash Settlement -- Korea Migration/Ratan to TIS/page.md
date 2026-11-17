# Background

As some payment need to manually key-in everyday via OLTP(UI), user hope that those payment information could get automatically from API.

Once cashflow is Released status in Ratan side, then SSI update is not supported.

Withdrawal cashflow will not be available for TIS/OTLP query, cashflow status will be in Settled with Reversed/Reversal flag.

# Payment types

1. For pay-side API, including UI-NO: 5338, 5339, 5318, 5319, 5323, 5324, 5325, all in scope to go live during July for RATAN & TIS.
2. Direct debit payment. 0201 and 3013 both in scope.

| | To TIS with 2 API |
| --- | --- |
| Filter A | STTL_MEANS = NOX and STTL_Account like ('%UISUS%' or '%UIBOK%' ) & Cashflow.Pay_Receive_Indicator ='Pay'& Cashflow.Cashflow_State in ('Released','Settled') & Cashflow.Cashflow_Event_Reason <> 'Reversal' & Cashflow.Payment_Date=Param 'settDate' & Entity.Booking_Entity_SCI_FMID='10036645' |
| Filter B | STTL_MEANS = NOX and STTL_Account like ('%UIDD%' ) & Cashflow.Pay_Receive_Indicator ='Receive' & Cashflow.Cashflow_State in ('Released','Settled') & Cashflow.Cashflow_Event_Reason <> 'Reversal' & Cashflow.Payment_Date=Param 'settDate' & Entity.Booking_Entity_SCI_FMID='10036645' |

Pay-side

| UI NO | Explanation | 57BIC | Settlement_Instruction.Account.SCB_Nostro_Account_Number | Currency | if M_BEN_ACC exists | Current through | Target through | in Payment method | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5338 | Internal Movement | SCBLKR | %UISUS% | KRW | Y start with 'BR%' | UI(OLTP) | TIS->UI(OLTP) | 1 | Manual |
| 5339 | Internal Movement | SCBLKR | %UISUS% | FCY | Y start with 'BR%' | UI(OLTP) | TIS->UI(OLTP) | 1 | Manual |
| 5319 | USD internal account. | SCBLKR | %UISUS% | FCY | Y not start with 'BR%' | UI(OLTP) | TIS->UI(OLTP) | 4 | Manual |
| 5318 | KRW settlement case. Book transfer | SCBLKR | %UISUS% | KRW | Y not start with 'BR%' | UI(OLTP) | TIS->UI(OLTP) | 4 | Manual |
| 5323 | another bank(IRN) | No-SCBLKR | %UISUS% | KRW | Y not start with 'BR%' | UI(OLTP) | TIS->UI(OLTP) | 3 | Manual |
| 5324 | bank of korea settlement | No-SCBLKR | %UIBOK% | KRW | N('dummy' or NULL) | UI(OLTP) | TIS->UI(OLTP) | 2 | Manual |
| 5325 | end client account. | No-SCBLKR | %UIBOK% | KRW | Y not start with 'BR%' | UI(OLTP) | TIS->UI(OLTP) | 2 | Manual |
| Not in TIS scope | Foreign currency External Client(Receiver BIC is external) | No-SCBLKR | not like %UIBOK% and not like %UISUS% | FCY | | ENISIS(MX+MT210) | ENISIS(MX+MT210) | 5 | Auto |

| Payment Method | |
| --- | --- |
| 1 | Internal Movement: Transfer funds to another branch, through UI(OLTP), krw&fcy, not in RAZOR-TIS |
| 2 | BOK-Wire: External transfer funds, KRW only, RAZOR, through UI(OLTP) |
| 3 | Interbank Remittance Network: External transfer funds via Interbank remittance network, RAZOR, KRW only |
| 4 | Credit to the account held in SCBK: KRW&FCY, RAZOR |
| 5 | SCBLKR to no SCB KR bank with foreign currency: to RATAN -- ENISIS |

# TIS GUI

![image-2026-3-6_9-9-42.png](attachments/image-2026-3-6_9-9-42.png)

# OLTP(UI)

![image-2026-3-6_9-10-51.png](attachments/image-2026-3-6_9-10-51.png)

All these payment will not generate Accounting and Swift messages in RATAN.

# API

| URL | POST header |
| --- | --- |
| [https://fmo-mfe-preprod.pi.dev.net:8453/api/ratan/v1/tis/query/payment/{paymentDate}](https://fmo-mfe-preprod.pi.dev.net:8453/api/ratan/v1/tis/query/payment/%7BpaymentDate%7D) | FMAA-token {your fmaa toke} FMAA-userId {your fmaa user id} FMAA-appId {your fmaa appId} |
| [https://fmo-mfe-preprod.pi.dev.net:8453/api/ratan/v1/tis/query/receipt/{paymentDate}](https://fmo-mfe-preprod.pi.dev.net:8453/api/ratan/v1/tis/query/receipt/%7BpaymentDate%7D) | FMAA-token {your fmaa toke} FMAA-userId {your fmaa user id} FMAA-appId {your fmaa appId} |

# Field Mapping for (UISUS or UIBOK)

TIS Query Parameter

| Field Name | Optional/Mandatory | Description | Format | Sample |
| --- | --- | --- | --- | --- |
| settDate | M | User manually select from TIS | YYYY-MM-DD | 2026-04-25 |

Sample API response

**EXPAND: RATAN - TIS Sample response**

{
    "msg": "success",
    "data": {
        "columns": [
            "AUDITTIMESTAMP",
            "CASHFLOWNO",
            "PRODUCT",
            "TYPE",
            "SETTDATE",
            "UINO",
            "CCY",
            "AMOUNT",
            "CNO",
            "SN",
            "AMT_IND",
            "PAYACCT_BR",
            "PAYACCT_IND",
            "PAYACCT_GLNO",
            "BIC",
            "BANKCD",
            "BOKCD",
            "BR_NM",
            "DEPACCT",
            "DEP_REQ_NM",
            "DEP_REQ_IND",
            "DEP_REQ_AR",
            "DEP_REQ_CMS",
            "COMMENTS",
            "COMMENT_ENG",
            "PAY_TM",
            "DEP_INF_IND",
            "DEP_IDENTITY",
            "FEE_IND",
            "FEE_REASON",
            "PRINT_IND",
            "STAT",
            "ACCOUNTTYPE",
            "BENE_FULL_NAME",
        ],
        "rows": [
            {
                "AUDITTIMESTAMP": "2026-02-03 06:02:08.584",
                "CASHFLOWNO": "M00126049621",
                "PRODUCT": "FXD",
                "TYPE": "FXD",
                "SETTDATE": "2026-01-22",
                "UINO": "5318",
                "CCY": "KRW",
                "AMOUNT": "73892",
                "CNO": "10075222",
                "SN": "STANCHART BK LDN",
                "AMT_IND": "2",
                "PAYACCT_BR": "017",
                "PAYACCT_IND": "5",
                "PAYACCT_GLNO": "000287",
                "BIC": "SCBLKRSEXXX",
                "BANKCD": null,
                "BOKCD": null,
                "BR_NM": null,
                "DEPACCT": "03910010005",
                "DEP_REQ_NM": "SCBK",
                "DEP_REQ_IND": null,
                "DEP_REQ_AR": null,
                "DEP_REQ_CMS": null,
                "COMMENTS": "SCBK",
                "COMMENT_ENG": "SCBK",
                "PAY_TM": null,
                "DEP_INF_IND": "01",
                "DEP_IDENTITY": "1028121843",
                "FEE_IND": null,
                "FEE_REASON": null,
                "PRINT_IND": null,
                "STAT": "0",
                "ACCOUNTTYPE": "GB",
                "BENE_FULL_NAME": "SCB HK"
            }
        ]
        
    }
}

**EXPAND_END**

| | Field Name | Field Description | Format | If used in | Logic Model | Value Sample | Remarks |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | AUDITTIMESTAMP | Time when message generate | datetime not null | ALL | TO_CHAR(SYSTIMESTAMP, 'yyyy-mm-dd hh:mm:ss.ff3') AS AUDITTIMESTAMP | 2026-02-03 06:02:08.584 | |
| 2 | CASHFLOWNO ~~DEALNO~~ | Cashflow ID | CHAR(12) not null | ALL | Cashflow.Cashflow_Id | M00126049621 | |
| 3 | ~~SEQ~~ | | ~~CHAR(1)~~ | | if net/split/SSI modify, could be '9' if not net/split/SSI modify, check if swap product (near leg, then '0' far leg, then '1') | null | |
| 4 | PRODUCT | Group | CHAR(5)-->CHAR(200) | ALL | trim(Instrument_Common.Murex_Product_Group) | IRS | If any fields only related to FMRP could replace |
| 5 | TYPE | Type | CHAR(20)-->CHAR(200) | ALL | trim(Instrument_Common.Murex_Product_Type) | CS | If any fields only related to FMRP could replace |
| 6 | SETTDATE | Payment Date | DATE yyyy-mm-dd | ALL | Cashflow.Payment_Date | 2026-01-22 | |
| 7 | UINO | Payment type in TIS | CHAR(4) not null | ALL | case when Settlement_Instruction.Account.Beneficiary_Account_Number not like 'BR%' then ( case when ((Settlement_Instruction.Account.Beneficiary_Account_Number not null) and (Settlement_Instruction.Account.Beneficiary_Account_Number not equal 'dummy')) then( case when Settlement_Instruction.Account.SCB_Nostro_Account_Number like '%UISUS%' then ( case when Cashflow.Payment_Currency in('KRW','KRO') then ( case when Settlement_Instruction.Account.Beneficiary_Bank_BIC_code like 'SCBLKR%' then '5318' else '5323' end) else '5319' end) else '5325' end) else '5324' end) else(case when Cashflow.Payment_Currency in ('KRO', 'KRW') then '5338' else '5339' end) end as UINO Please notice: the word 'DUMMY' in *Settlement_Instruction.Account.**Beneficiary_Account_Number* is not case-sensitive. | 5318 | 57BIC: Settlement_Instruction.Account.Beneficiary_Bank_BIC_code 59Account:Settlement_Instruction.Account.Beneficiary_Account_Number Nostro account:Settlement_Instruction.Account.SCB_Nostro_Account_Number |
| 8 | CCY | ISO Currency | CHAR(3) not null | ALL | Cashflow.Payment_Currency //ISO_CODE | KRW | |
| 9 | AMOUNT | Rounded amount | NUMBER(24,8) not null | ALL | trim(Cashflow.Payment_Amount) | 73892 | |
| 10 | CNO | Counterparty FMID | CHAR(20) not null | ALL | trim(Entity.Counterparty_SCI_FMID) | 10075222 | |
| 11 | SN | Counterparty FMCODE | CHAR(35) not null | ALL | trim(Entity.Counterparty_SCI_FMCODE) | STANCHART BK LDN | |
| 12 | AMT_IND | Amount of category | CHAR(1) not null | 5338, 5318, 5323 | Hardcoded '2' | 2 | |
| 13 | PAYACCT_BR | Payment account branch | CHAR(3) not null | ALL | Hardcoded '017' | 017 | |
| 14 | PAYACCT_IND | Payout Accounts (Classification) 5-Online payment of bank bills 6-Online payment of foreign currency expenses | CHAR(1) | 5338, 5339, 5318, 5319 | case when ( Cashflow.Payment_Currency in ('KRO', 'KRW') and Settlement_Instruction.Account.SCB_Nostro_Account_Number not like '%UIBOK%' and Settlement_Instruction.Account.Beneficiary_Bank_BIC_code = 'SCBLKRSEXXX' ) then '5' //5318 5338 when (Cashflow.Payment_Currency <> ('KRO') and Cashflow.Payment_Currency <> ('KRW')) then '6' //5319 5339 else '' //5323 5324 5325 | 5 | |
| 15 | PAYACCT_GLNO | Suspense account number | CHAR(6) | 5338, 5339, 5318, 5319 | case when ( Cashflow.Payment_Currency in ('KRO', 'KRW') and Settlement_Instruction.Account.SCB_Nostro_Account_Number not like '%UIBOK%' and Settlement_Instruction.Account.Beneficiary_Bank_BIC_code = 'SCBLKRSEXXX' ) then '000287' //5318 5338 need new account to replace '000287' when (Cashflow.Payment_Currency <> 'KRO' and Cashflow.Payment_Currency <> 'KRW') then '040446' //5319 5339 need new account to replace '040434' else '' //5323 5324 5325 end as PAYACCT_GLNO, | 040434 | |
| 16 | BIC | 57 BIC | CHAR(11) not null | ALL | trim(Settlement_Instruction.Account.Beneficiary_Bank_BIC_code) as BIC | SCBLKRSEXXX | |
| 17 | BANKCD | | | ALL | Hardcoded '' | null | |
| 18 | BOKCD | | | ALL | Hardcoded '' | null | |
| 19 | BR_NM | | | ALL | Hardcoded '' | null | |
| 20 | DEPACCT | 59 Account | CHAR(34) not null | 5338, 5339, 5318, 5319, 5323, 5325 | trim(Settlement_Instruction.Account.Beneficiary_Account_Number) | 03910010005 | |
| 21 | DEP_REQ_NM | | VARCHAR(100) not null | 5318, 5319, 5323, 5324, 5325 | Hardcode 'SCBK' | SCBK | |
| 22 | DEP_REQ_IND | Client Population 2-Financial institutions (including pension funds) | CHAR(1) | 5325 | case when (Cashflow.Payment_Currency in ('KRO','KRW') and Settlement_Instruction.Account.SCB_Nostro_Account_Number like '%UIBOK%' and (trim(Settlement_Instruction.Account.Beneficiary_Account_Number) is not equal 'dummy' and trim(Settlement_Instruction.Account.Beneficiary_Account_Number) is not null) ) then '2' //5325 else '' end as DEP_REQ_IND Please notice: the word 'DUMMY' in *Settlement_Instruction.Account.**Beneficiary_Account_Number* is not case-sensitive. | null | |
| 23 | DEP_REQ_AR | Client area 1-Seoul | CHAR(2) | 5325 | case when (Cashflow.Payment_Currency in ('KRO','KRW') and Settlement_Instruction.Account.SCB_Nostro_Account_Number like '%UIBOK%' and ( trim(Settlement_Instruction.Account.Beneficiary_Account_Number) is not equal 'dummy' and trim(Settlement_Instruction.Account.Beneficiary_Account_Number) is not null) ) then '01' //5325 else '' end as DEP_REQ_AR,*/ Please notice: the word 'DUMMY' in *Settlement_Instruction.Account.**Beneficiary_Account_Number* is not case-sensitive. | null | |
| 24 | DEP_REQ_CMS | Client CMS account 2-N | CHAR(1) | 5325 | case when (Cashflow.Payment_Currency in ('KRO','KRW') and Settlement_Instruction.Account.SCB_Nostro_Account_Number like '%UIBOK%' and (trim(Settlement_Instruction.Account.Beneficiary_Account_Number) is not equal 'dummy' and trim(Settlement_Instruction.Account.Beneficiary_Account_Number) is not null) ) then '2' //5325 else '' end as DEP_REQ_CMS Please notice: the word 'DUMMY' in *Settlement_Instruction.Account.**Beneficiary_Account_Number* is not case-sensitive. | null | |
| 25 | COMMENTS | Comments | CHAR(100) not null | | Hardcode 'SCBK' | SCBK | |
| 26 | COMMENT_ENG | Comments_Eng | CHAR(100) | 5318, 5319 | Hardcode 'SCBK' ~~case~~ ~~ when t.UINO='5318' and t.CNO = 400077867 then to_char(t.DEALNO)~~ ~~ when t.UINO='5318' and t.CNO <> 400077867 and t.ACCOUNTTYPE <>'KR' then 'SCBK'~~ ~~ when t.UINO = '5319' then 'SCBK'~~ ~~ else ''~~ ~~end as COMMENT_ENG~~ | SCBK | |
| 27 | PAY_TM | When to pay 0-Immediate | CHAR(1) | 5325 | case when (Cashflow.Payment_Currency in ('KRO','KRW') and Settlement_Instruction.Account.SCB_Nostro_Account_Number like '%UIBOK%' and ( trim(Settlement_Instruction.Account.Beneficiary_Account_Number) is not equal 'dummy' and trim(Settlement_Instruction.Account.Beneficiary_Account_Number) is not null) ) then '0' //5325 else '' end as PAY_TM Please notice: the word 'DUMMY' in *Settlement_Instruction.Account.**Beneficiary_Account_Number* is not case-sensitive. | null | |
| 28 | DEP_INF_IND | BOK IRM | CHAR(2) not null | 5323, 5324, 5325 | Hardcoded 01 | 01 | |
| 29 | DEP_IDENTITY | BOK IRM | CHAR(10) not null | 5323, 5324, 5325 | Hardcoded 1028121843 | 1028121843 | |
| 30 | FEE_IND | Fee Classification 3- Exemption | CHAR(1) | 5323, 5324, 5325 | case when Settlement_Instruction.Account.Beneficiary_Bank_BIC_code = 'SCBLKRSEXXX' then '' //5318 5319 5338 5339 else '3' //5323 5324 5325 end as FEE_IND | null | |
| 31 | FEE_REASON | Fee reason | CHAR(2) | 5323, 5324, 5325 | case when Settlement_Instruction.Account.Beneficiary_Bank_BIC_code = 'SCBLKRSEXXX' then '' //5318 5319 5338 5339 else ( case when Cashflow.Payment_Currency in ('KRO','KRW') and Settlement_Instruction.Account.SCB_Nostro_Account_Number like '%UIBOK%' then '17' //5324 5325 else '11' end //5323) end as FEE_REASON | null | |
| 32 | PRINT_IND | Receipt Output 2-Unoutput | CHAR(1) | 5324, 5325 | case when Cashflow.Payment_Currency in ('KRO','KRW') and Settlement_Instruction.Account.SCB_Nostro_Account_Number like '%UIBOK%' then '2' //5324 5325 else ''end as PRINT_IND | null | |
| 33 | STAT | Status 0- Initial status 1 - TIS have got the data 3 - UI already got the data | CHAR(1) not null | ALL | Hardcoded '0' | 0 | |
| 34 | ACCOUNTTYPE | Counterparty country | CHAR(35) not null | ALL | trim(Entity.Counterparty_SCI_DOMICILE_COUNTRY) | GB | |
| ~~35~~ | ~~CCY_OLTP~~ | ~~No need~~ | | | ~~Hardcoded~~ | ~~ null~~ | |
| 36 | BENE_FULL_NAME | 59 Beneficiary Customer Full Name | VARCHAR() | 5338, 5339 | case when Settlement_Instruction.Account.Beneficiary_Account_Number like 'BR%' //5338, new 2 then Settlement_Instruction.Account.Beneficiary_Account_Name else '' end | SCB HK | |

# Field Mapping for (UIDD)

TIS Query Parameter

| Field Name | Optional/Mandatory | Description | Format | Sample |
| --- | --- | --- | --- | --- |
| settDate | M | User manually select from TIS | YYYY-MM-DD | 2026-04-25 |

Sample Response

**EXPAND: UIDD Sample response**

{
    "msg": "success",
    "data": {
        "columns": [
            "AUDITTIMESTAMP",
            "CASHFLOWNO",
            "UINO",
            "SN",
            "CCY",
            "AMOUNT",
            "ACCOUNTNUM",
            "ACCOUNTTYPE",
            "VALUEDATE",
            "PRODUCT",
            "PRODTYPE",
            "CNO",
            "NOPD_REASON",
        ],
        "rows": [
            {
                "AUDITTIMESTAMP": "2026-02-03 06:02:08.584",
                "CASHFLOWNO": "M00126049621",
                "UINO": "0201",
                "SN": "STANCHART BK LDN",
                "CCY": "KRW",
                "AMOUNT": "73892",
                "ACCOUNTNUM": "35185014878",
                "ACCOUNTTYPE": "KR",
                "VALUEDATE": "2026-01-22",
                "PRODUCT": "FXD",
                "TYPE": "FXD",
                "CNO": "10075222",
                "NOPD_REASON": "18-SI"
            }
        ]
        
    }
}

**EXPAND_END**

| | Field Name | Field Description | Format | Logic Model | Value Sample | Remarks |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | AUDITTIMESTAMP | Time when message generate | datetime not null | TO_CHAR(SYSTIMESTAMP, 'yyyy-mm-dd hh:mm:ss.ff3') AS AUDITTIMESTAMP | 2026-02-03 06:02:08.584 | |
| 2 | CASHFLOWNO | Cashflow Number | CHAR(12) not null | Cashflow.Cashflow_Id | M00126049621 | |
| 3 | UINO | Payment type in TIS | CHAR(4) not null | case when (Cashflow.Payment_Currency in ('KRO', 'KRW')) then '0201' else '3013' end | 0201 | |
| 4 | SN | Counterparty name | CHAR(35) not null | trim(Entity.Counterparty_SCI_FMCODE) | ECLHOLDSLD*LDN | |
| 5 | CCY | ISO currency | CHAR(3) not null | Cashflow.Payment_Currency | KRW | |
| 6 | AMOUNT | Payment amount | NUMBER(24,3) not null | trim(Cashflow.Payment_Amount) | 73892.01 | |
| 7 | ACCOUNTNUM | 59 Account number | CHAR(34) not null | trim(Settlement_Instruction.Account.Beneficiary_Account_Number) | 35185014878 | |
| 8 | ACCOUNTTYPE | Counterparty country | CHAR(35) not null | trim(Entity.Counterparty_SCI_DOMICILE_COUNTRY) | KR | |
| 9 | VALUEDATE | Payment value date | DATE not null | Cashflow.Payment_Date | 2026-01-22 | |
| 10 | PRODUCT | Product Group | CHAR(5) not null ->CHAR(20) | trim(Instrument_Common.Murex_Product_Group) | FXD | |
| 11 | PRODTYPE | Product Type | CHAR(20) not null ->CHAR(50) | trim(Instrument_Common.Murex_Product_Type) | FXD | |
| 12 | CNO | Counterparty FMID | CHAR(20) not null | trim(Entity.Counterparty_SCI_FMID) | 10075222 | |
| 13 | NOPD_REASON | Reason for no Pswd | CHAR(5) not null | Hardcode '18-SI' | 18-SI | |

Status Code

| Success | 200 | Indicates that the request succeeded and that the requested information is in the response. This is the most common status code to receive. |
| --- | --- | --- |
| NotFound | 404 | Indicates that the requested resource does not exist on the server. |
| BadRequest | 400 | Indicates that the mandatory parameter of request doesn't exist. Or the parameter format doesn't meet the requirement. |
| Unauthorized | 401 | Indicates that the token is invalid |
| InternalServerError | 500 | Indicates that an error has occurred in the service. |

# Static Data

| Entity Name | FMID | Country Code | Branch code |
| --- | --- | --- | --- |
| SCFB_SEOUL | 10036645 | KR | 70 |

| | Sett Means | Sett Account | Cashflow Status Post Cutoff | Payment Type | Currency | Payment Process | Accounting |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | NOS | CCY MAIN | Released/Settled | External Client | FCY | SWIFT into ENISIS | Accounting entry into OLTP |
| 2 | NOS | CCY KEBSEO | Released/Settled | External Client | FCY | SWIFT into ENISIS | Accounting entry into OLTP |
| 3 | NOS | CCY WRBSEO | Released/Settled | External Client | FCY | SWIFT into ENISIS | Accounting entry into OLTP |
| 4 | NOX | CCY UISUS | Released | Internal Movement, 1. credit funds to another branch account hold in SCBK 2. credit funds to client account hold in SCBK 3. Interbank Remittance Network | KRW & FCY | Ratan->TIS->UI(OLTP) | Accounting entry will not flow into OLTP |
| 5 | NOX | CCY UIBOK | Released | BOK-Wire | KRW | Ratan->TIS->UI(OLTP) | Accounting entry into OLTP |
| 6 | NOX | CCY UIDD | Released | Internal Movement, 1. debit funds to another branch account hold in SCBK 2. debit funds to client account hold in SCBK | KRW & FCY | Ratan->TIS->UI(OLTP) | Accounting entry will not flow into OLTP |
| 7 | NOX | KRO BOKSEO | Released | Client is Bank, through BOK wire | KRW | User will manually query in SSDR, then manually upload into OLTP | Accounting entry into OLTP |

# Reference

| Reference description | files |
| --- | --- |
| JSON sample file Razor sent to TIS | |
| API sql used in Razor | |
| More payment samples in TIS | |
| Daily manual payment report from Murex-KR | |

| Korea Seoul Entity |
| --- |
| SCFB_SEOUL |
| ~~SCSK_SEOUL~~ |
| ~~SEOUL~~ |

# Open Questions

| Number | Question | Answer | |
| --- | --- | --- | --- |
| 1 | Razor query frequency? Post TIS query, any further message TIS will send to Razor — TIS | Several times NO | Done. |
| 2 | If duplicate query, will refresh in TIS? | No. Key is trade id/ Cashflow id. | Done. |
| 3 | Please share settlement account is KRO UISUS/KRO UIBOK/CNH UISUS — TIS Nostro static | In progress | |
| 4 | Fields meaning. AMT_IND. PAYACCT_GLNO and so on, check in Field mapping table. ---TIS | | Done |
| 5 | should RATAN be 039? PAYACCT_BR ---TIS | 017 | Done |
| 6 | Vostro account move to SSI+ ---Balaji | In progress | |
| 7 | Which fields are mandatory for TIS ----TIS | Shared all page to Crystal. No concern.2026-04-08 Need to check with Crystal.2026-03-18 In Field mapping table | Done |
| 8 | If any respond from TIS after query. After respond, any status changed? – TIS Post TIS query the API, any status change in Razor? – Razor | No respond from TIS. No change in RATAN | Done |
| 9 | Any firewall/special procedure for Korea onboarding? — TIS, Tech | Yes need firewall. service IP, PORT, | Done |
| 10 | 59a account should be mandatory, but in 5324 scenario, this field need to be empty. could we have another solution? Such as input '0' to instead of empty? | We could setup by entering “dummy” in the account number field. | Done. |
| 11 | How to deal with reversal cashflows which generated by cancellation or withdraw? In Ratan, the cashflow ID will be same with the original cashflow. | Not in scope to TIS | Done |
| 12 | For 'Product Group' and 'Product Type', the length in TIS now are not enough. Need to increase them. Need to check more fields length. PRODUCT CHARACTER 6 TYPE CHARACTER 20 in [SABRE Stella - FMRP Product Catalogue - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/SABRE+Stella+-+FMRP+Product+Catalogue) For products, max length is 15. ForeignExchange Equity InterestRate Commodity Credit LoanIQ If the rest of 'ISDA' could take as 'TYPE', max length should be 46. Option:PriceReturnBasicPerformance:SingleIndex Could extend PRODUCT and TYPE length to 20 and 50? | Comment2026-03-23 | Done |
| | For payment which not in filter, even consider all payment type process for KOREA. | | Done |
| | If exist currency code 'KRO' ? or just need to justify 'KRW'? | Both will be used. 'KRO' already in RATAN DB, and 'KRW' is ISO currency. | Done. |
| | Check field Bene_Full_Name with Crystal and Ji, Hoon | | Done |
| | Field 'COMMENT_ENG' hardcode 'SCBK' | | Done |
| | How about add field 'NOPD_REASON' for direct-debit payment | | Done |
| | Exception scenarios for API query. When query success, send 'msg' with value 'success'. When query failed, as data not exist, or value date not exist, or errors occur in the service, send 'msg' with value 'failed' Please share request sample and status code. | | Done |
| | Please ensure if need password in request message. | | Done |
| | If word 'DUMMY' in 59Beneficiary_Account_Number case-sensitive? | No. | Done |