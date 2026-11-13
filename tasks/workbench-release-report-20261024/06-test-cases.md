# Release report canonical test cases

These 14 tooling case definitions preserve RR-1 through RR-8 and RR-P1 through RR-P6 from the original release-report preparation.
Their stable IDs and complete Gherkin blocks remain unchanged.
The relocation supplies no new business approval, automation readiness, conformance result, or passing execution.

Use the [current report guide](../../docs/RELEASE_REPORT.md) for installed interfaces and limits.
The [retained assertion map](evidence/release-report-implementation-20261024/integration-case-map.json) records historical assertion mappings and case differences.
Read its exact source hashes and matching execution records before reusing an outcome.
Controlled mock results do not establish company endpoint compatibility or release authorization.

## Definition provenance

- Prior Workbench revision: `79a4104035785b7d8c37e6d424d5d4c888104eee`.
- Original definition source: `docs/RELEASE_REPORT_REPRODUCTION.md`; SHA-256 `a1de1b3ff1faf45b1196f5f263ce23e9a37215ed04da6cacdceae635ee70f83b`.
- Original definition source: `docs/RELEASE_REPORT_API_DESIGN.md`; SHA-256 `4330d2809511aeff60787768600ac6d100cec97072a3542e35c77dcd300609c2`.

Original preparation classified these as definition-only cases. Later implementation evidence remains independent.
RR-P2 retains the original WebApi wording and exact 20/8 request fixture. The current collector uses raw REST sessions; existing mock coverage does not establish that original predicate.
RR-P3 retains its proposed controlled clock; recorded loopback timing is a different execution boundary.
Preserve these differences when assessing conformance. Do not silently change the canonical case to match a passing implementation.

## Report boundaries

### RR-1: Preserve a failed build

```gherkin
Feature: Preserve collection completeness

  @RR-1
Scenario: Preserve a failed build read
  Given a release references build IDs 101 and 102
  And build 101 is readable
  And the read for build 102 returns a forbidden response
  When the collector creates the report
  Then the report contains both requested build IDs
  And build 102 has collection status "failed"
  And the report links the retained error evidence
  And the overall collection status is "partial"
```

### RR-2: Preserve an unknown production baseline

```gherkin
Feature: Preserve baseline uncertainty

  @RR-2
Scenario: Report an unavailable production comparison
  Given a candidate build has an exact source commit
  And no production baseline has supporting deployment evidence
  When the report evaluates the production comparison
  Then the comparison status is "unavailable"
  And the report contains the missing-baseline reason
  And the comparison has no passed verdict
```

### RR-3: Keep duplicate requirement evidence

```gherkin
Feature: Preserve build-specific test evidence

  @RR-3
Scenario: Keep test counts from different builds
  Given builds 101 and 102 contain test statistics for requirement 501
  And build 101 records 3 passed tests and 1 failed test
  And build 102 records 2 passed tests and 2 failed tests
  And no aggregation rule is configured
  When the report joins requirement evidence
  Then requirement 501 contains build 101 with 3 passed tests and 1 failed test
  And requirement 501 contains build 102 with 2 passed tests and 2 failed tests
  And the report identifies the unresolved aggregation rule
  And no combined statistic is reported
```

### RR-4: Replay retained evidence

```gherkin
Feature: Reproduce local rendering

  @RR-4
Scenario: Render a report without external access
  Given retained normalized JSON has a recorded SHA-256
  And no service credentials are available
  When the renderer creates HTML twice from the same JSON
  Then zero external requests occur
  And both HTML outputs have the same SHA-256
  And the HTML records the input SHA-256
```

### RR-5: Preserve graph limits

```gherkin
Feature: Display relationship evidence limits

  @RR-5
Scenario: Display unresolved graph evidence
  Given graph metadata contains warning "Story links are incomplete"
  And graph metadata identifies unresolved story 501
  When the renderer displays the graph section
  Then warning "Story links are incomplete" is visible
  And unresolved story 501 is visible
  And the report does not label the graph complete
```

### RR-6: Derive report identities

```gherkin
Feature: Collect related information from one release identity

  @RR-6
Scenario: Derive builds and work items from a Release work item
  Given Release work item 501 references builds 101 and 102
  And its Related relation identifies story 201
  And its Tested By relation identifies test case 301
  When the collector receives only Release work item ID 501
  Then the report identifies release 501
  And the report contains builds 101 and 102
  And the report contains story 201 and test case 301
  And no additional per-report identity input is requested
```

### RR-7: Link separate compliance content

```gherkin
Feature: Preserve Release Clinic separation

  @RR-7
Scenario: Link a Release Clinic HTML attachment
  Given release 501 has attachment named "TDAReport_STREAM_501.html"
  And its attachment URL is "https://ado.example/attachments/clinic-501"
  When the renderer creates the release report
  Then its compliance section links to "https://ado.example/attachments/clinic-501"
  And its link label is "TDAReport_STREAM_501.html"
  And zero Release Clinic generation operations occur
  And zero Release Clinic files are modified
  And zero compliance verdicts are recalculated
```

### RR-8: Continue without a compliance document

```gherkin
Feature: Keep unavailable compliance content explicit

  @RR-8
Scenario: Keep release information when no Clinic report is linked
  Given release 501 has no matching Release Clinic HTML attachment or local output
  And its build and work item reads succeed
  When the renderer creates the release report
  Then its compliance section displays "Release Clinic report unavailable"
  And its build and work item information remains present
  And zero Release Clinic generation operations occur
  And no additional per-report input is requested
```

## Scheduling and evidence boundaries

### RR-P1: Batch unique work item identities

```gherkin
Feature: Avoid duplicate work item reads

  @RR-P1
Scenario: Batch 401 unique work item IDs
  Given release references contain 401 unique work item IDs and 99 duplicate references
  And the response byte limit permits 200 IDs per batch
  When the collector schedules work item detail reads
  Then exactly 3 batch requests occur
  And each batch contains at most 200 IDs
  And each unique ID appears in exactly 1 batch
  And all 401 records remain represented in the report
```

### RR-P2: Bound actual requests and reuse sessions

```gherkin
Feature: Bound collection concurrency

  @RR-P2
Scenario: Collect independent ADO and Sonar data
  Given one collection has 20 independent ADO requests and 8 independent Sonar requests
  And the concurrency limits are 6 for ADO and 2 for Sonar
  When all fixture endpoints return successful responses
  Then peak ADO concurrency is at most 6
  And peak Sonar concurrency is at most 2
  And exactly 1 ADO bridge session and 1 Sonar bridge session are created
  And the ADO session reuses 1 WebApi connection
  And all 28 requested responses are retained
```

### RR-P3: Respect a delay on a successful response

```gherkin
Feature: Preserve successful responses during throttling

  @RR-P3
Scenario: Receive Retry-After with HTTP 200
  Given the test clock reads 10 seconds
  And an ADO read returns HTTP 200 with Retry-After value 3
  When the scheduler handles that response
  Then the successful response is retained
  And that completed read is not retried
  And no new request to that ADO host starts before test clock time 13 seconds
```

### RR-P4: Apply grants before cached data access

```gherkin
Feature: Keep collection authorization consistent

  @RR-P4
Scenario: Deny an ungranted inner operation
  Given the collection references an ADO tool absent from its exact allowed tool list
  And cached data exists for that tool request
  When the collection scheduler requests that data
  Then the operation returns TOOL_NOT_GRANTED
  And zero network requests occur for that operation
  And zero cached protected payloads are returned
```

### RR-P5: Retain evidence larger than one tool response

```gherkin
Feature: Separate evidence size from tool response size

  @RR-P5
Scenario: Retain a large test attachment
  Given a test attachment contains 5242880 bytes with a known SHA-256
  And connector JSON frames are limited to 4194304 bytes
  When the collector streams the attachment into its evidence directory
  Then the retained artifact contains exactly 5242880 bytes
  And its SHA-256 equals the known input SHA-256
  And each connector JSON frame contains at most 4194304 bytes
  And the returned manifest links the artifact and records its hash
```

### RR-P6: Resume without concealing changed sources

```gherkin
Feature: Keep resumed evidence identity explicit

  @RR-P6
Scenario: Resume after the release revision changes
  Given a retained collection checkpoint records Release work item 501 at revision 7
  And the current work item query returns revision 8
  When the collector resumes that checkpoint
  Then the revision mismatch is recorded
  And the old evidence remains retained
  And the collector does not mark the mixed revision snapshot complete
```
