# Channel coverage

Delivery's non-Apple workflows were refreshed against official documentation and
selected public agent skills and release tools on **2026-09-10**. These are
instructions for an agent using an existing project and provider access. They
are not provider SDKs or a claim of completed live releases on every platform.

| Channel | First delivery and preparation | Update, uncertainty and recovery | Consumer evidence |
|---|---|---|---|
| [Google Play](../references/google-play-delivery.md) | Account/app eligibility, signing, release artifact and current policy, reviewer access, declarations, conditional native and Billing checks | Existing executor defaults, edit concurrency, exact track/version promotion, managed publication, halt/fix and optional recovery | Eligible tester and actual version/signature; release health with freshness; paid flows only when relevant |
| [Microsoft Store](../references/microsoft-store-delivery.md) | Dashboard bootstrap, one submission writer, MSIX versus hosted EXE/MSI, reviewer access and release timing | Draft replacement and API compatibility, private audience versus flights, certification and forward-version repair | Intended Store account, acquisition, installed version and package lifecycle |
| [Chrome Web Store](../references/chrome-web-store-delivery.md) | Package, permissions/data declarations, listing/reviewer packet, exact test audience | Uploaded versus submitted/published revisions, explicit publication and rollout defaults, eligible rules-only updates, pending draft and rollback limits | Correct item/version installed from the intended distribution path and its critical behavior |
| [LinkedIn and X](../references/social-delivery.md) | Per-request posting identity, content and media manifest, multipart/processing readiness, alt text where requested | Per-post and thread-segment reconciliation, scheduler job versus provider post, partial effects and authorized correction | Canonical post/author/content/media and reply relationships through the intended audience's access |
| [YouTube](../references/youtube-delivery.md) | Channel-role/API distinction, feature and quota eligibility, private upload, processing and optional captions | Confirmed resumable offset, metadata preservation, caption visibility, scheduled versus public state and audience-specific withdrawal | Exact video, playback and requested caption/thumbnail/link behavior on the relevant viewer surface |
| [Web](../references/web-production-delivery.md) | Managed platform versus operated origin, build environment, immutable deployment, data, DNS/TLS and access | [Pages, Workers, Vercel and Netlify](../references/web-managed-platforms.md) promotion and rollback; host/Tunnel state; partial deployment recovery | Current domain/revision, deep links, assets, critical API/auth flow and expected access denial |
| [AWS](../references/aws-delivery.md) | Existing account/region/service, immutable artifact, scoped roles and first-release recovery limits | [ECS, Lambda, stacks, S3/CloudFront and Lightsail](../references/aws-service-release-flows.md) control loops, active revision proof, asynchronous updates and rollback limits | Actual task/function/deployment revision, health/traffic and the application's intended consumer path |

Apple remains covered by its [dedicated reference](../references/apple-delivery.md).
The shared [control contract](../references/delivery-control-contract.md) binds
authority, artifacts, provider identity and recovery across all channels.

## How the guidance was checked

The refresh compared first-release, update, partial-failure and recovery scenarios
with current primary sources and inspectable tool implementations. Selected
public candidates are recorded in [source provenance](../references/source-provenance.md).
Only relevant mechanisms were adapted. No third-party skill pack, executable,
MCP server, credential store or hosted dependency was imported.

Source review, package/resource validation, local receipt tests and skill
discovery establish different things. They do **not** establish store approval,
current account eligibility, a live deployment, paid entitlement, actual user
installation or playback. Obtain those observations during the real delivery.
Mutable policies, quotas and executor defaults must be checked again for the
specific account, artifact, tool version and requested release.
