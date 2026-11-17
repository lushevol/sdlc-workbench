#Common information should aligned same as which in CMDB

#Server type, /Service Activated/Status(active/passive/load balance)/Comments which does not exist in CMDB, need to input separately

| **Application ID** | **Application** | **Hostname** | **Server Type** | **BUSINESS CRITICALITY** | **Environment** | **DC Centre** | **Virtual** | **IP Address** | **Relevant APPs** | **Service Activated** | **Status(active/passive/load balance)** | **RAM** | **# of CPU** | **# of Core per CPU** | **# of Thread per Core** | **Host Type** | **Operating System** | **Comments** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 36250 | FM-BPMS-FRTP | uklvdpfrt002a | <VDaaS/ DaaS/ local/app server> | 3-Medium | Production | FARNBOROUGH | Virtual | 10.4.138.44 | FM-BPMS-FRTP | <YES/NO> | active | 128GB | 16 | 1 | 1 | Linux Server | Linux Red Hat - 8.10 | < DB server/list service details for app server > |

##Checklist to move server to production status

| Question / Checklist | Requirements / Notes | Response with Evidence |
| --- | --- | --- |
| Architecture and Design | Architecture Diagram | |
| | Cluster Setup Diagram, | |
| | Network Diagram | |
| | Production and non-production environments should have equivalent configurations | |
| Server level checks | Latest supported OS and software version | |
| | Open files: Soft and hard limits for nofile must be at least 65535 ulimit -S -n ulimit -H -n | |
| | Maximum processes: Soft and hard limits for nproc must be appropriate for the application ulimit -S -u >32768 ulimit -H -u >65535 | |
| | Core dump file size: ulimit -c = 0 | |
| | Data segment size: Application-specific, unlimited by default ulimit -d | |
| | File size limit: Application-specific , unlimited by default ulimit -f | |
| | CPU time limit: Application-specific , unlimited by default ulimit -t | |
| | File creation permissions: The application ID should use umask 0022 | |
| CPU/Memory/Disk Space | For an existing application, compare the allocation with the existing server and document any differences. | |
| | For a new application, confirm that the allocated resources are appropriate for the business requirements. | |
| | Confirm that all required mount points are configured. | |
| | Confirm that the time zone is correct(UTC). | |
| | Confirm that the server hostname, IP address(check if to be in same vlan), and FQDN are correctly registered. | |
| | Confirm that DNS forward and reverse resolution are working. | |
| Centrify Configuration | Existing application, Add the new server to the existing Centrify computer group. | |
| | New application, Create a new user group and server group. Add the required servers and users to the appropriate groups. | |
| | APP-Security related confluence update(sample:[RATAN -Security - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/RATAN+-Security)) | |
| Mandatory Software | ITRS, | |
| | ElasticAgent | |
| | Control-M | |
| | Airflow | |
| Monitoring | Confirm that the required ITRS license is available. | |
| | Complete COP onboarding. | |
| | Enable and validate ITRS and COP monitoring on infra related monitoring | |
| | Server configured to FM capacity tool | |
| Maintenance | Share maintenance window information | |
| | Confirm whether automatic reboot is enabled. | |
| | Confirm whether automatic Patching is enabled. | |
| | Configure and test automatic application startup after server reboot. | |
| | Define and test the recovery and restore procedures. | |
| | Confirm the backup policy.(backup schedule and time, if any conflict with application working hour) | |
| Documents update | ASRM | |
| | Test environment spec | |
| | Asset inventory confluence update ([BPMS Server Inventory - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/BPMS+Server+Inventory)) | |
| | CMDB Update | |
| SAT Approval | | |
| OAT Approval | | |

**
**##Addon list to deploy service to server

| Question / Checklist | Requirements / Notes | Response with Evidence |
| --- | --- | --- |
| SSH Access | Rundeck key | |
| | ADO key | |
| Firewall | Confirm that all required firewall rules have been configured. 1 Between application servers 2 Between application server and DB/ITRS/control-M etc.. 3 Between application server and relevant up/downstream 3 Between application server and relevant external systems | |
| | Share the firewall details with PSS. | |
| Identity and Access Management | List the application IDs and confirm their vaulting status. | |
| | Update the same information on the PSS Confluence page. (sample :[RATAN -Security - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/RATAN+-Security)) | |
| | Enable read-only login access for PSS. | |
| | Confirm that the read-only account has only the required permissions. | |