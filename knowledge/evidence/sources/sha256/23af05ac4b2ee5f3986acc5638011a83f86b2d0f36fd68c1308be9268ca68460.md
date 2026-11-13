### Background

We are encounter a DB process block when we use the jdbcTemplate.batchUpdate() method to handle the generatedKeys with a keyHolder in cqrs domain events batch insert scenario. So I have take a deep dive on this problem.

### Key point

- PgJDBC can experience client/server deadlocks during batch execution

```
   
  // It's possible for the send and receive streams to get "deadlocked" against each other since
  // we do not have a separate thread. The scenario is this: we have two streams:
  //
  // driver -> TCP buffering -> server
  // server -> TCP buffering -> driver
  //
  // The server behaviour is roughly:
  // while true:
  // read message
  // execute message
  // write results
  //
  // If the server -> driver stream has a full buffer, the write will block.
  // If the driver is still writing when this happens, and the driver -> server
  // stream also fills up, we deadlock: the driver is blocked on write() waiting
  // for the server to read some more data, and the server is blocked on write()
  // waiting for the driver to read some more data. 
```

- PgJDBC support batch returning but this approach does increase the deadlock risk.

```
This approach does increase the deadlock risk if a batch executes statements where each statement returns many generated keys (e.g. a big multi-entry VALUES clause or an INSERT INTO ... SELECT ...), as it assumes each execution will only return one generated key. 
That's a fairly reasonable assumption, given that the lack of intra-statement ordering guarantees means you can't reliably associate generated keys to the values that generated them unless you run one statement per generated result. 
I don't expect this to be an issue in practice. In any case, anyone who's doing this is likely to be doing so as an attempt to work around the very limitation this commit fixes.
```

- When estimatedReceiveBufferBytes >= MAX_BUFFERED_RECV_BYTES PgJDBC will forcing Sync, receive buffer full or batching disallowed

```
    // We know this is deprecated, but still respect it in case anyone's using it.
    // PgJDBC its self no longer does.
    @SuppressWarnings("deprecation")
    boolean disallowBatching = (flags & QueryExecutor.QUERY_DISALLOW_BATCHING) != 0;
---------------------------------------------------------------------------------------------
/**
  private static final int MAX_BUFFERED_RECV_BYTES = 64000;
  private static final int NODATA_QUERY_RESPONSE_SIZE_BYTES = 250;
**/
private void flushIfDeadlockRisk(Query query, boolean disallowBatching,
      ResultHandler resultHandler,
      @Nullable BatchResultHandler batchHandler,
      final int flags) throws IOException {
    // Assume all statements need at least this much reply buffer space,
    // plus params
    estimatedReceiveBufferBytes += NODATA_QUERY_RESPONSE_SIZE_BYTES;

    SimpleQuery sq = (SimpleQuery) query;
    if (sq.isStatementDescribed()) {
      // ignore no use code
    } else {
      /*
       * We only describe a statement if we're expecting results from it, so it's legal to batch
       * unprepared statements. We'll abort later if we get any uresults from them where none are
       * expected. For now all we can do is hope the user told us the truth and assume that
       * NODATA_QUERY_RESPONSE_SIZE_BYTES is enough to cover it.
       */
    }

    if (disallowBatching || estimatedReceiveBufferBytes >= MAX_BUFFERED_RECV_BYTES) {
      LOGGER.log(Level.FINEST, "Forcing Sync, receive buffer full or batching disallowed");
      sendSync();
      processResults(resultHandler, flags);
      estimatedReceiveBufferBytes = 0;
      if (batchHandler != null) {
        batchHandler.secureProgress();
      }
    }
```

### Conclusion

The generatedKey and batchSize both can effect the deadlock risk.  To reduce the risk just need to preset the generatedKey columns and adjust the appropriate batchSize.

### Test Result in lifecycle service

[Netting Compare - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Netting+Compare)

### Debug

The debug steps are shown below:

1、Spring →JDBC Template

![image-2025-7-14_9-23-1.png](attachments/image-2025-7-14_9-23-1.png)

![image-2025-7-14_9-27-51.png](attachments/image-2025-7-14_9-27-51.png)

2、PgDriver→PgStatement

![image-2025-7-14_9-33-59.png](attachments/image-2025-7-14_9-33-59.png)

3、PgDriver→QueryExecutorImpl.execute(...) (handle in a loop)

![image-2025-7-14_9-36-1.png](attachments/image-2025-7-14_9-36-1.png)

PgDriver→QueryExecutorImpl.sendQuery(...) (will block sendOneQuery())

![image-2025-7-14_9-40-41.png](attachments/image-2025-7-14_9-40-41.png)

PgDriver→QueryExecutorImpl.flushIfDeadlockRisk(...)

![image-2025-7-14_9-52-34.png](attachments/image-2025-7-14_9-52-34.png)

```
// Deadlock avoidance:
  //
  // It's possible for the send and receive streams to get "deadlocked" against each other since
  // we do not have a separate thread. The scenario is this: we have two streams:
  //
  // driver -> TCP buffering -> server
  // server -> TCP buffering -> driver
  //
  // The server behaviour is roughly:
  // while true:
  // read message
  // execute message
  // write results
  //
  // If the server -> driver stream has a full buffer, the write will block.
  // If the driver is still writing when this happens, and the driver -> server
  // stream also fills up, we deadlock: the driver is blocked on write() waiting
  // for the server to read some more data, and the server is blocked on write()
  // waiting for the driver to read some more data.
  //
  // To avoid this, we guess at how much response data we can request from the
  // server before the server -> driver stream's buffer is full (MAX_BUFFERED_RECV_BYTES).
  // This is the point where the server blocks on write and stops reading data. If we
  // reach this point, we force a Sync message and read pending data from the server
  // until ReadyForQuery, then go back to writing more queries unless we saw an error.
  //
  // This is not 100% reliable -- it's only done in the batch-query case and only
  // at a reasonably high level (per query, not per message), and it's only an estimate
  // -- so it might break. To do it correctly in all cases would seem to require a
  // separate send or receive thread as we can only do the Sync-and-read-results
  // operation at particular points, and also as we don't really know how much data
  // the server is sending.
  //
  // Our message size estimation is coarse, and disregards asynchronous
  // notifications, warnings/info/debug messages, etc, so the response size may be
  // quite different from the 250 bytes assumed here even for queries that don't
  // return data.
  //
  // See github issue #194 and #195 .
  //
  // Assume 64k server->client buffering, which is extremely conservative. A typical
  // system will have 200kb or more of buffers for its receive buffers, and the sending
  // system will typically have the same on the send side, giving us 400kb or to work
  // with. (We could check Java's receive buffer size, but prefer to assume a very
  // conservative buffer instead, and we don't know how big the server's send
  // buffer is.)
  //


```

[PgJDBC can experience client/server deadlocks during batch execution · Issue #194 · pgjdbc/pgjdbc](https://github.com/pgjdbc/pgjdbc/issues/194)

![image-2025-7-14_14-18-18.png](attachments/image-2025-7-14_14-18-18.png)

[PgJDBC does not pipeline batches that return generated keys · Issue #195 · pgjdbc/pgjdbc](https://github.com/pgjdbc/pgjdbc/issues/195)

![image-2025-7-14_14-21-26.png](attachments/image-2025-7-14_14-21-26.png)

[Batch returning support by ringerc · Pull Request #204 · pgjdbc/pgjdbc · GitHub](https://github.com/pgjdbc/pgjdbc/pull/204)

![image-2025-7-14_14-24-29.png](attachments/image-2025-7-14_14-24-29.png)

[BatchInsert + generatedKeys will cause insert block in DB · Issue #3726 · pgjdbc/pgjdbc](https://github.com/pgjdbc/pgjdbc/issues/3726)

![image-2025-7-14_14-27-13.png](attachments/image-2025-7-14_14-27-13.png)

[getGeneratedKeys returns all columns for Statement.RETURN_GENERATED_KEYS · Issue #99 · pgjdbc/pgjdbc](https://github.com/pgjdbc/pgjdbc/issues/99)

![image-2025-7-14_15-54-58.png](attachments/image-2025-7-14_15-54-58.png)

[Enable reWriteBatchedInserts by default · Issue #3694 · pgjdbc/pgjdbc](https://github.com/pgjdbc/pgjdbc/issues/3694)

![image-2025-7-14_16-34-20.png](attachments/image-2025-7-14_16-34-20.png)

4、Thread dump

![image (10).png](attachments/image (10).png)