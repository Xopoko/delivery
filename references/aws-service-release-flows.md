# AWS service release flows

Lifecycle contracts checked **2026-09-10**. Load only the selected service branch
after [AWS identity and authority](aws-delivery.md). These are control loops for
an existing project, not ready-to-run infrastructure templates or IAM policies.

## Container artifact and role preflight

Resolve the image's registry/account/region, digest, OS/architecture and required
sidecars. Confirm the deploy target can retrieve that exact image, including
network and registry access. Retain known-good digests against lifecycle cleanup:
a running task does not prove its image will remain pullable during recovery.
Changing a mutable tag does not change an existing task or prove the new digest
will run. Inspect the project's render/build result before registering it.

Distinguish deployer authority, task execution role and application task role.
For ECS, narrowly scoped `iam:PassRole` may be needed for the roles referenced by
the task definition; image pulls, logs and secret retrieval belong to the actual
execution path. Fix the identified permission or network boundary rather than
granting broad administrative access. Keep registry tokens and secret values
inside the existing protected integration.

Source: [ECS deployment action and scoped permissions at an inspected revision](https://github.com/aws-actions/amazon-ecs-deploy-task-definition/blob/10a12db2b4741703f03060448e2c9f1f6fa9c140/README.md).

## ECS

1. Bind cluster/service, launch type, deployment controller/strategy, current
   task definition, desired count, target groups, health grace period, active
   deployment and recovery revision. Check capacity and startup dependencies.
2. Render the exact task definition with each changed container's immutable
   image. Register or use that revision through the existing owner, then update
   the service once. A new registered task definition alone does not change the
   service; `forceNewDeployment` is a deployment effect, not a read-only refresh.
3. Observe the requested deployment, service events, task startup/stopped reasons
   and target health. Verify running tasks use the intended task definition and
   actual image digest. A zero-desired-count service cannot prove the image runs.
   Digest resolution can fail, so do not assume tag-based consistency succeeded.
4. Inspect rollback availability for the current strategy. Automatic rollback
   requires a previous successful deployment; a first release has no such
   baseline. Bind alarms and the observation window before cutover. Early
   completion criteria can end automatic rollback monitoring before all desired
   replacement tasks are healthy; check the actual population and consumer path.
5. On failure, inspect the deployment ID before another update. Distinguish
   startup/image-pull failure from application or target-group failure. Reconcile
   automatic rollback to the known-good revision or execute the authorized
   recovery; retain the failed revision's bounded diagnostics.

Sources: [rolling deployments and image version consistency](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html),
[deployment failure detection](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-failure-detection.html),
[early success criteria](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/early-success-criteria.html).

## Lambda

Bind the function, package type/hash or image digest, architecture/runtime,
configuration and layer versions, current `RevisionId`, published version,
alias weights, event-source mapping and API/function-URL route. A successful
test of `$LATEST` does not prove consumers invoke that code.

After updating code/configuration, wait for both function readiness and
`LastUpdateStatus=Successful`. `State=Active` alone can coexist with an update
in progress or a failed update while requests still execute old code. Compare
the returned code/config revision with the intended artifact before publishing.
When supported by the existing tool, use `CodeSha256`/`RevisionId` guards to
avoid publishing a concurrent writer's version.

Publish an immutable version, verify the qualified version, then change the
intended alias/traffic through the existing deployment owner. A published
version alone does not move an alias or an event source. For weighted release,
observe errors/latency for each version and verify the actual consumer route.
Use a known safe, scoped probe; invoking an event handler can send messages or
write data, and an asynchronous acceptance is not proof of successful handling.

If the update or publish response is ambiguous, read the function, version list,
code hash and alias before another write. Rollback shifts the alias to a retained
compatible version; it does not replay or reverse consumed events, external
writes or storage migrations. Keep `sam sync` and CDK hotswap in development;
production uses the project's full deployment path.

Sources: [function and update states](https://docs.aws.amazon.com/lambda/latest/dg/functions-states.html),
[publishing with revision/hash guards](https://docs.aws.amazon.com/lambda/latest/api/API_PublishVersion.html),
[weighted aliases](https://docs.aws.amazon.com/lambda/latest/dg/configuring-alias-routing.html),
[SAM sync scope](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/using-sam-cli-sync.html).

## CloudFormation, CDK and SAM

Inspect the exact stack, template/asset hashes, parameters without secrets,
execution role and current state. Use the project's normal synth/package/change-
set path. Review additions, replacements, deletions, IAM changes, data resources
and expected cost before execution. Creating a change set does not execute it
or guarantee that quotas, permissions and resource updates will succeed.

Execute the bound change set once and retain stack/change-set identity. Watch
events to a terminal state, then verify each affected service and consumer path.
An empty/no-change result is a valid no-op only if the active revision satisfies
the requested outcome. After disconnect, read the existing stack operation.

For `UPDATE_ROLLBACK_FAILED`, identify the failed resource and cause before
continuing rollback. Correct the narrow issue and use the provider's recovery
flow; skipping/orphaning a resource can leave template and resource inconsistent
and needs an explicit reconciliation plan. Do not delete the stack as generic
cleanup or synthesize a fresh stack to hide the failure. A first-create failure
also needs inspection of retained resources and data before retry or replacement.

Sources: [change sets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html),
[rollback failure troubleshooting](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/troubleshooting.html),
[stack failure options](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stack-failure-options.html).

## S3 and CloudFront

Bind the build manifest, bucket/key or object-version identities, distribution,
origin/access policy, cache settings and intended hostname. Prefer immutable
asset names. For a file-by-file release, upload referenced assets before the
entrypoint/manifest that makes them discoverable; avoid exposing mixed revisions
after an interrupted upload. Retain the previous entrypoint and its assets.

Verify uploaded bytes against the build using a supported checksum or direct
content comparison; do not assume a generic ETag is the build's SHA-256. Preserve
private origins and the existing CloudFront access mechanism. A bucket need not
be public for the site or signed-content distribution to work.

Bind any invalidation request and wait for its status, then verify the intended
domain and key pages/assets. CDN invalidation does not necessarily clear browser
or intermediary caches. A narrow cache correction or versioned asset reference
is preferable to repeatedly overwriting/deleting the whole site. Rollback restores
the retained entrypoint/object versions and its references, with cache-aware
consumer checks; it does not restore unretained or deleted data.

Sources: [CloudFront invalidation versus versioned files](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html),
[S3 checksums and ETag limits](https://docs.aws.amazon.com/AmazonS3/latest/userguide/checking-object-integrity-upload.html).

## Lightsail containers and existing hosts

For a container service, bind the full deployment's images, command, ports and
health-check configuration; select the intended endpoint container and port
only if the service uses a public endpoint. Record the new deployment version
and read its own state. If activation fails, a previously healthy deployment
can remain active while the service still says running. Compare the active
version with the requested one and inspect failed-container logs. On the first
release the service may instead remain ready without any active deployment.

For existing Lightsail/EC2 hosts, retain the revision and project-defined
service/file transition, backup and origin checks from
[web delivery](web-production-delivery.md). If CodeDeploy owns the deployment,
bind its group/revision/lifecycle and load-balancer traffic; a successful rollback
is a separate deployment of old code, not an undo of lifecycle scripts or data.
Do not switch deployment owners during uncertain recovery.

Sources: [Lightsail deployment failures](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-container-services-deployments.html),
[CodeDeploy rollback](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments-rollback-and-redeploy.html).
