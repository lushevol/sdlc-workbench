**EXPAND: 1: Introduction**

Below the business overview diagrams describes the core business capability of Ratan platform, in next sections the performance testing case design will focus on the core business capability.

Here is the logic architecture of Ratan platform, describes the core domain business services and surrounding systems.

**EXPAND_END**

**EXPAND: 2: Purpose**

Currently there are 6 VM nodes and 2 Database nodes in Ratan Prod environment, the 6 VMs consisted a active/active cluster cross 2 DCs, all of Ratan 's business services and infra & common service are mixed deployed together, sharing the limited VM resource,  with the business growth, there will be the **"resource shortage**" problem, meanwhile all service are tightly couple together, it is very difficult for "**fault isolation**", caused the risk for system stability.

In order to resolve the "resource shortage" problem, meanwhile isolate infra and business service, to ensure all business line be able to independently evaluate, Ratan plan to upgrade the PRDO deployment architecture to the new strategic deployment architecture 2025. the link: <u>**[https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3223270204](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3223270204)**</u>

Since in this change there are new **6 VMs** have been **added**, and all of Ratan's microservices have been **re-orchestrated,** some related application configuration have been adjusted to apply the new architecture. all of the changes bring the pentation risk of Ratan's service capability.

According to above awareness, before we update the new deployment in PROD environment, it is necessary to make a Ratan platform scope performance testing to assess if this deployment architecture upgrade lower the service capability, to ensure the stability of Ratan Prod.

The **testing type** for this are:

- **peak load test**: to evaluate the system performance under expected peak load conditions.
- **Stress test **to evaluate the system performance and analyze the bottleneck by running under stress conditions, with transaction loading in 200%,400%,600% and 800% when the system shows the bottleneck of no-longer meet the performance target
- **endurance test**: to check whether the software application can withstand the expected system load for a long time.

The **acceptance criteria** of this performance testing are:

- all case flow 's service processing capability not lower than before deployment upgrade (if there is previous baseline data to compare)
- (or) key stakeholder believe the performance be able to meet the business requirement.

**EXPAND_END**

**EXPAND: 3: NFR and Volumetrics**

The volume for testing follows the figures documented on SLM & Capacity Requirements of RATAN NFR document  [RATAN - 51358 - Global - Non Functional Requirements - System Delivery Framework - Confluence](https://confluence.global.standardchartered.com/display/SDF/RATAN+-+51358+-+Global+-+Non+Functional+Requirements)

**EXPAND_END**

**EXPAND: 3: Environment Introduction**

### 3.1: Deployment

Here this section describes the performance testing environment, according to the ***<u>[Ratan New Deployment diagram v51](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3223270204)</u>***, we setup 14 VM servers in Ratan staging environment, and separated them to 4 groups:

- **Cashflow Settlement Service Group**: dedicated serve for cashflow settlement business line, including 【vm-1(uklvadrat0001a), vm-2(uklvadrat0002a), vm-8(uklvadrat0006a), vm-9(uklvadrat0005a)】.
- **Trade Control Service Group**: dedicated serve for trade control business line, including 【vm-3(uklvadrat0003a), vm-10(uklvadrat0004a)】.
- **Infra & Common Service Group**: dedicated serve for infra and common service, including 【vm-4(uklvadrtn002a), vm-5(uklvadrtn004a),vm-6(uklvadrtn006a), vm-11(uklvadrtn003a),vm-12(uklvadrtn005a), vm-13(uklvadrtn007a)】.
- **Database Server Group**: dedicated serve for PostgreSQL server, including 【vm-7, vm-14】.

### 3.2: VM Specification

Here is the specification of above 14 staging VM servers

| Hostname | Type | IP Address | Env | System Model | Processor Clock Rate(MHz) | Cores | Processor Model | System Description | Memory Configured (GB) | DC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| uklvadrtn002a | App-X86 | 10.198.22.29 | Pre-Prod | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 8.10 | 128 | ARK |
| uklvadrtn003a | App-X86 | 10.198.22.30 | Pre-Prod | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 8.10 | 128 | ARK |
| uklvadrtn004a | App-X86 | 10.198.22.31 | Pre-Prod | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 8.10 | 128 | ARK |
| uklvadrtn005a | App-X86 | 10.198.22.32 | Pre-Prod | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 8.10 | 128 | ARK |
| uklvadrtn006a | App-X86 | 10.198.22.39 | Pre-Prod | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 8.10 | 128 | ARK |
| uklvadrtn007a | App-X86 | 10.198.22.40 | Pre-Prod | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 8.10 | 128 | ARK |
| uklvaddbs097 | App-X86 | 10.198.194.212 | Pre-Prod | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 8.10 | 64 | ARK |
| uklvadrat0001a | App-X86 | 10.198.23.31 | Pre-Prod | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 8.10 | 128 | ARK |
| uklvadrat0002a | App-X86 | 10.198.23.32 | Pre-Prod | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 8.10 | 128 | ARK |
| uklvadrat0003a | App-X86 | 10.198.23.33 | Pre-Prod | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 8.10 | 128 | ARK |
| uklvadrat0004a | App-X86 | 10.198.23.34 | Pre-Prod | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 8.10 | 128 | ARK |
| uklvadrat0005a | App-X86 | 10.198.23.35 | Pre-Prod | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 8.10 | 128 | ARK |
| uklvadrat0006a | App-X86 | 10.198.23.36 | Pre-Prod | VMware Virtual Platform | 2194 | 16 | Intel(R) Xeon(R) | RHEL Server release 8.10 | 128 | ARK |

**The capacity of PT environments are more or less the same as production environment, so we don't expect big difference between production environment and PT environment**

**EXPAND_END**

**EXPAND: 4: Test Case Definition**

According to *[Ratan Performance Testing Guideline v.24](https://confluence.global.standardchartered.com/display/DSP/Ratan+Performance+Testing+Guideline), *meanwhile consider of our purpose of this testing, we designed below cases carefully, they are the core cases for each business line, and we involved the GUI case to assess the user using experience during different system loading.  Below is the overview diagram of case definition:

For the detailed *<u>[case definition](https://confluence.global.standardchartered.com/display/DSP/Case+Definition)</u>**<u> </u>*please reference to bellow list:

- **Cash Settlement Business Line:** <u> *[sett-murex](https://confluence.global.standardchartered.com/display/DSP/sett-murex)*</u>, *<u>[sett-stella](https://confluence.global.standardchartered.com/display/DSP/sett-stella)</u>*, *<u>[sett-suspended](https://confluence.global.standardchartered.com/display/DSP/sett-suspended)</u>*, *<u>[bau-new](https://confluence.global.standardchartered.com/display/DSP/bau-new)</u>*
- **Trade Control Business Line**: *[<u>trade-murex</u>](https://confluence.global.standardchartered.com/display/DSP/trade-murex)*, *<u>[trade-fmrp](https://confluence.global.standardchartered.com/display/DSP/trade-fmrp)</u>*
- **FMO GUI**: *<u>[user-e2e-test-case](https://confluence.global.standardchartered.com/display/DSP/user-e2e-test-case)</u>*

**EXPAND_END**

**EXPAND: 5: Execution and Plan**

### 5.1: Execution Overview

- all test cases running in parallelly
- leveraging python script to generate backend test traffic data, mainly for Kafka message
- leveraging JMeter to simulate user invoking core APIs
- monitoring the whole test flow via Ratan Central Monitoring system and ELK
- increase the performance testing pressure from low to high (from 1x to nX)
- clear up testing data and reset testing environment once testing is completed

### 5.2: Test Plan

In this table we defined the expected/planed time for this testing activity:

| Traffic Volume | Start time | End time | Duration |
| --- | --- | --- | --- |
| 1X | 2026-03-18 20:25:00 SGT | 2026-03-18 21:25:00 SGT | 1 hr |
| 2X | 2026-03-19 07:40:00 SGT | 2026-03-19 08:40:00 SGT | 1 hr |
| 4X | 2026-03-19 19:00:00 SGT | 2026-03-19 20:00:00 SGT | 1 hr |
| 6X | 2026-03-19 23:15:00 SGT | 2026-03-20 00:15:00 SGT | 1 hr |
| 8h | 2026-03-18 21:50:00 SGT | 2026-03-19 05:50:00 SGT | 8h |

**EXPAND_END**