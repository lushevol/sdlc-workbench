# Execution responsibility

The `core/runtime.py` implementation dispatches provider operations and checks explicit operation grants.
The provider registry validates operation schemas and enabled plugins.
Configured test suites execute named command arrays and retain output.
The Robot provider executes registered suites through a separate Python environment.
It retains native reports, test statuses, source identity, and execution limits.
Shared skills coordinate agent-driven engineering work.
Durable workflow scheduling and independent agent orchestration belong to later delivery phases.
