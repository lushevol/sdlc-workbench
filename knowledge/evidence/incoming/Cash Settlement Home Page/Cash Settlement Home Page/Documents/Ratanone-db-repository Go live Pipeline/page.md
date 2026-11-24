#

# New Feature Branch Base on develop Branch

Base on develop not main or master.

# Make Code Change In Your New Branch

Create two directories, one for Go live another for Rollback

![image-2025-9-11_9-19-29.png](attachments/image-2025-9-11_9-19-29.png)

# Pull Request Merge Your Branch To Develop Branch(Need PR Approval)

Merge to develop branch (Not main or master)

# Run Pipeline with develop Branch

1、Run pipeline with develop branch twice.

Firstly for Go live directory

![image-2025-9-11_9-22-41.png](attachments/image-2025-9-11_9-22-41.png)

Secondly for Rollback directory

![image-2025-9-11_9-23-21.png](attachments/image-2025-9-11_9-23-21.png)

2、Get the build package version from Artifactory

Get the Go live package version and Rollback package version in their own pipeline.

Go live package version for example:

[Pipelines - Run 20250910.4](https://dev.azure.com/sc-ado/FMQPR/_build/results?buildId=8113120&view=JFrog.jfrog-azure-devops-extension.artifactory-build-info-tab)

![image-2025-9-11_9-25-17.png](attachments/image-2025-9-11_9-25-17.png)

[JFrog](https://artifactory.global.standardchartered.com/ui/builds/51358-ratanone-db-repository_generic_pipeline/20250910.4/1757495565302/published?buildRepo=artifactory-build-info)

![image-2025-9-11_9-26-19.png](attachments/image-2025-9-11_9-26-19.png)

# Run Pipeline with main Branch

Run another pipeline with main branch and fill the two package versions

![image-2025-9-11_9-28-57.png](attachments/image-2025-9-11_9-28-57.png)

sample:

![image-2025-11-18_11-5-39.png](attachments/image-2025-11-18_11-5-39.png)

This is the Go live pipeline.