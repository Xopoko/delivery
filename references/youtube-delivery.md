# YouTube and Shorts delivery

Official requirements checked 2026-08-24. YouTube limits, API quotas, upload
eligibility, policy surfaces, and Shorts classification can change; re-open the
linked primary sources during a real release.
Account delegation, quota/resume, caption visibility and scheduling guidance
rechecked **2026-09-10** against the sources beside those sections.

## Target contract

Bind before mutation:

- authenticated Google identity and exact channel ID/title;
- OAuth client/project, complete operation set, least scopes, quota availability
  and audit restriction, without recording credentials;
- channel feature eligibility, strikes, upload limits, and existing matching
  video IDs;
- new or changed media SHA-256/size and probed streams, duration, dimensions,
  aspect, frame rate, codecs and audio; hashes for supplied caption/thumbnail files;
- title, description, category, language, audience, age restriction, rights,
  paid promotion, altered/synthetic disclosure, license/embedding/remixing,
  comments, subscriber notification, visibility, schedule/timezone, and Shorts
  intent;
- desired effect: `private-ready`, `unlisted`, `scheduled`, or `public`.

Bind caption and thumbnail choices explicitly. Captions may be supplied,
existing, automatic, or absent where neither the requested outcome nor an
applicable requirement calls for them. Preserve accessibility goals and check
caption-certification obligations; do not create an unconditional caption-upload
gate. A thumbnail may use the provider's generated choice or a custom image.
Custom-thumbnail eligibility is a blocker only when that custom image is part
of the requested outcome. These choices and the current Shorts thumbnail route
were rechecked on **2026-09-10** against the official sources below; custom
Shorts thumbnails currently use YouTube Studio on a computer with a verified
account, so do not assume the general thumbnail API supports that operation.

For the shared receipt, map `private-ready` to normalized `stage`; map
`unlisted`, `scheduled`, and `public` to `release`, with exact visibility in
`channel` and `release_mode`. Use normalized `verify` for a later read-only
watch/Shorts proof.

Treat private upload and later visibility change as separate external effects
with separate authority and observations. A processed private video, completed
creative review, or successful caption operation does not authorize unlisted,
scheduled, or public visibility.

OAuth is user-based; YouTube Data API does not support service-account channel
ownership. An API project that has not passed the applicable audit may be
restricted to private uploads. Detect this before promising public API delivery
and use official Studio when appropriate—never try to evade the restriction.

## Account, route and operation preflight

Distinguish the channel owner, Brand Account access and an invited Studio role.
Someone who can upload as a Studio Editor does not necessarily have an API route
to that channel: invited channel permissions do not grant YouTube API management.
Confirm the exact channel returned by `channels.list(mine=true)` for the chosen
API authorization; never accept the first available channel or substitute the
operator's personal channel. Use the authorized Studio route when that is the
available permission surface. Do not change ownership or channel permissions
to make an upload tool work. See [channel permissions](https://support.google.com/youtube/answer/9481328?co=GENIE.Platform%3DDesktop&hl=en)
and [Brand Account delegation](https://support.google.com/youtube/answer/9367690).

Map the requested operation set before starting a large upload:

| Operation | What must be available |
|---|---|
| Upload and resume | Correct channel, upload authorization, project upload quota, channel allowance, protected session persistence |
| Processing and metadata | Owner-authorized video read, required update scopes and preservation of mutable fields |
| Captions or thumbnail | Supported operation, chosen asset/track identity and feature eligibility only when requested |
| Publication or schedule | Desired visibility, supported schedule semantics and permitted final viewer |
| Requested navigation | Current support for description links, chapters or a related Short video, plus a route to verify the rendered control |

An existing CLI's upload command may omit subscriber notification, declarations,
resumable persistence or required follow-up fields. Inspect its actual interface
against this operation set. Reuse its supported subset or the official route;
do not introduce an MCP, broad OAuth grant or new credential store to fill a
single missing command.

Budget against current project quotas **and** channel limits. The current
[quota calculator](https://developers.google.com/youtube/v3/determine_quota_cost)
and [video insert contract](https://developers.google.com/youtube/v3/docs/videos/insert)
separate video-upload and search quota buckets from other API operations. Do not
derive remaining uploads from an old shared per-upload unit cost. Include status
polls, metadata, requested captions and thumbnails in the operation budget.
`quotaExceeded` and channel `uploadLimitExceeded` require different remedies;
the latter is not a transient network error or evidence that a different API
project would help. Stop/defer the affected operation and retain completed IDs.
See the [error definitions](https://developers.google.com/youtube/v3/docs/errors).

For requested features, check the actual channel's current eligibility and
supported UI/API route: upload duration, custom thumbnail, clickable description
links, chapters and related-video navigation need their own proof. Feature
access is not interchangeable with API-project audit status or quota. An unused
optional feature never blocks the core video. The [feature access guide](https://support.google.com/youtube/answer/9890437)
identifies the current eligibility surfaces; refresh them instead of promising
that one verification step enables every requested feature.

## Artifact readiness

Use a real media probe. Prefer the current YouTube encoding guidance and retain
the native frame rate and aspect ratio rather than adding black bars. Verify a
video stream, sane duration, progressive playback readiness, and the format of
any supplied captions. Check audio presence and quality against the intended
artifact: missing expected narration or music is a defect; intentional silence
must remain explicit. Let provider validation establish format acceptance. A
codec/container recommendation is not a policy guarantee.

For Shorts intent, verify the current official aspect/duration rule and rights
behavior. Standard-channel square or vertical uploads up to three minutes are
categorized as Shorts under the current upload-date rules. As rechecked on
**2026-09-10**, a Short longer than one minute with any active copyright claim,
including a manual claim, is blocked globally until the claim is resolved.
Read the exact claim state before promising playback. Do not freeze these
thresholds; re-check them. The Data API exposes no documented writable
or authoritative `isShort` field, so classification is an external-surface
proof after publication.

## Provider flow

For an existing video, first reconcile its exact ID, channel and current state.
Skip insert/media-transfer steps for metadata, captions, visibility changes or
resumption after a completed upload. Preserve current visibility unless changing
it is the authorized effect. Reuse applicable artifact proof; do not fetch the
original file solely to edit metadata. Verify any changed assets and requested
viewer behavior against that same video identity.

1. When bootstrap is needed, complete it in official UI. Enumerate every planned
   call before consent: an upload-only scope may not authorize `videos.update`,
   captions, or other follow-up operations. Request only the resulting needed
   scopes, inspect current project quota/costs, and confirm identity with
   `channels.list(mine=true)` immediately before upload.
2. For a new upload, use `videos.insert` with resumable upload and
   `privacyStatus=private`. Include the truthful audience and synthetic-media declarations supported by the
   current API, and bind `notifySubscribers` explicitly—normally false for a
   private canary rather than relying on the API default.
3. Persist the stable video ID as a typed provider object in the delivery
   receipt. Keep the resumable session URI in a named protected-store entry with
   a nonsensitive lookup key, never in Git, logs, task receipts, or chat. Bind
   that protected record to the exact effect/request digest, media byte count,
   and latest provider-confirmed offset. Revalidate those bindings on resume and
   treat the stored URI as untrusted input: require HTTPS and a currently valid
   official endpoint before sending credentials or media.
4. On interruption, query the same trusted resumable session and resume by the
   provider-confirmed offset. If a stable returned video ID exists, reconcile by
   that ID. If `videos.insert` may have crossed the network but neither a trusted
   session reference nor stable video ID was durably captured, title, channel,
   or time-window search cannot prove absence. Keep `effect_unknown`, do not
   issue another insert, and require a provider-authoritative discriminator or
   an explicit new human decision that acknowledges duplicate risk.
5. Poll `videos.list` for upload and processing status. `uploaded`, `processed`,
   `failed`, and `rejected` are different states with explicit reasons.
6. For supplied captions, bind BCP-47 language, track name and draft intent,
   insert the timed track and persist the returned caption-track ID immediately
   as its own typed provider object. Reconcile a lost response by that ID and
   a deterministic identity such as video,
   language, and track name. Require one exact match: zero, multiple, or
   conflicting matches go to human review and never authorize a second insert.
   Read caption state with `captions.list(part=snippet, videoId=..., id=...)`;
   the processing state is `snippet.status`, not a `status` part. Wait for
   `serving` and retain `failureReason` when failed. For captions intended for
   published viewers, also require `isDraft=false` and verify the chosen language
   during playback; a serving draft is not publicly visible. For an authorized
   replacement, update the known caption ID rather than insert another track.
   An untimed transcript needs a supported Studio auto-sync route: the API's
   `sync` parameter is deprecated. See the [caption resource](https://developers.google.com/youtube/v3/docs/captions)
   and [insert contract](https://developers.google.com/youtube/v3/docs/captions/insert).
   For existing or automatic captions, inspect the intended track instead of
   inserting a duplicate. If captions are legitimately absent, record that
   choice without inventing a
   track. Apply the chosen thumbnail using its supported route and verify the
   rendered result; upload a custom image only when requested and eligible.
7. Review playback under the current authorized visibility (private for a new
   staged upload) as the intended viewer, plus Studio Checks and
   Notices. Confirm age restriction, paid promotion, license/embedding,
   remixing, comments and notification intent in the official surface when the
   API cannot prove them. Checks can be asynchronous and are not a promise
   against future claims.
8. Re-read all mutable status fields. For publication, use a complete
   read-modify-write payload: `videos.update` replaces the selected parts and
   can clear omitted fields.
9. Scheduling requires private visibility and an exact ISO-8601 timestamp. The
   current API limits `publishAt` to a video that is private and has never been
   published. Bind timezone and detect a past timestamp before mutation.

If later publication verification is requested, re-read the exact video after
its due time and inspect current notices. A Community Guidelines penalty can
keep a scheduled video private and require rescheduling after the penalty ends.
Do not infer publication from the clock, or repeat visibility changes while the
state is uncertain. Keep a confirmed schedule distinct from public playback.
See [scheduled publication](https://support.google.com/youtube/answer/1270709).

### Resumable status and byte boundaries

Use the same validated protected session. A status query is a zero-length `PUT`
with `Content-Range: bytes */TOTAL`, where TOTAL is the bound file size. A `308`
response means incomplete transfer, not a redirect to follow. Its inclusive
`Range` end determines the next byte: `bytes=0-999999` resumes at byte 1000000.
No `Range` means zero bytes confirmed, so resume at zero **within that session**.
Do not assume the bytes sent by the client were accepted.

Honor `Retry-After` and use bounded backoff for documented transient upload
failures. Keep nonfinal chunks a consistent multiple of 256 KiB, with the final
chunk allowed to be shorter. A status query for a completed upload can return
the original completion response; retain its stable video ID instead of issuing
another insert. Expired sessions and lost identities still follow the recovery
rules below. See the [resumable protocol](https://developers.google.com/youtube/v3/guides/using_resumable_upload_protocol).

## Recovery

| Symptom | Safe discriminator and recovery |
|---|---|
| Upload response lost | Query the validated protected resumable session, then read a known video ID. Without either identity, keep `effect_unknown`; heuristic title/channel/time matches do not prove absence or authorize another insert. |
| Session returns resumable offset | Resume from the provider range; do not restart from byte zero. |
| Session expired | Reconcile by stable video ID when available. If the earlier insert remains ambiguous, require provider-authoritative proof or a new human decision accepting duplicate risk before a new private upload. |
| Processing remains pending | Read processing details and notices with bounded backoff. Timeout is not rejection. |
| API quota or channel limit reached | Identify the exact error and quota bucket versus channel allowance. Defer safely; do not loop, change accounts/projects to evade the limit, or replay completed uploads. |
| Caption response lost | Reconcile by persisted caption ID plus deterministic identity. Require one exact match and read `snippet.status`; zero or multiple matches require human review, not another insert. |
| Caption is serving but absent for viewers | Check the exact track's draft state, language and selected playback track. Reconcile before an authorized update; do not insert a duplicate. |
| Visibility response lost | Read the exact video status before any update. |
| Schedule time passed but video is private | Read the exact video and notices, including a possible penalty hold. Report its actual state; a new schedule needs its own bound time and authority. |
| API upload remains private | Check API-project audit restriction and channel eligibility; do not retry or bypass it. |
| Private preview is creatively or legally rejected | Stop. Technical QA cannot authorize upload or publication of an unacceptable artifact. |
| Public watch URL works but Short is absent | Wait for classification/indexing and inspect the Shorts surface; keep `verified` false until the requested surface is observed. |

Choose recovery visibility by the intended access. `Unlisted` permits anyone
with the link to watch and reshare; it does not revoke existing link access and
can appear in a public playlist. `Private` restricts viewers. Bind and verify
the selected effect instead of treating these as equivalent withdrawal modes.
See [privacy settings](https://support.google.com/youtube/answer/157177).
Deletion is permanent and always needs a separate exact checkpoint.

## Completion evidence

- `private-ready`: exact video ID, processed at the chosen threshold, private
  playback checked as an intended viewer, full metadata/declaration intent plus
  caption/thumbnail choices recorded, any requested or required tracks/assets
  verified, and Checks/Notices observed. A valid absent-caption or generated-
  thumbnail choice does not fail readiness.
- `scheduled`: provider reports private plus the exact future `publishAt`;
  this does not establish that publication later occurred.
- `public`: provider reports public and anonymous playback works where region,
  age and audience permit; otherwise the intended-viewer limitation is explicit.
- `verified Short`: public playback plus observed Shorts classification/surface.

Retain limitations such as processing resolution still pending, a notice still
running, API audit restriction, unavailable requested custom-thumbnail
capability, or unproved Shorts classification.
Verify requested links, chapters, thumbnail and related-video navigation on the
actual watch/Shorts surface. Metadata readback alone cannot establish that a
requested consumer control is available or works.

## Official sources

- [YouTube Data API authentication](https://developers.google.com/youtube/v3/guides/authentication)
- [YouTube Data API getting started and quota](https://developers.google.com/youtube/v3/getting-started)
- [Quota and compliance audits](https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits)
- [Channels list and authenticated identity](https://developers.google.com/youtube/v3/docs/channels/list)
- [Feature eligibility](https://support.google.com/youtube/answer/9890437)
- [Videos resource and upload/privacy states](https://developers.google.com/youtube/v3/docs/videos)
- [List videos by stable video ID](https://developers.google.com/youtube/v3/docs/videos/list)
- [Insert a video and subscriber notification](https://developers.google.com/youtube/v3/docs/videos/insert)
- [Videos implementation and processing polling](https://developers.google.com/youtube/v3/guides/implementation/videos)
- [Resumable upload protocol](https://developers.google.com/youtube/v3/guides/using_resumable_upload_protocol)
- [Update video semantics](https://developers.google.com/youtube/v3/docs/videos/update)
- [Captions resource](https://developers.google.com/youtube/v3/docs/captions)
- [List caption tracks and snippet state](https://developers.google.com/youtube/v3/docs/captions/list)
- [Insert captions](https://developers.google.com/youtube/v3/docs/captions/insert)
- [Set a thumbnail](https://developers.google.com/youtube/v3/docs/thumbnails/set)
- [Custom video and Shorts thumbnails](https://support.google.com/youtube/answer/72431)
- [Add subtitles and captions](https://support.google.com/youtube/answer/2734796)
- [Caption certification](https://support.google.com/youtube/answer/2789511)
- [Upload videos in YouTube Studio](https://support.google.com/youtube/answer/57407)
- [Content notices](https://support.google.com/youtube/answer/17011221)
- [Three-minute Shorts](https://support.google.com/youtube/answer/15424877)
- [Recommended encoding settings](https://support.google.com/youtube/answer/1722171)
- [Altered or synthetic content disclosure](https://support.google.com/youtube/answer/14328491)
- [Made for kids guidance](https://support.google.com/youtube/answer/9528076)
- [Schedule publication](https://support.google.com/youtube/answer/1270709)

YouTube Analytics is downstream performance analysis, not delivery proof. Do
not create an analytics pipeline merely to verify publication.
