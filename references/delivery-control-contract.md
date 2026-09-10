# Delivery control contract

This contract is the shared authority, state, evidence, and recovery spine for
every Delivery channel. Platform references add provider semantics and current
official sources; they do not weaken these controls.

## 1. Bind the delivery epoch

A delivery epoch is one exact tuple:

```text
provider + provider account/team/tenant/channel + product/listing/resource identity
+ artifact/payload/source/image/deployment digest + version/build/revision
+ requested effect + destination/track/hostname/traffic + release mode
+ metadata/declaration/config/migration revision
```

Observe live provider state before constructing it. A local project name,
branch, old handoff, email, CLI exit code, or receipt cannot establish current
provider identity. If two artifacts or provider objects could match, stop the
write path until read-only evidence selects one.

Record only what recovery needs: provider, stable nonsensitive IDs, artifact or
deployment-manifest name/hash/size, version/build/revision, requested effect,
latest observed phase/status, provider object/submission/deployment ID, evidence
reference, timestamp, and next action.
Do not record contact data, private local paths, raw provider responses, access
or refresh tokens, cookies, session/upload URIs, signed URLs, reviewer
credentials, certificate private material, recovery codes, or secret-bearing
command lines.

## 2. State is typed

Delivery phases are:

```text
observed -> prepared -> uploaded -> processing -> staged -> submitted
-> in_review -> approved -> scheduled -> released -> verified
```

`rejected`, `failed`, `blocked`, and `effect_unknown` are explicit side states.
They do not imply permission to delete, replace, resubmit, or retry. Recovery
may return to an earlier phase only after live state and a new artifact or
provider revision are bound.

Provider-native names remain in `status`; the phase is a portable summary.
Never derive a later phase only from an earlier phase, elapsed time, an email,
or a local success. In particular:

- built or signed is not uploaded;
- uploaded is not processed;
- processed or valid is not assigned to testers or submitted;
- approved or certified is not released;
- released is not necessarily searchable, watchable, or installable;
- public listing/post/hostname is not proof of the intended artifact or service
  behavior.

Normalize the requested terminal effect independently of phase:

- `prepare`: local artifact and intent are ready; no provider object is needed;
- `stage`: draft, private, internal, beta, or test delivery without the final
  review/public effect;
- `submit`: send the exact object to provider review or certification;
- `release`: make or schedule the authorized distribution effect;
- `verify`: read-only proof of the requested provider and end-user surface.

Platform terms map into this set: Apple `test` is `stage` and `verify_public` is
`verify`; Google Play `draft` or a test track is `stage`; YouTube
`private-ready` is `stage`, while unlisted/public/scheduled visibility is
`release`; Chrome trusted-test or draft is `stage`, review is `submit`, and
Store publication is `release`; a local social payload is `prepare`, schedule
or post is `release`, and canonical readback is `verify`; a zero-traffic web/AWS
revision is `stage`, production deploy or traffic cutover is `release`, and the
consumer path is `verify`. Preserve the exact provider term in channel/status
evidence.

## 3. Authority without questionnaire fatigue

Classify an action by effect, not UI mechanics:

- Read-only observation, local validation, draft metadata, preview generation,
  and reversible preparation are routine once the channel is in scope.
- Private/internal/draft upload is allowed when the current request clearly
  asks for delivery through that channel and the exact artifact and audience
  are bound. Preview it first if it could notify testers, consume a limited
  build/version number, expose content, or create cost.
- Review submission, production rollout/deploy or traffic/DNS cutover, a public
  social post, public/unlisted visibility, automatic release-on-approval,
  price/territory change, and scheduling are consequential.
  A current request that explicitly names the same target and effect can
  authorize the transition; otherwise show one preview and request approval at
  the final boundary.
- Account registration, contracts, legal entity/trader status, tax, payment,
  identity/device verification, age/content/privacy/data/rights attestations,
  reviewer access, restricted capabilities, infrastructure cost, destructive
  migration and export declarations require truthful human or authoritative
  product evidence. Never infer or fabricate them.
- Cancellation, deletion, unpublish, package/listing replacement during active
  review, appeal/dispute, certificate/key rotation, or destructive rollback
  requires its own consequential checkpoint with queue/data impact.

Group related material choices into one decision surface. Do not ask the user
to choose CLI flags, file layout, polling intervals, or other implementation
mechanics.

If checkpoint authority is deliberately carried across sessions, bind it to
the exact delivery epoch, artifact and metadata hashes, channel, requested
effect, expiry, and one-time consumption state. Any bound-input drift or expiry
invalidates it. A persisted approval is scoped authority for that one effect,
not a reusable publishing credential.

## 4. Protected identity and credentials

Try public/anonymous and already-safe read-only surfaces first. When protected
identity is required:

1. Follow the host's native approval and protected credential workflow when
   one is available. Delivery requires no particular approval plugin, password
   manager, credential adapter, or computer-control tool.
2. Reuse an authorized provider session or configured credential broker only
   when it can perform the exact operation without exposing secret values to
   the model. Check availability through nonsensitive status, not secret reads.
3. For provider login, OTP, consent, API-token use, or signing-key access that
   lacks such a protected route, hand the official provider or operating-system
   UI to the user. Stop observation and capture while they enter secrets, then
   resume with nonsensitive provider identity and state readback.
4. Before creating, rotating, recovering, or first revealing a durable API key,
   service-account key, signing private key, certificate, upload keystore,
   recovery material, or provisioning secret, agree on its custody and prepare
   the approved secret-store destination. Use an official UI or a verified
   adapter that sends values directly to that store. If neither is available,
   hand credential creation and storage to the user before any bytes exist.

Use the host's approval surface for consequential decisions, or one concise
chat confirmation if it has no dedicated surface. An approval grants the named
effect; it does not prove login, credential validity, legal acceptance, or
storage. Never ask for secrets in chat, reveal them with a provider CLI, place
them in a receipt or Git, or capture them through browser DOM, screenshots,
clipboard, logs, or computer-control tools. Honor the host's cancel or stop
gesture immediately.

## 5. Capability selection

Use the path that already owns the artifact and returns the strongest receipt:

1. project-native release/deployment workflow with reviewed configuration;
2. installed specialist skill and official/project CLI;
3. official API with least privilege and machine-readable state;
4. official browser UI or Computer Use for first-item bootstrap, identity,
   contracts, declarations, previews, and API gaps only when provider policy
   permits automation. LinkedIn and X posting through their websites is a
   user-operated official-UI handoff, not a Computer Use publishing route.

Probe the actual capability, version, authentication state, output shape,
dry-run/validate mode, and mutation semantics. A binary name in documentation
is not runtime availability. Never silently install a CLI, activate a plugin,
enable telemetry, add a paid cloud or social path, create a service
principal/project, introduce an infrastructure framework, or replace a
project-native release system.

## 6. Write protocol and ambiguous effects

Before every provider write:

- re-read the target object and active review/submission;
- recompute artifact/payload/material metadata hashes and re-resolve remote
  image/deployment revisions;
- use provider validate/dry-run/draft/no-commit modes where available;
- state the exact expected object transition and verifier;
- preserve an idempotency key or stable external object identity when supported.

When a project-native durable workflow can do so, fence a non-idempotent write
before the provider call: atomically persist the exact request digest and
`executing` state and consume its one-shot approval. A crash after that fence is
`effect_unknown`, never an invitation to replay. The optional Delivery receipt
below records observations; it is not itself an execution fence or authority
store.

Execute once. A network timeout, browser crash, CLI hang, missing stdout, or
lost callback is `effect_unknown`. Do not repeat the call or switch tools. Read
the provider by stable ID, listing/version/build, upload session, edit,
submission, caption name, post timeline, deployment/change set/resource,
hostname/route, or visibility. Retry only after evidence proves the write did
not occur or the provider explicitly declares the operation safe to resume.

## 7. User-visible proof

Choose proof proportional to the requested effect:

- staging: exact provider object exists with the bound artifact and intended
  private/internal audience;
- submission: provider reports the exact object in review/certification;
- approval: provider reports approval/certification for the exact version;
- release: provider reports released/public/scheduled state;
- delivery: anonymous storefront/watch/post/hostname lookup and the real
  consumer path work.

For applications/extensions, prefer a clean provider-origin install plus launch
or core behavior and the relevant update, uninstall, alias, entitlement,
purchase, or backend smoke. For social/video, verify canonical author/channel,
payload/playback, media, metadata, captions, visibility/schedule, and Shorts
surface when requested. For web/cloud, prove exact active revision, origin
health, DNS/TLS/edge/traffic and the public product or client path. Preserve
failures and limitations; do not weaken “delivered” to whatever the last tool
exposed.

## 8. Optional receipt helper

Use `$PLUGIN_ROOT/scripts/delivery_receipt.py` only when processing/review spans
sessions or a precise handoff is otherwise at risk. The helper:

- creates one receipt bound to provider account, target, release ID, channel,
  release mode, requested effect, and artifact hash;
- appends idempotent events with an explicit event ID;
- binds each typed provider-object kind to one stable ID within the epoch and
  derives latest state by observation time rather than append order;
- rejects secret-shaped inputs;
- validates the schema and optionally re-hashes the artifact.

Use `provider_account_id` for the stable team/developer/seller/channel/cloud
identity and `release_id` for Apple version+build, Play `versionCode`, Microsoft
package version, Chrome extension version, social payload revision, video
revision, or web/cloud deployment revision. For `stage`, `submit`, `release`,
and `verify`, bind a
nonsensitive metadata manifest containing material version/build details,
listing/declaration revision, audience/destination, territories, schedule, and
other intent not represented by fixed fields. For a remote web/cloud artifact,
use a small nonsensitive deployment manifest as the artifact file to bind source
archive or image digest, config/migration revision, target IDs, backup and
recovery target; keep separate receipts for separate AWS and Cloudflare provider
objects. Its digest is part of the epoch; validation requires re-hashing it.
Never use either manifest as an arbitrary raw provider-response blob.

Before treating the manifest hash as readiness, inspect its coverage. It must
enumerate every independently mutable input needed for the requested effect,
such as the primary artifact or image, listing assets, declarations, audience,
schedule, routes, and provider intent. Hashing an incomplete manifest does not
bind omitted delivery inputs. Record source persistence separately as
`local_only`, pushed canonical remote, or verified private archive/bundle; a
local commit or deployed provider object does not prove source recoverability.

Keep a private task-local receipt outside Git when provider IDs are sensitive.
On resume, validate it, then observe the provider. The provider is canonical.
When recovery depends on nonsecret reports or screenshots held only in an
ephemeral directory, preserve the minimal necessary evidence in a bounded
private location with hashes. Do not archive raw chats, authentication pages,
credential-bearing provider dumps, or unrelated personal context.

## 9. Stop conditions

Stop after the requested state has direct evidence, or when the next transition
requires unavailable identity, a truthful human declaration, a provider review,
an exact artifact decision, or newly expanded authority. Report the strongest
proved phase, blocker, external object identity safe to share, and next
discriminator.

Create an asynchronous watcher only for an explicit monitor, wait, babysit, or
finish-through-review request. Bind stable provider/submission IDs, a baseline,
read-only checks, meaningful transitions, notification policy, and the requested
terminal state. Suppress unchanged observations. An intermediate transition may
notify and continue when the requested outcome is terminal review completion;
at terminal state, capture the final authoritative and user-surface proof, then
disable or delete the watcher. It must never mutate, retry, resubmit, publish,
or change release state. Do not create other dashboards, schedulers, CI, release
frameworks, or maintenance automation unless repeated work or an explicit
request justifies them.
