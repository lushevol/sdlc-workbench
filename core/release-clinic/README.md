# Release Clinic in AI SDLC Workbench

Run these tools through the installed Workbench command.
Configure variables in the Workbench root `.env`.
Use the root `.env.example` as the configuration template.
Process environment values take precedence over file values.

```sh
python -m pip install ".[release-clinic]"
ai-sdlc --workspace . release-clinic doctor
ai-sdlc --workspace . release-clinic path
```

Read the [integration guide](../../docs/RELEASE_CLINIC.md) for supported commands and configuration paths.
Read the [shared skill](../../.agents/skills/release-clinic/SKILL.md) for agent reporting procedures.
Imported plugin documents describe their original distribution.
Use the integration guide for Workbench installation, root configuration, and output paths.

Installed runtime assets stay in the Python package.
Generated workspaces receive guides and shared skills without runtime source.
