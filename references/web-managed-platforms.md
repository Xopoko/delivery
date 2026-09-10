# Managed web and edge releases

Lifecycle contracts checked **2026-09-10**. Use only the branch already owned by
the project. This reference supplements [web delivery](web-production-delivery.md);
it does not require a new host, account, framework, CLI or CI workflow.

## Bind the build before the deployment

Resolve the existing team/account, site/project ID, production branch, monorepo
root, build command, output directory, framework adapter, runtime and dependency
lock. Inspect project-local CLI help and the actual wrapper: a command named
`deploy`, `preview` or `upload` does not establish its effect. A Git push can
trigger production automatically. Identify that trigger before pushing.

Bind the build's environment and configuration to the artifact. Browser-exposed
variables are public bundle content; secrets must stay in the server/provider's
protected channel. A deployment flag cannot generally rewrite values already
baked into JavaScript or a generated config. Use the project's existing secret
binding; do not download or print its environment to demonstrate readiness.

Capture immutable deployment ID/permalink and the source/build revision before
using a moving branch alias or production domain. Verify preview access policy:
a preview URL can be public, and a preview build can still write production data
through shared bindings. No production traffic does not mean no external effect.
For first delivery, discover or explicitly authorize the project and domain;
do not interpret a failed lookup as permission to create a duplicate site.

## Cloudflare Pages

Identify Git integration versus Direct Upload and the existing production branch.
Direct Upload accepts the verified build output. A Git-connected build must
resolve the intended commit and its build context. Project mode is a creation
choice: switching it requires a separate migration, although a Git-integrated
project can also receive Wrangler uploads after automatic builds are controlled.
Do not recreate the project merely to use a different upload tool.

Check which branch/context the selected upload will target. Preserve the exact
deployment ID, build result, preview URL and production alias separately. Verify
the output directory includes required functions/routing/assets through the
project's framework adapter; a successful static upload cannot prove server-side
routes were included. On an uncertain upload, inspect deployments by project,
commit, branch and time before creating another one. Before rollback, inspect
retained production deployments and current automatic-build behavior.

Sources: [Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/),
[Git integration and direct CLI deployments](https://developers.cloudflare.com/pages/configuration/git-integration/).

## Cloudflare Workers

Use the repository's Wrangler/config generator as the configuration owner.
Confirm the selected environment's Worker name, resource IDs, bindings, secret
references, compatibility settings and routes; do not rely on inheritance or
dashboard state to supply omitted settings. Compare generated output with source
without editing a generated file. With the Cloudflare Vite plugin, select
`CLOUDFLARE_ENV` at **build** time: the generated config is flattened and changing
that variable at `wrangler deploy` time does not retarget it.

Distinguish these effects before choosing the project's command:

| Operation | Effect to bind |
|---|---|
| `wrangler versions upload` | Creates a version; does not switch production traffic |
| `wrangler versions deploy` | Assigns traffic to the selected version(s) |
| `wrangler deploy` / default Workers Builds | Creates a version and immediately deploys to 100% |
| `wrangler secret put` | Creates a version and immediately deploys it; it is a release mutation |
| `wrangler versions secret put` | Creates a version for later deployment |
| Trigger deployment | Applies routes, domains or cron configuration separately from a version upload |

Feature-probe exact syntax and supported behavior in the installed version.
Before gradual delivery, retain both version IDs, intended weights, compatible
bindings and a recovery version. Requests can hit different versions; check
cross-version API and stored-data compatibility. Observe actual version-specific
errors and consumer behavior before changing weights. Multi-Worker deployments
are not automatically atomic: record each stage and resume from actual state.

Rollback makes the chosen version active at 100%. It does not restore connected
data stores; deleted resources and certain Durable Object lifecycle changes can
prevent it. Preserve required bindings and data compatibility rather than
promising that any prior version is recoverable.

Sources: [Wrangler skill at an inspected revision](https://github.com/cloudflare/skills/blob/b052c32bab7dd493513260228a36c88294f343f1/skills/wrangler/SKILL.md),
[Vite environments](https://developers.cloudflare.com/workers/vite-plugin/reference/cloudflare-environments/),
[deployment management](https://developers.cloudflare.com/workers/versions-and-deployments/deployment-management/),
[secrets](https://developers.cloudflare.com/workers/configuration/secrets/),
[gradual deployments](https://developers.cloudflare.com/workers/versions-and-deployments/gradual-deployments/),
[rollback limits](https://developers.cloudflare.com/workers/versions-and-deployments/rollbacks/).

## Vercel

Resolve the linked project/team and deployment environment. Preview and production
can have different build-time variables. Promoting a preview to production creates
a production deployment through a rebuild; verify the resulting production build
and new ID. Promoting a staged **production** build does not rebuild it. Neither
operation is proved by an earlier preview screenshot alone.

Confirm domain auto-assignment and production-branch triggers. If a production
build is intentionally staged without domains, bind that state explicitly before
promotion. After a timeout, inspect the promotion and current deployment rather
than repeating the command. Instant rollback reassigns domains to a retained
deployment without rebuilding its environment. Check data compatibility, retained
artifacts and subsequent auto-deploy behavior before relying on it.

Sources: [promotion behavior](https://vercel.com/docs/deployments/promoting-a-deployment),
[promotion status](https://vercel.com/docs/cli/promote),
[environment variables](https://vercel.com/docs/environment-variables).

## Netlify

Resolve the existing site/team, deploy context, build command, publish directory,
functions and edge-function output. Preserve deploy ID/permalink independently
from the production site URL and moving branch/preview aliases. A new deploy is
atomic for its uploaded assets; do not apply a file-by-file SSH release procedure.
Check the selected CLI's draft/production and build flags instead of assuming
that every `deploy` invocation rebuilds the project.

Read whether the deploy is building, failed, pending permission, successful or
actually published. Rollback publishes a retained successful deploy without a
new build. With auto-publishing enabled, the next Git-triggered production deploy
can replace it. Bind any authorized publish-lock change and its eventual release;
do not silently leave the project frozen. Database state is separate from the
code/asset rollback and may require roll-forward or explicit data recovery.

Sources: [atomic deploys](https://docs.netlify.com/deploy/deploy-overview/),
[publish, rollback and locked deploys](https://docs.netlify.com/deploy/manage-deploys/manage-deploys-overview/),
[deployment URL identities](https://docs.netlify.com/manage/domains/domains-fundamentals/understand-domains/),
[database recovery boundary](https://docs.netlify.com/build/data-and-storage/netlify-database/backup-and-recovery/).

## Consumer proof and recovery

Use the immutable deployment URL to identify what was built, then the intended
domain to prove what receives traffic. Check a direct deep link/reload, critical
static assets or split chunks, redirects and the relevant API/auth path. Where
applicable, verify function execution and cache/service-worker behavior; a 200
HTML fallback for a missing JavaScript file is not a working application.

If a provider reports success but the domain serves the old revision, inspect
domain assignment, selected environment, cache and deployment identity first.
If a page loads but its API fails, inspect function inclusion and bound backend
configuration without exposing values. Keep expected unauthorized denial intact.
On failure preserve the last healthy deployment and the partial state; rollback
only to an available revision compatible with current data and dependencies.
