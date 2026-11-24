Align with [Stamping Exception Design](https://confluence.global.standardchartered.com/display/DSP/FMRP+-+SSI+Stamping+Flow), showing UI display exception panel condition logical.

## Exception Panel

Display exception highlight in UI condition

| Exception Type | Exception Name | Exception Code | Exception Status | Exception Status = Cashflow Sub Status | Show In Exception Panel | Comment |
| --- | --- | --- | --- | --- | --- | --- |
| vostro | Vostro | ["RATAN-201000010", "Per SSI Adhoc"] | INACTIVE | | No | This is SSI Good Stamping data, By default, there is a Adhoc button shown on the Vostro panel. Clicking this button, will change vostroTitle and nostroTitle => "Adhoc SSI - Nostro/Vostro". then user can edit these two forms. |
| vostro | Vostro | ["RATAN-201000002", "Multi Vostro"] | | exception status in ["Pending Operator", "Pending Verification"] | Yes | vostroTitile => `${exp.Exception_Code} Exception` vostroTitleColor => COLOR_WARNING |
| vostro | Vostro | ["RATAN-201000001", "Missing Vostro"] | | exception status in ["Pending Operator", "Pending Verification"] | Yes |
| vostro | Vostro | ["RATAN-201000003", "SI Mismatch"] | | exception status in ["Pending Operator", "Pending Verification"] | Yes |
| vostro | Vostro | ["RATAN-201000006", "Validate Bene Info"] | | exception status in ["Pending Operator", "Pending Verification"] | Yes |
| vostro | Vostro | ["RATAN-201000005", "Missing Nostro"] | | exception status in ["Pending Operator", "Pending Verification"] | Yes | If such an exception exists, an "Edit" button will be added to the Nostro panel. nostroTitle will be `${exp.Exception_Code} Exception` nostroTitleColor will be "warning" If you click edit button, vostro form will became editable too. |
| affirmation | Affirmation | | | exception status in ["Pending Operator", "Pending Verification"] | Yes | |
| back_value | Backvalue | | | exception status in ["Pending Operator", "Pending Verification"] | Yes | |
| nstp | NSTP | | | exception status in ["Pending Operator", "Pending Verification"] | Yes | |
| high_risk_nstp | HIGH_RISK_NSTP | | | exception status in ["Pending Operator", "Pending Verification"] | Yes | |
| hard_blocker | HARD_BLOCKER | | | exception status in ["Pending Operator", "Pending Verification"] | Yes | |
| other | Other | | | exception status in ["Pending Operator", "Pending Verification"] | Yes | |
| comment | Comment | | | exception status in ["Pending Operator", "Pending Verification"] | Yes | |