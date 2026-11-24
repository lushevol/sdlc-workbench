# Background:

when user login [FMO Post Trade Portal], will call login api, and UI will show the blotters according the response data.

Here if  current user's entitlement not contains "8"（Indonesia FMID）, then UI can show blotters for non-ID only

Login with user=1622463 in DEV

The picture below is [Tile Configuration], here is the place to store blotters info, and we can filter blotters by user's ENTITY FMID

**EXPAND: UI display**

![image-2026-7-3_17-16-39.png](attachments/image-2026-7-3_17-16-39.png)![image-2026-7-2_17-9-44.png](attachments/image-2026-7-2_17-9-44.png)

![image-2026-7-3_9-11-42.png](attachments/image-2026-7-3_9-11-42.png)

**EXPAND_END**

**EXPAND: ssoLogin code**

**EXPAND_END**

# Tech desgin:

## Overall

## Detail

| application_tile | application_tile_audit |
| --- | --- |
| ALTER TABLE post_trade_portal_service.application_tile ADD entry_name varchar(255) NULL; | ALTER TABLE post_trade_portal_service.application_tile_audit ADD entry_name varchar(255) NULL; |
| ALTER TABLE post_trade_portal_service.application_tile ADD filter_rule json NULL; | ALTER TABLE post_trade_portal_service.application_tile_audit ADD filter_rule json NULL; |

**EXPAND: sql init**

SELECT t.application_category_id,t.application_tile_id,t.module,t.tile,t.title,t.subtitle,t.filter_rule

FROM post_trade_portal_service.application_tile AS t

where t.application_tile_id in(161,164,165, 173,174,171,172, 166,167,168,169,170)

-- where t.application_tile_id in( 39,37,38, 33,34,29,30, 123,52,50,137,51)

-- ID tile

update post_trade_portal_service.application_tile AS t

set filter_rule='{

"filterType": "ems3",

"parameters": {

"appId": "51358",

"appName": "RATAN_ENTITLEMENT_RULE"

},

"expression": "#root[''Entity.Booking_Entity_SCI_FMID''].contains(''8'')"

}'::json

where t.application_tile_id in(161,164,165, 173,174,171,172, 166,167,168,169,170)

-- GDC tile

update post_trade_portal_service.application_tile AS t

set filter_rule='{

"filterType": "ems3",

"parameters": {

"appId": "51358",

"appName": "RATAN_ENTITLEMENT_RULE"

},

"expression": "!#root[''Entity.Booking_Entity_SCI_FMID''].?[#this != ''8''].isEmpty()"

}'::json

where t.application_tile_id in( 39,37,38, 33,34,29,30, 123,52,50,137,51)

**EXPAND_END**

**EXPAND: step 1: add expression on UI-page**

![image-2026-7-8_22-14-31.png](attachments/image-2026-7-8_22-14-31.png)

**options: option1 is adopted in current code**

**EXPAND: option 1: add one column(ruelFilter)**

ALTER TABLE post_trade_portal_service.application_tile ADD filter_rule json NULL;

| TABLE | KEY | VALUE | affected tiles (24 in total) | may affected functions |
| --- | --- | --- | --- | --- |
| post_trade_portal_service. application_tile | filter_rule | **ID-BLOTTER** { "filterType": "EMS3_REGION", "parameters": { "appId": "51358", "appName": "RATAN_ENTITLEMENT_RULE" }, "expression": "#root['Entity.Booking_Entity_SCI_FMID'].contains('8')" } | **settlement-3** Cashflow Dashboard [ID] Grouping Blotter [ID] Cashflow Blotter [ID] --- **business rule-4** Settlement NSTP Rules New [ID] Authorization Limits [ID] Suppression Rules [Cashflow][ID] Suppression Rules [Swift][ID] --- **static -5** Nostro Static [ID] BIC Netting Static [ID] Netting Static [ID] Utilization Static [ID] Nostro Threshold Static [ID] | (1)insert (2)update (3)verify (4)deactive |
| | | **GDC-BLOTTER** { "filterType": "EMS3_REGION", "parameters": { "appId": "51358", "appName": "RATAN_ENTITLEMENT_RULE" }, "expression": "!#root['Entity.Booking_Entity_SCI_FMID'].?[#this != '8'].isEmpty()" } | **settlement-3** Cashflow Dashboard Grouping Blotter Cashflow Blotter --- **business rule-4** Settlement NSTP Rules New Authorization Limits Suppression Rules [Cashflow] Suppression Rules [Swift] --- **static -5** Nostro Static BIC Netting Static Netting Static Utilization Static Nostro Threshold Static | |

**EXPAND_END**

**EXPAND: option 2: add multi column**

| TABLE | filter_type | filter_parameter | filter_rule | may affected functions |
| --- | --- | --- | --- | --- |
| application_tile | EMS3_REGION | { "appId": "51358", "appName": "RATAN_ENTITLEMENT_RULE" } | #root['Entity.Booking_Entity_SCI_FMID'].contains('8') | (1)insert (2)update (3)verify (4)deactive |
| | EMS3_REGION | { "appId": "51358", "appName": "RATAN_ENTITLEMENT_RULE" } | !#root['Entity.Booking_Entity_SCI_FMID'].?[#this != '8'].isEmpty() | |

**EXPAND_END**

**EXPAND: option 3: create filter table**

step1: create table

| create table |
| --- |
| CREATE TABLE post_trade_portal_service.application_tile_filter ( id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL, code varchar NULL, is_active bool NOT NULL, filter_type varchar(255) NULL, filter_rule json NULL, CONSTRAINT application_tile_filter_pk PRIMARY KEY (id) ); |

step 2: insert data

![image-2026-8-24_10-19-32.png](attachments/image-2026-8-24_10-19-32.png)

step3: alter table application_tile or store application_tile_id in the new table

ALTER TABLE post_trade_portal_service.application_tile ADD filter_code varchar NULL;

**EXPAND_END**

**EXPAND_END**

**EXPAND: step 2: usage of expression**

**EXPAND_END**

**EXPAND: ems3-response**

[
    {
        "user_data": {
            "app_name": "RATAN_ENTITLEMENT_RULE",
            "itam_id": "51358",
            "user_id": "1633330"
        },
        "entitlements": {
            "entitlement_name": [
                "RATAN_ENTITLEMENT_COMMON",
                "RATAN_ENTITLEMENT_GLOBAL",
                "FMO_OPS_BOM",
                "RATAN_ENTITLEMENT_DEV_USERS"
            ],
            "data_policies": {
                "policy_rules": [
                    {
                        "data_policy_name": "RATAN - GBS CN PSS",
                        "policy_owner": "2021102"
                    }
                ]
            },
            "data_profiles": {
                "data_profile_rules": [
                    {
                        "data_profile_name": "RATAN- Back2Back FMID CN",
                        "data_profile_owner": "1666699"
                    },
                    {
                        "data_profile_name": "RATAN - back2back FMID",
                        "data_profile_owner": "2021102"
                    },
                    {
                        "data_profile_name": "RATAN - ALL ACCESS User",
                        "data_profile_owner": "2021102"
                    }
                ]
            },
            "data_entitlements": [
                {
                    "key": "Entity.Booking_Entity_SCI_FMID",
                    "values": [
                        "10040387",
                        "400568282",
                        "10038345",
                        "400516442",
                        "400516443",
                        "400667486",
                        "10020899",
                        "FMIDBRAMX01",
                        "400683682",
                        "400327728",
                        "400107029",
                        "300010872",
                        "401053411",
                        "300036368",
                        "400910415",
                        "15",
                        "400075752",
                        "400609343",
                        "400058959",
                        "400677737",
                        "10041902",
                        "300010633",
                        "400011581",
                        "10041903",
                        "2",
                        "123",
                        "3",
                        "400130178",
                        "4",
                        "400095464",
                        "5",
                        "400452428",
                        "10038468",
                        "6",
                        "10054931",
                        "7",
                        "8",
                        "9",
                        "400131263",
                        "401081696",
                        "FINNKOREA01",
                        "400040353",
                        "300010782",
                        "400170359",
                        "10041530",
                        "300011470",
                        "MUXBZ01",
                        "10036981",
                        "401037180",
                        "300084297",
                        "123M",
                        "10075222",
                        "400013111",
                        "400960089",
                        "1234",
                        "400041070",
                        "400001378",
                        "400045551",
                        "10062461",
                        "300011345",
                        "400032489",
                        "400451508",
                        "400033177",
                        "400931959",
                        "10037164",
                        "10032025",
                        "10063428",
                        "400045549",
                        "300075472",
                        "400991880",
                        "400617263",
                        "235003861",
                        "400192940",
                        "300089409",
                        "400059978",
                        "10078716",
                        "400077046",
                        "400077044",
                        "400057714",
                        "400798477",
                        "400209000",
                        "401036553",
                        "FM ID TST 1",
                        "400088463",
                        "400085753",
                        "400220273",
                        "400218197",
                        "400007847",
                        "300063361",
                        "300011525",
                        "400077978",
                        "10036647",
                        "400054708",
                        "10036642",
                        "10036645",
                        "10038667",
                        "400193370",
                        "400090093",
                        "10022098",
                        "400994973",
                        "400521212",
                        "400130180",
                        "400013557",
                        "10037477",
                        "10036382",
                        "400227738",
                        "400054741",
                        "400172181",
                        "10036775",
                        "400054737",
                        "10036655",
                        "400044944",
                        "400625349",
                        "400823493",
                        "400229749",
                        "400093619",
                        "10036430",
                        "400018439",
                        "400906330",
                        "400017223",
                        "300010730",
                        "400147183",
                        "10036428",
                        "400022800",
                        "400185419",
                        "400899993",
                        "195000930",
                        "400823482",
                        "400823485"
                    ]
                }
            ],
            "role_entitlements": [
                {
                    "feature": "RATAN_SETTLEMENT_EXCEPTION",
                    "action": "ACCESS_FMO_POST_TRADE_PORTAL"
                },
                {
                    "feature": "RATAN_TRADE_BLOTTER",
                    "action": "F_Custom_View_Builder_Public"
                },
                {
                    "feature": "RATAN_AUTO_NETTING_RULE",
                    "action": "ACCESS_FMO_POST_TRADE_PORTAL"
                },
                {
                    "feature": "RATAN_SETTLEMENT_EXCEPTION",
                    "action": "F_Input_Delete_Modify_SI_Verify"
                },
                {
                    "feature": "RATAN_CASHFLOW_BLOTTER",
                    "action": "F_Custom_Query_Builder"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "F_Perform_Un_Net_Verify"
                },
                {
                    "feature": "RATAN_TRADE_BLOTTER",
                    "action": "F_Export_Data"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "F_Hold"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "F_Reinstate"
                },
                {
                    "feature": "RATAN_CASHFLOW_GROUP_BLOTTER",
                    "action": "F_ManualStp"
                },
                {
                    "feature": "RATAN_MO_EXCEPTION",
                    "action": "ACCESS_FMO_POST_TRADE_PORTAL"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "F_ManualStp"
                },
                {
                    "feature": "RATAN_SETTLEMENT_EXCEPTION",
                    "action": "F_Manual_Fix"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "F_Un_Hold"
                },
                {
                    "feature": "RATAN_TRADE_BLOTTER",
                    "action": "F_Custom_View_Builder_Private"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "F_Multi_Exception_Verify"
                },
                {
                    "feature": "RATAN_TRADE_BLOTTER",
                    "action": "F_Custom_Query_Builder"
                },
                {
                    "feature": "RATAN_SETTLEMENT_EXCEPTION",
                    "action": "F_Manually_Close_Exception"
                },
                {
                    "feature": "RATAN_CASHFLOW_BLOTTER",
                    "action": "ACCESS_FMO_POST_TRADE_PORTAL"
                },
                {
                    "feature": "RATAN_CASHFLOW_BLOTTER",
                    "action": "F_Add_Settlement_Comment"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "F_Perform_Un_Net_Initiate"
                },
                {
                    "feature": "RATAN_CASHFLOW_BLOTTER",
                    "action": "F_Export_Data"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "F_Multi_Exception_Verify_High_Risk"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "F_Custom_Query_Builder"
                },
                {
                    "feature": "RATAN_CASHFLOW_BLOTTER",
                    "action": "F_Perform_Un_Net_Verify"
                },
                {
                    "feature": "RATAN_CASHFLOW_BLOTTER",
                    "action": "F_Reinstate"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "ACCESS_FMO_POST_TRADE_PORTAL"
                },
                {
                    "feature": "RATAN_CASHFLOW_BLOTTER",
                    "action": "F_Custom_View_Builder_Private"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "F_Modify_Settlement_Means"
                },
                {
                    "feature": "RATAN_CASHFLOW_BLOTTER",
                    "action": "F_Cashflow_Affirmation_Status_Change"
                },
                {
                    "feature": "RATAN_SETTLEMENT_EXCEPTION",
                    "action": "F_Replay_Exception"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "F_Multi_Exception_Initiate"
                },
                {
                    "feature": "RATAN_NETTING_RULE",
                    "action": "ACCESS_FMO_POST_TRADE_PORTAL"
                },
                {
                    "feature": "RATAN_NOSTRO_BLOTTER",
                    "action": "ACCESS_FMO_POST_TRADE_PORTAL"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "F_Export_Data"
                },
                {
                    "feature": "RATAN_SETTLEMENT_EXCEPTION",
                    "action": "F_Custom_View_Builder_Public"
                },
                {
                    "feature": "RATAN_SETTLEMENT_EXCEPTION",
                    "action": "F_Input_Delete_Modify_SI_Initiate"
                },
                {
                    "feature": "Entitlement",
                    "action": "View"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "F_Custom_View_Builder_Public"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "F_Perform_Cashflow_Split"
                },
                {
                    "feature": "RATAN_CASHFLOW_BLOTTER",
                    "action": "F_Ad_Hoc_Nostro_Initiate"
                },
                {
                    "feature": "RATAN_VALIDATION_EXCEPTION",
                    "action": "ACCESS_FMO_POST_TRADE_PORTAL"
                },
                {
                    "feature": "RATAN_CASHFLOW_BLOTTER",
                    "action": "F_Ad_Hoc_SSI_Verify"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "F_Custom_View_Builder_Private"
                },
                {
                    "feature": "RATAN_CASHFLOW_BLOTTER",
                    "action": "F_Ad_Hoc_Nostro_Verify"
                },
                {
                    "feature": "RATAN_CASHFLOW_GROUP_BLOTTER",
                    "action": "F_Cashflow_Status_Change_Release"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "F_Perform_Ad_Hoc_Netting"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "F_Cashflow_Status_Change_Release"
                },
                {
                    "feature": "RATAN_CASHFLOW_BLOTTER",
                    "action": "F_Ad_Hoc_Suppress"
                },
                {
                    "feature": "RATAN_ENTITLEMENT_RULE",
                    "action": "ACCESS_FMO_POST_TRADE_PORTAL"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "F_Fail"
                },
                {
                    "feature": "RATAN_CASHFLOW_BLOTTER",
                    "action": "F_Perform_Un_Net_Initiate"
                },
                {
                    "feature": "RATAN_PROFILE_LIMITS",
                    "action": "ACCESS_FMO_POST_TRADE_PORTAL"
                },
                {
                    "feature": "RATAN_SETTLEMENT_EXCEPTION",
                    "action": "F_Custom_View_Builder_Private"
                },
                {
                    "feature": "RATAN_CASHFLOW_BLOTTER",
                    "action": "F_Custom_View_Builder_Public"
                },
                {
                    "feature": "RATAN_TRADE_BLOTTER",
                    "action": "ACCESS_FMO_POST_TRADE_PORTAL"
                },
                {
                    "feature": "RATAN_SUPPRESSION_RULE",
                    "action": "ACCESS_FMO_POST_TRADE_PORTAL"
                },
                {
                    "feature": "RATAN_CASHFLOW_BLOTTER",
                    "action": "F_Ad_Hoc_SSI_Initiate"
                },
                {
                    "feature": "RATAN_SETTLEMENT_STP_RULE",
                    "action": "ACCESS_FMO_POST_TRADE_PORTAL"
                },
                {
                    "feature": "RATAN_TRADE_BLOTTER",
                    "action": "F_Retrigger_Confirmation_Dispatch"
                },
                {
                    "feature": "RATAN_CASHFLOW_GROUP_BLOTTER",
                    "action": "ACCESS_FMO_POST_TRADE_PORTAL"
                },
                {
                    "feature": "RATAN_CASHFLOW_BLOTTER",
                    "action": "F_Perform_Ad_Hoc_Netting"
                },
                {
                    "feature": "RATAN_STRATEGIC_CASHFLOW_BLOTTER",
                    "action": "F_Ad_Hoc_Suppress"
                }
            ]
        }
    }
]

**EXPAND_END**

| Test Account： |
| --- |
| ID Ops User: Data Ops: 1434424 Shankar M, Shiva - Both GDC and ID 1528028 Ramakrishnan, Yogentar - GDC only & ID（change to "400093619", "8","9","300063361"） Settlement Ops: 1140336 Eliana, Eliana - ID only 1129381 Sumita - Both GDC and ID 1462616 - GDC only Sumita will share |

# Exception handle

| - if ems3 down,------**hide ** - if dataEntitlement.filter.size=0------**hide** - if filter_rule do not match filter,------**show (chk before release, so never happen)** the tiles show/hide? | case 1: no dataEntitlement stores in redis, only filter by ems2 all tiles filter by ems3, return false case 2: has dataEntitlement stores in redis(expiryTime =3600s), filter by ems2 ——> ems3 |
| --- | --- |

# Question

**EXPAND: Q&A**

| NO | Q | A |
| --- | --- | --- |
| 0 | UI change @Guiling Wang | |
| 1 | if UI store rawJsonRlue, need to verify accuracy before any update/insert? | (1)must do, so when filter drawers in AuthFilter class is easier (2)use List<Drawer> class, not List<Map<String, Object>> |
| 3 | the current filterDrawers is for ems2, do we need to refactor it as a Ems2AuthFilter? | no need, may be designed end of this year ems2 is function-filter ems3 is data-filter(regionFilter) |
| 4 | with -XX:MaxMetaspaceSize=128m, new deployed code caused an OOM due to insufficient metaspace | -XX:MaxMetaspaceSize=512m |

**EXPAND_END**