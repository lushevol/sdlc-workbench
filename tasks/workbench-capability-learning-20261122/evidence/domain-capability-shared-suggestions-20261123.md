# Shared domain capability suggestions

Retrieved: 23 November 2026.
Source: https://chatgpt.com/share/6b040c48-b048-83ea-8870-12dc4d24c84f
Conversation title: Design Reusable Skills.

This retained selection contains the relevant user messages and latest assistant suggestion.
User messages govern intent. Assistant suggestions supply design input within the current request.
Other conversation content remains outside this selection.

## User simplification direction

Source content item: `2320`.
UTF-8 content SHA-256: `d7e241598161baa682b33f97fb52781895eba2d55499084e75e8d44bebf589a5`.

I think you have made it a way too complex. I don't need hooks. I just need one skill to extract the relevant domain capabilities. The most use case is that something like API calls, or workflows, or instructions on some specific scenarios. So please focus on this contracts definition, and like APIs, I need the nearly OpenAPI schema I need, and the sample response on different payloads and parameters. And for workflows, it's including the failure point you tried in the agent sessions. Make it simple, but in detail on the skill definition, the construction.

## User domain layout direction

Source content item: `982`.
UTF-8 content SHA-256: `4579ac228a9482b42bc53c43e0c9341182a8cf6c354459fbebae291cc3255b99`.

Good. It's much better now. I prefer to keep the final files under Knowledge Integration folder, inside each domain, One is the Contracts folder, which contains the APIs, schemas, and some interface dependencies. One is the Workflows, which contains the concrete steps and the scripts and some reusable tools for this domain, if have failure points please record as well . And one is the Knowledge, which is the background context, something like that. Enrich it and discuss with me.

## Latest assistant suggestion

Source content item: `874`.
UTF-8 content SHA-256: `2c1fb074539dd638f3d87e38e50b38b000ac9495c8cf49cb08773e97b12acebd`.

I think this is a much better structure. It gives each external system its own **domain capability library**, with a clear separation between what the system exposes, how we use it, and what we know about it.

I would standardize your proposed three directories:

- **Contracts** — What the system exposes and how to interact with it.
- **Workflows** — How to accomplish specific tasks, including scripts, tools, and lessons from failures.
- **Knowledge** — What the system is, how it works, and why certain decisions or rules exist.

The important part is to make these three directories **interconnected**, rather than independent collections of documents.

## 1. Proposed project construction

<box border radius="lg" padding={3} gap={2}>
  <row align="center" gap={2}>
    <icon name="folder-open" color="secondary"/>
    **knowledge/integrations/**
  </row>
  <box padding={{left:3}} gap={2}>
    <row align="center" gap={2}>
      <icon name="folder-open" color="secondary"/>
      **ado/**
    </row>
    <box padding={{left:4}} gap={2}>
      <row align="start" gap={2}>
        <icon name="folder" color="secondary"/>
        <box flex="1" gap={1}>
          **Contracts/**

          <text size="xs" color="secondary">openapi.yaml, schemas/, examples/, dependencies.md</text>
        </box>
      </row>
      <row align="start" gap={2}>
        <icon name="folder" color="secondary"/>
        <box flex="1" gap={1}>
          **Workflows/**

          <text size="xs" color="secondary">deploy-artifact.md, resolve-build.md, scripts/, tools/</text>
        </box>
      </row>
      <row align="start" gap={2}>
        <icon name="folder" color="secondary"/>
        <box flex="1" gap={1}>
          **Knowledge/**

          <text size="xs" color="secondary">overview.md, conventions.md, architecture.md, decisions.md</text>
        </box>
      </row>
      <row align="start" gap={2}>
        <icon name="file-text" color="secondary"/>
        <box flex="1" gap={1}>
          **README.md**

          <text size="xs" color="secondary">Domain entry point and capability index</text>
        </box>
      </row>
    </box>
    <row align="center" gap={2}>
      <icon name="folder" color="secondary"/>
      **ces/** — same structure
    </row>
    <row align="center" gap={2}>
      <icon name="folder" color="secondary"/>
      **rundeck/** — same structure
    </row>
  </box>
</box>

Each directory is populated only as needed. For example, a domain with no reusable scripts does not need a `scripts/` directory.

I would also include one `README.md` in each domain. It is important because it helps the agent discover what capabilities already exist without reading every file.

## 2. Contracts — precise system interfaces

This directory should serve as the **technical source of truth for external interfaces actually used or investigated by the workbench**.

| Content | Suggested file | Requirements |
|---|---|---|
| REST APIs | `openapi.yaml` | OpenAPI 3.1, methods, paths, parameters, headers, request/response schemas, status codes, authentication |
| API examples | `examples/*.yaml` | Paired request/response cases, including varying parameters, payloads, and failures |
| Shared schemas | `schemas/` | Reusable domain objects, enums, field constraints |
| Other interfaces | `interfaces.md` | GraphQL, gRPC, SOAP, CLI, file exchange, Kafka, messaging |
| Dependencies | `dependencies.md` | Upstream/downstream systems, access prerequisites, protocols and runtime dependencies |

### What I would emphasize for API contracts

Do not just record the endpoint.

For each API, the agent should capture **how the response changes under different input conditions**.

For example, an ADO artifact lookup might have these observed cases:

| Scenario | Request variation | Expected evidence to record |
|---|---|---|
| Standard artifact | Valid build ID and artifact name | Returned artifact metadata |
| Release branch | Different branch-derived artifact name | Actual artifact identity |
| Missing artifact | Artifact name not present | HTTP status and error payload |
| Unauthorized | Insufficient permission | HTTP status and authorization error |
| Different build | Same naming convention, different build ID | Difference in returned artifact metadata |

These are example scenarios to investigate, not claims that your particular ADO instance behaves in these ways.

Each example should preserve its request and matching response, with sanitized values and the original evidence reference.

One practical recommendation: **do not copy the entire vendor OpenAPI specification into every domain**. Document the operations you actually use, then reference the official specification for additional details. This keeps contracts focused and manageable.

## 3. Workflows — reusable operational capability

This is the most valuable directory for your daily engineering work.

A workflow should describe a **complete, actionable scenario**, not merely a sequence of API calls.

For example:

<box border radius="lg" padding={3} gap={2}>
  **ADO — Deploy an application artifact**
  <list marker="number" connector="solid" gap={2}>
    <list-item>
      **Identify the target**

      Determine the application, deployment environment, repository, pipeline, and release version.
    </list-item>
    <list-item>
      **Resolve the build**

      Query ADO using the relevant contract. Select the correct build using verified project-specific conditions.
    </list-item>
    <list-item>
      **Resolve the artifact**

      Determine its name based on the verified version and branch convention. Confirm that the artifact actually exists.
    </list-item>
    <list-item>
      **Retrieve the package**

      Execute an existing script or documented API sequence. Verify artifact identity and integrity.
    </list-item>
    <list-item>
      **Deploy and verify**

      Follow the environment-specific deployment process, required approvals, and verification steps.
    </list-item>
  </list>
</box>

### Each workflow should contain

I suggest this standard template:

<CodeBlock language="markdown"># Workflow: Deploy ADO Artifact

## Purpose
What task this workflow accomplishes.

## Applicability
Which applications, pipelines and environments
this procedure applies to.

## Prerequisites
Required access, configuration and dependencies.

## Inputs
Required and optional parameters.

## Procedure
Ordered steps with exact commands or API references.

For every step:
- Action
- Required input
- API or script
- Expected output
- Next-step dependency

## Decision Rules
Selection logic, branches and stop conditions.

## Failure Points
For each encountered failure:
- Attempted action and inputs
- Observed error/response
- Confirmed cause or unresolved hypothesis
- Successful correction, if found
- Conditions where the failure occurs
- Evidence reference

## Verification
How to establish successful completion.

## Recovery
Safe retry, rollback or manual intervention.

## Related Contracts
Links to the relevant API operations and examples.

## Related Knowledge
Links to relevant conventions and background context.
</CodeBlock>

### Scripts and reusable tools

I support putting **domain-specific scripts directly under `Workflows/`**, as you proposed.

For example:

```text
Workflows/
├── deploy-artifact.md
├── resolve-build.md
├── scripts/
│   ├── resolve-artifact.mjs
│   ├── download-artifact.mjs
│   └── verify-package.mjs
└── tools/
    └── ado-artifact-client.mjs
```

The distinction I recommend:

**Scripts** implement concrete workflow steps. **Tools** provide reusable operations that multiple workflows can call.

A script should ideally have predictable inputs, structured JSON output, clear errors, and read-only or dry-run behavior where appropriate.

For example:

```bash
node scripts/resolve-artifact.mjs \
  --pipeline settlement \
  --branch release/1.2 \
  --version 1.2.0
```

This is an illustrative command interface, not a claim that such a script already exists.

One important boundary: keep generic ADO authentication and HTTP transport utilities in the existing shared connector layer if one exists. Avoid duplicating generic API clients inside every domain workflow.

### Preserve failed attempts

I especially agree with this requirement.

Suppose the agent tries three artifact-resolution methods before discovering the correct one. The resulting document should record all three attempts when they provide a meaningful lesson—not only the final successful command.

It should explain why earlier approaches failed, under what conditions they failed, and whether the observed failure is specific to a pipeline or environment.

This prevents future agents from repeating the same investigation.

---

## 4. Knowledge — background context and domain understanding

The Knowledge directory should explain the **meaning and rationale** behind contracts and workflows.

For ADO:

```text
Knowledge/
├── overview.md
├── pipeline-architecture.md
├── artifact-conventions.md
├── environments.md
└── decisions.md
```

For CES:

```text
Knowledge/
├── overview.md
├── entitlement-model.md
├── migration-background.md
├── migration-principles.md
├── environment-baselines.md
└── known-limitations.md
```

I would structure the content around four concerns:

| Knowledge type | Example |
|---|---|
| Background | Why CES replaced the legacy entitlement system |
| Architecture | Relationships between ADO pipelines, artifacts, repositories, and deployments |
| Domain rules | How an entitlement is mapped, validated, or reconciled |
| Decisions and limitations | Why a particular migration or integration approach was selected, and its constraints |

The agent should not unnecessarily reproduce API definitions here.

For example:

- `Contracts` documents the CES role-query API.
- `Workflows` explains how to reconcile migrated entitlements.
- `Knowledge` explains the approved migration mapping principles.

This separation keeps knowledge understandable even when the underlying API changes.

## 5. How the three directories relate

<box border radius="xl" padding={3} gap={2}>
  <box align="center" gap={1}>
    <box background="surface-secondary" radius="lg" padding={3} width="100%" align="center" gap={1}>
      <row align="center" justify="center" gap={2}>
        <icon name="workflow"/>
        **Workflows**
      </row>
      <text size="xs" color="secondary" textAlign="center">What to do, in which order, and how to recover</text>
    </box>
    <row align="center" justify="around" width="100%">
      <icon name="arrow-down-left" color="secondary" size="lg"/>
      <icon name="arrow-down-right" color="secondary" size="lg"/>
    </row>
  </box>
  <grid columns={2} gap={2}>
    <grid-item>
      <box border radius="lg" padding={3} height="100%" align="center" gap={1}>
        <icon name="file-code" color="secondary"/>
        **Contracts**
        <text size="xs" color="secondary" textAlign="center">How to communicate with systems</text>
      </box>
    </grid-item>
    <grid-item>
      <box border radius="lg" padding={3} height="100%" align="center" gap={1}>
        <icon name="book-open" color="secondary"/>
        **Knowledge**
        <text size="xs" color="secondary" textAlign="center">Why the system behaves this way</text>
      </box>
    </grid-item>
  </grid>
</box>

I recommend using Markdown relative links between them.

For example, a workflow might contain:

```markdown
## References

- [Artifact API](../Contracts/openapi.yaml)
- [API examples](../Contracts/examples/)
- [Artifact naming rules](../Knowledge/artifact-conventions.md)
```

This makes a workflow self-contained enough for execution while avoiding duplicated definitions.

## 6. How the single extractor skill should maintain this structure

The skill's job becomes straightforward.

| Stage | Agent action |
|---|---|
| 1. Identify | Determine which domain the current discovery belongs to |
| 2. Inspect | Read the domain README and relevant existing files |
| 3. Classify | Decide whether each discovery is a contract, workflow, or knowledge item |
| 4. Extract | Preserve precise API information, procedural steps, and useful failure experiences |
| 5. Merge | Enrich existing documents rather than create duplicates |
| 6. Verify | Check evidence, schema consistency, references, and applicability |
| 7. Update | Write the relevant domain files and update the README index |

There is no need to introduce another engine to do this.

The skill can use the agent's ordinary capabilities to inspect session context, read files, analyze code, and create or edit documentation.

I would add three rules to its instructions:

**First: Preserve detail, not session noise.** Keep exact API behavior, significant failed attempts, and confirmed resolutions. Discard irrelevant investigation steps.

**Second: Preserve uncertainty.** If the agent has only seen one API response, it should not infer a complete response model or assume that the same behavior applies to every environment.

**Third: Maintain rather than regenerate.** Every invocation must check existing domain files and merge discoveries, preserving valid information and flagging contradictions.

## 7. One additional improvement: domain capability indexing

I would make `README.md` a compact, discoverable index rather than a long general introduction.

For example:

<CodeBlock language="markdown"># Azure DevOps Integration

## Purpose
ADO integration for development, build,
release and operational workflows.

## Contracts
| Operation | Description |
|-----------|-------------|
| getBuild | Retrieve build metadata |
| getBuildArtifact | Resolve build artifact |

## Workflows
| Workflow | Purpose |
|----------|---------|
| resolve-build | Find the correct pipeline build |
| deploy-artifact | Retrieve and deploy an artifact |

## Knowledge
- Pipeline architecture
- Artifact naming conventions
- Environment configuration

## Known Limitations
- Record verified restrictions here
</CodeBlock>

Link each entry to its corresponding file in the actual implementation.

This index becomes the **entry point for AI retrieval**.

When you ask the workbench to deploy an application through ADO, the agent can first read the domain index, identify the relevant workflow, and then load only the referenced contracts and knowledge.

No vector database or knowledge graph is necessary for this initial version.

---

## 8. My proposed final boundaries

I would make these rules explicit:

| Directory | Primary question it answers | Should contain |
|---|---|---|
| **Contracts** | How can I interact with this system? | Interfaces, precise schemas, request/response examples, dependencies |
| **Workflows** | How do I complete this task correctly? | Procedures, conditions, executable scripts, verification, failure lessons |
| **Knowledge** | What must I understand about this system? | Background, architecture, business concepts, conventions, decisions |

And one `domain-capability-extractor` skill that maintains all three.

### One design choice worth discussing

You proposed placing scripts and reusable tools in `Workflows`, which makes sense. I would take this a little further:

**Should workflows be documentation only, or should every repeatable workflow eventually expose a standard executable entry point?**

My preference is a hybrid: a workflow always has a detailed Markdown procedure, but it can optionally provide scripts that an agent can execute directly. In that model, the workflow remains useful even when no script exists, and frequently repeated BAU tasks can progressively become executable without changing the domain structure.

---

If you want, I can:

- Define structure for Contracts folder
- List key files for Workflows folder
- Draft README.md template for each domain
