---
name: delivery-chrome-web-store
description: >-
  Deliver a Chrome extension through Chrome Web Store: bind item/package,
  inspect Manifest V3 permissions and privacy, stage review, publish or roll
  out, recover uncertainty, and prove Store installation. Excludes extension
  coding and growth.
---

# Chrome Web Store Delivery

Use this lane for a first Chrome Web Store listing, an existing extension
update, trusted-tester distribution, deferred publication, percentage rollout,
rollback, rejection recovery, or public-install verification. Read the
[shared control contract](../../references/delivery-control-contract.md) and
[Chrome Web Store reference](../../references/chrome-web-store-delivery.md)
before a provider write.

## Deliver

1. Classify the exact effect as `prepare`, trusted-tester or draft `stage`,
   `submit`, `release`, rollout change, rollback, or `verify`. Bind the Google
   developer identity, publisher and item ID, current channel/visibility,
   intended countries, existing review, and published version from live
   Developer Dashboard or API state. A local extension name is not Store
   identity.
2. Read the live Package state before choosing the upload format. Bind one ZIP
   for the standard Store-signed path, or one signed CRX only when this exact
   item already opted into Verified CRX Uploads. Record source revision,
   filename, format, size, SHA-256, root entry inventory, `manifest_version`,
   extension `version`, minimum Chrome version, public key/extension-ID
   relationship when relevant, and every permission, host permission,
   externally connectable origin, content script, web-accessible resource,
   service worker, CSP, and remote endpoint. Rebuild, repack, or resign means a
   new artifact epoch.
3. Load the unpacked candidate into an isolated Chrome profile and run the
   smallest install, update, restart, permissions, core behavior, options,
   uninstall/reinstall, and data-migration smokes that distinguish this release.
   Unpacked success is preflight only; it is not Store delivery.
4. Reconcile listing copy, icons/screenshots, category, language, support and
   privacy URLs, single-purpose explanation, permission justifications, data
   use/handling, authentication, payments, distribution visibility, countries,
   and trusted testers against the shipped bytes. Never minimize or fabricate
   a disclosure merely to improve review odds.
5. Use Developer Dashboard for developer-account bootstrap, fee/identity/2SV,
   the first item, privacy and listing forms, distribution changes, and fields
   the current API cannot represent. For an existing item, prefer a reviewed
   project-native publisher or Chrome Web Store API v2 only after probing its
   live auth, item/status, upload, publish, staged-publish, cancel, and rollout
   behavior. Do not introduce a publisher framework or service-account key for
   one release.
6. Upload the exact bound ZIP or Verified-CRX artifact once and read back its
   version/status/warnings. Preview item, format, hash, version,
   permission/data diffs, listing revision, visibility, countries, release
   mode, rollout, and the precise next effect. Then submit or publish once
   under the shared authority contract.
7. Preserve provider states: uploaded draft, pending review, rejected, approved
   and staged, published, partial rollout, full rollout, removed, and verified.
   On a timeout or lost browser result, read the existing item/status and match
   the version before retrying. Do not create a second item or bump/repackage
   merely to escape an unknown outcome.
8. Prove the requested surface. Public delivery requires the canonical Store
   listing in the intended region, correct publisher/version/permissions, a
   Store-origin install or update in a clean Chrome profile, restart, and the
   product-critical smoke. Trusted-tester delivery requires an eligible tester
   install through the provider route, not a locally loaded directory.

## Failure Boundary

- A new permission can disable an installed extension until the user accepts
  it. Treat permission growth as a user-impacting release decision.
- Percentage rollout is provider- and eligibility-dependent, can only move in
  allowed directions for that release, and is not a substitute for review.
- Deferred approval expires; read its live deadline. A staged item is not
  published.
- Rollback is a new provider transition with its own version and evidence; do
  not overwrite a current ZIP or promise instantaneous downgrade semantics.
- A `.pem`, OAuth secret, service-account key, token, cookie, or developer
  session is protected material. Legacy local packaging keys are neither Store
  authorization nor permission to expose or reuse them. Use the shared secure
  handoff and credential-storage boundary.
- Cancellation, unpublish, takedown appeal, ownership transfer, key rotation,
  or destructive listing change needs an exact consequential checkpoint.

Stop at the strongest proved state and name any still-external review,
eligibility, propagation, or public-install blocker exactly.
