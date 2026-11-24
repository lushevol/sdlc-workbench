# Background

Trade confirmation status is mandatory for payment STP, otherwise all the payments would be pending OPS manual affirmation.

Currently Murex Korea is not sending trade COMP anywhere for RATAN Settlement Platform to consume.

Korea OPS stated that it is mandatory to have the COMP status driven STP for business go live, as it is a small team cannot handle the volume of manual processing.

# Solution 1 (Initial solution by Nov 2025, ruled out by Jun 2026)

Proposal:

- Currently exists Murex Korea to Murex GDC flow but only including trade VALD even by using the flow to publish trade COMP event , then RATAN can still get COMP status through the existing flow.

Benefit:

- Confirmation flow is always strategic by retrieving from Trade Lake
- Reused existing flow between MUREX GDC and TDS3
- Reused existing flow betweenTDS3 and RATAN

Status:

- Rejected by Murex PSS
- Development was done by both RATAN and Murex but have to be reverted back

# Solution 2 (Simplified solution, ruled out by Apr 2026)

Proposal:

- Murex Korea to publish **SCBML** of trade to RATAN
- New IBMMQ integration between Murex Korea and RATAN

Benefit

- Simplified Murex development for both Murex Korea and Murex GDC by removing the integration with each other
- No tactical build in RATAN strategic Settlement platform
- Easily switch off once the flow (Murex Korea → TDS3) is ready, by removing the integration
- Simplify the Testing complexity by reducing integration

Status:

- Eventually found that Murex cannot generate SCBML

# Solution 3 (Current possible tactical solution)

Proposal:

- Murex Korea to publish **MXML** of trade to RATAN
- RATAN customization to handle the COMP events
- New IBMMQ integration between Murex Korea and RATAN

Benefit

- Simplified Murex development for both Murex Korea and Murex GDC by removing the integration with each other
- Simplify the Testing complexity by reducing integration

Downside:

- Tactical build in RATAN which eventually will be dropped
- Additional effort to support the delivery
- Technical debt have to be funded for removal, hard to track but need a clear plan

Status:

- Detailed design in progress