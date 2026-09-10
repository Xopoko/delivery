---
name: delivery
description: >-
  Deliver build-ready apps, extensions, posts, YouTube media, websites, and AWS
  services: route, stage, submit or release with exact authority, recover
  uncertainty, and prove the user-visible result. Excludes implementation.
---

# Delivery

Use this skill when the desired outcome is distribution to a store, TestFlight,
a testing track, a notarized download, a public social/video surface, or a
production website/cloud service. A direction such as “deliver this”
authorizes autonomous recovery, validation, draft creation, and reversible
staging inside the named channel. Bind the final external effect precisely; do
not turn the path into a questionnaire.

Read `$PLUGIN_ROOT/references/delivery-control-contract.md` before mutation.
Use `$PLUGIN_ROOT` (`$env:PLUGIN_ROOT` in PowerShell) for bundled references and
the optional receipt helper. If the host does not supply that variable, resolve
the plugin root as `../..` from this skill folder. No private companion plugin
or machine-specific configuration is required.

## Route

- iOS, TestFlight, App Store Connect, Mac App Store, Developer ID, Gatekeeper,
  or notarization: use `delivery-apple`.
- Android App Bundle, Play Console, Play testing, review, managed publishing, or
  rollout: use `delivery-google-play`.
- Windows 11, Partner Center, MSIX, App Installer, MSI/EXE, certification, or
  Store listing: use `delivery-microsoft-store`.
- Chrome extension, Chrome Web Store, trusted testers, extension review,
  deferred publish, rollout, or Store install: use `delivery-chrome-web-store`.
- LinkedIn post, company/member share, X post/thread, launch announcement, or
  canonical social-post proof: use `delivery-social`.
- YouTube video, Short, private upload, captions, checks, scheduling, or watch
  page: use `delivery-youtube`.
- Website, API, Ubuntu/self-hosted production, domain, DNS/TLS, reverse proxy,
  Cloudflare Tunnel, origin cutover, or public endpoint: use `delivery-web`.
- AWS Lightsail, EC2, ECS, Lambda, S3/CloudFront, CloudFormation, deployment,
  traffic shift, or AWS-hosted backend: use `delivery-aws`, composing
  `delivery-web` for the consumer-facing route.

If more than one destination is requested, bind and deliver each channel as a
separate provider object. Share product facts where truthful, but never share a
version, signing identity, review state, or authorization by inference.

## Control loop

1. Reconstruct `desired_effect` as `prepare`, `stage`, `submit`, `release`, or
   `verify`, plus the exact provider, account/team/tenant/channel, product
   identity, audience,
   territory or track, visibility, schedule, and price when relevant. Mark only
   material unknowns.
2. Observe source and Git state, artifact candidates, installed specialist
   capabilities, authenticated provider state, existing drafts/submissions,
   and current official requirements. Resume the matching object; do not create
   a new app, package, edit, upload, or video just because local state is thin.
3. Bind one release input by canonical source/version and an immutable digest:
   file SHA-256, media/package hash, exact post payload hash, source archive,
   OCI digest, function/version, or rendered deployment revision. Bind stable
   provider identifiers and signing/deployment identity without secrets.
   Recompute or re-resolve it immediately before upload, deploy, or final commit.
4. Select the narrowest live route: existing project workflow first, then an
   official or already-owned CLI/API, then official browser UI or Computer Use
   for bootstrap and unsupported fields. Do not introduce a release/deployment
   framework, paid cloud or social service, MCP, CI pipeline, infrastructure
   layer, or global setting for one delivery.
5. Validate on the provider-relevant surface. Stage as a draft, internal test,
   private upload, zero-traffic origin/revision, or no-commit submission when
   supported. Preserve returned object IDs and observe asynchronous processing
   instead of inferring it.
6. Before a consequential transition, show one compact preview bound to the
   current artifact hash, destination, metadata/declarations, release mode,
   markets/track/visibility/schedule/price, and provider object. Request approval
   if that exact effect is not already authorized by the current request or if a
   truthful human attestation is required. Do not ask twice for an unchanged
   effect that the current request already authorizes exactly.
7. Perform one bounded write and retain the provider receipt. On timeout,
   disconnect, or missing response, record `effect_unknown` and read provider
   state before any retry or alternate writer.
8. Prove the strongest achieved state independently: provider/API state, then
   the surface available to the intended audience, and finally install, launch,
   update, uninstall, alias, browser-extension behavior, canonical post, playback/captions/Shorts
   classification, or the DNS/TLS/origin/application path where that
   behavior defines delivery. For protected products, check expected anonymous
   denial or challenge and the authorized consumer path; a successful deployment
   must preserve the requested access restrictions.
9. Stop at the requested outcome. If review or processing remains external,
   preserve the exact observed state and next discriminator. Create monitoring
   only when the user explicitly asks to wait, finish, or babysit it.

For work spanning sessions, use the optional helper described in the control
contract. It is a receipt, not a source of truth and not permission to mutate.

## Completion language

Say `prepared`, `uploaded`, `processing`, `staged`, `submitted`, `in review`,
`approved`, `scheduled`, `posted`, `deployed`, `traffic shifted`, `released`,
or `user-visible` exactly. Never compress them to “published.” Report a valid
provider rejection or a precise identity, policy, agreement, credential,
review, health, migration, or propagation blocker as the completed current
outcome; do not manufacture progress around it.
