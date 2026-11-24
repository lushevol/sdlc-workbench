# Story Status Descirption

| ADO Status | Description | Story Mandatory Value | Related Sub Task |
| --- | --- | --- | --- |
| Open | Story initialized and yet prioritize | | |
| Prioritized | Story prioritized and ready for planning | 1. Priority 2. Release date 3. Exit criteria 4. Description | |
| In Analysis | Picked by engineer, if there is BA task then BA work in progress, if only developer task, then developer design in progress | | Yes Analysis task |
| Ready for Development | BA/DEV/QA analysis task done, or analysis partial complete and able to start development | 1. BA requirement clearly brief to DEV and QA | Yes Analysis task Development task QA case development task |
| On Hold | Critical issue / blockers result in the story can't be | 1. Blocker/issue commented attach evidence | Yes Analysis task - On Hold Development task- On Hold QA case development task - On Hold |
| In Development | Dev coding in progress QA case development in progress | 1. Technical design approved | Yes Development task QA case development task |
| Dev Done | Coding done UT done PR merge to target develop/release branch CI pass CD done to the target environment Sanity check done and ready for QA start QA case development done | 1. UT/dev testing evidence. 2. QA case get reviewed | Yes QA verification task |
| In Test | QA case execution in progress | 1. QA testing in progress 2. QA testing done with a release | Yes QA verification task |