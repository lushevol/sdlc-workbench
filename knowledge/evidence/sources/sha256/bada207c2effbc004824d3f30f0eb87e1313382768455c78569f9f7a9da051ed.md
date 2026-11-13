# Multi-Exception Handling Flow

##

# What is N+1 problem and how to resolve it?

## N+1 problem explanation

Say you query for a list of cashflows, and each cashflow includes multi-exceptions, and for each exception, there is a Stashing. Also the cashflow, exceptions and stashings are owned by different services which are query-service, exception-service and nstp-service. In a naïve implementation, to load 50 cashflows, you would have to call the exception service 50 times, once for each cashflow. This totals 51 queries: one query to get the list of cashflows, and 50 queries to get the exception data for each cashflow. This obviously wouldn’t perform very well. Assume in the future maybe 1 exception has multi-stashing or some other children objectd, the query time will be grown exponentially.

It would be much more efficient to create a list of exception to load, and load all of them at once in a single call. This first of all must be supported by the exception service, because that service needs to provide a way to load a list of exception. The data fetchers in the query-service need to be smart as well, to take care of batching the requests to the exception service, even nstp-service.

This is where data loaders come in.

Solution

[https://netflix.github.io/dgs/data-loaders/](https://netflix.github.io/dgs/data-loaders/)

DGS Framework provided a solution named Data Loaders which is responsible for loading data for a given list of keys. In this example, it just passes on the list of keys to the backend that owns exception.  there is no logic needs to be implement manually about how to make batching works so it is transparent to developers. this is all handled by the framework! The framework will recognize that many directors need to be loaded when many movies are loaded, batch up all the calls to the data loader, and call the data loader with a list of IDs instead of a single ID. The data loader implemented above already knows how to handle a list of IDs, and that way it avoids the N+1 problem.

# Bulk Exception Handling Preview Query Sample:

# Bulk Exception Handling Sample - Orchestration Service

## **Submit **

### **Request Sample**

**Post: **[http://localhost:8080/v2/camunda/task/NSTPSSI/maker](http://localhost:8080/v2/camunda/task/NSTPSSI/maker)

### **Response sample:**

## **Reject**

### **Request Sample**

**Post: **[http://localhost:8080/v2/camunda/task/NSTPSSI/c](http://localhost:8080/v2/camunda/task/NSTPSSI/maker)hecker

### Response sample:

# Threshold as 1000 bulk affirmation exception resolve.

When threshold extend from 100 to 1000, we found the performance is not that good.

| | Case | Count | API | Thread Pool | DB pool | Solution / Change | Cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 100 cashflows in a single batch and verify the checker under 20 core threads | 100 | checker | app thread pool: core thread size: 20 max thread size: 50 queue capacity: 10000 | | | 22.84 |
| 2 | 1000 cashflows in a single batch and verify the checker under 20 core threads | 1000 | checker | app thread pool: core thread size: 20 max thread size: 50 queue capacity: 10000 | | | 210 （10X） |
| 3 | 1000 cashflows in a single batch and verify the checker under 50 core threads | 1000 | checker | app thread pool: core thread size: 50 max thread size: 50 queue capacity: 10000 | | | 132 |
| 4 | 50 per batch by backend service and utilize all the live instances capability | 1000 | checker | app thread pool: core thread size: 50 max thread size: 50 queue capacity: 10000 | db thread pool: minimumIdle: 4maximumPoolSize: 50 | backend divided into 20 batches, with 50 cashflows in each batch | 70 |

We decided to utilize the all the instance to balance the load as enhancement.