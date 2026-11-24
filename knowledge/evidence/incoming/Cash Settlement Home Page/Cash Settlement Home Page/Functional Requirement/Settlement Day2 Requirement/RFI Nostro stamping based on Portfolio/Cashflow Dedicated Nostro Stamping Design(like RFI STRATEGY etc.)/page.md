# Backgroup & Purpose

1. brief **backgroup**: need to stamp nostro for **RFI** case using **dedicated** nostro config
2. currently **stamping nostro** need to support some **ways** are as follows: 1. use multi condition like **entity+ccy+settlementMeans+settlementAccount** to query nostro data(**existing **behaviour in prod) 2. use **portfolio+****ccy **to query nostro data(for **RFI**) 3. more demands and other conditions...
3. for supporting **RFI **case and more forthcomings **dedicated small quantity **nostro** **demands, we want a. to make this stamping **nostro** logic more **relevant universal **to meet more cases and **easy** to change,

involving ssi can refer:  [SSI Relevant - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/SSI+Relevant#SSIRelevant-StampingInvolvingSystem)
more demands can refer:  [RFI Nostro stamping based on Portfolio - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RFI+Nostro+stamping+based+on+Portfolio)

**EXPAND: more action need to do**

1. from walking through design and code we found there are many **duplicated** code and **tricky** code in existing project,
2. so **currently **we enhance minimum changing point, // **currently** we need to do
3. but for the **long term** we had better to do some **re-structure** to let it more changable and easy understand // **next step** we will do

**EXPAND_END**

# Changing Point

non-economic logic can refer:

# Economic Logic Changing in Group Service

for "customize logic" part
base on returned nostroId, then group-service can compare data between New and Withdrawal cashflow to **identify **if change has occurred

# Cashflow Stamping Logic Changing in SSI Service

# Nostro Maintain and Identify Dedicated

## DB Changing

## Logic Changing

1. Identify dedicated nostro Choices

| | Choice | logic seq | Pros | Cros | |
| --- | --- | --- | --- | --- | --- |
| 1 | use db directly+ child table only keep itself data | for RFI use sql where **mainTable **ccy='KOR' and dedicated->>'portfolio' in ('IR_SWP_KOR_RFI','IR_SWP_KOR_NYRF') for STRATEGY (need to golive add code to process) use sql where mainTable ccy='xxx' and dedicated->>'strategy' in ('aa','bb') and other condition | 1.data stored one place and fetch from one place | 1.maybe involve performance if have many nostroType, which will occurs many fetch to db, even if this is a normal cashflow rather than dedicated 2.lead performance affect to nostro table fetching | |
| 2 | use db directly+ duplicated data in child table | for RFI use sql where **childTable **ccy='KOR' and dedicated->>'portfolio' in ('IR_SWP_KOR_RFI','IR_SWP_KOR_NYRF') for STRATEGY (need to golive add code to process) use sql where childTable ccy='xxx' and dedicated->>'strategy' in ('aa','bb') and other condition | above all 1.identify dedicated type only fetching childTable | above 1 | |
| 3 | use memory logic | for RFI fixed column portoflio in bean identify RFI in memory sync data into condition list in memory when related nsotroType changed in db for STRATEGY(need to golive add code to process) fix column portoflio in bean add logic to identify RFI in memory sync data into condition list in memory when related nsotroType changed | 1.quick identify even if many nostroType | 1.need to load data into memory 2.when related data changed may occurs data not consistent | |
| 4 | use memory+db | for dedicated type fixed column portoflio in bean identify dedicated in memory when every request | 1.all data keep in db 2.after checker approve the data can be used no any duplicated logic or missing risk | 1.need to load data into memory 2.when dedicated nostro volumn become huge will take some time to identify | |
| 5 | **Conclustion**: from performance and affect existing system side, we prefer Choice3, and can support forthcomings dedicated demands, but due to the volumn for dedicated nostro is small and avoid some missing risk we finally select option4 one thing need **highlight** all Choices need change code and lead time for new nostroType | |

2. Chaning in nostro table Choices

| | Choice | Pros | Cros | |
| --- | --- | --- | --- | --- |
| 1 | use jsonb | 1.only one table easy to understand and maintain 2.keep compability for exisitng logic 3.easy extension for any field since it designed unstructured | involving new field in existing table | |
| 2 | use child table | 1.have seperate table maintain dedicated info | 1.not easy to extension, every adding new type like strategy, need add one column 2.every type data may have some blank value for other purpose 3.need change existing logic to meet compability 4.sql need to join to fetch data | |
| 3 | use child table with jsonb | as above choice2 | as above choice2 point 3&4 | |
| 4 | **Conclustion**: consider nostro data volumn is not huge and basic stable, and easy to understantd and maintain, lie RFI and other demand is belong to edge case, so we prefer chioce3 | |

3. **New **similar dedicated demand will involve **actions **we need to do like **strategy**:
1.let user give us strategy list  // **must**
2.let user give us match condition, RFI is portfolio+ccy  // **must****
**5.add code and new mapping field in ratanone-static-service  // **must
**

**Conclusion**:
**if **current nostro_table all field is enough(currently we provided **nostroType **and** dedicated_info**** **field for common)
**and**
all attribute value coming from cashflow xml or trade xml  // should be
we **only** need to do **minor** code change and **add** mapping config for new type**
**for more **complex** case we need do some code change base on further design

# Golive Manual Book

| | action | description | comment |
| --- | --- | --- | --- |
| 1 | deploy service | 51358-ratanone-static-data-service 51358-ratan-cash-settlement-ssi-stamping-service 51358-ratan-cash-settlement-group-management-service 51358-ratanone-swift-service 51358-ratan-cash-settlement-query-service | golive service enable RFI |
| 2 | execute db repo | 51358-ratanone-db-repository | migrate existign nostro static data to RFI |
| 3 | check log | | to see there is not any error log to ensure golive correctly |

# Q&A

| | question | answer | | |
| --- | --- | --- | --- | --- |
| 1 | 1.As per regulation deals must be settled via a dedicated RFI Nostro account held with SCB Korea only for special **portfolio(chagne avaliable) **and **ccy(KRO) **to use dedicated Nostro? 2.currently only KRO will trigger the RFI stamping means only KRO's portfoli can be identified? | yes | | |
| 2 | from flow chart, 1.existing vostro stamping logic will be affected? // no 2.or only affect the stamping nostro flow? // yes refer: [SSI Relevant - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/SSI+Relevant#SSIRelevant-InternalDetailFlow) | yes | | |
| 3 | if there is a trade with RFI portfolio and currency pair is USD/KOR. then the USD leg should follow normal stamping, only KOR leg apply the RFI stamping. which field in xpath? ![image-2025-12-22_9-40-8.png](attachments/image-2025-12-22_9-40-8.png) // yes on trade xml or cashflow xml? need to see code to find if have relevant field | yes | | |
| 4 | portfolio case only use portfolio and ccy two condition to find matched nostro? | yes | | |
| 5 | same logic need to be applied to both cashflow/trade stamping. how about adhoc? or other stamping? if we need consider split stamp? currently, we have **5 entry point**: 1.**cashflow **workflow stamp, normal case 2.user manual do **adhoc **stamp in WAITTING status//add logic to check if meed rfi condition, need to confirm // todo need to confirm 3.**trade **stamp used by out CDU system// if have this field?, exception like before 4.**accouting **stamp when cashflow may do pass normal stamp workflow 5.**split **stamp when manual split and chose SSI // todo need to confirm, **all above need** | yes | | |
| 6 | if cashflow is with RFI portfolio, but not KOR, such as GBP/USD, should it stamp to the RFI nostro? - No, only KRO will trigger the RFI stamping for now. KOR? how to identify? ccy, use portfolio path and ccy | yes | | |
| 7 | from flow chart, if we can assume existing query nostro way and newly adding query nostro using portfolio way are **exclusive**? means if meet portfolio condition(**portfolio+ccy**) will fetch special nostro static config otherwise use existing query? only some nostro dedicated for special RFI purpose? or can intersect? // also need to confirm with PO | yes | | |
| 8 | from flow chart, 1.if do not found any rfi nostro config will throw missing nostro exception? refer: //yes 2.if found multi how to process? will throw multi nostro exception? or make priority to find best match? // theoretically, one record need allowed at creating, but if multi found will throw multi nostro exception 3.use existing nstp exception or define new exception to identify this special behaviour? //keep as before 4.after throw exception will need user to manually process nostro config at WAITTING status in blotter? //can add and refresh at nostro static config we page | yes | | |
| 9 | from flow chart, if we stamp nostro for RFI do not depend any vostro info? like settlementMeans and settlementAccount? //only need portfolio+ccy | yes | | |
| 10 | if user perform adhoc SSI, will user be able to see other nostro or system directly set the portfolio nostro. allow this behaviour? seems do not follow the RFI itself restriction? //need to confirm | yes | | |
| 11 | settlement means/settlement account need to be the same between vostro/nostro, this validation does not need to apply to RFI portfolio cashflow need to remove this limit from backend, but, from UI side still need remove this restriction?//yes if only for adhoc case? since from fifth question, we can see there are five ways support stamping//all need | yes | | |
| 12 | if allow user to create multi same nostroType and nostroKey? like RFI+OP_GBL_EUR_STL+KRO? //unique | yes | | |
| 13 | Portfolio changes must update the Nostro selection, means if cashflow portfolio changed from Non-RFI to? dynamic or some special cashflowStatus restrict this behaviour or not support? // exist when nostro static config is updated? different portfolio match diferrent nostro? or multi? // nostroType+nostroKey is unique | yes | | |
| 14 | for RFI nostro static config, is the exisitng field enough like below? existing field will keep? // keep ![image-2025-12-3_13-57-36.png](attachments/image-2025-12-3_13-57-36.png) | yes | | |
| 15 | Vostro stamping should not overwrite Nostro stamping? // exclusive refer: [SSI Relevant - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/SSI+Relevant#SSIRelevant-InternalStampDetailFlow) | yes | | |
| 16 | add two column is enough? // yes currently we have web page for nostro info ![image-2025-12-5_14-0-23.png](attachments/image-2025-12-5_14-0-23.png) to avoid to introduce more complicated for user in UI webpage we will reuse this page and add two new filed, named nostro_type: DEFAULT|RFI|etc.. nostro_key: ""|portfolio_corresponding_value|etc.. // tech if we need more input to compose the nostroKey? // do not need currently currently we may use the portfolio field value + ccy to fetch nostro static config if we need additional field as condition to fetch, or all field already exist in nostro static config? // no | yes | | |
| 17 | ~~in flow chart in "Query Portfolio Nostro" node, ssi+ team will need change accordingly? who can I reach out? or for RFI we will responsible maintain static config like primary nostro static?~~ | ~~yes~~ | | |
| 18 | add hoc nostro do not need any check? allow user select any nostro by willing | need to confirm | | |
| 19 | how to notify user when there are multi rule meet one cashflow? | tech failed reason enhance | | |
| 20 | what is the trade portfolio path? ![image-2025-12-23_15-22-43.png](attachments/image-2025-12-23_15-22-43.png) | Y | | |
| 21 | how to identify economic-change? rfi->non-rfi non-rfi->rfi rfi1->rfi2 match condition: bookingEntityId+counterpartyFmId+paymentCurrency+paymentAmount+ValueDate+Direction+**settlementMethod**(7 factors) **--important: we assume c1 new and c1 withdraw 7 factors must be keep same** case one: group1: c1 new group2: c1 withdraw // direct flow into workflow to cancel case two: group1: c1 new group2: c1 withdraw+c2 new(**same** 7 factors) // amendment case three: group1: c1 new, group2: c1 withdraw(**settlementMethod1 different**)+c2 new // nothappen case four: group1: c1 new, group2: c1 withdraw+c2 new(**settlementMethod1 different**) // economic case five: group1: c1 new, group2: c1 withdraw(**settlementMethod1 different**)+c2 new(**settlementMethod1 different**) // not happen case six: group1: c1 new, group2: c1 withdraw(**settlementMethod2 different**)+c2 new(**settlementMethod1 different**) // nothappen | Y | | |
| 22 | how to adapt to the recent changes? created one rule rfi1, then message into group flaged with rfi1 change rule config, non-economic come amendment two message into group flaged with rfi2, this case should be treated as economic? --**only care **currently two message in group, if previous and currently do not same, will treat this group is economic | Y | | |
| 23 | ~~we enhance techFail case so as to let us or pss team to quick know what errors happened?~~ ![image-2025-12-30_14-46-48.png](attachments/image-2025-12-30_14-46-48.png) | Y | | |
| 24 | currently we found do not have any "MULTI_NOSTRO_ERROR" in prod db ![image-2025-12-30_14-52-55.png](attachments/image-2025-12-30_14-52-55.png) may be we do not use this error // keep it as is | Y | | |
| 25 | why we first choose rule-engine but then give up? first version, we prefer use rule-engine to do some decision logic, **but** for RFI dedicated case(refer to economic change part), we will need portfolio+ccy to decide if chagne happen, and also do not want to involve long invocation chain, which will **changing** rule-engine default behaviour **also** this rule is not avaliable to user, we will maintain it in backend so we will put this match RFI condition into ratan-cash-settlement-ssi-stamping-service to let it easy and minimal dependency | Y | | |
| 26 | if we need engage CDUPS team to double confirm which path(portfolio+ccy) can be used in rule? since in currnetly testing we found: 1."fixing" product do not have portfolio path 2."bullion swap" product have mult portfolio path 3.others type may be have some missing.. // currently we do not consider trade stamping | Y | | |
| 27 | if we occrurs some tech fail in group, how to process it? if this group is non amendment, **keep** it as before. if this group is amendment(new+withdrawal) and economic, **keep** it as before. if this group is amendment(new+withdrawal) and NonEcoAmend_Replace, **keep** it as before. if this group is amendment(new+withdrawal) and NonEcoAmend, will continue to go futher into workflow // need change to economic | Y | | |
| 28 | if we need to consider migration when golive? // supposed no, since currently we have unique key entity+ccy+settlementMeans+settlementAccount and based on user demand that only create nostro for RFI without any normal nostro static same as RFI, // so, we do not need to do any migration about before cashflow data | Y | | |
| 29 | who will create nostro static config ? developer or user? 1.we create RFI nostro config and rule at Saturday user can see the change and effected cashflow in Monday, then maintain nostro later 2.we create rule then notify user to create RFI nostro config a.if golive first at Saturday configed rule, user config nostro static data at next Monday, will lead some cashflow into missing vostro, then need user add some nostro data to trigger refresh machnism b.if user config nostro static data at Friday, golive at upcoming Saturday configed rule, // **cannot** support, because currently for RFI nostro can only allow user to add RFI config since we have uniqueKey do not allow user config other nostro config seems option1 is better | Y | | |
| 30 | duplicate check? EntityFmId+currency+settlementMeans+settlementAccount+nostroType? which do not allow user to create multi RFI with diferrent ebbsAccount? EntityFmId+currency+settlementMeans+settlementAccount+nostroType+portfolio? // maybe better? // finaly we use EntityFmId+currency+settlementMeans+settlementAccount+nostroType, only allow user to create one record with 5 same factors | Y | | |
| 31 | need to do partial migration: 1. add column named nostroType with default value 'DEFAULT' 2. in prod env, change special RFI nostro static config into nostroType=RFI as well as insert into dedicated table relevant data, // need user provide us RFI data already exist in prod others will set to 'DEFAULT' | Y | | |
| 32 | why we use nostroStaticId? after do some test in dev env, we found the id do not change even in create/update action also in fetching audit history we need this id to retrieve all audit data, so this id cannot be change, only one purpose is user have been familiar with this nostroStaticId? | | | |