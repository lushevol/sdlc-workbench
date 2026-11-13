# Agreements

Design page: [Foundation Service Mesh Platform - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Foundation+Service+Mesh+Platform)

1. **All domain services should share same infrastructures, following the FSM1.0 design, to share servers and foundation services, since we are building cash settlement platform.** 1. **Infrastructures contain** 1. **Kafka** 2. **Redis** 3. **ELK** 4. **Servers** 5. **PostgreSQL** 2. **Microservice foundation services contain** 1. **Consul, for service registration and configuration** 2. **Spring Cloud API Gateway** 3. **Authentication Server** 3. **Archetype for domain service build** 1. **API registration starter** 2. **Distributed lock starter** 3. **Duplication check starter** 4. **Camunda workflow starter** 5. **Logging starter** 6. **Kafka starter** 7. **Redis starter** 8. **Actuator starter** 4. **Common CI/CD pipeline to ** 1. **Build the infrastructures and foundation services** 2. **Domain services build and deployment** 5. **Version of software list: [Foundation Service Mesh Platform - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Foundation+Service+Mesh+Platform#FoundationServiceMeshPlatform-ThetechnicalstacksoftheFSM1.0)**
2. **Camunda workflow currently used by Ratan should be a component to be reused or enhanced.**
3. **Using spring boot and spring cloud native components for development**
4. **If any development required before archetype ready, please focus on the business logic only and bypass the development with dependency on infrastructure services, for example all the starters listed above**
5. **Everyone from the team can suggest and contribute for above components**

# Action point

1. **Archetype to be created on open source repository**
2. **FSM-foundation to be created containing all the dependencies and starters**
3. **Shared library to be created for infrastructure setup and application installation**
4. **Testing env on cluster to be created**

| | Action | Status | Owner | Update |
| --- | --- | --- | --- | --- |
| 1 | **FSM-foundation to be created containing all the dependencies and starters** | | Eric | |
| 2 | **Archetype to be created on open source repository** | | Eric | |
| 3 | **Shared library to be created for infrastructure setup and application installation** | | | |
| 4 | **Testing env on cluster to be created for verification** | | Geoffrey | **Features:** 4 CPU + 8 G memory + 70 Disk **Server list: ** 10.198.52.248 10.198.52.247 10.198.52.252 **Confidential:** infra2/Foundation@123 |
| 5 | **Infra services installation on testing env (ansible scripts)** | | | |
| 6 | **Foundation services installation on testing env** | | | |
| 7 | **Demo domain service build** | | | |

# Meeting minutes

**8th Aug**

Attendee: Rich, Eric, Zikai, Lina, Geoffrey

1. Eric shared the FSM 1.0 and 2.0 design
2. **It is agreed that all domain services should share same infrastructures, following the FSM1.0 design, to share servers and foundation services, since we are building cash settlement platform. 2**Options: 1. One cluster for all, share same servers and foundation services. 1. Open question: PSS responsibility, how 2 PSS groups will handle the platform together 2. Ratan VM cluster to provide infrastructure services including Kafka, ELK, Redis, Auth server, API gateway, Service registration, etc. And Razor physical servers work as cluster members which hold only the domain services. 1. Open question: Synchronization problem on services availability, there will be some downtime for VM on patching, on physical servers there is even hard reboot.
3. **It is agreed that camunda workflow should be a component to be reused or enhanced, Ratan has got 3 workflows live on production already for past 2 years, we will share and discuss further in next session**

Agenda for next meeting (10<sup>th</sup> Aug):

1. Camunda sharing on Ratan practice
2. MIEX architecture understanding

**10th Aug**

Attendee: Rich, Eric, Karl, Lina, Geoffrey

1. Geoffrey shared the Ratan Camunda usage, no key blocker on supporting the new business flow
2. Rich briefed the MIEX structure, key difference is on API gateway, but with only limited effort on migration to Spring Cloud API Gateway

Agenda for next meeting (15<sup>th</sup> Aug):

1. Camunda discussion on workflow
2. Agreement on above

**15th Aug**

Attendees: Rich, Eric, Karl, Zikai, Wayne, Geoffrey

We have made the agreement as the first section on the page.

Let’s work strictly to the agreement, keep each other posted to avoid redundant development, thanks. [@Li, Rich Yuan](mailto:Rich-Yuan.Li@sc.com) please help to extend it to whoever will be involved in the cash settlement platform development, thanks.

Agenda for next meeting (17th Aug):

1. Ratan Camunda workflow to the shared and reused.

**17th Aug**

Attendees: Rich, Lu, Krishna, Zikai, Lina, Wayne, Eric, Geoffrey

Ratan camunda starter was shared on the technical functionalities, also showed how it works for BCS settlement.

From our discussion on the Ratan Camunda Starter, we don’t see risks on its supporting for the China Settlement workflow. Also it was designed for strategic settlement flow and proved by BCS project to be working, thus it could be a perfect candidate to support the workflow.

If anyone find any new business requirements that it cannot support, please share them and we are happy to have a talk again perhaps on Friday’s call to find out solution together.

Summary on the ratan camunda starter:

1. The starter provided by Ratan is a technical component to support camunda workflow diagrams on orchestrating domain services
2. The development mode is only focusing on bpmn diagrams creation for service orchestration and start a spring boot application without coding.
3. Technically, current camunda starter is flexible enough to support
4. Functionally, BCS workflow already support below and can be reused and enhanced to support CN settlement
5. Any enhancement required, let’s find out the business requirement first

**19th Aug**

Attendees: Liam, Zikai, Eric, Lina, Wayne, Geoffrey

Mainly we went through the agreements we have made.

Topics for next session:

Camunda workflow definition.