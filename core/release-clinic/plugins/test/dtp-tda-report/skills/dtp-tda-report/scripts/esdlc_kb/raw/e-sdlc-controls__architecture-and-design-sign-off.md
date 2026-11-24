# Controls: Architecture and Design Sign-off

---

## Control Attributes

| **Control Name** | Architecture and Design Sign-off |
| --- | --- |
| **L3 Risk Taxonomy** | Technology Change |
| **Control Objective** | Solution Architecture and Solution Design of IT Solutions are developed and agreed and cover requirements for - security, - resilience, - stability, and - business viability. Solution Architecture and Solution Design of IT Solutions are aligned to the bank's<br/>- Technology Strategy,<br/>- Enterprise Architecture Principles, and<br/>- Architecture goals Solution Components identified follow SCB Technology Standards |
| **Control Requirements** |<br/>- Ensure intended Solution aligns with the Enterprise Architecture principles, Architecture Roadmap and Architecture goals<br/>- Ensure stakeholder agreement on high-level solution design is achieved before major investments in solution development is done<br/>- Ensure to reassess and update the designs when significant issues occur during detailed design or building phases, or as the solution evolves<br/>- Apply a user-centric approach (ensure that stakeholders actively participate in the design and approve each version)<br/>- Security review for the new solution or enhancement to the existing solution is managed as part of the Solution Intent review<br/>- Ensure strict version control for the Solution Intent<br/>- Ensure Production Architecture details are up to date and available in a central location ahead of operational use of the associated solution.<br/>- Ensure design deviations are tracked and appropriately fixed. |
| **Control Tasks** |<br/>- Perform Architecture impact assessment and determine if there are architecture changes.<br/>- Create Solution Intent to meet the requirements for proposed EPIC/ Feature/ User Story.<br/>- Map the Functional and Non-Functional requirements with the Solution Intent.<br/>- Provide linkage to associated overall architecture roadmaps<br/>- Develop and document design for the solution in terms of technology, business processes and workflows<br/>- Manage changes to the Solution intent by creating new version of SI document with incremental updates.<br/>- Document changes to the Architecture and have them reviewed and approved ahead of the start of activities which build on them.<br/>- Publish up-to-date Production architecture details in a central location. |
| **Evidence** | When using the bank's standard engineering pipeline Note: Domain Architect/Country Architect must ensure PO review is completed before Solution Intent reaches to him/her for impact review. Domain Architect/Country Architect is accountable to review the conceptual design and detailed design with intended forums as stated in Solution Intent procedure and provide signoff in ADO. Refer QA stage of the Pipeline validationfor the SI checks in the pipeline. |

| **Sl.No** | **What** | **When** | **Scope** | Performer | **Approver** | **Update / Review Frequency** | **Evidencing - ADO** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Solution Intent | Discovery, Inception | Proposed / Target Architecture of a Solution / Initiative | Product Owner (or delegate) / Delivery Team | Impact Assessment:<br/>1. Domain Architect or Country Architect Conceptual Design: (If Material Impact and Deemed as Applicable)<br/>1. Domain Technology Council Note : Domain Architect or Country Architect approves in ADO and the minutes of the Domain Technology Council meeting must be attached in ADO. Detailed Design: (If material Impact)<br/>1. Architect Review Forum<br/>2. Domain Technology Council (Optional) Note : Domain Architect or Country Architect approves in ADO and the minutes of the Architect Review Forum meeting must be attached in ADO. Sub-Council Review: (Sub-Council reviews decided by Domain Architect/Country Architect)<br/>1. Cloud Review<br/>2. Data Review<br/>3. Resilience Review Refer Note provided below: | Create/Clone/Update Solution Intent and Tag it with either EPIC (or) Feature (or) User Story level based on the nature of Solution Design changes to be implemented under EPIC / Feature / User Story. Not to Tag Solution Intent at Release Work Item level (or) Initiative level. Solution Intent is mandatory irrespective of the type of Initiative. Note: Security Review is now part of ARF/DTC | Use Solution Intent workitem to perform Material impact assessment and update the relevant sections. (Refer Tool Mentor<br/>- SI) |
| 2 | Application Architecture | Deploy | Architecture of Application (Instance) in production post proposed change | Delivery Team | Technology Service Owner |<br/>- Review annually, OR - whenever there is a material impact in architecture triggered by Solution Intent Note:<br/>- Application Architecture must be up to date and maintained | Application Architecture documented in the prescribed template and uploaded as part of Application Workitem |

Note:  Domain Architect/Country Architect must ensure PO review is completed before Solution Intent reaches to him/her for impact review. Domain Architect/Country Architect is accountable to review the conceptual design and detailed design with intended forums as stated in [Solution Intent procedure](https://confluence.global.standardchartered.com/display/ENTARCH/EA-SOP-SIDMP-0002%20-%20Solution%20Intent%20Document%20Procedure) and provide signoff in ADO. 
Refer QA stage of the [Pipeline validation](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2763057422) for the SI checks in the pipeline.
GTC approval is mandatory for creating Solution Intent and new ITAM ID creation.
## Relationships

### Content References

- [How To - Update a link in Azure Boards?](../tools/next-gen-pipeline-ado/how-to-update-a-link-in-azure-boards.md)


### Qualified References
- **Disciplines**
  - [Design and Architecture](../disciplines/design-and-architecture.md)
- **Tasks**
  - [Define High-Level Solution Architecture](../disciplines/design-and-architecture/define-high-level-solution-architecture.md)
  - [Determine Solution Impact](../disciplines/design-and-architecture/determine-solution-impact.md)
  - [Conduct Security Business Impact Assessment](../disciplines/all-tasks/conduct-security-business-impact-assessment.md)
  - [Conduct Privacy Impact Assessment (PIA)](../disciplines/design-and-architecture/conduct-privacy-impact-assessment-pia.md)
  - [Complete (IT) Resilience Business Impact Assessment](../disciplines/design-and-architecture/complete-it-resilience-business-impact-assessment.md)
  - [Conduct Data Quality impact assessment, submit the remediation plan if impact is identified, communicate the impact to affected parties](../disciplines/design-and-architecture/conduct-data-quality-impact-assessment-submit-the.md)
  - [Conduct Deployment Impact Assessment](../disciplines/deployment/conduct-deployment-impact-assessment.md)
  - [Initiate Security Impact Assessment](../disciplines/design-and-architecture/initiate-security-impact-assessment.md)
  - [Refine the Architecture](../disciplines/all-tasks/refine-the-architecture.md)
  - [Define Solution Intent](../disciplines/all-tasks/define-solution-intent.md)
  - [Obtain sign off on Solution Design and arrive at high level architecture](../disciplines/design-and-architecture/obtain-sign-off-on-solution-design-and-arrive-at.md)
  - [Obtain sign-off for adequacy of DQ controls implementation](../disciplines/all-tasks/obtain-sign-off-for-adequacy-of-dq-controls.md)
  - [Uplift DQ control](../disciplines/all-tasks/uplift-dq-control.md)
- **Roles**
  - [Domain Architect](../roles/domain-architect.md)
  - [Solution Architect](../roles/solution-architect.md)
- **Artifacts**
  - [[Technology Architecture]](../practices/end-to-end-impact-assessment/work-products/technology-architecture.md)
  - [Infrastructure Solution Design Document](../work-products/analysis-amp-design/infrastructure-solution-design-document.md)
  - [API Technical Specification](../work-products/analysis-amp-design/api-technical-specification.md)
  - [High Level Architecture](../practices/end-to-end-impact-assessment/work-products/high-level-architecture.md)
  - [Solution Intent Document](../work-products/analysis-amp-design/solution-intent-document.md)
- **Tools**
  - [Next Gen Pipeline-ADO](../tools/next-gen-pipeline-ado.md)
  - [Next Gen Pipeline- ADO - General FAQ](../tools/next-gen-pipeline-ado/next-gen-pipeline-ado-general-faq.md)
  - [How To - Upload an attachments in Azure Boards?](../tools/next-gen-pipeline-ado/how-to-upload-an-attachments-in-azure-boards.md)
  - [Understanding Application Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-application-work-item-in-ado.md)
  - [Understanding Release approval in the pipeline](../tools/next-gen-pipeline-ado/understanding-release-approval-in-the-pipeline.md)
  - [Understanding Solution Intent Work Item in ADO](../tools/next-gen-pipeline-ado/understanding-solution-intent-work-item-in-ado.md)
  - [User Board Journey in ADO](../tools/next-gen-pipeline-ado/user-board-journey-in-ado.md)
  - [How to create Release workitem](../appendix/guidance/how-to-create-release-workitem.md)
  - [How to do application control evidencing in ADO](../appendix/guidance/how-to-do-application-control-evidencing-in-ado.md)
  - [Solution Intent](../appendix/guidance/solution-intent.md)
- **Templates**
  - [Solution Intent Document Template](../templates/solution-intent-document-template.md)
  - [Infrastructure Solution Design Document Template](../templates/infrastructure-solution-design-document-template.md)
  - [API Technical Specification](../templates/api-technical-specification.md)
  - [Application Architecture Template](../templates/application-architecture-template.md)
- **Guidelines**
  - [API Guidelines](../guidance/guidelines-by-discipline/testing/api-guidelines.md)
  - [Enterprise Monitoring Guidelines](../guidance/guidelines-by-discipline/operations-amp-support/enterprise-monitoring-guidelines.md)
  - [Performing a Solution Impact Assessment](../guidance/guidelines-by-discipline/analysis-and-design/performing-a-solution-impact-assessment.md)
  - [API Classifications](../guidance/guidelines-by-discipline/testing/api-classifications.md)
  - [Solution Intent FAQs](../guidance/all-guidelines/solution-intent-faqs.md)
  - [Solution Intent Procedure and Template](../guidance/all-guidelines/solution-intent-procedure-and-template.md)
  - [Internal Digital Certificate Management: Guidelines and Procedures](../guidance/all-guidelines/internal-digital-certificate-management.md)

- **Checklists**
  - [Release Compliance Controls — Pre-Flight Checklist](../checklist/compliance-checks-preflight-checklist.md)