---
name: delivery-youtube
description: >-
  Deliver a YouTube video or Short: bind channel and media, upload private,
  recover resumably, verify processing/checks, publish or schedule with exact
  authority, and prove watch/Shorts surfaces. Excludes creation and growth
  strategy.
---

# YouTube Delivery

Read `$PLUGIN_ROOT/references/delivery-control-contract.md` and
`$PLUGIN_ROOT/references/youtube-delivery.md`. Refresh mutable requirements from
the dated official sources before relying on limits, feature eligibility,
classification, or API behavior.

Resolve `$PLUGIN_ROOT` from the host, or as `../..` from this skill folder when
the host does not supply it.

## Deliver

First distinguish a new upload from an update or resumed operation on an existing
video. Bind the existing video ID and current state; reuse applicable retained
proof and perform only the requested transitions. Metadata/caption/visibility
work does not require re-uploading, downloading the original media, or making an
already-public video private. Bind new media hashes only for changed assets.

1. Observe the intended Google identity, exact YouTube channel ID/title, API
   project audit/consent state, required operation set and OAuth scopes, current
   quota buckets, channel feature eligibility, strikes or upload limits, existing
   videos, and installed project-native workflow. A Google account alone is not
   channel identity, and delegated Studio access does not establish API access.
   Confirm the exact channel on the selected route; use official UI for bootstrap.
2. For new or changed video media, bind byte size and SHA-256 plus duration,
   width/height, aspect ratio, frame rate, video/audio codecs, audio sample rate, and hashes for any
   supplied caption or thumbnail files. Use `ffprobe`/`ffmpeg` when available;
   missing media proof is a blocker, not permission to guess from a filename.
3. Bind title, description, category, language, thumbnail and caption choices,
   audience, age restriction, altered/synthetic-media disclosure, rights, paid promotion,
   license/embedding/remixing, comments, subscriber notification, visibility,
   and schedule with timezone. Do not infer made-for-kids, rights, claims,
   promotion, or synthetic-content answers from genre or prompt text.
   Preserve requested accessibility and applicable caption requirements, while
   allowing legitimate absent-caption and provider-generated-thumbnail choices.
   Check eligibility and delivery route for requested features such as longer
   uploads, clickable links, chapters, a related Short video or a custom thumbnail;
   an unused optional feature must not become a publication gate.
4. Prefer an existing reviewed project workflow. Otherwise use the official
   YouTube Data API for repeatable uploads or YouTube Studio/Computer Use for
   first-time setup, checks, notices, and fields the API cannot prove. Preflight
   the full operation set: upload-only authorization is not necessarily enough
   for metadata updates, thumbnails or captions. Use least-privilege OAuth
   through protected official UI; do not use a service account.
5. For a new video, upload exactly once as `private`, with subscriber notification
   explicitly bound (normally false for a private canary). Store a resumable session URI
   only in a named protected OS store entry with a nonsensitive lookup key; it
   is a secret capability. Bind the protected record to the exact effect,
   request/media digest, byte count, and confirmed offset, and validate it as
   untrusted input before resume. Use the reference's status/range protocol and
   bounded retry policy; channel upload limits are not transient network errors.
   Persist the returned video ID as the stable provider object. If both
   identities are missing after an ambiguous insert,
   keep `effect_unknown`; title/channel/time heuristics do not authorize a
   second upload.
6. Wait for the chosen processing threshold. Attach supplied captions or
   inspect the intended existing/automatic track; require tracks only when the
   requested outcome or applicable requirements call for them. For an inserted
   track, persist the caption ID as a separate provider object, require one
   exact deterministic match, and read processing from `snippet.status`.
   For published viewer captions, verify `serving`, `isDraft=false`, language and
   playback. Use the supported Studio route for untimed transcript auto-sync;
   the API's old `sync` option is deprecated.
   Missing or conflicting identity after insertion requires human review
   rather than another insert. Apply and verify the chosen thumbnail through
   its supported route; custom-thumbnail eligibility is not a universal
   publication prerequisite.
   Verify the watch page under its current authorized visibility as an intended
   viewer, and inspect Studio Checks/Notices plus bound declarations. Technical processing is not copyright
   clearance or publication approval.
7. Present one final preview bound to video ID, applicable media/metadata hashes, exact
   channel, thumbnail, captions, audience and disclosure answers, unchanged or
   requested visibility, and any timestamp/timezone. Request approval
   through the host if this exact effect was not already authorized.
8. When a visibility or scheduling change is requested, apply it once with
   read-modify-write semantics. Re-read the video
   after an ambiguous response; never repeat `videos.update` blindly because
   omitted mutable fields can be removed. A confirmed future schedule is its
   own completion state; when due-time verification is requested, re-read the
   exact video and notices before claiming publication.
9. Prove provider status, anonymous watch-page playback where audience/age and
   region permit it, expected metadata and captions, and—when requested—actual
   discovery on a Shorts surface. Use an intended eligible viewer for restricted
   content and state that limitation. A `/watch` URL and vertical dimensions
   alone do not prove Shorts classification. Verify any requested links,
   chapters, related-video navigation and thumbnail on their actual surface.

Use a separate consequential checkpoint for deletion, copyright disputes or
appeals, monetization, paid promotion, or changes to an already-public video.
For withdrawal, bind the intended access: unlisted retains access for anyone
with the link, while private restricts viewers. Do not treat them as equivalent.
Stop at private-ready, scheduled, public, or a precise provider/policy blocker;
do not start content generation or channel-growth work.
