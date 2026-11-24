> **⚠️ ARCHIVED** — This migration is now complete. See [README.md](../../README.md) and [INSTALLATION.md](../INSTALLATION.md) for current state.

# Complete NPM Package Migration for One-Click Install

## Executive Summary

This migration is **complete**. The project is published to SCB artifactory and supports one-click install.

**Current State:**
- ✅ Monorepo architecture with Lerna
- ✅ Binary executable names configured
- ✅ ES Module setup
- ✅ Comprehensive documentation (ONE_CLICK_INSTALL_EXPLAINED.md, NPM_PACKAGE_MIGRATION_PLAN.md)
- ⚠️ Partial: Only ADO package has shebang
- ⚠️ Partial: `bin` fields present but missing `files` and `publishConfig`
- ❌ No command-line argument parsing
- ❌ No install URL generation tooling
- ❌ No one-click install badges in README

---

## Implementation Steps

### Step 1: Implement Command-Line Argument Parsing

**File:** `packages/core/src/config.js`

**Current State (Lines 7-11):**
```javascript
export function getConfig() {
  const configPath = path.resolve(__dirname, '../../../config.json');
  // Only reads from config.json
}
```

**Required Changes:**
- Add command-line argument parsing as first priority (`process.argv.slice(2)`)
- Add environment variable fallback
- Keep config.json as last resort (backwards compatibility)
- Support 6 parameters: ADO URL, PAT, proxy, Confluence URL/user/token
- Add credential masking in logs
- Provide clear error messages with usage instructions

**Reference:** NPM_PACKAGE_MIGRATION_PLAN.md lines 57-107

---

### Step 2: Add Shebangs to Entry Points

**Files Requiring Changes:**

1. **`packages/unified/src/index.js`**
   - Line 1: Add `#!/usr/bin/env node`
   - Status: ❌ Missing

2. **`packages/confluence/src/index.js`**
   - Line 1: Add `#!/usr/bin/env node`
   - Status: ❌ Missing

3. **`packages/ado/src/index.js`**
   - Status: ✅ Already has shebang

**Purpose:** Enable direct execution via `npx` without specifying `node` command

---

### Step 3: Configure Packages for NPM Publishing

**Files to Update:** All 4 package.json files

#### 3.1 `packages/ado/package.json`
**Add:**
```json
"files": [
  "src/**/*",
  "README.md",
  "LICENSE"
],
"publishConfig": {
  "registry": "https://[SCB_REGISTRY_URL]"
}
```

#### 3.2 `packages/unified/package.json`
**Add:**
```json
"files": [
  "src/**/*",
  "README.md",
  "LICENSE"
],
"publishConfig": {
  "registry": "https://[SCB_REGISTRY_URL]"
}
```

#### 3.3 `packages/core/package.json`
**Add:**
```json
"files": [
  "src/**/*",
  "README.md",
  "LICENSE"
],
"publishConfig": {
  "registry": "https://[SCB_REGISTRY_URL]"
}
```

#### 3.4 `packages/confluence/package.json`
**Add:**
```json
"files": [
  "src/**/*",
  "README.md",
  "LICENSE"
],
"publishConfig": {
  "registry": "https://[SCB_REGISTRY_URL]"
}
```

**Purpose:**
- `files` field prevents publishing node_modules, tests, coverage, etc.
- `publishConfig` ensures packages go to SCB private registry, not public npmjs.org

---

### Step 4: Create Install URL Generation Script

**Create:** `scripts/create-install-url.js`

**Requirements:**
1. Define VS Code input prompts (6 inputs):
   - `ado_pat`: "Azure DevOps Personal Access Token" (password: true)
   - `https_proxy`: "HTTPS Proxy URL (optional)"
   - `confluence_pat`: "Confluence API Token (optional)" (password: true)

2. Define server configuration:
   ```json
   {
     "type": "stdio",
     "command": "npx",
     "args": [
       "-y",
       "@sc-ado/mcp-server",
       "${input:ado_pat}",
       "${input:https_proxy}",
       "${input:confluence_pat}"
     ]
   }
   ```

3. Encode configurations using `encodeURIComponent(JSON.stringify(...))`

4. Generate URLs:
   - VS Code Stable: `https://insiders.vscode.dev/redirect/mcp/install?name=...&config=...&inputs=...`
   - VS Code Insiders: Same with `&quality=insiders`

5. Generate markdown badges:
   ```markdown
   [![Install with NPX in VS Code](badge-url)](install-url)
   ```

**Reference:** NPM_PACKAGE_MIGRATION_PLAN.md lines 282-344

---

### Step 5: Update README with One-Click Install

**File:** `README.md`

**Current State (Lines 46-69):**
- Manual setup instructions only
- No install badges
- No encoded VS Code redirect URLs

**Required Changes:**
1. Replace Quick Start section with:
   - Two install badges (stable + insiders) using generated URLs
   - Explanation: "What happens when you click"
   - List of prompts users will see
   - Note about SCB private registry requirement
   - Keep manual setup as fallback (move to separate section)

**Reference:** NPM_PACKAGE_MIGRATION_PLAN.md lines 360-395

---

## Critical Dependencies & Blockers

### 1. SCB NPM Registry URL (BLOCKER)

**Current State:**
- `lerna.json` line 14: Points to `https://registry.npmjs.org/` (public registry)
- No SCB registry URL documented

**Required:**
- Actual SCB private NPM registry URL
- Format: `https://[scb-registry-domain]`
- Needed for:
  - `publishConfig.registry` in all package.json files
  - `lerna.json` publish configuration
  - `.npmrc` configuration (optional but recommended)
  - Install URL generation script

**Action:** Contact SCB DevOps/Infrastructure team to obtain private NPM registry URL

---

### 2. Package Naming Strategy (DECISION REQUIRED)

**Current State:**
- Multiple separate packages: `@sc-node-mcp/ado`, `@sc-node-mcp/unified`, `@sc-node-mcp/confluence`, `@sc-node-mcp/core`

**Migration Plan Proposes:**
- Single unified package: `@sc-ado/mcp-server`

**Decision Needed:**
- **Option A:** Publish all 4 packages separately (current structure)
  - Pro: Users can install only what they need
  - Con: More complex for one-click install (which package to use?)
  
- **Option B:** Create single unified package
  - Pro: Simpler one-click install experience
  - Con: Users install everything even if only need ADO

**Recommendation:** Option B (unified package) for one-click install simplicity, matching Azure DevOps MCP pattern

---

### 3. Publishing Permissions (VERIFICATION REQUIRED)

**Need to Verify:**
- Do accounts 1540326 (Saravanan R) and 2002918 (Shiyamkumar U) have publishing permissions to SCB NPM registry?
- How to authenticate: `npm login --registry=https://[SCB_REGISTRY]`
- Who to contact if permissions missing?

---

### 4. Backwards Compatibility Strategy (DECISION REQUIRED)

**Current Behavior:**
- Code breaks without `config.json` file
- No fallback mechanism

**Migration Plan Suggests:**
- Support all three methods during transition:
  1. Command-line arguments (highest priority)
  2. Environment variables (fallback)
  3. config.json (backwards compatibility)

**Decision Needed:**
- Keep config.json support permanently or deprecate after migration?
- Force immediate migration or provide transition period?

**Recommendation:** Keep all three methods permanently for flexibility (local dev uses config.json, production uses args/env vars)

---

## Testing Plan

### Phase 1: Local Testing (Pre-NPM)

```bash
# Test command-line arguments
node packages/unified/src/index.js \
  "https://dev.azure.com/sc-ado" \
  "test-pat-token" \
  "http://10.239.9.190:443"

# Test environment variables
export AZURE_DEVOPS_ORG_URL="https://dev.azure.com/sc-ado"
export AZURE_DEVOPS_PAT="test-pat-token"
node packages/unified/src/index.js

# Test error handling (missing args)
node packages/unified/src/index.js
# Should show clear error message with usage instructions

# Test npm link (simulate npx)
cd packages/unified
npm link
npx sc-node-mcp "https://dev.azure.com/sc-ado" "test-token"
npm unlink
```

### Phase 2: NPM Package Testing (Post-Publish)

```bash
# Test installation from SCB registry
npx @sc-ado/mcp-server@latest \
  "https://dev.azure.com/sc-ado" \
  "test-token" \
  --registry=https://[SCB_REGISTRY]

# Test with all parameters
npx @sc-ado/mcp-server@latest \
  "https://dev.azure.com/sc-ado" \
  "pat-token" \
  "http://proxy:443" \
  "https://confluence.scb.com" \
  "user@scb.com" \
  "conf-token"

# Verify package contents
npm pack @sc-ado/mcp-server --registry=https://[SCB_REGISTRY]
tar -tzf sc-ado-mcp-server-1.0.0.tgz
# Should NOT contain: node_modules/, tests/, coverage/, config.json
```

### Phase 3: VS Code Integration Testing

1. Update `.vscode/mcp.json` with npx configuration
2. Restart MCP server in VS Code
3. Test tool execution in Copilot Chat:
   - "List my ADO work items"
   - "Show PR #123"
   - "Search for work item with title X"
4. Verify authentication works
5. Test error scenarios (wrong credentials, network issues)

### Phase 4: One-Click Install Testing

1. Generate install URLs using script
2. Test clicking badge:
   - Verify VS Code shows install dialog
   - Verify all 6 input prompts appear
   - Verify server starts after configuration
3. Test in both VS Code Stable and Insiders
4. Verify npx downloads from SCB registry

---

## Implementation Checklist

### Code Changes
- [ ] Update `packages/core/src/config.js` - Implement command-line arg parsing
- [ ] Add shebang to `packages/unified/src/index.js`
- [ ] Add shebang to `packages/confluence/src/index.js`
- [ ] Add `files` field to `packages/ado/package.json`
- [ ] Add `publishConfig` to `packages/ado/package.json`
- [ ] Add `files` field to `packages/unified/package.json`
- [ ] Add `publishConfig` to `packages/unified/package.json`
- [ ] Add `files` field to `packages/core/package.json`
- [ ] Add `publishConfig` to `packages/core/package.json`
- [ ] Add `files` field to `packages/confluence/package.json`
- [ ] Add `publishConfig` to `packages/confluence/package.json`
- [ ] Update `lerna.json` registry URL to SCB registry

### Tooling & Documentation
- [ ] Create `scripts/` directory
- [ ] Create `scripts/create-install-url.js`
- [ ] Run script to generate install URLs
- [ ] Update `README.md` with one-click install badges
- [ ] Update `README.md` Quick Start section
- [ ] Create `.npmrc` file (optional but recommended)

### Testing
- [ ] Test local execution with command-line args
- [ ] Test local execution with environment variables
- [ ] Test local execution with config.json (backwards compatibility)
- [ ] Test error handling (missing args)
- [ ] Test with `npm link` locally
- [ ] Verify `files` field excludes test/coverage/node_modules

### NPM Publishing
- [ ] Obtain SCB NPM registry URL
- [ ] Configure NPM CLI for SCB registry: `npm config set registry https://[SCB_REGISTRY]`
- [ ] Login to SCB NPM registry: `npm login --registry=https://[SCB_REGISTRY]`
- [ ] Verify publishing permissions
- [ ] Dry run: `npm pack --dry-run` in each package
- [ ] Publish to SCB registry: `lerna publish --registry=https://[SCB_REGISTRY]`
- [ ] Verify package published: `npm view @sc-ado/mcp-server --registry=https://[SCB_REGISTRY]`

### Integration Testing
- [ ] Test installation from SCB registry
- [ ] Test VS Code integration with npx config
- [ ] Test one-click install badge in browser
- [ ] Test all 6 input prompts
- [ ] Verify server starts and tools work
- [ ] Test in VS Code Stable
- [ ] Test in VS Code Insiders

### Documentation Updates
- [ ] Update SETUP.md with new installation method
- [ ] Mark NPM_PACKAGE_MIGRATION_PLAN.md as completed
- [ ] Add troubleshooting section for common issues
- [ ] Document SCB registry authentication process

---

## Timeline Estimate

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| **Phase 1: Code Changes** | 3-4 hours | SCB registry URL needed before publishConfig |
| **Phase 2: Tooling & Scripts** | 2-3 hours | Phase 1 complete |
| **Phase 3: Local Testing** | 2 hours | Phase 1 complete |
| **Phase 4: NPM Setup** | 1-2 hours | Registry URL, permissions verified |
| **Phase 5: Publishing** | 1 hour | All phases complete |
| **Phase 6: Integration Testing** | 2-3 hours | Published to NPM |
| **Phase 7: Documentation** | 1-2 hours | All testing complete |
| **Total** | **12-17 hours** | Assuming no blockers |

---

## Risk Assessment

### High Risk
1. **SCB NPM Registry URL Unknown** - Blocks publishConfig setup
   - Mitigation: Contact SCB DevOps immediately
   
2. **Publishing Permissions Not Verified** - Blocks npm publish
   - Mitigation: Request access in parallel with development

### Medium Risk
3. **Package Naming Not Finalized** - Affects URLs, documentation
   - Mitigation: Decide early (recommend unified package)

4. **Backwards Compatibility Concerns** - May break existing users
   - Mitigation: Support all three config methods

### Low Risk
5. **URL Encoding Issues** - Install buttons may not work
   - Mitigation: Test generated URLs before publishing

6. **VS Code Input Prompts Not Working** - Users can't configure
   - Mitigation: Test in VS Code Stable and Insiders

---

## Success Criteria

### Must Have (Required for Completion)
- ✅ Command-line arguments work for all 6 parameters
- ✅ All 4 packages published to SCB NPM registry
- ✅ One-click install badges in README
- ✅ VS Code redirect URLs work in browser
- ✅ All 6 input prompts appear and work
- ✅ Server starts successfully after one-click install
- ✅ Tools work in Copilot Chat after installation

### Should Have (Recommended)
- ✅ Backwards compatibility with config.json
- ✅ Environment variable support
- ✅ Clear error messages with usage instructions
- ✅ Credential masking in logs
- ✅ .npmrc file for SCB registry default

### Nice to Have (Optional)
- ✅ Validation script (prepublishOnly)
- ✅ Automated tests for config loading
- ✅ CI/CD pipeline updates for NPM publishing
- ✅ Version management strategy documented

---

## Post-Migration Tasks

1. **Announce to Users**
   - Email with new installation method
   - Show one-click install demo
   - Provide migration guide for existing users

2. **Monitor Usage**
   - Track NPM download counts
   - Collect feedback on installation experience
   - Monitor error logs for common issues

3. **Deprecation Plan** (If Applicable)
   - If forcing migration from config.json:
     - Set deprecation timeline (e.g., 3 months)
     - Show warnings in server logs
     - Update documentation

4. **Documentation Maintenance**
   - Keep install URLs updated with new versions
   - Document common troubleshooting scenarios
   - Update screenshots/videos

---

## Open Questions

1. **Registry Authentication:** How do SCB users authenticate to private NPM registry? (SSO, PAT, certificate?)

2. **Network/Proxy:** Will NPX work behind SCB proxy (185.46.212.98:443)?

3. **Node.js Version:** What Node.js version is standard at SCB? (Migration plan assumes 20+)

4. **Versioning Strategy:** Use Lerna fixed mode (all packages same version) or independent?

5. **CI/CD Integration:** Should Azure Pipeline automatically publish on merge to main?

---

## References

- **Migration Plan:** `docs/archive/NPM_PACKAGE_MIGRATION_PLAN.md`
- **Install Mechanism:** `docs/ONE_CLICK_INSTALL_EXPLAINED.md`
- **Azure DevOps MCP Example:** https://github.com/microsoft/azure-devops-mcp
- **VS Code MCP Docs:** https://code.visualstudio.com/docs/copilot/chat/mcp
- **NPX Documentation:** https://docs.npmjs.com/cli/v10/commands/npx

---

*Plan Created: 2 February 2026*
*Authors: Saravanan R (1540326), Shiyamkumar U (2002918)*
*Status: Ready for Implementation (Pending SCB Registry URL)*
