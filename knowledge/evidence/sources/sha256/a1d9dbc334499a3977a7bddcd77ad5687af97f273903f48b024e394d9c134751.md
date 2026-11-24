## **BPMS Existing Flow/Feature Operational Readiness Questionnaire**

## 1. SNOW (ServiceNow Change Management)

*Ensure the Change Request (CR) is accurately documented and approved in ServiceNow.*

| Question / Checklist | Requirements / Notes | Response / Evidence |
| --- | --- | --- |
| **Change Scope** | - List all ADO work items related to this change(User Story/Bug/Task), Links only | [Story 14193672 [ISO] 2026 4a Go-Live - SG](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14193672) |
| **Justification** | - ** Existing Flow/Enhancement:** Provide details of involved flow/feature and the change. - ** Issue Fixing:** Provide the issue nature, fix details | As 4a go live plan, MX bifurcation need to be enhanced for SG. |
| **Change Test Sign-off** | - Provide evidence link/attachment or N/A with reason 1). Functional Test Evidence 2). Regression Test Evidence 3). Performance Test Evidence 4). UAT Sign-off 5). DR Test Evidence | ![image-2026-7-22_10-32-16.png](attachments/image-2026-7-22_10-32-16.png) |
| **UVT plan** | - List details of UVT plan | Follow ISO project team runbook |
| **Rollback plan** | - List details of rollback plan | ADO rollback stage |
| **Change Scheduling** | - Any downtime outside greenzone needs to have **BO's approval** (Attached to Justification Attachment). | 26/07/2026 |
| **PSS Resource Booking** | - PSS resource booked via <u>[BPMS Application Release Timeslot Booking - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Application+Release+Timeslot+Booking)</u> - Duration: **2 hours maximum** for each CR (including both implementation and verification). | 09:00~10:00 |
| **Safe Change Attestations** | - Safe/Not Safe | Safe |

---

##

## 2. SAFE change checklist

| Key Checks | Description | Is the change compliant with "SAFE" criteria - YES/NO/NA |
| --- | --- | --- |
| **No deletions / Amendments ** | **Implies** : Change that does not delete or amend existing database/data/systems **Target** : Immutable infrastructure and non-destructive rollouts | - [x] YES - [ ] NO - [ ] N/A |
| **Backward compatibility** | **Implies** : Change should be backward compatible to ensure that newer systems, software, or devices can seamlessly work with older versions or legacy data **Target** : Upgrade won't "break" existing tools, seamless upgrades, phased migrations, preventing sudden disruptions | - [x] YES - [ ] NO - [ ] N/A |
| **Automated System restarts ** | **Implies **: Were its relevant system restarts are fully automated (application shuts down and boots back ) with minimal manual intervention for faster uptimes **Target** : Routine Maintenance, Systems updates , crash recovery etc. where a device, server, or software application shuts down and boots back up entirely on its own. | - [x] YES - [ ] NO - [ ] N/A |
| **Automated Change Rollback** | **Implies** : As part of rollback plan a change should encompass automated change rollback to it’s a previous stable state with minimal manual intervention **Target** : Robust pre-deployment practices, database backward compatibility, documented runbooks, rigorous testing to support automated rollback | - [x] YES - [ ] NO - [ ] N/A |
| **Rigorous Testing** **(within the remit of the change and its dependencies)** | **Implies **: Validating new code, infrastructure, or configurations in a safe, isolated/lower/non-prod/pre-pod environment to prevents bugs, security vulnerabilities, and system outages in production **Target **: Testing systems through phased environments, automated testing, and defined operational readiness gates to ensure successful deployment | - [x] YES - [ ] NO - [ ] N/A |
| **Change Impact assessment (CIA)** **(within the remit of the change and its dependencies)** | **Implies** : Change impact assessment in terms of how the deployment will have a cascading impact to the technical infrastructures, business operations and client journeys - both positive and negative—of deploying new software, hardware, or system updates **Target **: Review dependency mapping, tested rollout and backout plans, updated runbooks and supportability to evaluate the technical, operational, and user-facing effects of a deployment | - [x] YES - [ ] NO - [ ] N/A |
| **Automated deployment** | **Implies** : Using ADO for automated pipeline deployment or in certain cases using tools and scripts to automatically push software, hardware, or system updates from development into production, minimizing manual deployments **Target : **Shift from manual to automated workflows that allow support to deploy changes safely and autonomously by automating the change lifecycle, risk-based routing, automated testing and validation | - [x] YES - [ ] NO - [ ] N/A |
| **Eliminate/Minimize Outage** | **Implies **: Deployment through a structured implementation plan to prevent, minimize, or eliminate system downtime **Target :** Comprehensive risk assessment, dependency mapping, pre-testing ,blue-green deployment or use canary release by leveraging automation and observability to reduce or eliminate downtime | - [x] YES - [ ] NO - [ ] N/A |
| **Change Risk assessment (CRA)** **(within the remit of the change and its dependencies)** | **Implies **: Change assessment to identify, analyze, and mitigate potential risks/hazards before implementing a change **Target :** Define the scope, identify potential impact, analyze potential threats to operations, evaluate the likelihood and impact, and establish robust mitigation and rollback plans | - [x] YES - [ ] NO - [ ] N/A |
| **Change Dependencies** | **Implies **: Change scope mapping of which software, hardware, upstream and downstream applications and journeys are within the scope of deployment and impact **Target **: integrate mapping directly into your CI/CD pipelines, adopt CMDB mapping to ensure right scoping and impact radius | - [x] YES - [ ] NO - [ ] N/A |
| **Change deployment timelines are been coordinated** **(Cross domain Muti-support deployment)** | **Implies : **Aligning the technical rollouts with support staff and synchronizing system updates, to ensure smooth deployment **Target :** Aligning technical milestones with cross-functional readiness through a centralized review framework, automated deployment pipelines and structured communication | - [x] YES - [ ] NO - [ ] N/A |
| **Change Communication** | **Implies :** Pre/During/Post communication - transparently explaining the why (benefits), the what (about) and How (progress of deployment) **Target **: Phased communication plan, communicating pre-planning, timelines, outcome and during deployment milestone progress updates | - [x] YES - [ ] NO - [ ] N/A |

---

## ✅ Approval & Sign-off

| Role | Name | Signature / Date | Comments |
| --- | --- | --- | --- |
| **DEV Lead** | | | |
| **PSS Manager** | | | |

---

*Last Updated: [Insert Date]* | *Owner: [Insert Name]*