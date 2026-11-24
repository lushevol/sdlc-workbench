# 1. Outline

In order to support the function of self service in business and ensure the compatibility of existing business functions, and integrate to the existing unified maker/checker mechanism, the following design is made.

Furthermore, in order to facilitate the user's operation, we choose **one** form and **once** maker/checker operation to simplify the user's operation.

# Decision Choice

## All Static Data store in Static-Service

Using one schema, confirmed the fact that static-service is responsible for all static data config maintainance

## All Static Data store in Domain-Service

Using multi schema, confirmed the fact that seperated domain service is responsible for itself static data config maintainance

## Responsible Comparing Matrix

| | Choice | Prons | Crons | |
| --- | --- | --- | --- | --- |
| 1 | static config store in static-service | 1.unified static config 2.static-service has its existing value 3.data maintain easy, especially for self-service cross multi static config | 1.other domain service need depend static-serivce | |
| 2 | | | | |
| 3 | static config store in domain-service seperated | 1.domain service maintain itself static config 2.do not depend any other service for function from config side | 1.once data being share someday, will produce responsible misunderstanindg like group-service and fxu-service about rounding-config 2.static-service do not have its existing meaning | |
| 4 | | | | |
| 5 | Temporary Conclusion: based on above comparing, we can draw a conclusion is that: static-service is one independent micro service which is **responsible **for maintaining static config and provide querying function to other domain service | |

## Self-service Choice

| | Choice | Prons | Prons | Crons |
| --- | --- | --- | --- | --- |
| 1 | all static data stored in static-service | | 1.static-service has its exsiting meaning 2.easy to implement self-service 3.do not involve complicated tech easy to maintian 4.do not other domain-service change code, they will keep code as before to fetch data | |
| 2 | | | | |
| 3 | all static data stored in domain-service seperated using event mechanism | | 1.domain serivce data store in its schema | 1.more complicated and many failure case need to be considered |
| 4 | | | | |
| 5 | all static data stored in domain-service seperated using distribute transaction | too complicated to implement, since have many tech detail need to involve and it so complicated that we do not prefer this way. | can utilize third part code to integrate | 1.too complicated to implement 2.not easy to maintain |