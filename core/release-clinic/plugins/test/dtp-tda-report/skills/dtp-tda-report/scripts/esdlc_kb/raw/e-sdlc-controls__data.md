# Controls: Data

---

## Key Consideration

## Control Attributes

| **Control Name** | Data |
| --- | --- |
| **L3 Risk Taxonomy** | Technology Change |
| **Control Objective** |<br/>- Impact Assessment on data changes is based on Data Quality Management Policy and Standard requirements.<br/>- The impact assessment on downstream data consumers is to be done primarily on Critical Data Elements (CDE), while other data elements are to be assessed where applicable.<br/>- Data changes made without proper assessment and notification could lead to significant downstream process impact. |
| **Control Requirements** |<br/>- Perform an impact assessment of the Critical Data Elements (CDE) in scope of the Group Data Quality Management Policy (section 5).<br/>- Access the Metadata Smart View tool to identify and review information on system critical data elements, downstream processes, process owners, immediate interfaces and system owners.<br/>- Refer to DQ change Managemement process to understand the scope of DQ control required for uplift.<br/>- Engage respective dataset custodian/owner of impacted downstream processes and interfaces, and notify on CDE change implementation.<br/>- Assess if the change impacts the information captured in MSV/Axon/Rosetta [For FM systems]. If yes then the relevant changes have to be implemented in MSV/Axon. For example: Any impact on data dictionary, data lineage, transformation logic, interface logic etc and make relevant changes in the metadata tools [MSV/Axon] |
| **Control Tasks** |<br/>- Ensure impact on system and on upstream & downstream data consumer is considered early in the delivery lifecycle. Delivery teams need uplift Data Quality control before release.<br/>- Ensure the data impact assessment completed and notification mails sent are recorded in respective CIO inventory |

## Relationships

### Content References

- [Determine Solution Impact](../disciplines/design-and-architecture/determine-solution-impact.md)


### Qualified References
- **Tasks**
  - [Conduct Data Quality impact assessment, submit the remediation plan if impact is identified, communicate the impact to affected parties](../disciplines/design-and-architecture/conduct-data-quality-impact-assessment-submit-the.md)
  - [Conduct Privacy Impact Assessment (PIA)](../disciplines/design-and-architecture/conduct-privacy-impact-assessment-pia.md)
  - [Uplift DQ control](../disciplines/all-tasks/uplift-dq-control.md)
  - [Obtain sign-off for adequacy of DQ controls implementation](../disciplines/all-tasks/obtain-sign-off-for-adequacy-of-dq-controls.md)
- **Artifacts**
  - [PIA Threshold Assessment](../work-products/analysis-amp-design/pia-threshold-assessment.md)
- **Tools**
  - [Using Privacy Impact Assessment Tool](../appendix/guidance/using-privacy-impact-assessment-tool.md)
  - [Metadata Manager](../practices/impact-assessment-on-system-and-on-downstream/metadata-manager.md)
- **Guidelines**
  - [Group Privacy Standard](../guidance/all-guidelines/group-privacy-standard.md)

- **Checklists**
  - [Release Compliance Controls â€” Pre-Flight Checklist](../checklist/compliance-checks-preflight-checklist.md)