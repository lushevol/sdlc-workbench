# Background

Teams need predictable Kafka DR behavior across regions for Ratan Indonesia, design, runbook, verification are required.

# Problem to Resolve

In a cross-DC outage or partition, teams cannot confidently achieve RTO/RPO without standardized replication direction, failover/failback flow, and evidence-based validation.

# Objectives

POC objective: Prove an operable MM2-based DR baseline with measurable RTO/RPO, controlled failover/failback, and production-ready governance gates.

# Scope

**In scope**: Critical-topic replication, offset/checkpoint sync, failover drill, failback drill, cross-DC edge-case tests.
**Out of scope**: Full automation of every incident path in phase 1.

# Rollout Plan

| Phase | Milestone | Description | Status | Owner | |
| --- | --- | --- | --- | --- | --- |
| 1 | Direction & Design | Finalize service-tier RTO/RPO, select DR pattern, freeze topic/group allow lists | | @Xinmiao Huang | |
| 2 | POC Delivery | Deploy MM2 lab, run end-to-end failover/failbck, capture evidence | | @Xinmiao Huang | POC reviewed by Geoffrey on 09-11 |
| 3 | Non-Prod Readiness | Cluster mode deployment, test case verification, monitoring setup | | @Xinmiao Huang @Haolin Song @Junli Gao @Zeyu Zhou | |
| | | 1. Cluster deployed and sanity check pass | | @Haolin Song @Junli Gao | |
| | | 2. DevOps playbook development | | | |
| | | 3. Test case verification | | | |
| | | 4. Monitoring setup | | | |
| 4 | Production Hardening | Alerting/SLOs, change approvals, rollback automation, monitoring | | | |

# Architecture

# Phase-1 Direction & Design

There are 3 topics to be settled for phase-1

## RTO/RPO:

- **RTO:** Within 2 hours (automated)
- **RPO:** 0 minutes for Active-Passive deployments
- Reference page: [RATAN active-active to active-passive - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATAN+active-active+to+active-passive)

## Topic/group scope:

- **All existing topics in Ratan ID cash settlement**

## DR pattern

### A. Runtime deployment modes(how MM2 runs)

| Mode | Description | Landing approach | Pros | Risks / Limits | Recommended use |
| --- | --- | --- | --- | --- | --- |
| Standalone Mode | One host runs connect-mirror-maker | Quick bootstrap with connect-mirror-maker-*.properties | Fastest setup | SPOF, weak HA | Dev POC only |
| Multi-node MM2 process cluster style | Same MM2 process started on multiple workers with connect-mirror-maker | Start on 3 workers, same config | Better HA, simple | Process-level ops, less fine-grained REST control | Small/medium environments |
| Distributed Connect + MM2 connectors | Dedicated Connect worker cluster + MM2 source/checkpoint/heartbeat connectors via REST | Use connect-distributed-MM2.properties + config/mm2-connectors/*.json | Best governance, pause/resume per connector, clearer SRE ops | Higher setup complexity | **Production preferred** |

### B. Replication direction modes (how data flows)

| Mode | Description | Landing approach | Pros | Risks / Limits | Recommended use |
| --- | --- | --- | --- | --- | --- |
| Primary -> Standby (one-way) | Steady-state DR replication | Enable primary->standby; disable reverse | Lowest conflict risk, clear ownership | Standby usually read-only | Default baseline |
| Standby -> Primary (failback window) | Temporary back-sync after primary recovers | Pause forward flow; enable failback connectors/config | Controlled reconciliation | Requires strict change window | Use during failback |
| Bidirectional (active-active) | Both directions enabled | A->B and B->A both active | Potential low RTO at region loss | Conflict, loops, offset complexity | Not recommended unless strict governance and conflict controls exist |

# Phase-2 POC Delivery

1. Config properties

```
bootstrap.servers=10.198.75.22:9092,10.198.75.23:9092,10.198.75.24:9092

# Unique name for this MM2 worker cluster
group.id=connect-mm2-cluster

# MM2 mirrors Kafka records as bytes; keep converter overhead minimal
key.converter=org.apache.kafka.connect.converters.ByteArrayConverter
value.converter=org.apache.kafka.connect.converters.ByteArrayConverter
key.converter.schemas.enable=false
value.converter.schemas.enable=false

# Dedicated Connect internal topics for MM2 isolation
offset.storage.topic=mm2-connect-offsets
offset.storage.replication.factor=3
#offset.storage.partitions=25

config.storage.topic=mm2-connect-configs
config.storage.replication.factor=3

status.storage.topic=mm2-connect-status
status.storage.replication.factor=3
#status.storage.partitions=5

# Flush interval
offset.flush.interval.ms=10000

# REST API for distributed workers
listeners=HTTP://0.0.0.0:8083
rest.advertised.host.name=uklvadrat0016a
rest.advertised.port=8083
#rest.advertised.listener=

# Add connector plugin directories if needed
plugin.path=/apps/ratanrt/utilities/kafka/live/plugins
```

2. run command

```bash
cd utilities/kafka/live/
export KAFKA_OPTS=-Djava.io.tmpdir=/apps/ratanrt/utilities/kafka/live/tmp
export JAVA_HOME=/apps/ratanrt/utilities/java-17-openjdk/java-17-openjdk-17.0.1.0.12-2.portable.jdk.el.x86_64
./bin/connect-distributed.sh -daemon ./config/connect-distributed.properties

Standalone
./bin/connect-standalone.sh  ./config/connect-standalone-1.properties 
```

3. register connecter

![image-2026-9-11_13-46-14.png](attachments/image-2026-9-11_13-46-14.png)

```bash
cd utilities/kafka/live/

curl -sS -X POST -H 'Content-Type: application/json' \
  --data @./config/mm2-connectors/mm2-ps-mirror-source.json \
  http://10.198.75.22:8083/connectors

curl -sS -X POST -H 'Content-Type: application/json' \
  --data @./config/mm2-connectors/mm2-ps-mirror-checkpoint.json \
  http://10.198.75.22:8083/connectors

curl -sS -X POST -H 'Content-Type: application/json' \
  --data @./config/mm2-connectors/mm2-ps-mirror-heartbeat.json \
  http://10.198.75.22:8083/connectors
```

4. check connectors

```bash
curl http://10.198.75.22:8083/connectors
```

5. check topics

6. Verify

# Phase-3 Non-Prod Readiness

## Cluster deployed and sanity check pass

## DevOps playbook development

## Test case verification

Test Matrix

| SN | Description | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Primary side sync to standby data success with 3 worker running, no data missing | | |
| 2 | 1 worker down, data sync to standby can success as well, no data missing | | |
| 3 | 2 worker down, data sync to standby can success as well, no data missing | | |
| 4 | 3 works all down, data sync can be continue from the failure point, no data missing | | |
| 5 | DR switch with Kafka lags, application start in backup DC, no message missing, backup cluster can sync data to primary | | |
| 6 | DR fail back, application start in primary DC, no message missing | | |

## Monitoring setup

# Phase-4 Production Hardening

## Performance tuning for high throughput

Confirm whether need a PT plan and performance tuning depends on the PT result if required.

## DR rehearsal

TBD

# Appendix

Reference document:

[Kafka MirrorMaker 2: Multi-Datacenter Replication Guide - Florian Courouge](https://floriancourouge.com/en/blog/kafka-mirrormaker2-replication)

[Kafka MirrorMaker 2: Cross-Cluster Replication | Conduktor](https://www.conduktor.io/glossary/kafka-mirrormaker-2-for-cross-cluster-replication)