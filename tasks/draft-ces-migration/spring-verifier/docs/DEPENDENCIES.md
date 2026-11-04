---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Spring verifier dependencies

> **Local readiness does not establish live migration parity.**
> Action: prepare exact SDK artifacts, pass the verifier tests, and execute the declared company-network scope.
> Consequence: missing artifacts or incomplete live results keep migration coverage unverified.
> Owner: internal operator, identity unknown.
> Evidence: [user request](../../evidence/spring-verifier-20261104/user-input.md#exact-user-input).

## Current consumer and boundary

This project is the user's requested task-owned Spring example.
It compares actual EMS2 and CES SDK permission maps through isolated class loaders.
It is not a Workbench core dependency or generated-workspace component.
The Workbench Python runtime does not load this Java project.
The two SDK JARs remain external artifacts. Their implementation source is not copied into this project.

## Prerequisites

| Component | Required version | Current consumer | Installation and platform boundary |
| --- | --- | --- | --- |
| JDK | 17 or later; reviewed runtime is JDK 17. | SDK preparation, Maven compilation, and Java application. | Use the company's approved JDK for Windows, macOS, or Linux. |
| Maven | 3.8 or later; reviewed build uses Maven 3.9. | SDK preparation and verifier build. | Use approved Maven or its company-managed distribution. |
| Git | Existing supported command-line installation. | Export the two exact SDK revisions. | The SDK checkout must already contain both commits. No clone or fetch runs automatically. |
| Python | 3.10 or later. | Optional `prepare-sdks.py` helper. | Uses only the standard library; no pip installation. |
| SDK baseline | Commit `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`. | Baseline EMS2 client loaded from `lib/ems2-sdk.jar`. | Build its original source in an isolated export. |
| SDK candidate | Commit `fd9a157e260850b6d9efa10da3223950ea61133a`. | CES client loaded from `lib/ces-sdk.jar`. | Build its original source and require every declared test to pass. |

Run diagnosis before acquisition:

```sh
python3 prepare-sdks.py --sdk-repo /path/to/single-ui-sdk-starter --check
```

On Windows, use `py -3` instead of `python3`.
Supply `--java-home PATH` or `--maven PATH` when approved installations are outside `PATH`.
Diagnosis checks Java, Maven, Git, exact revisions, and writable destinations.
It does not download packages, build SDKs, or contact company services.

## Maven package dependencies

| Dependency | Constraint | Purpose |
| --- | --- | --- |
| Spring Boot starter | `4.0.6`. | Non-web Spring application startup and configuration. |
| Spring Web | Version managed by Spring Boot `4.0.6`. | Real `RestTemplate` transport shared with both isolated SDKs. |
| Jackson 2 databind | `2.21.2`. | SDK DTO binding and JSON report serialization. |
| Apache Commons Lang | Version managed by Spring Boot `4.0.6`. | `StringUtils` used by the actual SDK lookup implementations. |
| JUnit Jupiter | Version managed by Spring Boot `4.0.6`; test scope. | Consequential comparison, transport, and reporting assertions. |
| Spring Test | Version managed by Spring Boot `4.0.6`; test scope. | Controlled transport and framework tests. |
| Maven resources plugin | `3.3.1`. | Copy the application resources. |
| Maven compiler plugin | `3.14.1`. | Compile Java 17 source. |
| Maven Surefire | `3.5.5`. | Discover and execute all declared unit tests. |
| Maven JAR plugin | `3.4.2`. | Build the application archive. |
| Spring Boot Maven plugin | `4.0.6`. | Package an executable JAR with its declared runtime libraries. |

The [POM](../pom.xml) is the authoritative version manifest.
The SDK preparation build also resolves each original SDK POM's existing packages and plugins.
Its formatter and flatten plugins can need dependencies even when formatting is disabled.
Do not remove tests or rewrite SDK source to bypass missing packages.
The baseline source has no tracked tests. Its zero-test count is recorded explicitly.
The candidate requires a nonzero test count and zero failures, errors, and skips.

## Acquisition and network bounds

Maven uses its configured repositories and company-approved mirrors.
The default public package source is `https://repo.maven.apache.org/maven2/`.
Use exact Maven coordinates, versions, and checksums when preparing a company mirror or transferred cache.
Private repository credentials belong only in private Maven settings.
The helper neither reads credential values nor writes them into its manifest.

The helper bounds each SDK Maven build to 600 seconds by default.
Change this bound explicitly with `--deadline-seconds N`, from 1 through 86400 seconds.
The deadline includes dependency resolution and build work. Timeout ends the build process tree.
HTTP connection timeout is 15 seconds. Request timeout is 60 seconds.
Wagon and Resolver HTTP retry counts are bounded to one.
There is no automatic build retry or startup download.

Build with an explicit prepared-cache destination when reproducibility requires it:

```sh
python3 prepare-sdks.py --sdk-repo /path/to/single-ui-sdk-starter --maven-repository /path/to/maven-cache
```

The helper creates isolated source exports and preserves build evidence under `lib/build-evidence/`.
It records exact commits, source hashes, Maven arguments, test counts, log hashes, and SDK artifact hashes.
The completed `lib/sdk-manifest.json` exposes separate `baseline` and `candidate` artifact identities.
It never changes the SDK checkout's branch, tracked files, or installed Maven artifacts.

## Offline preparation and recovery

Prepare dependencies on an approved connected machine with matching package coordinates.
JDK and Maven installations must suit the target operating system and CPU architecture.
Use the same Maven repository for connected and offline checks:

```sh
python3 prepare-sdks.py --sdk-repo /path/to/single-ui-sdk-starter --maven-repository /path/to/maven-cache --output lib-connected
python3 prepare-sdks.py --sdk-repo /path/to/single-ui-sdk-starter --maven-repository /path/to/maven-cache --offline --output lib-offline
```

After moving the chosen artifacts into `lib/`, retain its matching `sdk-manifest.json` and build evidence.
Alternatively, configure the verifier's JAR and manifest paths to the chosen output directory.
Prepare the verifier's own Maven packages on that staging machine too:

```sh
mvn -Dmaven.repo.local=/path/to/maven-cache clean verify
mvn -o -Dmaven.repo.local=/path/to/maven-cache clean verify
```

For a blocked or timed-out SDK download, preserve the incomplete evidence directory.
Restore the missing exact coordinates through the approved Maven Central source or company mirror.
Transfer the prepared cache unchanged. Rerun diagnosis, then select `--offline` and a new artifact output directory.
The helper refuses to overwrite existing SDK JARs or a completed manifest.
Incomplete output never receives `READY` status.
Inspect local Maven logs before sharing them through the company's approved evidence process.

## Runtime access

Running the packaged verifier does not invoke Maven or download packages.
Replay mode uses controlled loopback services and requires no company credentials.
Live mode uses configured EMS2 and CES endpoints through normal JVM TLS trust.
No browser, database, public CDN, or report server is required.
Company DNS, routing, credentials, and trusted certificates remain external prerequisites.
Python CA variables do not configure the application's JVM trust store.
Live credentials stay in process variables or ignored local configuration, as the application guide specifies.
Mock success does not establish live endpoint access, complete company account scope, or seamless deployed behavior.

## Platform and evidence limits

The launchers check Java 17 and the built application JAR before execution.
`run.command` targets macOS or POSIX shells. `run.cmd` targets Windows Command Prompt.
Windows behavior requires a Windows execution record before claiming platform verification.
The source and declared Maven coordinates are portable. Target-specific installations remain independently verifiable.
