# LinkedIn and X delivery

Official interfaces checked **2026-08-24**. LinkedIn marketing-version headers,
API access tiers, organization roles, X access plans, posting limits and media
interfaces change. Probe current official UI/API state during a real post.

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

The current LinkedIn Posts create contract publishes immediately and the X
create-Post endpoint is also immediate; neither is a generic scheduling API.
Autonomous scheduling therefore requires an already-approved official/partner
integration that explicitly supports it. Otherwise prepare the exact payload
and use the user-operated official scheduler without claiming `scheduled` until
the user or a permitted provider read confirms it.

Do not create a LinkedIn app, X project, paid access plan, scheduler, browser
extension, remote MCP, or durable API token merely for one post. If API access
is absent, use the user-operated official-UI handoff or report the exact blocker.

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

Perform exactly one provider write through the approved API, or hand the exact
action to the user in official UI. Preserve post ID/URN or canonical URL and
timestamp. After an ambiguous API result, use the provider object endpoint or
another provider-permitted read and compare exact text/media/link/time. When a
LinkedIn member read scope is unavailable, preserve `effect_unknown` and request
one user-operated official-UI check; inability to read is not proof of absence.
For a user-operated action, ask for one canonical URL/status rather than
automating the feed. Search views, algorithmic feeds and `Most relevant` sorting
are insufficient reconciliation surfaces. Retry only after provider absence is
established.

## Verification and correction

Verify exact author, publication time/state, text, truncation/line breaks,
media order and playback, alt text when observable, link destination, audience,
thread/reply relationship and canonical URL through an official API or
provider-permitted public lookup. If only official UI can show it, use one
user-operated confirmation and say `user-attested`; do not call it anonymous or
agent-verified.

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
