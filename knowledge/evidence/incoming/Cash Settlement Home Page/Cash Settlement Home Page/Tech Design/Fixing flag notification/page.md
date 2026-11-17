Lein Tech Design:  [LIEN Processing & Pending Fixing Flag Technical Design]

requirement: [IRS Fix Leg & Floating leg payment handling - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2726685251)

NAS folder :

/apps/ratannas/murex_ratan_transfer/fixing/ack

/apps/ratannas/murex_ratan_transfer/fixing/payment

/apps/ratannas/murex_ratan_transfer/fixing/payment/Done

/apps/ratannas/murex_ratan_transfer/fixing/payment/Error

Need to confirm

naming convention

content

ack/nack

Latest solution

Lifecycle workflow

Changes

| Service Name | |
| --- | --- |
| Batch Service | 1. Processing new folder 2. Validation 3. Sending notification to Kafka |
| Lifecycle Service | 1. Consume batch file notification 2. Persist original notification (batch & real-time) 3. If cashflow cancelled then do nothing, else force setting fixing flag and revert cashflow to queued to reprocessing |
| Netting Service | IRS check API, check if is it match waiting fixing flag rule |

case1 - couples notifications as flag changes

t1, C1 with flag X send to ratan,   C1 is PendingFixing

t2. C1 notification with flag Y send to ratan,  C1 is WaitingAnotherLeg

t3. C1 notification with flag N send to ratan,  C1 is not waitingAnotherLeg

case2 - notification come first

t1. C1 with notification Y send to ratan

t2. C1 with flag  X send to ratan

t3. C1 is waitingAnotherLeg

case3 - withdrawal

t1. C1 with flag X send to ratan, C1 is PendingFixing

t2. C1 withdrawal send to ratan

t3 C1 notification with flag send to ratan

t4. C1 is  still cancelled but flag changed,  GUI can see the latest flag

case4 - failed or techfailed

t1. C1 with flag X send to ratan, C1 is pendingFixing

t2. C1 get failed or techfailed

t3. C1 notification with flag Y send to ratan

T4. C1 reinstate and stamped as Y

case5 -  cashflow & notification the same time

t1. C1 with flag X send to ratan

C1 notification send to ratan with flag Y

t2. C1 is waitingAnotherLeg