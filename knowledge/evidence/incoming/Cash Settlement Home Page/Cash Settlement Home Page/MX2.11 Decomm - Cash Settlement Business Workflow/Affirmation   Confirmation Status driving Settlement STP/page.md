Note: STP / NSTP rules will be defined agnostic of client segment (Bank vs Corporate) to achieve maximum STP rate. Where NSTP is required, it will be driven based on product / individual client level parameters.

| Product | Trade Affirmation Status CDU PS | Trade Confirmation Status CDU PS | Cashflow Affirmation Status RATAN | Comments |
| --- | --- | --- | --- | --- |
| **Method** | **Product** | **Unaffirmed** | **Economics Affirmed** | **Full Affirmed** | **Unconfirmed** | **Economics** **Matched** | **Matched** | **Unaffirmed** | **Affirmed** | |
| Gross | FX - Cash, Tom, Spot | **NSTP** | **NSTP** | **STP** | **NSTP** | **NSTP** | **STP** | **NSTP** | **Manual Affirm** | Release Cashflow if Trade is Full Affirmed or Matched (or) Cashflow is Affirmed |
| FX - FORWARD | **NSTP** | **NSTP** | **STP** | **NSTP** | **NSTP** | **STP** | **NSTP** | **Manual Affirm** | |
| FX SWAP | Near and Far Leg should independently follow the STP workflow based upon the product type / tenure |
| DEPO | **NSTP** | **NSTP** | **STP** | **NSTP** | **NSTP** | **STP** | **NSTP** | **Manual Affirm** | Hold payment until receipt of funds is confirmed (O/N for China Day1) |
| LOAN | **NSTP** | **NSTP** | **STP** | **NSTP** | **NSTP** | **STP** | **NSTP** | **Manual Affirm** | |
| **All Derivatives Products** - Trade Cashflows | **NSTP** | **NSTP** | **STP** | **NSTP** | **NSTP** | **STP** | **NSTP** | **Manual Affirm** | |
| **All Derivative Products**- Fixing Cashflows including IRS / NDF | **NSTP** | **NSTP** | **NSTP** | **NSTP** | **NSTP** | **NSTP** | **NSTP** | **STP if Confirmation is Fully Matched + Fixing is done** | - STP if underlying Trade must be Full Matched + Fixing completed (i.e., NSTP if Trade is Fully Affirmed + Fixed). - Currently Fixing cashflows are STP for some of the products without cashflow affirmation |
| FXMM/Derivatives - **Internal trades** **requiring payment** | STP if the generation is triggered by external venue (example: prime services are matched in Trianna / SCALE) |
| Derivatives - Inter Entity | STP if trade is in a 'validated' status on the back of reconciliation done by TCG <<Controls at TCG based on SABRE TDS3 recon via ONEVALUATIONS view to be verified>> |
| Islamic Trades | ** NSTP **<<Current state / target state to be reviewed as a separate exercise>> |
| Self Executed Trades by Clients Negative Affirmation Clients | Release payment based on Confirmation Dispatch and no matching required <<<Engage Legal to challenge NCA requirement for Self executed trades>>> |
| Netting - FX / Derivatives | STP if the netting is 1) triggered by client (S2B NG) or 2) Validated from an external venue 3) STP for specific clients based on auto netting at a predefined netting cutoff provided underlying trades are fully Affirmed / fully Matched <<<Further analysis required to define the logic>>> |
| Clearing Trades | <<Currently being suppressed in MX2.11, target state to be agreed>> |