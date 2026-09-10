---
name: delivery-web
description: >-
  Deliver a website or API on an existing host: bind revision, origin,
  process, data, DNS, TLS and Cloudflare ingress; deploy once, recover safely,
  and prove intended consumer access. Excludes implementation and cloud
  architecture redesign.
---

# Web Production Delivery

Use this lane for an existing website/API/backend moving to or updating a
production hostname, including an Ubuntu host, Docker/systemd origin,
Cloudflare Tunnel, reverse proxy, static host, or project-owned platform. When
AWS owns the compute or managed service, compose `delivery-aws`. Read the
[shared control contract](../../references/delivery-control-contract.md) and
[web production reference](../../references/web-production-delivery.md).

## Deliver

1. Define the terminal effect: prepare a deployable revision, stage an origin,
   deploy production, cut over traffic, recover, or verify. Bind the canonical
   hostname and user path, owner/provider account, origin host, environment,
   process/service, listener, ingress/tunnel/proxy, DNS zone/record, TLS mode,
   data stores, release mode, intended audience and access controls, and current
   live revision. Similar hostnames or containers are not identity.
2. Bind one immutable release input: exact source revision or source archive,
   dirty-state decision, artifact/image digest, config schema, runtime and
   dependency lock, migration revision, public asset manifest, and secret
   references without values. Never deploy an unexamined mutable working tree,
   `latest` image, or locally generated file under an old receipt.
3. Read project-native deployment docs and live topology. Prove clean or
   intentionally captured source, disk/capacity, backup/restore readiness,
   secret custody, dependency availability, process ownership, port binding,
   health endpoint, logs, firewall, ingress match, DNS/TLS, monitoring and an
   executable known-good recovery. Use dry-run diff/sync or provider preview
   before changing bytes.
4. Stage where the topology permits: build and inspect offline, deploy a new
   version alongside old, or start behind a nonpublic/zero-traffic route. Run
   origin-level health and product-critical smoke before traffic cutover. A
   process that merely started is not healthy.
5. For Cloudflare Tunnel production, bind the existing tunnel and its management
   mode. For a locally managed tunnel, validate its actual ingress configuration,
   rule matching, and final catch-all. For a remotely managed tunnel, inspect
   the effective routes and origin parameters through its dashboard or API;
   a local configuration check does not verify those routes. Preserve the
   management mode, protected connector credential, active connector evidence,
   and intended loopback/private origin. A Quick Tunnel is preview evidence
   only. Do not replace the tunnel, expose the origin publicly, or broaden
   ingress because discovery was incomplete.
6. Preview revision/digest, target host and service, file/config/migration diff,
   backup, expected downtime, origin and consumer checks, hostname/DNS/TLS,
   cache behavior, traffic transition, cost impact, and recovery command or
   provider action. Apply the shared authority contract: an exact current
   request can authorize its named DNS/traffic cutover. Request approval when
   that effect was not authorized precisely, production intent is ambiguous, authority must
   expand, or the transition adds an irreversible migration, unexpected resource
   or cost exposure, destructive action, or required human attestation.
7. Execute one bounded deployment and observe it by deployment/process identity.
   Acquire the project's existing target-scoped deploy lock when present; do
   not invent a lock service for one host.
   On disconnect or unknown result, inspect host files, service/container state,
   provider deployment, logs, origin health and deployed revision evidence before
   any repeat. Do not alternate between SSH, CI and dashboard writers.
8. Prove both boundaries: origin/service health from its trust boundary, then
   the intended consumer path through DNS, TLS, edge/tunnel/proxy and cache.
   For public content, verify anonymous access. For protected content, verify
   the expected anonymous denial or sign-in challenge where reachable, then
   use an authorized consumer session or client to identify the exact release
   and exercise its critical behavior. Preserve access controls; a public
   hostname does not imply public content. Observe errors and logs after
   cutover for a bounded period proportional to risk.

## Recovery And Stop

Rollback means an executable provider-specific transition to a known-good
revision. It does not reverse database writes, migrations, DNS caches, external
side effects, or secret rotation. Prefer roll-forward when state compatibility
makes a binary rollback unsafe. Test or inspect the recovery path before the
consequential transition; do not invent it after an outage.

Stop as `origin staged`, `deployed`, `traffic cut over`, or `consumer verified`;
use `publicly verified` only when the intended content is public.
If review, DNS propagation, certificate issuance, health, data compatibility,
or access remains unresolved, preserve exact live state and the next read-only
discriminator.
