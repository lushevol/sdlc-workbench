> **INFO**
> To increase even more of the settlement STP rate, we are building the capability of automating cashflow affirmation process
>
> 1. enable cashflow affirmation automated by email to client
> 2. to drive the auto settlement process with the response from AI factory layer

# Email Integration (Outbound Flow)

In user daily BAU, they are collecting mandatory cashflow details, drafting in email then send to client, in order to on behalf of user to automate email, we need to build the capacity of doing the same thing. Key points are

1. mandatory cashflow details (need to confirm)
2. timing of sending email per country
3. Distribution audit 1. Timing that sent to CDUPS 2. Timing that email sent to Client from CDUPS
4. etc.

#### #1. Mandatory Cashflow Detail (to be confirmed with business)

| Email Field Name | Mandatory (Y/N) | Description | User Email Sample |
| --- | --- | --- | --- |
| Trade ID | Y | for Gross cashflow, value is parent trade id, for netted resultant cashflow, value is **Net** | |
| FlowID | Y | cashflow id |
| Entity | N | cashflow booking entity name, could be blank for net resultant |
| Value Date | Y | value date |
| Counterpart | Y | counterparty name, could be blank for net resultant |
| Cur | Y | currency |
| Amount | Y | credit / debit, SCB pay will be less than zero (-12,270.00), SCB receive will be greater than zero (12,270.00) |
| SCB Pay / Receive | Y | SCB Pay / SCB Receive |
| Taxonomy | N | optional for resultant cashflow |
| Portfolio | N | optional for resultant cashflow |
| Strategy | N | |
| Bene_AC | N | |
| Bene_Agent | N | |
| Bene_Int | N | |

#### #3. Email Integration

As per architect, we'll leverage CDUPS existing email distribution capability, referring to <u>[Outbound Affirmation Emails - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/display/FMRP/Outbound+Affirmation+Emails)</u>

1. NFRs: to be confirmed by PO
2. Connection protocol: Solace
3. Distribution ack/nack

#### #4. RATAN Workflow

TBU

**EXPAND: Affirmation Integration (Inbound Flow) -- Draft**

# Automated Affirmation Integration (Inbound Flow)

**EXPAND_END**