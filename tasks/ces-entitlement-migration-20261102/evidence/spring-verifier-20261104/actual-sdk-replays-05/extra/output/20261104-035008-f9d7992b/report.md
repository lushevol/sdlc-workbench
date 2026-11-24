---
writing_review:
  standard: ASD-STE100
  automated_check: NOT_RUN
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# EMS2 to CES SDK verification

**Result: DIFFERENCES.**

Mode: replay. Complete migration verified: false.

Percentages apply only to declared scope. Failed reads and zero denominators do not establish complete coverage.

## Scope

```json
"Exact original SDK lookup output for the declared account list and configured entities"
```

## Metrics

```json
{
  "declared" : 3,
  "assessed" : 3,
  "matching" : 2,
  "unassessed" : 0,
  "assessedAccountPercent" : 100.0,
  "sdkParityPercent" : 66.66666666666667
}
```

## Open gaps and evidence limits

```json
[ "Complete role definitions beyond assigned accounts remain outside this measurement.", "Resolved data restrictions are not returned by either SDK map.", "Downstream business journeys are not executed by this command." ]
```

## Account 1

```json
{
  "userId" : "alice",
  "startedAt" : "2026-11-04T03:50:08.984977Z",
  "baseline" : {
    "permissions" : {
      "LEGACY_APP:EMPTY" : { },
      "LEGACY_DATA:GLOBAL" : {
        "DATA" : [ "view" ]
      },
      "LEGACY_APP:READER" : {
        "TRADE" : [ "view", "view", "export" ]
      }
    },
    "requests" : [ {
      "method" : "GET",
      "path" : "/ems2/account/{userId}",
      "stage" : "EMS2_ACCOUNT",
      "status" : 200,
      "responseBytes" : 220,
      "responseSha256" : "5c311ec04866b2dc132136e06c622db1c19e67199bdf673ae3b6c213f390c891"
    }, {
      "method" : "POST",
      "path" : "/ems2/entitlements",
      "stage" : "EMS2_ENTITLEMENTS",
      "status" : 200,
      "responseBytes" : 632,
      "responseSha256" : "52892ec57492f64ebe0be7bb285950999274a10ecd85403ae4cbe878efbb99a7"
    } ],
    "errors" : [ ],
    "jarSha256" : "67d32bb9e6d4c5873712e77edbaf36ddff6882018b6f61860e4d7b9497c3b017"
  },
  "candidate" : {
    "permissions" : {
      "LEGACY_APP:READER" : {
        "TRADE" : [ "view", "view", "export" ]
      },
      "LEGACY_APP:EMPTY" : { },
      "LEGACY_DATA:GLOBAL" : {
        "DATA" : [ "view" ]
      }
    },
    "requests" : [ {
      "method" : "GET",
      "path" : "/ces/user/{userId}",
      "stage" : "CES_ASSIGNED_ROLES",
      "status" : 200,
      "responseBytes" : 572,
      "responseSha256" : "6aacef02085f3803b84d8da555b75f9bc3385bf21e0d599608f06f6576229321"
    } ],
    "errors" : [ ],
    "jarSha256" : "9b4405045e02eab3db49443a5e7c320235efae9713db862b1d6af93cd984cb29"
  },
  "comparison" : {
    "matches" : true,
    "metrics" : {
      "roles" : {
        "expected" : 3,
        "actual" : 3,
        "matched" : 3,
        "missing" : 0,
        "additional" : 0,
        "coveragePercent" : 100.0,
        "denominatorEmpty" : false
      },
      "subjects" : {
        "expected" : 2,
        "actual" : 2,
        "matched" : 2,
        "missing" : 0,
        "additional" : 0,
        "coveragePercent" : 100.0,
        "denominatorEmpty" : false
      },
      "roleScopedPermissions" : {
        "expected" : 4,
        "actual" : 4,
        "matched" : 4,
        "missing" : 0,
        "additional" : 0,
        "coveragePercent" : 100.0,
        "denominatorEmpty" : false
      },
      "roleScopedPermissionDefinitions" : {
        "expected" : 3,
        "actual" : 3,
        "matched" : 3,
        "missing" : 0,
        "additional" : 0,
        "coveragePercent" : 100.0,
        "denominatorEmpty" : false
      },
      "effectivePermissions" : {
        "expected" : 3,
        "actual" : 3,
        "matched" : 3,
        "missing" : 0,
        "additional" : 0,
        "coveragePercent" : 100.0,
        "denominatorEmpty" : false
      },
      "duplicateOccurrences" : {
        "baseline" : 1,
        "candidate" : 1
      },
      "comparedActionSequences" : 2,
      "actionSequenceMismatches" : 0,
      "validEmpty" : false,
      "validEmptyPermissions" : false,
      "missingPermissionOccurrences" : 0,
      "additionalPermissionOccurrences" : 0,
      "comparisonBoundary" : "Successful SDK maps only; role and subject keys, action multiplicity, and action order."
    },
    "differences" : [ ]
  },
  "status" : "MATCH",
  "finishedAt" : "2026-11-04T03:50:09.121902Z"
}
```

## Account 2

```json
{
  "userId" : "bob",
  "startedAt" : "2026-11-04T03:50:09.123578Z",
  "baseline" : {
    "permissions" : {
      "LEGACY_APP:READER" : {
        "TRADE" : [ "view", "view", "export" ]
      }
    },
    "requests" : [ {
      "method" : "GET",
      "path" : "/ems2/account/{userId}",
      "stage" : "EMS2_ACCOUNT",
      "status" : 200,
      "responseBytes" : 88,
      "responseSha256" : "02013ae2fbf1895d6b24174288596bb1db047c955c5a2059d6136c9037670846"
    }, {
      "method" : "POST",
      "path" : "/ems2/entitlements",
      "stage" : "EMS2_ENTITLEMENTS",
      "status" : 200,
      "responseBytes" : 482,
      "responseSha256" : "74102dad85fee412831029a7f96913f1c4744c68a7073ab8920508ebed45d00f"
    } ],
    "errors" : [ ],
    "jarSha256" : "67d32bb9e6d4c5873712e77edbaf36ddff6882018b6f61860e4d7b9497c3b017"
  },
  "candidate" : {
    "permissions" : {
      "LEGACY_APP:READER" : {
        "TRADE" : [ "view", "view", "export", "delete" ]
      }
    },
    "requests" : [ {
      "method" : "GET",
      "path" : "/ces/user/{userId}",
      "stage" : "CES_ASSIGNED_ROLES",
      "status" : 200,
      "responseBytes" : 379,
      "responseSha256" : "df565015b6a89c8786818cd5a7f4bc04584f492d5fe30f5df97d332acddb030e"
    } ],
    "errors" : [ ],
    "jarSha256" : "9b4405045e02eab3db49443a5e7c320235efae9713db862b1d6af93cd984cb29"
  },
  "comparison" : {
    "matches" : false,
    "metrics" : {
      "roles" : {
        "expected" : 1,
        "actual" : 1,
        "matched" : 1,
        "missing" : 0,
        "additional" : 0,
        "coveragePercent" : 100.0,
        "denominatorEmpty" : false
      },
      "subjects" : {
        "expected" : 1,
        "actual" : 1,
        "matched" : 1,
        "missing" : 0,
        "additional" : 0,
        "coveragePercent" : 100.0,
        "denominatorEmpty" : false
      },
      "roleScopedPermissions" : {
        "expected" : 3,
        "actual" : 4,
        "matched" : 3,
        "missing" : 0,
        "additional" : 1,
        "coveragePercent" : 100.0,
        "denominatorEmpty" : false
      },
      "roleScopedPermissionDefinitions" : {
        "expected" : 2,
        "actual" : 3,
        "matched" : 2,
        "missing" : 0,
        "additional" : 1,
        "coveragePercent" : 100.0,
        "denominatorEmpty" : false
      },
      "effectivePermissions" : {
        "expected" : 2,
        "actual" : 3,
        "matched" : 2,
        "missing" : 0,
        "additional" : 1,
        "coveragePercent" : 100.0,
        "denominatorEmpty" : false
      },
      "duplicateOccurrences" : {
        "baseline" : 1,
        "candidate" : 1
      },
      "comparedActionSequences" : 1,
      "actionSequenceMismatches" : 1,
      "validEmpty" : false,
      "validEmptyPermissions" : false,
      "missingPermissionOccurrences" : 0,
      "additionalPermissionOccurrences" : 1,
      "comparisonBoundary" : "Successful SDK maps only; role and subject keys, action multiplicity, and action order."
    },
    "differences" : [ {
      "kind" : "ADDITIONAL_PERMISSION",
      "role" : "LEGACY_APP:READER",
      "subject" : "TRADE",
      "action" : "delete",
      "baselineCount" : 0,
      "candidateCount" : 1,
      "missingOccurrences" : 0,
      "additionalOccurrences" : 1
    }, {
      "kind" : "ACTION_SEQUENCE_CHANGED",
      "role" : "LEGACY_APP:READER",
      "subject" : "TRADE",
      "baselineActions" : [ "view", "view", "export" ],
      "candidateActions" : [ "view", "view", "export", "delete" ]
    }, {
      "kind" : "ADDITIONAL_EFFECTIVE_PERMISSION",
      "entity" : "LEGACY_APP",
      "subject" : "TRADE",
      "action" : "delete"
    } ]
  },
  "status" : "DIFFERENT",
  "finishedAt" : "2026-11-04T03:50:09.137544Z"
}
```

## Account 3

```json
{
  "userId" : "service.demo",
  "startedAt" : "2026-11-04T03:50:09.138267Z",
  "baseline" : {
    "permissions" : {
      "LEGACY_SYSTEM:SERVICE" : {
        "SYSTEM" : [ "query" ]
      }
    },
    "requests" : [ {
      "method" : "GET",
      "path" : "/ems2/account/{userId}",
      "stage" : "EMS2_ACCOUNT",
      "status" : 200,
      "responseBytes" : 92,
      "responseSha256" : "4d10aeb68d2603ef5f3e7bf770a1f8cc5f71dd3e9adbb74411ab78a1880b499e"
    }, {
      "method" : "POST",
      "path" : "/ems2/entitlements",
      "stage" : "EMS2_ENTITLEMENTS",
      "status" : 200,
      "responseBytes" : 199,
      "responseSha256" : "ce960a7edc3f16d924bcd462cf8b149fc238aa72619c19299600e569b5322cec"
    } ],
    "errors" : [ ],
    "jarSha256" : "67d32bb9e6d4c5873712e77edbaf36ddff6882018b6f61860e4d7b9497c3b017"
  },
  "candidate" : {
    "permissions" : {
      "LEGACY_SYSTEM:SERVICE" : {
        "SYSTEM" : [ "query" ]
      }
    },
    "requests" : [ {
      "method" : "GET",
      "path" : "/ces/user/{userId}",
      "stage" : "CES_ASSIGNED_ROLES",
      "status" : 200,
      "responseBytes" : 171,
      "responseSha256" : "0f0139352502f4a5ca3b0282f92ba659f7f171c89d56034339ea70ba08472d28"
    } ],
    "errors" : [ ],
    "jarSha256" : "9b4405045e02eab3db49443a5e7c320235efae9713db862b1d6af93cd984cb29"
  },
  "comparison" : {
    "matches" : true,
    "metrics" : {
      "roles" : {
        "expected" : 1,
        "actual" : 1,
        "matched" : 1,
        "missing" : 0,
        "additional" : 0,
        "coveragePercent" : 100.0,
        "denominatorEmpty" : false
      },
      "subjects" : {
        "expected" : 1,
        "actual" : 1,
        "matched" : 1,
        "missing" : 0,
        "additional" : 0,
        "coveragePercent" : 100.0,
        "denominatorEmpty" : false
      },
      "roleScopedPermissions" : {
        "expected" : 1,
        "actual" : 1,
        "matched" : 1,
        "missing" : 0,
        "additional" : 0,
        "coveragePercent" : 100.0,
        "denominatorEmpty" : false
      },
      "roleScopedPermissionDefinitions" : {
        "expected" : 1,
        "actual" : 1,
        "matched" : 1,
        "missing" : 0,
        "additional" : 0,
        "coveragePercent" : 100.0,
        "denominatorEmpty" : false
      },
      "effectivePermissions" : {
        "expected" : 1,
        "actual" : 1,
        "matched" : 1,
        "missing" : 0,
        "additional" : 0,
        "coveragePercent" : 100.0,
        "denominatorEmpty" : false
      },
      "duplicateOccurrences" : {
        "baseline" : 0,
        "candidate" : 0
      },
      "comparedActionSequences" : 1,
      "actionSequenceMismatches" : 0,
      "validEmpty" : false,
      "validEmptyPermissions" : false,
      "missingPermissionOccurrences" : 0,
      "additionalPermissionOccurrences" : 0,
      "comparisonBoundary" : "Successful SDK maps only; role and subject keys, action multiplicity, and action order."
    },
    "differences" : [ ]
  },
  "status" : "MATCH",
  "finishedAt" : "2026-11-04T03:50:09.151103Z"
}
```

## Complete source bindings and result

```json
{
  "startedAt" : "2026-11-04T03:50:08.964145Z",
  "migrationVerified" : false,
  "scope" : "Exact original SDK lookup output for the declared account list and configured entities",
  "limits" : [ "This measures SDK-map parity; it does not certify all enterprise accounts or unassigned role definitions.", "Resolved data policies and real consumer authentication, logout, token renewal, and allowed/denied journeys need separate evidence.", "A completeness declaration records operator input; it does not authenticate its business authority." ],
  "gaps" : [ "Complete role definitions beyond assigned accounts remain outside this measurement.", "Resolved data restrictions are not returned by either SDK map.", "Downstream business journeys are not executed by this command." ],
  "accounts" : [ {
    "userId" : "alice",
    "startedAt" : "2026-11-04T03:50:08.984977Z",
    "baseline" : {
      "permissions" : {
        "LEGACY_APP:EMPTY" : { },
        "LEGACY_DATA:GLOBAL" : {
          "DATA" : [ "view" ]
        },
        "LEGACY_APP:READER" : {
          "TRADE" : [ "view", "view", "export" ]
        }
      },
      "requests" : [ {
        "method" : "GET",
        "path" : "/ems2/account/{userId}",
        "stage" : "EMS2_ACCOUNT",
        "status" : 200,
        "responseBytes" : 220,
        "responseSha256" : "5c311ec04866b2dc132136e06c622db1c19e67199bdf673ae3b6c213f390c891"
      }, {
        "method" : "POST",
        "path" : "/ems2/entitlements",
        "stage" : "EMS2_ENTITLEMENTS",
        "status" : 200,
        "responseBytes" : 632,
        "responseSha256" : "52892ec57492f64ebe0be7bb285950999274a10ecd85403ae4cbe878efbb99a7"
      } ],
      "errors" : [ ],
      "jarSha256" : "67d32bb9e6d4c5873712e77edbaf36ddff6882018b6f61860e4d7b9497c3b017"
    },
    "candidate" : {
      "permissions" : {
        "LEGACY_APP:READER" : {
          "TRADE" : [ "view", "view", "export" ]
        },
        "LEGACY_APP:EMPTY" : { },
        "LEGACY_DATA:GLOBAL" : {
          "DATA" : [ "view" ]
        }
      },
      "requests" : [ {
        "method" : "GET",
        "path" : "/ces/user/{userId}",
        "stage" : "CES_ASSIGNED_ROLES",
        "status" : 200,
        "responseBytes" : 572,
        "responseSha256" : "6aacef02085f3803b84d8da555b75f9bc3385bf21e0d599608f06f6576229321"
      } ],
      "errors" : [ ],
      "jarSha256" : "9b4405045e02eab3db49443a5e7c320235efae9713db862b1d6af93cd984cb29"
    },
    "comparison" : {
      "matches" : true,
      "metrics" : {
        "roles" : {
          "expected" : 3,
          "actual" : 3,
          "matched" : 3,
          "missing" : 0,
          "additional" : 0,
          "coveragePercent" : 100.0,
          "denominatorEmpty" : false
        },
        "subjects" : {
          "expected" : 2,
          "actual" : 2,
          "matched" : 2,
          "missing" : 0,
          "additional" : 0,
          "coveragePercent" : 100.0,
          "denominatorEmpty" : false
        },
        "roleScopedPermissions" : {
          "expected" : 4,
          "actual" : 4,
          "matched" : 4,
          "missing" : 0,
          "additional" : 0,
          "coveragePercent" : 100.0,
          "denominatorEmpty" : false
        },
        "roleScopedPermissionDefinitions" : {
          "expected" : 3,
          "actual" : 3,
          "matched" : 3,
          "missing" : 0,
          "additional" : 0,
          "coveragePercent" : 100.0,
          "denominatorEmpty" : false
        },
        "effectivePermissions" : {
          "expected" : 3,
          "actual" : 3,
          "matched" : 3,
          "missing" : 0,
          "additional" : 0,
          "coveragePercent" : 100.0,
          "denominatorEmpty" : false
        },
        "duplicateOccurrences" : {
          "baseline" : 1,
          "candidate" : 1
        },
        "comparedActionSequences" : 2,
        "actionSequenceMismatches" : 0,
        "validEmpty" : false,
        "validEmptyPermissions" : false,
        "missingPermissionOccurrences" : 0,
        "additionalPermissionOccurrences" : 0,
        "comparisonBoundary" : "Successful SDK maps only; role and subject keys, action multiplicity, and action order."
      },
      "differences" : [ ]
    },
    "status" : "MATCH",
    "finishedAt" : "2026-11-04T03:50:09.121902Z"
  }, {
    "userId" : "bob",
    "startedAt" : "2026-11-04T03:50:09.123578Z",
    "baseline" : {
      "permissions" : {
        "LEGACY_APP:READER" : {
          "TRADE" : [ "view", "view", "export" ]
        }
      },
      "requests" : [ {
        "method" : "GET",
        "path" : "/ems2/account/{userId}",
        "stage" : "EMS2_ACCOUNT",
        "status" : 200,
        "responseBytes" : 88,
        "responseSha256" : "02013ae2fbf1895d6b24174288596bb1db047c955c5a2059d6136c9037670846"
      }, {
        "method" : "POST",
        "path" : "/ems2/entitlements",
        "stage" : "EMS2_ENTITLEMENTS",
        "status" : 200,
        "responseBytes" : 482,
        "responseSha256" : "74102dad85fee412831029a7f96913f1c4744c68a7073ab8920508ebed45d00f"
      } ],
      "errors" : [ ],
      "jarSha256" : "67d32bb9e6d4c5873712e77edbaf36ddff6882018b6f61860e4d7b9497c3b017"
    },
    "candidate" : {
      "permissions" : {
        "LEGACY_APP:READER" : {
          "TRADE" : [ "view", "view", "export", "delete" ]
        }
      },
      "requests" : [ {
        "method" : "GET",
        "path" : "/ces/user/{userId}",
        "stage" : "CES_ASSIGNED_ROLES",
        "status" : 200,
        "responseBytes" : 379,
        "responseSha256" : "df565015b6a89c8786818cd5a7f4bc04584f492d5fe30f5df97d332acddb030e"
      } ],
      "errors" : [ ],
      "jarSha256" : "9b4405045e02eab3db49443a5e7c320235efae9713db862b1d6af93cd984cb29"
    },
    "comparison" : {
      "matches" : false,
      "metrics" : {
        "roles" : {
          "expected" : 1,
          "actual" : 1,
          "matched" : 1,
          "missing" : 0,
          "additional" : 0,
          "coveragePercent" : 100.0,
          "denominatorEmpty" : false
        },
        "subjects" : {
          "expected" : 1,
          "actual" : 1,
          "matched" : 1,
          "missing" : 0,
          "additional" : 0,
          "coveragePercent" : 100.0,
          "denominatorEmpty" : false
        },
        "roleScopedPermissions" : {
          "expected" : 3,
          "actual" : 4,
          "matched" : 3,
          "missing" : 0,
          "additional" : 1,
          "coveragePercent" : 100.0,
          "denominatorEmpty" : false
        },
        "roleScopedPermissionDefinitions" : {
          "expected" : 2,
          "actual" : 3,
          "matched" : 2,
          "missing" : 0,
          "additional" : 1,
          "coveragePercent" : 100.0,
          "denominatorEmpty" : false
        },
        "effectivePermissions" : {
          "expected" : 2,
          "actual" : 3,
          "matched" : 2,
          "missing" : 0,
          "additional" : 1,
          "coveragePercent" : 100.0,
          "denominatorEmpty" : false
        },
        "duplicateOccurrences" : {
          "baseline" : 1,
          "candidate" : 1
        },
        "comparedActionSequences" : 1,
        "actionSequenceMismatches" : 1,
        "validEmpty" : false,
        "validEmptyPermissions" : false,
        "missingPermissionOccurrences" : 0,
        "additionalPermissionOccurrences" : 1,
        "comparisonBoundary" : "Successful SDK maps only; role and subject keys, action multiplicity, and action order."
      },
      "differences" : [ {
        "kind" : "ADDITIONAL_PERMISSION",
        "role" : "LEGACY_APP:READER",
        "subject" : "TRADE",
        "action" : "delete",
        "baselineCount" : 0,
        "candidateCount" : 1,
        "missingOccurrences" : 0,
        "additionalOccurrences" : 1
      }, {
        "kind" : "ACTION_SEQUENCE_CHANGED",
        "role" : "LEGACY_APP:READER",
        "subject" : "TRADE",
        "baselineActions" : [ "view", "view", "export" ],
        "candidateActions" : [ "view", "view", "export", "delete" ]
      }, {
        "kind" : "ADDITIONAL_EFFECTIVE_PERMISSION",
        "entity" : "LEGACY_APP",
        "subject" : "TRADE",
        "action" : "delete"
      } ]
    },
    "status" : "DIFFERENT",
    "finishedAt" : "2026-11-04T03:50:09.137544Z"
  }, {
    "userId" : "service.demo",
    "startedAt" : "2026-11-04T03:50:09.138267Z",
    "baseline" : {
      "permissions" : {
        "LEGACY_SYSTEM:SERVICE" : {
          "SYSTEM" : [ "query" ]
        }
      },
      "requests" : [ {
        "method" : "GET",
        "path" : "/ems2/account/{userId}",
        "stage" : "EMS2_ACCOUNT",
        "status" : 200,
        "responseBytes" : 92,
        "responseSha256" : "4d10aeb68d2603ef5f3e7bf770a1f8cc5f71dd3e9adbb74411ab78a1880b499e"
      }, {
        "method" : "POST",
        "path" : "/ems2/entitlements",
        "stage" : "EMS2_ENTITLEMENTS",
        "status" : 200,
        "responseBytes" : 199,
        "responseSha256" : "ce960a7edc3f16d924bcd462cf8b149fc238aa72619c19299600e569b5322cec"
      } ],
      "errors" : [ ],
      "jarSha256" : "67d32bb9e6d4c5873712e77edbaf36ddff6882018b6f61860e4d7b9497c3b017"
    },
    "candidate" : {
      "permissions" : {
        "LEGACY_SYSTEM:SERVICE" : {
          "SYSTEM" : [ "query" ]
        }
      },
      "requests" : [ {
        "method" : "GET",
        "path" : "/ces/user/{userId}",
        "stage" : "CES_ASSIGNED_ROLES",
        "status" : 200,
        "responseBytes" : 171,
        "responseSha256" : "0f0139352502f4a5ca3b0282f92ba659f7f171c89d56034339ea70ba08472d28"
      } ],
      "errors" : [ ],
      "jarSha256" : "9b4405045e02eab3db49443a5e7c320235efae9713db862b1d6af93cd984cb29"
    },
    "comparison" : {
      "matches" : true,
      "metrics" : {
        "roles" : {
          "expected" : 1,
          "actual" : 1,
          "matched" : 1,
          "missing" : 0,
          "additional" : 0,
          "coveragePercent" : 100.0,
          "denominatorEmpty" : false
        },
        "subjects" : {
          "expected" : 1,
          "actual" : 1,
          "matched" : 1,
          "missing" : 0,
          "additional" : 0,
          "coveragePercent" : 100.0,
          "denominatorEmpty" : false
        },
        "roleScopedPermissions" : {
          "expected" : 1,
          "actual" : 1,
          "matched" : 1,
          "missing" : 0,
          "additional" : 0,
          "coveragePercent" : 100.0,
          "denominatorEmpty" : false
        },
        "roleScopedPermissionDefinitions" : {
          "expected" : 1,
          "actual" : 1,
          "matched" : 1,
          "missing" : 0,
          "additional" : 0,
          "coveragePercent" : 100.0,
          "denominatorEmpty" : false
        },
        "effectivePermissions" : {
          "expected" : 1,
          "actual" : 1,
          "matched" : 1,
          "missing" : 0,
          "additional" : 0,
          "coveragePercent" : 100.0,
          "denominatorEmpty" : false
        },
        "duplicateOccurrences" : {
          "baseline" : 0,
          "candidate" : 0
        },
        "comparedActionSequences" : 1,
        "actionSequenceMismatches" : 0,
        "validEmpty" : false,
        "validEmptyPermissions" : false,
        "missingPermissionOccurrences" : 0,
        "additionalPermissionOccurrences" : 0,
        "comparisonBoundary" : "Successful SDK maps only; role and subject keys, action multiplicity, and action order."
      },
      "differences" : [ ]
    },
    "status" : "MATCH",
    "finishedAt" : "2026-11-04T03:50:09.151103Z"
  } ],
  "mode" : "replay",
  "populationDeclaredComplete" : true,
  "populationSource" : "Built-in synthetic fixture population; not enterprise users",
  "populationFileSha256" : "fdb463b39e86fc2023150d2763609fd3f6fa0b2d0f915b68d3fbae803500dd9b",
  "declaredAccounts" : [ "alice", "bob", "service.demo" ],
  "artifacts" : {
    "baseline" : {
      "sha256" : "67d32bb9e6d4c5873712e77edbaf36ddff6882018b6f61860e4d7b9497c3b017",
      "revision" : "b0aa82005e7f14202f85f5ef583f25e42da9eeb3"
    },
    "candidate" : {
      "sha256" : "9b4405045e02eab3db49443a5e7c320235efae9713db862b1d6af93cd984cb29",
      "revision" : "fd9a157e260850b6d9efa10da3223950ea61133a"
    }
  },
  "artifactManifestSha256" : "7689cda4a812541baaa2f4cd4b5f3034b1734d8d2c06aa19bbf1eff912817355",
  "mappingSha256" : "c5c864cc3daed831db072da96c58d0ccb54621305749cf58ec28bb61b7fe47bb",
  "entities" : [ "LEGACY_APP", "LEGACY_DATA", "LEGACY_SYSTEM" ],
  "fixture" : "Built-in synthetic HTTP fixtures; both actual SDK jars execute against loopback HTTP.",
  "metrics" : {
    "declared" : 3,
    "assessed" : 3,
    "matching" : 2,
    "unassessed" : 0,
    "assessedAccountPercent" : 100.0,
    "sdkParityPercent" : 66.66666666666667
  },
  "status" : "DIFFERENCES",
  "finishedAt" : "2026-11-04T03:50:09.152167Z",
  "exitCode" : 1
}
```

