# Background

Instead of Murex-KR, RATAN will send real time accounting messages to OLTP. Cashflow scope is same with that flow into RATAN from Murex-KR.

![image-2026-3-18_8-59-38.png](attachments/image-2026-3-18_8-59-38.png)

![image-2026-2-25_14-35-49.png](attachments/image-2026-2-25_14-35-49.png)

# Business Scenarios

| | Cashflow event | Accounting behavior |
| --- | --- | --- |
| 1 | For cashflow with new action | If SCB pay, increase on Bridge account, decrease on Nostro account If SCB receive, increase on Nostro account, decrease on Bridge account |
| 2 | For cashflow with withdrawal | If SCB pay, decrease on Bridge account, increase on Nostro account If SCB receive, increase on Bridge account, decrease on Nostro account |
| 3 | SWIFT_SUPPRESS/FAILED | |

# Accounting Status

| **Accounting Status in RATAN** | **Account Status Reason** | **Comment** | **Action to fix the failure** |
| --- | --- | --- | --- |
| HOLD | | Accounting entry generated but not reaching VD yet, so holding the posting | Not Required |
| DISABLED | | Accounting entry generated for Sett Means = 'NOX' and Sett Account in ('CCY UISUS', 'CCY UIDD'), but not sent to OLTP. So disable it. | Not Required |
| SENT | | Accounting entry generated and sent to OLTP but didn't receive response from OLTP yet. | Not Required |
| SUCCESS | | OLTP consume the accounting entry successfully and return the ACK | Not Required |
| REJECTED | OLTP Error Code | OLTP can't consume the accounting entry and response with error code. | Not Required |
| MISSING_INFO | | It's for the SWIFT_SUPPRESSED case when the Nostro is not available, Ratan won't generate the accounting entry Or if any mandatory field value is missing. | Not Required |

# Filter for OLTP

Cashflow status scope: Failed/Swift_suppressed/Released/Settled

If match below condition, accounting need send to OLTP.

1. Sett Means = 'NOS'
2. Sett Means = 'NOX' and Sett Account in ('KRO UIBOK', 'KRO BOKSEO')

| | Sett Means | Sett Account | Cashflow Status Post Cutoff | Payment Type | Currency | Payment Process | Accounting |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | NOS | CCY MAIN(CCY means currency) | Released/Settled | External Client | FCY(foreign currency) | SWIFT into ENISIS | Accounting entry into OLTP |
| 2 | NOS | CCY KEBSEO(CCY means currency) | Released/Settled | External Client | FCY(foreign currency) | SWIFT into ENISIS | Accounting entry into OLTP |
| 3 | NOS | CCY WRBSEO(CCY means currency) | Released/Settled | External Client | FCY(foreign currency) | SWIFT into ENISIS | Accounting entry into OLTP |
| 4 | NOX | CCY UISUS(CCY means currency) | Released | Internal Movement, 1. credit funds to another branch account hold in SCBK 2. credit funds to client account hold in SCBK 3. Interbank Remittance Network | KRW & FCY(foreign currency) | Ratan->TIS->UI(OLTP) | Accounting entry will not flow into OLTP |
| 5 | NOX | KRO UIBOK | Released | BOK-Wire | KRW | Ratan->TIS->UI(OLTP) | Accounting entry into OLTP |
| 6 | NOX | CCY UIDD(CCY means currency) | Released | Internal Movement, 1. debit funds to another branch account hold in SCBK 2. debit funds to client account hold in SCBK | KRW & FCY(foreign currency) | Ratan->TIS->UI(OLTP) | Accounting entry will not flow into OLTP |
| 7 | NOX | KRO BOKSEO | Released | Client is Bank, through BOK wire | KRW | User will manually query in SSDR, then manually upload into OLTP | Accounting entry into OLTP |

Please note: the filter logic in code is black list.  Only NOX(UIDD,UISUS) can't to OLTP, others can send to OLTP. If add new account which can't send accounting to OLTP in the future, RATAN need code change.

# Fields Mapping

In 'TRANDATA' tag

| | Field name | Field name in Murex report | Format | Sample value | Description | Logical model | Ratan Source xpath/json path/DB column |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | AIGRILJA | Date | NUMBER(8) | 20251107 | Same with value date | Cashflow.Payment_Date | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentDate/conf:unadjustedDate |
| 2 | AIREFNO | Reference Number | CHAR(16) | M000054313360101 | Mandatory length 16: Cashflow_ID (12) + Business version(2)+ Minor version (2) | Cashflow.Cashflow_ID (12) Business version(2)Minor version (2) | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:header/scb:cashflowIdentifier/scb:cashflowId[@cashflowIdScheme="[http://www.sc.com/coding-scheme/cashflowId](http://www.sc.com/coding-scheme/cashflowId)"] |
| 3 | AIGJJRSU | Number of iterations | NUMBER(2) | 02 | Hardcode 02 | | |
| 4 | AIGJ | | | | | | |
| 5 | AIBRNO(1) AIBRNO(2) | Bank GL Code | NUMBER(3) | 017 | Branch code 017 Hardcode | | |
| 6 | AICODE(1) AICODE(2) | Bank Account Code | NUMBER(6) | 000259 | AICODE(1): Bank Account Code(Column E in original OLTP report) Bridge account(Suspend account) KRW:000287 NO-KRW:040446 --------------------- AICODE(2): Bank Account Code(Column L in original OLTP report) Nostro Account. ~~if nostro account is 0, then if currency is "KRW" or "KRO"(Currency code:999) then 000261;~~ ~~else 043151~~ | AICODE(1): KRW:000287 NO-KRW:040446 AICODE(2): settlement_Instruction.account.EBBS_Account_Number ![image-2026-5-19_11-18-15.png](attachments/image-2026-5-19_11-18-15.png) | |
| 7 | AISECD(1) AISECD(2) | Default 00 | NUMBER(2) | 00 | Hardcode 00 | | |
| 8 | AITONG(1) AITONG(2) | Currency Code | CHAR(3) | USD | ISO currency | Cashflow.Payment_Currency | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentAmount/conf:currency[@currencyScheme="[http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15](http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15)"] |
| 9 | AIIPJI(1) AIIPJI(2) | Credit/Debit Indicator | CHAR(2) | 10 | “10” for “Debit”(pay) and “30” for “Credit”(receive) | AIIPJI(1) --Bridge account(Suspend account) logic: Get payer reference Cashflow.Payment_Payer_Party_Reference from cashflow if Cashflow.Payment_Payer_Party_Reference == party1 ~~and Cashflow.Cashflow_Event_Type==New~~ then return '10' else return '30' AIIPJI(2) – Nostro account is opposite direction of AIIPJI(1). When cashflow direction is 'PAY', (Bridge)AIIPJI(1) is '10', (Nostro)AIIPJI(2) is '30' When cashflow direction is 'RECEIVE', (Bridge)AIIPJI(1) is '30', (Nostro)AIIPJI(2) is '10' | |
| 10 | AIAMT(1) AIAMT(2) | Foreign Amount | NUMBER(15,2) Refer below table** Format for field 'AIAMT' and 'AIRCAMT'** | 15501370.00 | Payment_Amount | Cashflow.Payment_Amount | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentAmount/conf:amount |
| 11 | AIGUBN(1) AIGUBN(2) | Domestic Amount | CHAR(1) | N | Hardcode 'N' | | |
| 12 | AIRCJRSU | | NUMBER(2) | 01 | Hardcode '01' | | |
| 13 | AIRC | | | | | | |
| 14 | AIRCTYPE | Recon. Type | CHAR(1) | 1 | Hardcode '1' | | |
| 15 | AIRCBIC | BIC Bank code | CHAR(11) | BOKRKRSExxx | Nostro correspondent BIC | settlement_Instruction.account.booking_Entity_Correspondent_BIC_code Then process BIC as below logic | Scenarios | Original BIC | Target BIC | | | --- | --- | --- | --- | | SCBLGB2LTSY | SCBLGB2LTSY | SCBLGB2Lxxx | 'xxx' means 3 spaces | | BIC with 8 chars | SCBLIDJX | SCBLIDJXxxx | 'xxx' means 3 spaces | | BIC with 11 chars and the last 3 chars are 'XXX' | SCBLEGCAXXX | SCBLEGCAxxx | 'xxx' means 3 spaces | | BIC with 11 chars and the last 3 chars are not 'XXX' | SCBLCNSXSHA | SCBLCNSXSHA | | | |
| Scenarios | Original BIC | Target BIC | |
| SCBLGB2LTSY | SCBLGB2LTSY | SCBLGB2Lxxx | 'xxx' means 3 spaces |
| BIC with 8 chars | SCBLIDJX | SCBLIDJXxxx | 'xxx' means 3 spaces |
| BIC with 11 chars and the last 3 chars are 'XXX' | SCBLEGCAXXX | SCBLEGCAxxx | 'xxx' means 3 spaces |
| BIC with 11 chars and the last 3 chars are not 'XXX' | SCBLCNSXSHA | SCBLCNSXSHA | |
| 16 | AIRCTONG | Currency Code | CHAR(3) | USD | ISO currency | Cashflow.Payment_Currency | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentAmount/conf:currency[@currencyScheme="[http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15](http://www.fpml.org/coding-scheme/external/iso4217-2001-08-15)"] |
| 17 | AIRCIPJI | Credit/Debit | CHAR(1) | 2 | Recon pay/receive direction same with bridge direction | “1” for Credit (receive) “2” for Debit(pay) | |
| 18 | AIRCDATE | Reconcile Date | NUMBER(8) | 20251107 | Same with value date | Cashflow.Payment_Date | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentDate/conf:unadjustedDate |
| 19 | AIRCAMT | Reconcile Amount | NUMBER(15,2) Refer below table** Format for field 'AIAMT' and 'AIRCAMT'** | 15501370.00 | Payment_Amount | Cashflow.Payment_Amount | /scb:SCBML/scb:payload/scb:cashflowPayload/scb:cashflow/scb:payment/conf:paymentAmount/conf:amount |
| 20 | AIRCREF | Ref. No for Reconfile | CHAR(16) | DV70M00125825123 | "DV70"+Cashflow ID(12) | "DV70"+Cashflow_ID | |
| 21 | AIRCGBN | Correction Indicator | CHAR(1) | NULL | Hardcode NULL | | |

**Format for field 'AIAMT' and 'AIRCAMT'**

| | Amount in RATAN | Send to OLTP | Comments |
| --- | --- | --- | --- |
| 3 decimals | 1.236 | 1.24 | Rounding |
| 2 decimals | 1.23 | 1.23 | |
| 1 decimal | 1.2 | 1.20 | Add '0' to make up 2 decimals |
| 0 decimal | 12345 | 12345.00 | Add '.00' to make up 2 decimals |
| More than 15digit | 12345678901234.56 | 12345678901234.56 | Nack message (“TXN00060”) is returned |

# Accounting Entry JSON template for New.

Note: all fields marked as 'hardcord ' could be hardcoded as sample value.

{
    "SCBML": {
        "ns:header": {
            "ns:messageDetails": {
                "ns:messageVersion": "1.0", //hardcord
                "ns:messageType": {
                    "ns:typeName": "CoreBanking:ratanCommonRoute" //hardcord
                }
            },
            "ns:originationDetails": {
                "ns:messageSender": {
                    "ns:messageSender": {
                        "*body": "RATAN" //hardcord
                    },
                    "ns:senderDomain": {
                        "ns:domainName": {
                            "*body": "CoreBanking" //hardcord
                        }
                    },
                    "ns:countryCode": "KR" //hardcord
                },
                "ns:initiatedTimestamp": "2026-04-08T02:28:35.563+00:00", //Timestamp Ratan send the message in GMT yyyy-MM-dd'T'HH:mm:ssXXX  
                "ns:trackingId": "M0000123456.1.7" //RATAN side External Key
            },
            "ns:captureSystem": "OLTP" //hardcord
        },
        "payload": {
            "ns:payloadFormat": "json", //hardcord
            "ns:payloadVersion": "1.0", //hardcord
            "scbmlPayload": {
                "REQUESTMESSAGE": {
                    "SYSTEMHEADER": {
                        "TMSG_WRTG_DT": "20260408", //RATAN side    GMT   YYYYMMDD
                        "TMSG_WRTG_TM": "111149", //RATAN side    GMT      HHMMSS
                        "TRSC_GRCO_CD": "01", //hardcord
                        "TMSG_CRE_SYS_NM": null, //hardcord
                        "ISS_SRL_NO": "", //hardcord
                        "IPV6_ADR": "10.61.17.205", //hardcord
                        "INPT_DLV_CD": "T", //hardcord
                        "ENVR_INFO_DV_CD": "D", //hardcord
                        "RQST_RSPS_DV_CD": "Q", //hardcord
                        "TRSC_SYNC_DV_CD": "S", //hardcord
                        "TRAN_CD": "CB_RAT_OLTP_001", //hardcord
                        "TMSG_RSPS_DTM": "",//hardcord
                        "PROC_RSLT_DV_CD": "",//hardcord
                        "CHNL_TYP_CD": "RAT",//hardcord
                        "MCI_ND_NO": "",//hardcord
                        "MCI_SESS_ID_NO": ""//hardcord
                    },
                    "TRANCOMMONHEADER": {
                        "TMSG_MSG_TYP_CD": "1",//hardcord
                        "BLNG_GRCO_CD": "01",//hardcord
                        "BLNG_BR_NO": "0998",//hardcord
                        "EMP_NO": null,//hardcord
                        "OFLV_CD": null,//hardcord
                        "OFDY_CD": null,//hardcord
                        "EMP_CD_NO": null,//hardcord
                        "TXN_BR_NO": "0998",//hardcord
                        "APV_CD": null, //hardcord
                        "APV_BRNCD_1": null,//hardcord
                        "APV_EMP_NO_1": null,//hardcord
                        "APV_PASSWD_1": null,//hardcord
                        "APV_BRNCD_2": null,//hardcord
                        "APV_EMP_NO_2": null,//hardcord
                        "APV_PASSWD_2": null,//hardcord
                        "APV_BRNCD_3": null,//hardcord
                        "APV_EMP_NO_3": null,//hardcord
                        "APV_PASSWD_3": null,//hardcord
                        "SCRN_ID": null,//hardcord
                        "SUB_SCRN_ID": null,//hardcord
                        "SIMUL_CD": null,//hardcord
                        "PSBK_PRTR_CONN_DV_CD": "0",//hardcord
                        "PSBK_DV_CD": "0",//hardcord
                        "PSBK_MS_VAL": null,//hardcord
                        "PSBK_COVER_PAGE": null,//hardcord
                        "OUTPUT_LINE_VAL": "0",//hardcord
                        "CRD_DV_CD": null,//hardcord
                        "CRD_MDCL_DV_CD": null,//hardcord
                        "PAPER_DV_CD": null,//hardcord
                        "FUTURE_TRAN_KEY": null,//hardcord
                        "CANCEL_KEY": null,//hardcord
                        "PREV_DAY_KEY": null,//hardcord
                        "PAST_DATE_KEY": null,//hardcord
                        "PRINT_CONT_START": null,//hardcord
                        "PRINT_CONT": null,//hardcord
                        "MPGB": null,//hardcord
                        "TRXCD": "TI1FBS02", //hardcord
                        "BIZDISTCD": "89",//hardcord
                        "INPUTDISTCD": "G002",//hardcord
                        "INPUTDISTCD_CANCEL": null,//hardcord
                        "CHANNELID": "T",//hardcord
                        "OLDACCTCD": "89",//hardcord
                        "MACRO_AI": "AIYJM60",//hardcord
                        "MACRO_AO": "AOYJM60",//hardcord
                        "SERVERMSG": null //hardcord
                    },
                    "TRANDATA": {
                        "AIGRILJA": "20260408", //RATAN side 
                        "AIREFNO": "M000054313360101", //RATAN side
                        "AIGJJRSU": "02",//RATAN side
                        "AIGJ": [
                            {
                                "AIBRNO": "017",//RATAN side
                                "AICODE": "043150",//RATAN side
                                "AISECD": "00",//RATAN side
                                "AITONG": "USD",//RATAN side
                                "AIIPJI": "10",//RATAN side
                                "AIAMT": "235102.23",//RATAN side
                                "AIGUBN": "N"//RATAN side
                            },
                            {
                                "AIBRNO": "017",//RATAN side
                                "AICODE": "040320",//RATAN side
                                "AISECD": "00",//RATAN side
                                "AITONG": "USD",//RATAN side
                                "AIIPJI": "30",//RATAN side
                                "AIAMT": "235102.23",//RATAN side
                                "AIGUBN":"N"//RATAN side
                            }
                        ]
                        "AIRCJRSU": "01",//RATAN side
                        "AIRC": [
                            {
                                "AIRCTYPE": "1",//RATAN side
                                "AIRCBIC": "KOEXKRSE   ",//RATAN side
                                "AIRCTONG":"USD",//RATAN side
                                "AIRCIPJI": "2",//RATAN side
                                "AIRCDATE": "20260408",//RATAN side
                                "AIRCAMT": "235102.23",//RATAN side
                                "AIRCREF": "MX000000000000C",//RATAN side
                                "AIRCGBN": null//RATAN side
                            }
                        ]
                    }
                }
            }
        }
    }
}

# ACK/NACK JSON template for New.

Key part in 'TRANDATA'

**EXPAND: Entire success respond message**

{                        
    "SCBML": {                        
        "ns:header": {                        
            "ns:messageDetails": {                        
                "ns:messageVersion": "1.0", //hardcord                         
                "ns:messageType": {                        
                    "ns:typeName": "CoreBanking:ratanCommonRoute"     //hardcord                    
                }                        
            },                        
            "ns:originationDetails": {                        
                "ns:messageSender": {                        
                    "ns:messageSender": {                        
                        "*body": "RATAN"    //hardcord                      
                    },                        
                    "ns:senderDomain": {                        
                        "ns:domainName": {                        
                            "*body": "CoreBanking"  //hardcord                       
                        }                        
                    },                        
                    "ns:countryCode": "KR"     //hardcord                    
                },                        
                "ns:initiatedTimestamp": "2025-11-28T02:28:35.563+00:00"                         
                "ns:trackingId": "M0000123456.1.7" //same value as request
            },                        
            "ns:captureSystem": "OLTP"       //hardcord                  
        },                        
        "payload": {                        
            "ns:payloadFormat": "json",      //hardcord                   
            "ns:payloadVersion": "1.0",      //hardcord                  
            "scbmlPayload": {                        
                "REQUESTMESSAGE": {                        
                    "SYSTEMHEADER": {                        
                        "TMSG_WRTG_DT": "20251128",       //RATAN side                  
                        "TMSG_WRTG_TM": "111149",          //RATAN side               
                        "TRSC_GRCO_CD": "01",        //hardcord                 
                        "TMSG_CRE_SYS_NM":  null,    //hardcord                    
                        "ISS_SRL_NO": "",               //hardcord          
                        "IPV6_ADR": "10.61.17.205", //hardcord                      
                        "INPT_DLV_CD": "T",       //hardcord                  
                        "ENVR_INFO_DV_CD": "D",     //hardcord                    
                        "RQST_RSPS_DV_CD": "Q",      //hardcord                   
                        "TRSC_SYNC_DV_CD": "S",      //hardcord                   
                        "TRAN_CD": "CB_RAT_OLTP_001",   //hardcord                      
                        "TMSG_RSPS_DTM": "",      //hardcord                    
                        "PROC_RSLT_DV_CD": "",    //hardcord                      
                        "CHNL_TYP_CD": "RAT",     //hardcord                     
                        "MCI_ND_NO": "",          //hardcord                
                        "MCI_SESS_ID_NO": ""       //hardcord                   
                    },                        
                    "TRANCOMMONHEADER": {                        
                        "TMSG_MSG_TYP_CD" : "1", //hardcord
                        "BLNG_GRCO_CD" : "01",   //hardcord
                        "BLNG_BR_NO" : "0998",   //hardcord
                        "EMP_NO" : null,         //hardcord
                        "OFLV_CD" : null,        //hardcord
                        "OFDY_CD" : null,        //hardcord
                        "EMP_CD_NO" : null,      //hardcord
                        "TXN_BR_NO" : "0998",    //hardcord
                        "APV_CD" : null,         //hardcord
                        "APV_BRNCD_1" : null,    //hardcord
                        "APV_EMP_NO_1" : null,    //hardcord
                        "APV_PASSWD_1" : null,   //hardcord
                        "APV_BRNCD_2" : null,    //hardcord
                        "APV_EMP_NO_2" : null,   //hardcord
                        "APV_PASSWD_2" : null,   //hardcord
                        "APV_BRNCD_3" : null,    //hardcord
                        "APV_EMP_NO_3" : null,    //hardcord
                        "APV_PASSWD_3" : null,    //hardcord
                        "SCRN_ID" : null,         //hardcord
                        "SUB_SCRN_ID" : null,     //hardcord
                        "SIMUL_CD" : null,        //hardcord
                        "PSBK_PRTR_CONN_DV_CD" : "0",  //hardcord
                        "PSBK_DV_CD" : "0",        //hardcord
                        "PSBK_MS_VAL" : null,       //hardcord
                        "PSBK_COVER_PAGE" : null,   //hardcord
                        "OUTPUT_LINE_VAL" : "0",  //hardcord
                        "CRD_DV_CD" : null,  //hardcord
                        "CRD_MDCL_DV_CD" : null,  //hardcord
                        "PAPER_DV_CD" : null,  //hardcord
                        "FUTURE_TRAN_KEY" : null,  //hardcord
                        "CANCEL_KEY" : null,  //hardcord
                        "PREV_DAY_KEY" : null,  //hardcord
                        "PAST_DATE_KEY" : null,  //hardcord
                        "PRINT_CONT_START" : null, //hardcord
                        "PRINT_CONT" : null, //hardcord
                        "MPGB" : null, //hardcord
                        "TRXCD" : "TI1FBS02", //hardcord
                        "BIZDISTCD" : "89", //hardcord
                        "INPUTDISTCD" : "G002", //hardcord
                        "INPUTDISTCD_CANCEL" : null,//hardcord 
                        "CHANNELID" : "T", //hardcord
                        "OLDACCTCD" : "89", //hardcord
                        "MACRO_AI" : "AIYJM60", //hardcord
                        "MACRO_AO" : "AOYJM60", //hardcord
                        "SERVERMSG" : null //hardcord
                    },                        
                    "CUSTOMINFO": null,             
                    "CONTTRAN": null,                     
                       "TRANDATA": {                    
                           "AOERRCD" : "0000",
                           "AOERWICH" : "",
                           "AOOUTNY1" : "",
                           "AOACK":"ACK",  
                           "AOEERR":"TXN00000”,   
                           "AOEMSG":"SUCCESS" 
                          }        
                    }                        
                }                        
            }                        
        }                        
    }                        
}

**EXPAND_END**

**EXPAND: Entire failure message**

{                        
    "SCBML": {                        
        "ns:header": {                        
            "ns:messageDetails": {                        
                "ns:messageVersion": "1.0", //hardcord                         
                "ns:messageType": {                        
                    "ns:typeName": "CoreBanking:ratanCommonRoute"     //hardcord                    
                }                        
            },                        
            "ns:originationDetails": {                        
                "ns:messageSender": {                        
                    "ns:messageSender": {                        
                        "*body": "RATAN"    //hardcord                      
                    },                        
                    "ns:senderDomain": {                        
                        "ns:domainName": {                        
                            "*body": "CoreBanking"  //hardcord                       
                        }                        
                    },                        
                    "ns:countryCode": "KR"     //hardcord                    
                },                        
                "ns:initiatedTimestamp": "2025-11-28T02:28:35.563+00:00"                         
                "ns:trackingId": "M0000123456.01.07" //same value as request
            },                        
            "ns:captureSystem": "OLTP"       //hardcord                  
        },                        
        "payload": {                        
            "ns:payloadFormat": "json",      //hardcord                   
            "ns:payloadVersion": "1.0",      //hardcord                  
            "scbmlPayload": {                        
                "REQUESTMESSAGE": {                        
                    "SYSTEMHEADER": {                        
                        "TMSG_WRTG_DT": "20251128",       //RATAN side                  
                        "TMSG_WRTG_TM": "111149",          //RATAN side               
                        "TRSC_GRCO_CD": "01",        //hardcord                 
                        "TMSG_CRE_SYS_NM":  null,    //hardcord                    
                        "ISS_SRL_NO": "",               //hardcord          
                        "IPV6_ADR": "10.61.17.205", //hardcord                      
                        "INPT_DLV_CD": "T",       //hardcord                  
                        "ENVR_INFO_DV_CD": "D",     //hardcord                    
                        "RQST_RSPS_DV_CD": "Q",      //hardcord                   
                        "TRSC_SYNC_DV_CD": "S",      //hardcord                   
                        "TRAN_CD": "CB_RAT_OLTP_001",   //hardcord                      
                        "TMSG_RSPS_DTM": "",      //hardcord                    
                        "PROC_RSLT_DV_CD": "",    //hardcord                      
                        "CHNL_TYP_CD": "RAT",     //hardcord                     
                        "MCI_ND_NO": "",          //hardcord                
                        "MCI_SESS_ID_NO": ""       //hardcord                   
                    },                        
                    "TRANCOMMONHEADER": {                        
                        "TMSG_MSG_TYP_CD" : "1", //hardcord
                        "BLNG_GRCO_CD" : "01",   //hardcord
                        "BLNG_BR_NO" : "0998",   //hardcord
                        "EMP_NO" : null,         //hardcord
                        "OFLV_CD" : null,        //hardcord
                        "OFDY_CD" : null,        //hardcord
                        "EMP_CD_NO" : null,      //hardcord
                        "TXN_BR_NO" : "0998",    //hardcord
                        "APV_CD" : null,         //hardcord
                        "APV_BRNCD_1" : null,    //hardcord
                        "APV_EMP_NO_1" : null,    //hardcord
                        "APV_PASSWD_1" : null,   //hardcord
                        "APV_BRNCD_2" : null,    //hardcord
                        "APV_EMP_NO_2" : null,   //hardcord
                        "APV_PASSWD_2" : null,   //hardcord
                        "APV_BRNCD_3" : null,    //hardcord
                        "APV_EMP_NO_3" : null,    //hardcord
                        "APV_PASSWD_3" : null,    //hardcord
                        "SCRN_ID" : null,         //hardcord
                        "SUB_SCRN_ID" : null,     //hardcord
                        "SIMUL_CD" : null,        //hardcord
                        "PSBK_PRTR_CONN_DV_CD" : "0",  //hardcord
                        "PSBK_DV_CD" : "0",        //hardcord
                        "PSBK_MS_VAL" : null,       //hardcord
                        "PSBK_COVER_PAGE" : null,   //hardcord
                        "OUTPUT_LINE_VAL" : "0",  //hardcord
                        "CRD_DV_CD" : null,  //hardcord
                        "CRD_MDCL_DV_CD" : null,  //hardcord
                        "PAPER_DV_CD" : null,  //hardcord
                        "FUTURE_TRAN_KEY" : null,  //hardcord
                        "CANCEL_KEY" : null,  //hardcord
                        "PREV_DAY_KEY" : null,  //hardcord
                        "PAST_DATE_KEY" : null,  //hardcord
                        "PRINT_CONT_START" : null, //hardcord
                        "PRINT_CONT" : null, //hardcord
                        "MPGB" : null, //hardcord
                        "TRXCD" : "TI1FBS02", //hardcord
                        "BIZDISTCD" : "89", //hardcord
                        "INPUTDISTCD" : "G002", //hardcord
                        "INPUTDISTCD_CANCEL" : null,//hardcord 
                        "CHANNELID" : "T, //hardcord
                        "OLDACCTCD" : "89", //hardcord
                        "MACRO_AI" : "AIYJM60", //hardcord
                        "MACRO_AO" : "AOYJM60", //hardcord
                        "SERVERMSG" : null //hardcord
                    },                        
                    "CUSTOMINFO": null,             
                    "CONTTRAN": null,                     
                       "TRANDATA": {                    
                             "AOERRCD" : "0000",
                             "AOERWICH" : "",
                             "AOOUTNY1" : "",
                             "AOACK" : "NACK", //"NACK"
                             "AOEERR" : "TXN00002", //"TXN00001"
                             "AOEMSG" :"Transaction date must be today & the previous business day"     
                        }        
                    }                        
                }                        
            }                        
        }                        
    }                        
}

**EXPAND_END**

# SOLACE Header From Ratan to OLTP

| 1 | Type | Mandatory or Not? | Field | Ratan Accounting | OLTP Response | OLTP logic | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | JMS Header | M | X-Outbound-Property-mxDocID | M01775024570.0.3 | M01775024570.0.3 | Same with Request | Can be used by OLTP |
| 2 | JMS Header | M | X-Outbound-Property-messageType | Settlement | Settlement | Same with Request | Can be used by OLTP |
| 3 | JMS Header | M | X-Outbound-Property-trackingId | M01775024570.0.3 | M01775024570.0.3 | Same with Request | Can be used by OLTP |
| 4 | JMS Header | M | X-Outbound-Property-sender | RatanOne | RatanOne | Same with Request | Can be used by OLTP |
| 5 | JMS Header | O | X-Outbound-Property-targetSystem | OLTP | RATAN | Can be empty | Can be used by OLTP |
| 6 | JMS Header | O | X-Outbound-Property-OPICSBranch | 45 | 45 | Can be empty | Can be used by OLTP |
| 7 | JMS Header | O | X-Outbound-Property-bookingSystem | RATAN | OLTP | Can be empty | Can be used by OLTP |
| 8 | JMS Header | M | imsCorrelationId | M00AER010001 | M00AER010001 | Same with Request | Used by IMS |
| 9 | JMS Header | M | imsEvent | SENT | RECEIVED | Hardcode | Used by IMS |
| 10 | JMS Header | M | imsTimestamp | 1775113029668 | 1775113090000 | To be Updated by ENISIS as system time | Used by IMS |
| 11 | JMS Header | M | imsTraceId | a3fe87d8-fbaf-4667-bd9c-0eacf113a01b | a3fe87d8-fbaf-4667-bd9c-0eacf113a01b | Same with Request | Used by IMS |
| 12 | JMS Header | M | imsPreviousCorrelationId | M00AER010001 | M00AER010001 | Same with Request | Used by IMS |
| 13 | JMS Header | M | imsSpans | RATAN | RATAN,OLTP | Hardcode | Used by IMS |
| 14 | JMS Header | M | trackingId | M01775024570.0.3 | Not applicable for Ratan To be aligned between OLTP/KR EDMi/FM SOLACE | Not applicable | Mandatory for SOLACE |
| 15 | JMS Header | M | sender | RATAN | Not applicable for Ratan To be aligned between OLTP/KR EDMi/FM SOLACE | Not applicable | Mandatory for SOLACE |
| 16 | JMS Header | M | domainName | FM | Not applicable for Ratan To be aligned between OLTP/KR EDMi/FM SOLACE | Not applicable | Mandatory for SOLACE |
| 17 | JMS Header | M | initiatedTimestamp | 1775113029668 | Not applicable for Ratan To be aligned between OLTP/KR EDMi/FM SOLACE | Not applicable | Mandatory for SOLACE |
| 18 | JMS Header | M | countryCode | KR | Not applicable for Ratan To be aligned between OLTP/KR EDMi/FM SOLACE | Not applicable | Mandatory for SOLACE |

# Error code:

| ERROR TYPES | ERRORCODE | DESCRIPTION |
| --- | --- | --- |
| | VARCHAR(10) | VARCHAR(100) |
| Transaction posting (Multi_Leg - Posting type) | TXN00000 | |
| TXN00001 | Transaction date must be in numeric format |
| TXN00002 | Transaction date must be today & the previous business day |
| TXN00003 | Must be a valid Reference no. |
| TXN00004 | Number of iterations must be in numeric format |
| TXN00005 | Number of iterations must be the hardcoded value "2" |
| TXN00006 | Number fields(digit) in the first array of AIGJ must be numeric format |
| TXN00007 | Numeric data error in the second account information |
| TXN00008 | AIBRNO(1) field value error in the first array of AIGJ |
| TXN00009 | AICODE(1) field value error of the first array of AIGJ |
| TXN00010 | AITONG(1) field value error of the first array of AIGJ |
| TXN00011 | AIIPJI(1) field value error of the first array of AIGJ |
| TXN00012 | AIAMT(1) field value error of the first array of AIGJ |
| TXN00013 | AIGUBN(1) field value error of the first array of AIGJ |
| TXN00014 | AIBRNO(2) field value error in the first array of AIGJ |
| TXN00015 | AICODE(2) field value error of the first array of AIGJ |
| TXN00016 | AITONG(2) field value error of the first array of AIGJ |
| TXN00017 | AIIPJI(2) field value error of the first array of AIGJ |
| TXN00018 | AIAMT(2) field value error of the first array of AIGJ |
| TXN00019 | AIGUBN(2) field value error of the first array of AIGJ |
| TXN00020 | Number of iterations must be in numeric format |
| TXN00021 | Error if the array count exceeds two |
| TXN00022 | Number fields(digit) in the first array of AIRC must be numeric format |
| TXN00023 | AIRCTYPE(1) field value error of the first array of AIRC |
| TXN00024 | AIRCBIC(1) field value error of the first array of AIRC |
| TXN00025 | AIRCIPJI(1) field value error of the first array of AIRC |
| TXN00026 | AIRCDATE(1) field value error of the first array of AIRC |
| TXN00027 | AIRCAMT(1) field value error of the first array of AIRC |
| TXN00028 | AIRCREF(1) field value error of the first array of AIRC |
| TXN00029 | AIRCGBN(1) field value is "null" |
| TXN00030 | CCY code unmatch betwwen AITONG(1) and AIRCTONG(1) |
| TXN00031 | Error if this condition is not met |
| TXN00032 | Number fields(digit) in the second array of AIRC must be numeric format |
| TXN00033 | AIRCTYPE(2) field value error of the second array of AIRC |
| TXN00034 | AIRCBIC(2) field value error of the second array of AIRC |
| TXN00035 | AIRCIPJI(2) field value error of the second array of AIRC |
| TXN00036 | AIRCDATE(2) field value error of the second array of AIRC |
| TXN00037 | AIRCAMT(2) field value error of the second array of AIRC |
| TXN00038 | AIRCREF(2) field value error of the second array of AIRC |
| TXN00039 | AIRCGBN(2) field value is "null" |
| TXN00040 | CCY code unmatch betwwen AITONG(2) and AIRCTONG(2) |
| TXN00041 | AIBRNO field value error |
| TXN00042 | OLTP Mapping error of AITON field value |
| TXN00043 | AICODE field value error |
| TXN00044 | SECD value provided but not maintained in OLTP account code table |
| TXN00045 | SECD value mismatch between OLTP account code table and message |
| TXN00046 | AITONG field is KRW, AICODE is a foreign ccy account |
| TXN00047 | AITONG field is the foreign CCY, AICODE is a KRW account |
| TXN00048 | Exchange rate not registered in OLTP |
| TXN00049 | Error during OLTP internal program(GTQUOTE) processing |
| TXN00050 | BIC code conversion error in OLTP |
| TXN00051 | Error during OLTP account processing program(GFGSEDT) |
| TXN00052 | DB setting error during OLTP account processing |
| TXN00053 | Transaction date must be a business day (Based on Korean business days) |
| TXN00054 | CCY code unmatch betwwen AITONG(1) and AITONG(2) |
| TXN00055 | Amount unmatch betwwen AIAMT(1) and AIRCAMT(1) |
| TXN00056 | Amount unmatch betwwen AIAMT(2) and AIRCAMT(2) |
| TXN00057 | Amount unmatch betwwen AIAMT(1) and AIAMT(2) |
| TXN00058 | CCY code must be in character format |
| TXN00059 | CCY code mapping error |
| TXN00060 | AIAMT(1) must include a decimal point before the last two digits |
| TXN00061 | AIAMT(2) must include a decimal point before the last two digits |
| TXN00062 | AIRCAMT(1) must include a decimal point before the last two digits |
| TXN00063 | AIRCAMT(2) must include a decimal point before the last two digits |

TXN00042 ----TXN00052 & TXN00059 are for OLTP error.

# OLTP EOD Exception

During OLTP EOD cutoff timings (11:30 PM KST - 12:30 AM KST), cashflow will be STPed directly or settlement ops manually release during EOD timing, which would be rare case, considering accounting entry will only be sent on VD real time and release cutoff are all configured as on VD 10:30 AM KST, The OLTP EOD Break will be treated as an exception scenario and handled manually by the operations team.

- KREDMI would send NACK message to Ratan. 'ns:trackingId' will be same with the request message. - Ratan will display the accounting error on the Dashboard. - KR OPS will manually handle such accounting error in Oscar/OLTP.

When exception with '"*body" : "Error"', mark accounting status as 'REJECTED' with reason 'Can not reach to OLTP'.

OLTP_EOD_ERROR("EOD001", "Can not reach to OLTP")

**EXPAND: Exception JSON sample from KREDMI**

{

"SCBML" : {

"ns:header" : {

"ns:messageDetails" : {

"ns:messageType" : {

"ns:subType" : { },

"ns:typeName" : "CoreBanking:businessOnlineBCommonRoute"

},

"ns:messageVersion" : "1.0",

"ns:multiMessage" : {

"ns:multiMessageKnown" : { }

}

},

"ns:originationDetails" : {

"ns:trackingId" : "BBW010120260513174000921031",

"ns:checksum" : { },

"ns:initiatedTimestamp" : "2026-05-13T17:40:00:435",

"ns:serviceBusID" : "CB_TBS03_H221",

"ns:messageSender" : {

"ns:countryCode" : "KR",

"ns:messageSender" : {

"*body" : "BOB"

},

"ns:senderDomain" : {

"ns:domainName" : {

"*body" : "CoreBanking"

},

"ns:subDomainName" : { }

}

},

"ns:possibleDuplicate" : "FALSE"

},

"ns:captureSystem" : "OLTP",

"ns:process" : {

"ns:eventType" : ""

},

"ns:exceptions" : {

"ns:exception" : [ {

"ns:timestamp" : "2026-05-13T08:41:02.101+00:00",

"ns:code" : {

"*body" : "Error"

},

"ns:description" : "com.wm.app.b2b.server.ServiceException: [ISS.0086.9067] wait timed out\n\tat scbIntServicesUtilities.java.throwException(java.java:938)\n\tat jdk.internal.refle

} ]

}

}

}

}

**EXPAND_END**

# Open Questions:

| Number | Question | Answer | If Finished | Remark |
| --- | --- | --- | --- | --- |
| 1 | For 'Bank GL Code', the value is 17, is it branch code of Korea? | Yes.2026-03-16 | Done. | |
| 2 | Could OLTP get hardcode columns instead of sending from RATAN? 12 columns hardcoded now. | No need now.2026-03-16 | Done | |
| 3 | if all bridge currency same with nostro currency? if bridge amount always same with nostro amount? | Yes, until now.2026-03-16 | Done | |
| 4 | ACK/NACK sample | Body ready, error code ready. Need to confirm solace header.2026-04-08 Send email to ask EDMI team.2026-03-16 | Done | |
| 5 | Request Fields mapping and respond fields mapping. | Only for solace header.2026-04-08 Got request fields mapping. Need respond message 2026-03-16 | Done | |
| 6 | Ratan change status to 'SUCCESS' after EDMI ACK or OLTP ACK? | After OLTP ACK, no EDMI ACK now.2026-03-17 | DONE | |
| 7 | If accounting status is 'REJECTED', what will user do? Reprocess it in Oscar? Or other actions? | No action needed in RATAN, OPS team will process it separately. Asked in email, no response.2026-03-17 | DONE | |
| 8 | Study more business scenarios to trigger accounting. | | DONE | |
| 9 | Nostro account if nostro account is not 0, capture nostro account; if nostro account is 0, then if currency is "KRW" or "KRO"(Currency code:999) then 000261; else 043151 | User would like to know more mapping between RATAN account and Murex account.2026-03-25 Talked internally. Only capture Nostro account, replace logic when nostro accounting is 0.2026-03-17 Need to recheck with OLTP user.2026-03-16 | DONE | |
| 10 | For "AIRCBIC":"KOEXKRSE___", //RATAN side Could directly use 53BIC? Need to clarify logic. | Will update in DOI that must update nostro correspondent BIC when add/update Nostro static data.2026-04-09 Nostro correspondent BIC, when NOS, this BIC can't be empty. And for other NOX account, ensure also to fill in this BIC. 2026-04-08 Under discussion2026-03-17 | DONE | |
| 11 | Check with OLTP whether they need retry 3 times. | No need retry. 2026-03-25 | DONE | |
| 12 | Could RATAN send currency code directly instead of code numbers. For example, USD, not 001. | Yes. 2026-03-25 | DONE | |
| 13 | Share error code to OLTP for reference | Already got error code from OLTP2026-04-08 Shared by Lina.2026-03-17 | DONE | |
| 14 | In the future, if reference number less than 16 chars, could accept it? -->OLTPAIREFNO | No need further discussion now. 2026-03-25 | DONE | |
| 15 | The accounting messages which already in HOLD status before value date will be send at 6AM Local time, and if amount of accounting is huge, will continue send every one hour. -->OLTP | Accepted by user. | DONE | |
| 16 | OLTP EOD break down time during 23:30-00:30 Korea time | KREDMI will back time out exception message. - Ratan will display the accounting error on the Dashboard. - KR OPS will manually handle such accounting error in Oscar/OLTP. | | |

# Static Data

| Entity Name | FMID | Country Code | Branch code |
| --- | --- | --- | --- |
| SCFB_SEOUL | 10036645 | KR | 70 |

| M_ENTITY | FMID | ISO Currency | Bridge Account |
| --- | --- | --- | --- |
| SCFB_SEOUL | 10036645 | KRW | 000287 |
| SCFB_SEOUL | 10036645 | FCY(foreign currency) | 040446 |

# Reference page:

[Cash Settlements Migration -Korea- Scope & Plan - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3588497557)

[Cash Settlement - EBBS Accounting - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Cash+Settlement+-+EBBS+Accounting#CashSettlementEBBSAccounting-eBBSfilefieldmapping)

[Sender BIC / Receiver BIC Pick-Up for different Payment template - Murex Development Team - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3085500215)

[Cash Settlement - EBBS Accounting - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Cash+Settlement+-+EBBS+Accounting#CashSettlementEBBSAccounting-eBBSfilefieldmapping)