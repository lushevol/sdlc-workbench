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
  "startedAt" : "2026-11-04T03:46:54.147180Z",
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
      "responseSha256" : "df819bd1cb4984858842ff0829a6650df54c0b4beb258f28f4bcec9817a1c70e"
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
      "responseSha256" : "0e3db98e7ca8eb07b8fabfb3b77fab65b2f49ecd49b3ec9807c1a7038fe6cd0d"
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
  "finishedAt" : "2026-11-04T03:46:54.318894Z"
}
```

## Account 2

```json
{
  "userId" : "bob",
  "startedAt" : "2026-11-04T03:46:54.320617Z",
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
      "responseSha256" : "66cecc10de0f7bada13e6c8e18c01f8800dc3045413d3f28d120f1c8a6010526"
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
      "responseSha256" : "8735344e7eb9dffecfe18b7d21743a17d8832ea8cd87891d173d525d46bd485f"
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
  "finishedAt" : "2026-11-04T03:46:54.334901Z"
}
```

## Account 3

```json
{
  "userId" : "service.demo",
  "startedAt" : "2026-11-04T03:46:54.335655Z",
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
      "responseSha256" : "076424797a4ae11a4390e96a33d388955ec7e99b7e94f6c74425c12e2932a67b"
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
      "responseSha256" : "17b997cf44187cab0fa6a3135d6ac36199262d0f123e5076996def241f3957ca"
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
  "finishedAt" : "2026-11-04T03:46:54.348762Z"
}
```

## Complete source bindings and result

```json
{
  "startedAt" : "2026-11-04T03:46:54.125474Z",
  "migrationVerified" : false,
  "scope" : "Exact original SDK lookup output for the declared account list and configured entities",
  "limits" : [ "This measures SDK-map parity; it does not certify all enterprise accounts or unassigned role definitions.", "Resolved data policies and real consumer authentication, logout, token renewal, and allowed/denied journeys need separate evidence.", "A completeness declaration records operator input; it does not authenticate its business authority." ],
  "gaps" : [ "Complete role definitions beyond assigned accounts remain outside this measurement.", "Resolved data restrictions are not returned by either SDK map.", "Downstream business journeys are not executed by this command." ],
  "accounts" : [ {
    "userId" : "alice",
    "startedAt" : "2026-11-04T03:46:54.147180Z",
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
        "responseSha256" : "df819bd1cb4984858842ff0829a6650df54c0b4beb258f28f4bcec9817a1c70e"
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
        "responseSha256" : "0e3db98e7ca8eb07b8fabfb3b77fab65b2f49ecd49b3ec9807c1a7038fe6cd0d"
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
    "finishedAt" : "2026-11-04T03:46:54.318894Z"
  }, {
    "userId" : "bob",
    "startedAt" : "2026-11-04T03:46:54.320617Z",
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
        "responseSha256" : "66cecc10de0f7bada13e6c8e18c01f8800dc3045413d3f28d120f1c8a6010526"
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
        "responseSha256" : "8735344e7eb9dffecfe18b7d21743a17d8832ea8cd87891d173d525d46bd485f"
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
    "finishedAt" : "2026-11-04T03:46:54.334901Z"
  }, {
    "userId" : "service.demo",
    "startedAt" : "2026-11-04T03:46:54.335655Z",
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
        "responseSha256" : "076424797a4ae11a4390e96a33d388955ec7e99b7e94f6c74425c12e2932a67b"
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
        "responseSha256" : "17b997cf44187cab0fa6a3135d6ac36199262d0f123e5076996def241f3957ca"
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
    "finishedAt" : "2026-11-04T03:46:54.348762Z"
  } ],
  "mode" : "replay",
  "populationDeclaredComplete" : true,
  "populationSource" : "Built-in synthetic fixture population; not enterprise users",
  "populationFileSha256" : "fdb463b39e86fc2023150d2763609fd3f6fa0b2d0f915b68d3fbae803500dd9b",
  "declaredAccounts" : [ "alice", "bob", "service.demo" ],
  "artifacts" : {
    "candidate" : {
      "sha256" : "9b4405045e02eab3db49443a5e7c320235efae9713db862b1d6af93cd984cb29",
      "revision" : "fd9a157e260850b6d9efa10da3223950ea61133a"
    },
    "baseline" : {
      "sha256" : "67d32bb9e6d4c5873712e77edbaf36ddff6882018b6f61860e4d7b9497c3b017",
      "revision" : "b0aa82005e7f14202f85f5ef583f25e42da9eeb3"
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
  "finishedAt" : "2026-11-04T03:46:54.349897Z",
  "exitCode" : 1
}
```

