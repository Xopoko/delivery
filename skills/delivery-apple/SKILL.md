---
name: delivery-apple
description: >-
  Deliver build-ready iOS or macOS products through App Store, TestFlight, Mac
  App Store, or Developer ID notarization: reconcile state, compose the existing
  Apple toolchain, gate release, and prove the artifact. Excludes implementation.
---

# Apple Delivery

Use this lane when the requested outcome is an Apple release, TestFlight build,
App Review submission, Mac App Store version, or directly distributed notarized
Mac app. Read
[`../../references/delivery-control-contract.md`](../../references/delivery-control-contract.md)
and
[`../../references/apple-delivery.md`](../../references/apple-delivery.md)
before acting.

## Start From Reality

1. Classify the target as `ios_app_store`, `mac_app_store`, or
   `mac_direct_notarized`, and the desired effect as prepare, test, submit,
   release, or public verification. Do not silently substitute one channel for
   another. For Store delivery, also bind native iOS/iPadOS, iOS-on-Mac,
   Catalyst, or native macOS plus public, unlisted, or Custom App distribution.
2. Run Apple toolchain work on the Mac that owns the project and signing state.
   From another host, use an already configured remote Mac transport instead of
   retrying missing Apple tools locally.
3. Reconcile the repository, exported artifacts, Apple account/team, App Store
   Connect or notary state, and any existing submission before changing
   anything. Live provider state outranks a saved handoff.
4. Bind the release to the exact team, bundle ID, platform, version, live next
   build number, artifact path and SHA-256, and provider IDs. Rebind after any
   rebuild, re-export, repackaging, or metadata target change.

## Route The Mechanics

Prefer the project's existing release workflow for Apple-specific mechanics.
An installed Apple specialist is optional; inspect its current contract and
tool help before delegating. This lane owns orchestration and proof.

- For iOS or Mac App Store work, use the existing Xcode, Xcode Cloud, fastlane,
  or App Store Connect workflow for the current blocker: record/ID resolution,
  signing, archive/export/upload, processed-build monitoring, metadata,
  screenshots, TestFlight, review readiness, or release direction.
- For direct macOS distribution, inspect signatures and entitlements with
  Apple's tooling, use the project's packaging workflow, and use `notarytool`
  and `stapler` where supported. Discover exact syntax from the installed
  toolchain and linked Apple documentation.
- Use the official Apple UI for bootstrap and gaps. Do not add a release
  framework, new CI lane, or credential surface merely to complete one delivery.

## Keep States Distinct

Never collapse uploaded, processing, Apple build `VALID`, TestFlight testing,
staged, submitted, in review, approved, released, and publicly visible into
"published." For direct macOS, notarization accepted, ticket stapled to the
supported payload, Gatekeeper accepted, distribution uploaded, and
user-download verified are
also separate facts.

Keep first IAP/subscription item/group/version review, TestFlight 90-day expiry,
and phased-release active/paused/completed state explicit when relevant. Apple
does not provide App Store binary rollback: pause a bad phased release and ship
a new fixed version rather than promising a downgrade.

After a timeout, disconnect, or ambiguous browser result, perform read-only
reconciliation using the bound identifiers before retrying. Never create a new
app record, version, upload, submission, certificate, profile, or notarization
request just because the previous call did not return a terminal response.

## Authority And Secrets

- Prepare drafts, inspect state, build, validate, and stage only within the
  authority in the current task and the shared control contract.
- Before the first consequential review, release, scheduling, public distribution,
  cancellation, or destructive credential action not already authorized for
  the exact target, show one final preview and request approval through the host.
- Route login, 2FA, review credentials, private keys, certificates, API keys,
  and passwords through the host's protected handoff. Before creating,
  rotating, recovering, or first exposing durable credential material, confirm
  the approved storage destination and use an official or verified adapter. The
  model, chat, logs, receipts, environment examples, and repository must never
  receive secret bytes.
- Treat agreements, tax/commerce identity, export answers, privacy claims,
  content rights, age rating, and other attestations as human-owned facts.

## Finish On The User Surface

Report the exact artifact tuple, last observed provider state, submission or
notary identifiers, release choice, evidence timestamp, and remaining blocker.
Success requires the requested terminal surface: a TestFlight installation,
an anonymous intended-region App Store page plus install/launch, or a freshly
downloaded notarized Mac artifact whose hash, Gatekeeper acceptance, and launch
match the bound release. Stop at the precise nonterminal state when Apple
review or propagation is still pending.
