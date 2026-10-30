"""Plain-English copy for the 104 individual non-combination cases."""
from pathlib import Path
from collections import Counter
import datetime,hashlib,json,re
HERE=Path(__file__).resolve().parent
TASK=HERE.parent.parent
SOURCE=TASK/'evidence/report-impact-priority-20261029/case-priority-audit.json'
REASONS=TASK/'evidence/report-clarity-20261029/execution-reason-audit.json'
source=json.loads(SOURCE.read_text()); old={r['id']:r for r in source['rows'] if not r['id'].startswith('RN-C')}
rows={}

def owner(r):
 text=r['owner'].removeprefix('unknown ').removesuffix(' owners').removesuffix(' owner')
 return text.capitalize()+' owner not yet assigned.'
def add(i,title,happened,reason,impact,missing,action,limits=None):
 r=old[i]
 priority_reason={
  'P1':'The test proves that logout leaves a valid way back into the session. This is a security release blocker.',
  'P4':'The test did not show an interrupted session or an unusable app. Keep this as a backlog item.',
  'P3':'The test does not prove that users experience a problem. Keep this as planned follow-up.',
 }[r['new_priority']]
 rows[i]={'id':i,'title':title,'what_happened':happened,'reason':reason,'user_impact':impact,
          'missing_check':missing,'priority_reason':priority_reason,'next_action':action,
          'limits':limits or 'The checks used controlled test conditions. They do not establish behavior in production.',
          'owner':owner(r)}

# The failed activity checks share causes, but retain their individual user actions.
activity={
 'RN-A001':('Moving the mouse continuously did not start session renewal','The test moved the mouse repeatedly for 15 seconds. No renewal succeeded.','Every mouse movement restarts a five-second waiting period. Continuous movement prevents renewal from starting.'),
 'RN-A002':('Typing continuously did not start session renewal','The test typed repeatedly for 15 seconds. No renewal succeeded.','The portal does not start activity-based renewal when the user types.'),
 'RN-A003':('Scrolling continuously did not start session renewal','The test scrolled repeatedly for 15 seconds. No renewal succeeded.','The portal does not start activity-based renewal when the user scrolls.'),
 'RN-A004':('Mixed mouse, keyboard, and scroll activity did not start session renewal','The test alternated mouse movement, typing, and scrolling for 15 seconds. No renewal succeeded.','Mouse movement repeatedly resets the waiting period. Keyboard and scroll actions do not start their own renewal.'),
 'RN-A005':('Keyboard-only navigation did not start session renewal','The test navigated with the keyboard for 15 seconds. No renewal succeeded.','Keyboard navigation does not start activity-based renewal.'),
 'RN-A006':('Scrolling inside an embedded application did not start session renewal','The test scrolled inside an embedded application pane for 15 seconds. No renewal succeeded.','Scrolling inside the pane does not start activity-based renewal.'),
 'RN-A013':('Holding a key did not start session renewal','The test held a key during the 15-second interval. No renewal succeeded.','Repeated keyboard input does not start activity-based renewal.'),
 'RN-W029':('Mouse movement in an open workspace did not start session renewal','The test moved the mouse inside the open workspace for 15 seconds. No renewal request started.','Continuous movement keeps restarting the five-second waiting period.'),
 'RN-W030':('Typing in an embedded module did not start session renewal','The test typed inside an embedded module for 15 seconds. No renewal request started.','Typing in the module does not start activity-based renewal.'),
 'RN-W031':('Scrolling in a workspace grid did not start session renewal','The test scrolled inside the workspace grid for 15 seconds. No renewal request started.','Scrolling in the grid does not start activity-based renewal.'),
}
for i,(title,happened,reason) in activity.items():
 add(i,title,happened,reason,
     'The tested activity did not start session renewal. Later sign-out, work interruption, and lost work were not observed.',
     'A successful renewal during the stated 15-second activity interval.',
     'Keep the activity gap in the backlog. Raise its priority if a supported user journey demonstrates session interruption.')
add('RN-Q009','The loading indicator disappeared before another request finished',
 'One request failed while another request was still waiting. The loading indicator disappeared.',
 'The error did not identify its request. The shared error handler cleared loading status for every request.',
 'Users could think loading has finished too soon. The test did not show blocked work, repeated transactions, or data loss.',
 'Loading must remain visible until the other request finishes.',
 'Track this visual defect in the backlog. Preserve each request\'s loading status when handling this error.')
add('RN-S002','Logout reported success but did not stop the session from being renewed',
 'Access had expired when logout reported success. Reusing the same valid refresh credential then issued new access.',
 'The server recorded no instruction to reject further use of that session\'s refresh credential.',
 'Someone already holding that valid refresh credential could regain access after apparent logout. Production access and credential theft were not demonstrated.',
 'The same refresh credential must be rejected after logout.',
 'Correct the logout behavior or prove the affected path is absent from this release. Retest rejection after logout.',
 'The actual server controller and signature checks ran. Supporting storage and request services were test substitutes. Production was not tested.')
add('RN-S023','The server accepted conflicting refresh credentials in one request',
 'The test sent two different refresh credentials. The server used the first and issued access for that user.',
 'The server accepted the first value instead of rejecting the ambiguous request, as the proposed test expected.',
 'The test did not show access to another user\'s account. The required rejection rule and production request handling remain unconfirmed.',
 'The agreed duplicate-header rule and the deployed gateway\'s handling of multiple values.',
 'Agree the rule for conflicting values. Test it through the real gateway before escalating this issue.')
add('RN-S035','An external request included the portal access credential',
 'The shared request code added the portal access credential to a request addressed to an external test destination.',
 'The request code added the credential without restricting it to a trusted portal destination.',
 'A supported external request could disclose access credentials. The test intercepted the request, so no external server received them.',
 'Whether a supported application sends such requests, and whether its destination can actually receive the credential.',
 'Check supported external destinations and outgoing requests. Raise priority if a real external receiver can obtain the credential.')
add('RN-S037','A configured request header skipped the sign-in check',
 'The test supplied a configured bypass header without a login credential. The test-only protected handler still ran.',
 'The server authentication filter treats this configured header as permission to skip credential validation.',
 'An untrusted caller could bypass authentication if the real route accepts that header. Actual protected business data was not accessed.',
 'Whether the public gateway removes forged bypass headers and whether a real protected route is reachable.',
 'Test a forged header through the actual gateway and protected service. Escalate if an unauthenticated caller gains access.')

# Partially completed cases: say what passed and exactly what remains unknown.
add('RN-A009','Background connection checks were not fully tested as user activity',
 'The session expired without user input. The test did not run a real background connection heartbeat.',
 'The required live connection was unavailable. The no-input result does not answer whether connection heartbeats count as activity.',
 'Whether background connection checks affect session renewal remains unknown. No heartbeat-related user failure was demonstrated.',
 'A live connection that sends regular keep-alive messages, with its session-renewal behavior observed.',
 'Run the real connection without user input. Check session expiry and renewal against the agreed activity rule.')
add('RN-B013','Recovery after actual browser suspension remains unverified',
 'The test simulated the browser resuming after access expired. The recovery check ran.',
 'The test did not actually suspend the browser or device.',
 'The result does not show whether a real suspension interrupts recovery. No suspension-related user failure was demonstrated.',
 'Actual browser suspension followed by recovery and a protected-service access check.',
 'Repeat the test with real suspension. Check the visible recovery options and server access after resuming.')
add('RN-D009','The server result after closing the renewal tab is unknown',
 'The test closed the browser tab that owned the renewal request. The browser-side observation completed.',
 'No matching server record showed whether that request completed after the tab closed.',
 'The test does not establish the server outcome after closing the tab. No resulting user failure was demonstrated.',
 'The actual server request outcome after the renewal tab closes.',
 'Repeat the sequence while recording the matching server request and its final result.')
add('RN-H011','Renewal across normal and private windows remains partly tested',
 'Two isolated browser sessions kept their stored information separate.',
 'The test did not complete renewal in an actual normal window and an actual private window.',
 'Storage separation passed. Complete renewal and access in both window types remain unverified.',
 'Renewal and protected-service access in normal and private browser windows.',
 'Run the complete session-renewal sequence in both actual window types.')
listener={
 'RN-L004':('Cleanup after 1,000 successful recoveries is not confirmed','All 1,000 recovery cycles completed. The number of browser event handlers changed from 329 to 327.'),
 'RN-L005':('Cleanup after two failed-then-successful renewals is not confirmed','Both recovery cycles completed. The number of browser event handlers changed from 329 to 337.'),
 'RN-L006':('Cleanup after ten failed-then-successful renewals is not confirmed','All ten recovery cycles completed. The number of browser event handlers changed from 329 to 337.'),
 'RN-L010':('Cleanup after 100 workspace switches is not confirmed','The workspace switches completed. The number of browser event handlers changed from 344 to 336.'),
}
for i,(title,happened) in listener.items():
 add(i,title,happened,
     'The before-and-after screens differed because assets, notifications, or popovers changed. Their event-handler counts cannot be compared fairly.',
     'The count difference does not prove a memory leak or repeated actions. No interrupted session or unusable screen was demonstrated.',
     'A comparison of the same screen state, event handlers, and timers before and after the cycles.',
     'Repeat the cleanup check with matching screen states after notifications and loading have settled.')
add('RN-L011','Four simulated hours passed, but real sign-in and service access remain unverified',
 'The browser continued for four simulated hours. No local sign-in screen appeared, and the test service accepted the renewed credential.',
 'The run used a substitute sign-in service. It did not observe real sign-in prompts or validate access through the real service.',
 'Local continuation passed. Whether users can continue for four hours with the real sign-in provider remains unknown.',
 'Real sign-in prompt behavior and protected-service access throughout the same interval.',
 'Repeat the interval with the actual sign-in provider and a protected service that validates the renewed credential.',
 'The clock was accelerated. Four simulated hours do not establish four hours of production use.')
signed={
 'RN-P014':('Renewal with a lowercase response header needs a real service check','The browser accepted and installed the renewed test credential from a lowercase response header.'),
 'RN-P015':('Renewal with a mixed-case response header needs a real service check','The browser accepted and installed the renewed test credential from a mixed-case response header.'),
 'RN-P016':('Renewal without a replacement refresh credential needs a real service check','The browser installed renewed access even though the successful response supplied no replacement refresh credential.'),
 'RN-P017':('Renewal with a future issue time needs a real service check','The browser installed a test credential whose issue time was in the future.'),
}
for i,(title,happened) in signed.items():
 add(i,title,happened,
     'Only a substitute service accepted the installed credential. The real service did not validate its signature or user identity.',
     'Browser installation passed. The test does not establish whether the user can access the real protected service afterward.',
     'The real service must accept the stated response format and confirm the correct user.',
     'Use valid signed credentials and the current protected service for this exact response format.')
add('RN-Q019','The browser submitted once, but the saved financial transaction count is unknown',
 'The browser submitted the financial request once while renewal was pending.',
 'The test had no real financial service or transaction record to confirm how many writes the server saved.',
 'No duplicate browser submission was observed. Duplicate saved financial transactions were neither demonstrated nor ruled out.',
 'The real server\'s saved transaction count for this operation.',
 'Run the same operation against the real test service. Match its transaction records to the browser request.')
add('RN-S044','A test access credential appeared in the console; exported logs remain unchecked',
 'A failed credential-acquisition request produced a console message containing a test access credential.',
 'The test had no application log exporter or agreed rule for removing credentials from exported logs.',
 'A console exposure was observed. Exported disclosure and access by unauthorized readers were not demonstrated.',
 'The actual exported log content, its readers, and the required removal of credentials.',
 'Identify the exported logs and their readers. Verify that credentials are removed before raising the priority.')
add('RN-S045','Credential safety during reconnects and external navigation remains partly checked',
 'The test observed the portal\'s renewal URLs. It did not test a real authenticated reconnect or receiving website.',
 'The required reconnecting application and receiving website were unavailable.',
 'The test does not establish whether reconnects or external navigation disclose credentials through URLs or browser history.',
 'Actual reconnect URLs, browser history, and information received by another website.',
 'Run the real reconnect and navigation paths. Check both the browser and receiving server for credentials.')
add('RN-W016','Unsaved test form data survived renewal; real record handling remains unchecked',
 'Unsaved entries remained in the test form after renewal.',
 'No real business application or matching server record was available to verify the complete editing workflow.',
 'The test form retained its entries. Preservation of actual business records and unsaved work remains unverified.',
 'The real application\'s unsaved entries and matching server record before and after renewal.',
 'Repeat renewal while editing a real test record. Compare unsaved entries and the stored record afterward.')
add('RN-W032','Background updates to an inactive workspace need a live connection check',
 'The test delivered substitute update callbacks to the inactive workspace.',
 'No real notification connection or application update receiver was available.',
 'The test does not establish whether real background updates affect renewal or the inactive workspace correctly.',
 'Actual incoming updates and their effect on workspace data and session activity.',
 'Load the real update connection and application receiver. Observe incoming updates without user input.')

# Blocked cases. Each description names the missing condition instead of implying a product failure.
# Fields: ID | plain title | why unavailable | what remains to check | user-facing uncertainty | next step
blocked='''
RN-A011|Touch-screen activity could not be tested|No real touch device was available. Simulated touch input would not show actual browser behavior.|Native tapping and swiping, with session-renewal requests observed.|Whether touch activity keeps the session active remains unknown.|Run the case on a real touch device and observe renewal during tapping and swiping.
RN-A012|Typing through an input method could not be tested|No real input-method editor was available for entering composed characters.|Actual composed-text entry and the resulting session activity.|Whether composed-text input keeps the session active remains unknown.|Use a real input-method editor and observe renewal while entering text.
RN-D004|Account separation between browser profiles could not be fully tested|The test lacked a second user's permissions and a service that records denied trade requests.|Separate profiles with different users, permissions, and protected trade results.|The test does not establish whether one profile can access another user's protected trades.|Run separate real profiles with distinct test users and inspect the service's access decisions.
RN-D006|Duplicating a browser tab could not be tested|The test tool could open a new tab but could not use the browser's actual Duplicate Tab action.|The copied session information and first protected request after duplicating a tab.|A new tab does not establish whether a duplicated tab restores the correct session.|Use the browser's Duplicate Tab action and check the copied session and server access.
RN-D007|Back navigation after logout could not be tested|Browser-history restoration and the server's rejection of logged-out credentials were not available together.|Back navigation after logout, including restored pages and protected requests.|Whether a restored page can still access protected data after logout remains unknown.|Restore the page through browser history and check that the real server rejects ended-session credentials.
RN-D008|Returning to a tab after another tab changes accounts could not be tested|The test lacked a second user's permissions and records of server access decisions.|The returning tab's visible identity and its permission to access protected trades.|Whether the old tab uses the correct account and permissions remains unknown.|Switch accounts in one tab, return to the other, and check the real service's access decisions.
RN-D010|Session behavior across separate browser windows could not be tested|Two actual browser windows were not configured. Two test tabs would not meet this case's conditions.|Session information and access across separate browser windows.|Whether separate windows interfere with each other's session information remains unknown.|Run the case in separate browser windows and inspect each window's account and protected requests.
RN-D011|An embedded application from another website could not be tested|No supported embedded application from another website was configured.|User input, session expiry, and recovery in the real embedded application.|Session continuity while using that embedded application remains unknown.|Load the supported embedded application and repeat input, expiry, and renewal checks.
RN-D012|An embedded application's session identity could not be tested|No supported embedded application and delayed-response test were available.|Whether embedded application responses stay associated with the correct signed-in user.|The test does not establish that embedded responses cannot mix users' session information.|Load the real embedded application and check delayed responses during a session change.
RN-D013|Restarting the browser after credentials expire could not be tested|The test could not restart a persistent browser profile after both credentials expired.|Restored browser state and server access after restarting with expired credentials.|Whether the restarted browser restores an expired session safely remains unknown.|Restart an actual saved browser profile and check the sign-in screen and server rejection of expired credentials.
RN-D014|Two portal instances in one page could not be tested|The available application starts one portal. No supported page with two independently signed-in portals was available.|Session separation between two supported portal instances in one page.|The test does not establish whether two portal instances can interfere with each other's session.|Provide the supported two-portal page and verify each portal's identity and requests.
RN-F008|Renewal after a secure-connection certificate failure could not be tested|No test server could produce the required secure-connection certificate failure.|Renewal failure, recovery options, and protection against sending credentials over an insecure connection.|The app's response to this secure-connection failure remains unknown.|Provide a controlled server with the required certificate failure and observe renewal and recovery.
RN-H001|Restoring a cached page during renewal could not be tested|The setup could not verify that the browser cached and restored the page during a pending renewal.|Actual browser page caching and restoration while renewal is pending.|Whether a restored cached page handles the pending renewal correctly remains unknown.|Use a browser setup that confirms page caching and restoration, then repeat the pending-renewal sequence.
RN-H002|The server result after reloading during renewal remains unverified|The page reloaded, but the real protected service did not validate the first request afterward.|The first protected request after reload and the user accepted by the server.|The page action alone does not establish that access after reload belongs to the correct user.|Repeat reload while recording the first protected request and the real server's accepted user.
RN-H003|Recovery from a browser-page crash during renewal could not be tested|No controlled page-crash and recovery setup was available.|The pending renewal, crash recovery, and first request after restoration.|Whether the page can recover its session safely after this crash remains unknown.|Use a controlled browser-page crash and observe the restored session and first protected request.
RN-H004|Device sleep before scheduled credential acquisition could not be tested|The isolated browser test could not put a device to sleep or independently measure elapsed sleep time.|Actual sleep, wake-up timing, and session recovery afterward.|Whether a sleeping device misses renewal and recovers correctly remains unknown.|Run the case on a controlled device with real sleep and an independent elapsed-time record.
RN-H006|Changing VPN connections during renewal could not be tested|No separate test VPN and service route were available. The user's network connection was not changed.|Actual VPN change during renewal and the resulting request and recovery behavior.|Whether a VPN change interrupts renewal or recovery remains unknown.|Use a controlled VPN environment and repeat renewal while changing the VPN connection.
RN-H007|Expired credentials after reconnecting were not checked by the real service|The browser went offline and reconnected, but no current service checked the expired credentials.|The real service must reject expired credentials after reconnection.|Reconnection was observed. Whether the service rejects the expired credentials remains unknown.|Repeat the sequence with the actual protected service and record its response to expired credentials.
RN-H010|Duplicating a tab during renewal could not be tested|The actual Duplicate Tab action and first protected request afterward were not available to the test.|Copied tab information and the server's accepted user during a pending renewal.|Whether duplicating a tab preserves a correct session during renewal remains unknown.|Duplicate the tab through the browser and check its copied session and first protected request.
RN-H012|Session behavior across two devices could not be tested|Two independent devices and a shared server session-ending service were unavailable.|Whether ending a session reaches both devices and stops protected access.|Cross-device session and logout behavior remain unknown.|Run the case on two real test devices and inspect server access after the session ends.
RN-L007|One hundred logout-and-login cycles could not be tested|The setup lacked complete repeated sign-in and a reliable comparison of browser event handlers.|One hundred complete logout-and-login cycles, followed by resource cleanup checks.|Long-run sign-in reliability and cleanup remain unknown.|Provide repeatable sign-in and compare the same browser event handlers before and after all 100 cycles.
RN-L008|One hundred open-and-close component cycles could not be tested|The browser test could not repeatedly create and remove the real component while checking cleanup.|One hundred complete component start-and-stop cycles and matching event-handler counts.|Repeated component cleanup and long-run usability remain unknown.|Run the actual component lifecycle 100 times and compare the same event handlers afterward.
RN-Q020|Progress updates during a long request could not be tested|No real application request produced the required progress updates.|Actual progress updates and whether they affect session activity.|Whether request progress changes renewal behavior remains unknown.|Run a real long request with progress updates and observe session renewal without extra user activity.
RN-S033|Renewal requested from another website could not be tested|No current browser-and-server setup exposed the required cross-website renewal request.|Whether a request without portal credentials is rejected and whether another website can read its response.|The actual cross-website access behavior remains unknown.|Configure the current server's cross-website rules and test requests from the separate website.
RN-S034|Cookie-only renewal from another website could not be tested|No agreed cookie-only renewal rule or valid current-server cookie session was available.|The allowed cookie-based behavior and responses to requests from another website.|Whether cookie-only cross-website renewal is supported or safe remains unknown.|Confirm the cookie-only rule, then test it using the current server and a valid test session.
RN-S036|A connection request from an untrusted website could not be tested|No running protected connection or active website-origin rule was available.|Whether the server rejects connection setup from an untrusted website.|The test does not establish whether untrusted websites can start an authenticated live connection.|Run the protected connection through the real server and test an untrusted website address.
RN-S038|Access rights after restoring a workspace could not be tested|The real workspace application, protected service, and second user's access rights were unavailable.|Restoring the workspace under the current user's actual permissions.|Whether restoration can expose protected data without permission remains unknown.|Restore the real workspace with separate test users and verify the service's permission checks.
RN-S040|Embedding the renewal prompt in an untrusted website could not be tested|The portal's active anti-embedding rules and an authenticated embedding test page were unavailable.|Whether another website can embed the signed-in portal and its renewal prompt.|The test does not establish whether an untrusted page can display the authenticated renewal prompt.|Inspect the portal's actual response rules and test embedding from a separate website.
RN-S042|Old-account workspace data after switching users could not be tested|No real business application, first-user-only record, or second-user permission setup was available.|Whether the second user can see or request data belonging only to the first user.|Protection against exposing old-account business data remains unverified.|Use distinct test users and protected records to check workspace data after an account change.
RN-S043|Logout propagation between tabs could not be tested|No current browser-and-server setup could track logout reaching another tab and ending its server access.|Logout in one tab and rejection of ended-session credentials from another tab.|Whether another tab retains accepted access after logout remains unknown.|Run both tabs against the current service and check the second tab's access after logout.
RN-S046|Shared response caching after renewal could not be tested|No test caching server and agreed cache rules separated requests for two different users.|Whether cached renewal responses remain private to the correct user.|The test does not establish whether a cache can return one user's renewed response to another user.|Test the actual cache rules with distinct users and inspect which response each user receives.
RN-S048|Stopping live messages after the session ends could not be tested|No authenticated message server or agreed deadline for stopping delivery was available.|Message delivery after the server ends access, including the allowed stopping time.|Whether live messages stop when access ends remains unknown.|Agree the stopping deadline and observe real message delivery after the server ends the session.
RN-S049|Credentials used by reconnecting live connections could not be tested|No running application connection exposed its reconnect credentials and subscriptions for observation.|The renewed credential and correct subscriptions when a real connection reconnects.|Whether reconnect uses the current session remains unknown.|Run the actual connection and record its sign-in information and subscriptions after renewal.
RN-S050|A queued reconnect after logout could not be tested|No live reconnect queue and authenticated subscription server were available.|Whether a queued retry reconnects or restores subscriptions after logout.|Whether logout prevents a queued connection retry from restoring access remains unknown.|Queue a retry in the actual application, log out, and check the server connection and subscriptions.
RN-S051|Subscription permission changes during renewal could not be tested|No live subscription server or changing-permission test was available. The continued-access rule also remains undecided.|Whether a user loses access to a message channel after that permission is removed.|The test does not establish whether renewed subscriptions respect removed permissions.|Agree the access rule, remove the test user's permission, and observe messages from the actual server.
RN-S052|Retry limits after repeated access rejection could not be tested|No live reconnect scheduler was available to run the proposed three-attempt experiment.|The number and timing of retries after repeated authentication rejection.|Whether repeated rejection causes excessive retries remains unknown.|Run the proposed three-attempt check using the actual connection and retry scheduler.
RN-S053|A completed financial transaction being retried after renewal could not be tested|No financial service, saved transaction record, or agreed duplicate-request rule was available.|Whether retrying the same operation creates a second saved financial transaction.|One browser request cannot prove that the server saved exactly one transaction.|Use a real test financial operation and compare saved transaction records before and after retry.
RN-S054|Upload permissions after a credential change could not be tested|No real upload service or permission-change test could check access when the upload finishes.|Whether the current user remains authorized when an upload is completed and saved.|The test does not establish whether an upload can finish after access rights change.|Change permissions during a real test upload and inspect the server's decision before saving the object.
RN-S055|Old-user queued messages after switching accounts could not be tested|No real application message queue, second-user screen, or message store was available.|Whether messages queued for the first user can appear after the second user signs in.|Protection against displaying the first user's buffered messages remains unverified.|Queue real test messages, switch accounts, and inspect the second user's screen and message delivery.
RN-T001|The GraphQL connection's renewed credentials could not be tested|The GraphQL live-data connection and its application were not running in the test portal.|Which access credential the real GraphQL connection uses after reconnecting.|Whether the live-data connection uses renewed access remains unknown.|Run the actual application and GraphQL server, then inspect reconnect authentication.
RN-T002|The STOMP messaging connection's renewed credentials could not be tested|The cashflow application's STOMP messaging connection and server were not running in the test portal.|Which stored access credential the messaging connection uses after reconnecting.|Whether the messaging connection uses renewed access remains unknown.|Load the actual cashflow application and messaging server, then inspect reconnect authentication.
RN-T003|An existing live connection after access expiry could not be tested|No running GraphQL live-data connection was available. The rule for enforcing expiry remains undecided.|Whether an established connection must stop, renew, or reconnect when access expires.|Behavior of an already-open connection after expiry remains unknown.|Agree the expiry rule and observe the actual connection when its access credential expires.
RN-T004|Messaging keep-alive traffic during expiry could not be tested|No running STOMP messaging connection was available. Whether its keep-alive messages count as activity remains undecided.|Session expiry and renewal while only connection keep-alive messages are exchanged.|Whether keep-alive traffic affects session expiry remains unknown.|Agree the activity rule and run the real messaging connection without user input.
RN-T005|Incoming live messages during expiry could not be tested|No actual live-data receiver or protected message server was available. The activity rule remains undecided.|Session expiry and renewal while only protected server messages arrive.|Whether incoming messages keep the user's session active remains unknown.|Agree the activity rule and observe incoming messages without user input on the real connection.
RN-T006|Live-data reconnect after logout could not be tested|No real GraphQL connection and server session-ending records were available.|Whether the server rejects a reconnect attempted after logout.|Whether a live-data connection can regain access after logout remains unknown.|Log out while using the actual connection and record the server's response to reconnect.
RN-T007|A delayed messaging retry after logout could not be tested|No running cashflow messaging connection and signed-out application screen were available.|Whether a queued messaging retry runs after logout and whether the server accepts it.|Whether delayed messaging retries can restore signed-out access remains unknown.|Queue a reconnect in the real application, log out, and inspect the screen and server result.
RN-T008|Live connection reconnect after switching accounts could not be tested|No real connection host or second user's access-permission setup was available.|The current account and permissions used when reconnecting after an account change.|Whether reconnect can retain the first user's access remains unknown.|Switch between distinct test users and inspect reconnect authentication and protected messages.
RN-T009|A delayed live-data callback after switching accounts could not be tested|No real trading update receiver or second-user test setup was available.|Whether a callback queued for the first user can update the second user's screen.|Whether delayed updates can cross account boundaries remains unknown.|Queue an actual trading update, switch users, and observe the callback and resulting screen.
RN-T010|Live reconnect while manual renewal is pending could not be tested|No real live connection ran alongside the portal's renewal dialog.|The credentials and recovery behavior when reconnect overlaps a pending manual renewal.|Whether reconnect and manual renewal interfere with each other remains unknown.|Run the actual connection alongside the renewal dialog and observe both overlapping requests.
RN-T011|Separate workspace message subscriptions could not be tested|No real multi-workspace application or authorized message channels were available.|Whether each workspace subscribes only to its permitted message channel.|The test does not establish whether workspace messages stay separated correctly.|Load both workspaces and inspect actual channel permissions, subscriptions, and message delivery.
RN-T012|Two workspace connections using the same address could not be tested|No real multi-workspace application opened the required same-address GraphQL connections.|Whether reconnect keeps each workspace's subscriptions and data separate despite a shared server address.|Connection separation between the workspaces remains unverified.|Run the actual same-address connections and inspect each workspace's subscriptions and delivered data.
RN-T013|Duplicate messaging subscriptions after reconnect could not be tested|The messaging helper code was available, but no real browser application and messaging server were connected.|Whether reconnect creates duplicate subscriptions or repeated message deliveries.|The test does not establish whether users receive duplicate updates after reconnect.|Run the actual messaging connection through reconnect and count subscriptions and delivered updates.
RN-T014|Repeated message handling after reconnect could not be tested|No real reconnecting application or screen-update receiver was available. The repeated-message rule remains undecided.|Whether messages repeated after reconnect should update the screen once or more than once.|Whether reconnect can duplicate visible updates remains unknown.|Agree the repeated-message rule and test actual reconnect messages against the application screen.
RN-T015|Recovery of missed messages after reconnect could not be tested|No actual message-recovery application was available. The rule for recovering missed messages remains undecided.|Whether reconnect restores messages missed during renewal.|Whether users miss business updates during reconnect remains unknown.|Agree the recovery rule and compare actual messages sent, missed, and restored across reconnect.
RN-T016|Malformed messaging data after an account change could not be tested|No actual cashflow messaging receiver or business-update observer was available.|Whether malformed messages can change data under the wrong account.|The test does not establish whether malformed messages affect another user's information.|Send malformed messages through the actual test connection and inspect account-specific screen and data changes.
RN-T017|Access to an unauthorized message channel after renewal could not be tested|No real server checked access to the requested message channel.|Whether the server rejects subscriptions to channels the user cannot access.|Message-channel authorization after renewal remains unverified.|Renew access and request a forbidden channel through the actual server.
RN-T018|Stopping an open connection after server-side logout could not be tested|No running connection could observe the server ending that session's access.|Whether a connection already open stops delivering protected data after server-side logout.|Whether an existing connection retains access after the session ends remains unknown.|End the test session on the real server and observe the existing connection and message delivery.
RN-T019|Credentials in live-connection addresses could not be checked|No real GraphQL or STOMP network connection was available for address inspection.|Connection URLs and browser-visible addresses during authentication and reconnect.|Whether live connections expose access credentials through URLs remains unknown.|Run both real connection types and inspect their URLs and outgoing connection requests.
RN-T020|Connection authentication failure during renewal could not be tested|No real connection-error handler ran alongside the session-renewal request.|Whether the application distinguishes failed connection authentication from successful session renewal.|Whether the app reports connection failure correctly during renewal remains unknown.|Run the real connection and renewal together, then observe an authentication failure and the visible result.
RN-T023|Server-sent event authentication could not be tested|No actual protected server-sent event connection was identified. Its authentication rule also remains undocumented.|Whether the application uses this connection type and how it handles renewal and expiry.|No user failure is established because this protected connection has not been identified in the release scope.|Identify an actual connection before testing it. Record its required authentication behavior if one exists.
RN-T024|Resuming server-sent events under another account could not be tested|No protected event server and two-user access test were available.|Whether an event-resume marker from one account can retrieve another account's protected messages.|Protection against cross-account event replay remains unverified.|Use two test users and verify the actual server's access checks when resuming events.
RN-T026|One saved upload across renewal could not be tested|No inspected upload service or saved-upload record was available.|Whether renewal or retry saves the same upload more than once.|The test does not establish whether users can create duplicate saved uploads.|Use a real test upload and compare the server's saved objects across renewal and retry.
RN-T027|Canceling an upload when logging out could not be tested|No actual upload-resume service, temporary upload storage, or logout-aware server was available.|Whether logout stops the upload and prevents an incomplete upload from later being saved.|Whether an upload can continue or finish after logout remains unknown.|Log out during a real test upload and inspect transfer, temporary data, and final save behavior.
RN-T028|Background processing after logout could not be tested|No supported background worker and real server access checks were configured.|Whether background processing can continue protected work after the session ends.|Whether background work retains unauthorized access after logout remains unknown.|Identify the actual background worker and test its server access after logout.
RN-T029|Cached protected data after switching accounts could not be tested|No supported browser background cache for protected responses was identified in this portal setup.|Whether cached responses from the first account can be returned after switching users.|Protection against old-account data appearing from the browser cache remains unverified.|Identify the actual protected-data cache, then inspect responses after switching between distinct users.
RN-T030|A secure-connection interruption during renewal could not be tested|The local setup used unencrypted test traffic. It could not produce the required secure-connection interruption.|The connection error, session response, and prevention of insecure credential fallback.|The app's response to secure-connection failure remains unknown.|Use a controlled encrypted connection and interrupt it while observing renewal and recovery.
RN-W013|Removing access to an inactive workspace could not be tested|No real permission service could remove access while the workspace was inactive.|Whether the inactive workspace stops exposing protected information after access is removed.|Behavior after workspace permission removal remains unverified.|Remove permission through the actual test service and inspect the inactive workspace when it becomes visible.
RN-W014|Account switching with existing workspace data could not be tested|The available sign-in server supported one test identity. A second user's permissions and service records were unavailable.|Whether old-account workspace data remains visible or accessible after switching accounts.|The test does not establish whether workspace data stays private between accounts.|Use distinct test users and inspect both the visible workspace and protected service requests after switching.
RN-W019|Delayed application-list validation before Home opens could not be tested|The test delivered the application list all at once during login. It could not delay the permission-validation step.|Whether Home waits correctly while the real application list and permissions are being validated.|Home readiness during slow validation remains unknown.|Run the actual application-list validation with a controlled delay and observe Home's loading and available actions.
RN-W025|Restoring a workspace after a browser crash could not be tested|No actual browser-crash recovery setup included the real application's unsaved work.|The restored workspace, unsaved entries, and server session after restarting the browser.|Whether a crash loses work or restores an unusable session remains unknown.|Crash a controlled test browser while editing a real test record, then inspect the restored workspace.
RN-W028|An OpenFin launch request during renewal could not be tested|The OpenFin desktop connection was not running. Whether launch requests should wait during renewal also remains undecided.|The real desktop launch request, its timing, and the agreed handling during renewal.|Whether a desktop launch is lost, delayed, or handled correctly during renewal remains unknown.|Agree the launch rule and run the actual OpenFin desktop connection during renewal.
'''
for line in blocked.strip().splitlines():
 i,title,reason,missing,impact,action=line.split('|')
 happened={
  'RN-H002':'The browser reloaded while renewal was pending. The required server access check afterward did not run.',
  'RN-H007':'The browser stayed offline past expiry and then reconnected. The required server rejection check did not run.',
 }.get(i,'The required complete check could not run in the available test setup.')
 add(i,title,happened,reason,impact,missing,action,
     'The missing test setup does not prove an application failure. Actual user impact remains unverified.')

assert set(rows)==set(old),(set(old)-set(rows),set(rows)-set(old))
assert len(rows)==104
# Check sentence lengths as an editorial aid. IDs and proper names do not establish dictionary compliance.
long=[]
for r in rows.values():
 for field,text in r.items():
  if field=='id':continue
  for sentence in re.split(r'(?<=[.!?])\s+',text):
   words=sentence.split()
   if len(words)>20:long.append({'id':r['id'],'field':field,'words':len(words),'sentence':sentence})
output={'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'Plain-language display copy for 104 non-combination cases. Source outcomes and priorities remain unchanged.',
 'source_audit_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
 'rows':[rows[r['id']] for r in source['rows'] if r['id'] in rows],
 'checks':{'rows':len(rows),'exact_source_ids':True,'long_sentences':long},
 'writing_review':{'standard':'ASD-STE100','automated_check':'PASSED' if not long else 'FAILED','asd_review':'PENDING','reviewer':None,'reviewed_at':None,
 'limitations':['Automated checks do not check the complete approved dictionary or grammar rules.']}}
(HERE/'case-copy.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'rows':len(rows),'long_sentences':long},indent=2))
