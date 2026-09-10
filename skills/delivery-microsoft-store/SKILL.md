---
name: delivery-microsoft-store
description: >-
  Deliver Windows 11 apps through Microsoft Store MSIX or hosted MSI/EXE: bind
  identity and artifact, stage Partner Center, submit, recover certification,
  and prove public acquisition. Excludes Windows app implementation.
---

# Microsoft Store Delivery

Set `$PLUGIN_ROOT` (`$env:PLUGIN_ROOT` in PowerShell) to the host-provided plugin
root when available; otherwise resolve this skill folder's `../..`.

Read both contracts before changing Partner Center state:

- shared authority, state, credential, receipt, retry, and completion rules:
  `$PLUGIN_ROOT/references/delivery-control-contract.md`
- Microsoft-specific package, listing, recovery, and proof rules:
  `$PLUGIN_ROOT/references/microsoft-store-delivery.md`

The outcome is not "package uploaded" or "certification passed." It is the
requested delivery effect, proved at its real boundary: a correct draft, a
specific submitted artifact, or an anonymously visible and installable Store
release.

## Workflow

1. **Recover intent and live state.** Classify the requested effect as
   `stage`, `submit`, `release`, or `verify`. Read repository guidance and the
   current Partner Center product/submission before assuming a first release or
   update. Preserve Microsoft's raw status alongside the shared normalized
   phase.
2. **Select the lane.** Keep Store-hosted MSIX/AppX packages, acquired through
   Microsoft Store/App Installer, separate from the hosted MSI/EXE installer
   lane. The latter has a different submission API, publisher-hosted versioned
   HTTPS installers, signing, and update semantics. Do not silently convert
   between them.
3. **Bind target identity.** Record the Partner Center product ID, reserved
   product name, exact case-sensitive package `Identity` name and publisher,
   visible application ID and aliases, package version, architecture/device
   scope, markets, visibility, pricing, release mode, and any flight. Resolve
   these from live Partner Center identity details, not remembered values.
   Read name-reservation ownership/expiry and remember that a product already
   made public cannot simply be changed back to private.
4. **Bind the actual artifact.** Produce a build receipt for the exact upload
   file with a portable filename or private task-local locator, size, SHA-256,
   package identity/version, and inspected nested payload. Do not substitute a
   loose build directory or a later rebuild. For a
   hosted installer, bind both its local hash and the bytes served by its
   versioned HTTPS URL.
5. **Run proportional preflight.** Inspect the packaged manifest and payload,
   application count/aliases, restricted capabilities and justifications,
   signing expectations, supported Windows versions, and listing assets. Run
   WACK against the candidate when applicable; a hang or missing verdict is
   `undetermined`, never pass. Keep local certificate trust failures separate
   from Store certification. For hosted MSI/EXE, require a standalone/offline
   installer and prove silent installation with the submitted EXE switches or
   default silent behavior, or MSI `/qn`, on an authorized test surface.
6. **Stage a draft.** Prefer the project's already-working official tooling.
   When the Microsoft Store Developer CLI is present and supports this exact
   product/lane, feature-probe its current help and use draft-preserving
   behavior such as `--noCommit`; otherwise use Partner Center. Use the UI for
   account/bootstrap, identity reservation, legal declarations, and any field
   the CLI/API cannot faithfully represent. Never install tooling or change its
   global telemetry/auth configuration silently.
7. **Read back and preview.** Re-read the draft from Partner Center or the
   official API. Show one exact final preview containing product, artifact hash,
   identity/version, listing/markets, visibility, price, schedule or publishing
   hold, declared capabilities, and the next external effect. Route unresolved
   attestations and consequential choices through the shared human checkpoint.
8. **Commit once and observe.** After authority is satisfied, submit or publish
   exactly once, capture the returned submission identity/state, and re-read it.
   A timeout is unknown outcome: query status before any retry. Never replace,
   cancel, or delete a draft/submission without its own checkpoint.
9. **Prove the requested boundary.** Distinguish preprocessing,
   certification, release, publishing, and `In the Store`. For a public release,
   verify the anonymous listing and acquisition path, then proportionally prove
   Store install, launch, alias behavior, update, and uninstall on Windows 11.
   Do not call `In certification` public or done. Start a recurring watcher only
   when the user explicitly asks to wait, monitor, babysit, or finish through
   asynchronous review; suppress unchanged observations, continue through
   meaningful intermediate states to the requested terminal, prove the final
   customer surface, and remove the completed watcher.

For package flights, bind group/rank/device-family ceiling and separate
certification state. For gradual rollout, remember that it affects package
updates rather than listing changes, 100% is not necessarily finalized, and
halt is not rollback. Windows chooses the highest applicable version; repair
with a higher version rather than promising an old-package downgrade.

## Failure Boundary

- Re-read current product, draft, and submission state before recovery; never
  create a duplicate product or submission merely because an operation timed
  out or a local receipt is stale.
- If the artifact changed after upload, invalidate that upload's proof and
  stage the new hash deliberately. Deletion/cancellation remains a separate
  consequential action.
- If a package contains a hidden second application, unbound identity, loose
  payload mismatch, unjustified restricted capability, leaked screenshot or
  URL identity, or no determinate WACK verdict, stop before submission and use
  the recovery map in the Microsoft reference.
- Never request, print, store, or pass Partner Center credentials, certificate
  private material, client secrets, or test-account secrets through chat,
  command arguments, logs, receipts, or committed files. Use the shared secure
  handoff contract.
