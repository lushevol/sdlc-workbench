## Background & Problem Statement

### 1.1 Current Pain Points

Relational databases (PostgreSQL / MySQL / Oracle) suffer from the following issues when storing large fields (BLOB / CLOB / TEXT / BYTEA):

| Problem | Description |
| --- | --- |
| **Performance Degradation** | Large fields co-located with business columns cause full table scans and index bloat, slowing down queries |
| **High Storage Cost** | Database storage unit cost is significantly higher than object storage (approx. 10~50x) |
| **Slow Backups** | Large fields inflate backup file sizes, increasing backup/restore time considerably |
| **Connection Pool Pressure** | Reading large fields occupies database connections for extended periods, reducing concurrency throughput |
| **Poor Scalability** | Vertical scaling of databases is expensive; horizontal scaling is complex |

### 1.2 Typical Large Field Scenarios

- Contract/report PDF files (Finance, Legal industries)
- **Trade message XML/JSON raw payloads (current project context)**
- Images, attachments, audio/video
- Logs and audit record snapshots

---

## 2. Solution Overview

### 2.1 Core Approach: Database + Object Storage Separation (Hybrid Storage Pattern)

## 3. Architecture Design

### 3.1 Overall Architecture Diagram

` ┌─────────────────┐
│ API Gateway │
└────────┬────────┘
│
┌────────▼────────┐
│ Application │
│ Service │
└──┬──────────┬───┘
│ │
┌────────────▼──┐ ┌────▼───────────────┐
│ PostgreSQL │ │ MinIO Cluster │
│ (Metadata) │ │ │
│ │ │ ┌───────────────┐ │
│ object_ref ──┼──┼─►│ Primary Site │ │
│ │ │ └───────┬───────┘ │
└───────────────┘ │ │ Replicate │
│ ┌───────▼───────┐ │
│ │ DR Site │ │
│ └───────────────┘ │
└─────────────────────┘
`
### 3.2 Data Model Changes

#### Before (Large fields stored directly in the database)

`CREATE TABLE trade_message (
id UUID PRIMARY KEY,
trade_id VARCHAR(50),
status VARCHAR(20),
raw_message TEXT, -- ❌ Large field stored directly, can reach 10MB+
created_at TIMESTAMP
);
`
#### After (Reference pattern)

`CREATE TABLE trade_message (
id UUID PRIMARY KEY,
trade_id VARCHAR(50),
status VARCHAR(20),
raw_msg_bucket VARCHAR(100), -- MinIO bucket name
raw_msg_key VARCHAR(500), -- MinIO object key
raw_msg_size BIGINT, -- File size (bytes), useful for monitoring
raw_msg_checksum VARCHAR(64), -- SHA-256, used for integrity verification
created_at TIMESTAMP
);
`
### 3.3 Object Key Naming Convention

`{bucket}/{env}/{year}/{month}/{day}/{business-type}/{uuid}.{ext}

Examples:
trade-raw-messages/prod/2026/05/06/cashflow/550e8400-e29b-41d4-a716-446655440000.xml
contract-docs/prod/2026/05/06/loan/7f3b2a1c-9d4e-4f8b-b3c2-1a2b3c4d5e6f.pdf
`
---

## 4. Detailed Design

### 4.1 Write Flow

`Client Request
│
▼
┌────────────────────────────────────────────┐
│ Step 1: Business Validation │
│ - File size limit (e.g. 50MB) │
│ - File type whitelist (MIME Type check) │
│ - Virus scanning (enterprise scenarios) │
└────────────────┬───────────────────────────┘
│
▼
┌────────────────────────────────────────────┐
│ Step 2: Upload to MinIO │
│ - Compute SHA-256 Checksum │
│ - Small file (<5MB): PutObject │
│ - Large file (≥5MB): Multipart Upload │
│ - Set object metadata (Content-Type, etc) │
└────────────────┬───────────────────────────┘
│ Upload succeeded?
├── NO ──► Throw exception, rollback, do NOT write DB
│
▼ YES
┌────────────────────────────────────────────┐
│ Step 3: Write to Database (reference only)│
│ - INSERT business metadata + object_key │
│ - Performed within a single DB transaction│
└────────────────┬───────────────────────────┘
│ DB write failed?
├── YES ──► Compensate: async delete MinIO object
│ (Orphan Object Cleaner)
▼ NO
Return success response
`
### 4.2 Read Flow (Two Modes)

#### Mode 1: Direct Streaming Response (Recommended — no disk buffering)

`Client ──GET /api/trade/{id}/raw──► Service
│
├─ Query DB for bucket + key
│
├─ Call MinIO getObject() → InputStream
│
└─ Stream directly into HttpResponse
No need to buffer full content in memory
`
#### Mode 2: Presigned URL (Suitable for direct front-end downloads)

`Client ──GET /api/trade/{id}/download-url──► Service
│
├─ Query DB for key
│
└─ Generate Presigned URL (15min TTL)
Return URL to Client
Client downloads directly from MinIO
(Bypasses application, reduces bandwidth pressure)
`
### 4.3 Core Code Design (Java / Spring Boot)

#### MinIO Service Wrapper

`@Service
@Slf4j
public class MinioStorageService {

private final MinioClient minioClient;
private final MinioProperties props;

// Upload (auto-selects standard or multipart upload)
public ObjectReference upload(String bucket, String keyPrefix,
InputStream content, long size, String contentType) {
String key = buildKey(keyPrefix);
String checksum = DigestUtils.sha256Hex(content); // compute before upload

if (size >= props.getMultipartThreshold()) {
uploadMultipart(bucket, key, content, size, contentType);
} else {
minioClient.putObject(PutObjectArgs.builder()
.bucket(bucket).object(key)
.stream(content, size, -1)
.contentType(contentType)
.build());
}
return new ObjectReference(bucket, key, size, checksum);
}

// Streaming read
public InputStream download(String bucket, String key) {
return minioClient.getObject(
GetObjectArgs.builder().bucket(bucket).object(key).build());
}

// Generate presigned URL
public String presignedUrl(String bucket, String key, int expiryMinutes) {
return minioClient.getPresignedObjectUrl(
GetPresignedObjectUrlArgs.builder()
.method(Method.GET)
.bucket(bucket).object(key)
.expiry(expiryMinutes, TimeUnit.MINUTES)
.build());
}

// Delete (used for compensation)
public void delete(String bucket, String key) {
minioClient.removeObject(
RemoveObjectArgs.builder().bucket(bucket).object(key).build());
}
}
`
---

## 5. Exception Handling Design

### 5.1 Exception Classification & Handling Strategy

| Exception Scenario | Handling Strategy |
| --- | --- |
| MinIO upload failure | Return error immediately, **do not write to DB**, client retries |
| MinIO upload success but DB write fails | **Compensating delete**: publish async message to Dead Letter Queue; Orphan Cleaner removes orphaned objects periodically |
| MinIO download failure (object not found) | Return 404, trigger alert, manually investigate data consistency |
| MinIO cluster unavailable | **Circuit Breaker** (Resilience4j) trips; degrade to read-only mode or return 503 |
| Network timeout | Configure retry (max 3 attempts, exponential backoff); alert if all retries exhausted |
| Object checksum mismatch | Reject data return, trigger alert, mark object as CORRUPTED |

### 5.2 Orphan Object Cleaner

`Scheduled task (daily at 2:00 AM):
 1. Scan MinIO {bucket}/pending/ for objects older than 1 hour
 2. Query DB to check whether the corresponding object_key has a valid record
 3. If NOT found → delete MinIO object, write cleanup log
 4. If found → skip
`
### 5.3 Data Consistency Verification Task

`Scheduled task (weekly):
 1. Query all object_key records from DB in batches (1000 per batch)
 2. Call MinIO statObject() to verify each object exists
 3. Optionally compare checksum (higher cost)
 4. Log inconsistencies and send alert report
`
---

## 6. Access Control Design

### 6.1 MinIO IAM Model

`┌─────────────────────────────────────────────┐
│ MinIO IAM Structure │
├─────────────┬───────────────────────────────┤
│ Service │ Policy │
│ Account │ │
├─────────────┼───────────────────────────────┤
│ app-writer │ s3:PutObject on trade-* │
│ │ s3:GetObject on trade-* │
│ │ s3:DeleteObject on trade-* │
├─────────────┼───────────────────────────────┤
│ app-reader │ s3:GetObject on trade-* (RO) │
├─────────────┼───────────────────────────────┤
│ backup-user │ s3:GetObject on * (backup use) │
├─────────────┼───────────────────────────────┤
│ admin │ Full access (ops team only) │
└─────────────┴───────────────────────────────┘
`
### 6.2 Bucket-Level Policy Example

`{
"Version": "2012-10-17",
"Statement": [
{
"Effect": "Allow",
"Principal": { "AWS": ["arn:aws:iam:::user/app-writer"] },
"Action": ["s3:PutObject", "s3:GetObject"],
"Resource": ["arn:aws:s3:::trade-raw-messages/*"]
},
{
"Effect": "Deny",
"Principal": "*",
"Action": ["s3:DeleteObject"],
"Resource": ["arn:aws:s3:::trade-raw-messages/*"],
"Condition": {
"StringNotEquals": {
"aws:username": "admin"
}
}
}
]
}
`
### 6.3 Data Encryption

| Layer | Approach |
| --- | --- |
| **Transport Encryption** | TLS 1.2+ (HTTPS) |
| **Encryption at Rest** | MinIO SSE-S3 (server-side auto-encryption, AES-256) |
| **Sensitive Data** | SSE-C (client-managed key, highest security level) |
| **Key Management** | Integrate HashiCorp Vault or AWS KMS |

### 6.4 Application-Level Access Control

`// Spring Security + custom annotation for access control
@PreAuthorize("hasRole('TRADE_VIEWER')")
@GetMapping("/trade/{id}/raw")
public ResponseEntity<StreamingResponseBody> getRawMessage(@PathVariable String id) {
// Additional check: users can only access data within their own department
validateDepartmentAccess(id, SecurityContextHolder.getContext());
...
}
`
---

## 7. Disaster Recovery Management

### 7.1 MinIO High Availability Deployment

`Production recommendation: MinIO Distributed Mode (minimum 4 nodes)

Node1 Node2 Node3 Node4
│ │ │ │
└──────┴──────┴──────┘
MinIO Cluster
Erasure Code (EC:4)
Tolerates 2 node failures while remaining available
RPO = 0, RTO < 1 min
`
### 7.2 Cross-Site Disaster Recovery (Active-Active or Active-Passive)

`┌─────────────────┐ ┌─────────────────┐
│ Primary Site │ │ DR Site │
│ (Shanghai) │ │ (Beijing) │
│ │ │ │
│ MinIO Cluster │◄───────►│ MinIO Cluster │
│ (Active) │ Bucket │ (Passive/ │
│ │ Replic. │ Active) │
└─────────────────┘ └─────────────────┘
`
**MinIO Bucket Replication Configuration Notes:**

- Enable **bidirectional** or **unidirectional** replication (based on cost requirements)
- Replication lag target: < 30 seconds
- On replication failure: object retained at source, async retry queue
- Monitoring: alert if replication lag exceeds 5 minutes

### 7.3 Backup Strategy

| Backup Type | Frequency | Retention | Tool |
| --- | --- | --- | --- |
| Full Backup | Every Sunday | 90 days | `mc mirror` or Velero |
| Incremental Backup | Daily | 30 days | MinIO Replication |
| Database Backup | Daily | 30 days | pg_dump |
| Configuration Backup | Every change | Permanent | Git |

### 7.4 RTO / RPO Targets

| Scenario | RPO | RTO |
| --- | --- | --- |
| Single node failure | 0 (no data loss) | < 1 minute |
| Full primary site failure | < 30 seconds | < 15 minutes |
| Accidental data deletion | Depends on when versioning was enabled | < 30 minutes |

> **Recommendation: Enable MinIO Versioning** to protect against accidental deletion.

---

## 8. Data Migration Plan

### 8.1 Migration Strategy: Dual-Write + Gradual Cutover (Zero Downtime)

`Phase 1: Dual-Write (new data written to both DB and MinIO; old data remains in DB)
─────────────────────────────────────────────────────────────────────────────────
New requests ──► Write large field to both DB and MinIO simultaneously
Add nullable object_key column to DB

Phase 2: Backfill Migration (async background job — no business impact)
─────────────────────────────────────────────────────────────────────────────────
Migration job (500 records per batch, rate-limited):
SELECT * FROM trade_message WHERE object_key IS NULL LIMIT 500
→ Upload large field content to MinIO
→ UPDATE record with object_key, clear raw_message column

Phase 3: Read Cutover
─────────────────────────────────────────────────────────────────────────────────
Read logic:
IF object_key IS NOT NULL → read from MinIO
ELSE → read from DB (backward compatibility)

Phase 4: Drop Legacy Column (after migration is verified complete)
─────────────────────────────────────────────────────────────────────────────────
ALTER TABLE trade_message DROP COLUMN raw_message;
`
### 8.2 Migration Job Design

`@Component
@Slf4j
public class LargeFieldMigrationJob {

@Scheduled(fixedDelay = 5000) // one batch every 5 seconds
@ConditionalOnProperty("migration.enabled")
public void migrate() {
List<TradeMessage> batch = repo.findUnmigratedBatch(500);
if (batch.isEmpty()) {
log.info("Migration complete!");
return;
}
batch.parallelStream().forEach(msg -> {
try {
// 1. Upload to MinIO
ObjectReference ref = minioService.upload(
"trade-raw-messages",
"migration/",
new ByteArrayInputStream(msg.getRawMessage().getBytes()),
msg.getRawMessage().length(),
"application/xml"
);
// 2. Update DB reference
repo.setObjectRef(msg.getId(), ref.getBucket(), ref.getKey(),
ref.getSize(), ref.getChecksum());
// 3. Optional: clear original field (or defer cleanup)
migrationCounter.increment();
} catch (Exception e) {
log.error("Migration failed for id={}", msg.getId(), e);
// Log failure; do not block other records
}
});
}
}
`
### 8.3 Migration Verification

`Post-migration verification checklist:
✅ Total record count aligned (DB count == MinIO object count)
✅ Random sample of 1,000 records — checksum comparison passes
✅ Load test read performance (post-migration vs pre-migration)
✅ Error rate monitoring shows no anomalies
✅ Rollback plan in place (retain legacy column data for at least 2 weeks before dropping)
`
---

## 9. Monitoring & Alerting

| Metric | Tool | Alert Threshold |
| --- | --- | --- |
| MinIO disk utilization | Prometheus + MinIO Exporter | 80% |
| Object upload/download latency | Prometheus | P99 > 2s |
| Upload failure rate | Application Metrics | 1% |
| Replication lag | MinIO Console | 5 minutes |
| Orphan object count | Custom scheduled task | 100 |
| Data consistency check failures | Custom scheduled task | 0 |

---

## 10. Non-Functional Requirements

| Metric | Target |
| --- | --- |
| Upload throughput | ≥ 500 MB/s (cluster level) |
| Single object upload latency (1MB) | < 200ms (P99) |
| Read latency (1MB) | < 100ms (P99) |
| System availability | 99.99% |
| Data durability | 99.999999999% (11 nines) |

---

## 11. Technology Stack Summary

| Component | Technology | Notes |
| --- | --- | --- |
| Object Storage | MinIO (Distributed Mode) | Private cloud preferred, S3-compatible |
| Java SDK | `io.minio:minio:8.5.x` | Official SDK |
| Circuit Breaker | Resilience4j | Spring Boot native integration |
| Message Queue (compensation) | Kafka / RabbitMQ | Orphan object cleanup |
| Monitoring | Prometheus + Grafana | Official MinIO Exporter available |
| Key Management | HashiCorp Vault | Enterprise-grade secret management |
| Database | PostgreSQL | Metadata and object references only |

---

## 12. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| MinIO cluster failure | Low | High | Multi-node cluster + DR site + circuit breaker fallback |
| Data inconsistency (DB has ref, MinIO has no object) | Low | High | Periodic consistency checks + alerting |
| Service disruption during migration | Low | Medium | Dual-write pattern guarantees zero downtime |
| Accidental object deletion | Low | High | Enable Versioning + MFA-protected delete |
| Storage cost exceeding forecast | Medium | Medium | Lifecycle policies for automatic archiving/cleanup |

---

*End of Document — Further elaboration can be provided for specific modules such as Kubernetes deployment configuration, Flyway SQL scripts, or Terraform infrastructure-as-code.*