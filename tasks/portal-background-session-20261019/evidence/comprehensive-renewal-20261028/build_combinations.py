"""Generate bounded interaction designs; no browser or service execution."""
import itertools
import json
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent
FACTORS = {
    "workspaces": ["1", "2", "8"],
    "loading": ["idle", "one-request", "two-requests", "mixed-outcomes"],
    "trigger": ["manual", "refresh-acquisition", "activity"],
    "access_ms": ["60000", "25000", "24999", "0"],
    "refresh": ["valid-four-hours", "valid-two-seconds", "expired", "missing", "revoked"],
    "response": ["usable", "rejected", "timeout", "malformed"],
    "ownership": ["unchanged-A", "logout-A", "replace-with-B"],
    "lifecycle": ["visible", "hidden-after-start", "resume-before-delivery", "unmount-after-start"],
    "transport": ["http", "graphql-websocket", "stomp", "sse", "long-poll", "file-transfer"],
    "delivery": ["fifo", "reverse", "same-tick"],
    "network": ["online", "slow", "reconnect-before-delivery"],
}
KEYS = list(FACTORS)
DOMAINS = list(FACTORS.values())
PAIRS = list(itertools.combinations(range(len(KEYS)), 2))

def pairs(row):
    return {(i, row[i], j, row[j]) for i,j in PAIRS}

universe = {(i,a,j,b) for i,j in PAIRS for a in DOMAINS[i] for b in DOMAINS[j]}
remaining = set(universe)
rows = []
rng = random.Random(20261028)
while remaining:
    # Every candidate completes a currently uncovered pair. The seed is fixed.
    targets = sorted(remaining)
    candidates = []
    for _ in range(500):
        i,a,j,b = targets[rng.randrange(len(targets))]
        row = [rng.choice(d) for d in DOMAINS]
        row[i],row[j] = a,b
        candidates.append(row)
    best = max(candidates, key=lambda r: len(pairs(r) & remaining))
    remaining.difference_update(pairs(best))
    rows.append(dict(zip(KEYS,best)))

for i,row in enumerate(rows,1):
    row["row_id"] = f"PAIR-{i:03}"
    row["expected_owner"] = {"unchanged-A":"A","logout-A":"none","replace-with-B":"B"}[row["ownership"]]
    row["expected_obsolete_installs"] = 0
    row["acceptance"] = "PROPOSED_INVARIANT; activity/transport policy remains separate"

high_risk = []
for i,vals in enumerate(itertools.product(FACTORS["trigger"],FACTORS["access_ms"],FACTORS["response"],FACTORS["ownership"]),1):
    row = dict(zip(["trigger","access_ms","response","ownership"],vals))
    row.update(row_id=f"RISK-{i:03}",expected_owner={"unchanged-A":"A","logout-A":"none","replace-with-B":"B"}[row["ownership"]])
    high_risk.append(row)

events = ["start-A", "logout-A", "login-B", "start-B", "reply-B", "reply-A"]
orders=[]
for p in itertools.permutations(events):
    pos={v:p.index(v) for v in events}
    if not (pos["start-A"]<pos["logout-A"]<pos["login-B"]<pos["start-B"]<pos["reply-B"]):
        continue
    if pos["reply-A"]<pos["start-A"]:
        continue
    for outcome in ["usable", "rejected", "malformed"]:
        orders.append(dict(row_id=f"ORDER-{len(orders)+1:03}",events=" > ".join(p),old_response=outcome,expected_owner="B"))

result = {
    "schema_version":1,"seed":20261028,"factors":FACTORS,
    "cartesian_population":math.prod(map(len,DOMAINS)),
    "feasibility":"All rows are event-injection designs. Start renewal before lifecycle changes. Guarded requests may produce no POST.",
    "constraints":[],"pairwise_rows":rows,"risk_rows":high_risk,"order_rows":orders,
    "coverage":{"required_pairs":len(universe),"covered_pairs":len(universe)-len(remaining),"uncovered_pairs":len(remaining)},
    "execution_status":"NOT_RUN",
    "limits":["Pair coverage measures only declared factor-value pairs, not business correctness.",
              "Fixture workspace counts and request timing values are representative, not supported product maxima.",
              "Transport authorization, activity eligibility, and recovery policies need separate reviewed oracles.",
              "No finite design enumerates all user histories, browser versions, failures, or security threats."]}
(OUT/"combinations.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"pairwise_rows":len(rows),"risk_rows":len(high_risk),"order_rows":len(orders),"population":result['cartesian_population'],"coverage":result['coverage']}))
