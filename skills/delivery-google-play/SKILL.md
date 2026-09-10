---
name: delivery-google-play
description: >-
  Deliver an Android release through Google Play: bind account, AAB, signing
  identity; qualify first releases, stage tracks, submit, roll out, deliver an
  optional purchase catalog, recover, and prove Store installation. Excludes
  app development, fabricated declarations/testers, and unapproved release.
---

# Google Play Delivery

Use this skill when the destination is Google Play. Read the
[shared control contract](../../references/delivery-control-contract.md) and
the [Google Play delivery reference](../../references/google-play-delivery.md)
before acting. This lane begins with an existing Android release candidate; it
does not design, implement, or debug application features.

## Deliver

1. Name the requested effect: prepare a draft, distribute to a test track,
   submit for review, release to production, change a staged rollout, or recover
   an existing delivery. Treat purchase catalogs, Internal App Sharing,
   preregistration, and unpublishing as optional, separately scoped effects.
   Bind the exact developer account, application record,
   `packageName`, track, countries, release mode, and current Play Console state.
2. Inspect the app dashboard, Publishing overview, App content, Policy status,
   App integrity, and active releases before writing. Discover account-specific
   developer verification/package registration, target API by form factor,
   native 16KB compatibility, applicable Billing Library policy, and actual
   production-access/tester prerequisites. Build the reference's dated readiness
   matrix; elapsed testing time is not a production-access approval.
3. Bind one release candidate by source revision, `versionCode`, version name,
   AAB path, byte size, SHA-256, upload-certificate fingerprint, and the distinct
   Play app-signing certificate fingerprint. Reuse the bound, tested artifact
   and version for promotion or unchanged-binary delivery while its proof remains
   applicable. Build only when needed with the project's release task, then run
   relevant `bundletool` validation and local generated-APK install smoke before
   upload. Check transitive native libraries when present; local
   alignment, a 16KB runtime test, and a later Play-distributed install are
   separate evidence. Preserve release-matched mapping/symbol files when used.
4. Prefer an already working project-native release path. Use Gradle Play
   Publisher, fastlane, or EAS only when the project already owns it or the user
   explicitly chooses that dependency or cloud boundary. Otherwise use the
   Android Publisher API for supported repeatable operations and official Play
   Console UI for record creation, first-release bootstrap, declarations, and
   gaps in API coverage. Bind explicit artifact/track/status parameters and
   inspect defaults: a tool's validation or read command may still open an edit
   or upload data. Never resolve an artifact conflict by silently renumbering it.
5. Reconcile the listing and every required App content answer against observed
   product behavior: Data safety, privacy policy, ads, target audience, app
   access, account deletion, content rating, permissions, and any live dashboard
   requirement. Prove a reusable reviewer path to restricted features. For a
   requested purchase catalog, bind product/plan/offer identities and sandbox
   entitlement proof; track enrollment alone does not prevent real charges.
   Ask the user to attest only facts the agent cannot observe. Never invent an
   answer, reviewer credential, legal declaration, or tester participation.
6. Stage the least-public useful route: internal, closed, open, then production
   as eligibility and requested effect require; this is not a mandatory ladder.
   Resolve actual track IDs and competing eligible version codes. For API writes,
   coordinate one edit owner, create one edit,
   add the exact artifact and intended mutations, validate it, show the resulting
   target diff, then commit once with review-safe behavior. Treat an ambiguous
   response as unknown and reconcile before retrying. Preserve retained releases
   and untouched metadata. Catalog and Data safety writes are outside this edit.
   Remember that internal testing ignores country targeting and that other
   tracks use Play-account country semantics; prove the intended audience with
   an eligible account.
7. Before an effect that submits changes for review, publishes approved changes,
   expands visibility, changes price/countries, or alters a rollout, present one
   exact preview: account, package, artifact hash, `versionCode`, track,
   audience, countries, percentage, review behavior, and release timing. Use the
   shared authority contract to decide whether current authorization is already
   exact or an explicit approval is required.
8. Follow external state without collapsing it: uploaded, processing, staged,
   sent for review, in review, approved, ready to publish, serving, and verified.
   Use fresh, version-specific health evidence before expanding a rollout.
   On rejection or timeout, read Play Console and the current edit/release first;
   do not create a duplicate app, upload, edit, or production release.
9. Finish only with evidence matching the requested effect. Public delivery
   requires the canonical public listing, the expected live `versionCode`, and a
   clean Google Play install/update-and-launch smoke on an eligible device or a
   precise statement of the still-external review or propagation blocker.
   Internal App Sharing is separate QA distribution; remote app recovery is a
   user update prompt, not proof that every targeted device updated.

## Boundaries

- Package names, version codes, signing identities, tracks, and artifact hashes
  are immutable delivery evidence. Similar display names are not identity.
- Keep upload keys, service-account material, OAuth credentials, reviewer
  credentials, and recovery material out of chat, commands, logs, receipts, and
  repository files. Use the shared approval and protected credential contract.
- Do not create, rotate, export, or replace a signing key as a routine repair.
  Losing an upload key and losing the app-signing key are different incidents.
- Managed publishing is not first-publication staging. Verify whether the app is
  already eligible, and distinguish approval from the explicit publish action.
- A free app cannot become paid after publication. Bind the first free/paid
  choice and payments-profile readiness before creating the public record; do
  not promise a later price toggle.
- A successful API call, uploaded AAB, approved review, or visible listing alone
  is not proof that the intended build is installable by the intended users.
