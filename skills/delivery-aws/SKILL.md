---
name: delivery-aws
description: >-
  Deliver an existing app or backend through its project-owned AWS service:
  bind account, region, resource and immutable revision; deploy, recover, and
  prove health and traffic. Excludes cloud design and account bootstrap.
---

# AWS Delivery

Use this adapter when AWS owns the target compute, container, function, static
site, or deployment state. It composes `delivery-web` when a website/API
and edge route are part of the outcome. Read the
[shared control contract](../../references/delivery-control-contract.md) and
[AWS delivery reference](../../references/aws-delivery.md).
Then load only the relevant branch of
[service release flows](../../references/aws-service-release-flows.md) for ECS,
Lambda, stacks, static delivery or Lightsail/CodeDeploy.

## Deliver Through The Existing AWS Owner

1. Observe the caller identity without exposing credentials. Bind account, region,
   environment, service family, stable resource IDs/tags, current deployment,
   traffic route, dependencies, data stores, intended endpoint and audience,
   access controls, alarms and cost posture. Never infer production from a
   default CLI profile, resource name, old handoff, or region remembered from
   another app.
2. Select the project's existing service and deployment owner: Lightsail
   instance/container service, EC2/CodeDeploy, ECS, Lambda alias, S3/CloudFront,
   CloudFormation/CDK, or another already-adopted route. AWS Copilot CLI reached
   end of support in 2026 and is not a new delivery choice; treat an existing
   Copilot project as legacy state with an explicit migration boundary. Feature-probe
   current AWS CLI/provider state and project scripts. Do not migrate services,
   introduce infrastructure as code, create a CI role, or add CDK/Kamal
   merely to perform one release.
3. Bind an immutable epoch: source revision/archive hash, container image
   digest or versioned object, rendered task/function/stack/deployment revision,
   configuration schema, secret references, data/migration revision,
   architecture/runtime, target resource, desired traffic, and recovery target.
   A mutable image tag can be a locator only; resolve and record the digest.
4. Preflight the exact service: planned provider diff/change set, IAM ability
   needed for this operation, quotas/capacity, disk and image availability,
   backup/snapshot/restore reality, secret and encryption custody, network and
   firewall exposure, health checks, logs/metrics/alarms, deployment concurrency,
   downtime, migration compatibility, and cost delta. AWS Budgets alert; they
   do not guarantee a hard cap or healthy release.
5. Prefer a reversible stage or zero-traffic revision when supported. Verify
   service health before traffic. Bind the exact transition: registered task
   definition versus running task, updated function versus published version
   versus alias, or prepared versus executed change set. On a first release,
   record that no earlier healthy revision exists. For a single in-place host, take the
   project-defined backup, dry-run the file/config transition, keep secrets and
   mutable data outside the release snapshot, and prove the prior revision can
   actually be redeployed or restored.
6. Preview exact account/region/resource, revision/digest, provider diff,
   traffic and health policy, data/migration effect, network change, cost,
   expected downtime, and recovery. Apply the shared authority contract: an
   exact current request can authorize its named deployment and traffic cutover.
   Request approval for unapproved resource creation, resource or snapshot
   deletion, IAM or public-exposure expansion, irreversible migration, unexpected cost,
   required human attestation, or a non-exact production request.
7. Execute once using the one selected writer. Preserve the deployment/change-
   set/task/function/version identity; honor an existing target-scoped deploy
   lock and observe provider status, instance or
   task health, target health, logs and alarms. After a timeout, query those
   identities before retrying or switching to the console.
8. Prove the service and its consumer boundary: exact active revision/digest,
   desired instance/task/function count, healthy provider state, no new critical
   errors/alarms, and the actual application/API/mobile path through its intended
   public or private endpoint and authorization boundary. For protected content,
   verify authorized consumer access and expected denial to unauthorized
   requests; do not add a public endpoint or weaken access controls to obtain
   proof. In particular, check Lambda's update result as well as `State`, the
   actual ECS task digests, and the active Lightsail deployment version: a
   failed update can leave old code healthy. A green deployment alone is not
   product delivery.

## Recovery Boundary

- CodeDeploy rollback is a new deployment of an older revision. ECS, Lambda,
  Lightsail and CloudFormation each have different traffic and recovery state;
  use the live service contract rather than the word “rollback.”
- A previous binary or image may be incompatible with a completed schema
  migration or external side effect. Choose roll-forward or a separately
  approved data recovery when rollback cannot restore consistency.
- A snapshot proves recoverable bytes only after its scope, age, retention and
  restore path are understood. Creating a replacement resource may change IPs,
  DNS, credentials and cost.
- Keep AWS access keys, session tokens, SSO/device codes, SSH keys, tunnel
  credentials, secret values and signed URLs inside official or protected
  credential channels. Do not print broad IAM state or secret-bearing config.

Report `prepared`, `staged`, `deploying`, `active`, `traffic shifted`,
`recovered`, or `consumer-verified` exactly, plus current AWS identifiers safe
to share and any remaining external blocker.
