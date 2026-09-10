# AWS delivery adapter

Official AWS contracts checked **2026-08-24**. AWS service features, quotas,
runtime versions, deployment options and prices change. Observe the current
account/region/resource and official service contract during every release.
Consumer access guidance rechecked **2026-09-10**.
Service release lifecycles expanded and rechecked **2026-09-10** in
[AWS service release flows](aws-service-release-flows.md). Load the matching
service branch after binding identity below.

## Evidence boundary

This adapter provides service-neutral delivery guidance. It ships no AWS
credentials, account topology, infrastructure stack, or deployment executor.
Local helper tests do not prove resource readiness, production health, traffic
shift, recovery, or customer behavior. Obtain that evidence from the selected
account, service, and consumer path during the actual delivery.

## AWS identity and immutable revision

Bind:

- authenticated principal type and allowed operation without exposing identity
  credentials; exact AWS account, region and environment;
- service family and stable resource identifiers/tags: instance, container
  service/deployment, CodeDeploy app/group/deployment, ECS cluster/service/task
  definition, Lambda function/version/alias, bucket/distribution, or stack;
- current active deployment, traffic route, intended audience and access policy;
- exact source archive hash, image digest, versioned object, function version,
  task definition, stack template/change set or deployment revision;
- runtime/architecture, config schema, secret references, data/migration
  revision, network/security groups/firewalls, health checks and dependencies;
- desired traffic, downtime, alarms, cost delta, known-good revision and data
  recovery boundary.

An AWS CLI default profile, resource display name, mutable tag or remembered
region is not identity. Resolve image tags to digests and rendered infrastructure
to the provider revision that will actually run.

For a first release, mark the absence of a known-good deployment explicitly.
An existing service name is not a rollback baseline. Check whether the selected
executor also creates resources, runs migrations or switches traffic; classify
each real effect before using a command advertised as a preview or validation.

## Use the natural service owner

Do not redesign the platform inside delivery. Use the path already selected by
the project:

| Existing target | Provider state to bind | Minimum proof | Recovery semantics |
|---|---|---|---|
| Lightsail instance | instance/region, snapshot/backup, deployed revision, service/container | host process, origin health, logs, firewall and consumer path | redeploy known-good revision or create/restore replacement resource; IP/DNS may change |
| Lightsail container service | service, image digest, deployment version, intended public/private endpoint and health | deployment `Active`, intended endpoint health, logs and authorized consumer path | create a new deployment from a saved version; one running deployment at a time |
| EC2 with CodeDeploy | app, group, deployment configuration/revision | deployment/instance lifecycle, target health, logs and consumer path | rollback is a new deployment of the old revision; scripts/data are not undone |
| ECS | cluster, service, task definition/image digest, desired count, deployment/traffic | service stable, healthy tasks/targets, logs/alarms and consumer path | circuit breaker or a new service deployment; inspect traffic/task-set state |
| Lambda | function, immutable version, alias weights, event source | version/config, alias traffic, errors/latency and real invocation | shift alias to known-good version; external writes remain |
| S3/CloudFront | bucket/key versions or hashed assets, distribution/config, audience/access policy | exact object hashes, TLS/cache and page/assets through the intended authorization boundary | point to versioned files or invalidate narrowly; deleted/unversioned data may not return |
| CloudFormation/CDK | stack, template hash, change set and rendered resource diff | stack events/status plus service and consumer proof | stack rollback has resource-specific limits; continue/repair explicitly |

For Lightsail, inspect IPv4 and IPv6 firewalls independently; they govern
public-IP ingress and do not prove the private/Tunnel route. A snapshot restore
creates a new resource rather than rewinding the existing instance and can
change IP/DNS/cost. Automatic snapshot retention and deletion are tied to the
source resource, so preserve a manual snapshot only when the exact recovery
plan and cost preview require it.

CDK, GitHub Actions, Terraform, Kamal or another framework is an executor only
when the project already owns it. AWS Copilot CLI reached end of support on
2026-06-12 and must not be newly adopted; an existing Copilot project is legacy
state that needs a separate migration decision. Static inspection of these
tools informs deployment locks, immutable IDs, previews and stability waits;
it does not authorize introducing them. For CloudFormation, prefer current
native change sets or an already-owned maintained CLI; production delivery must
not use hotswap/express shortcuts as proof of the declared stack change.

## Preflight and authority

Use the least AWS permissions that can read state, preview and execute the
selected deployment. SSO/device authorization, access keys, session tokens,
SSH keys, secret values, signed URLs and connector credentials stay inside
official/protected channels. Do not print full environment/config responses or
create a durable access key/CI role for one operation.

Before deployment, prove:

- current provider deployment is reconciled and no conflicting mutation runs;
- artifact/image/template revision exists in the intended region/account;
- quota, capacity, disk and runtime support are sufficient;
- backup/snapshot scope, age, retention and restore mechanics are understood;
- migration and old/new-version compatibility are explicit;
- network exposure and firewall/security-group diff are intentional;
- health checks, logs, metrics and alarms distinguish startup from serving;
- expected downtime/traffic policy and a known-good recovery are executable;
- resource and data-transfer cost changes are visible.

AWS Budgets and billing data can lag and are alerts rather than hard caps. A
budget alarm is useful readiness evidence but neither permission to spend nor a
deployment-health signal.

Preview account, region, service/resource, immutable revision, exact provider
diff, traffic, health threshold, data/migration, network/IAM, expected downtime,
cost and recovery. The current exact delivery request may authorize the
production action; otherwise request one explicit approval. New resource creation,
public exposure, IAM broadening, deletion, snapshot removal, irreversible
migration or unexpected cost expansion always needs the applicable exact
authority.

## Observe one write and recover by identity

Use one writer and preserve the returned deployment/change set/task definition/
function version identity. Observe bounded provider state, target/service
health, logs, metrics and alarms. A timeout or disconnected SSH/CLI is
`effect_unknown`; query the exact provider objects and host revision before
retrying or switching to the console.

Rollback is service-specific. CodeDeploy implements rollback as a new
deployment. Lightsail snapshot restore can create a new resource. ECS and
Lambda can shift traffic to a prior immutable version. CloudFormation rollback
can fail or leave resources requiring continuation. None of these reverses
database migrations, queue consumption, emails, payments, external API writes
or secret rotation. Prefer roll-forward when old code cannot safely consume the
new state.

Provider `Active`, `CREATE_COMPLETE`, stable tasks or a healthy target is not
the terminal product proof. Verify the real application/API/mobile-client path
through its intended DNS, TLS, edge/tunnel/load balancer and authorization
boundary, and observe bounded post-cutover errors. Lightsail container services
can use only their private endpoint, and CloudFront can require signed URLs or
cookies. Preserve the intended access model: prove anonymous access for public
content, or authorized access and expected unauthorized denial for protected
content. Keep authentication material within the protected consumer session;
do not create public exposure to make a delivery check pass.

## Official sources

- [Lightsail instances and container services](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-container-services.html)
- [Lightsail container deployments and versions](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-container-services-deployments.html)
- [Lightsail snapshots](https://docs.aws.amazon.com/lightsail/latest/userguide/understanding-snapshots-in-amazon-lightsail.html)
- [Lightsail firewalls](https://docs.aws.amazon.com/lightsail/latest/userguide/understanding-firewall-and-port-mappings-in-amazon-lightsail.html)
- [Lightsail metrics and alarms](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-resource-health-metrics.html)
- [CodeDeploy deployment types](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments.html)
- [CodeDeploy rollback and redeploy](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments-rollback-and-redeploy.html)
- [ECS deployment failure detection](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-failure-detection.html)
- [Lambda weighted alias routing](https://docs.aws.amazon.com/lambda/latest/dg/configuring-alias-routing.html)
- [CloudFront invalidation and versioned files](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html)
- [CloudFront private content](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PrivateContent.html)
- [CloudFormation change sets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html)
- [AWS Budgets best practices](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-best-practices.html)
