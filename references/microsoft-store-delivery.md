# Microsoft Store Delivery Reference

This reference covers last-mile delivery of Windows 11 applications. It does
not teach application architecture or implementation. Microsoft primary
documentation links were reviewed on **2026-08-24**; reopen the relevant pages
before a consequential action because Partner Center fields, policies, CLI
coverage, and review behavior can change.
The MSI/EXE silent-install and standalone/offline-installer requirements were
rechecked against Microsoft's package and certification pages on **2026-09-07**.
The first-submission, audience, hosted-installer, API writer and publishing-hold
guidance was refreshed on **2026-09-10**, including the CLI's pending-draft
replacement and `--noCommit` semantics. Sources beside each section distinguish
provider rules from behavior of an optional tool.

## Completion Contract

Use the shared delivery phases while preserving Partner Center's exact raw
status and observation time:

| Observable Microsoft state | Normalized meaning | What it proves |
| --- | --- | --- |
| Draft with validated package/listing | `staged` | Partner Center accepted the current draft inputs; nothing was submitted |
| Pre-processing or In certification | `submitted` / `in_review` | The exact submission entered Microsoft's pipeline; nothing is public yet |
| Certification passed or release-ready | `approved` | Review passed; publication and customer visibility remain unproved |
| Publishing | `processing` | Publication is in progress; customer acquisition remains unproved |
| In the Store | `released` | Partner Center reports Store release; intended-audience availability and installation still need direct proof |
| Intended audience can view, acquire and install the Store version | `verified` | The requested customer-facing boundary was observed; public listings also have anonymous proof |
| Certification report with failure | `rejected` | This submission failed with a concrete report; it is a valid terminal observation, not a reason to erase history |

Do not compress these into a single "published" boolean. Record `observed_at`,
source surface, stable product/submission IDs when exposed, and evidence links
or bounded receipts. A submission that is `In certification` proves entry into
that provider phase; it does not prove a public release. Local helper tests do
not replace live certification, acquisition, or install evidence.

## Choose the Distribution Lane

### Store-hosted MSIX/AppX and App Installer acquisition

Use for `.msix`, `.msixbundle`, `.msixupload`, `.appx`, `.appxbundle`, or
`.appxupload` submissions. Microsoft hosts and, after successful certification,
re-signs Store-delivered packages. Preserve a separate signing plan for any
sideloader or direct-distribution artifact; local trust and Store trust are not
the same surface.

Bind these fields from Partner Center's **Product identity** page and the
candidate's actual manifest:

- Partner Center product ID and reserved product name;
- package `Identity/Name` and `Identity/Publisher`, including exact casing and
  punctuation;
- publisher display name and package family identity where relevant;
- package version and each applicable architecture/device family;
- visible `Application/@Id`, execution aliases, and declared capabilities.

Name reservation has its own provider lifecycle and expiry. Bind the live
reservation owner and expiry before relying on a name. Names are unique, and
deleting a product/reservation can make recovery impossible or the name
available to someone else; never delete/re-reserve as a discovery technique.

For the Windows 10/11 package classes covered by Microsoft's current MSIX
package requirements, verify the package-version rule before upload. As
reviewed on 2026-08-24, the fourth component is Store-reserved and the uploaded
version must end in `.0`. Treat a different rule observed in live Partner
Center or current official docs as a stop-and-refresh signal, not something to
work around.

Windows selects the highest applicable Store package version for a device. A
lower previously published package is not a customer downgrade mechanism.
Model update/supersedence and device-family applicability explicitly, and ship
a higher compatible version to repair a bad release.

The package should expose the intended customer application. A second hidden
`Application` entry created only to host a command alias is a review and
maintainability risk. Keep the alias beneath the one real visible application
when the manifest schema supports that design. Count applications and aliases
from the packaged manifest, not the source template.

Capabilities such as `runFullTrust` or another restricted capability need a
specific product reason, least-privilege review, and certification notes. Do
not remove a capability merely to satisfy a validator if the shipped behavior
actually requires it; fix the product/manifest contract or provide an accurate
justification through a human-reviewed declaration.

### Publisher-hosted MSI/EXE

This is a separate Store lane for non-gaming PC products, not an alternate
filename for the MSIX API.
Microsoft downloads an `.msi` or `.exe` from a publisher-hosted URL and does not
re-sign that installer. Use the current MSI/EXE Partner Center flow, Developer
CLI commands, or the dedicated Microsoft Store submission API only after
feature-probing the selected surface.

Before staging:

- use an immutable, versioned, publicly reachable HTTPS URL;
- require the URL to resolve directly to the intended `.msi` or `.exe`, not an
  HTML landing page, authentication wall, mutable `latest` path, or redirect to
  unrelated content;
- verify code-signing signatures on the installer and all included Portable
  Executable (PE) files, with a chain to a CA in the Microsoft Trusted Root
  Program; use approved certificate custody without exposing private material;
- hash the local installer, download the staged URL to a bounded temporary
  location, and require byte-for-byte SHA-256 equality;
- require a standalone/offline installer containing the submitted application
  binaries, not a downloader that fetches those binaries when invoked;
- prove silent installation without visible installer UI under the Store's
  invocation: supply the tested EXE switches unless it is silent by default;
  MSI uses `/qn`. Record the exact invocation, result, and installed version;
- verify installation from a standard user account, accurate install/uninstall
  metadata, and clean uninstall on the authorized test surface. Existing
  elevation and physical-control checkpoints still apply;
- never change bytes at a submitted URL. Publish a new versioned URL and create
  a new submission for changed bytes.

Bind each package's architecture, supported languages, URL/hash and installer
type separately. For EXE installers that use custom return codes, map the
tested success, cancellation, reboot or failure results to the Store's handling
fields and provide error documentation where needed. These mappings improve
customer diagnostics; do not invent return codes or require optional mappings
from an installer that does not use them. Silent installation can still invoke
UAC; it does not authorize the agent to accept elevation. See
[policy 10.2.9](https://learn.microsoft.com/en-us/windows/apps/publish/store-policies)
and [MSI/EXE package fields](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msi/upload-app-packages).

The MSI/EXE submission API uses Microsoft Entra application authentication and
is operationally distinct from the MSIX service. Do not introduce a service
principal or durable client secret merely for one delivery if Partner Center's
official UI can complete it. If automation is justified, route creation and
storage of durable credentials through the shared credential-storage
checkpoint before secret bytes exist.

## Exact Artifact Receipt

Create the receipt before upload and preserve it through review. At minimum it
contains:

```text
source revision or source snapshot
portable artifact filename or private task-local locator, or immutable hosted URL
artifact type and byte size
SHA-256
Partner Center product ID
package identity name and publisher
package/application IDs and aliases
package version and architectures
manifest capability set
nested packaged payload inventory or digest
build and packaging command identity
preflight and WACK verdicts with observation time
```

For `.msixupload`/`.appxupload` and bundles, inspect the containers recursively:
find the actual customer package(s), read their packaged manifests, and inspect
their payload. A clean loose-output directory does not prove that the nested
MSIX contains the same executables, configuration, assets, or aliases. Never
infer packaged contents from build logs alone.

After every rebuild, recompute the receipt. If the SHA changes, the earlier
upload, review, screenshot notes, and package-specific proof remain historical;
they do not transfer automatically to the new artifact.

Record source persistence independently of artifact lineage: `local_only`, a
pushed canonical private remote, or a verified private archive/bundle. A local
commit or tag proves which source produced the package but does not make that
source recoverable, and Store publication is not a source backup.

## Preflight

Use the smallest checks that establish the Store boundary:

1. Compare manifest identity and publisher byte-for-byte with current Partner
   Center identity details.
2. Check package version, architecture/device scope, minimum supported Windows
   version, application count, aliases, capabilities, assets, and actual nested
   payload.
3. Verify package or installer signature according to the selected lane.
4. Install the exact candidate in an isolated Windows 11 test surface when
   safe, then launch the primary entry point and any advertised execution
   alias. Exercise uninstall and update from a prior Store-applicable version
   when those are material to the release.
5. Run the Windows App Certification Kit against the exact candidate when
   applicable. Record WACK version, candidate hash, start/end time, a private
   task-local report locator, and one of `passed`, `failed`, or `undetermined`.
   A frozen UI, timeout, killed
   process, missing report, or partial log is `undetermined`; repeating the same
   run without a changed environment produces no new evidence.

Local install error `0x800B0109` commonly describes an untrusted local signing
chain. It does not establish that the package would fail Store certification,
because Store-delivered MSIX/AppX packages are re-signed after certification.
Diagnose the local signing/trust surface separately. Do not add certificates to
machine trust, invoke an elevated installer, or accept UAC on the user's behalf
without the required human checkpoint.

## Listing And Declarations

Read the current draft first, then prepare only fields owned by this release:

- product title, category, description, release notes, features, supported
  languages, system requirements, and certification notes;
- markets, pricing/acquisition, discoverability, public/private audience,
  schedule, publishing hold, and any package flight/rollout;
- IARC age-rating answers, app access, legal/product declarations, and precise
  restricted-capability explanations;
- screenshots, logos, privacy-policy URL, support URL/contact, and website.

Treat declarations as assertions by the product owner, not copywriting blanks
for the agent to guess. Privacy collection, age/content answers, paid terms,
restricted-capability purpose, agreements, and reviewer-account instructions
need human attestation or a verified existing canonical source.

For a first listing, assemble one release packet: product identity, exact
package receipt, supported languages/markets, required copy and exported assets,
declaration answers with their evidence, and outstanding owner decisions. Reuse
the project's existing release documents; local preparation does not require a
provider object. Before creating an app, reconcile the existing Partner Center
products and name reservations. Then follow the
[first MSIX submission sequence](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/create-app-submission)
under the shared authority contract.

Reviewer notes should describe the shortest path to locked features, relevant
regional behavior and what changed. If sign-in is required, supply a working
demo account through the protected Notes for certification field and keep the
backend available during review. Record that access was verified, never the
credential values. Public listing text and reviewer-only instructions are
separate artifacts. See [testability policy 10.3](https://learn.microsoft.com/en-us/windows/apps/publish/store-policies)
and [certification notes](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/manage-submission-options).

For screenshots, capture in physical pixels on the target display, then inspect
the final exported files at 100%. Mixed-DPI Windows desktops can make logical
coordinates crop the wrong region. Reject screenshots containing unrelated
windows, cursors over critical content, notifications, machine/user names,
device identifiers, network addresses, account data, media titles, or other
private context. Verify that the image actually demonstrates the described app
state and meets the current Store dimensions.

Open privacy and support URLs anonymously. Require a stable HTTPS response,
correct product/publisher identity, current content, and no personal placeholder
or private-host leakage. A syntactically valid URL or HTTP success alone is not
meaningful proof.

Visibility is not always reversible: after a submission has made a product
public, Partner Center does not let the same product become private. Bind
public/private/discoverability before the first public submission instead of
assuming that unpublishing will restore private-product semantics.

## Flights And Gradual Rollout

Choose the MSIX distribution route before the first release:

| Intended result | Route and proof |
| --- | --- |
| Confidential first beta | Private audience; verify known-user membership, the authenticated private-product link and tester acquisition |
| Available to anyone with a link | Public audience with restricted discoverability; a direct link still permits access and is not a privacy boundary |
| Test a package update after initial publication | Package flight; bind tester group, package/rank and delivered version while preserving the base listing |

Private-audience testers need personal Microsoft accounts matching the known
user group; Entra work/school accounts do not substitute. Use the private link
from the product identity page. Removing a tester does not remove an installed
copy. Package flights can also target subsets of an already-published private
audience. These are MSIX mechanisms; do not assume the MSI/EXE lane supports
them. See [visibility](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/visibility-options)
and [testing routes](https://learn.microsoft.com/en-us/windows/apps/publish/beta-testing-and-targeted-distribution).

Package flights are separate distribution objects. Bind the flight, tester
group, ranking/priority, device-family ceiling, package versions and flight
certification state. A higher-ranked applicable flight can supersede another;
flight availability is not base-submission availability. Prove a real eligible
Windows 11 Store update from the intended flight.
When promoting a tested flight to the base submission, reuse its exact package
through the supported [package-copy path](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/upload-app-packages)
and rebind the broader audience. A rebuild needs new artifact proof.

Gradual package rollout applies to package updates; listing changes still reach
the full audience. Bind the live percentage and package set. Reaching 100% does
not itself finalize the rollout, and halting prevents expansion rather than
downgrading customers who already received the update. Halt or finalize the
current gradual rollout before a subsequent submission when Partner Center
requires it. A repair is normally a higher version, not an old-package rollback.

## Partner Center And CLI Control Loop

Use Partner Center for first-product setup, name reservation, identity details,
agreements, account state, declarations, and fields not faithfully supported by
the selected API. Prefer an already-working project-native tool path for
repeatable updates; do not add CI, an Entra app, or a new packaging stack merely
because automation exists.

For the MSIX submission API, Microsoft requires an initial submission created
in Partner Center, including the age-rating questionnaire. This is not a
requirement to release publicly first. Once the API creates a submission, keep
its subsequent changes in that API: editing it in Partner Center can prevent
later API edit/commit and leave it unable to proceed. If an unsupported field
forces a change of surface, deliberately finish through the Dashboard where
supported; do not return to API commit assuming compatibility. Any required
delete/recreate recovery retains its own exact checkpoint.

Check product compatibility before choosing the API. Mandatory app updates and
Store-managed consumables are unsupported in the documented MSIX submission
API. Pricing Version 2 requires Partner Center for Pricing and availability,
though other modules can still use the API. Metadata-only changes can reuse an
unchanged package. See the [API prerequisites and limits](https://learn.microsoft.com/en-us/windows/uwp/monetize/create-and-manage-submissions-using-windows-store-services)
and [update guidance](https://learn.microsoft.com/en-us/windows/apps/publish/faq/manage-and-update-your-app).

When `msstore` is already available:

1. Record its version and feature-probe `msstore --help` and the exact command's
   help. The Developer CLI is a changing surface and MSIX versus MSI/EXE command
   coverage differs. An existing `winapp store` wrapper still needs the same
   underlying lane and effect checks.
2. Use read-only commands such as submission status/get before mutations.
3. For the MSIX `publish` path, use the exact `--inputFile` and `--appId`, plus
   `--noCommit` to skip committing, only when current help confirms them. Never
   allow the CLI to auto-select an ambiguous "best" artifact. `--noCommit` does
   not preserve a pending draft: for an already-published app, `msstore publish`
   deletes it and creates a replacement from the last published submission,
   discarding staged metadata. Before that replacement, read the existing draft,
   preserve the needed nonsensitive metadata and asset references privately,
   and require authority explicitly covering replacement. If the draft must
   remain, use Partner Center or a supported existing-submission update against
   fresh current state. For an authorized replacement, upload before editing
   metadata through the same compatible mutation surface, then restore the
   intended changes to the new draft.
4. Do not assume `submission update` is nondestructive because of its name.
   Check current lane/pricing support and whether it creates a missing draft
   or deletes one on an unsupported path. The
   [inspected CLI implementation](https://github.com/microsoft/msstore-cli/blob/901c6f3e515339c614fff6afa0454013727a12cd/MSStore.CLI/Commands/Submission/UpdateCommand.cs)
   does both. Use the Dashboard if these effects cannot be safely bound. For
   supported MSI/EXE updates, read the current package JSON, change only the
   intended fields and use a current supported file/stdin payload mechanism;
   do not construct stale JSON from an example. See
   [MSI/EXE commands](https://learn.microsoft.com/en-us/windows/apps/publish/msstore-dev-cli/commands-exe).
5. Read the complete draft back from its authoritative surface. CLI exit zero
   proves only command completion, not that the intended hash, listing, or
   release options are staged.
6. Invoke a commit/publish command only after the exact final preview and
   authority checkpoint. Read status again immediately afterward.

Tenant, client, and seller IDs are account identifiers; keep any required
private identifiers in approved task-local config or receipts outside Git.
Retain only the minimum needed to bind the provider account and recover the
operation. Do not place client secrets, certificate private material/passwords,
access tokens, or test-account credentials in committed config, shell history,
literal command arguments, screenshots, or receipts. Do not silently change
the CLI's global telemetry setting; expose that separate
preference only if it materially blocks the authorized task.

### Exact final preview

Before `Submit for certification`, `Publish now`, or equivalent API/CLI commit,
show one bounded preview with:

- Partner Center product name and stable ID;
- lane, exact artifact path/URL, byte size, SHA-256, identity, publisher,
  application IDs, version, architecture/device scope, and payload summary;
- restricted capabilities and the proposed justifications;
- listing languages, privacy/support URLs, markets, price/acquisition, audience
  and discoverability;
- package flight or rollout percentage when applicable;
- release schedule or publishing hold, and whether approval would publish
  automatically;
- exact next side effect and whether it can still be cancelled afterward.

An explicit user instruction already authorizing this exact target, artifact,
and public/review effect may satisfy the shared consequential-action contract.
Otherwise use the host's approval surface; do not ask the user to reconstruct
the preview from several messages.

### Publishing hold and customer availability

Keep a manual publishing hold, an earliest publishing-start date and the
customer availability schedule distinct. Manual hold waits for a later publish
action. A dated hold starts publishing no earlier than that time; certification
and processing can make availability later. Read back the provider's timezone,
market schedule and release mode, and record their UTC interpretation. A
publishing-start date currently must be at least 24 hours ahead and can change
only before the submission enters Publish. Do not report a scheduled time as
observed availability. See [publishing hold options](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/manage-submission-options).

## Human Checkpoints

Read-only inspection, package analysis, listing drafts, anonymous URL checks,
and status reads do not need a checkpoint. Use the shared secure/human surface
before:

- developer-account creation/reactivation, identity verification, tax/payment
  setup, or protected sign-in;
- accepting agreements, completing IARC or other legal/content declarations,
  or attesting privacy/restricted-capability facts;
- creating, importing, trusting, rotating, or using protected certificate or
  application credential material;
- UAC/elevation or changing machine certificate trust;
- the final submit, publish, pricing/market/visibility/schedule commitment when
  not already explicitly authorized at that exact scope;
- cancelling certification, deleting a draft/product, or replacing an uploaded
  draft whose history would otherwise be lost.

Group related review fields into one coherent checkpoint. A checkpoint approves
only the named action and exact scope; it does not prove that credentials were
entered, agreements were accepted, or Partner Center committed the transition.

## Recovery Map

| Observation | Correct discriminator and recovery | Do not do |
| --- | --- | --- |
| A second hidden `Application` exists only for an alias | Inspect the packaged manifest; rebuild with one customer-visible application and place the alias under it when supported; rerun receipt and WACK | Argue for a waiver or hide it in listing text |
| Artifact changed after upload | Compare old/new hashes and manifests; stage the new hash in a deliberate draft; request a checkpoint before deleting/cancelling the old draft | Keep the old upload receipt or click submit against an unknown candidate |
| Local install fails with `0x800B0109` | Inspect local signing chain and Store-versus-sideload context; test the Store-signed build only after publication | Call it a Store rejection or globally trust a certificate without approval |
| WACK hangs or produces no report | Record `undetermined`, preserve bounded diagnostics, change environment/method before one new attempt | Report pass/fail or poll indefinitely |
| Screenshots are cropped or leak desktop data | Re-capture using physical-pixel bounds, inspect exported pixels, and redact by recreating the shot rather than blurring secrets | Upload logical-coordinate crops or personal desktop context |
| Privacy/support page exposes personal or placeholder identity | Replace it with an intentional public publisher surface; verify anonymously and review rendered content | Treat an HTTP 200 or repository default page as proof |
| Loose output and packaged payload differ | Inspect the nested MSIX/bundle; rebuild from a clean source and bind proof to its hash | Approve the package from the loose directory or build log |
| CLI/API times out after mutation | Re-read submission status and package metadata from the authoritative surface | Retry publish and risk a duplicate transition |
| Account appears deactivated or inaccessible | Check current Partner Center account state and support path; reactivate the intended existing account through a checkpoint. Preserve the reinstatement receipt plus any deadline, required continued presence, or follow-up obligation; a successful login does not prove those obligations disappeared. | Create a duplicate developer identity to bypass the issue or treat one login as completed recovery |
| Certification fails | Read the current certification report, bind it to the exact hash, fix only the observed product/package/listing issue, create a new submission, and retain the failed receipt | Delete the evidence, rebuild blindly, or claim a later draft inherited the old proof |

## Customer-Surface Proof

After Partner Center reports `In the Store`, use a signed-out/private browser to
open a public release's canonical listing in each material market. Confirm
publisher/product identity, acquisition availability, screenshots,
privacy/support links, and intended audience/price. A dashboard status alone
cannot prove regional or anonymous discoverability.

For private-audience or flight delivery, use the eligible tester and provider
acquisition route instead. Record the intended audience, observed package
version and result without storing tester email addresses. A public base
listing or an anonymous access denial cannot prove that the flight reached its
testers.

On an appropriate clean Windows 11 surface, acquire the app through Microsoft
Store rather than sideloading the pre-submission package. Record Store-delivered
package identity/version, install result, launch result, and the smallest
product-critical smoke. When the release contract includes them, verify command
aliases, update from the previous applicable Store version, and uninstall
behavior. Do not treat a locally signed test install as this proof.

For a command-capable app, resolve the alias from the Store-installed package,
invoke it without relying on the app GUI, prove its protocol and one safe
read-only operation, then uninstall and verify that both package and alias are
gone. A source-build alias or pre-existing PATH entry is not Store lifecycle
proof.

Treat the Store listing, privacy/support URLs, and companion product website as
independently mutable objects. Verify public pages anonymously and a gated listing
through its intended audience's access. A stale companion
site does not negate a proved Store release, but it limits the overall delivery
claim and should be corrected through `delivery-web` under its own exact effect
and authority.

For asynchronous review, persist the exact artifact receipt, product and
submission IDs, raw/normalized status, last observation time, release mode,
pending human choice, and next authoritative read. A status watcher or recurring
poll is a separate requested effect: start one only when the user explicitly
asks to wait, monitor, babysit, or finish through review. Follow the shared
watcher contract: suppress unchanged observations, allow meaningful intermediate
notifications to continue toward the requested terminal, capture final
authoritative and intended-audience proof, plus anonymous proof for public
releases, and then remove the completed watcher.

## Microsoft Primary Sources

Reviewed on **2026-08-24**. Prefer these primary pages over remembered UI text
or third-party tutorials, and record the access date in a real delivery receipt.

- [Microsoft Store Developer CLI overview for MSIX](https://learn.microsoft.com/en-us/windows/apps/publish/msstore-dev-cli/overview)
- [Microsoft Store Developer CLI commands for MSIX](https://learn.microsoft.com/en-us/windows/apps/publish/msstore-dev-cli/commands)
- [Microsoft Store Developer CLI commands for MSI/EXE](https://learn.microsoft.com/en-us/windows/apps/publish/msstore-dev-cli/commands-exe)
- [View app identity details](https://learn.microsoft.com/en-us/windows/apps/publish/view-app-identity-details)
- [Reserve an app name](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/reserve-your-apps-name)
- [Create an MSIX app submission](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/create-app-submission)
- [MSIX app package requirements](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/app-package-requirements)
- [Upload MSIX app packages](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/upload-app-packages)
- [Sign an MSIX package](https://learn.microsoft.com/en-us/windows/msix/package/sign-msix-package-guide)
- [Windows App Certification Kit](https://learn.microsoft.com/en-us/windows/uwp/debug-test-perf/windows-app-certification-kit)
- [App capability declarations](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/app-capability-declarations)
- [Manage MSIX submission options](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/manage-submission-options)
- [MSIX screenshots and images](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/screenshots-and-images)
- [MSIX visibility options](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/visibility-options)
- [Gradual package rollout](https://learn.microsoft.com/en-us/windows/apps/publish/gradual-package-rollout)
- [Package flights](https://learn.microsoft.com/en-us/windows/apps/publish/package-flights)
- [MSIX certification process](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/app-certification-process)
- [MSIX submission controls](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/app-submission-control)
- [Upload MSI/EXE app packages](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msi/upload-app-packages)
- [MSI/EXE certification process](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msi/app-certification-process)
- [Microsoft Store submission API for MSI/EXE](https://learn.microsoft.com/en-us/windows/apps/publish/store-submission-api)
