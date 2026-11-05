# Upstream origin and adoption boundary

This skill adapts the Markdown authoring workflows from SamurAIGPT/llm-wiki-agent.
Upstream revision: `37145b8ba04d0acc6f3b6b0c02606768d1862c9a`.
Source: [pinned agent instructions](https://github.com/SamurAIGPT/llm-wiki-agent/blob/37145b8ba04d0acc6f3b6b0c02606768d1862c9a/AGENTS.md).
License: [MIT notice](../LICENSE.md).

| Upstream workflow | Adopted behavior |
| --- | --- |
| Read sources and compile pages | Read selected canonical domain records and write one linked summary per record. |
| Living overview, entities, concepts | Generate supported cross-source explanations with exact citations and visible source states. |
| Query with inline citations | Navigate the wiki, reopen canonical records, and answer with evidence and explicit unknowns. |
| Health before lint | Check structure and coverage first, then review meaning and contradictions. |
| Changed-source refresh | Use full input hashes to identify affected navigation and preserve unchanged sources. |
| Graph navigation | Reuse the existing evidence graph and its relationship meanings. |

The upstream project provides root agent instructions and optional Python tools, rather than a packaged project skill.
This adaptation packages the instruction-based route as a canonical Workbench skill.
It retains the upstream source-summary and connected-synthesis pattern.
It changes page metadata, paths, links, and update boundaries to fit existing Workbench contracts.

The upstream Python tools, provider defaults, converters, automatic healer, scheduler recipe, and graph format are not installed.
Their capabilities remain separate from this adopted skill.
No upstream root instructions replace the workspace's `AGENTS.md`.

Ordinary Markdown links replace stem-based wikilinks.
Navigation pages use directory `index.md` files, rather than unsupported record types.
Exact canonical record identities replace filename-only authority.
Wiki generation preserves candidate states and cannot supply human publication approval.
