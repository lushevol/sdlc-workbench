# User direction: model-availability gate

Date: 16 November 2026 (Asia/Singapore).

Source thread: `01a1e003-14e9-7153-b3b4-3547f178ad4f`.

## Current decision: native selection accepted

The [latest explicit user clarification](user-review-model-decision-20261116.md#exact-user-input) resolves GATE-04. Explicit native model and reasoning selection is sufficient for fresh work, with unavailable independent runtime confirmation retained as a limit. Use `gpt-6.1-sol` / `medium` for review workers; retain `gpt-6-luna` / `max` for document-processing workers where applicable.

The earlier mismatch directions below remain historical evidence. They no longer block fresh work under this clarified execution-evidence requirement. Earlier unverified semantic drafts retain that limitation and need fresh affected review before integration. No business-policy answer or publication approval is supplied.

## Preflight mismatch direction

> The model-correction preflight in merge-ccil reports actual_runtime_model=deepseek-v4-flash from CHATBOT_OPENAI_MODEL/DEEPSEEK_LLM_MODEL, despite requested gpt-6-luna. Treat this as a hard model-availability blocker for semantic worker evidence. Continue only deterministic/no-change checks that require no model; keep all semantic updates, candidate integration, and wiki semantic maintenance pending unless a fresh runtime preflight explicitly reports GPT-6 Luna Max. Record the mismatch and exact path .workbench/ingestion/luna-max-20261115/workers/merge-ccil/resume-20261116/model-correction/model-mismatch.md in the checkpoint.

## Resumed handoff audit direction

> Handoff audit confirms model metadata is inconsistent: merge-ccil says actual deepseek-v4-flash; merge-cn-workflow/manual-netting/SSI-Nostro say exact deployment unavailable; cashflow/ratan-interface say runtime model not exposed. Only some handoffs copy the requested gpt-6-luna label. Treat all semantic merge drafts as model-unverified and keep them pending. You may record deterministic no_change receipts and structural checks, but do not claim GPT-6 Luna Max semantic completion or integrate drafts without an explicit model-verified handoff.

## Resumed thread and saved-plan direction

> All ten resumed merge child threads now show idle. The saved current RATAN plan files exist: coordinator-plan-20261116/ratan-plan-after-nochange.json (plan_id 70489f99..., process 64, review 3, unchanged 122) and workers/resume-plan-wiki/ratan-plan-current.json. If the source-operation lock still fails, record that deterministic lock blocker with the saved plan hash and finalize the checkpoint; do not delete or bypass the lock.

## Outstanding input request

Status: resolved for fresh native work by the [16 November user answer](user-review-model-decision-20261116.md). The original coordinator request below is retained as historical context.

Can you provide fresh runtime preflight evidence that explicitly reports GPT-6 Luna Max with Max reasoning, plus model-verified handoffs for every semantic merge?

The historical preflight reports `deepseek-v4-flash`. Other historical handoffs omit exact runtime or reasoning metadata. These earlier drafts remain unverified; fresh affected reviews may now proceed under the clarified native-selection requirement above.

The 41 held source selections need owner evidence or missing artifacts. Their questions remain in [the canonical question annex](canonical-draft-questions-20261115.md).
