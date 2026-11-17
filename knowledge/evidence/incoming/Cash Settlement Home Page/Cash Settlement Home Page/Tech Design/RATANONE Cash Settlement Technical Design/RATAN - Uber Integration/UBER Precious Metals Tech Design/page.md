# Requriment

[Story 14562333 [FMRP 9.0 Commodities] Precious Metals - Update relevant APIs for dowstream systems(CIS) 26C](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14562333)

[Story 14449450 [FMRP 9.0 Commodities] Precious Metals - Swift Msg - Field_26_Commodity_Identity](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14449450)

# Tech Details

For UBER message cashlfows, using **Custodian_SCI_FMID(Custodian_Name)/****Delivery_Location **to**  **identify precious metals and apply special logic for

**Custodian name stamping – Group Service**

**API for CIS query – Query Service **

**Netting logic for precious metal  – Netting Service**

**26C field generation – Swift Service**

**Rule Setup - Nstp,Netting,RuleEngine Service**

All these changes except rule setup rely on the new version of SEBRA SDK.

New Fields Path:

Custodian_SCI_FMID:  tradeRecord.Entity.Custodian_SCI_FMID

Delivery_Location:       tradeRecord.Delivery_Location

## Sabre SDK

current version:  v7.23-RELEASE-20260130.2-17e9c9eb

upgrade version:  v7.54-RELEASE-20260902.5-3f9f4726

domain service impact: **message-bridge, orchestration, group, lifecycle, query, netting, swift, utilization, open-search, ssi-stamping**

## Foundation

Foundation upgrade version: 8.0.9.1

## Message Bridge

Foundation upgrade version: 8.0.9.1

## Orchestration

Foundation upgrade version: 8.0.9.1

## Lifecycle Service

Foundation upgrade to 8.0.9.1

## Utilization Service

Foundation upgrade to 8.0.9.1 （Settlement Method Update will trigger cashflow stamping）

## Group Service

Foundation upgrade to 8.0.9.1 & cashflow stamping  custodian name by calling DA with custodian FMID

## SSI Stamping Service

Foundation upgrade to 8.0.9.1

## Orchestration

@Chen Yang

## Query Service

Add delivery location for all product.

Path list as blow:

- Trade.Structured_Instrument.Forward_Future_Instrument.Far_Leg.Delivery_Location
- Trade.Structured_Instrument.Forward_Future_Instrument.Near_Leg.Delivery_Location
- Trade.Loan_Deposit_Instrument.Delivery_Location
- Trade.Forward_Future_Instrument.Delivery_Location
- Trade.Swap_Instrument.Commodity_Leg.First_Leg.Delivery_Location
- Trade.Swap_Instrument.Commodity_Leg.Second_Leg.Delivery_Location
- Trade.Option_Instrument.Commodity_Leg.Delivery_Location
- Trade.Intent_To_Allocate
- Trade.Entity.Custodian_Name
- Trade.Entity.Custodian_SCI_FMID
- Trade.Delivery_Location

## Open Search

@zhang jiangnan

Add delivery location for all product.

Path list as blow:

- Trade.Structured_Instrument.Forward_Future_Instrument.Far_Leg.Delivery_Location
- Trade.Structured_Instrument.Forward_Future_Instrument.Near_Leg.Delivery_Location
- Trade.Loan_Deposit_Instrument.Delivery_Location
- Trade.Forward_Future_Instrument.Delivery_Location
- Trade.Swap_Instrument.Commodity_Leg.First_Leg.Delivery_Location
- Trade.Swap_Instrument.Commodity_Leg.Second_Leg.Delivery_Location
- Trade.Option_Instrument.Commodity_Leg.Delivery_Location
- Trade.Intent_To_Allocate
- Trade.Entity.Custodian_Name
- Trade.Entity.Custodian_SCI_FMID
- Trade.Delivery_Location

## Netting Service

### Netting

for precious metals fields.

- Murex cashflows use Murex_Product_Strategy.
- Historical stella cashflows for Portfolio PRC_ECOM_SPOT_STL also use Murex_Product_Strategy.
- New stella cashflows use Trade.Entity.Custodian_SCI_FMID and Trade.Delivery_Location.

.

### Splitting

Not support PM currency.

## Swift Service

### 26C fields generate Logic:

### Murex FMRP Strategy mapping

new api:     /v1/ratan/swift/isUdfStrategyMapped

### New Table

![image-2026-9-24_10-58-51.png](attachments/image-2026-9-24_10-58-51.png)
![image-2026-9-24_10-59-26.png](attachments/image-2026-9-24_10-59-26.png)

# Appendix

## Netting Test Result

env: fmrp1

1000 cashflows netting

![image-2026-9-1_16-14-51.png](attachments/image-2026-9-1_16-14-51.png)

![image-2026-9-1_16-25-26.png](attachments/image-2026-9-1_16-25-26.png)

3000 cashflows netting

![image-2026-9-1_16-34-58.png](attachments/image-2026-9-1_16-34-58.png)

![image-2026-9-1_16-36-55.png](attachments/image-2026-9-1_16-36-55.png)

5000 cashflows netting

![image-2026-9-1_16-46-19.png](attachments/image-2026-9-1_16-46-19.png)

![image-2026-9-1_16-51-3.png](attachments/image-2026-9-1_16-51-3.png)

staging:

![image-2026-10-6_15-40-21.png](attachments/image-2026-10-6_15-40-21.png)

![image-2026-10-6_15-39-34.png](attachments/image-2026-10-6_15-39-34.png)

![image-2026-10-6_15-44-11.png](attachments/image-2026-10-6_15-44-11.png)