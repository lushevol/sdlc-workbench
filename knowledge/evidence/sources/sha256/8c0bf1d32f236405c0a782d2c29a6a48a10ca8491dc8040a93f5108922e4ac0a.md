###

### Background

We encounter slow query  on prod environment frequently, and most of them due to the slow SQL in PostgreSQL. So it's necessary to take a deep dive on it. The 'Explain' result shows the details of a execute plan, so understand 'Explain' in PostgreSQL is a good beginning.

### Overview of query lifecycle

![image (1).png](attachments/image (1).png)

> **INFO**
> Most of popular RDBMS such as Oracle、MySQL、PostgreSQL have different query lifecycle implementation, but have similar phases and functions.

#### 1.Parser

The parser generates a parse tree from an SQL statement in plain text.(grammar validation)

![image-2025-5-14_11-10-51.png](attachments/image-2025-5-14_11-10-51.png)

```cpp
typedef struct SelectStmt
{
        NodeTag         type;

        /*
         * These fields are used only in "leaf" SelectStmts.
         */
        List       *distinctClause;     /* NULL, list of DISTINCT ON exprs, or
                                         * lcons(NIL,NIL) for all (SELECT DISTINCT) */
        IntoClause *intoClause;         /* target for SELECT INTO */
        List       *targetList;         /* the target list (of ResTarget) */
        List       *fromClause;         /* the FROM clause */
        Node       *whereClause;        /* WHERE qualification */
        List       *groupClause;        /* GROUP BY clauses */
        Node       *havingClause;       /* HAVING conditional-expression */
        List       *windowClause;       /* WINDOW window_name AS (...), ... */

        /*
         * In a "leaf" node representing a VALUES list, the above fields are all
         * null, and instead this field is set.  Note that the elements of the
         * sublists are just expressions, without ResTarget decoration. Also note
         * that a list element can be DEFAULT (represented as a SetToDefault
         * node), regardless of the context of the VALUES list. It's up to parse
         * analysis to reject that where not valid.
         */
        List       *valuesLists;        /* untransformed list of expression lists */

        /*
         * These fields are used in both "leaf" SelectStmts and upper-level
         * SelectStmts.
         */
        List       *sortClause;         /* sort clause (a list of SortBy's) */
        Node       *limitOffset;        /* # of result tuples to skip */
        Node       *limitCount;         /* # of result tuples to return */
        List       *lockingClause;      /* FOR UPDATE (list of LockingClause's) */
        WithClause *withClause;         /* WITH clause */

        /*
         * These fields are used only in upper-level SelectStmts.
         */
        SetOperation op;                /* type of set op */
        bool            all;            /* ALL specified? */
        struct SelectStmt *larg;        /* left child */
        struct SelectStmt *rarg;        /* right child */
        /* Eventually add fields for CORRESPONDING spec here */
} SelectStmt;
```

![fig-3-02.png](attachments/fig-3-02.png)

#### 2. Analyzer/Analyser

The analyzer/analyser carries out a semantic analysis of a parse tree and generates a query tree.(semantic analysis)

```cpp
/*
 * Query -
 *	  Parse analysis turns all statements into a Query tree
 *	  for further processing by the rewriter and planner.
 *
 *	  Utility statements (i.e. non-optimizable statements) have the
 *	  utilityStmt field set, and the Query itself is mostly dummy.
 *	  DECLARE CURSOR is a special case: it is represented like a SELECT,
 *	  but the original DeclareCursorStmt is stored in utilityStmt.
 *
 *	  Planning converts a Query tree into a Plan tree headed by a PlannedStmt
 *	  node --- the Query structure is not used by the executor.
 */
typedef struct Query
{
	NodeTag		type;

	CmdType		commandType;	/* select|insert|update|delete|merge|utility */

	/* where did I come from? */
	QuerySource querySource pg_node_attr(query_jumble_ignore);

	/*
	 * query identifier (can be set by plugins); ignored for equal, as it
	 * might not be set; also not stored.  This is the result of the query
	 * jumble, hence ignored.
	 */
	uint64		queryId pg_node_attr(equal_ignore, query_jumble_ignore, read_write_ignore, read_as(0));

	/* do I set the command result tag? */
	bool		canSetTag pg_node_attr(query_jumble_ignore);

	Node	   *utilityStmt;	/* non-null if commandType == CMD_UTILITY */

	/*
	 * rtable index of target relation for INSERT/UPDATE/DELETE/MERGE; 0 for
	 * SELECT.  This is ignored in the query jumble as unrelated to the
	 * compilation of the query ID.
	 */
	int			resultRelation pg_node_attr(query_jumble_ignore);

	/* has aggregates in tlist or havingQual */
	bool		hasAggs pg_node_attr(query_jumble_ignore);
	/* has window functions in tlist */
	bool		hasWindowFuncs pg_node_attr(query_jumble_ignore);
	/* has set-returning functions in tlist */
	bool		hasTargetSRFs pg_node_attr(query_jumble_ignore);
	/* has subquery SubLink */
	bool		hasSubLinks pg_node_attr(query_jumble_ignore);
	/* distinctClause is from DISTINCT ON */
	bool		hasDistinctOn pg_node_attr(query_jumble_ignore);
	/* WITH RECURSIVE was specified */
	bool		hasRecursive pg_node_attr(query_jumble_ignore);
	/* has INSERT/UPDATE/DELETE in WITH */
	bool		hasModifyingCTE pg_node_attr(query_jumble_ignore);
	/* FOR [KEY] UPDATE/SHARE was specified */
	bool		hasForUpdate pg_node_attr(query_jumble_ignore);
	/* rewriter has applied some RLS policy */
	bool		hasRowSecurity pg_node_attr(query_jumble_ignore);
	/* is a RETURN statement */
	bool		isReturn pg_node_attr(query_jumble_ignore);

	List	   *cteList;		/* WITH list (of CommonTableExpr's) */

	List	   *rtable;			/* list of range table entries */

	/*
	 * list of RTEPermissionInfo nodes for the rtable entries having
	 * perminfoindex > 0
	 */
	List	   *rteperminfos pg_node_attr(query_jumble_ignore);
	FromExpr   *jointree;		/* table join tree (FROM and WHERE clauses);
								 * also USING clause for MERGE */

	List	   *mergeActionList;	/* list of actions for MERGE (only) */
	/* whether to use outer join */
	bool		mergeUseOuterJoin pg_node_attr(query_jumble_ignore);

	List	   *targetList;		/* target list (of TargetEntry) */

	/* OVERRIDING clause */
	OverridingKind override pg_node_attr(query_jumble_ignore);

	OnConflictExpr *onConflict; /* ON CONFLICT DO [NOTHING | UPDATE] */

	List	   *returningList;	/* return-values list (of TargetEntry) */

	List	   *groupClause;	/* a list of SortGroupClause's */
	bool		groupDistinct;	/* is the group by clause distinct? */

	List	   *groupingSets;	/* a list of GroupingSet's if present */

	Node	   *havingQual;		/* qualifications applied to groups */

	List	   *windowClause;	/* a list of WindowClause's */

	List	   *distinctClause; /* a list of SortGroupClause's */

	List	   *sortClause;		/* a list of SortGroupClause's */

	Node	   *limitOffset;	/* # of result tuples to skip (int8 expr) */
	Node	   *limitCount;		/* # of result tuples to return (int8 expr) */
	LimitOption limitOption;	/* limit type */

	List	   *rowMarks;		/* a list of RowMarkClause's */

	Node	   *setOperations;	/* set-operation tree if this is top level of
								 * a UNION/INTERSECT/EXCEPT query */

	/*
	 * A list of pg_constraint OIDs that the query depends on to be
	 * semantically valid
	 */
	List	   *constraintDeps pg_node_attr(query_jumble_ignore);

	/* a list of WithCheckOption's (added during rewrite) */
	List	   *withCheckOptions pg_node_attr(query_jumble_ignore);

	/*
	 * The following two fields identify the portion of the source text string
	 * containing this query.  They are typically only populated in top-level
	 * Queries, not in sub-queries.  When not set, they might both be zero, or
	 * both be -1 meaning "unknown".
	 */
	/* start location, or -1 if unknown */
	int			stmt_location;
	/* length in bytes; 0 means "rest of string" */
	int			stmt_len pg_node_attr(query_jumble_ignore);
} Query;
```

![fig-3-03.png](attachments/fig-3-03.png)

#### 3.Rewriter

The rewriter transforms a query tree using the rules stored in the [rule system](http://www.postgresql.org/docs/current/static/rules.html) if such rules exist.(rules(e.g. views) apply)

![image-2025-5-14_11-16-53.png](attachments/image-2025-5-14_11-16-53.png)

![image-2025-5-14_11-17-19.png](attachments/image-2025-5-14_11-17-19.png)

![fig-3-04.png](attachments/fig-3-04.png)

#### 4.Planner

The planner generates the plan tree that can most effectively be executed from the query tree.

The planner in PostgreSQL is based on **pure cost-based optimization.** It **does not support rule-based optimization or [hints](https://pg-hint-plan.readthedocs.io/_/downloads/en/pg15/pdf/)**. This planner is the most complex subsystem in PostgreSQL.

![image-2025-5-14_11-19-42.png](attachments/image-2025-5-14_11-19-42.png)

```cpp
typedef struct PlannedStmt
{
	pg_node_attr(no_equal, no_query_jumble)

	NodeTag		type;

	CmdType		commandType;	/* select|insert|update|delete|merge|utility */

	uint64		queryId;		/* query identifier (copied from Query) */

	bool		hasReturning;	/* is it insert|update|delete RETURNING? */

	bool		hasModifyingCTE;	/* has insert|update|delete in WITH? */

	bool		canSetTag;		/* do I set the command result tag? */

	bool		transientPlan;	/* redo plan when TransactionXmin changes? */

	bool		dependsOnRole;	/* is plan specific to current role? */

	bool		parallelModeNeeded; /* parallel mode required to execute? */

	int			jitFlags;		/* which forms of JIT should be performed */

	struct Plan *planTree;		/* tree of Plan nodes */

	List	   *rtable;			/* list of RangeTblEntry nodes */

	List	   *permInfos;		/* list of RTEPermissionInfo nodes for rtable
								 * entries needing one */

	/* rtable indexes of target relations for INSERT/UPDATE/DELETE/MERGE */
	List	   *resultRelations;	/* integer list of RT indexes, or NIL */

	List	   *appendRelations;	/* list of AppendRelInfo nodes */

	List	   *subplans;		/* Plan trees for SubPlan expressions; note
								 * that some could be NULL */

	Bitmapset  *rewindPlanIDs;	/* indices of subplans that require REWIND */

	List	   *rowMarks;		/* a list of PlanRowMark's */

	List	   *relationOids;	/* OIDs of relations the plan depends on */

	List	   *invalItems;		/* other dependencies, as PlanInvalItems */

	List	   *paramExecTypes; /* type OIDs for PARAM_EXEC Params */

	Node	   *utilityStmt;	/* non-null if this is utility stmt */

	/* statement location in source string (copied from Query) */
	int			stmt_location;	/* start location, or -1 if unknown */
	int			stmt_len;		/* length in bytes; 0 means "rest of string" */
} PlannedStmt;
```

![fig-3-05.png](attachments/fig-3-05.png)

> **INFO**
> Mistake in The internals of PostgreSQL: 'List *plantree' in the figure above should be* '*struct Plan  *plantree' according to the source code.

#### 5.Executor

The executor executes the query by accessing the tables and indexes in the order that was created by the plan tree.

Each plan node has information that the executor requires for processing. In the case of a **single-table query**, the executor processes** from the end of the plan tree to the root**.

For example, the plan tree shown above is a list of a sort node and a sequential scan node. Therefore, the executor scans the table *tbl_a* by a **sequential scan** and **then sorts **the obtained result.

The executor reads and writes tables and indexes in the database cluster via the **buffer manager**. When processing a query, the executor uses some memory areas, such as **temp_buffers **and **work_mem**, **allocated in advance** and creates **temporary files **if necessary.

![fig-3-06.png](attachments/fig-3-06.png)

sort node receives tuples **one by one** from the scan node, then sorts them in ***work_mem ***buffer.

![fig-3-16.png](attachments/fig-3-16.png)

#### Memory Use Constants

`shared_buffers` (`integer`)

Sets the amount of memory the database server uses for shared memory buffers.

`temp_buffers` (`integer`)

Sets the maximum amount of memory used for temporary buffers within each database session. These are session-local buffers used only for access to temporary tables.

`work_mem` (`integer`)

Sets the base maximum amount of memory to be used by a query operation (such as a sort or hash table) before writing to temporary disk files.

### Explain output Structure

The structure of a query plan is a tree of *plan nodes*. Nodes at the **bottom level of the tree **are scan nodes: they return raw rows from a table.

There are different types of scan nodes for different table access methods:

- sequential scans
- index scans
- bitmap index scans
- There are also non-table row sources, such as `VALUES` clauses and set-returning functions in `FROM`, which have their own scan node types.

SELECT * FROM (VALUES (1, 'Alice'), (2, 'Bob')) AS t(id, name);

SELECT * FROM generate_series(1, 5);

If the query requires joining, aggregation, sorting, or other operations on the raw rows, then there will be additional nodes above the scan nodes to perform these operations.

The output of `EXPLAIN` has **one line for each node** in the plan tree, showing the **basic node type plus the cost estimates** that the planner made for the execution of that plan node.

Additional lines might appear, indented from the node's summary line, to show additional properties of the node.

Here is a trivial example, just to show what the output looks like:

![image-2025-5-9_17-10-22.png](attachments/image-2025-5-9_17-10-22.png)

There are three kinds of costs: start-up, run and total. The total cost is the sum of the start-up and run costs, so only the start-up and run costs are independently estimated.

- The **start-up** cost is the cost expended before the first tuple is fetched. For example, the start-up cost of the index scan node is the cost of reading index pages to access the first tuple in the target table.(So in sequential scan, start-up cost always 0 )
- The **run** cost is the cost of fetching all tuples.
- The **total** cost is the sum of the costs of both start-up and run costs.

The costs are **measured in arbitrary units** determined by the planner's cost parameters (see [Section 20.7.2](https://www.postgresql.org/docs/14/runtime-config-query.html#RUNTIME-CONFIG-QUERY-CONSTANTS)). Traditional practice is to measure the costs in units of disk page fetches; that is, **[seq_page_cost](https://www.postgresql.org/docs/14/runtime-config-query.html#GUC-SEQ-PAGE-COST) is conventionally set to `1.0`** and the other cost parameters are set relative to that. The examples is run with the default cost parameters.

Illustration：

- The cost of an upper-level node includes the cost of all its child nodes.
- The cost only reflects things that the planner cares about.
- The cost does not consider the time spent transmitting result rows to the client, which could be an important factor in the real elapsed time; but the planner ignores it because it cannot change it by altering the plan. (Every correct plan will output the same row set, we trust.)
- The `rows` value is a little tricky because it is not the number of rows processed or scanned by the plan node, but rather the number emitted by the node. This is often less than the number scanned, as a result of filtering by any `WHERE`-clause conditions that are being applied at the node.

### Planner Cost Constants

The *cost* variables described are measured on an arbitrary scale.** Only their relative values matter, **hence scaling them all up or down by the same factor will result in no change in the planner's choices.

Commonly, we consider **index scan using random io access**, as well as **seq scan using  sequential io access; **random io access is always more expensive than sequential io access.

`***seq_page_cost ***(`floating point`)`

Sets the planner's estimate of the cost of a disk page fetch that is part of a series of sequential fetches. The default is 1.0. This value can be overridden for tables and indexes in a particular tablespace by setting the tablespace parameter of the same name (see [ALTER TABLESPACE](https://www.postgresql.org/docs/14/sql-altertablespace.html)).

`***random_page_cost ***(`floating point`)`

Sets the planner's estimate of the cost of a non-sequentially-fetched disk page. The default is 4.0. This value can be overridden for tables and indexes in a particular tablespace by setting the tablespace parameter of the same name (see [ALTER TABLESPACE](https://www.postgresql.org/docs/14/sql-altertablespace.html)).

Reducing this value relative to `seq_page_cost` will cause the system to prefer index scans; raising it will make index scans look relatively more expensive. You can raise or lower both values together to change the importance of disk I/O costs relative to CPU costs, which are described by the following parameters.

Random access to mechanical disk storage is normally much more expensive than four times sequential access. However, a lower default is used (4.0) because the majority of random accesses to disk, such as indexed reads, are assumed to be in cache. The default value can be thought of as modeling random access as **40 times** slower than sequential, while expecting 90% of random reads to be cached.

If you believe a 90% cache rate is an incorrect assumption for your workload, you can increase `random_page_cost `to better reflect the true cost of random storage reads. Correspondingly, if your data is likely to be completely in cache, such as when the database is smaller than the total server memory, decreasing `random_page_cost `can be appropriate. Storage that has a low random read cost relative to sequential, e.g., solid-state drives, might also be better modeled with a lower value for `random_page_cost`, e.g., `1.1`.

***`cpu_tuple_cost` ***(`floating point`)

Sets the planner's estimate of the cost of processing each row during a query. The default is 0.01.

***`cpu_index_tuple_cost` ***(`floating point`)

Sets the planner's estimate of the cost of processing each index entry during an index scan. The default is 0.005.

***`cpu_operator_cost` ***(`floating point`)

Sets the planner's estimate of the cost of processing each operator or function executed during a query. The default is 0.0025.

### Cost Estimation in Single-Table Query

#### Sequential Scan

The cost of the sequential scan is estimated by the cost_seqscan() function. We will explore how to estimate the sequential scan cost of the following query:

![image-2025-5-13_15-33-47.png](attachments/image-2025-5-13_15-33-47.png)

In the sequential scan, the start-up cost is equal to 0, and the run cost is defined by the following equation:

'run cost' = 'cpu run cost' + 'disk run cost' = (cpu_tuple_cost + cpu_operator_cost) × *N<sub>tuple </sub>*+ seq_page_cost × *N<sub>page</sub>*

where *[seq_page_cost](https://www.postgresql.org/docs/current/static/runtime-config-query.html#GUC-SEQ-PAGE-COST)*, *[cpu_tuple_cost](https://www.postgresql.org/docs/current/static/runtime-config-query.html#GUC-CPU-TUPLE-COST) *and *[cpu_operator_cost](https://www.postgresql.org/docs/current/static/runtime-config-query.html#GUC-CPU-OPERATOR-COST) *are list in previous section, and the default values are 1.0, 0.01, and 0.0025, respectively. *N*<sub>tuple</sub> and *N*<sub>page</sub> are the numbers of all tuples and all pages of this table, respectively.

These numbers can be shown using the following query:

![image-2025-5-13_15-34-10.png](attachments/image-2025-5-13_15-34-10.png)

Therefore,

'run cost' = (0.001 + 0.0025) * 10000 + 1.0 * 45 = 170.0

Finally,

'total cost' = 0.0 + 170.0 = 170

![image-2025-5-13_15-34-43.png](attachments/image-2025-5-13_15-34-43.png)

**As understood from the run-cost estimation, PostgreSQL assumes that all pages will be read from storage.** In other words, PostgreSQL does not consider whether the scanned page is in the shared buffers or not.

#### Index Scan

We explore how to estimate the index scan cost of the following query:

![image-2025-5-13_15-36-17.png](attachments/image-2025-5-13_15-36-17.png)

the numbers of the index pages and index tuples, *N<sub>index,page</sub>* and *N<sub>index,tuple</sub>* are shown below:

![image-2025-5-13_15-39-11.png](attachments/image-2025-5-13_15-39-11.png)

##### Start-Up Cost

The start-up cost of the index scan is the cost of reading the index pages to access the first tuple in the target table. It is defined by the following equation:

'start-up cost' = {ceil(log<sub>2</sub>(*N*<sub>*index,tuple*</sub>)) + (*H<sub>index</sub>* + 1) * 50* *} **  *cpu_operator_cost

where *H<sub>index</sub>* is the height of the index tree. The detail of this calculation is explained in the comments of [btcostestimate()](https://github.com/postgres/postgres/blob/ef6e028f05b3e4ab23c5edfdfff457e0d2a649f6/src/backend/utils/adt/selfuncs.c#L7022).

Therefore,

'start-up cost' = {ceil(log<sub>2</sub>(10000)) + (1 + 1) * 50}  * 0.00025 = 0.285

##### Run Cost

The run cost of the index scan is the sum of the CPU costs and the I/O (input/output) costs of both the table and the index:

'run_cost' = ('index cpu cost' + 'table cpu cost') + ('index IO cost' + 'table IO cost') = 13.2

details refer to: [https://www.interdb.jp/pg/pgsql03/02.html#3222-run-cost](https://www.interdb.jp/pg/pgsql03/02.html#3222-run-cost)

anyway, the  cpu cost is related to the `cpu_tuple_cost `and `cpu_index_tuple_cost`*,* the IO cost is related to the `random_page_cost `constants.

##### Total Cost

‘total_cost’ = 0.285 + 13.2 = 13.485

![image-2025-5-13_16-3-49.png](attachments/image-2025-5-13_16-3-49.png)

#### Sort

The sort path is used for sorting operations, such as ORDER BY, the preprocessing of merge join operations, and other functions. The cost of sorting is estimated using the `cost_sort`() function.

details refer to: [https://www.interdb.jp/pg/pgsql03/02.html#323-sort](https://www.interdb.jp/pg/pgsql03/02.html#323-sort)

anyway, it related to the *cpu_operator_cost *constant.

### Continue Explain

#### Why the cost goes up?

Returning to our example:

you will find that `tenk1` has 358 disk pages and 10000 rows. The estimated **run **cost is computed as(separate way from different book.)

1. **'run cost' = 'cpu run cost' + ‘disk run cost’ = (`cpu_tuple_cost `+ `cpu_operator_cost`) * *N<sub>tupe </sub>+ `seq_page_cost `* N*<sub>page ([3.2. Cost Estimation in Single-Table Query :: Hironobu SUZUKI @ InterDB](https://www.interdb.jp/pg/pgsql03/02.html))</sub>**
2. **'run_cost' = 'cpu run cost' + ‘disk run cost’ = (`[cpu_tuple_cost](https://www.postgresql.org/docs/14/runtime-config-query.html#GUC-CPU-TUPLE-COST) * `*rows scanned ) + ( `[seq_page_cost](https://www.postgresql.org/docs/14/runtime-config-query.html#GUC-SEQ-PAGE-COST) `** disk pages read) ([PostgreSQL: Documentation: 14: 14.1. Using EXPLAIN](https://www.postgresql.org/docs/14/using-explain.html))**

I think maybe #1 is closer to reality.

By default, `seq_page_cost` is 1.0 and `cpu_tuple_cost` is 0.01, so the 'total cost' estimated is (358 * 1.0) + (10000 * 0.01) = 458.

Now let's modify the query to add a `WHERE` condition:

![image-2025-5-12_15-15-55.png](attachments/image-2025-5-12_15-15-55.png)

Notice that the `EXPLAIN` output shows the `WHERE` clause being applied as a “**filter**” condition attached to the Seq Scan plan node. This **means that the plan node checks the condition for each row it scans**, and outputs only the ones that pass the condition. The estimate of output rows has been reduced because of the `WHERE` clause. However, the scan will still have to visit all 10000 rows, so the cost hasn't decreased; in fact it has gone up a bit (by 10000 * `cpu_operator_cost`, to be exact) to reflect the extra CPU time spent checking the `WHERE` condition.

Now, let's make the condition more restrictive:

![image-2025-5-12_17-54-52.png](attachments/image-2025-5-12_17-54-52.png)

Here the planner has decided to use a two-step plan: the child plan node visits an index to find the locations of rows matching the index condition, and then the upper plan node actually fetches those rows from the table itself. Fetching rows separately is much more expensive than reading them sequentially, but because not all the pages of the table have to be visited, this is still cheaper than a sequential scan.

Now let's add another condition to the `WHERE` clause:

![image-2025-5-12_17-55-29.png](attachments/image-2025-5-12_17-55-29.png)

The added condition `stringu1 = 'xxx'` reduces the output row count estimate, but not the cost because we still have to visit the same set of rows. Notice that the `stringu1` clause cannot be applied as an index condition, since this index is only on the `unique1` column. Instead it is applied as a filter on the rows retrieved by the index. Thus the cost has actually gone up slightly to reflect this extra checking.

#### Order By condition matches the index order

In some cases the planner will prefer a “simple” index scan plan:

![image-2025-5-12_15-20-50.png](attachments/image-2025-5-12_15-20-50.png)

In this type of plan the table rows are fetched in index order, which makes them even more expensive to read, but there are so few that the extra cost of sorting the row locations is not worth it. You'll most often see this plan type for queries that fetch just a single row. It's also often** used for queries that have an `ORDER BY` condition that matches the index order,** **because then no extra sorting step is needed to satisfy the `ORDER BY`. **In this example, adding `ORDER BY unique1` would use the same plan because the index already implicitly provides the requested ordering.

#### When to use index combination

If there are separate indexes on several of the columns referenced in `WHERE`, the planner might choose to use an AND or OR combination of the indexes:

![image-2025-5-12_16-4-7.png](attachments/image-2025-5-12_16-4-7.png)

But this requires visiting both indexes, so it's not necessarily a win compared to using just one index and treating the other condition as a filter. If you vary the ranges involved you'll see the plan change accordingly.

Here is an example showing the effects of `LIMIT`:

![image-2025-5-12_16-0-17.png](attachments/image-2025-5-12_16-0-17.png)

This is the same query as above, but we added a `LIMIT` so that not all the rows need be retrieved, and the planner changed its mind about what to do. Notice that the total cost and row count of the Index Scan node are shown as if it were run to completion. However, the Limit node is expected to stop after retrieving only a fifth of those rows, so its total cost is only a fifth as much, and that's the actual estimated cost of the query. This plan is preferred over adding a Limit node to the previous plan because the Limit could not avoid paying the startup cost of the bitmap scan, so the total cost would be something over 25 units with that approach.

#### Use bitmap scan to reduce the random scan cost

Now, let's look the same example mentioned above：

![image-2025-5-12_15-11-49.png](attachments/image-2025-5-12_15-11-49.png)

**Bitmap Index Scan: **construct from index, location default mark as '0', records that meet the condition will be marked as '1' .

**Bitmap Heap Scan**: Fetch rows use the bitmap.

The reason for using two plan levels is that the upper plan node sorts the row locations identified by the index into physical order before reading them, to minimize the cost of separate fetches. The “bitmap” mentioned in the node names is the mechanism that does the sorting.

According the official document we know:

- bitmap is constructed using the indexes.
- bitmap will sort using page No. to reduce the random io access.

##### **Lossy mode**

Bitmap will be convert to lossy mode(remember pages instead of remember tuples) when it is too large(using work memory), this will cause condition recheck and slow down performance.(PT in Ratan business: [SQL performance when using bitmap scan - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/SQL+performance+when+using+bitmap+scan))

### Some Best Practices

- #### Index Cond and Filter

In `WHERE `clause multi conditions, the more index column it used, probability the better performance it could be, especial there is a big result data, since the conditions on index column will be applied as a 'Index Cond' operation on the data search step, but the non index column conditions will be applied as a 'Filter' operation, which will fetch more data and slow down the performance.

![image-2025-5-16_13-46-1.png](attachments/image-2025-5-16_13-46-1.png)

![image-2025-5-16_13-59-21.png](attachments/image-2025-5-16_13-59-21.png)

- #### ORDER BY match the index order

`ORDER BY` condition matches the index order, because no extra sorting step is needed to satisfy the `ORDER BY`.

![](https://confluence.global.standardchartered.com/download/attachments/3331052801/image-2025-4-17_16-29-43.png?version=1&modificationDate=1747281863000&api=v2)

![](https://confluence.global.standardchartered.com/download/attachments/3331052801/image-2025-4-17_15-49-19.png?version=1&modificationDate=1747281857000&api=v2)

- #### Use LIMIT to cutoff

Use `LIMIT `to cutoff result, avoid the unnecessary operations on remain tuples.

Refer to the second example in previous section 'When to use index combination'

- #### Gradual change of the Explain output

In Ratan DEV cashflow_data table

total record: 124635

example SQL:  select * from cash_settlement_query_cn.cashflow_data where created_at < '2024-02-27 08:35:40';

There is an btree  index on column created_at.

**When the query result records quantity is less than 2010, which around 1.6% of total, it use index scan.**

![image-2025-5-19_13-59-3.png](attachments/image-2025-5-19_13-59-3.png)

**When the query result records quantity is between 2006 and 17161, which is 1.6%~13.7% of total, it use bitmap index scan.**

![image-2025-5-19_13-53-11.png](attachments/image-2025-5-19_13-53-11.png)

**When the query result records quantity is more than 17214, which is around 13.8% of total, it use seq scan.**

![image-2025-5-19_13-55-51.png](attachments/image-2025-5-19_13-55-51.png)

According to the test above, we can infer that query on an index column, when the return records is less than 13.8%, it will use index scan, when it grows up more than 13.8%, it will use seq scan.

- so on...

### Summary

PostgreSQL devises a *query plan* for **each query it receives**. Choosing the right plan to match the query structure and the properties of the data is absolutely critical for good performance, so the system includes a complex *planner* that tries to choose good plans.

You can use the [`EXPLAIN`](https://www.postgresql.org/docs/14/sql-explain.html) command to see what query plan the planner creates for any query. Plan-reading is an art that requires some experience to master, but this page attempts to cover the basics.

### Reference

#### [PostgreSQL: Documentation](https://www.postgresql.org/docs/14/using-explain.html)

#### [The Internals of PostgreSQL](https://www.interdb.jp/pg/pgsql03.html)

#### [PostgreSQL: Re: Bitmap indexes etc.](https://www.postgresql.org/message-id/12553.1135634231@sss.pgh.pa.us)

#### [TidBitmap in PostgreSQL](https://blog.51cto.com/frankiewb/1603921)

#### [Pg-Hint-Plan](https://pg-hint-plan.readthedocs.io/_/downloads/en/pg15/pdf/)