```
ALTER TABLE cash_netting_service.t_cashflow ADD COLUMN IF NOT EXISTS cashflow__splitting_id text NOT NULL DEFAULT '';
CREATE UNIQUE INDEX t_cashflow__splitting_id_idx ON cash_netting_service.t_cashflow (cashflow__cashflow_id,cashflow__splitting_id);

```

Split process detail:

Unsplit process Detail：

Withdraw：