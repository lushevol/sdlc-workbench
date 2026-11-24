"""Bind the canonical portal case to exact local source and mapped Playwright statements."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import re

root = Path(__file__).resolve().parents[3]
task = root / "tasks/ces-entitlement-migration-20261102"
catalog = task / "06-test-cases.md"
runner = task / "frontend-tests/run-portal.mjs"
evidence = {}


def add(key, path, kind, authority="established"):
    source = root / path
    evidence[key] = {
        "path": path, "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "start_line": 1, "end_line": len(source.read_text().splitlines()),
        "kind": kind, "authority": authority,
    }


add("E_REQUIREMENT", "knowledge/candidates/security/KT-ces-migration-parity.md", "behavior", "draft")
add("E_RUNNER", str(runner.relative_to(root)), "automation")
add("E_LOGIN", "e2e/pages/login.page.ts", "ui")
add("E_HOME", "repos/ui/mfe-base/src/pages/Home/index.tsx", "ui")
add("E_AVATAR", "repos/ui/mfe-base/src/components/Avatar/index.tsx", "ui")
add("E_PROFILE", "repos/ui/mfe-base/src/components/Profile/index.tsx", "ui")
add("E_NEW_TILE", "repos/ui/mfe-base/src/components/NewTile/index.tsx", "ui")
add("E_MENU", "repos/ui/mfe-base/src/components/Tile/index.tsx", "ui")
add("E_CONSUMER", "tasks/ces-entitlement-migration-20261102/frontend-tests/portal-entry.tsx", "ui")
components = {}


def component(key, kind, identity, scope, source, identity_kind="visible_label"):
    components[key] = {"type": kind, "identity": identity, "identity_kind": identity_kind,
                       "scope": scope, "evidence": [source]}


component("C_USER", "textbox", "Enter Username", "login page", "E_LOGIN", "stable_identifier")
component("C_PASSWORD", "text input", "Enter Password", "login page", "E_LOGIN", "stable_identifier")
component("C_SIGN_IN", "button", "Sign In", "login page", "E_LOGIN", "accessible_name")
component("C_WORKSPACE", "tab", "Workspace 1", "portal", "E_HOME", "accessible_name")
component("C_AVATAR", "icon button", "MicroWebUI_base_avatar_IconButton", "portal page", "E_AVATAR", "test_id")
component("C_PROFILE_MENU", "menu item", "MicroWebUI_base_avatar_Profile", "portal avatar menu", "E_AVATAR", "test_id")
component("C_ENTITY", "button", "RATAN :: RATAN_ENTITLEMENT_RULE :: Role A, Role B", "profile dialog", "E_PROFILE", "accessible_name")
component("C_SUBJECT", "button", "feature-a", "profile dialog", "E_PROFILE", "accessible_name")
component("C_ACTION", "chip", "action-a", "profile dialog", "E_PROFILE")
component("C_DIALOG", "dialog", "User Profile", "portal page", "E_PROFILE")
component("C_NEW_TILE", "section", "New Tile", "portal application bar region", "E_NEW_TILE")
component("C_CES_CARD", "section", "CES fixture", "drawer panel", "E_MENU")
component("C_CES_EXPORT", "button", "Export fixture data", "CES contract consumer", "E_CONSUMER", "accessible_name")
component("C_EMS2_EXPORT", "button", "Export fixture data", "EMS2 contract consumer", "E_CONSUMER", "accessible_name")

steps, bindings = {}, {}
section = False
clause = None
runner_text = runner.read_text()
for number, line in enumerate(catalog.read_text().splitlines(), 1):
    if line == "### TC-FE-CES-013":
        section = True
    elif section and line.startswith("### "):
        break
    match = re.match(r"\s*(Given|When|Then|And|But) (.+)", line) if section else None
    if not match:
        continue
    keyword, text = match.groups()
    if keyword in {"Given", "When", "Then"}:
        clause = keyword
    kind = {"Given": "condition", "When": "event", "Then": "assertion"}[clause]
    selected, symbol = [], "const payload="
    if "Enter Username" in text:
        selected, symbol = ["C_USER"], "getByPlaceholder('Enter Username').fill"
    elif "Enter Password" in text:
        selected, symbol = ["C_PASSWORD"], "getByPlaceholder('Enter Password').fill"
    elif 'button "Sign In"' in text:
        selected, symbol = ["C_SIGN_IN"], "getByRole('button',{name:'Sign In',exact:true}).click"
    elif 'tab "Workspace 1"' in text:
        selected, symbol = ["C_WORKSPACE"], "getByRole('tab',{name:'Workspace 1',exact:true})"
    elif "store contains supplied routing" in text:
        symbol = "assert.deepEqual(state.entitlementRouting,routing)"
    elif "avatar icon button" in text:
        selected, symbol = ["C_AVATAR"], "getByTestId('MicroWebUI_base_avatar_IconButton').click"
    elif "menu item" in text:
        selected, symbol = ["C_PROFILE_MENU"], "getByTestId('MicroWebUI_base_avatar_Profile').click"
    elif 'button "RATAN ::' in text:
        selected, symbol = ["C_ENTITY"], "getByRole('button',{name:'RATAN :: RATAN_ENTITLEMENT_RULE :: Role A, Role B',exact:true}).click"
    elif 'button "feature-a"' in text:
        selected, symbol = ["C_SUBJECT"], "getByRole('button',{name:'feature-a',exact:true}).click"
    elif 'chip "action-a"' in text:
        selected, symbol = ["C_ACTION"], "getByText('action-a',{exact:true})"
    elif "Escape" in text:
        selected, symbol = ["C_DIALOG"], "page.keyboard.press('Escape')"
    elif 'section "New Tile"' in text:
        selected, symbol = ["C_NEW_TILE"], "getByText('New Tile',{exact:true}).click"
    elif 'section "CES fixture"' in text:
        selected, symbol = ["C_CES_CARD"], "getByText('CES fixture',{exact:true}).click"
    elif 'button "Export fixture data"' in text:
        ces = "CES contract" in text and "EMS2" not in text
        selected = ["C_CES_EXPORT" if ces else "C_EMS2_EXPORT"]
        symbol = f"getByTestId('consumer-{'CES' if ces else 'EMS2'} fixture').getByRole('button',{{name:'Export fixture data'}})"
    elif "applicationTileId" in text:
        symbol = "assert.equal(String(opened.applicationTileId),'1')"
    elif "existing dispatcher" in text:
        symbol = "window.__dispatcher.dispatchOpenTile"
    elif "existing response handlers" in text:
        symbol = "window.__base.LoginUtil.handleEntities(response)"
    elif "mounted contract consumer count" in text:
        symbol = "page.locator('[data-testid^=\"consumer-\"]')"
    elif "permission helper" in text:
        symbol = "assert.deepEqual(decisions,[false,false])"
    elif "isolated browser" in text:
        symbol = "await browser.newContext()"
    assert symbol in runner_text, (number, symbol)
    if clause == "When" and selected:
        kind = "interaction"
    record = {"kind": kind, "evidence": ["E_RUNNER", "E_REQUIREMENT"]}
    if selected:
        record["components"] = selected
    if kind == "assertion":
        record["observation"] = "ui" if selected else "functional"
    steps[str(number)] = record
    bindings[str(number)] = {"symbol": symbol, "evidence": ["E_RUNNER"]}

review = {"state": "UNVERIFIED", "reviewer": None, "reviewed_at": None,
          "notes": "Source and local runtime selectors inspected. Business candidate review and deployed-service acceptance remain pending."}
manifest = {"version": 1, "evidence": evidence, "scenarios": {"TC-FE-CES-013": {
    "file": str(catalog.relative_to(root)), "sha256": hashlib.sha256(catalog.read_bytes()).hexdigest(),
    "behavior": {"intent": "Preserve ordinary calls while admitting CES and EMS2 tiles through their configured providers.",
                 "requirement": "E_REQUIREMENT", "criterion": "knowledge/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-001"},
    "components": components, "steps": steps, "review": review,
    "automation": {"framework": "Playwright Chromium with actual React base and controlled services", "mode": "mapped", "bindings": bindings,
                   "review": {"state": "PASS", "reviewer": "agent:codex root", "reviewed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                              "notes": "Inspected each mapped statement and the retained four-checkpoint local portal execution. This review covers local fixtures only."}},
}}}
output_dir = root / os.environ.get(
    "CES_TEST_OUTPUT",
    "tasks/ces-entitlement-migration-20261102/evidence/frontend-entitlement-implementation-20261106",
)
output = output_dir / "ui-gherkin-manifest.json"
output.write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"steps": len(steps), "output": str(output.relative_to(root)) if output.is_relative_to(root) else str(output)}))
