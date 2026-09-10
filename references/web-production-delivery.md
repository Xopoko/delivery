# Web production delivery

Official Cloudflare contracts checked **2026-08-24**. This runbook is
provider-neutral at the origin and composes the project's existing platform.
It does not choose a cloud architecture or teach application implementation.
Tunnel management and consumer access guidance rechecked **2026-09-10**.
Managed-host and edge lifecycles checked **2026-09-10** in the
[managed platform reference](web-managed-platforms.md).

## Evidence boundary

This runbook is deployment guidance, not a bundled host configuration or a live
availability claim. Discover the project's current origin, edge, deployment
owner, and recovery path. Local helper tests do not prove DNS, TLS, active
traffic, a healthy production origin, or a successful rollback. Mutable image
tags and in-place rebuilds require particular care because they can prevent an
exact revision from being identified or restored.

## Production epoch

Bind one deployment epoch:

```text
owner/account + environment + canonical hostname + host/service or managed project
+ applicable listener/ingress/tunnel/proxy + DNS/TLS route + exact build/deployment ID
+ source revision/artifact/image digest
+ config schema + secret-reference revision + data/migration revision
+ release effect + traffic mode + audience/access policy + known-good recovery target
```

Record stable nonsensitive IDs, hashes, ports and public hostnames needed for
recovery. Keep private host paths task-local when possible. Never record secret
values, connector tokens/credentials, SSH keys, environment files, signed URLs,
database dumps, customer data or raw config responses.

## Observe and preflight

Read repository guidance and live topology before choosing commands:

Choose the existing deployment owner first. For managed static/edge platforms,
read the [managed platform flow](web-managed-platforms.md): bind the project,
build environment, deployment ID and domain assignment. SSH, a process supervisor
and listening ports are host-specific checks, not prerequisites for managed
hosting. For an origin you operate, apply the host checks below; inspect only
components present in the actual route.

1. source revision and dirty state; build/runtime lock files; current artifact
   or image digest; current deployed revision evidence;
2. host identity, OS/runtime, disk/memory, process supervisor, service/container
   ownership, listeners and dependencies;
3. configuration schema and secret references; mutable data volumes; database
   and migration state; backups, retention and an actual restore path;
4. origin health endpoint, startup/readiness behavior, logs and bounded error
   baseline;
5. reverse proxy or Tunnel ingress, origin binding and trust model, DNS record,
   TLS mode/certificate and cache behavior;
6. current consumer route, intended audience and access controls, redirects,
   critical browser/API path, monitoring, alarms, expected downtime and
   known-good recovery.

The deployed input must be reproducible. Prefer an exact commit archive,
versioned package or immutable image digest. `git archive` is useful when the
contract intentionally excludes untracked state and secrets. Use a dry-run
file sync/diff before the write. A mutable tag such as `latest` may remain a
project locator only if the actual digest is resolved and bound.

Backups are scoped evidence: name included data/config, excluded secrets,
timestamp, hash, retention and restore consequence. A successful backup command
does not prove restoration. Database migrations need forward/backward
compatibility and roll-forward/restore decisions before deployment.

## Deploy and shift traffic

Use one existing owner: project script, service manager/container workflow,
provider deployment, or CI release. Do not let SSH, dashboard and CI race to
write the same service.

Prefer the cheapest reversible stage:

- build and inspect off-host;
- start a new revision behind a nonpublic listener;
- deploy a versioned directory/container/task next to the old revision;
- create a provider preview/zero-traffic version;
- run migrations in the project-defined safe order;
- prove origin health before DNS/route/traffic change.

A provider preview may already be publicly reachable and can use production
backend bindings. Verify its intended access and side effects before staging.
For managed deployments, build readiness and preview proof precede a separately
bound domain promotion; a successful build is not necessarily serving traffic.

On a single in-place host, capture the current revision and service/config
state, take the required backup, dry-run the transition, set an explicit
downtime expectation, update once, and observe supervisor/container state plus
logs. A restart receipt is not health.

## Cloudflare Tunnel contract

For production, bind the existing tunnel ID/name, connector/service, management
mode, hostname route and origin service. Preserve the current management mode:

- Locally managed: validate the actual local ingress configuration, rule
  matching, and its final catch-all rule.
- Remotely managed: inspect the effective route configuration and origin
  parameters through the dashboard or API. Cloudflare stores this configuration;
  validating a local file does not prove the active remote routes.

Verify active connector/HA connection evidence and the expected DNS route to
the tunnel. Quick Tunnels are temporary preview paths, not a production identity
or release receipt.

Replicas of one tunnel provide availability, not deterministic blue/green
traffic: Cloudflare does not guarantee which replica receives a request. Do not
run different application revisions behind replicas and call that a controlled
rollout. Use a stable local proxy cutover, separate origins/tunnels with the
project's existing load-balancing route, or another explicitly owned strategy.

Prefer a loopback or private-network origin and a host firewall that does not
open the application port publicly when Tunnel is intended to be the only
ingress. Authenticated Origin Pulls do not protect a Cloudflare Tunnel origin in
the same way they protect direct proxied HTTPS origins; establish origin trust
from the actual tunnel/network/listener boundary. Cloudflare account
certificates, tunnel credential files and remotely managed connector tokens
have different scope but are all protected material.

A connector being connected proves only the transport. Separately prove:

- the intended ingress rule selects the intended origin;
- origin health succeeds at its local/private boundary;
- DNS and TLS resolve for the canonical hostname;
- the intended consumer path returns the expected exact revision and behavior;
- public content is anonymously accessible; protected content requires the
  intended authorization, and unauthenticated requests receive the expected
  denial or sign-in challenge where the endpoint is reachable;
- cache does not hide the old release. Prefer versioned assets or the narrowest
  cache purge; do not purge everything by reflex.

Cloudflare Access can protect an application behind a public hostname. Preserve
its policies and token validation, then verify the product through an authorized
consumer session or client. A public hostname or healthy tunnel does not require
making the application anonymously readable.

DNS proxied records commonly use automatic TTL, but local caches and certificate
issuance can outlast a dashboard change. Preserve observed state instead of
declaring propagation complete by elapsed time.

## Ambiguity, rollback and proof

After a connection loss, inspect exact file/image revision, service/container
identity, deployment record, logs, origin health, connector state, DNS/TLS and
deployed revision evidence. Do not rerun a deploy until the first effect is known.

Rollback is not one universal command. It can be a traffic switch to a healthy
old version, redeployment of a known-good artifact, provider rollback, or a
separately approved restore. It does not automatically reverse migrations,
external writes, queues, DNS caches, certificate changes or secrets. If the old
binary is data-incompatible, stop and roll forward or invoke the pre-agreed data
recovery boundary.

Completion evidence:

- `origin_staged`: exact revision passes health/smoke behind the intended staged
  access boundary; identify any publicly reachable preview explicitly;
- `deployed`: supervisor/provider reports exact revision healthy on target;
- `traffic_cut_over`: canonical route targets that revision;
- `consumer_verified`: the intended HTTPS DNS/TLS/edge path and product-critical
  browser/API flow identify the exact revision under the required access policy,
  with bounded post-cutover logs and error signals observed;
- `publicly_verified`: additionally, the intended public content and behavior
  are anonymously accessible. Use this state only for a public audience.

## Official Cloudflare sources

- [Cloudflare Tunnel overview and connector model](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/)
- [Tunnel deployment guides](https://developers.cloudflare.com/tunnel/deployment-guides/)
- [Set up a named Tunnel](https://developers.cloudflare.com/tunnel/setup/)
- [Quick Tunnels are for testing](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/)
- [Tunnel and replica terminology](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/get-started/tunnel-useful-terms/)
- [Route DNS or an application to a Tunnel](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/routing-to-tunnel/)
- [Locally managed ingress configuration](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/local-management/configuration-file/)
- [Local and remote tunnel management](https://developers.cloudflare.com/tunnel/advanced/local-management/)
- [Protect a published application with Access](https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/self-hosted-public-app/)
- [Tunnel credential scopes](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/local-management/tunnel-permissions/)
- [Run parameters and connector tokens](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/configure-tunnels/run-parameters/)
- [Tunnel metrics](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/monitor-tunnels/metrics/)
- [Authenticated Origin Pulls limitations](https://developers.cloudflare.com/ssl/origin-configuration/authenticated-origin-pull/)
- [DNS TTL behavior](https://developers.cloudflare.com/dns/manage-dns-records/reference/ttl/)
- [Purge cache](https://developers.cloudflare.com/cache/how-to/purge-cache/)
