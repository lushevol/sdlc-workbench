Blade dev 3: [Markets](https://dev-dev3-dtp.apps.dtp-np.ocp.standardchartered.com/?stream=rates,ptfx,lifecycle)

2006593 (MO user) SCBpassword1$

Ratan: [FMO Post Trade Portal](https://fmo-mfe-fmrp2.pi.dev.net:8453/?show_normal_login=y&survey=no)

# Scenario1: C1 New (Released) -> Purge C1 -> PFR (C1 withdrawal waiting, C2 new in waiting) -> Manual net C1 and C2 to 0 ->PFR (C2 withdrawal and C3 new will be hold in group blotter)

**EXPAND: Expand**

Trade booking: 7114035790

![image-2026-1-31_11-53-16-1.png](attachments/image-2026-1-31_11-53-16-1.png)

Purge:

![image-2026-1-31_11-53-24-1.png](attachments/image-2026-1-31_11-53-24-1.png)

PFR:

![image-2026-1-31_11-53-29-1.png](attachments/image-2026-1-31_11-53-29-1.png)

Netting to 0:

![image-2026-1-31_11-53-34-1.png](attachments/image-2026-1-31_11-53-34-1.png)

PFR again, USD not replaced as manual netted and EGO replace as no manual touch:

![image-2026-1-31_11-53-39-1.png](attachments/image-2026-1-31_11-53-39-1.png)

USD payments held in group as non eco amend:

![image-2026-1-31_11-53-43-1.png](attachments/image-2026-1-31_11-53-43-1.png)

**EXPAND_END**

# Scenario2: C1 New (Released) -> Purge C1 -> Cancellation (C1 withdrawal waiting)

**EXPAND: Expand**

Trade booking: 7117008001

![1.png](attachments/1.png)

Purge:

![2.png](attachments/2.png)

Book terminate , cashflow cancelled

![3.png](attachments/3.png)

**EXPAND_END**

# Scenario3: C1 New (Released) -> Purge C1 -> eco amendment (effective date as past date) (C1 withdrawal waiting, C2 new in waiting)

**EXPAND: Expand**

Trade booking: 7117011003

![image-2026-1-31_12-52-53.png](attachments/image-2026-1-31_12-52-53.png)

Purge:

![image-2026-1-31_12-53-19.png](attachments/image-2026-1-31_12-53-19.png)

Amendment:

![image-2026-1-31_12-54-10.png](attachments/image-2026-1-31_12-54-10.png)

![image-2026-1-31_12-54-42.png](attachments/image-2026-1-31_12-54-42.png)

**EXPAND_END**

# Scenario4[Revised]: C1 New (Manual SWIFT Suppressed) -> Purge C1 -> PFR (C1 withdrawal and C2 new will be hold in group blotter)

~~Scenario4: C1 New (Manual SWIFT Suppressed) -> Purge C1 -> PFR (C1 withdrawal cancelled, C2 new in waiting) -> Manual net C1 and C2 to 0 ->PFR (C2 withdrawal and C3 new will be hold in group blotter) - ~~

**EXPAND: Expand**

Trade booking: 7114035798

![image-2026-1-31_12-6-53.png](attachments/image-2026-1-31_12-6-53.png)

Purge:

![image-2026-1-31_12-7-36.png](attachments/image-2026-1-31_12-7-36.png)

PFR:

![image-2026-1-31_12-10-46.png](attachments/image-2026-1-31_12-10-46.png)

![image-2026-1-31_12-35-54.png](attachments/image-2026-1-31_12-35-54.png)

**EXPAND_END**

# Scenario5:  C1 New (Manual SWIFT Suppressed) -> Purge C1 -> eco amendment (C1 withdrawal cancelled, C2 new in waiting)  -

**EXPAND: Expand**

Trade booking:7114035799(Manual SwiftSuppress 000054018683)

![image-2026-1-31_12-16-21.png](attachments/image-2026-1-31_12-16-21.png)

Purge:

![image-2026-1-31_12-17-36.png](attachments/image-2026-1-31_12-17-36.png)

Eco Amendment

![image-2026-1-31_12-21-5.png](attachments/image-2026-1-31_12-21-5.png)

Cashflow Status

![image-2026-1-31_12-21-49.png](attachments/image-2026-1-31_12-21-49.png)

**EXPAND_END**

# Scenario6: C1 New (Auto SWIFT Suppressed) -> Purge C1 -> PFR (C1 withdrawal cancelled, C2 new in auto suppress)

**EXPAND: Expand**

7117011001

![image-2026-1-31_12-47-12-1.png](attachments/image-2026-1-31_12-47-12-1.png)

Purge:

![image-2026-1-31_12-47-17-1.png](attachments/image-2026-1-31_12-47-17-1.png)

PFR:

![image-2026-1-31_12-47-22-1.png](attachments/image-2026-1-31_12-47-22-1.png)

**EXPAND_END**

# Scenario7: C1 New (Auto SWIFT Suppressed) -> Purge C1 -> eco amendment (C1 withdrawal cancelled, C2 new auto suppress)

**EXPAND: Expand**

7117011002

![image-2026-1-31_12-46-11-1.png](attachments/image-2026-1-31_12-46-11-1.png)

Amendment 1 & Purge:

![image-2026-1-31_12-46-19-1.png](attachments/image-2026-1-31_12-46-19-1.png)

Amendment 2:

![image-2026-1-31_12-46-25-1.png](attachments/image-2026-1-31_12-46-25-1.png)

**EXPAND_END**

# Scenario8: C1 New (Netted and netting resultant is cashflow_suppressed) -> Purge C1 -> PFR (All component unneted in Waiting) -> Manual net and cashflow suppression->PFR (C2 withdrawal and C3 new will be hold in group blotter)

**EXPAND: Expand**

7114035794,7114035795 (N00000107754, N00000107755)

Booking

![image-2026-1-31_12-26-0-1.png](attachments/image-2026-1-31_12-26-0-1.png)

![image-2026-1-31_12-26-16-1.png](attachments/image-2026-1-31_12-26-16-1.png)

Purge:

![image-2026-1-31_12-26-28-1.png](attachments/image-2026-1-31_12-26-28-1.png)

PFR:

![image-2026-1-31_12-26-44-1.png](attachments/image-2026-1-31_12-26-44-1.png)

Net & Suppress

![image-2026-1-31_12-26-49-1.png](attachments/image-2026-1-31_12-26-49-1.png)

PFR again:

![image-2026-1-31_12-26-55-1.png](attachments/image-2026-1-31_12-26-55-1.png)

Group holding for non eco amend:

![image-2026-1-31_12-26-59-1.png](attachments/image-2026-1-31_12-26-59-1.png)

**EXPAND_END**

# 10K data loading Result:

![image-2026-1-31_12-59-11.png](attachments/image-2026-1-31_12-59-11.png)

History data total

![image-2026-1-31_13-8-5.png](attachments/image-2026-1-31_13-8-5.png)