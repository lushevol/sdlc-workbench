# Frontend migration compatibility decisions

- Source: User message in the current Codex chat.
- Date: 2026-11-06 (Asia/Singapore).
- Priority: High-priority reference for frontend migration design.

## Exact user input

> The principle is try best to compatible with existing mfe-base and mfe-container APIs for upper applications. only one gap I can identify is that role is no more unique as before, others I think can keep the same. Another decision is that we can't migrate all tiles to CES in batch, so we must allow tiles to choose which entitlement system they are going to take, if EMS2, then all logic goes usual, if EMS2 (CES) then go on new logic with new app (entity) and new data structure.

## Interpretation for this stage

Preserve existing `mfe-base` and shared container APIs for upper applications where possible.
Keep named roles separate from effective feature/action permissions. The user identifies non-unique roles as the known compatibility gap.
Select authorization per tile. EMS2 tiles retain their existing logic.
CES tiles use their configured application identity and CES data structure.
Interpret the final `EMS2 (CES)` phrase as CES, using the existing `EMS3` wire value.
This interpretation follows the user's explicit EMS2-versus-CES distinction. Preserve the exact wording above.
The request authorizes analysis and knowledge refinement. It does not request application implementation or deployment.
