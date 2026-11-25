# Reuse and review rules

Search `assets/experience/index.yaml` by domain, problem, trigger, repository, capability, tool, environment, and variable name.
Read the matching packet before acting. Confirm its status, applicability, source revisions, prerequisites, and verification conditions.

Use a packet as follows.

1. Bind the current task and environment.
2. Resolve variables from approved local configuration.
3. Adapt paths and commands only where the packet permits it.
4. Execute the smallest authorized step that tests applicability.
5. Record the new result and evidence in the current task.
6. Keep the packet unchanged until a review records a successor or a status change.

Mark a packet stale or create a successor when a source revision, dependency, endpoint contract, variable contract, or governing knowledge record changes.
Retain the prior packet and its evidence links. A failed replay is reusable failure knowledge and must not erase the earlier successful result.

The first implementation uses exact text and YAML indexing. Add semantic compilation through the existing wiki lifecycle only after canonical knowledge records are ready.
