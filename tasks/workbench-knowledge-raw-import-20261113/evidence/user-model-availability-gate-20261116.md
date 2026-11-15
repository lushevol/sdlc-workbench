# User direction: model-availability gate

Date: 16 November 2026 (Asia/Singapore).

Source thread: `01a1e003-14e9-7153-b3b4-3547f178ad4f`.

## Preflight mismatch direction

> The model-correction preflight in merge-ccil reports actual_runtime_model=deepseek-v4-flash from CHATBOT_OPENAI_MODEL/DEEPSEEK_LLM_MODEL, despite requested gpt-6-luna. Treat this as a hard model-availability blocker for semantic worker evidence. Continue only deterministic/no-change checks that require no model; keep all semantic updates, candidate integration, and wiki semantic maintenance pending unless a fresh runtime preflight explicitly reports GPT-6 Luna Max. Record the mismatch and exact path .workbench/ingestion/luna-max-20261115/workers/merge-ccil/resume-20261116/model-correction/model-mismatch.md in the checkpoint.

## Resumed handoff audit direction

> Handoff audit confirms model metadata is inconsistent: merge-ccil says actual deepseek-v4-flash; merge-cn-workflow/manual-netting/SSI-Nostro say exact deployment unavailable; cashflow/ratan-interface say runtime model not exposed. Only some handoffs copy the requested gpt-6-luna label. Treat all semantic merge drafts as model-unverified and keep them pending. You may record deterministic no_change receipts and structural checks, but do not claim GPT-6 Luna Max semantic completion or integrate drafts without an explicit model-verified handoff.

## Resumed thread and saved-plan direction

> All ten resumed merge child threads now show idle. The saved current RATAN plan files exist: coordinator-plan-20261116/ratan-plan-after-nochange.json (plan_id 70489f99..., process 64, review 3, unchanged 122) and workers/resume-plan-wiki/ratan-plan-current.json. If the source-operation lock still fails, record that deterministic lock blocker with the saved plan hash and finalize the checkpoint; do not delete or bypass the lock.
