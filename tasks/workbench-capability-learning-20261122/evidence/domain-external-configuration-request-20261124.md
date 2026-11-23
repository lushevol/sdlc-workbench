# Domain external dependencies and configuration

Date: 24 November 2026, Asia/Singapore.
Source: User message in Codex session `01a207fd-fe29-7f81-b9be-4d41f7918f0f`.
Priority: High-priority user reference.

## Exact user input

> please consider in domain capability that there are cases depends on external system like credentials which can't maintains in skill have to refer from env vars, or configures depends on project settings.

## Authorized scope

Refine the extractor and CES configuration guidance using existing variable and connector conventions.
Document external credential references and project-owned settings without storing their values in skills.
Preserve offline extraction and inspection when live dependencies are unavailable.
This change does not authorize external calls, credential collection, or project configuration changes.
