# ***Introduction:***

*       GraphQL is a query language for your API, and a server-side runtime for executing queries using a type system you define for your data. GraphQL isn't tied to any specific database or storage engine and is instead backed by your existing code and data.*

![image2023-4-19_10-14-12.png](attachments/image2023-4-19_10-14-12.png)

# ***Reasons for using GraphQL:***

*1) GraphQL APIs have a strongly typed schema*
*2) No more overfetching and underfetching*
*3) GraphQL enables rapid product development*
*4) Composing GraphQL APIs*
*5) Rich open-source ecosystem and an amazing community*

# ***GraphQL features:** *

1. *Query for reading data (recommended in ratan)*
2. *Mutation for writing data*
3. *Subscription for automatically receiving real-time data over time.(recommended in ratan)*

# ***RATANONE use cases:***

## ***Standard & Principle***

| | *Principal * | *Comment* | Exceptions |
| --- | --- | --- | --- |
| 1 | All RATANONE front end query to backend APIs are supposed to go via GraphQL | | |
| 2 | GraphQL schema should be defined clearly for each use cases before implementing it | Reduce the number of API calls from UI to backend, best utilize the capability of GraphQL to aggregate data. | If any aggregation party cause performance issue, we may consider to make it a single API call. |
| 3 | All fields/attributes used by GraphQL query need to be defined as standard logical model/Biz term natively in DM or RATAN extension. | All the fields should be from the fields defined in rule service, Data modelling indexed term is the first choice, Ratan specific fields should be defined otherwise and mark as RATAN_DATA | |
| 4 | The performance of GraphQL query should be tracked and monitored | | |
| 5 | | | |

## ***Use cases

**ANCHOR: usecases**
***

| *No.* | *Case* | *Type* | *Schema* | *Description* |
| --- | --- | --- | --- | --- |
| | *Query Trade List* | *HTTPS GET* | Click: | |
| | *Query Trade Detail* | *HTTPS GET* | |
| | *Quick search on Trade blotter * | *HTTPS GET* | |
| | *Trade Notification* | *Subscription * | |
| | *Query Cashflow List* | *HTTPS GET* | Click: [▶ Multi Exceptions - Exceptions in Cashflow CN (figma.com)](https://www.figma.com/proto/crlFDt3cKfWzIXWdUhrtQ7/Exceptions-in-Cashflow-CN?node-id=521-2&scaling=scale-down-width&page-id=0%3A1&starting-point-node-id=521%3A2) | |
| | *Query Cashflow Detail* | *HTTPS GET* | |
| | *Quick search on Cashflow blotter * | *HTTPS GET* | |
| | *Cashflow Notification* | *Subscription* | |
| | *Query Counterparties Info* | *HTTPS GET* | Click: | |
| | *Query Exceptions List* | *HTTPS GET* | Click: | |
| | *Exceptions Notification* | *Subscription * | |
| | *Quick Search* | *UX* | | *for user can search by static fields* |
| | *Custom Filter* | *UX* | | *for user build search conditions by multi search fields* |
| | *Custom View* | *UX* | | *for user customize table columns and query list response structure* |

## **Trade Schema Diagram

**ANCHOR: trade_schema**
**

### Query Schema

### Result Schema

### Trade Notification Schema

## **Cashflow (BCS) Schema Diagram

**ANCHOR: cashflow_schema**
**

### **Query Schema**

#### cashflow

#### Cashflow Audits

### **Result Schema**

#### cashflow

#### Cashflow Audits

### Cashflow Notification

## **Cashflow (Settlement CN) Schema Diagram

**ANCHOR: cashflow_schema**
**

### **Query Schema**

#### cashflow

#### Cashflow Audits

#### Cashflow Details

### **Result Schema**

#### cashflow

#### Cashflow Audits

#### Cashflow Details

For more information, please refer to

### Cashflow Notification

## **Sc****hema

**ANCHOR: counterparties_schema**
**

### **Query Schema**

### **Result Schema**

****

## **Exception Sc****hema

**ANCHOR: exception_schema**
**

### **Query Schema**

### **Result Schema**

****

### Exception Notification Schema

****

# * PT - Graphql VS Restful*

*[Ratan UI Performance Analysis (2022 Dec) - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2608466605)*