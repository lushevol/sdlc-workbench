# Knowledge graph option source excerpts

- Retrieved: 3 November 2026.
- Method: Browser-visible primary documentation.
- Capture: Selected exact prose excerpts. Line wrapping and Markdown formatting were normalized.
- Limit: These excerpts are not byte-identical full source snapshots.
- Scope: Technology roles, operating requirements, temporal provenance, and local concurrency limits.
- No software was installed or executed.

## E1: SQLite local storage and concurrency

Source: [Appropriate Uses For SQLite](https://www.sqlite.org/whentouse.html).
The page states its last update as `2025-05-31 13:08:22Z`.

> SQLite strives to provide local data storage for individual applications and devices. SQLite emphasizes economy, efficiency, reliability, independence, and simplicity.

> SQLite supports an unlimited number of simultaneous readers, but it will only allow one writer at any instant in time.

> A good rule of thumb is to avoid using SQLite in situations where the same database will be accessed directly (without an intervening application server) and simultaneously from many computers over a network.

## E2: SQLite graph traversal

Source: [The WITH Clause](https://www.sqlite.org/lang_with.html#recursive_common_table_expressions).
The page states its last update as `2025-05-12 11:56:41Z`.

> A recursive common table expression can be used to write a query that walks a tree or graph.

Source section: [Queries Against A Graph](https://www.sqlite.org/lang_with.html#queries_against_a_graph).
The section supplies indexed edge tables and recursive traversal examples.

## E3: Neo4j role and deployment

Source: [What is Neo4j?](https://neo4j.com/docs/getting-started/whats-neo4j/).
The inspected page has no pinned revision recorded in this review.

> Neo4j is a native graph database, which means that it implements a true graph model all the way down to the storage level.

> Neo4j uses Cypher®, a declarative query language similar to SQL, but optimized for graphs.

> Neo4j is available for installation on Linux, macOs, and Windows.

> Neo4j has free and subscription-based licensing options.

The page links local installation, Desktop, Docker, cloud, and Kubernetes deployment options.
The page identifies Java and Scala as implementation languages.
Edition-specific feature and license conditions were not audited.
No deployment or platform behavior was tested.

## E4: Graphiti role, provenance, and prerequisites

Source: [Graphiti README](https://github.com/getzep/graphiti/blob/7e0342a49ce5a04f6415ac2f64ce150bb81b0689/README.md).
Observed repository HEAD: `7e0342a49ce5a04f6415ac2f64ce150bb81b0689`.

> Graphiti is an open-source Python framework for building and querying temporal context graphs. You supply the graph database, LLM, and embedder, and you build the service around it: ingestion, tenancy, access control, and operations.

> Temporal Fact Management: Facts have validity windows. When information changes, old facts are invalidated — not deleted. Query what's true now, or what was true at any point in time.

> Episodes & Provenance: Every entity and relationship traces back to the episodes (raw data) that produced it. Full lineage from derived fact to source.

> Prescribed & Learned Ontology: Define entity and edge types upfront via Pydantic models (prescribed), or let structure emerge from your data (learned). Start simple, evolve as patterns appear.

The requirements list Python 3.10 or higher and graph backends including Neo4j, FalkorDB, and Amazon Neptune.
The README defaults to OpenAI for inference and embedding.
It also documents OpenAI-compatible hosted providers and local model servers.
It warns that smaller or local models can fail structured extraction schemas.
It documents an embedded FalkorDB extra requiring Python 3.12 or higher.
It marks Kuzu support deprecated and recommends other backends for new projects.
No backend, extraction quality, or platform behavior was tested.

## E5: Graphiti reference server boundary

Same source and revision as E4.

> The reference servers have no authentication, no authorization, and no prompt-injection protection.

> Your service must supply authentication, authorization, tenant isolation, and input controls.

These are the project's documented reference-server limits.
They do not establish that all Graphiti-based applications have those limits.

## E6: Microsoft GraphRAG role and maintenance status

Source: [GraphRAG README](https://github.com/microsoft/graphrag/blob/34b2b67ae4601ad0b47bcd179fbe3f2a23aa0857/README.md).
Observed repository HEAD: `34b2b67ae4601ad0b47bcd179fbe3f2a23aa0857`.

> This project is largely in maintenance mode, and won't be accepting new PRs or implementing new features. We'll perform bug fixes and dependency updates as appropriate, particularly to address CVEs as they arise.

> The GraphRAG project is a data pipeline and transformation suite that is designed to extract meaningful, structured data from unstructured text using the power of LLMs.

> Please note that the provided code serves as a demonstration and is not an officially supported Microsoft offering.

> Warning: GraphRAG indexing can be an expensive operation, please read all of the documentation to understand the process and costs involved, and start small.

## E7: Microsoft GraphRAG retrieval architecture

Source: [GraphRAG documentation](https://microsoft.github.io/graphrag/).
This documentation page has no pinned revision recorded in this review.

> The GraphRAG process involves extracting a knowledge graph out of raw text, building a community hierarchy, generating summaries for these communities, and then leveraging these structures when perform RAG-based tasks.

The documentation describes global search over community summaries and local search around entity neighbors.
It describes TextUnits as fine-grained output references.
It recommends prompt tuning for the selected data.
These statements describe the documented method. No accuracy, cost, or performance claim was reproduced.
