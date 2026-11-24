#

# 1 Appearance

Issue：

There is delay when trade service consumes the message on EKS ENV and UAT ENV can work well.

![image2024-3-21_11-33-20.png](attachments/image2024-3-21_11-33-20.png)

# 2 Analysis

Find log to show consumer poll timeout has expired.

| Mar 19, 2024 @ 17:09:02.860 | log: {"@timestamp":"2024-03-19T09:09:02.859Z","sequence":323166,"level":"WARN","logger_name":"org.apache.kafka.clients.consumer.internals.ConsumerCoordinator","hostname":"ratanone-trade-service-594979864d-2ggxh","appName":"ratanone-trade-service","port":"8080","PID":"7","thread":"kafka-coordinator-heartbeat-thread | ratanone-trade-service-fx-replicate","message":"[Consumer clientId=consumer-ratanone-trade-service-fx-replicate-2, groupId=ratanone-trade-service-fx-replicate] consumer poll timeout has expired. This means the time between subsequent calls to poll() was longer than the configured [max.poll.interval.ms](http://max.poll.interval.ms), which typically implies that the poll loop is spending too much time processing messages. You can address this either by increasing [max.poll.interval.ms](http://max.poll.interval.ms) or by reducing the maximum size of batches returned in poll() with max.poll.records."} |
| --- | --- |

a)   Too Many data sent from TDS3 to Kafka

b)   The performance provided by EKS resources is inferior to that of UAT environments.  （From dev view）

c） new trade process  ( fx-replication) is complex than before ([Replay Function Testing Operation - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/pages/viewpage.action?spaceKey=DSP&title=Replay+Function+Testing+Operation))

# 3 Proposal

Only do Business testing on EKS Env with small data volume

Change Kafka setting for different ENV for ensure that Kafka's messages can be always consumed.

# 4 Solution

customization setting for Kafka

kafka:
       properties:
[             max.poll.interval.ms](http://max.poll.interval.ms): xxxxx
[             session.timeout.ms](http://session.timeout.ms): xxxxx

# 5 Action

a）short-term action

| Service name | optimize point | owner | process | note |
| --- | --- | --- | --- | --- |
| Trade service | Trade service modify the application.yml to add properties and then do one testing kafka: properties: [ max.poll.interval.ms](http://max.poll.interval.ms): xxxxx [ session.timeout.ms](http://session.timeout.ms): xxxxx | ben /hawk | already change setting and deployed to EKS | testing so far so good ![image2024-3-22_13-56-19.png](attachments/image2024-3-22_13-56-19.png) ![image2024-3-22_13-57-45.png](attachments/image2024-3-22_13-57-45.png) ![image2024-3-22_13-58-40.png](attachments/image2024-3-22_13-58-40.png) ![image2024-3-22_14-1-58.png](attachments/image2024-3-22_14-1-58.png) |
| | Consider to optimizing the performance of the trade fx-replication part How to optimize: use rule service to parse the scbml to Json, since rule service upgrade to new library from TDS3 which use to parse the scbml. | ben /hawk | already deploy to EKS and Staging. | ![image2024-3-28_13-40-48.png](attachments/image2024-3-28_13-40-48.png) |

b) long-term action

| Service name | properties | owner | process | note |
| --- | --- | --- | --- | --- |
| Application service which need to recover the properties value | kafka: properties: [ max.poll.interval.ms](http://max.poll.interval.ms): xxxxx [ session.timeout.ms](http://session.timeout.ms): xxxxx | deliver lead/Owner | | |

# Conclusion

Drop3 migration testing rerun from 5/9 , there are no lag or delay for the trade service after the optimizing, So the issue should be fixed, and we will close this topic.

![image2024-5-10_9-51-59.png](attachments/image2024-5-10_9-51-59.png)