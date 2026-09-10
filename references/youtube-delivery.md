# YouTube and Shorts delivery

Official requirements checked 2026-08-24. YouTube limits, API quotas, upload
eligibility, policy surfaces, and Shorts classification can change; re-open the
linked primary sources during a real release.

## Target contract

Bind before mutation:

- authenticated Google identity and exact channel ID/title;
- OAuth client/project, complete operation set, least scopes, quota availability
  and audit restriction, without recording credentials;
- channel feature eligibility, strikes, upload limits, and existing matching
  video IDs;
- media SHA-256/size and probed streams, duration, dimensions, aspect, frame
  rate, codecs, audio, caption and thumbnail hashes;
- title, description, category, language, audience, age restriction, rights,
  paid promotion, altered/synthetic disclosure, license/embedding/remixing,
  comments, subscriber notification, visibility, schedule/timezone, and Shorts
  intent;
- desired effect: `private-ready`, `unlisted`, `scheduled`, or `public`.

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

## Artifact readiness

Use a real media probe. Prefer the current YouTube encoding guidance and retain
the native frame rate and aspect ratio rather than adding black bars. Verify at
least one video and audio stream, sane duration, progressive playback readiness,
and selected caption format. A codec/container recommendation is not a policy
guarantee.

For Shorts intent, verify the current official aspect/duration rule and rights
behavior. As of the observation date, standard-channel square or vertical
uploads up to three minutes are categorized as Shorts, while longer-than-one-
minute Shorts with an active Content ID claim can be blocked. Do not freeze
these thresholds; re-check them. The Data API exposes no documented writable
or authoritative `isShort` field, so classification is an external-surface
proof after publication.

## Provider flow

1. Complete channel and OAuth bootstrap in official UI. Enumerate every planned
   call before consent: an upload-only scope may not authorize `videos.update`,
   captions, or other follow-up operations. Request only the resulting needed
   scopes, inspect current project quota/costs, and confirm identity with
   `channels.list(mine=true)` immediately before upload.
2. Use `videos.insert` with resumable upload and `privacyStatus=private`. Include
   the truthful audience and synthetic-media declarations supported by the
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
6. Insert timed captions and persist the returned caption-track ID immediately
   as its own typed provider object. Reconcile a lost response by that ID and a
   deterministic identity such as video, language, and track name. Require one
   exact match: zero, multiple, or conflicting matches go to human review and
   never authorize a second insert. Read caption state with
   `captions.list(part=snippet, videoId=..., id=...)`; the processing state is
   `snippet.status`, not a `status` part. Wait for `serving` and retain
   `failureReason` when failed. Upload a thumbnail only after channel
   eligibility is confirmed.
7. Review private playback as the intended viewer plus Studio Checks and
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

## Recovery

| Symptom | Safe discriminator and recovery |
|---|---|
| Upload response lost | Query the validated protected resumable session, then read a known video ID. Without either identity, keep `effect_unknown`; heuristic title/channel/time matches do not prove absence or authorize another insert. |
| Session returns resumable offset | Resume from the provider range; do not restart from byte zero. |
| Session expired | Reconcile by stable video ID when available. If the earlier insert remains ambiguous, require provider-authoritative proof or a new human decision accepting duplicate risk before a new private upload. |
| Processing remains pending | Read processing details and notices with bounded backoff. Timeout is not rejection. |
| Caption response lost | Reconcile by persisted caption ID plus deterministic identity. Require one exact match and read `snippet.status`; zero or multiple matches require human review, not another insert. |
| Visibility response lost | Read the exact video status before any update. |
| API upload remains private | Check API-project audit restriction and channel eligibility; do not retry or bypass it. |
| Private preview is creatively or legally rejected | Stop. Technical QA cannot authorize upload or publication of an unacceptable artifact. |
| Public watch URL works but Short is absent | Wait for classification/indexing and inspect the Shorts surface; keep `verified` false until the requested surface is observed. |

The safest reversible rollback is normally `private` or `unlisted`. Deletion is
permanent and always needs a separate exact checkpoint.

## Completion evidence

- `private-ready`: exact video ID, processed at the chosen threshold, private
  playback checked as an intended viewer, full metadata/declaration intent plus
  thumbnail/captions bound, Checks/Notices observed.
- `scheduled`: provider reports private plus the exact future `publishAt`.
- `public`: provider reports public and anonymous playback works where region,
  age and audience permit; otherwise the intended-viewer limitation is explicit.
- `verified Short`: public playback plus observed Shorts classification/surface.

Retain limitations such as processing resolution still pending, a notice still
running, API audit restriction, missing thumbnail capability, or unproved
Shorts classification.

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
- [Upload videos in YouTube Studio](https://support.google.com/youtube/answer/57407)
- [Content notices](https://support.google.com/youtube/answer/17011221)
- [Three-minute Shorts](https://support.google.com/youtube/answer/15424877)
- [Recommended encoding settings](https://support.google.com/youtube/answer/1722171)
- [Altered or synthetic content disclosure](https://support.google.com/youtube/answer/14328491)
- [Made for kids guidance](https://support.google.com/youtube/answer/9528076)
- [Schedule publication](https://support.google.com/youtube/answer/1270709)

YouTube Analytics is downstream performance analysis, not delivery proof. Do
not create an analytics pipeline merely to verify publication.
