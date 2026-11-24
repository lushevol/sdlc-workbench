# Perimeter And Network

Ratan settlement deployed on GDCW data center with Active-Passive model in cluster.

All micro-services is not accessible from outside SCB.

All micro-services are internal network, no internet connection.

Microservices and message middleware(e.g. Kafka) communication via TLS.

Secrets are vaulted using Hashicorp.

No direct communication between user terminal and backend instances. Firewall  only allow the ports in white list.

Web UI communicate with backend services over nginx and api gateway. Api gateway will validate the user token by FMAA.

Ratan settlement deployment via ADO pipeline

Architect Diagram

# API Security

Settlement UI uses REST over HTTPS protocol to communicate with Ratan settlement Micro-Services.

# Access control

- Internal User - Internal user authentication uses 2FA implementation with combination of PASSWORD and MFA OTP

- External User or Client - Not accessible

# For  51358-ratan-cash-settlement-orchestration CVE Risk Control

1. This service do not receive message from upstream application directly.
2. All message from upstream, should pass by message bridge and group service. And these two service already fixed the CVE issue.
3. No external API and message middleware to expose, like above diagram, Orchestration service only receive the internal Group service. Group service no such a CVE issue

| Risks associated | Control |
| --- | --- |
| CVE-2026-68497 is an unauthenticated CPU-exhaustion vulnerability in Jackson Databind’s default XML datatype deserializers. When a JSON string is bound to **javax.xml.datatype.Duration** or **XMLGregorianCalendar**, Jackson passes the raw value to the JDK **DatatypeFactory**. An attacker can supply millions of numeric digits inside the string, bypassing Jackson’s numeric-token length control and triggering quadratic-cost **BigInteger** or **BigDecimal** parsing. A single request may occupy a worker thread for tens of seconds or minutes; several concurrent requests can saturate CPU and worker pools, making the service unavailable. The issue does not require polymorphic typing or special ObjectMapper configuration. | 1. ratan-cash-settlement-orchestration only receive the message from group service. And group service have fixed the CVE issue 2. javax.xml.datatype.Duration is not supported for our XML parsing processor, so it will cause parsing failed |
| CVE-2026-47884 affects Spring MVC applications using **XsltView** with a broad **/**** mapping that renders a view without explicitly setting its name. In this configuration, Spring can derive the view name from the attacker-controlled request path and use it to locate an XSLT stylesheet. A remote, unauthenticated attacker may therefore cause the server to fetch internal or external resources and, depending on the XSLT processor and runtime configuration, execute arbitrary code in the application JVM. Successful RCE can provide full compromise of the application host and credentials or services accessible to its runtime identity. | 1. Ratan settlement application do not match the 3 trigger condition a. XsltView never used in ratan application. b. GUI Rendering is base on Javascript |
| CVE-2026-59283 affects Spring Framework applications that evaluate Spring Expression Language expressions through **SimpleEvaluationContext** while the SpEL expression compiler is active. Under these conditions, a crafted expression can bypass the safety restrictions expected from the limited evaluation context. If untrusted input reaches such an evaluation sink, a remote unauthenticated attacker may execute unsafe compiled expression behaviour with the application’s privileges, enabling unauthorised data or state modification and service disruption. The published CVSS vector assigns High integrity and availability impact but no direct confidentiality impact. | 1. All accessible API are manually added in API gateway 2. API parameter are serialized |
| CVE-2026-59284 affects Spring Cloud Commons when the writable **/actuator/env** endpoint is enabled without an allow list for property keys. An authenticated attacker with high privileges can submit arbitrary property names and values, modifying the application environment at runtime. Depending on which properties the application consumes and whether a refresh or restart applies them, exploitation may alter security controls, routing, logging, integrations, resource behaviour, or other configuration. The changed-scope CVSS rating reflects the possibility that manipulated settings affect components beyond the vulnerable endpoint. | 1. /actuator/env have disabled by our prod access list config, it's not accessible ![image-2026-10-6_14-14-22.png](attachments/image-2026-10-6_14-14-22.png) |