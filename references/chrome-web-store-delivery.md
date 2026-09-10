# Chrome Web Store delivery

Official requirements checked **2026-08-24**. Review times, policy language,
API versions, rollout eligibility and dashboard fields are mutable; refresh the
linked official pages during a real delivery.

## Evidence boundary

This runbook is source-backed guidance. Local package checks and helper tests
do not prove developer registration, upload, review approval, public listing,
or a Store-origin install. Bind and verify those states in the actual delivery;
do not infer them from the presence of this runbook or an unpacked-browser test.

## Delivery identity

Bind these facts before upload:

- Google developer identity, publisher ID, extension item ID, current status,
  published version, visibility/channel, countries and matching active review;
- registration/agreement, verified contact email, 2-step verification and live
  Trader/Non-Trader status; do not copy personal or public trader fields into a
  receipt;
- source revision and exact upload package format/name, size, SHA-256, payload
  root inventory and `manifest.json` hash;
- Manifest V3 version, extension version, minimum Chrome version, update
  behavior, public key/ID relationship if the project explicitly uses one;
- permissions, optional permissions, host permissions, content-script matches,
  externally connectable origins, web-accessible resources, service worker,
  CSP, externally fetched code/data and every network endpoint;
- listing/localization revision, icons/screenshots, category, support/privacy
  URLs, single purpose, data-use declarations, authentication/reviewer path,
  payments, audience, countries, trusted testers and release mode;
- desired effect: local-ready, trusted-test, review submission, automatic or
  deferred publication, percentage rollout, rollback, or public verification.

The item ID, not the display name or unpacked extension ID, is provider
identity. The package payload must contain `manifest.json` at its root and the
complete extension, not a repository or an outer directory. The extension
version must increase for an update. The current version format is one to four
integer components from 0 to 65535, and the standard prepared ZIP limit is 2
GB; verify all applicable constraints from current docs/dashboard rather than
accepting a package tool's exit code.

In the standard Web Store path, upload a ZIP and let the Store sign the CRX. A
manifest `key` is public material used to stabilize a development ID; it is not
the private signing key. If the item has explicitly opted into Verified CRX
Uploads, every later package update must instead be signed with that item's RSA
key and uploaded as CRX. Opt-in, recovery, creation or rotation of the private
key is a credential-storage and consequential boundary—never infer this lane
from a legacy `.pem` beside a build.

## Preflight the bytes and the user impact

Inspect the payload extracted from the exact ZIP or signed CRX rather than a
loose build directory. Reject path traversal, unexpected nested archives,
source maps/private files, secrets, embedded signing material, test fixtures,
development endpoints and missing referenced assets. Load that exact payload
in a clean Chrome profile and exercise:

- install and service-worker/background startup;
- the critical user path and options/settings;
- requested host access and permission prompts;
- restart/browser update behavior;
- update from the previous released version and user-data migration when
  available;
- uninstall/reinstall and removal of any privileged persistent behavior.

Compare the new manifest to the currently published one. Permission expansion
is material: it can trigger new review scrutiny and can disable an installed
extension until the user grants the new permission. Explain why every
permission is necessary for the extension's disclosed single purpose. Do not
request broad host access or remote code merely to simplify implementation.

Reconcile the privacy form with actual code and endpoints: collection, use,
sharing/sale, authentication, user controls, retention and public privacy URL.
The policy answer is an attestation, not a phrase to optimize. If observation
cannot establish a claim, route that exact fact to the owner.

Validate current listing requirements and exported pixels. At the observation
date the reliable minimum included a 128×128 PNG icon, at least one 1280×800 or
640×400 screenshot, and a 440×280 small promo tile; dashboard validation remains
canonical where official pages conflict. Bind localization behavior, rating,
test instructions and a publicly served privacy URL rather than treating local
Markdown as a published policy.

## Dashboard and API boundary

Use the official Developer Dashboard for account registration/verification,
first-item creation, listing and privacy bootstrap, distribution settings,
policy declarations, ownership changes and any field the API does not expose.
Two-step verification and any registration fee or identity step are protected
human/account boundaries.

The current v2 API updates an existing item; it does not replace dashboard-first
creation and initial listing/privacy/distribution/test-instruction work. Reconcile
an existing item before `Add new item` to avoid a duplicate. New publishers can
also have live publication-count limits, so read the dashboard rather than
freezing them here.

Chrome Web Store API v2 can support an already-existing item:

1. read item and status;
2. upload the exact new ZIP for the standard path or signed CRX for an item
   already enrolled in Verified CRX Uploads;
3. read warnings/status and reconcile the version;
4. submit with automatic or staged publication intent;
5. later publish a staged approval, cancel the active submission, or adjust an
   eligible deployment percentage.

Probe current endpoints, OAuth scope, identity and response schema before use.
The legacy v1 API is deprecated and scheduled to stop being supported on
2026-10-15; do not build a new route around it. API authorization is protected
material. A service account is optional, not a reason to create a durable key
for one release. A visibility change made in the dashboard can require a manual
publish before API publication works again.

## Review, publication and rollout states

Keep these provider states distinct:

`local_ready -> uploaded_draft -> pending_review -> rejected | approved`

Then either:

`approved -> published -> verified`

or:

`approved_staged -> manual_publish -> published -> verified`.

For an existing item, the previously published version remains available while
an update is reviewed. Deferred publication has a provider deadline; current
guidance gives up to 30 days after approval before it returns to draft, but
read the live date rather than calculating from memory.

Percentage rollout is currently offered only to eligible already-published
items with more than 10,000 seven-day active users. Bind the initial percentage
and read the current value before increasing it. A new version can stop further
rollout of the previous partial release; multiple simultaneous rollouts are not
available. Never promise rollout merely because an API field exists.

Public, Unlisted and Private have different discovery/audience but the same
policy-review boundary. Private tester eligibility and Google Group/account
membership must be observed. A parallel beta/testing extension is a separate
item and can trigger repetitive-content policy unless clearly differentiated.

Chrome supports provider rollback to a previous version, but rollback is still
a consequential Store transition. Read current eligibility and outcome, bind
the restored package/version, and verify which version new and existing users
actually receive. Cancellation, rollback and unpublish are not interchangeable.

Before rollback, test the exact target package against data written by the current
version; incompatible stored-data changes can break the extension or lose user
data. Preview the exact replacement version and all pending review or staged
submissions that the rollback will discard. During a percentage rollout, the
provider restores the previous version that reached 100%, which may be older
than the immediately preceding partial version, and aborts the partial rollout.
Do not infer these consequences from the generic word "rollback". These
provider behaviors were rechecked on **2026-09-10** against the official
[rollback guidance](https://developer.chrome.com/docs/webstore/rollback).

## Recovery and proof

After a lost upload/submit/publish response, fetch the existing item/status and
match item ID, version, timestamp and review state. Do not upload a repacked or
resigned package, bump again, or create a second listing until absence is
proved. On rejection, bind the exact violation/enforcement state to the exact
submitted ZIP or CRX and decide whether the repair belongs to code/permissions,
listing/privacy, rights, or a truthful owner answer.

Completion evidence:

- trusted test: provider item/version assigned to the intended tester audience
  and installed through that provider path;
- submitted: exact item/version is pending review;
- staged: approved exact version waits for manual publication and its live
  expiry is known;
- published: provider reports the version published to the intended visibility;
- verified: canonical listing is visible in the intended region and a clean
  Chrome profile installs or updates the Store version, restarts, and passes the
  critical smoke.

## Official sources

- [Publish in the Chrome Web Store](https://developer.chrome.com/docs/webstore/publish)
- [Register a Chrome Web Store developer account](https://developer.chrome.com/docs/webstore/register)
- [Set up the developer account](https://developer.chrome.com/docs/webstore/set-up-account)
- [Trader verification FAQ](https://developer.chrome.com/docs/webstore/program-policies/trader-verification-faq)
- [Share item ownership and roles](https://developer.chrome.com/docs/webstore/share-ownership)
- [Prepare extension files](https://developer.chrome.com/docs/webstore/prepare)
- [Manifest version field](https://developer.chrome.com/docs/extensions/reference/manifest/version)
- [Manifest public key](https://developer.chrome.com/docs/extensions/reference/manifest/key)
- [Complete listing information](https://developer.chrome.com/docs/webstore/cws-dashboard-listing)
- [Privacy practices fields](https://developer.chrome.com/docs/webstore/cws-dashboard-privacy)
- [Distribution settings](https://developer.chrome.com/docs/webstore/cws-dashboard-distribution)
- [Chrome Web Store program policies](https://developer.chrome.com/docs/webstore/program-policies/policies)
- [Listing requirements](https://developer.chrome.com/docs/webstore/program-policies/listing-requirements)
- [Extension quality guidelines](https://developer.chrome.com/docs/webstore/program-policies/quality-guidelines-faq/)
- [Image requirements](https://developer.chrome.com/docs/webstore/images)
- [User data policy FAQ](https://developer.chrome.com/docs/webstore/program-policies/user-data-faq)
- [Review process](https://developer.chrome.com/docs/webstore/review-process)
- [Cancel a pending review](https://developer.chrome.com/docs/webstore/cancel-review)
- [Troubleshoot violations](https://developer.chrome.com/docs/webstore/troubleshooting)
- [Update, deferred publication and percentage rollout](https://developer.chrome.com/docs/webstore/update)
- [Rollback an extension](https://developer.chrome.com/docs/webstore/rollback)
- [Use Chrome Web Store API v2](https://developer.chrome.com/docs/webstore/using-api)
- [API v2 publish method](https://developer.chrome.com/docs/webstore/api/reference/rest/v2/publishers.items/publish)
- [API v2 item status](https://developer.chrome.com/docs/webstore/api/reference/rest/v2/publishers.items/fetchStatus)
- [API v2 item states](https://developer.chrome.com/docs/webstore/api/reference/rest/v2/ItemState)
- [Distribute extensions](https://developer.chrome.com/docs/extensions/how-to/distribute)
- [Store discovery](https://developer.chrome.com/docs/webstore/discovery/)
