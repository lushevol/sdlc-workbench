# CES domain model

## Access concepts

| Concept | What to establish |
| --- | --- |
| Application | Bind the CES application name and its observed external reference where available. Check the origin of any internal application ID used by a consumer. |
| Entitlement definition | A named application-scoped definition can contain feature and action pairs. Preserve the application in any comparison of entitlement names. |
| Assignment | An entitlement can have members and zero feature actions. An assignment describes membership in that definition. |
| Role-level grant | Assigned-role details can bind a feature and action to an entitlement. Use the matching request and application scope. |
| Effective functional access | The effective-user view returns assigned names and resolved feature and action pairs. The pairs can be shared by several entitlements, so the effective view leaves role attribution unresolved. |
| Data scope | `data_policies`, `data_profiles`, and `data_entitlements` are distinct data sections. Interpret resolved rules and values using the applicable policy and enforcement contract. |

An effective action and a data restriction can both apply to the same operation.
A result can therefore include a read action while a query predicate excludes a particular record.
To confirm a restriction, identify the resolved rule, the record values, and the predicate applied by the consumer.
For query or notification visibility, establish the actual enforcement point and the observed outcome for the same account and resource.
When comparing two data sections, verify operator meaning, precedence, and value resolution before claiming equivalent access.

## Evidence and ownership

Use a complete catalog capture to make completeness claims about its declared application scope.
Use an effective-user capture to report what its matched account and application returned.
Use a scoped assertion or execution record to establish what an integration allowed, denied, or filtered.
Keep missing captures, unavailable services, explicit empty records, and unresolved policies visible as distinct findings.

The response model comes from retained CES catalog and effective-user captures.
Historical CES designs describe HR-derived policy, role-derived profiles, and filters at query and notification boundaries.
Find the applicable approved policy before applying any historical rule, field list, or precedence.
Keep credentials and personal data in the authorized source location. Cite sanitized evidence references in reports.
