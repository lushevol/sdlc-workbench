![image-2026-7-3_14-34-38.png](attachments/image-2026-7-3_14-34-38.png)

**        1. Orchestration service：**

a. parse cashflow scbml to get cashflowId、businessVersion

b. call lifecycle api to get  STP / NSTP information、lastUser

c. update publish topic function（LOANIQ cashflow send to message-bridge and Fmrp cashflow send to swift service） to add message header "X-Outbound-Property-"

**        2. Lifecycle service：**

a. provide a internal api to support get STP / NSTP information、lastUser function

**        3. Swift service：**

a. topic consumer recevice message header

b. add MT/MX message header

**        4. Query service:**

a. query/save function support USD equivalent

**        5. Netting service**

a. provide a internal api to support query parent cashflow by splittingId