# Direct ADE wiki maintenance

Use this procedure after the bridge selects llm-wiki-agent and the user authorizes compilation or maintenance. Read the original agent's semantic workflow, then apply this Workbench contract to the shared OpenKB-format files. A printed handoff alone performs no compilation.

## Author complete native-format pages

Native OpenKB compiler prompts ask for body text because native code writes frontmatter. Direct ADE file authoring must create or retain the complete frontmatter below. These Workbench layout and metadata rules take precedence over the original agent's different page types and folders. Original upstream files remain unchanged.

Summary at `wiki/summaries/<source-name>.md`:

```yaml
---
type: Summary
description: One sentence describing this source's contribution.
doc_type: short
full_text: sources/<source-name>.md
---
```

Concept at `wiki/concepts/<slug>.md`:

```yaml
---
type: Concept
description: One sentence describing this focused topic.
sources: [summaries/<source-name>.md]
---
```

Entity at `wiki/entities/<slug>.md`:

```yaml
---
type: Product
description: One sentence identifying this named thing.
sources: [summaries/<source-name>.md]
---
```

Use the actual supported, capitalized entity subtype, such as `Organization` or `Product`. Preserve additional valid fields on existing pages. Saved explorations use the existing `query:` frontmatter. Replace illustrative names and descriptions with the inspected source and actual content. Add a document title, source-status note, meaningful body and wiki-relative links; register each page in the corresponding index section. Keep exact canonical criterion links beside important rules.

## Prepare and perform semantic work

Use [bind-wiki-sources](../../bind-wiki-sources/SKILL.md) to validate selection, aliases, source-before hashes, and paired provenance before-images.
Then use [maintain-wiki-content](../../maintain-wiki-content/SKILL.md) for full semantic maintenance and the reviewed source/output receipt.
These reusable units apply the original agent's reasoning to the native page metadata defined above.

## Complete provenance after review

Use [finalize-wiki-update](../../finalize-wiki-update/SKILL.md#ade-provenance-completion) after semantic review.
It owns both state-file writes, full verification, paired recovery, and truthful operation logging as one coordinated operation.
Use [check-wiki-health](../../check-wiki-health/SKILL.md) independently for read-only diagnosis.
Completion records reviewed bytes; it does not supply semantic correctness, human approval, or deployed behavior.
