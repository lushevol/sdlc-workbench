# Code of Conduct

## Our Pledge

We as contributors and maintainers pledge to make participation in this project a respectful and harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socioeconomic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

We pledge to act and interact in ways that contribute to an open, welcoming, diverse, inclusive, and healthy community.

## Our Standards

Examples of behavior that contributes to a positive environment:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community and the project
- Showing empathy towards other contributors

Examples of unacceptable behavior:

- The use of sexualized language or imagery, and sexual attention or advances
- Trolling, insulting or derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

## Project-Specific Obligations

Beyond the general standards above, contributors to this project have specific documentation responsibilities:

### Tool Changes

Any new or modified **tool** (defined via `server.tool()` in `packages/*/src/tools/*.js`) **must** be accompanied by a corresponding update to [docs/TOOLS_REFERENCE.md](docs/TOOLS_REFERENCE.md). Pull requests that add or change tools without updating the reference doc will not be merged.

### Prompt Changes

Any new or modified **prompt** (defined in `packages/unified/src/prompts.js`) **must** be accompanied by a corresponding update to [docs/PROMPTS.md](docs/PROMPTS.md). Pull requests that add or change prompts without updating the prompts doc will not be merged.

### Pre-PR Script

Before raising a pull request, contributors must run:

```bash
yarn pre-pr
```

This command refreshes the one-click install badge URLs in `README.md`, updates the live tool/prompt stats in `CONTRIBUTING.md`, and runs the full test suite. PRs where this has not been run (detectable via stale stats or failing tests) will be sent back.

### Credential Safety

Never commit credentials, tokens, or secrets. `config.json` is gitignored — keep it that way. If you accidentally expose a credential, rotate it immediately and let a maintainer know.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to the project maintainers. All complaints will be reviewed and investigated promptly and fairly.

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, issues, and other contributions that do not align with this Code of Conduct, and will communicate reasons for moderation decisions when appropriate.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant](https://www.contributor-covenant.org), version 2.1.
