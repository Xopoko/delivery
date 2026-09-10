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
target API levels, asset dimensions, or review timing into universal automation.
Resolve the current target-API requirement immediately before the release and
fail closed when the uploaded artifact or declared device surface is below it;
the dated examples below are lookup aids, not evidence for a particular account.

### Build A Dated Readiness Matrix

Record applicability, observed value, provider requirement, checked date, and
proof/blocker for each row. A Console extension is valid only when actually
granted to this app; a request for one does not change its deadline.

| Gate | Evidence to bind |
| --- | --- |
| First-release eligibility | Account type/creation date, completed setup, real cohort and continuous opt-in period, application for production access, actual decision |
| Target SDK and device surface | Release manifest, phone/Wear/Automotive/TV/XR targets, new/update versus existing-app availability rule, any granted extension |
| Native compatibility | Direct and SDK-provided native libraries, AAB configuration, generated APK and ELF alignment, 16KB runtime result or explicit gap |
| Billing compatibility, if used | Resolved release Billing Library version and applicable submission deadline/extension; a Gradle declaration alone may not describe the shipped dependency |
| Developer/package verification | Developer identity status, package registration, relevant signing identity, affected countries and account-specific deadline |
| Product declarations | Actual features, SDK data flows, review access, deletion paths and current Console-specific forms |

Policy snapshot checked **2026-09-10**: the target-SDK page lists API36 for new
apps and updates from 2026-08-31, with Wear/Automotive API35 and TV/XR API34
exceptions. Existing-app availability has its own matrix. Billing Library 7's
submission cutoff is 2026-08-31, subject to a granted extension; this applies only
when the app uses Billing. The 16KB guide lists 2027-02-01 update blocking for
affected API35+ 64-bit apps. Re-open the linked official pages and the app's
Console notices before using any of these dates as a gate.

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

Play developers normally complete Android developer verification through their
existing Play Console; do not create an outside-Play developer account as a
routine prerequisite. Reconcile automatic package registration rather than
assuming that verified identity proves every package is registered. The current
verification guide starts enforcement on 2026-09-30 in Brazil, Indonesia,
Singapore and Thailand, with further rollout later. If the provider requires a
signed package-ownership challenge, bind its nonce, package and certificate via
the protected signing path. That proof file is distinct from the release AAB;
it grants no authority to replace a signing key or upload a new public build.

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

For personal accounts created after 2023-11-13, the checked requirement is at
least 12 testers continuously opted in for the preceding 14 days before applying
for production access. Preserve real opt-in/cohort and feedback evidence, then
record Google's decision. Passing the duration/count check is not approval, and
recruiting testers or sending invitations needs its own authorized audience.

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

Use the actual track identifiers returned by the selected API/Console, including
custom closed tracks and form-factor prefixes. A CLI alias such as `internal`
need not be the raw API identifier. Testers can receive the highest compatible
version code across all tracks for which they are eligible; a higher production
version can mask a lower test candidate. Bind test-list/group membership, opt-in,
Play account/country, device compatibility and installed version. Internal
testers may need to opt out before receiving an open or closed test. Share the
exact authorized opt-in link when the app is not searchable; a listed email alone
does not prove enrollment or installation.

## Artifact And Signing Proof

Use the project's existing release build task, commonly `bundleRelease` or a
variant-specific equivalent. Do not introduce a publication framework merely
to invoke Gradle once. Before upload:

1. Start from a clean, identified revision and run the project-owned release
   checks required by that artifact.
2. Reuse the identified, tested signed AAB while its evidence remains applicable;
   build with the project task only when needed. Calculate or verify its SHA-256
   and byte size. Promotion of the same uploaded version requires no rebuild or
   repeated local smoke solely because its track changes.
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

Check the actual artifact container and manifest, not just its filename suffix.
If the manifest cannot be read, stop artifact binding rather than uploading on a
warning. A version-code collision first requires reconciliation: the candidate
may already have uploaded. A genuinely changed binary needs a new higher code,
new hash and repeated relevant checks. Promote an already tested version without
rebuilding it. Preserve matching R8/ProGuard mapping and native debug symbols when
the app uses them, associate them with the same release, and keep private source
paths or source-bearing diagnostic artifacts out of public receipts.

### Native 16KB Compatibility

This branch applies to native code, including `.so` files bundled indirectly by
frameworks and third-party SDKs. A wholly Java/Kotlin app and all of its
dependencies may need no native rebuild; establish that from the release
artifact. A framework version alone does not prove the shipped SDKs comply.

Use current official Android tools from the existing project toolchain:

| Check | What it proves and what remains |
| --- | --- |
| `bundletool dump config --bundle=<release.aab>` | Inspect requested page alignment, including `PAGE_ALIGNMENT_16K`; not ELF or runtime correctness |
| `zipalign -v -c -P 16 4 <release.apk>` | Check ZIP placement in each relevant generated release APK; retain the process exit status |
| `llvm-objdump -p <library.so>` | Inspect relevant 64-bit ELF LOAD segments for alignment of at least `2**14`; ZIP alignment cannot repair ELF segments |
| Install/launch on an identified 16KB environment | Prove actual page size and exercise native-dependent critical paths; emulator and physical-device evidence stay distinct |

Check Play-generated APKs when available as well as local packaging. A locally
working build can differ from APKs generated from its bundle. If any layer fails,
identify the library/toolchain owner and request a compatible rebuild; do not
patch binary headers, repack or re-sign a package as a compatibility workaround.

### Play-Generated APKs And Internal App Sharing

For targeted delivery QA, App bundle explorer or `generatedapks` can expose APKs
for the uploaded version. Bind the version code, signing-certificate group,
device configuration and downloaded artifact identity. A draft-track commit or
internal test used to obtain Play-generated artifacts is still a provider write
with its own approved scope. Do not select an arbitrary certificate group.

Internal App Sharing (IAS) is a separate optional rapid-QA path. It produces a
temporary sharing link, requires authorized testers and device-side enablement,
and re-signs artifacts with the IAS certificate. Its install is not evidence of
the production signing certificate, test-track release or public availability.
Keep capability-bearing download/session/share URLs protected; record a safe
reference rather than placing them in public logs. Promotion uses a normal
uploaded track version, not an IAS link.

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

Use a compact cross-check: feature or SDK -> observed permission/data flow ->
declared purpose/handling -> reviewer-visible behavior. A source scan is useful
evidence, not a replacement for product behavior or a guaranteed compliance
decision. For ordinary public Play apps, Data safety is required for
closed/open/production distribution even when no data is collected; the
documented exclusively-internal-testing exception must not be applied after the
app enters another track. For permanently private organizational distribution,
check the provider's separate exemption and exact app scope.

When the app allows account creation, check the applicable in-app deletion path
and an externally reachable web deletion-request path for accounts and associated
data. Verify that the served page identifies the app/developer and actually
enables the request. A generic privacy-policy URL alone is insufficient.

Reviewer access must remain usable: reusable, non-expiring, location-independent
credentials or another supported path, clear English instructions, and access
to restricted/paywalled features without a reviewer purchase. If OTP/MFA or a
regional restriction blocks review, arrange an owner-approved scoped review
account/environment or supported alternative. Do not disable production security
or invent a backdoor. Verify the path privately and transmit access material
only through the protected provider channel.

Metadata synchronization also needs an exact scope: enumerate locales, listing
fields, release notes and each image/screenshot set to change, retaining the
rest. Downloading an existing listing can bootstrap local metadata; a subsequent
upload must not prune omitted locales or replace media without the intended diff.

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

### Inspect The Existing Executor

Record the installed version and relevant help/configuration before choosing a
command. The following are source-checked risks as of **2026-09-10**, not promises
that a wrapper is installed, authenticated or compatible with the current API:

| Executor | Bind before running |
| --- | --- |
| Gradle Play Publisher | Exact variant/task and artifact set; `artifactDir` may publish multiple files. Do not enable AUTO version resolution or IGNORE collisions as a retry repair. `commit=false` holds a temporary edit, not a durable saved draft. |
| fastlane `upload_to_play_store` | Explicit package, artifact, track and release status; defaults include production/completed. `validate_only` opens an edit and uploads before validation, so it is neither offline nor read-only. Inspect automatic `rescue_changes_not_sent_for_review` behavior and prevent an unapproved retry from changing review submission. |
| EAS Submit | Exact project/profile/build artifact and job identity, selected cloud/credential custody, track/status/rollout parameters, and final Play Console state. EAS job completion does not prove review, release or installation. |
| API or community CLI/MCP | Inspect its actual method/flags, raw API versus alias track names, edit creation, retry/commit behavior and output redaction. A tool's `readOnlyHint`, `dry-run` name or confirmation flag is not an authority boundary. |

For fastlane, metadata, changelogs, images and screenshots have separate upload
controls; skipping one does not imply the others are skipped. For every route,
preview the complete intended delta and explicitly retained versions. If a
wrapper cannot preserve the review-safe commit behavior, use a supported direct
API or Console path. Do not assume a first-app API upload is supported merely
because a wrapper advertises submission: verify the exact route and retain the
Console bootstrap fallback required by the provider's setup flow.

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

Coordinate one edit owner for the app. A new edit by the same user invalidates
that user's previous edit; Console changes or another committed edit invalidate
open edits. Do not start an edit just to "read" while another release owns one.
Use genuinely non-mutating provider reads or the owning edit where supported,
and distinguish a limited release summary from a complete artifact inventory.
On invalidation or expiry, reconcile current state before planning a replacement
transaction; replaying an old whole-track payload can overwrite someone else's
changes.

Track updates must include version codes intended to remain in the release.
Validate actual track status, release notes and retained artifacts. A rollout
fraction must satisfy `0 < userFraction < 1` for `inProgress` or `halted`;
completion uses the `completed` state. Country targeting and update priority have
their own API restrictions, so inspect the current track schema before changing
them. A display release name is not a unique identifier.

Not every Play write belongs to an edit. Product/subscription operations and the
`applications.dataSafety` CSV endpoint are outside the release transaction.
They need their own preview, authority and effect readback. Do not imply that an
uncommitted release edit or managed publishing holds such changes. An empty
successful API body is not proof of the consumer-visible declaration or catalog;
read the appropriate Console/product surface after the write.

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

When the selected uploader supports Google's resumable protocol, interrupted
media transfer can resume within the same protected upload session after querying
the server's received byte range. A completed status response may mean the
original upload already succeeded. Do not blindly restart from zero or expose
the session URI in receipts. If the session has expired, reconcile the artifact
and edit before preparing a replacement upload. This transport recovery does not authorize replay of an
uncertain `edits.commit`, product activation or recovery action.

## Optional Purchase Catalog Delivery

Enter this branch only when the requested release includes an existing or
explicitly requested monetization product. Delivery verifies catalog and consumer
behavior; implementing billing/backend entitlement logic remains with the app
owner. Record whether any catalog change is actually needed before writing.

| Product shape | Identity and state to reconcile |
| --- | --- |
| One-time product | Package/product ID, purchase option (for example buy/rent), applicable offer, state, localized display, regions and currency/price |
| Subscription | Package/product ID, base plan, applicable offer, active/inactive state, renewal/prepaid terms, localized display and regional availability/price |
| Existing catalog with no requested change | Read the exact IDs selected by the shipped client; do not synchronize, deactivate missing local entries or migrate subscribers as cleanup |

Activation, region/price changes, existing subscriber price cohorts, tax choices,
refunds, revocation and deletion have distinct financial/user effects. Scope them
explicitly; a release approval alone does not authorize them. Read-back API state
and the app's displayed purchasable option must agree for the intended account,
country and installed version. Deactivating a subscription base plan can leave it
available to existing subscribers; it is not a cancellation of their entitlement.

Test-track enrollment is separate from license testing. Ordinary purchases on a
test track can charge real money. Use an explicitly configured license tester
and approved test payment instrument; confirm the account used for the Play
download/purchase, especially on devices with multiple accounts. Exercise the
applicable purchase, pending, acknowledgment, entitlement, restore and
subscription-state paths with the project's existing sandbox facilities. Record
what was observed and distinguish accelerated sandbox behavior from production.
Do not require a real charged purchase, refund, Billing Lab installation or a new
third-party billing service to finish a generic release task.

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

Health evidence must match the candidate. Record metric name, version/device
slice, time window/time zone, freshness watermark and user denominator before
comparing with the project's release thresholds and previous baseline. The Play
Developer Reporting API is a separate optional read surface; check each metric
set's `freshnessInfo` before querying. Missing, lagged or tiny-sample data is
inconclusive, not zero crashes/ANRs. Do not automate percentage increases using a
universal fixed threshold or a clock-only schedule.

## Recovery And Proof

For a rejection, extract the exact policy issue, affected version, evidence,
deadline, and available action. Separate an artifact defect, declaration defect,
account/identity issue, permission issue, tester prerequisite, and review-only
blocker. Correct the narrow owner, produce a new artifact only when binary state
changed, and preserve the rejected submission identity in the receipt.

For an eligible app, Play's remote app recovery can prompt affected users to
update to a newer compatible version. Check current eligibility, the target
version's availability on all affected tracks, and exclusions for the app's
signing/protection/form-factor configuration. Bind the bad version, exact
audience and recovery-action ID before activation. The prompt is dismissible;
activation is not proof that every device updated. Canceling a recovery action
does not undo updates already installed. Record provider recovery status/counts
and observed consumer behavior separately.

Two other lifecycle effects are optional. Preregistration starts a country-bound
launch obligation; the checked current rule is 90 days and pausing does not stop
the clock. Enter it only with an explicit launch plan and record each country's
deadline. Unpublishing prevents new acquisition while existing users may keep
using the app and receive updates; it is not an installed-version rollback or
subscription revocation. Read current prerequisites and preview that audience
effect before changing availability.

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

The lifecycle additions below were checked on **2026-09-10**; retained baseline
sources were previously checked on **2026-08-24**. Re-open the relevant page at delivery
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
- [Distribute releases to specific countries and Play country](https://support.google.com/googleplay/android-developer/answer/7550024?hl=en)
- [Use a pre-launch report to identify issues](https://support.google.com/googleplay/android-developer/answer/9842757?hl=en)
- [Control review submission and managed publishing](https://support.google.com/googleplay/android-developer/answer/9859654)
- [Release updates with staged rollouts](https://support.google.com/googleplay/android-developer/answer/6346149)
- [Prepare App content for review](https://support.google.com/googleplay/android-developer/answer/9859455)
- [Data safety declarations](https://support.google.com/googleplay/android-developer/answer/10787469)
- [Android app signing and Play App Signing](https://developer.android.com/studio/publish/app-signing)
- [Android App Bundle and bundletool](https://developer.android.com/tools/bundletool)
- [Android Publisher API](https://developers.google.com/android-publisher/api-ref/rest)
- [`edits.validate`](https://developers.google.com/android-publisher/api-ref/rest/v3/edits/validate)
- [`edits.commit` and review-safe behavior](https://developers.google.com/android-publisher/api-ref/rest/v3/edits/commit)
- [Current developer-verification workflow](https://developer.android.com/developer-verification/guides)
- [16KB page sizes and native compatibility](https://developer.android.com/guide/practices/page-sizes)
- [Billing Library submission deadlines](https://developer.android.com/google/play/billing/deprecation-faq)
- [Reviewer login access](https://support.google.com/googleplay/android-developer/answer/15748846)
- [Account and data deletion requirements](https://support.google.com/googleplay/android-developer/answer/13327111?hl=en-EN)
- [Edits, bootstrap and invalidation](https://developers.google.com/android-publisher/edits)
- [Track identifiers and form factors](https://developers.google.com/android-publisher/tracks)
- [Track/release schema and retained versions](https://developers.google.com/android-publisher/api-ref/rest/v3/edits.tracks)
- [Data safety CSV write](https://developers.google.com/android-publisher/api-ref/rest/v3/applications/dataSafety)
- [Resumable media uploads](https://developers.google.com/android-publisher/upload)
- [Download Play-generated APKs](https://developers.google.com/android-publisher/download-apks?hl=en)
- [Generated APK signing-certificate groups](https://developers.google.com/android-publisher/api-ref/rest/v3/generatedapks/list)
- [Internal App Sharing](https://support.google.com/googleplay/android-developer/answer/9844679?hl=en)
- [One-time products and purchase options](https://developers.google.com/android-publisher/api-ref/rest/v3/monetization.onetimeproducts)
- [Subscriptions and base plans](https://developers.google.com/android-publisher/api-ref/rest/v3/monetization.subscriptions)
- [License testers and purchase testing](https://developer.android.com/google/play/billing/test?hl=en)
- [Version-sliced crash metrics and freshness](https://developers.google.com/play/developer/reporting/reference/rest/v1beta1/vitals.crashrate)
- [Remote app recovery](https://support.google.com/googleplay/android-developer/answer/13812041?hl=en)
- [Preregistration](https://support.google.com/googleplay/android-developer/answer/9859047?hl=en-EN)
- [Update or unpublish an app](https://support.google.com/googleplay/android-developer/answer/9859350?hl=en)

Existing-executor references (read the installed version's configuration and help):

- [Gradle Play Publisher](https://github.com/Triple-T/gradle-play-publisher)
- [fastlane upload_to_play_store](https://docs.fastlane.tools/actions/upload_to_play_store/)
- [EAS Android submission](https://docs.expo.dev/submit/android/)
- [EAS credential and first-upload constraints](https://docs.expo.dev/app-signing/security/)
