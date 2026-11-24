# **Auto Stamping process**

# **ssi exception generate**

To generate PRE_ADHOC_ERROR Exception need any condition as below：

1. checker approve : after close Vostro/Nostro Exception
2. auto SSI stamping: have no any Vostro/Nostro Exception
3. auto SSI stamping: have Vostro/Nostro Exception && adleToSendPerSSIAdhocException== true

PRE_ADHOC_ERROR Exception will close before ADHOC_SSI_EXCEPTION generation, and generate again after ADHOC_SSI_EXCEPTION close

ADHOC_SSI_EXCEPTION generate when perform adhoc SSI reject or submit

# **Vostro trigger stamping**

# **Nostro trigger stamping**