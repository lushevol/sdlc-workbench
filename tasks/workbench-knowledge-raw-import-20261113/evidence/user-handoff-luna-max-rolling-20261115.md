# Rolling source-review handoff

- Date: 15 November 2026 (Asia/Singapore)
- Source thread: `01a1dfcd-b46f-7ea0-a3fa-376110a87bef`
- Owning processing thread: `01a1de64-056c-7d01-be99-51706c903144`

## Exact user direction

> The user authorized this handoff and requested that all new review workers use GPT-6 Luna with Max reasoning, with a one-hour target. We launched 31 disjoint source-review chats for the 504-page checkpoint 162 queue and three separate reviewers for the 41 source-selection holds. All 34 jobs started. You remain the sole writer of canonical records, receipts, task progress, and wiki. Please use `.workbench/ingestion/luna-max-20261115/coordinator-handoff.md` now and process ready rows in rolling batches while workers continue. Run `python3 .workbench/ingestion/luna-max-20261115/check_progress.py` and read the referenced worker evidence. A draft-only output does not support a no-change receipt. Reuse current, exact worker review evidence on each fresh plan; group proposals that touch the same output, then apply the existing final-byte review, audit, receipt and wiki checks. Keep receiving and integrating supported batches without waiting for all workers. Exact user input and dispatch links are in the task evidence file you linked at checkpoint 163. Report the concrete canonical queue and blockers at the one-hour checkpoint.
