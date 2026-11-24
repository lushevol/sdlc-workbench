"""Retained test-design inputs. Does not execute application tests."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
REV = "66c6411ade58e4d134e381c2baee8ad3f76a8dbf"
HOME = "repos/ui/mfe-base/src/pages/Home/common/useController.ts"
TIMEOUT = "repos/ui/mfe-base/src/components/Timeout/common/useController.ts"
SERVICE = "repos/ui/mfe-base/src/hooks/service/index.ts"
RESPONSE = "repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts"
EPOCH = "repos/ui/mfe-base/src/utils/sessionEpoch.ts"
CASES = []

def add(code, title, family, use_case, given, when, then, ac=(), basis="observed", source=HOME, lines="1-205", level="browser-e2e", limits="New definition; executable binding and target execution remain unavailable."):
    CASES.append(dict(id=code, title=title, family=family, use_case=use_case,
        level=level, basis=basis, ac_ids=list(ac), given=given, when=when,
        then=then, sources=[dict(path=source, lines=lines, revision=REV)],
        limits=limits, priority="P1" if basis == "proposed-security" else "P2"))

for i, (activity, ac) in enumerate([( "mouse movement", "AC-1"), ("keyboard input", "AC-2"), ("scroll activity", "AC-3")], 1):
    add(f"RN-A{i:03}", f"Continuous {activity} reaches the requested renewal target", "activity", "UC-R01",
        ["User A has access valid for at least 30 seconds in workspace WA", "the fixture uses successful renewal responses and the controlled clock"],
        [f"User A generates {activity} every 100 milliseconds for 15 seconds"],
        ["the recorded successful renewal count is at least 1 before the 15-second interval ends", "a protected validation request with the installed access credential returns result true"],
        [ac], "target", lines="60-79")

for i, (condition, action, result) in enumerate([
    ("User A alternates pointer, keyboard, and scroll input", "the fixture repeats the input sequence every 100 milliseconds for 15 seconds", "the successful renewal count is at least 1 during that interval"),
    ("User A uses keyboard navigation without pointer input", "User A continues keyboard input every 100 milliseconds for 15 seconds", "the successful renewal count is at least 1 during that interval"),
    ("User A scrolls a nested application pane", "User A sends scroll input every 100 milliseconds for 15 seconds inside that pane", "the trace records whether the shell receives each eligible scroll event"),
    ("User A edits inside a cross-origin iframe", "User A types continuously for 15 seconds inside the iframe", "the trace distinguishes iframe input from shell-received input"),
    ("User A reads without input", "the controlled clock advances past access expiry", "the timeout observation records the access-expired state"),
    ("User A generates only WebSocket heartbeats", "the controlled clock advances past access expiry", "the trace records 0 pointer, keyboard, and scroll events"),
    ("User A generates synthetic script events", "the fixture dispatches 100 synthetic activity events", "the trace records the trusted flag for all 100 events"),
    ("User A uses a touch screen", "User A swipes the application pane for 15 seconds", "the trace records which shell event types the browser emits"),
    ("User A uses an input method editor", "User A composes and commits text in workspace WA", "the trace records composition and keyboard events separately"),
    ("User A holds one keyboard key", "the fixture emits repeat key events every 100 milliseconds for 15 seconds", "the successful renewal count is at least 1 during that interval"),
    ("User A moves the pointer every 4900 milliseconds", "the fixture continues activity through two access deadlines", "the trace records pending activity timers and successful renewals at both deadlines"),
    ("User A moves the pointer then stops", "the controlled clock advances 5000 milliseconds after the last movement", "the source-observation trace records the scheduled activity callback exactly once"),
],4):
    open_policy = i in {7,9,10,11,12,14}
    acs = {4:["AC-1","AC-2","AC-3"],5:["AC-2"],6:["AC-3"],13:["AC-2"]}.get(i, [])
    if i==6:
        condition="User A scrolls a same-origin nested application pane"
        result="the successful renewal count is at least 1 during that 15-second interval"
    add(f"RN-A{i:03}", condition, "activity", "UC-R02", ["User A has a valid session in WA with at least 30 seconds of access remaining",condition], [action], [result],
        acs, "policy-open" if open_policy else "target" if acs else "observed",
        lines="60-79", limits=("Activity eligibility or acceptance for this input context needs owner review; record observations only." if open_policy else "Target assertion; existing continuous-activity failures remain visible."))

for i, remaining in enumerate([24999,25000,25001],1):
    add(f"RN-B{i:03}", f"Activity request boundary at {remaining} milliseconds", "timing", "UC-R03",
        [f"User A has access remaining {remaining} milliseconds", "logout is false and the activity endpoint is isolated"],
        ["the fixture invokes the shared activity renewal function once"],
        [f"the activity POST count equals {0 if remaining < 25000 else 1}"],
        source="repos/ui/mfe-base/src/hooks/service/util/extend.ts", lines="8-30", level="component-integration")
for i, delta in enumerate([-1,0,1],4):
    add(f"RN-B{i:03}", f"Manual recovery deadline offset {delta} milliseconds", "timing", "UC-R04",
        [f"the controlled clock is {abs(delta)} milliseconds {'before' if delta < 0 else 'after' if delta > 0 else 'at'} the refresh expiry minus 2000 milliseconds", "User A sees the timeout dialog and has no renewal pending"],
        ["the fixture invokes the timeout controller renewal action once"],
        [f"the relogin request count equals {1 if delta < 0 else 0}"], source=TIMEOUT, lines="75-177", level="component-integration")
for i, delta in enumerate([-1,0,1],7):
    add(f"RN-B{i:03}", f"Refresh reuse boundary offset {delta} milliseconds", "timing", "UC-R05",
        [f"User A has refresh validity of {10800000 + delta} milliseconds", "the fixture records POST calls independently of promise settlement"],
        ["the fixture invokes getRefreshToken once"], [f"the refresh-token acquisition POST count equals {0 if delta > 0 else 1}"],
        source=SERVICE, lines="29-118", level="component-integration")
for i,(condition,action,then) in enumerate([
    ("a scheduled acquisition callback is 1 millisecond late with access still valid", "the fixture delivers the callback", "the acquisition POST count equals 1"),
    ("a scheduled acquisition callback arrives after access expiry", "the fixture delivers the callback", "the acquisition POST count equals 0"),
    ("the browser becomes hidden before the scheduled callback", "the fixture delivers the callback while hidden", "the scheduled acquisition POST count equals 0"),
    ("access has expired while the browser is suspended", "the fixture resumes the browser and dispatches visibilitychange", "the timeout state equals visible"),
    ("the system clock moves backward by 10 minutes", "the fixture reconciles the session on visibility return", "the trace records absolute access expiry and the effective clock before any renewal decision"),
    ("the system clock moves forward by 24 hours", "the fixture reconciles the session on visibility return", "the timeout state equals visible"),
    ("the timezone changes from UTC to Asia/Singapore without changing epoch time", "the fixture reconciles the session", "the computed access deadline equals its pre-change epoch timestamp"),
    ("access and refresh expire at the same epoch timestamp", "the controlled clock reaches that timestamp", "the acquisition POST count after that timestamp equals 0"),
],10):
    add(f"RN-B{i:03}", condition, "timing", "UC-R06", ["User A has a controlled session in WA",condition] + (["the document is visible with no prompt, logout, or acquisition pending", "refresh remains valid for one hour"] if i==10 else []), [action],[then],
        basis="policy-open" if i==14 else "observed", lines="110-205")

for i,(condition,action,expected) in enumerate([
    ("the relogin response is held pending", "User A clicks the button labeled Extend inside the timeout dialog", ["the successful dialog closure count equals 0 while the request is pending"]),
    ("the relogin response supplies usable future access", "User A clicks the button labeled Extend inside the timeout dialog", ["the successful dialog closure count equals 1 after response completion", "the next protected validation returns result true using the installed access"]),
    ("the relogin response rejects while refresh remains usable", "User A clicks the button labeled Extend inside the timeout dialog", ["the successful dialog closure count equals 0", "the controller permits another renewal attempt after rejection"]),
    ("the first relogin rejects and the second response supplies usable access", "the fixture performs two ordered manual renewal attempts", ["the relogin POST count equals 2", "the successful dialog closure count equals 1 after the second response"]),
    ("the first relogin is pending", "the fixture activates the Extend button 20 times before settlement", ["the relogin POST count equals 1", "the successful dialog closure count equals 0 before settlement"]),
    ("the relogin response remains pending", "User A activates the timeout dialog logout action", ["the pending relogin signal is aborted", "a later relogin response installs 0 credentials"]),
    ("the relogin response remains pending", "the fixture unmounts the timeout controller", ["the later response causes 0 dialog closure callbacks on the unmounted controller"]),
    ("the relogin request fails after the recovery deadline", "the fixture delivers the rejection", ["the next manual renewal action sends 0 relogin POSTs"]),
    ("the relogin request starts before the recovery deadline and succeeds after it", "the fixture delivers a response with usable access", ["the source-observation trace records whether pending renewal suppresses local logout", "the next protected validation uses the actual installed access"]),
    ("an access-only acquisition promise is pending when the timeout mounts", "the fixture delivers acquisition settlement without credentials", ["the trace distinguishes promise settlement from credential installation", "the successful renewal count equals 0 without usable returned access"]),
    ("the timeout controller belongs to session A and session B replaces A", "User A activates the stale controller renewal action", ["the stale controller sends 0 relogin requests for session B"]),
    ("the timeout controller belongs to session A and session B replaces A", "User A activates the stale controller logout action", ["the stale controller starts 0 logout requests for session B"]),
],1):
    ac = ["AC-5"] if i in [1,5] else ["AC-6"] if i==2 else ["AC-7"] if i in [3,4] else []
    add(f"RN-M{i:03}", condition, "manual", "UC-R07" if i<6 else "UC-R08",
        ["User A sees the source-defined timeout dialog with usable refresh unless the case states otherwise",condition], [action],expected,
        ac, "target" if ac else "observed", source=TIMEOUT, lines="24-177",
        limits="Source-derived UI label; runtime accessible name and uniqueness need verification. Late-response acceptance needs service-time policy review." if i==9 else "Source-derived UI action; new end-to-end binding and target execution remain unavailable.")

invalid_payloads = [
    ("missing access header", "no access credential"), ("empty access header", "an empty string"),
    ("unreadable access payload", "the string not-a-jwt"), ("missing exp", "a payload without exp"),
    ("string exp", "a payload with exp as a numeric string"), ("expired exp", "a payload exp one second before the controlled clock"),
    ("exp at current time", "a payload exp equal to the controlled clock"), ("missing iat", "a payload without iat"),
    ("zero iat", "a payload with iat equal to 0"), ("negative iat", "a payload with iat equal to -1"),
    ("iat equals exp", "a payload with iat equal to exp"), ("iat exceeds exp", "a payload with iat greater than exp"),
    ("nonfinite exp multiplication", "a numeric exp whose millisecond conversion overflows"),
]
for i,(title,payload) in enumerate(invalid_payloads,1):
    add(f"RN-P{i:03}", f"Relogin rejects {title}", "payload", "UC-R09",
        ["User A has a pending manual relogin with no logout requested",f"the response supplies {payload}"],
        ["the fixture delivers the relogin response through the real response interceptor"],
        ["the successful dialog closure count equals 0", "the response installs 0 access credentials"],
        ["AC-5","AC-7"], "observed", source=RESPONSE, lines="37-89", level="component-integration")
for i,(title,payload) in enumerate([
    ("valid lowercase header", "a valid access token in single-ui-authorization"),
    ("valid title-case header", "a valid access token in Single-UI-Authorization"),
    ("missing refresh on successful access renewal", "valid renewed access without a replacement refresh token"),
    ("future issued-at", "a future iat that is less than exp"),
    ("conflicting access header casing", "different access values under lowercase and title-case header names"),
],14):
    add(f"RN-P{i:03}", title, "payload", "UC-R09", ["User A has a pending manual renewal",f"the response contains {payload}"],
        ["the fixture delivers the response"],
        ["the trace records the selected header value and installed expiry", "a service-side protected validation records the accepted identity"],
        basis="policy-open" if i>=16 else "observed", source=RESPONSE, lines="37-89",level="component-integration" if i==18 else "browser-e2e")

for i,(outcome,action,expected) in enumerate([
    ("success", "the fixture logs out A before response delivery", "the late success installs 0 credentials"),
    ("failure", "the fixture logs out A before response delivery", "the late failure changes 0 current authentication fields"),
    ("success", "the fixture replaces A with authenticated session B before response delivery", "the final installed identity equals B"),
    ("failure", "the fixture replaces A with authenticated session B before response delivery", "the final installed identity equals B"),
    ("success", "the fixture aborts the request before response delivery", "the response installs 0 credentials"),
    ("success", "the fixture starts a fresh login while renewal is pending", "the old renewal installs 0 credentials after the login epoch changes"),
    ("failure", "the fixture starts a fresh login while renewal is pending", "the old failure clears 0 fields in the new login epoch"),
    ("success", "the fixture completes A to B to A account switching before delivery", "the old response changes 0 fields in the replacement A session"),
],1):
    add(f"RN-R{i:03}", f"Late renewal {outcome}: {action.removeprefix('the fixture ')}", "race", "UC-R10",
        ["session A owns one held renewal request",f"the held response outcome is {outcome}"], [action,"the fixture delivers the held response"],
        [expected], basis="proposed-security", source=EPOCH, lines="1-20")

for i,(n,kind) in enumerate([(1,"acquisition"),(2,"acquisition"),(8,"acquisition"),(64,"acquisition"),(2,"manual"),(20,"manual")],1):
    add(f"RN-R{i+8:03}", f"{n} simultaneous {kind} callers share one pending operation", "race", "UC-R11",
        ["User A has unchanged access identity and session epoch", "refresh reuse does not suppress acquisition", "the first response remains pending"] + (["all manual calls use the same mounted Timeout controller extend action"] if kind=="manual" else []),
        [f"the fixture invokes {n} {'same-controller extend actions' if kind=='manual' else 'acquisition callers'} before settlement"],
        [f"the { 'refresh-token acquisition' if kind=='acquisition' else 'relogin'} POST count equals 1", "all accepted callers observe the same final installed identity"],
        basis="observed", source=SERVICE if kind=="acquisition" else TIMEOUT, lines="29-177", level="component-integration")

for i,(condition,action,then) in enumerate([
    ("an old acquisition is pending when access changes", "the fixture requests acquisition for the new access", "the old abort signal equals aborted and the new request owner equals current access"),
    ("an old aborted request settles after a new request starts", "the fixture settles the old request", "the pending-request pointer still identifies the new request"),
    ("two acquisition callers have different session epochs", "the fixture delivers responses in reverse order", "only the current epoch response can install credentials"),
    ("the timeout timer and renewal success have the same due time", "the fixture runs both possible delivery orders", "each order records closure count, logout count, and final owner separately"),
    ("a protected response and a relogin response finish together", "the fixture runs both possible response orders", "the final owner remains A and the trace records the final access expiry"),
    ("a stale unauthorized response arrives after successful renewal", "the fixture delivers the unauthorized response", "the trace records whether the renewed session is cleared by the old response"),
],15):
    add(f"RN-R{i:03}", condition, "race", "UC-R12", ["User A has an isolated session",condition],[action],[then],
        basis="policy-open" if i>=18 else "observed", source=SERVICE, lines="29-135")

for i,(n,mode) in enumerate([(1,"success"),(2,"success"),(10,"success"),(1000,"success"),(2,"failure then success"),(10,"failure then success"),(100,"logout then login"),(100,"mount then unmount"),(100,"hide then show"),(100,"workspace switch")],1):
    add(f"RN-L{i:03}", f"Repeat {mode} for {n} cycles", "loop", "UC-R13",
        ["User A uses a fresh isolated browser context", "the fixture records request owners, credentials, callbacks, timers, and listeners"],
        [f"the fixture completes {n} ordered {mode} cycles", "the fixture settles all accepted work after the final cycle"],
        ["the final installed identity equals the final authenticated fixture identity", "the number of unresolved owned network operations equals 0", "each successful manual recovery has exactly 1 closure transition", "the final mounted listener and timer counts equal the recorded mounted baseline"],
        basis="proposed-security" if mode=="logout then login" else "observed", source=TIMEOUT if mode=="mount then unmount" else HOME, lines="24-205",
        limits="Finite resource observation; fixture cycle counts are not approved performance limits. Transport cleanup policies remain separate.")
add("RN-L011", "Four-hour requested target crosses initial refresh expiry", "loop", "UC-R14",
    ["User A has accepted activity before every access deadline", "the initial refresh expires within four controlled hours", "renewal responses remain successful"],
    ["the fixture advances through four controlled hours of continued activity"],
    ["the fresh SSO prompt count caused solely by an earlier elapsed-time maximum equals 0", "the protected validation at the end returns result true"],
    ["AC-4"],"target",lines="110-205",limits="Controlled four-hour fixture. This cannot prove indefinite execution or production timing.")

for i,(condition,action,assertion) in enumerate([
    ("the browser enters back-forward cache with a pending renewal", "the browser restores WA from back-forward cache", "the trace records restored session owner before the first protected request"),
    ("the browser reloads during a pending manual renewal", "the browser loads the shell from persisted state", "the first protected request records the restored credential owner and service validation result"),
    ("the renderer crashes with renewal pending", "the browser restores the session after renderer restart", "the trace records 0 deliveries from the terminated renderer"),
    ("the device sleeps before the acquisition deadline", "the device resumes after access expiry", "the trace records actual elapsed time and timeout state before any protected mutation"),
    ("the device loses network during renewal", "the network returns while refresh remains usable", "the next explicit renewal attempt records its request, returned access, and protected validation"),
    ("the device changes VPN during renewal", "the browser retries an explicit renewal on the new network", "the trace records service origin and accepted identity for the retry"),
    ("the browser is offline past refresh expiry", "the browser reconnects to the service", "the protected service accepts 0 expired credentials"),
    ("the browser disables persistent storage", "the browser attempts renewal with storage writes blocked", "the trace records each storage exception and whether access is installed"),
    ("the local storage quota is exhausted", "the browser receives successful renewed access", "the trace records the installed in-memory state and storage error separately"),
    ("the tab is duplicated during manual renewal", "the duplicate tab requests a protected resource", "each request records its own tab owner and service authorization result"),
    ("the user has a normal and private browser window with distinct fixture sessions", "both windows renew their isolated sessions", "a credential write in the normal context changes exactly 0 credential hashes in the private context"),
    ("the user has two independent devices", "device A logs out while device B renews", "the trace records the service revocation scope separately for each device"),
],1):
    add(f"RN-H{i:03}", condition, "lifecycle", "UC-R15", ["User A uses a synthetic account and isolated target",condition],[action],[assertion],
        basis="proposed-security" if i==7 else "policy-open",lines="110-205",
        limits="Record observations. Cross-device logout, storage recovery, and lifecycle recovery policies require owner review.")

for i, failure in enumerate(["HTTP 401", "HTTP 403", "HTTP 429 with Retry-After", "HTTP 500", "HTTP 503", "connection reset", "DNS failure", "TLS validation failure", "client timeout", "explicit request cancellation"],1):
    add(f"RN-F{i:03}", f"Manual renewal rejects after {failure}", "failure", "UC-R16",
        ["User A sees the timeout dialog with refresh usable beyond the test interval", f"the isolated service rejects relogin with {failure}"],
        ["User A clicks the button labeled Extend inside the timeout dialog", "the fixture delivers the rejection"],
        ["the successful dialog closure count equals 0", "the next explicit retry remains available while refresh remains usable"],
        ["AC-7"], "target", source=TIMEOUT, lines="149-177",
        limits="No automatic retry budget or delay is invented. Retry-After conformance requires a reviewed service contract.")
add("RN-F011", "Renewal never settles", "failure", "UC-R16",
    ["User A has a pending manual renewal", "the service fixture never settles that request"],
    ["the controlled clock advances through the original recovery deadline"],
    ["the successful dialog closure count equals 0", "the trace records pending state and logout availability at the deadline"],
    ["AC-5"],"target",source=TIMEOUT,lines="90-177",limits="A maximum request duration and pending-state recovery policy remain undefined.")
add("RN-F012", "Malformed success releases its loader without proving renewal", "failure", "UC-R16",
    ["User A has a pending manual renewal as the only loading request", "the service returns HTTP 200 without usable access"],
    ["the fixture delivers the response through the real interceptor"],
    ["the successful dialog closure count equals 0", "the installed usable-access count from that response equals 0", "the shared loader is not visible after the request settles"],
    ["AC-5","AC-7"],"observed",source=RESPONSE,lines="37-89")

OUT.mkdir(parents=True, exist_ok=True)
for case in CASES:
    if case['sources'][0]['path']==TIMEOUT:
        bounds=[int(x) for x in case['sources'][0]['lines'].split('-')]
        case['sources'][0]['lines']=f"{bounds[0]}-{min(bounds[-1],169)}"
(OUT/"core-cases.json").write_text(json.dumps(CASES,indent=2)+"\n")
print(json.dumps({"cases":len(CASES),"families":sorted({c['family'] for c in CASES})}))
