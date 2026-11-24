---
name: check-wiki-health
description: Inspect derived wiki source freshness, canonical aliases, native structure, and semantic quality without advancing provenance or publishing knowledge.
---

# Check wiki health

Input: the selected workspace, optional reviewed source/output receipt, and requested integrity or semantic scope.
Use read-only checks to diagnose maintenance or verify a completed update.

## Check source bindings and structure

Run commands through the [project-scoped launcher](../llm-wiki/references/workflows.md#project-scoped-commands):

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py verify
python3 .agents/skills/llm-wiki/scripts/wiki.py plan --source knowledge/records/candidates --output .workbench/wiki/health-plan.json
```

The bridge checks canonical source hashes, both relative aliases, registry consistency, and all six native structural categories.
These local checks use no model call in either semantic mode.
Verification covers recorded bindings and native structure.
Local planning compares requested canonical inventory, completion receipts, and current output dependencies without model calls.
Report bootstrap review, pending attempts, missing outputs, changed recipes, and omitted sources separately from structural findings.
Inspect receipt notes and claims for semantic fidelity; matching hashes cannot establish meaning by themselves.
Report stale sources, missing paths, broken bindings, and structural findings with their affected scope.
`run status` and `run list` can supply local discovery. They do not replace full verification.

## Check before advancing bindings

During [finalization](../finalize-wiki-update/SKILL.md), run native structure checks before provenance updates:

```sh
.venv-openkb/bin/python -c "from pathlib import Path; from openkb.lint import run_structural_lint; print(run_structural_lint(Path('knowledge/llm-wiki')))"
```

On Windows, use `.venv-openkb\Scripts\python.exe` with the same arguments.
Run from the selected workspace root. Inspect all six categories for zero findings.
This explicit KB path uses no global default or model call.
Stale recorded bindings can be expected before finalization; full verification must pass afterward.

## Review semantic quality when requested

Check fidelity to canonical sections, completeness, contradictions, applicability, and visible source lifecycle qualifications through direct agent inspection.
Native `run lint` persists a report and log, even without `--fix`.
Keep that report-producing operation outside a read-only health check.
When the user requests engine lint output, route it through [llm-wiki](../llm-wiki/SKILL.md) and its engine selection contract.
Do not run original upstream health/graph scripts on this shared OpenKB layout; their index/link assumptions differ.
Candidate sources remain candidates. Structural success cannot supply publication approval or verify business execution.

For a changed source, inspect the retained implementation and test evidence named by the affected task in addition to the derived wiki outputs. Confirm that each removed numeric or behavioural claim has a reviewed disposition and evidence locator. A clean canonical closure search does not prove that implementation or execution facts were safely retained.

## Result and stop conditions

Return checked source scope, actual commands/mode, findings, receipt mismatches, and evidence limits.
Do not edit pages, advance provenance hashes, delete missing inputs, or promote knowledge while checking health.
An unavailable checker is incomplete verification; preserve the error and concrete recovery action.
