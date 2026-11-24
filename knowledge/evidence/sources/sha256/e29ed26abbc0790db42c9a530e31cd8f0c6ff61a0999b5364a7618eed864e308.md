#

# Open Mock SSI Config

Location: 51358-ratan-service-properties repository and staging-master branch and application-staging.yml file

[application-staging.yml - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-service-properties?path=/config-repo/application-staging.yml&version=GBstaging-master&_a=contents)

# SSI MOCK

SSIPLUS_HOST: 10.198.199.160:9200
SSIPLUS_INDEX: index-ssi-goldensource-logstash-v5
SSIPLUS_CLUSTER: RatanRT-ES-Cluster
SSIPLUS_NODE: uklvadapp1340

# SSI UAT

SSIPLUS_HOST: 10.198.37.147:9200,10.198.37.148:9200
SSIPLUS_INDEX: index-ssi-goldensource-logstash-v5
SSIPLUS_CLUSTER: scanner
SSIPLUS_NODE: scanner-uat
# Run Develop Branch Pipeline

[Pipelines - Runs for 51358-ratan-service-properties_generic_pipeline](https://dev.azure.com/sc-ado/FMQPR/_build?definitionId=13289)

![image-2025-9-10_22-57-41.png](attachments/image-2025-9-10_22-57-41.png)

# Get Package Version

[Pipelines - Run 20250910.4 logs](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8111588&view=logs&j=2831d33e-84dd-5533-eda0-8105954f1bc8&t=95821634-ff70-5c13-fcfb-9d8a5d21f8ed)

![image-2025-9-10_22-59-5.png](attachments/image-2025-9-10_22-59-5.png)

# Deploy By Rundeck

[https://devrundeck.gdc.standardchartered.com/selfservice/project/RATANRT/job/show/dab42927-dace-4956-8bcf-7e2c0225c16b](https://devrundeck.gdc.standardchartered.com/selfservice/project/RATANRT/job/show/dab42927-dace-4956-8bcf-7e2c0225c16b)

Copy one from activity

![image-2025-10-13_11-52-29.png](attachments/image-2025-10-13_11-52-29.png)

![image-2025-9-10_23-2-29.png](attachments/image-2025-9-10_23-2-29.png)

# Restart Data Ambassador By Rundeck

[Jobs - RATANRT](https://devrundeck.gdc.standardchartered.com/selfservice/project/RATANRT/jobs)

![image-2025-9-10_23-3-37.png](attachments/image-2025-9-10_23-3-37.png)

![image-2025-9-10_23-4-31.png](attachments/image-2025-9-10_23-4-31.png)

![image-2025-9-10_23-5-3.png](attachments/image-2025-9-10_23-5-3.png)

# Reverse Operation

Open the UAT SSI config in Step 1 and repeat the remaining operations.