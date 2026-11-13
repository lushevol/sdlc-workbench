# Overall process flow

# FileIT Infra info

FileIT can be configured whether to remove source file after file delivered or not. (we choose yes to remove)

##### DEV

source path: /share/**imft070**/ratanone/aspire

target path:

- /share/**imft115**/ASPIRE/RATAN/HK/data/incoming/<file_name>
- /share/**imft115**/ASPIRE/RATAN/TW/data/incoming/<file_name>
- /share/**imft115**/ASPIRE/RATAN/TH/data/incoming/<file_name>

##### PROD

source path: /share/**imft054**/ratanone/aspire

target path:

- /share/**imft157**/ASPIRE/RATAN/HK/data/incoming/<file_name>
- /share/**imft157**/ASPIRE/RATAN/TW/data/incoming/<file_name>
- /share/**imft157**/ASPIRE/RATAN/TH/data/incoming/<file_name>

## FileIT SPOC

fileIT dev spoc: **Boppudi, Suresh Babu<[SureshBabu.Boppudi@sc.com](mailto:SureshBabu.Boppudi@sc.com)>  Korrapati, Naga Kiran<[NagaKiran.Korrapati@sc.com](mailto:NagaKiran.Korrapati@sc.com)>
**

fileIT dev lead: **Rohit, Chhibber<[Chhibber.Rohit@sc.com](mailto:Chhibber.Rohit@sc.com)>**

<u>**Solace connection info**</u>

![image-2025-7-11_9-49-26.png](attachments/image-2025-7-11_9-49-26.png)

**topic name:** v1/51358-ratan-one/fileit/imft-json-1.0/-/req    (MB topic name: Cash_Settlement_Aspire_FileIT_Process_Out)

**ack queue name:** q-51358-ratan-one-imft-ack-all (FileIT will publish ack message to this queue)  (MB topic name: Cash_Settlement_Aspire_FileIT_Ack)

DEV:

- <u>**HOST:** [smfs://hk-np3.fs-solace.dev.net:55443,smfs://hk-np4.fs-solace.dev.net:55443](smfs://hk-np3.fs-solace.dev.net:55443,smfs:)</u>
- **VPN**: vpn-fs-imft-t1
- **USERNAME**: 51358-ratan

PROD:

- <u>**HOST:** </u>[smfs://hk-prd3.fs-solace.sc.net:55443,smfs://hk-prd4.fs-solace.sc.net:55443](smfs://hk-prd3.fs-solace.sc.net:55443,smfs:)
- **VPN**: vpn-fs-imft-p1
- **USERNAME**: 51358-ratan

Request solace message to FileIT:

```js
"ImftFileRequest": {
      "header": {
        "messageVersion": "v1",
        "flowIdentifier": "RATAN_CASHSTLMT_GL",
        "uuid": "74e081a1-e599-45a7-b6a2-ab7540ff0b37",  -- <generate new for each request>
        "country": "GL",
        "sourceName": "51358-RATAN"
      },
      "payload": {
        "source": {
          "srcFilePath": "/share/imft054/ratanone/xxx.gz"
        },
        "target": {
          "dstName": "51282-ASPIRE",
          "dstFilePath": "/some-nas/consumer-use/ratanone/xxx.gz"
        }
      }
    }
```

Ack from FileIT:

```js
{
   "IMFTFileNotification" : {
        "Header" : {
            "Version" : " ",            //1.0
            "Identifier" : "",          //EBBS_MT940_HK
            "UUID" : " ",               //90e6bb42-66bf-11ea-bc55-0242ac130003
            "SrcJMSID" : " ",           //1234569999999
            "Source": "",               //43454-EBBS
            "Target": "",               //50821-IMFT
            "Country": " "              //HK
            "Timestamp":" "             //yyyy-MM-dd HH:mm:ss.S Z ("2020-05-04 20:46:19.511 +0800")
        },
        "Payload" : {
            "Component" : "",           // IS/CFT/GW/TDE
            "SubComponent" : " ",       // EBBS_IMFT_MT940_HK for CFT or EBBS.EBS.HK.IMFT.IMFT.HK.MT940 at TDE
            "TrackingID": " ",          //tracking id specific component
            "SrcFilePath" : " ",        // /imft/shared/ebbs/sample.zip/
            "Status" : {
                "Code":"",              //2000
                "Reason" : "",          //CFT_SUCCESSFUL
                "Causes" : {
                   "Details":["",""]   // File Transfer completed to destination
                }                     
            }
        }
    }
}
```

more details for request and response taxonomy at: [Solace Message Structure And Taxonomy](https://confluence.global.standardchartered.com/display/IMFT/Solace+Message+Structure+And+Taxonomy)

## Return Codes

| Notification Type | code | Reason | Description |
| --- | --- | --- | --- |
| ftaccepted | 1000 | ACCEPTED | File Transfer Request Accepted for flow |
| failed | 1001 | NOT_AUTHORIZED | Not Authorized to trigger flow |
| 1002 | BAD_REQUEST | Invalid Request |
| 1003 | INVALID_ROUTING_RULE | Missing Routing Rule for flow |
| 1004 | CFT_AUTHORIZATION_FAILURE | Invalid CFT API Credential |
| 1005 | CFT_UNAVAILABLE | Source CFT is down |
| 1006 | COPILOT_UNAVAILABLE | Source Copilot is down |
| ftinitiated | 1100 | INITIATED | File Transfer Request Accepted for flow |
| ftsuccessful | 2000 | CFT_SUCCESSFUL | File Transfer Successful for flow |
| failed | 2001 | CFT_SOURCE_PATH_INVALID | Source path does not exit |
| 2002 | CFT_SOURCE_PRE_PROCESSING_FAILED | Source Pre-processing Script failed |
| 2003 | CFT_SOURCE_POST_PROCESSING_FAILED | Source Post-processing script failed |
| 2004 | CFT_PARTNER_INVALID | Target CFT name not correctly mentioned |
| 2005 | CFT_TARGET_PATH_INVALID | Destination path not correctly mentioned |
| 2006 | CFT_TARGET_POST_PROCESSING_FAILED | Target Post processing script failed |
| 2007 | CFT_SOURCE_FILE_INSUFFICIENT_PERMISSION | Source file do not have permission |
| 2008 | CFT_TARGET_PATH_INSUFFICIENT_PERMISSION | Target path do not have permission |
| 2010 | CFT_SOURCE_IDF_INVALID | Idf not correctly mentioned |
| 2020 | CFT_TRANSFER_FAILED | Transfer failed |
| notify | 5000 | CFT_NOTIFICATION | Receiver notification successful from Receiver processing script |
| 5001 | CFT_NOTIFICATION | Receiver notification failure from Error processing script |