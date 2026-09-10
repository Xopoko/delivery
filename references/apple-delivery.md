# Apple Delivery Runbook

This runbook turns a release intention into a resumable, evidence-bound Apple
delivery. It does not teach app implementation. Apple compilation, signing,
App Store Connect operations, TestFlight operations, and notarization mechanics
belong to the project's Apple toolchain; Delivery owns target selection,
cross-step state, authority, recovery, and proof on the user-visible surface.
An installed specialist may help, but is not required. Inspect the selected
workflow and live tool help before acting rather than copying stale syntax.

## Capability Evidence

These runbooks provide source-backed guidance, not a bundled provider
integration or certification of every Apple channel. Local helper tests do not
prove account access, signing, App Review, notarization, or a successful install.
Report the exact provider and user-surface evidence obtained in each delivery;
do not inherit a success claim from this reference.

## 1. Select One Delivery Contract

Do not begin by choosing a command. First name one channel and one terminal
effect.

| Channel | Release artifact | Apple path | Possible terminal effects |
| --- | --- | --- | --- |
| `ios_app_store` | Exported App Store IPA | App Store Connect build, optional TestFlight, App Review, App Store | internal test, external test, submitted, approved, released, public and installable |
| `mac_app_store` | Exported Mac App Store PKG | App Store Connect build, optional TestFlight, App Review, Mac App Store | internal test, external test, submitted, approved, released, public and installable |
| `mac_direct_notarized` | Developer ID signed ZIP, DMG, or flat PKG | Apple notary service, stapling, Gatekeeper, owner-selected distribution endpoint | notarized, distributable, released at endpoint, public and downloadable |

Ask for a target choice only when repository and provider state cannot resolve
it. A macOS target with an existing Mac App Store record does not prove that
Store distribution is intended; a Developer ID identity does not prove direct
distribution is intended. The channels use different signing, entitlements,
release surfaces, and user expectations.

For a Store product, also bind the runtime/platform shape explicitly:
`native_ios_ipados`, `ios_on_mac` on Apple silicon, `mac_catalyst`, or
`native_macos`. These can share product records or purchase relationships while
still having different binaries, entitlements, screenshots, availability and
user proof. Do not treat “runs on Mac” as evidence of a Mac App Store target.
When the requested audience is organizational or link-only, bind standard
public, unlisted, or Custom App distribution instead of silently publishing to
the public catalog; Custom Apps also require the exact organization path.

The desired effect is the smallest externally meaningful terminal state:

- `prepare`: produce and inspect a bound release artifact without external
  submission;
- `test`: make that exact artifact available to the named TestFlight audience;
- `submit`: send the selected version to App Review or the direct artifact to
  the notary service, without claiming release;
- `release`: perform the selected Store release or publish the direct artifact
  to the selected endpoint;
- `verify_public`: prove anonymous discovery/download and installation or
  launch on the intended user surface.

In the shared receipt, map `test` to normalized `stage` and `verify_public` to
`verify`; the other Apple effects keep their names. Preserve the Apple term in
provider status/evidence.

If the user says only "ship" or "publish," reconstruct the likely destination
from the project and existing provider state, then show the exact final effect
before its first consequential transition.

## 2. Ownership And Skill Routing

Use the narrowest existing workflow that can resolve the current step. Optional
specialist skills may wrap these tools, but no named companion plugin is
required. Validate current command help and the linked official contract.

| Need | Project-native or official execution route |
| --- | --- |
| Broad Store release and readiness | Existing release lane plus this runbook |
| Validate, stage, submit, monitor, cancel, or repair | App Store Connect API or official UI; existing release automation |
| Account, schema, and object IDs | App Store Connect API or official UI with protected authentication |
| App record bootstrap | Official App Store Connect UI where required |
| Bundle resources, capabilities, certificates, and profiles | Xcode signing tools and Apple developer account UI |
| Version/build, archive, export, IPA/PKG upload | Existing Xcode/Xcode Cloud/fastlane lane; Xcode Organizer or supported uploader |
| Processing state and live next build | App Store Connect API or official UI |
| TestFlight groups, testers, distribution, and notes | App Store Connect API or TestFlight UI |
| Metadata, localization, screenshots, pricing, subscriptions, privacy readiness | Supported App Store Connect API operations or official UI |
| Direct Mac signature, entitlements, trust | `codesign`, `spctl`, and the current Apple signing documentation |
| Direct Mac packaging and notarization readiness | Project packaging workflow and Apple distribution documentation |
| Notary submit/status/log/staple | `xcrun notarytool` and `xcrun stapler` where supported |

Use project-owned Fastlane, Xcode Cloud, or another release lane if it is
already the source of truth and remains healthy. Do not introduce it by default
or split responsibility between two automation systems. If a project-native
lane and an optional specialist disagree, inspect the actual artifact and provider
state, choose one executor, and record why.

## 3. Build A Release Identity Before Mutating State

Keep one compact delivery capsule for work that spans uploads, review, or a
later session. It is a locator, not a second source of truth. Store no secret,
cookie, token, private key, certificate payload, provisioning profile contents,
review-account password, or personal tester data.

Record these nonsecret fields when applicable:

- delivery channel and desired terminal effect;
- source repository and immutable source revision, plus whether the worktree
  contained intentional uncommitted release changes;
- execution Mac and transport capability, without credentials;
- Apple team ID and selected nonsecret account/team label;
- App Store Connect app ID, bundle ID, platform, version record ID, semantic
  version, and build number;
- private task-local archive/export locators plus a portable artifact filename,
  byte size, SHA-256, and the time the hash was computed; do not copy private
  absolute paths into a durable receipt or committed handoff;
- bundle ID, version, build, supported platform, minimum OS, and signing facts
  read from the exported artifact rather than inferred only from project files;
- App Store Connect delivery/build ID and provider build state;
- TestFlight group/build relationship and beta-review state, but not tester
  emails;
- review submission ID, item/version status, release mode, territories,
  pricing decision, schedule, and last provider observation time;
- for direct macOS: Developer ID certificate kind and public fingerprint, notary
  submission ID, notary status, stapling result, Gatekeeper result, container
  hash, distribution URL, and downloaded hash;
- evidence URLs or local receipts needed to resume, with any signed or
  credential-bearing query parameters removed.

The release tuple is immutable after upload:

`channel + team + bundle_id + platform + version + build + artifact_sha256`

If the artifact changes by even one byte, create a new tuple. A local rebuild,
re-export, re-sign, repackage, or metadata change that is embedded in the
binary invalidates the old hash and all preflight evidence tied to it. Never
describe a later artifact using an earlier upload receipt.

Resolve the next build number from live App Store Connect state immediately
before editing the project. A locally guessed increment is not sufficient.

## 4. Reconcile Before Creating Or Retrying

Start every new or resumed attempt with read-only observation.

1. Inspect the current Git revision, release configuration, workspace/project,
   scheme, bundle ID, version/build settings, entitlements, existing exported
   artifacts, and project-owned delivery notes or automation.
2. Confirm the actual Mac execution locus and installed Xcode/CLI capabilities.
   Do not retry Apple-only tools on Windows or Linux.
3. Resolve the selected Apple team, registered identifier, capabilities,
   certificates/profiles or Developer ID identity, and account role. Do not
   mutate signing assets merely because automatic discovery was incomplete.
   If entitlements/capabilities changed, re-read identifier state and regenerate
   or validate every affected provisioning profile. Managed capabilities may
   require Apple approval; an old profile is not proof that the new binary is
   authorized.
4. Read existing App Store app/version/build/submission/TestFlight state or
   existing notary submissions. Match candidates against the full release
   tuple and timestamps.
5. Check account-level blockers such as agreements, role limitations, and
   commerce setup without pretending those observations authorize acceptance.
6. Reconcile any saved capsule with the provider. Append the new observation;
   do not overwrite history to make an interrupted run appear clean.

If an upload or submit operation timed out, assume `unknown`, not failed.
Search by app, bundle ID, version/build, artifact/delivery ID, notary submission
ID, and time window. Retry only after the live state proves that no equivalent
operation exists or that Apple marked it terminally failed.

Never automatically recreate an app record, version, TestFlight group,
submission, certificate, provisioning profile, or notary request after an
ambiguous result. Never revoke or delete an old signing asset as a discovery
technique.

## 5. Inspect The Artifact That Will Actually Ship

The Xcode project is evidence about intent; the final export is evidence about
delivery. Inspect both the archive and exported artifact before upload.

### Archive

Confirm the archive is the expected release configuration and contains the
expected app, bundle ID, marketing version, build number, platform, signing
team, entitlements, embedded extensions/helpers, debug-symbol disposition, and
archive timestamp. A successful archive is not an export and cannot be bound
to an upload until the export is inspected.

### iOS IPA

Inspect the app inside the IPA payload and verify:

- bundle ID, version, build number, supported platforms, minimum OS, and device
  families;
- distribution signing and the entitlements/capabilities of the app and every
  extension;
- production configuration, privacy manifests where applicable, icons, and
  embedded frameworks/assets expected for release;
- absence of unintended debug-only configuration, local endpoints, or private
  files;
- the final IPA byte size and SHA-256 after export.

Do not print a provisioning profile, certificate, or entitlement payload into
the delivery report. Record only the nonsecret findings required to identify
the artifact and explain readiness.

### Mac App Store PKG

Inspect the exported package and its contained app rather than trusting the
`.pkg` filename. Verify package and bundle identifiers, version/build,
distribution signature, App Sandbox and required entitlements, nested code,
minimum macOS version, package payload, and final SHA-256. Keep the Mac App
Store path separate from Developer ID notarization; Store submission already
has its own Apple security and review path.

### Direct Mac Container

Inspect the `.app` and every nested executable before creating the ZIP, DMG, or
flat PKG used for submission. Verify the intended Developer ID identity, secure
timestamp, hardened runtime, entitlements, nested signatures, package signature
where applicable, and submission-container hash. Bind the exact signed payload
inside that container. Some supported submission containers cannot themselves
carry a stapled ticket, so keep the submission-container hash and final
user-facing-container hash separate. Re-signing or changing the signed payload
requires a new notarization decision; a post-acceptance staple/repackage still
requires a new hash and full final-artifact validation.

Use the selected Apple toolchain inspectors and uploader to produce this
evidence. This runbook deliberately contains no parallel archive, code-signing,
upload, or notarization command recipes.

## 6. iOS App Store Flow

### Observe And Prepare

1. Resolve the app record, team, bundle ID, version, existing builds,
   TestFlight state, version/submission state, availability, and release mode.
2. Resolve the live next build number and bind it to the release revision.
3. Use existing healthy signing first. If signing setup is genuinely missing,
   use the project's Xcode signing workflow and official Apple developer account
   UI under the credential rules below. An installed signing specialist is
   optional; verify it is available before routing to it.
4. Run the project-owned release tests and user-path smoke needed for this
   product. Delivery does not invent a generic test suite or fix unrelated app
   architecture.
5. Archive, export, inspect, and hash the IPA using the focused owners.

### Upload And Processing

1. Validate and upload the exact bound IPA. Capture the returned delivery/build
   identifier and timestamp before waiting.
2. Preserve these as separate facts:
   `uploaded` -> `processing` -> Apple build status `VALID`.
3. A transport success proves only receipt. A build that appears in App Store
   Connect but is still processing is not ready for TestFlight or App Review.
4. If processing fails, read Apple's diagnostics and repair the smallest owning
   surface. If polling times out, reconcile later by provider ID and release
   tuple; do not upload a duplicate.

### TestFlight

TestFlight is an optional delivery surface, not a mandatory ceremony. Use it
when the requested effect is beta delivery or when a real installation is the
cheapest meaningful release discriminator.

1. Bind the `VALID` build to the intended internal or external group and add
   truthful What to Test information.
2. Keep internal availability, external beta-review submission, beta approval,
   tester notification, and tester installation as separate states.
3. Treat external beta review as an Apple review boundary. Never fabricate
   tester identities, consent, or test results.
4. Prove test delivery by the selected build being available to the intended
   group and, when in scope, by installation and launch on a real target device.
5. TestFlight builds expire after 90 days. Bind the provider expiry rather than
   promising durable beta access. An `Internal Only` build cannot be promoted
   to external testing or App Review; expiring/stopping a build changes tester
   availability and is a separate deliberate effect.

### Review Readiness And Submission

Before staging, reconcile the selected build and validate the complete version:

- localized listing metadata and screenshots/previews;
- support, privacy, and other required public URLs as actually served;
- app privacy responses against the shipped binary and integrated SDKs;
- content rights, export compliance, age rating, audience, and review details;
- pricing, territories, availability, subscriptions/IAP, and other review items
  relevant to the product;
- release mode: manual, automatic after approval, or automatic no earlier than
  the selected date.

For a first in-app purchase or subscription, do not stop at the word
“subscriptions.” Bind the product/group IDs, type/duration, localization,
pricing/territories, tax category, availability, review screenshot, version or
submission relationship and current item states. Prove the purchase graph in
Sandbox, then TestFlight when appropriate, and preserve production availability
as a separate result. The first item of each IAP type (consumable,
non-consumable, auto-renewable subscription, or non-renewing subscription) must
accompany a new app version. Each new subscription group needs at least one of
its subscriptions; put the version, group, and items being reviewed together in
the same draft submission. Removal, price/territory changes and subscription
group changes can affect existing customers and require an exact preview; never infer
that deleting a draft cancels an active customer entitlement.

Resolve readiness from the bound artifact, declarations, and current App Store
Connect state, then use the selected release workflow. `Ready for Review`
means staged in a draft submission; it does not mean sent to App Review.

Before the first transition that sends the exact version to review, present the
final preview described in section 10. Then preserve:

`staged` -> `submitted` -> `waiting_for_review` -> `in_review` ->
`approved` or `rejected/unresolved_issues`.

On rejection, read the exact rejected item and reviewer message. Decide whether
the repair is metadata-only, requires a new binary/build, needs a factual owner
answer, or should be appealed. Do not rebuild by reflex and do not silently
change claims. Reconcile the existing submission before resubmitting.

### Release And Public Proof

Approval is not release. Respect the previewed release mode:

- manual release remains pending until the authorized release action;
- automatic release can still be waiting on Apple processing or the selected
  earliest date;
- release can precede storefront propagation.

For a phased release, bind `active`, `paused`, `resumed`, and `completed`
separately and read the current percentage/day from Apple. Pause is the first
safe response to a bad rollout when available. Apple does not roll an App Store
binary back to a prior version: repair requires a new version/build, while
removing availability affects acquisition rather than downgrading installed
users. Do not call either operation rollback.

After release, verify the canonical App Store page anonymously for each
intended storefront that materially matters. Confirm app identity, version,
seller, screenshots/listing, availability, and install action. When the desired
effect is end-user delivery, install the Store build and launch the critical
user path on a supported physical device. Only then record `public_verified`.

## 7. Mac App Store Flow

Use the iOS App Store control loop with platform `MAC_OS`, but do not reuse iOS
artifact or signing assumptions.

1. Confirm that Mac App Store distribution, App Sandbox/capabilities, and the
   selected Mac App Store app record are actually intended.
2. Resolve the live version/build and Store signing state, archive the macOS
   target, export the Mac App Store PKG, inspect its contained app and package,
   and bind the final hash.
3. Upload and keep `uploaded`, `processing`, and Apple build `VALID` distinct.
4. Use macOS TestFlight only when beta delivery is part of the desired effect;
   keep beta review and tester installation separate from App Review.
5. Validate macOS-specific listing, screenshots, privacy, entitlements,
   availability, review instructions, and any privileged behavior the reviewer
   must exercise.
6. Stage, preview, submit, monitor, and release through the same explicit
   App Review state model.
7. Prove the public Mac App Store page anonymously, then install and launch the
   Store-delivered app on a supported Mac when user delivery is the terminal
   effect.
8. For iPhone/iPad apps offered on Apple-silicon Macs, verify that availability
   separately from a native Mac or Catalyst binary. Bind universal-purchase and
   platform-record relationships rather than assuming that a shared bundle name
   gives users the intended entitlement.

Do not submit the Mac App Store PKG to the notary service as a substitute for
App Review. Do not sign a Mac App Store artifact with Developer ID merely
because a Developer ID identity exists.

This branch is reference guidance. Preserve exact deviations, failures, and
proof from the live run; the runbook itself does not establish Mac App Store
release or installation evidence.

## 8. Direct Notarized macOS Flow

This branch delivers outside the Mac App Store. It does not create or submit an
App Store version and does not use TestFlight or App Review.

### Prepare And Notarize

1. Name the distribution container and final endpoint before packaging. A
   notarized app with nowhere users can obtain it is not a released product.
2. Inspect existing Developer ID identities before creating anything. Distinguish
   application signing from installer-package signing where the container
   requires both.
3. Use Apple's signing and assessment tools for signature/entitlement diagnosis,
   the project's packaging workflow for artifact readiness, and the supported
   `notarytool`/`stapler` workflow for the notary operation.
4. Bind the signed app and final container hash, submit that exact container,
   and record the notary submission ID before waiting.
5. Keep these states distinct:

   `notary_uploaded` -> `notary_in_progress` -> `notary_accepted` or
   `notary_invalid` -> `ticket_stapled` -> `gatekeeper_verified`.

6. Read the notary log for an invalid result and for material warnings on an
   accepted result. Repair nested signing, hardened runtime, entitlements,
   timestamp, or packaging in the owning surface, then produce a new artifact
   tuple. A timeout is `unknown`; reconcile by submission ID before retrying.
7. Staple only an accepted ticket to a supported artifact carrying the matching
   signed payload, then verify the final distributable. If the submission
   container cannot be stapled directly, staple the supported inner artifact
   and repackage without changing its signed payload. In either case, compute
   the final user-facing container hash after the transformation.

### Publish And Prove

Publishing to a website, update feed, package host, or other endpoint is a
separate external effect from notarization. Show the endpoint, version, final
hash, visibility, replacement behavior, and any update-feed consequence in the
final preview.

After upload, retrieve the artifact through the same anonymous path a new user
will use. Verify the downloaded hash, Gatekeeper assessment in a realistic
quarantined-download context, installation or mount behavior, and first launch
on a clean supported Mac. Notary acceptance without this path is
`gatekeeper_verified` at most, never `public_verified`.

This branch does not design hosting, an updater, pricing, or a marketing site.
If the product lacks a distribution endpoint, report that precise adjacent
dependency and stop at a correctly notarized artifact unless the current task
also authorizes the endpoint work.

This branch is reference guidance. Preserve the live run's nonsensitive command
details, errors, artifact hashes, provider IDs, and user-path proof. Notarization
guidance alone does not establish a downloadable, trusted, working application.

## 9. Recovery By Failure Class

Always read current state before applying a recovery. The table names the first
discriminator, not an automatic fix.

| Symptom | First discriminator | Recovery boundary |
| --- | --- | --- |
| Wrong app/team or record not found | Compare selected team, app ID, bundle ID, role, and visible account | Switch to the correct existing context; do not create a duplicate record |
| Build number rejected as already used | Read live builds and next build number for the exact version/platform | Increment, rebuild, re-export, inspect, and bind a new hash |
| Upload returned no terminal response | Query deliveries/builds by tuple, provider ID, and time | Resume observation; retry only when absence or terminal failure is proven |
| Upload processed as failed/invalid | Read Apple delivery/build diagnostics | Repair the named binary, signing, metadata, or toolchain issue and create a new tuple |
| Build remains processing | Re-read provider state and notifications after a bounded wait | Hand off `processing`; do not duplicate the upload |
| Build is `VALID` but cannot be selected | Check version/platform, export compliance, active submissions, and required processing | Repair the exact relationship or compliance blocker |
| Signing/profile mismatch | Inspect exported app, entitlements, capabilities, selected team, certificate, and profile | Use signing owner; create/rotate only after credential-storage checkpoint |
| Capability changed after a profile was created | Compare identifier capability approval, entitlements, and embedded profiles for every target | Regenerate or obtain approval for affected profiles; do not remove the entitlement or rotate certificates by reflex |
| App record/bootstrap field unavailable via API | Confirm official UI and current account role | Use visible official UI with protected sign-in; no selector-loop retries |
| Agreement, tax, banking, privacy, export, rights, rating, or review fact blocks progress | Identify the exact missing attestation and accountable role | Host approval surface and official UI; never infer or fabricate |
| TestFlight external build is unavailable | Read group linkage, beta information, beta-review, and notification state | Repair only the missing TestFlight state; do not submit App Review by accident |
| App Review rejected or has unresolved issues | Read rejected item and reviewer message; classify metadata versus binary | Make the smallest truthful repair; new binary only when required |
| Approved version is not public | Read release mode, pending developer release, schedule, availability, and propagation state | Perform only the authorized release action, then wait/recheck storefront |
| Phased release has a severe defect | Read current phased state, day, percentage, and installed-user impact | Pause when available and prepare a new fixed version; Apple binary rollback does not exist |
| Storefront page is public but wrong version or cannot install | Compare storefront region, version, phased/availability state, and supported device | Treat as not publicly verified; repair availability or propagation evidence |
| Notary result is invalid | Read the notary log and inspect nested signatures/runtime/entitlements/timestamp | Repair package/signing, create new hash, and submit a new request |
| Notary accepted but stapling fails | Confirm submission ID, artifact identity, supported staple target, and network | Retry stapling only against the same accepted artifact; do not resubmit first |
| Gatekeeper rejects an accepted artifact | Inspect the exact downloaded artifact and its signature/ticket/quarantine state | Diagnose signing or packaging; notary acceptance alone is insufficient |
| Final artifact differs from receipt | Recompute hashes and compare archive/export/upload/download stages | Invalidate the receipt; rebind and repeat only the affected downstream proof |

After two equivalent failures with no new evidence or state change, change the
discriminator or report the blocker. Do not continue polling, clicking, or
re-uploading as a substitute for understanding the state.

## 10. Authority, Approval, And Credential Custody

### Routine Work

Within the exact delivery request, read-only discovery, local release builds,
artifact inspection, validation, draft preparation, and private/internal
staging may proceed when the shared control contract authorizes them. An
existing explicit instruction to submit or release the exact target can satisfy
the corresponding action checkpoint; do not ask twice merely because the work
crossed sessions.

### Final Preview

Before the first consequential transition not already exactly authorized,
present one compact preview containing:

- channel and intended state transition;
- team ID, App Store app ID where applicable, bundle ID, platform, version, and
  build;
- final artifact path, size, SHA-256, source revision, and validation result;
- TestFlight audience or App Review submission items;
- listing/metadata differences, privacy/legal/compliance attestations still
  owned by the user, territories, price, release mode, and schedule;
- for direct macOS, Developer ID kind/fingerprint, notary status, final
  container, endpoint, visibility, and replacement/update consequence;
- what the provider will do immediately and what remains asynchronous.

Use the host's approval surface for a material review/approval, legal or factual
attestation, final submit/release/schedule/publication, cancellation, record
deletion, certificate revocation, or another destructive external action.

### Protected Identity And Secrets

Try public/anonymous evidence first. Reuse an already authenticated official
UI session when safe. When protected access is required, follow the shared
control contract and the host's protected credential workflow:

- use nonsensitive credential-broker status only to learn whether a suitable
  credential may be available; availability does not prove validity or
  authorize use;
- use an authorized credential broker that does not expose values to the model,
  or hand the official provider UI to the user with observation and capture
  stopped while they handle secrets;
- before creating, rotating, recovering, or first revealing a durable API key,
  distribution certificate/private key, installer identity, or other reusable
  secret, confirm its approved storage destination before secret bytes exist;
- create and store durable material directly through official UI or a verified
  closed provider-to-secret-store sink. If no such sink exists, stop before
  creation and hand the official UI custody step to the user;
- keep `.p8`, `.p12`, private keys, passwords, API tokens, session cookies,
  2FA/OTP values, recovery material, and reviewer-account passwords out of
  model-visible input/output, shell output, browser capture, receipts, Git, and
  ordinary environment examples.

Pause screen capture before the user handles secrets. A completed approval
proves only permission for the named protected channel; it does not prove login,
credential validity, agreement acceptance, or secret storage.

Human-owned facts include developer agreement acceptance, organization and tax
identity, banking/commerce setup, content rights, age rating, encryption/export
answers, privacy/data collection claims, tracking behavior, review demo-account
facts, and claims about regulated or restricted features. The agent may collect
evidence and prepare a draft but must not attest on the user's behalf.

## 11. State Model And Completion Proof

Use provider-native names in evidence and these normalized states only as a
cross-session summary.

### App Store Channels

`observed` -> `artifact_bound` -> `uploaded` -> `processing` -> `valid` ->
optional `testflight_internal` / `testflight_beta_review` /
`testflight_external` -> `staged` -> `submitted` -> `waiting_for_review` ->
`in_review` -> `approved` -> `released` -> `public_verified`

Terminal alternatives include `invalid`, `rejected`, `unresolved_issues`,
`cancelled`, and `blocked`. `unknown` is a recoverable observation state, not a
provider result.

### Direct macOS

`observed` -> `artifact_bound` -> `signed` -> `packaged` ->
`notary_uploaded` -> `notary_in_progress` -> `notary_accepted` ->
`ticket_stapled` -> `gatekeeper_verified` -> `distribution_released` ->
`public_verified`

Terminal alternatives include `notary_invalid`, `gatekeeper_rejected`,
`cancelled`, and `blocked`.

Every report must say which state was freshly observed, on which surface, and
at what time. Never translate these into a stronger claim:

- archive success is not export success;
- upload receipt is not processing completion;
- Apple build `VALID` is not TestFlight or App Review readiness;
- TestFlight availability is not App Store submission;
- `Ready for Review` is not submitted;
- submission is not review approval;
- approval is not release;
- release is not storefront propagation;
- storefront visibility is not successful install/launch;
- notarization acceptance is not stapling or Gatekeeper acceptance;
- Gatekeeper acceptance is not a public downloadable release.

### Required Evidence By Terminal Effect

| Claimed effect | Minimum proof |
| --- | --- |
| Prepared | final artifact inspection, source revision, version/build, team/bundle target, size, SHA-256 |
| Uploaded | provider delivery/build or notary submission ID tied to the release tuple |
| TestFlight delivered | provider build/group state and, when requested, installation/launch of that build |
| Submitted | review submission/version ID and freshly observed submitted/waiting/in-review state |
| Approved | freshly observed accepted/approved state for every required submission item |
| Store released | release mode completed and Apple provider state reports release/ready-for-distribution |
| App Store public | anonymous intended-region product page shows the expected identity/version and a Store install/launch succeeds when in scope |
| Direct Mac notarized | accepted submission, matching ticket/staple proof, final hash, and Gatekeeper acceptance |
| Direct Mac public | anonymous fresh download, matching hash, Gatekeeper acceptance, install/mount, and first launch from the intended endpoint |

If Apple review or storefront propagation remains asynchronous, finish with an
exact resumable handoff: release tuple, provider IDs, last observed state/time,
next read-only discriminator, authorized future effect, and the condition that
would require a new decision. Do not call the product delivered early.

## 12. Official Apple Sources

These primary sources were checked on 2026-08-24. Apple changes upload,
submission, screenshot, privacy, review, role, and tool requirements; re-open
the relevant source before each live release instead of freezing values from
this runbook.

The first-IAP-type and new-subscription-group submission requirements were
rechecked against Apple's submission guidance on **2026-09-10**.

- [Distributing your app for beta testing and releases](https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases)
- [Upload builds](https://developer.apple.com/help/app-store-connect/manage-builds/upload-builds/)
- [Build upload statuses](https://developer.apple.com/help/app-store-connect/reference/app-uploads/build-upload-statuses/)
- [View builds and metadata](https://developer.apple.com/help/app-store-connect/manage-builds/view-builds-and-metadata/)
- [Choose a build to submit](https://developer.apple.com/help/app-store-connect/manage-builds/choose-a-build-to-submit/)
- [TestFlight overview](https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview/)
- [Add internal testers](https://developer.apple.com/help/app-store-connect/test-a-beta-version/add-internal-testers/)
- [Stop testing a build](https://developer.apple.com/help/app-store-connect/test-a-beta-version/stop-testing-a-build/)
- [Invite external testers](https://developer.apple.com/help/app-store-connect/test-a-beta-version/invite-external-testers/)
- [Overview of submitting for review](https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/overview-of-submitting-for-review/)
- [Submit an app](https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/submit-an-app/)
- [App and submission statuses](https://developer.apple.com/help/app-store-connect/reference/app-information/app-and-submission-statuses/)
- [Manage a submission with unresolved issues](https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/manage-a-submission-with-unresolved-issues/)
- [Select an App Store version release option](https://developer.apple.com/help/app-store-connect/manage-your-apps-availability/select-an-app-store-version-release-option/)
- [Release a version update in phases](https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases/)
- [Create a new version](https://developer.apple.com/help/app-store-connect/update-your-app/create-a-new-version/)
- [Manage app availability](https://developer.apple.com/help/app-store-connect/manage-your-apps-availability/manage-availability-for-your-app-on-the-app-store/)
- [Remove an app](https://developer.apple.com/help/app-store-connect/create-an-app-record/remove-an-app/)
- [Submit an in-app purchase](https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/submit-an-in-app-purchase/)
- [Configure in-app purchases](https://developer.apple.com/help/app-store-connect/configure-in-app-purchase-settings/overview-for-configuring-in-app-purchases/)
- [Add platforms to an app record](https://developer.apple.com/help/app-store-connect/create-an-app-record/add-platforms/)
- [iPhone and iPad app availability on Apple-silicon Macs](https://developer.apple.com/help/app-store-connect/manage-your-apps-availability/manage-availability-of-iphone-and-ipad-apps-on-macs-with-apple-silicon/)
- [Custom App distribution](https://developer.apple.com/custom-apps/)
- [Unlisted app distribution](https://developer.apple.com/support/unlisted-app-distribution/)
- [Manage app privacy](https://developer.apple.com/help/app-store-connect/manage-app-information/manage-app-privacy/)
- [Certificates overview](https://developer.apple.com/help/account/certificates/certificates-overview/)
- [Enable app capabilities](https://developer.apple.com/help/account/identifiers/enable-app-capabilities/)
- [Provisioning with managed capabilities](https://developer.apple.com/help/account/reference/provisioning-with-managed-capabilities/)
- [Developer ID certificates](https://developer.apple.com/help/account/certificates/create-developer-id-certificates/)
- [Notarizing macOS software before distribution](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution)
- [Customizing the notarization workflow](https://developer.apple.com/documentation/security/customizing-the-notarization-workflow)

When official documentation and live provider behavior disagree, preserve the
exact contradiction, prefer the provider's current safe/read-only reality for
the immediate handoff, and route the capability mismatch for repair after the
user outcome is protected.
