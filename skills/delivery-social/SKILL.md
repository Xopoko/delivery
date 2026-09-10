---
name: delivery-social
description: >-
  Publish truthful product or release posts to LinkedIn or X: bind evidence,
  account, payload and media; preview, post once through an allowed route,
  recover uncertainty, and verify the URL. Excludes campaigns and engagement
  automation.
---

# Social Delivery

Use this lane when the requested delivered artifact is a LinkedIn post or an X
post/thread about a product, release, article, demo, or result. Read the
[shared control contract](../../references/delivery-control-contract.md) and
[social delivery reference](../../references/social-delivery.md) before
publication.

## Turn Evidence Into One Publishable Artifact

1. Reconstruct the single communication outcome, destination, exact member or
   organization account, audience/visibility, timing, language, link, and
   whether the user asked for preparation, provider-supported scheduling, or
   public posting. Keep
   LinkedIn and X as separate provider objects even when they share facts.
2. Mine only authoritative release inputs: the shipped artifact and public
   page, exact observed features, screenshots/demo, release notes, known
   limitations, attribution and rights. Build a compact fact ledger with a
   source pointer for every material claim. Do not invent adoption, performance,
   customer, availability, security, or launch claims.
3. Draft natively for the channel instead of mechanically truncating one text.
   Preserve the same proposition while adapting opening, density, line breaks,
   link placement, mentions/hashtags, media, alt text, and thread shape. Remove
   unsupported hype and internal/private context. This is delivery editing,
   not a content calendar or growth campaign.
4. Bind the outbound payload as exact UTF-8 text plus ordered media hashes,
   alt text, link targets, audience, reply/quote/reshare relationship,
   poll options/duration, comment/reply settings, paid-partnership and AI
   disclosure, rights attestation, scheduling time and timezone. Inspect the
   rendered preview and link card in a user-operated official UI when those
   materially affect the result.
5. Observe identity and matching recent posts through a provider-permitted
   read path. Publish automatically only through an official API or already-
   approved integration. LinkedIn and X prohibit third-party browser automation
   of posting/activity; do not type, click Submit, scrape authenticated feeds,
   or otherwise use Computer Use as a publisher. For LinkedIn, bind member `sub`
   or organization create authorization and whether a permitted read scope
   exists. For X, bind `/users/me`, protected state, OAuth scopes, media
   readiness, credits/cost and rate-limit state. If no approved API path exists,
   prepare the exact payload and open one user-operated official-UI handoff.
   Do not create a developer app, paid API plan, scheduler, MCP, or social-
   management service for one post.
6. Show one final preview containing account, exact text, ordered media/alt
   text, link, audience, relationship, schedule, and whether the effect is
   immediately public. If the current request does not already authorize that
   exact public effect, request approval. A content draft is not permission to
   publish.
7. Through the approved API, perform one post/schedule action and capture the
   provider post ID or canonical URL. LinkedIn write access does not imply the
   restricted member-read scope needed for autonomous reconciliation. In a
   user-operated UI handoff, treat the returned URL or explicit user
   confirmation as user-attested until a permitted provider read proves it.
   After an ambiguous API response, reconcile by exact provider object or
   permitted newest-first account read. If that read is unavailable, keep
   `effect_unknown` and request one user-operated official-UI check; never
   publish a duplicate to manufacture certainty.
8. Verify the provider state and canonical post surface through the official API
   or a provider-permitted public lookup. If only the official UI can show it,
   request one user-operated confirmation and label it `user-attested`; do not
   automate authenticated feed reading. Confirm exact
   author, text, media, link, visibility, ordering/thread relationship, and
   schedule or publication time.

## Boundaries

- LinkedIn member and organization publication are different authority paths;
  organization roles must be observed, not inferred from profile access.
- X post creation and media upload are separate effects. Reconcile uploaded
  media before a post retry, and reconcile the post before uploading again.
- Editing support and semantics vary. A correction, deletion, repost, reply,
  quote, reshare, poll, paid promotion, or organization-targeted distribution
  is its own exact effect.
- LinkedIn post visibility is immutable; rich media cannot be replaced by a
  text edit. X edit availability varies by API/UI/account and creates an edit
  chain. Probe the exact route; never promise correction without delete/recreate
  impact and a fresh preview.
- Never auto-reply, react, follow, mention people, send DMs, boost, or cross-post
  to an unrequested account. Do not turn publication into engagement work.
- OAuth tokens, cookies, session state, media upload handles, and drafts with
  private launch facts stay out of chat, Git, logs, screenshots, and receipts.

Completion is `prepared`, `scheduled`, `posted`, or `publicly verified` for
each channel separately. A user-attested older post is historical evidence,
not a current provider receipt.
