# Quick search

Cashflowid / trade id ---pass

trade original id — by pass

Value date must be mandatory

Value date + booking entity fmid / booking entity fmcode --pass

Value date + counterparty fmid / counterparty fmcode --pass

Neither booking entity or counterparty -- refuse

Add Cashflow State into quick search, support multiple search, there is no validation about this field

# Custom Filter

Any field end with "_id" in filter ---by pass

Payment date + booking entity fmid + cashflow state -- pass

Operator only support (= , in, bet, <=, >= )  for payment date

Operator only support (=, in ) for booking entity fmid and cashflow state

# Behavior of Custom Filter

User select and open filter only validation and pop msg if failed and still can see that filter

Do not allow user save/create/search validation failed filter

Allow user delete filter anyway, keep same

# Search Bar

Disable search bar

When query search or filter need clear search bar

# Query Amount

Re-enabled now,

1) clicking to navigate to the detailed cashflows along with button highlighted

2) re-click to disable

**Add Cashflow Sub State into Quick Search after confirm with user.**
**Right Top Value Today high light after user click and allow user re-click it to cancel this quer**

1. **<u> By Default </u>**
2. **<u> Navigated </u>**