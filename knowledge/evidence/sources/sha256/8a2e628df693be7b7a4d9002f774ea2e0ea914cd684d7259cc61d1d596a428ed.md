# logic flow

## description

1. For single group message ,flow the original logic, only group message status in PENDING or ERROR and no pending for previous major version can manual stp.

2. For multi group message, grouping by trade and executing by multi threads

3.  For each trade, precheck all trade:

3.1 **Pass** : order by major version and filter the group status =DATA_VALIDATION_FAILED/PENDING_PRE_GROUP and executing each group message by original logic.

3.2 **Failed**:  feedback to frontend the error message.

## Multi manual stp case

| case | **trade_group_majorVersion** | **UI S****elect ** | **expected result** |
| --- | --- | --- | --- |
| 1 | **T1_G1_V1**: PENDING_TRADE_VALIDATION C1：PENDING C2：PENDING ... C294：PENDING | **T1_G1_V1**: PENDING_TRADE_VALIDATION C1：PENDING C2：PENDING ... C291：PENDING ** ** | **T1_G1_V1**: PENDING_TRADE_VALIDATION C1：END C2：END ... C291：END |
| 1.2 | **T1_G1_V1**: **PENDING_TRADE_VALIDATION** c1:PENDING c2:END c3:ERROR **T1_G1_V2**: **PENDING_PRE_GROUP** c1: PENDING c2:END c3:PENDING | **T1_G1_V1**: **PENDING_TRADE_VALIDATION** c1:PENDING c2:END c3:ERROR **T1_G1_V2**: **PENDING_PRE_GROUP** c1: PENDING | **T1_G1_V1**: **COMPLETED** c1:PENDING c2:END c3:ERROR **T1_G1_V2**: **PENDING_PRE_GROUP** c1: PENDING |
| 1.3 | **T1_G1_V1**: **PENDING_TRADE_VALIDATION** c1:PENDING c2:PENDING **T1_G1_V2**: **PENDING_PRE_GROUP** c1: PENDING c2:PENDING | **T1_G1_V1**: **PENDING_TRADE_VALIDATION** c1:PENDING c2:PENDING **T1_G1_V2**: **PENDING_PRE_GROUP** c1: PENDING c2:PENDING | **T1_G1_V1**: **COMPLETED** c1:END c3:END **T1_G1_V2**: **COMPLETED** c1:END c3:END |
| 2.1 | **T1_G1_V1**: PENDING_TRADE_VALIDATION C1: END....C291:END C292：PENDING C293：PENDING C294：PENDING **T1_G2_V2**: PENDING_TRADE_VALIDATION C1:PENDING **T1_G3_V3**: PENDING_TRADE_VALIDATION C1:PENDING ** ** | **T1_G2_V2**: PENDING_TRADE_VALIDATION C1:PENDING | **N/A** |
| 2.2 | **T1_G1_V1**: PENDING_TRADE_VALIDATION C1: END....C291:END C292：PENDING C293：PENDING C294：PENDING **T1_G2_V2**: PENDING_TRADE_VALIDATION C1:PENDING **T1_G3_V3**: PENDING_TRADE_VALIDATION C1:PENDING ** ** | **T1_G2_V2**: PENDING_TRADE_VALIDATION C1:PENDING **T1_G3_V3**: PENDING_TRADE_VALIDATION C1:PENDING ** ** | **N/A** |
| 2.3 | **T1_G1_V1**: PENDING_TRADE_VALIDATION C1: END....C291:END C292：PENDING C293：PENDING C294：PENDING **T1_G2_V2**: PENDING_TRADE_VALIDATION C1:PENDING **T1_G3_V3**: PENDING_TRADE_VALIDATION C1:PENDING | **T1_G3_V3: **PENDING_TRADE_VALIDATION C1:PENDING | **N/A** |
| 3.1 | **T1_G1_V1**: PENDING_TRADE_VALIDATION C1: END....C291:END C292：PENDING C293：PENDING C294：PENDING **T1_G2_V2**: PENDING_TRADE_VALIDATION C1:PENDING **T1_G3_V3**: PENDING_TRADE_VALIDATION C1:PENDING | **T1_G1_V1**: PENDING_TRADE_VALIDATION C292：PENDING **T1_G2_V2**: PENDING_TRADE_VALIDATION C1:PENDING **T1_G3_V3**: PENDING_TRADE_VALIDATION C1:PENDING | **T1_G1_V1**: PENDING_TRADE_VALIDATION C292：END |
| 3.2 | **T1_G1_V1**: PENDING_TRADE_VALIDATION C1: END....C292:END C293：PENDING C294：PENDING **T1_G2_V2**: PENDING_TRADE_VALIDATION C1:PENDING **T1_G3_V3**: PENDING_TRADE_VALIDATION C1:PENDING ** ** | **T1_G1_V1**: PENDING_TRADE_VALIDATION C293：PENDING **T1_G2_V2**: PENDING_TRADE_VALIDATION C1:PENDING ** ** | **T1_G1_V1: **PENDING_TRADE_VALIDATION C293：END |
| 3.3 | **T1_G1_V1**: PENDING_TRADE_VALIDATION C1: END....C293:END C294：PENDING **T1_G2_V2**: PENDING_TRADE_VALIDATION C1:PENDING **T1_G3_V3**: PENDING_TRADE_VALIDATION C1:PENDING ** ** | **T1_G1_V1: **PENDING_TRADE_VALIDATION C294：PENDING **T1_G3_V3**: PENDING_TRADE_VALIDATION C1:PENDING | **T1_G1_V1:** COMPLETED C294：END |
| 4.1 | **T1_G2_V2**: PENDING_TRADE_VALIDATION C1:PENDING **T1_G3_V3**: PENDING_TRADE_VALIDATION & is_trade_validated=false C1:PENDING ** ** | **T1_G2_V2: **PENDING_TRADE_VALIDATION C1:PENDING | **T1_G2_V2:**COMPLETED C1:END |
| 4.2 | **T1_G2_V2**: PENDING_TRADE_VALIDATION C1:PENDING **T1_G3_V3**: PENDING_TRADE_VALIDATION & is_trade_validated=true C1:PENDING | **T1_G2_V2**: PENDING_TRADE_VALIDATION C1:PENDING | **T1_G2_V2**:COMPLETED C1:END **T1_G3_V3**:PENDING_TRADE_VALIDATION C1:END |
| 4.3 | **T1_G2_V2**: PENDING_TRADE_VALIDATION C1:PENDING **T1_G3_V3**:PENDING_PRE_GROUP & is_trade_validated=true C1:PENDING ** ** | **T1_G2_V2: **PENDING_TRADE_VALIDATION C1:PENDING | **T1_G2_V2**:COMPLETED C1:END **T1_G3_V3**:COMPLETED C1:END ** ** |
| 5.1 | **T1_G1_V1**: PENDING_TRADE_VALIDATION C11:PENDING **T2_G1_V1**:PENDING_PRE_GROUP C21:PENDING | **T1_G1_V1**: PENDING_TRADE_VALIDATION C11:PENDING **T2_G1_V1**:PENDING_PRE_GROUP C21:PENDING | **T1_G1_V1**:COMPLETED C11:END **T2_G1_V1**:COMPLETED C21:END |

# Test cases

| AC-No | Function | Scenario | Expected Result | test evidence |
| --- | --- | --- | --- | --- |
| 1 | Bulk manual deliver - partial stp cashflows in 1 group with same trade | 1. book C1,C2 cashflow which are same major version and cnt is 3 2. ops bulk manual deliver above 2 cashflows | 1. C1,C2 message status = 'PENDING', G1 group status = 'PENDING' 2. after bulk manual deliver 3. C1,C2 message status = 'END', G1 group status = 'COMPLETED', bookingSystemEvent = 'ManualDeliver' 4. C1,C2 flow to cashflow blotter | |
| 2 | Bulk manual deliver - all stp cashflows in 1 group with same trade | 1. book C1,C2cashflow which are same major version and cnt is 2 and trade state is Booked 2. ops bulk manual deliver above 3 cashflows | 1. C1,C2 message status = 'PENDING', G1 group status = 'PENDING_TRADE_VALIDATION' 2. after bulk manual deliver 3. C1,C2 message status = 'END', G1 group status = 'COMPLETED', bookingSystemEvent = 'ManualDeliver' 4. C1,C2 flow to cashflow blotter | uat6 tradeId: 4364000000 |
| 3 | Bulk manual deliver - stp cashflows in 2 group with same trade | 1. book C1 cashflow which major version is 1 and cnt is 2 and trade state is Booked 2. book C3 cashflow which major version is 2 and cnt is 2 and trade state is Booked 3. ops bulk manual deliver above 2 cashflows | 1. C1 message status = 'PENDING', G1 group status = 'PENDING' 2. C3 message status = 'PENDING', G2 group status = 'PENDING' 3. after bulk manual deliver 4. C1, C3 message status='END', G1&G2 group status='COMPLETED' | |
| 4 | Bulk manual deliver - stp cashflows in 2 group with same trade | 1. book C1,C2 cashflow which major version is 1 and cnt is 2 and trade state is Booked 2. book C3 cashflow which major version is 2 and cnt is 2 and trade state is Booked 3. ops bulk manual deliver above 3 cashflows | 1. C1,C2 message status = 'PENDING', G1 group status = 'PENDING_TRADE_VALIDATION' 2. C3 message status = 'PENDING', G2 group status = 'PENDING' 3. after bulk manual deliver 4. C1,C2,C3 message status = 'END', G1 group status = 'COMPLETED', G2 group status = 'COMPLETED', bookingSystemEvent = 'ManualDeliver' 5. C1,C2,C3 flow to cashflow blotter | |
| 5 | | 1. book C1,C2 cashflow which major version is 1 and cnt is 2 and trade state is Booked 2. book C3,C4 cashflow which major version is 2 and cnt is 2 and trade state is Booked 3. ops bulk manual deliver above 3 cashflows | 1. C1,C2 message status = 'PENDING', G1 group status = 'PENDING_TRADE_VALIDATION' 2. C3,C4 message status = 'PENDING', G2 group status = 'PENDING_PRE_GROUP' 3. after bulk manual deliver 4. C1,C2,C3,C4 message status = 'END', G1 group status = 'COMPLETED', G2 group status = 'COMPLETED', bookingSystemEvent = 'ManualDeliver' 5. C1,C2,C3,C4 flow to cashflow blotter | |
| 6 | Bulk manual deliver - stp cashflows in 3 group with same trade | 1. book C1(New),C2 cashflow which major version is 1 and cnt is 2 and trade state is Booked 2. book C1(Withdrawal) cashflow which major version is 2 and cnt is 1 and trade state is Booked 3. book C3,C4 cashflow which major version is 3 and cnt is 2 and trade state is Booked 4. ops bulk manual deliver above C2,C3 cashflows | 1. C1,C2 message status = 'PENDING', G1 group status = 'PENDING_TRADE_VALIDATION' 2. C1 message status = 'OFFSET',G2 group status = 'COMPLETED' 3. C3,C4 message status = 'PENDING', G3 group status = 'PENDING_PRE_GROUP' 4. after bulk manual deliver 5. C2,C3,C4 message status = 'END', G1 group status = 'COMPLETED', G3 group status = 'PENDING_TRADE_VALIDATION', bookingSystemEvent = 'ManualDeliver' 6. C2,C3,C4 flow to cashflow blotter | |

ops