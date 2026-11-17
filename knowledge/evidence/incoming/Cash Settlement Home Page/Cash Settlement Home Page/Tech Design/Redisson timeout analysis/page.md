# phenomenon

| type | Date | log |
| --- | --- | --- |
| application log | Jan 28th Jan 29th | redis_errors_writing_to_the_AOF_file_No_space_left_on_device_0 lifecycle [https://ratan-cashflow-lifecycle-service/v2/ratan/camunda/lifecycle/status/move--Unexpected](https://ratan-cashflow-lifecycle-service/v2/ratan/camunda/lifecycle/status/move--Unexpected) exception while processing command [https://ratan-cashflow-lifecycle-service/v2/ratan/camunda/lifecycle/status/move--Unable](https://ratan-cashflow-lifecycle-service/v2/ratan/camunda/lifecycle/status/move--Unable) to write command into connection! Check CPU usage of the JVM. Try to increase nettyThreads setting. Netty pending tasks: 0, Node source: NodeSource [slot=339, addr=null, redisClient=null, redirect=null, entry=null], connection: RedisConnection@846458253 [redisClient=[addr=[redis://10.198.24.59:6379,10.198.24.59/10.198.24.59:6379](redis://10.198.24.59:6379,10.198.24.59/10.198.24.59:6379)], channel=[id: 0xc9a1d99d, L:/10.198.24.248:48258 ! R:10.198.24.59/10.198.24.59:6379], currentCommand=null, usage=1], command: (EVALSHA, cached script: local currentTime = tonumber(ARGV[1]);local currentThread = ARGV[2];if (redis.call('hexists',KEYS[1], currentThread) > 0) then return 1;else return 0;end;return 1;), params: [eba07649a730cc1108b07ffaa8d8716589666772, 1, 19c50575-72a5-446b-af8c-3739f4ea8104{100}, 1769674914557, 7422554529732689920, 007313301431{100}] after 4 of 4 retry attempts [https://ratan-cashflow-lifecycle-service/v2/ratan/camunda/cashflow/preCheck--[500](https://ratan-cashflow-lifecycle-service/v2/ratan/camunda/cashflow/preCheck--[500) ] during [POST] to [[https://ratan-cashflow-lifecycle-service/v2/ratan/camunda/cashflow/preCheck](https://ratan-cashflow-lifecycle-service/v2/ratan/camunda/cashflow/preCheck)] [CommonServiceCaller#execute(URI,CamundaApiRequest)]: [{"status":500,"errorCode":"SERVICE_INTERNAL_ERROR","errorMessage":"Unable to write command into connection! Check CPU usage of the JVM. Try to increase nettyThreads setting. Netty pending tasks: 0, No... (922 bytes)] Query service Unable to write command into connection! Check CPU usage of the JVM. Try to increase nettyThreads setting. Netty pending tasks: 0, Node source: NodeSource [slot=339, addr=null, redisClient=null, redirect=null, entry=null], connection: RedisConnection@929579677 [redisClient=[addr=[redis://10.198.24.59:6379,10.198.24.59/10.198.24.59:6379](redis://10.198.24.59:6379,10.198.24.59/10.198.24.59:6379)] |
| redis log | T1 Jan 28th Jan 29th T2 Jan 29th | 2794370:M 28 Jan 2026 08:10:44.012794370:M 28 Jan 2026 08:13:42.013 # AOF write error looks solved, Redis can write again. 2794370:M 29 Jan 2026 09:36:47.512 # User requested shutdown... 321619:M 29 Jan 2026 09:37:46.589 * Ready to accept connections |

# Root cause

1. It only happened when connected to Redis node [redis://10.198.24.59:6379](redis://10.198.24.59:6379,10.198.24.59/10.198.24.59:6379). But no space in this server.
2. Redisson default retry config as below. If Redis encounter long shutdown, reconnection will be failed. | parameter | meaning | value | | --- | --- | --- | | retryAttempts | Error will be thrown if Redis command can't be sent to Redis server after retryAttempts. But if it sent successfully then timeout will be started | 4 | | reconnectionDelay | Defines the delay strategy for a new attempt to reconnect a connection. | EqualJitterDelay first time delay 100ms, the following delay is a random value between 100ms - 10s | | connectTimeout | Timeout during connecting to any Redis server | 10s | | retryDelay | Defines the delay strategy for a new attempt to send a command | same with reconnectionDelay | | keepAlive | TCP keepAlive for connection | false |

# Reproduce the issue

1. Startup the service, try to lock increased keys in a infinity loop
2. Stop the Redis cluster and wait 10mins
3. Log will show the same error

# Solution

1. Give up auto config in Redisson by default
2. Customize config parameters as below

| parameter | meaning | value |
| --- | --- | --- |
| retryAttempts | Error will be thrown if Redis command can't be sent to Redis server after retryAttempts. But if it sent successfully then timeout will be started | 4 |
| reconnectionDelay | Defines the delay strategy for a new attempt to reconnect a connection. | ConstantDelay 3s |
| connectTimeout | Timeout during connecting to any Redis server | 60 * 60 * 1000 |
| retryDelay | Defines the delay strategy for a new attempt to send a command | ConstantDelay 3s |
| keepAlive | TCP keepAlive for connection | **true** |

# Verification

1. Startup the service, try to lock increased keys in a infinity loop
2. Stop the Redis cluster and wait 2 hours
3. Log will show the same error
4. Start up Redis cluster after 10mins
5. The key operations are back to normal

**In downtime， one key will try 4 times by default,  exception will be throwed out when 4 failed attempts**

![image-2026-2-25_14-13-11.png](attachments/image-2026-2-25_14-13-11.png)

**After 2 hours, lock operation is back to normal,  service no need to restart**

![image-2026-2-25_14-16-46.png](attachments/image-2026-2-25_14-16-46.png)

| Config | |
| --- | --- |
| Default | Doesn't work |
| config.useClusterServers().addNodeAddress(nodes) .setPassword(redisProperties.getPassword()); | Doesn't work |
| config.useClusterServers().addNodeAddress(nodes) .setScanInterval(5000) .setRetryDelay(new ConstantDelay(Duration.ofSeconds(3))) .setReconnectionDelay(new ConstantDelay(Duration.ofSeconds(3))) .setConnectTimeout(10000) .setPassword(redisProperties.getPassword()); | Works |
| | |