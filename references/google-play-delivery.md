# Google Play Delivery Contract

This reference governs the last mile from an existing Android release candidate
to an observable Google Play result. It intentionally does not teach Android
architecture, feature development, marketing, or store-ranking work. This
official-source guidance is not proof of a successful Play publication. Reconcile
it with current provider state and record the live delivery evidence separately.

## Completion Is An External State

Choose one requested effect before changing Play state:

| Effect | Minimum evidence |
| --- | --- |
| `draft` | Exact app and release exist in Play Console, bound to an AAB hash and not sent for review |
| `test` | Exact release is serving on the named internal, closed, or open track and an eligible tester can install it |
| `submit` | Play shows the intended changes sent for review with a captured submission/release identity |
| `release` | The intended release is serving in production for the requested countries and rollout scope |
| `verify` | Anonymous listing plus clean Play install/update and launch prove the expected public build |

Keep provider phases separate. A useful normalized sequence is:

`observed -> prepared -> uploaded -> processing -> staged -> submitted -> in_review -> approved -> ready_to_publish -> serving -> verified`

`rejected`, `failed`, and `blocked` are terminal observations until a new fact or
new artifact changes the state. Play Console wording is canonical; normalized
labels are only a durable summary. An HTTP timeout, missing UI refresh, or stale
local receipt is `unknown`, never permission to retry a write.

For the shared receipt, map Google `draft` and `test` to normalized `stage`;
`submit`, `release`, and `verify` retain their names. Preserve the exact track
and Play wording in channel/status evidence.

## Bind Identity Before Action

Create a private delivery receipt that contains no credentials and binds:

- developer-account identity and account type as a non-secret label;
- Play application ID/console URL and immutable `packageName`;
- source repository and exact revision;
- release variant, `versionCode`, version name, portable AAB filename or private
  task-local locator, bytes, and SHA-256;
- upload-certificate SHA-256 fingerprint;
- Play app-signing certificate SHA-256 fingerprint;
- requested track, tester audience, countries, rollout percentage, pricing,
  managed-publishing state, and desired effect;
- existing edit, release, review, rejection, or ready-to-publish state;
- tool and credential channel selected, without secret paths or values.

The display title is not an application identity. The local certificate that
signs the uploaded AAB is not necessarily the certificate on APKs users install.
Never overwrite a prior receipt when the artifact changes: record a new hash and
explicitly invalidate the old candidate.

## Observe The Live Console

Before any mutation, read these surfaces where available:

1. Home/Dashboard for incomplete setup and account-specific eligibility gates.
2. Publishing overview for changes not sent, changes in review, and changes
   ready to publish.
3. Latest releases/App bundle explorer for active `versionCode`, retained
   artifacts, delivery status, and Play-generated APK details.
4. App integrity for Play App Signing enrollment and both public certificate
   fingerprints.
5. Testing and Production for tracks, countries, tester configuration, active
   staged rollouts, and outstanding releases.
6. Policy status and App content for declarations, deadlines, warnings,
   rejections, and reviewer-access needs.
7. Store presence and monetization for listing state, contact/privacy URLs,
   price, and country availability.

Requirements change and may differ by developer account, app category, country,
form factor, permissions, and account history. Treat the current dashboard and
current official help as evidence. Do not freeze tester counts, waiting periods,
target API levels, asset dimensions, or review timing in automation or guidance.
Resolve the current target-API requirement immediately before the release and
fail closed when the uploaded artifact or declared device surface is below it;
do not rely on a dated number copied into this runbook.

## First App And First Release

Use Play Console UI for the initial application record and every setup or legal
surface the API does not expose. Before creating a record, reconcile by exact
`packageName`; package names are permanent and cannot be reused. Record creation
includes consequential classifications and agreements, so obtain human input or
attestation for app/game type, free/paid choice, contact identity, policy/export
acknowledgements, and Play App Signing terms.

As Android developer verification and package-name registration are rolled out,
read the live account/package status and applicable deadline before creating or
uploading. Play Console ownership, Android developer verification, and package
registration are related but distinct provider states. Do not register a new
package or developer identity merely because an existing app is not visible in
one account context.

Bind free versus paid before first publication. A published free app cannot be
changed into a paid app; charging later requires a new app/package rather than a
price toggle. A paid choice also needs the correct payments-profile readiness.
Price, payments identity and package creation are consequential and must be
previewed together.

Do not assume API access proves that first-app setup is complete. Follow the
live dashboard until it identifies no blocking setup item. Production access and
testing prerequisites are account-specific: record the exact live requirement,
the real tester cohort and dates, and the production-access decision. The agent
may configure an authorized real test, but may not fabricate tester accounts,
opt-ins, participation, feedback, answers, or elapsed time.

Internal, closed, open, and production are distribution audiences, not a fixed
mandatory ladder for every account. Choose the least-public track that proves
the next uncertainty. A first production release differs from an update:

- managed publishing is unavailable for an app's first publication;
- a staged percentage is an update mechanism, not a first-release option;
- review can delay the first fully configured internal release or a release
  after a prior rejection, but production access is not its prerequisite;
- closed testing requires complete app setup. Where a new personal account must
  earn production access through a closed test, that access gates open testing
  and production—not the internal or closed track needed to qualify;
- clicking the first production rollout can make the app available across the
  selected countries after review, so its preview must be treated as a public
  publication decision.

Country targeting has track-specific semantics. Internal testing ignores
country availability; intended testers can receive it from supported locations.
For other tracks, eligibility follows the tester's Play country/account rather
than current physical location, and country changes can synchronize between
tracks according to current Console rules. Bind both track and countries and
verify with an eligible account instead of assuming that one device IP proves
regional availability.

## Artifact And Signing Proof

Use the project's existing release build task, commonly `bundleRelease` or a
variant-specific equivalent. Do not introduce a publication framework merely
to invoke Gradle once. Before upload:

1. Start from a clean, identified revision and run the project-owned release
   checks required by that artifact.
2. Build a signed AAB and calculate SHA-256 and byte size immediately.
3. Inspect its manifest with current Android tools and record `packageName`,
   `versionCode`, version name, minimum/target SDK, delivery modules, and release
   variant. Fail if they do not match the Play record and intended release.
4. Verify the AAB signature and compare the public upload-certificate fingerprint
   with App integrity. Never print keystore passwords or private-key material.
5. Run `bundletool validate` and use `bundletool build-apks`/`install-apks` on a
   representative connected device or emulator for a packaging/install/launch
   smoke. This locally generated APK set does not prove Play's signing or serving.
6. After upload, use App bundle explorer or a test track to inspect and install
   Play-generated delivery artifacts. Confirm the installed package, signing
   certificate, version code, launch behavior, and update compatibility.

Play App Signing separates custody:

- the **upload key** signs the submitted AAB and remains the publisher's secret;
- the **app-signing key** signs Play-generated APKs installed by users and is
  managed according to the app's Play App Signing configuration;
- their public certificates/fingerprints are safe identity evidence, but private
  keys, keystores, passwords, PEPK output, and recovery material are protected.

Before creating, importing, rotating, resetting, or first revealing a durable
key, confirm the approved storage destination and use an official UI or a
verified adapter that sends values directly to that store. Keep durable
credentials there without exposing bytes to the agent. A lost upload
key may have an upload-key reset path; never "repair" it by replacing the app's
signing identity. If multi-store continuity requires one app-signing key, make
that custody choice explicitly before Play App Signing enrollment.

## Listing And App Content Are Product Facts

Reconcile declarations from observed behavior, source/configuration evidence,
SDK inventory, privacy materials, and human attestation. The delivery agent may
assemble evidence and enter approved answers; it may not determine unknown legal
or product facts by optimism. Cover the current console surfaces, including:

- main and localized store listing, icons/graphics/screenshots, category,
  contact and support information;
- served privacy-policy URL and consistency with in-app behavior;
- Data safety for collection, sharing, purpose, handling, deletion, encryption,
  and third-party SDK behavior;
- ads declaration and behavior of included ad SDKs;
- target audience and any resulting families requirements;
- reviewer app access, restrictions, regional/device prerequisites, and working
  test credentials delivered only through an approved protected channel;
- content-rating questionnaire and any category-specific declaration;
- sensitive permissions/APIs, news, health, finance, government, accessibility,
  or other current dashboard modules when applicable.

Never copy declarations from another app, infer "no data collected" from a lack
of a privacy screen, or put reviewer credentials into repository metadata. A
human attestation is evidence of the human's answer, not independent verification
of the underlying fact.

## Choose The Execution Route

Prefer the narrowest route already owned by the project:

1. Existing Gradle Play Publisher, fastlane, or EAS configuration may remain the
   executor when its identity, artifact, credential, and release semantics are
   understood. EAS is a cloud/paid boundary and requires explicit selection when
   not already native to the project.
2. The Android Publisher API is suitable for supported repeatable artifact,
   listing, track, and release operations after the app and API access exist.
3. Official Play Console is the fallback and the normal owner of first-app
   bootstrap, agreements, declarations, production-access applications, and
   any current workflow not faithfully represented by API or project tooling.

Do not install a community MCP or release framework just because delivery is
possible through it. New automation must remove a repeated burden and preserve
the same receipts, preview, credential boundary, and provider-state semantics.

### Protected access

Use anonymous/read-only evidence first. When a signed-in identity is necessary,
follow the shared protected credential contract: use nonsensitive broker status
and an authorized protected channel, or hand official Google sign-in, OAuth
grant, service-account setup, or a credential prompt to the user with capture
stopped. Keep OAuth refresh tokens, client secrets, service-account JSON, signing
keystores, passwords, reviewer credentials, and their private storage paths out
of model-visible output and durable receipts. Use a verified credential broker or
an official provider-owned UI rather than copying secrets into environment examples
or command arguments. Developer-account registration, identity verification,
payments, agreements, policy attestations, and production-access answers remain
human decisions even when the agent can navigate the UI.

## Transactional Android Publisher Edits

An edit is a temporary transaction, not proof of publication. Use this sequence:

1. Read active tracks, artifacts, Publishing overview, and in-review changes.
2. Create exactly one edit for the intended release and record its `editId`.
3. Upload the exact AAB hash and apply only the intended listing/track changes.
4. Read the edit back and compare package, version code, track, status, countries,
   release notes, and rollout fraction with the preview.
5. Call `edits.validate`; validation success does not persist the edit.
6. Commit once only after authorization for the resulting review/publication
   effect, then capture the response and reconcile Publishing overview.

The current commit API's default behavior may cancel changes already in review
and submit the combined change set. Use `changesInReviewBehavior=ERROR_IF_IN_REVIEW`
as the fail-closed default when supported. Select cancellation/resubmission only
after an exact preview of what review is being cancelled and what replaces it.
Use the provider's current `changesNotSentForReview` behavior only in the
documented rejected-app flow, when intentionally staging changes for a later
Console submission, and verify where the changes landed. Never assume `commit`
means "save draft" or "public now."

After any timeout, disconnected browser, 5xx, or ambiguous CLI exit, do not
repeat insert/upload/commit. Read the current application, tracks, edit if still
available, bundle explorer, and Publishing overview. Continue from the observed
provider state or stop with an exact blocker.

## Review, Managed Publishing, And Rollout

Distinguish three controls:

- **Changes not yet sent for review** delay review submission.
- **Review** is Google's external decision and may produce rejection or requests.
- **Managed publishing** holds most approved changes until a separate publish
  action, but is unavailable for first publication and has documented exceptions.

Capture whether managed publishing is on before submission and re-check it
before claiming an approved build is held. Treat "ready to publish" as approved,
not public. The explicit Publish changes action is consequential and requires the
same exact-target preview as production release unless current authorization
already covers it.

Use staged rollouts only for eligible updates. Record starting percentage and
countries, then verify the serving state. Increasing, halting, resuming, or
completing a rollout is a new distribution effect; read crash/ANR signals and
user feedback, preview the exact change, and capture rollout history. A halt
prevents further expansion but does not remove the version from users who
already received it. If the artifact is defective, prefer a new higher
`versionCode` release over attempts to replace the uploaded binary.

## Recovery And Proof

For a rejection, extract the exact policy issue, affected version, evidence,
deadline, and available action. Separate an artifact defect, declaration defect,
account/identity issue, permission issue, tester prerequisite, and review-only
blocker. Correct the narrow owner, produce a new artifact only when binary state
changed, and preserve the rejected submission identity in the receipt.

For completion, prove each requested surface independently:

1. **Provider receipt:** exact `packageName`, `versionCode`, track/release ID,
   countries, rollout scope, and Play state.
2. **Listing:** canonical `play.google.com/store/apps/details?id=<packageName>`
   is anonymously reachable where public visibility was requested, with the
   expected title, publisher, privacy/support links, and current assets.
3. **Distribution:** an eligible account/device can discover and install or
   update the exact track release through Google Play.
4. **Installed identity:** package, version code, and app-signing certificate
   match the receipt; the app launches through the normal user path.
5. **Propagation:** if one region/device has stale Store state, report it as
   propagation evidence and do not relabel approval as universal availability.

When Play produces a pre-launch report, use it as an additional device/crash/
accessibility/security signal tied to the exact uploaded artifact. It is neither
a mandatory ceremony nor a substitute for the real intended-device install and
critical user path.

If external review is still running, a complete handoff names the exact state,
submission/release identity, artifact hash, last observed timestamp, next
provider transition, next read-only discriminator, and the action that would
require human authority. Do not create a polling service unless the user asked
to wait or monitor.

## Official Primary Sources

These links were checked on **2026-08-24**. Re-open the relevant page at delivery
time; Google changes requirements and Console behavior independently of this
plugin.

- [Create and set up an app](https://support.google.com/googleplay/android-developer/answer/9859152)
- [Prepare and roll out a release](https://support.google.com/googleplay/android-developer/answer/9859348)
- [Set up internal, closed, or open testing](https://support.google.com/googleplay/android-developer/answer/9845334)
- [Account-specific personal-account testing requirements](https://support.google.com/googleplay/android-developer/answer/14151465)
- [Android developer verification](https://developer.android.com/developer-verification)
- [Package-name registration in Play Console](https://support.google.com/googleplay/android-developer/answer/16761053)
- [Current Google Play target API requirements](https://developer.android.com/google/play/requirements/target-sdk)
- [Set app pricing and paid-app constraints](https://support.google.com/googleplay/android-developer/answer/6334373)
- [Distribute releases to specific countries](https://support.google.com/googleplay/android-developer/answer/7550024/distribute-app-releases-to-specific-countries)
- [Country availability and Play country](https://support.google.com/googleplay/android-developer/answer/9842757)
- [Control review submission and managed publishing](https://support.google.com/googleplay/android-developer/answer/9859654)
- [Release updates with staged rollouts](https://support.google.com/googleplay/android-developer/answer/6346149)
- [Prepare App content for review](https://support.google.com/googleplay/android-developer/answer/9859455)
- [Data safety declarations](https://support.google.com/googleplay/android-developer/answer/10787469)
- [Android app signing and Play App Signing](https://developer.android.com/studio/publish/app-signing)
- [Android App Bundle and bundletool](https://developer.android.com/tools/bundletool)
- [Android Publisher API](https://developers.google.com/android-publisher/api-ref/rest)
- [`edits.validate`](https://developers.google.com/android-publisher/api-ref/rest/v3/edits/validate)
- [`edits.commit` and review-safe behavior](https://developers.google.com/android-publisher/api-ref/rest/v3/edits/commit)
