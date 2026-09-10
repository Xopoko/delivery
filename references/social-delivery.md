# LinkedIn and X delivery

Official interfaces checked **2026-08-24**. LinkedIn marketing-version headers,
API access tiers, organization roles, X access plans, posting limits and media
interfaces change. Probe current official UI/API state during a real post.
Media, account selection, threads and scheduling guidance rechecked
**2026-09-10** against the sources beside those sections.

## Evidence boundary

This runbook is source-backed guidance. A prepared payload, approved preview,
or local helper test does not establish API access or publication. A live post
needs its own provider identity, canonical URL, payload, and visibility proof.
Keep one requested post scoped to that artifact and preserve `prepared` versus
`posted` in every report.

## One source bundle, separate channel artifacts

Start from a small release evidence bundle:

- product/result name and one-sentence proposition;
- exact shipped availability, version and canonical public link;
- 2-5 material observed facts with source pointers;
- screenshot/demo/media with ownership and hashes;
- known limitation or scope boundary that makes the claim truthful;
- desired audience, language and call to action.

Produce separate LinkedIn and X payloads. A payload contains exact UTF-8 text,
ordered media and hashes, alt text, link targets, mentions/hashtags, account,
visibility, reply/quote/reshare relationship, schedule/timezone and a SHA-256 of
the serialized intent. Bind poll options/duration, comment/reply controls,
paid-partnership and AI disclosure, and a rights attestation when applicable.
Do not maintain a campaign plan, performance dashboard,
hashtag database, voice system or calendar unless the user actually asks for
that adjacent product.

Channel adaptation is allowed: LinkedIn can carry a more contextual professional
narrative; X may need a compact post or deliberate thread. The proposition and
facts may not drift. Inspect length and rendering using the current provider
surface rather than freezing character limits that vary by account/features.

## Publication route

LinkedIn and X both prohibit third-party tools/bots from automating activity on
their websites. Do not use Browser/Computer Use to type, click publish, schedule,
react, or scrape an authenticated feed. The official UI remains a safe
**user-operated handoff**: prepare the exact payload and preview, route protected
sign-in to the official surface, then let the user perform the provider action.
The agent receives only a canonical URL or explicit status and labels it
user-attested until a permitted provider read proves it.

Use an API only when an existing project already owns the developer app,
authorization and operational need:

- LinkedIn member posting requires the current member authorization such as
  `w_member_social`. Organization posting additionally requires the correct
  organization role and product/API access. The current versioned Posts API
  uses a LinkedIn version header; older UGC examples do not override the live
  supported contract. Member-read access such as `r_member_social` is
  restricted: write authorization does not prove that an agent can list the
  author's posts after a lost response.
- Resolve member identity with the official OIDC `userinfo/sub` surface. For an
  organization, verify the exact organization authorization action (not merely
  a remembered role label), API product/app-review state, and whether the
  intended organic content type is supported.
- X creation uses user-context authorization. Media is uploaded first and its
  provider media ID is then attached to the post. Current self-serve creation
  limits and reply restrictions are mutable and must be probed. An app bearer
  token alone is not evidence that the intended user can publish.
- Resolve X identity with `/2/users/me`, including protected-account state;
  inspect granted user scopes, current credit/payment boundary, media async
  status, and endpoint/user/app rate headers. Payment or auto-recharge is a
  separate consequential decision.

The LinkedIn Posts create contract requests publication on creation; X's
create-Post endpoint also creates a post immediately. Neither is a generic
scheduling API. Creation acceptance is not proof that media has finished
processing or the post is rendered.
Autonomous scheduling therefore requires an already-approved official/partner
integration that explicitly supports it. Otherwise prepare the exact payload
and use the user-operated official scheduler without claiming `scheduled` until
the user or a permitted provider read confirms it.

Do not create a LinkedIn app, X project, paid access plan, scheduler, browser
extension, remote MCP, or durable API token merely for one post. If API access
is absent, use the user-operated official-UI handoff or report the exact blocker.

### Preflight the whole operation set

Record the selected route for the operations the artifact actually needs:

| Operation | Required binding or discriminator |
|---|---|
| Identity | Exact app, member/organization or X user, and permitted audience |
| Media | Owner, supported content type, upload/status access, expiry and accessibility fields |
| Post and verification | Create access plus a permitted read or user-operated verification route |
| Correction | Supported edit/delete operation, current object/version and exact authority |
| Schedule | Existing integration account, validation, job readback, and supported cancel/update route |

Carry the same app/account selector through media, post and verification calls.
An installed CLI or SDK may use a different default account, omit response
fields, or lack a needed endpoint. Inspect its installed help/version and the
current provider contract before reuse. For an already adopted `xurl`, prefer
per-request app/user selection; do not change persistent defaults for a single
delivery. Its token command and verbose output are unsuitable for an agent
session because they can expose credentials. The inspected
[xurl skill](https://github.com/xdevplatform/xurl/blob/41259e8aef85f847145c383d02be6a40a2435466/SKILL.md)
documents these boundaries; it is an optional adapter, not a plugin dependency.

## Media readiness before posting

For every asset bind owner, file hash/size/type, provider media ID or URN and
expiry. Keep signed upload URLs, tokens and multipart continuation material in
protected storage; retain only nonsensitive references in the receipt. Validate
returned upload destinations before sending bytes. A media upload and the post
that uses it are different effects.

### LinkedIn

Choose the current Images, Videos, Documents or MultiImage route for the actual
organic content type. Do not substitute sponsored-carousel or ad requirements.
Initialize under the intended post owner. For video, send the exact inclusive
byte ranges returned in `uploadInstructions`, retain each part's returned ETag
in order, and finalize with the corresponding upload token and ordered part IDs.
Use returned expiry and current route limits rather than guessing chunk bounds
or copying a universal size constant. Read `AVAILABLE`, `PROCESSING`,
`WAITING_UPLOAD` or `PROCESSING_FAILED` and its reason where permitted; a returned
URN alone proves neither successful processing nor publication. If the granted
scope cannot read media state, use a user-operated official preview and label
that proof. See [Videos API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/videos-api)
and [Images API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/images-api).

Bind supplied image alt text in the supported media/post field and preserve
media ordering. Request video captions or a custom thumbnail only when part of
the intended artifact; verify their supported format/language and processing
separately. A feed video being servable does not prove its requested caption or
thumbnail succeeded. The [Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api)
describes content-type and media field selection.

### X

Use the current v2 initialize, append, finalize and status endpoints. The v2
flow has dedicated paths; old command-style INIT/APPEND/FINALIZE examples do not
define the current protocol. Bind the media category and posting account's
entitlement as well as the returned ID and expiry. If finalize supplies
`processing_info`, wait for `succeeded` or `failed`, honoring `check_after_secs`
within a bounded observation window. Otherwise follow the endpoint's documented
ready response. Pending at timeout remains pending. Successful upload does not
guarantee that the posting account may attach the asset. See
[chunked media upload](https://docs.x.com/x-api/media/quickstart/media-upload-chunked).

Apply supplied image descriptions before posting through the current
[media metadata endpoint](https://docs.x.com/x-api/media/create-media-metadata)
(`metadata.alt_text.text` in its documented schema). Preserve the exact intended
text and bind it to that media ID. Verify it using media fields/expansions when
permitted; a post lookup that omits media is not evidence that alt text is absent.
The [data dictionary](https://docs.x.com/x-api/fundamentals/data-dictionary)
defines image `alt_text` and attached-media expansion. Expiry governs reuse of
the upload handle for a new post, not removal of an already published post.
Reconcile an uncertain post before replacing expired media or uploading again.

## Scheduled jobs and published posts

For an existing approved scheduler, bind its connected-account ID, job ID,
exact timestamp/timezone and final per-channel payload. Inspect validation,
readback and cancel/update support before queueing; a recurring queue slot and
a fixed publication time are different intents. Read back the accepted job's
state and time. Keep its job ID separate from each LinkedIn/X post ID.

If verification after the due time is requested, read the existing job/run and
then the returned provider objects. A queued job, expired connection, failed
attempt or user-marked completion does not prove a live post. Preserve successful
channels and reconcile only unresolved effects. Preview a schedule correction;
use the supported update/cancel route and confirm cancellation before any
authorized replacement. An ambiguous cancellation is not permission to create
a second job. These distinctions are also visible in the inspected
[scheduler workflow](https://github.com/social-media-skills/skills/blob/6e30eeb2f6736bda8683b6bbaa674af3641d7945/skills/scheduling-and-queue/references/scheduling-workflow.md).
Do not add a scheduler, recurring task or webhook merely to complete a post.

## Exact public effect

Before publication, use a provider-permitted read to check for a matching recent
payload. If that read is unavailable, ask the user to check the official UI;
inability to read is not evidence of absence. Then preview:

- provider and exact member/organization/account;
- complete text and thread order;
- media previews, hashes and alt text;
- canonical links and rendered link card;
- visibility/audience, reply/quote/reshare target and schedule;
- immediate-public consequence and the post-publication verifier.

An explicit current request to publish that exact payload/account can authorize
the action. Otherwise obtain one explicit approval. Prepare/draft language alone does
not authorize posting. Mentions can notify people and are part of the preview.

Perform each bound post effect once through the approved API, or hand the exact
action to the user in official UI. Preserve post ID/URN or canonical URL and
timestamp. After an ambiguous API result, use the provider object endpoint or
another provider-permitted read and compare exact text/media/link/time. When a
LinkedIn member read scope is unavailable, preserve `effect_unknown` and request
one user-operated official-UI check; inability to read is not proof of absence.
For a user-operated action, ask for one canonical URL/status rather than
automating the feed. Search views, algorithmic feeds and `Most relevant` sorting
are insufficient reconciliation surfaces. Retry only after provider absence is
established.

### X thread continuation

Keep an ordered manifest of each segment's exact text/media digest and expected
parent. Create the first segment, persist its returned ID, then create the next
as a reply to that ID using `reply.in_reply_to_tweet_id`. Repeat only while each
preceding effect is known. The [create Post API](https://docs.x.com/x-api/posts/create-post)
defines this relationship; a thread is not an atomic batch operation.

If segment two is uncertain, preserve segment one and stop before segment three.
Read the exact second object or use the approved reconciliation path; after
uncertainty is resolved, continue only the remaining authorized suffix. Never
restart the whole thread, guess a parent ID, or delete the successful prefix to
make a clean retry. A deliberate rewrite or removal needs its own exact effect.

## Verification and correction

Verify exact author, publication time/state, text, truncation/line breaks,
media order and playback, alt text when observable, link destination, audience,
thread/reply relationship and canonical URL through an official API or
provider-permitted public lookup. If only official UI can show it, use one
user-operated confirmation and say `user-attested`; do not call it anonymous or
agent-verified.

For LinkedIn, preserve the `x-restli-id` response header and exact share/ugcPost
URN. Read `PUBLISH_REQUESTED`, `PUBLISH_FAILED` and `PUBLISHED` as distinct states;
the first is awaiting asynchronous publication, not rendered-post proof. The
[Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api)
documents these states. Do not derive API URNs by swapping prefixes on a URL ID.

For X, request the fields and expansions needed to verify author, complete text,
attachments, reply relationship and current edit history. A shortcut's partial
response cannot prove omitted content. Check an edited object's resulting ID
and chain using the [edit metadata](https://docs.x.com/x-api/fundamentals/edit-posts).
For protected content, use permitted intended-viewer access without broadening
visibility. Report `consumer verified` with that audience limitation; reserve
`publicly verified` for permitted anonymous proof of intended public content.

Editing, deleting, reposting, quoting, replying, resharing, pinning and paid
promotion are separate effects. A factual or rendering defect is not permission
to delete/repost. Preview the correction and its duplicate/notification impact.
Never auto-react, reply to comments, follow accounts or send direct messages as
part of delivery.

For LinkedIn, audience visibility is immutable after publication, text can be
edited only within current UI/provider rules, and rich media replacement can
require destructive delete/recreate. For X, the API and UI can expose different
edit windows/eligibility; bind the exact route, edit chain and resulting IDs.
Deleting an original can affect its edit chain. Never promise an edit, retain
an old canonical ID, or perform delete/repost without a new exact preview.

## Official sources

- [LinkedIn Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api)
- [LinkedIn community management access](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-overview)
- [LinkedIn organization access control](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/organizations/organization-access-control-by-role)
- [LinkedIn organization authorizations](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/organizations/organization-authorizations/organization-authorizations)
- [Sign in with LinkedIn OIDC](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/sign-in-with-linkedin-v2)
- [LinkedIn community-management app review](https://learn.microsoft.com/en-us/linkedin/marketing/community-management-app-review)
- [Share on LinkedIn for members](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin)
- [Getting access to LinkedIn APIs](https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access)
- [LinkedIn prohibited software and extensions](https://www.linkedin.com/help/linkedin/answer/a1341387/prohibited-software-and-extensions)
- [LinkedIn User Agreement](https://www.linkedin.com/legal/user-agreement)
- [LinkedIn post visibility](https://www.linkedin.com/help/linkedin/answer/a523141/visibility-of-shared-posts)
- [Edit LinkedIn posts](https://www.linkedin.com/help/linkedin/answer/a522811)
- [X Manage Posts](https://docs.x.com/x-api/posts/manage-tweets/introduction)
- [X authenticated user identity](https://docs.x.com/x-api/users/get-my-user)
- [X API pricing](https://docs.x.com/x-api/getting-started/pricing)
- [X posting integration guide](https://docs.x.com/x-api/posts/manage-tweets/integrate)
- [X create Post endpoint](https://docs.x.com/x-api/posts/create-post)
- [X media upload overview](https://docs.x.com/x-api/media/quickstart/media-upload-chunked)
- [X automation rules](https://help.x.com/en/rules-and-policies/x-automation)
- [X edit posts](https://docs.x.com/x-api/fundamentals/edit-posts)
- [X rate limits](https://docs.x.com/x-api/fundamentals/rate-limits)
