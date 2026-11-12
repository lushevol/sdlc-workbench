# Cash Settlement Netting import review

The [initial request](user-input.md#exact-user-input) identifies Settlement as a Post Trade Portal domain. The [follow-up](user-followup.md#exact-user-input) authorizes the Workbench initial-ingestion process and selects Sub2API. The [model instruction](user-followup.md#model-selection) selects `gpt-6-luna`.

## Source boundary

The current migrated Settlement collection is `knowledge-base/raw/sources` in the parent `ratan-release-impact` checkout. Its `config/kb-source-map.json` identifies 55 raw Markdown files. All 55 hashes match that map. The [provenance crosswalk](source-crosswalk.json) binds upstream IDs to Workbench snapshots. The Markdown attachment in the source map is included. Other attachment formats remain in the upstream collection.

The historical `Ratan-Settlement` checkout retains broader source history at `dcee25d2992444039c6f9d51c4f96b7156b5fb24`. The current collection covers Netting. The initial canonical batch covers the auto-netting workflow. Source approval and applicability need domain-owner evidence.

## Source selection and pilot review

The [source selections](../../../evidence/knowledge/selections/settlement-netting.json) bind 37 section selections, four complete pages, 11 evidence-only pages, two exclusions, and one held draft to their retained bytes. The held normalized-payment-schedule draft relies on an unavailable workbook. Its latest scenarios remain unresolved. Owner is unknown. Obtain the referenced workbook before using those cases.

The [auto-netting candidate](../../../knowledge/candidates/settlement/KT-settlement-auto-netting.md) uses five selected documents. Day 2 and the September 2026 flow support the scheduled queue, rule identity, matching execution keys, and resultant mapping. Confidence is high for the wording in those sources. Effective calendar, late-arrival, precedence, and exception policy remains open across the dated versions. Ask the Settlement domain owner to confirm applicability before publication. The other kept sources remain queued for canonical processing.

The refresh tool reserialized earlier YAML formatting. The import restored the exact pre-import manifest byte prefix and appended the new records. The resulting YAML parses to the same records produced by refresh.

## Canonical pilot outcome

The [candidate audit event](../../../evidence/knowledge/audit/AUD-20261112-KT-settlement-auto-netting-v1.yaml) binds the agent review to the final candidate bytes. The sealed ingestion check passed with 46 local links, 22 physical line fragments, and zero findings. The [processing receipts](../../../evidence/knowledge/processing/settlement-netting.json) close five source items. The plan still has 36 canonical processing items and one held source review.

For the retrieval question about two eligible cashflows, the candidate traces the answer to the Day 2 grouping rule and the September Function Flow. Both the rule identity and every field in the configured execution key must match. The candidate also preserves the documented Bilateral Netting key and the disputed date and exception policies.

## Derived wiki outcome

The Workbench bridge selected OpenKB with the URL and key loaded from the user's shell settings for the operation. The ignored local model configuration selects `openai/gpt-6-luna`. The exact wiki plan queues the auto-netting candidate with recipe `sub2api-gpt-6-luna-v1`.

The initial provider probes returned non-JSON HTTP 403 responses through both Chat Completions and Responses. The cause remains unknown.

The [follow-up catalog check](user-followup.md#provider-catalog-check) succeeded on 12 November 2026. The configured key listed 27 models, including `gpt-6-luna`. That model returned completions through Chat Completions and Responses using short test prompts. The probes contained no Settlement content.

Automatic approval review initially rejected the scoped wiki compilation because it would send the auto-netting candidate and relevant existing wiki context to the configured Sub2API endpoint. The user then [explicitly approved that payload and destination](user-followup.md#compilation-approval).

OpenKB compiled the approved candidate with `gpt-6-luna`. The review checked the [summary](../../../knowledge/llm-wiki/wiki/summaries/KT-settlement-auto-netting.md), the concepts for [rule selection](../../../knowledge/llm-wiki/wiki/concepts/auto-netting-rule-selection.md), [scheduling](../../../knowledge/llm-wiki/wiki/concepts/auto-netting-scheduling.md), and [grouping and outcomes](../../../knowledge/llm-wiki/wiki/concepts/cashflow-netting-grouping-and-outcomes.md), and the [wiki index](../../../knowledge/llm-wiki/wiki/index.md). The final wording keeps the execution key scoped to netting type and preserves the unresolved outcomes for unmatched cashflows by type and rule configuration.

The wiki bridge recorded reviewed completion for the candidate. It verified 13 linked canonical records with zero structural findings. The candidate retains its draft status and unresolved policy questions.
