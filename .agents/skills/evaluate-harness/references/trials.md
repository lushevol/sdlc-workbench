# Trial and scorecard fields

Use one manifest per trial and retain each payload once.

```yaml
schema_version: 1
trial_id: unique-id
case_id: bounded-case
variant: baseline-or-candidate
fixture:
  synthetic: true
  root: relative-or-external-trial-path
  source_hashes: {}
skills:
  - id: skill-id
    root: relative-path
    sha256: pinned-hash
settings:
  model: observed-or-UNKNOWN
  reasoning: observed-or-UNKNOWN
  client: observed-or-UNKNOWN
permitted_actions: []
criteria: []
respondent:
  output: relative-path
  artifacts: []
  commands: []
assessor:
  independent: true
  identity: observed-or-UNKNOWN
  outcomes: []
limits: []
```

For paired trials, keep the questions, sources, applicability, draft boundary, and assessor criteria identical. Change only the selected skill revision or the explicitly tested workflow input.
Count each criterion once. Report `NOT_ASSESSED` separately from failure. Keep baseline and candidate outputs side by side so a later reviewer can reproduce the comparison.
