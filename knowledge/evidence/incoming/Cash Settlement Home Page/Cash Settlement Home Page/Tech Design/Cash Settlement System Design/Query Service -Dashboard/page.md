# Requirement from PO

- Real time Dashboard showing the count of cashflows in different statuses
- Auto refreshed as and when cashflow statuses change
- Clicking on a particular datapoint should display the list of cashflow details underneath that
- Ability to apply Filters (values must be alphabetically sorted)
- QUEUED should include only next 5 business days (normally should be zero volume in QUEUED)
- Exposure column should be calculated only based on items pending for Ops action (rephrase as ‘Top Exposure based on o/s Cashflows， WAITING, ERROR, QUEUED, READY, HOLD, NACK, FAILED)
- On Friday, VD-1 should include Saturday, Sunday and Monday
- All Exceptions should be included with scroll bar

![](https://dev.azure.com/sc-ado/777f0ba6-cfdf-4f44-99dd-ae1dc434f5c5/_apis/wit/attachments/e5203114-5ea6-4b5f-bf39-f157f950addd?fileName=image.png)

# Design

## Diagram

## Graph data model for the Dashboard （query service part）

```erl
type GraphCashFlowDashBoard{
    Status_Num:CashflowStatusNum
    Failed_Num:CashflowFailedNum
    Volume_By_VD:VolumeByVD
    Exception_Num:ExceptionNum
    Top_Exposure:TopExposure
}

type TopExposure{
    Exposure_List:[Exposure]
}

type Exposure{
    Amount:String
    Counter_Party:String
    Type:String
}
type ExceptionNum{
    VD_Exceptions:[VDException]
}

type VDException{
    Exception_Code:String
    VD_Num:Int
    VD1_Num:Int
    VD2_Num:Int
    VDM_Num:Int
}
type VolumeByVD{
    VD_Num:Int
    VD1_Num:Int
    VD2_Num:Int
    VDM_Num:Int
}
type CashflowFailedNum{
    Total_Num:Int
    Internal_Total_Num:Int
    External_Total_Num:Int
    Total_Today_Num:Int
    Internal_Today_Num:Int
    External_Today_Num:Int


    Total_Yesterday_Num:Int
    Internal_Yesterday_Num:Int
    External_Yesterday_Num:Int

    Total_PriorDates_Num:Int
    Internal_PriorDates_Num:Int
    External_PriorDates_Num:Int

}
type CashflowStatusNum{
    Wating_Today_Num:Int
    Error_Num:Int
    Queued_Num:Int
    Nack_Num:Int
    Hold_Num:Int
    Group_Error_Num:Int
    Group_Pending_Num:Int
    Failed_Today_Num:Int
}
```

## Interface

| API Name | Interface | Method | Request Sample | Response Sample | Header | Note |
| --- | --- | --- | --- | --- | --- | --- |
| Query Cashflows | http://{domain}/[graphql](https://uklvadapp1346.uk.dev.net:8868/graphql) | Post | { cashflowDashboard( filter: [] page: 0 size: 6 ) { Status_Num { Wating_Today_Num Error_Num Queued_Num Nack_Num Hold_Num Group_Num Failed_Today_Num } Volume_By_VD{ VD_Num VD1_Num VD2_Num VDM_Num } Exception_Num{ VD_Exception{ High_Value_Num GSAM_Num Missing_Vostor_Num Missing_Nostor_Num Back_Value_Date_Num Secondary_Vostro_Num Pending_Affirmation_Num } VD1_Exception{ High_Value_Num GSAM_Num Missing_Vostor_Num Missing_Nostor_Num Back_Value_Date_Num Secondary_Vostro_Num Pending_Affirmation_Num } VD2_Exception{ High_Value_Num GSAM_Num Missing_Vostor_Num Missing_Nostor_Num Back_Value_Date_Num Secondary_Vostro_Num Pending_Affirmation_Num } VDM_Exception{ High_Value_Num GSAM_Num Missing_Vostor_Num Missing_Nostor_Num Back_Value_Date_Num Secondary_Vostro_Num Pending_Affirmation_Num } } Top_Exposure{ Exposure_List { Amount Counter_Party Type } } Failed_Num { Total_Num Internal_Total_Num External_Total_Num Total_Today_Num Internal_Today_Num External_Today_Num Total_Yesterday_Num Internal_Yesterday_Num External_Yesterday_Num Total_PriorDates_Num Internal_PriorDates_Num External_PriorDates_Num } } } | { "data": { "cashflowDashboard": { "Status_Num": { "Wating_Today_Num": 5, "Error_Num": 0, "Queued_Num": 0, "Nack_Num": 0, "Hold_Num": 0, "Group_Error_Num": 51, "Group_Pending_Num": 7094, "Failed_Today_Num": 0 }, "Volume_By_VD": { "VD_Num": 5, "VD1_Num": 4, "VD2_Num": 0, "VDM_Num": 0 }, "Exception_Num": { "VD_Exceptions": [ { "Exception_Code": "ReInstate", "VD_Num": 1, "VD1_Num": 0, "VD2_Num": 0, "VDM_Num": 0 }, { "Exception_Code": "Missing Vostro", "VD_Num": 1, "VD1_Num": 0, "VD2_Num": 0, "VDM_Num": 0 }, { "Exception_Code": "Pending Affirmation", "VD_Num": 0, "VD1_Num": 1, "VD2_Num": 0, "VDM_Num": 0 }, { "Exception_Code": "Murex IRS", "VD_Num": 1, "VD1_Num": 0, "VD2_Num": 0, "VDM_Num": 0 } ] }, "Top_Exposure": { "Exposure_List": [ { "Amount": "-17736934.095781", "Counter_Party": "BOA*MMB", "Type": "BANK" }, { "Amount": "2002.020000", "Counter_Party": "LEONTEQ SECUR*ZRH", "Type": "FININST" }, { "Amount": "2002.000000", "Counter_Party": null, "Type": "null" }, { "Amount": "1001.000000", "Counter_Party": "LEONTEQ SECUR*ZRH", "Type": "null" }, { "Amount": "-773.818065", "Counter_Party": "SCB SUZHOU*SUZ", "Type": "INTECOM" } ] }, "Failed_Num": { "Total_Num": 336, "Internal_Total_Num": 3, "External_Total_Num": 333, "Total_Today_Num": 0, "Internal_Today_Num": 0, "External_Today_Num": 0, "Total_Yesterday_Num": 0, "Internal_Yesterday_Num": 0, "External_Yesterday_Num": 0, "Total_PriorDates_Num": 336, "Internal_PriorDates_Num": 3, "External_PriorDates_Num": 333 } } } } | | |

## Query flow

Note more detail in the diagram

![image2024-5-10_16-20-40.png](attachments/image2024-5-10_16-20-40.png)