# Brief Introduce Demand

when cashflows meet one Nostro Threshold Staitc data, RATAN system will **split **this cashflow into some **child** cashflows, relevant UI are as follows
![image-2026-1-29_17-20-11.png](attachments/image-2026-1-29_17-20-11.png)
![image-2026-1-29_17-20-29.png](attachments/image-2026-1-29_17-20-29.png)

static data from **RAZOR**
![image-2025-11-24_20-48-45.png](attachments/image-2025-11-24_20-48-45.png)
more detail can refer:

# Brief Workflow Involving

# Introduce Split Algorithm

![image-2026-1-29_17-37-0.png](attachments/image-2026-1-29_17-37-0.png)![image-2026-1-29_17-37-6.png](attachments/image-2026-1-29_17-37-6.png)
like above **sample **data and **major **algorithm from **RAZOR**

**1. Formula** and limitation:
**accDeductAmount**=accDeductAmount+decutAmunt, **xchild**: threashold-accDeductAmount, **restAmount**=restAmount-xchild
...
skip child when every ten times
at last child, if duplicated will split to restAmount-deductAmount and deductAmount
when xchild less or equal than limitation will shrink deductAmount=deductAmount/10, continue split as above

2. **Sample**:
user **config **some static data:
threashold=80,000,000
deductAmount=200,000
limitation=60,000,000

case **one**:  when coming cashflow amount **100,000,000**
since 100,000,000>80,000,000, we will **split **it 
first child:  80,000,000-200,000=79,800,000, leftAmount=100,000,000-79,800,000=20,200,000
second child: 20,200,000(since 20,200,000<100,000,000 do not need split further)

case **two**:  when coming cashflow amount **554,800,000**
since 554,800,000>80,000,000, we will **split **it 
first child:  80,000,000-200,000=**79,800,000**, leftAmount=554,800,000-79,800,000=475,000,000
second child: 80,000,000-200,000-200,000=**79,600,000**, leftAmount=475,000,000-79,600,000=395,400,000
third child: 80,000,000-200,000-200,000-200,000=**79,400,000**, leftAmount=395,400,000-79,400,000=316,000,000
fouth child: 80,000,000-200,000-200,000-200,000-200,000=**79,200,000**, leftAmount=316,000,000-79,200,000=236,800,000
fifth child: 80,000,000-200,000-200,000-200,000-200,000-200,000=79,000,000, leftAmount=236,800,000-79,000,000=157,800,000
sixth child: 80,000,000-200,000-200,000-200,000-200,000-200,000-200,000=**78,800,000**, leftAmount=157,800,000-78,800,000=79,000,000(already **less** than threashold=80,000,000 but **duplicated **previous child)
seventh and eighth child(): 79,000,000-200,000/10=78,980,000 and 200,000

case **three**:  when coming cashflow amount **7,389,700,000**
since 7,389,700,000>80,000,000, we will **split **it 
first child:  80,000,000-200,000=**79,800,000**, leftAmount=7,389,700,000-79,800,000=7,309,900,000
second child: 80,000,000-200,000-200,000=**79,600,000**, leftAmount=7,309,900,000-79,600,000=7,230,300,000
third child: 80,000,000-200,000-200,000-200,000=**79,400,000**, leftAmount=7,230,300,000-79,400,000=7,150,900,000
fouth child: 80,000,000-200,000-200,000-200,000-200,000=**79,200,000**, leftAmount=7,150,900,000-79,200,000=7,071,700,000
fifth child: 80,000,000-200,000-200,000-200,000-200,000-200,000=**79,000,000**, leftAmount=7,071,700,000-79,000,000=6,992,700,000
sixth child: 80,000,000-200,000-200,000-200,000-200,000-200,000-200,000=**78,800,000**, leftAmount=6,992,700,000-78,800,000=6,913,900,000
...
tenth child: 80,000,000-200,000-200,000-200,000-200,000-200,000-200,000=**~~78,000,000~~**(since algorithm from **RAZOR** need **skip** splited child every ten times, we also will **keep** this)
...
some child meet case: 60000000, first skip for ten times, then got 59,800,000 which less or equal than Limitation=60000000, then **shrink** deductAmount=deductAmount/10,
then **continue **above logic, child=80000000-newDeductAmount

# Potential Issue

from above formula and sample data analyzed basically from **RAZOR **already practiced**,** but in case any unkonw issues at split processing,
so we **add** one **logic** to break down infinite splitting: when deductAmount is **less than** 1 we will **throw** exceptionas
then we will **move** this cashflow status to "**READY**+NA+Pending_Exception" using action=**AutoSplitFail**
then the expectation for user is
1). to **rectify **the nostro static threashold static config
2). then do manuailFail+reinstate to recover 

above case can cover **major **case, **but **we still have **one **case do not cover:
if cashflow status is in "**READY**+NA+Pending_Exception", then come one **withdraw** message, which will lead this withdrawal cashflow **lost**, since currently system **cannot** support move status

# Solution

base on above anlayzed, we will fix this **potential **issue using action=**TechFail** rather than** AutoSplitFail**, some reasons as follows:
a. since the action=**AutoSplitFail** is a **new **created status and **do not** be used or affect any other system,
b. if we choice to enhance action=**AutoSplitFail** and relevant result, maybe will **introduce** many other actions and need efforts
c. and our system **already **support action=**TechFail** in prod relevant mature,
d. so we want to **reuse **this action and behaviour which user already **familiar** with to resolve this case keep as-is in prod, also we **enhance** the TechFail behavour adding **comment, **result as bellow

![image-2026-2-1_11-56-17.png](attachments/image-2026-2-1_11-56-17.png)