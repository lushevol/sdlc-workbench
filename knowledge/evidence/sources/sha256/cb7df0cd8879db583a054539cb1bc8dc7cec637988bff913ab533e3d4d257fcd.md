Open Search is going to be the business data storage strategic, and so far Cash Settlement, Flow Zero was designed to use Open Search as the main NOSQL database, the data visibility is required for easy querying data and statistics.

# Solution A - Open Search Dashboard

Official document: <u>[OpenSearch Dashboards - OpenSearch Documentation](https://docs.opensearch.org/latest/dashboards/)</u>

From capability prospective, Open Search dashboard is no difference with Kibana

# Solution B - DBever

## Step 1 - Download Driver

**Official Document: **

[JDBC driver - OpenSearch Documentation](https://docs.opensearch.org/latest/sql-and-ppl/sql/jdbc/)

**Download Page: **

[GitHub - opensearch-project/sql-jdbc: This is the driver for JDBC connectivity to a cluster running with OpenSearch SQL support.](https://github.com/opensearch-project/sql-jdbc)

**Jar file**:

You can get the jar from either GitHub and attached file, take as needed. Unzip the tar.gz and get the **opensearch-sql-jdbc-shadow-1.4.0.1.jar **under shadowJar folder

## Step 2 - Setup Connection

**1. The main tab information you can get all from 51358-ratanone-service-properties code repo. Below information is FMRP for reference.**

![image-2026-2-11_10-58-3.png](attachments/image-2026-2-11_10-58-3.png)

2.  **Click "Driver Settings" → "Libraries" → "Add File", choose opensearch-sql-jdbc-shadow-1.4.0.1.jar downloaded in step-1, click "OK", **

**![image-2026-2-11_11-5-25.png](attachments/image-2026-2-11_11-5-25.png)**

**3. Click "Driver properties", add 3 properties like below:**

trustSelfSigned = true

trustStoreLocation = C:\Users\1633330\certs\ssl\java\ratan_truststore_fmrp2.jks[Get it from server]

trustStorePassword = getFromConfiguration

**![image-2026-2-11_11-8-48.png](attachments/image-2026-2-11_11-8-48.png)**

**4. Test Connection**

**![image-2026-2-11_11-11-37.png](attachments/image-2026-2-11_11-11-37.png)**

**5. Explore the data with SQL like PG:**

**![image-2026-2-11_11-16-39.png](attachments/image-2026-2-11_11-16-39.png)**

## For more complex query please refer to the official document:

**[SQL - OpenSearch Documentation](https://docs.opensearch.org/latest/sql-and-ppl/sql/index/)**

BTW, The simple query and complex query are almost same with RDB SQL, but function has some difference, you can refer to the document above or ask AI if you don't want to read the boring line 1 by 1:)