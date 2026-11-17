# Backgroup & Purpose

1. There are some data inconsistant when below case a. first generate **accounting **info and status in HOLD b. then nostro refreshed c. finally time reached will send **accounting **info

# Services Involved

# Changing in ratan-cash-settlement-accounting-service

# Q&A

| | question | answer | comment |
| --- | --- | --- | --- |
| 1 | when will we put ebbsAccountNum when below case: 1.fail→generate task 1 in hold // **old** nostro 2.reinstate→generate task 2 in hold // **old** nostro 3.nostro refresh 4.fail→generate task 1 in hold // new nostro 5.reinstate→generate task 2 in hold // new nostro 6.time reached will send to downstream | all task need re-genereate partial requestion info related nostro, then send | |
| 2 | 1.c1+c2 net c3 2.release c3 in HOLD // old nostro1 3.withdrawal c1 and released in HOLD // old nostro1 4.nostro refresh 5.day reach 6.send c3 // new nostro2? 7.send c1 // new nostro2? | | |