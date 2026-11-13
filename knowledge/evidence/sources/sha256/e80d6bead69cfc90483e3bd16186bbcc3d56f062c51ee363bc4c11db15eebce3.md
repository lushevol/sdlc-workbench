Has impact:

| Case | Sample | Solution |
| --- | --- | --- |
| LocalDateTime.now() will be based on the JVM time zone | ![image-2026-5-12_14-21-36.png](attachments/image-2026-5-12_14-21-36.png) | 1. vm options: -Duser,timezone=UTC 2. OS env variable: export TZ=UTC |
| Job scheduled cron will be based on JVM time zone | ![image-2026-5-12_14-23-21.png](attachments/image-2026-5-12_14-23-21.png) |
| Run now()/date function in DB script will be based on DB server time zone | now()/current_date/current_timestamp | 1. postgresql.conf → Timezone = UTC 2. alter database set timezone |

No impact:

| Case | Sample |
| --- | --- |
| Java LocalDateTime ↔ DB timestamp | ![image-2026-5-12_14-58-7.png](attachments/image-2026-5-12_14-58-7.png) ![image-2026-5-12_14-58-34.png](attachments/image-2026-5-12_14-58-34.png) |
| Jave LocalDateTime ↔ String | ![image-2026-5-12_15-11-30.png](attachments/image-2026-5-12_15-11-30.png) ![image-2026-5-12_15-9-51.png](attachments/image-2026-5-12_15-9-51.png) |
| Jave LocalDateTime ↔ ZonedDateTime | ![image-2026-5-12_15-33-1.png](attachments/image-2026-5-12_15-33-1.png) ![image-2026-5-12_15-4-46.png](attachments/image-2026-5-12_15-4-46.png) |