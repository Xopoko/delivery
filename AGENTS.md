# Contributing with an agent

Delivery Skills is developed and tested as a Codex plugin, with a Claude Code
package included. Keep workflows in `skills/`, shared provider guidance in
`references/`, and deterministic local tools in `scripts/`.

- Preserve exact target identity, authority, artifact binding, and recovery after
  an uncertain external effect. Keep native provider states visible.
- Keep the core usable without another plugin, secret manager, or host service.
  Discover optional tools; provide a project-native or official-UI fallback.
- Never commit delivery receipts, user accounts, local paths, provider responses,
  or credentials. Examples must be synthetic and clearly labeled.
- Update both plugin manifests and the marketplace together when versioning.
- Validate with `python scripts/validate_package.py`. For executable changes,
  run `python -m unittest discover -s tests -v` and `python scripts/demo.py`.
  Prose edits need link validation and a focused diff review.
- Local tests establish local behavior. Store approval, deployment, publication,
  installation, and end-user acceptance each need their own evidence.
