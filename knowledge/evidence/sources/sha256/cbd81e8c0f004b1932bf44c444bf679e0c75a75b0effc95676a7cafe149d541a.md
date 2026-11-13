# 1、Background

- There is a business requirement about Cashflow Auto Netting, (Detailed could refer to [Cashflow Auto Netting - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Cashflow+Auto+Netting)), in this scenario, it requires API high performance.
- There are many steps in the update cashflow status API, which is complex. In other words, it contains many business logic, but not all seems related to status changed.
- It had already occurred some prod issues as the long execution time of the update cashflow status API.

In order to keep the API more reasonable and easy maintenance, we need to refactor it.

# 2、Analysis

## 2.1 What is Cashflow Netting

User combines two or more cashflows to generate a new cashflow, which is called resultant cashflow, the combined cashflows are called component cashflows.

Then the resultant cashflow will flows until settled, those component cashflows will stop flowing. That means component cashflow's status will be updated to netted, and don't change anymore.

## 2.2 Current Netting API

Current Logical Summary:

1. prepare cashflow net request
2. update cashflows status
3. save cashflow net request

Maybe you have a question** ——When and Where the resultant cashflow is generated? **

**EXPAND: current net flow diagram**

PS: trigger resultant cashflow to flow, that means publish the scbml into the **Cash_Settlement_Orchestration_Process_In **topic(activate the workflow).

**EXPAND_END**

**EXPAND: net sequence diagram**

**EXPAND_END**

From above process, we get the answer **—— The resultant cashflow is generated in the update cashflow status API.**

Updating cashflow status and generating the resultant cashflow, two kinds of things, are in a same API. ** Is it reasonable?**

Do you remember the Single Responsibility Principle （**SRP**)?

## 2.3 Current Updating Cashflow Status API

Let's take an in-depth look at the logic of this API.

**EXPAND: current update cashflow status process**

**EXPAND_END**

From above process, you may find something as below:

1. It has many steps to update cashflow status. It seems that many business logic apart from updating cashflow status.
2. It's a big transaction, and seems that some steps aren't needed in it.
3. The developer has to read the whole logic to understand what happens when the cashflow status changed from X to Y.
4. The developer must do the full regression test when adjusting the existing logic or adding new logic.

**Is it reasonable?**

## 2.4 Responsibility

Now, we find some unreasonable things in the updating status API, but what's that?

Before answer it, let's review some principles of software development.

### 2.4.1 Principle of Software Development

**EXPAND: Principle Detail**

| # | Principle | **Comment** |
| --- | --- | --- |
| 1 | Single Responsibility Principle (SRP) | - Each module, class, or function should have a single, well-defined responsibility - Avoid mixing multiple concerns within a single unit of code - Facilitate understanding, testing, and maintenance of the codebase |
| 2 | Open-Closed Principle (OCP) | - Software entities should be open for extension but closed for modification - Encourage the use of abstractions and interfaces to enable extensibility - Minimize the impact of changes on existing code |
| 3 | Keep It Simple, Stupid (KISS) | - Strive for simplicity in design and implementation - Avoid unnecessary complexity that can hinder understanding and maintainability - Focus on creating [clean, readable, and concise code](https://fullscale.io/blog/write-efficient-code/) |
| 4 | Dependency Inversion Principle (DIP) | - High-level modules should depend on abstractions, not concrete implementations - Invert the dependency flow to make code more flexible and testable - Utilize dependency injection and interfaces to decouple modules |
| 5 | Least Knowledge Principle (LKP) (The Law of Demeter-LoDP) | It states that an object should have only limited knowledge of other objects, and should interact with them through well defined interfaces. In other words, a software entity should have as little interaction as possible with other entities. This helps to reduce the coupling between different parts of a system, making it more modular, maintainable, and less prone to errors when changes are made. |
| 6 | You Aren’t Gonna Need It (YAGNI) | Implement features that are currently required and avoid over-engineering - Resist the temptation to add unnecessary functionality that may never be used - Focus on delivering value incrementally and iteratively |
| 7 | Liskov Substitution Principle (LSP) | - Subtypes should be substitutable for their base types without affecting correctness - Ensure that derived classes adhere to the contract of their parent classes - Maintain behavioral consistency and avoid unexpected side effects |
| 8 | Don’t Repeat Yourself (DRY) | - Eliminate redundancy in code and processes - Promote [code reuse](https://www.sciencedirect.com/topics/computer-science/code-reuse) and modular design to improve efficiency and reduce errors - Centralize common functionalities and avoid duplicatio |
| 9 | Interface Segregation Principle (ISP) | - Clients should not be forced to depend on [interfaces](https://www.indeed.com/career-advice/career-development/what-are-interfaces) they do not use - Split large interfaces into smaller, more specific ones - Promote loose coupling and improve modularity |
| 10 | Separation of Concerns Principle (SCP) | - Divide software into distinct, independent modules or components - Each module should have a clear responsibility and minimal overlap with others - Promote loose coupling and high cohesion for maintainability and [scalability](https://fullscale.io/blog/vertical-vs-horizontal-scaling/) |
| 11 | Modularity Principle (MP) | - Design software as a collection of interchangeable, reusable modules - Encapsulate related functionalities into self-contained units - Enable easy modification, testing, and replacement of individual modules |

**EXPAND_END**

**We can find that the updating status API is not followed at least five principles: SRP、OCP、KISS、DIP、LKP.**

### 2.4.2 Responsibility Analysis

| Service | Responsibility | Comment |
| --- | --- | --- |
| lifecycle service | 1. initialize cashflow stella message event ( when consuming the topic Cash_Settlement_Orchestration_Process_In message） 2. maintain cashflow status (change the cashflow's status from X to Y) | 1. lifecycle means one cashflow from generation to completion (0→1, 1→ 100) 2. the stella message event is the cashflow main data. in other words, it is used in every state change. |
| netting service | All cashflow net logic. 1. net 2. unnet 3. manage the component cashflow status (if need) 4. net rule check 5. renet 6. ..... | It's the entry point of the cashflow netting because it manages the relationship between resultant and component cashflow, |

# 3、Refactor

Base on above analysis, we can refactor cashflow net process.

## 3.1 New APIs

Base on the service responsibility, we define the new APIs as below table.

| Service | Function | Responsibility | Comment |
| --- | --- | --- | --- |
| Lifecycle Service | updateStatus | change the cashflow's status from X to Y | |
| initializeCashflow | generate a new cashflow stella message event. | |
| Netting Service | net | 1. net cashflow to generate a resultant cashflow 2. update component cashflow's status | manual and auto netting. |
| unnet | 1. unnet a resultant cashflow 2. update component cashflow's status | manual unnet. |
| manageComponentCashflowStatus | consume domain event to update component cashflow's status if need | when the resultant cashflow's status is changed released/settled. topic: cash_settlement_cashflow_domain_events |
| netRuleCheck | check one cashflow is matched netting rules or not. | |
| renet | find uncompleted cashflow net requests to re-generate resultant cashflow | |

## 3.2 The New Update Cashflow Status API

**EXPAND: refactor update cashflow status process**

**Principle：different action has different behavior (template mode).  That makes the logic Clearly、Understandable and Easy Maintenance.**

**EXPAND_END**

**EXPAND: Class Diagram**

**EXPAND_END**

## 3.4 Manage Component Cashflow Status

# 4、Roadmap

| date | content | comment |
| --- | --- | --- |
| 2025.5 | analysis+redefine+implement Net/NetNew/RevertToQueue action | |
| 2025.6 | implement most of action except new/withdrawal action | |
| 2025.7 | implement new/withdrawal action think how to support uber? | |
| 2025.8 | migrate some action to new api | |
| 2025.9 | migrate other actions to new api | migrate done. all actions use new implemention. |
| 2025.10 | adaptor cash settlement | |
| | | |

# 5、Open Questions

| # | Description | Comment |
| --- | --- | --- |
| 1 | Why is generating a resultant cashflow after updating cashflow status? | |
| 2 | Can generating a resultant cashflow is before updating cashflow status? | |
| 3 | How to unet resultant cashflow? | |