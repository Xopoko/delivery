# Delivery source provenance

Initial observation date: 2026-08-24. Non-Apple refresh: **2026-09-10**.

Delivery's provider guidance synthesizes mechanisms and failure boundaries
from the candidates below. The retained synthesis records report static
inspection at immutable commits, with no candidate executable code run or MCP
server installed. Platform behavior remains governed by current official
documentation and live provider state.

## Public candidates inspected

| Candidate | Commit | Mechanism retained or rejected |
|---|---|---|
| `android/skills` | `6685cac2923e3ccc7e5c385019464374699cda95` | Current-policy discovery as a separate step; no frozen policy claims |
| `microsoft/msstore-cli` | `1bbca9610025efb173c38cb3030b31e41f497346` | Draft/no-commit and status/poll surfaces; runtime availability must be probed |
| `Triple-T/gradle-play-publisher` | `abb096156789e9c967be435f6fee7caeca5529a8` | Project-native track/release automation only when already adopted |
| `fastlane/fastlane` | `a9a72554e1f4d6658842d4f3a7b0ca236b5c1589` | Existing project workflow composition, not default dependency introduction |
| `expo/skills` | `472d040092900dc8bbf84dc7efb0c90abff77a0d` | Existing EAS submit route with explicit paid/cloud boundary |
| `Bin-Huang/youtube-data-cli` | `10a1b87277969588bab73d3ca4227e6b14593566` | Data API surface inventory; credential-file behavior rejected |
| `DraconDev/youtube-video-uploader` | `771d422155b3d24c2598209de9ac6f6acb0045e6` | Resumable upload evidence; low-maturity credential patterns rejected |
| `sosteam65/app-store-connect-skill` | `4b905ade2bf20d2bc6e7a8da8f1bf628d5d1de61` | Agent routing patterns; secret-in-environment examples rejected |
| `rorkai/app-store-connect-cli-skills` | `3f71de280bdf8773910ef3699fa770dffbe24012` | App Store Connect capability decomposition without copying command catalogs |
| `mikusnuz/app-publish-mcp` | `9749d8d352872321941e351c58dffb55fe93fa6b` | MCP publication surface inspected; rejected as incomplete extra credential boundary |
| `pampas93/fastlane-mcp` | `39e0736945b9d51633ed7cb71707c75a74f39b79` | MCP wrapper inspected; rejected in favor of an existing project-native fastlane path |
| `lusky3/play-store-mcp` | `ebdd9fdd4caa66180b8e5cbc58df5794248140a2` | Play MCP inspected; rejected for incomplete bootstrap/policy coverage and secret surface |
| `GoogleChrome/modern-web-guidance` | `460e5536b8e61034d83ff4af24bb0bf1112d2cb0` | Extension publishing checklist and policy-oriented package review; official provider state remains canonical |
| `aklinker1/publish-browser-extension` | `8ce1e500903796f738636a9ea741e76dae7e8985` | API v2 upload-only, staged publish, warnings and rollout mechanisms; framework and secret-file defaults rejected |
| `fregante/chrome-webstore-upload` / CLI | `25a6b4cf3d714f4eca920673c4c2460dd3a8b797` / `07b39cee24e05203caf5c9dce7b36907b932c5c4` | Upload polling and explicit publication modes; incomplete dashboard/privacy/recovery coverage and environment-secret defaults rejected |
| `VaughnBosu/cws-cli` | `0fd7b1ddecfbc187529c9153ef128a6923b8e769` | Validate/package/status/rollout/cancel JSON surface; low maturity and plaintext credential wizard reject default adoption |
| `PlasmoHQ/bpp` | `82f236cc7fc8e28941bbd1e080ace0121c7a5a92` | Cross-store artifact/version mapping only; legacy credential and incomplete v2 state handling rejected |
| `langchain-ai/deepagents` | `4b4928613262ac23d419f0e8788f24412a8fdafb` | Source-backed social content shaping; campaign expansion and publication authority are not inherited |
| `LocoreMind/locoagent` | `c01bb3f8a7b06a0db9f697c5bea485947959d226` | Browser posting patterns inspected and rejected because LinkedIn/X prohibit website activity automation |
| `philipbankier/zernio-social-skill` | `b49b8d971993d11e5cd81ab5b8329ecd30f654ce` | Social scheduling/publishing surface inspected; paid dependency and credential boundary rejected as a default |
| `linkedin-developers/linkedin-api-python-client` | `6331e52f5ea59b326447efa67a9bf925ed2d9ec7` | Rest.li headers, URN/query and returned entity identity; beta/old client and special license reject default dependency |
| `xdevplatform/xurl` | `41259e8aef85f847145c383d02be6a40a2435466` | Official optional API/PKCE/media-status CLI for an already-owned route; plaintext token custody and token output rejected |
| `coollabsio/shoutrrr` | `e0b896cbcbb8cfe677c261360e2afba3517f1991` | Per-target/thread-segment receipts only; scheduler, queue, analytics, vault, generic retry and stale platform limits rejected |
| `openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | Provider routing and preview/production separation; automatic network retry, environment-specific escalation and suppression of consumer verification rejected |
| `cloudflare/skills` | `f96bff754e428838818017f75817f0f9428acd48` | Provider capability routing only; product catalog and command breadth not copied |
| `cloudflare/cloudflared` | `d1df7985bdf189c4caf34e290bafbf8f411e603b` | Active edge-connection readiness and ingress validation; mutable `latest` deployment rejected |
| `basecamp/kamal` | `eee0083b38661c3707c6b6052cc89e85038a096c` | Target/version deploy locks, health gates and immutable rollback; Kamal is not introduced unless project-native |
| `aws-actions/amazon-ecs-deploy-task-definition` | `2a913b360c33e87681f788667ec02c36a924e45b` | Unique image IDs, rendered task-definition revisions and bounded stability waits for existing GitHub/ECS paths |
| `aws/aws-cdk-cli` | `8f5a9c0c264a66614f0e82249e63c6ca11bd2f15` | Change-set preparation, actual-change diff, drift and rollback for existing CDK; production hotswap/express rejected |
| `aws-cloudformation/rain` | `90e8c6f55803775f23ff2c1ef70fd4e79574ae15` | Change summary and watch for existing CloudFormation; experimental forecast/content deployment is not authority |
| `aws/copilot-cli` | `a0dbe68908e55c4292e5838bd6cfbaea38364879` | Rejected for new adoption because support ended 2026-06-12; existing projects are legacy migration cases |

Other inspected agent-skill collections added no plan-changing mechanism after
the documented convergence point.

## Non-Apple refresh — 2026-09-10

The following selected sources informed the seven-channel expansion. These are
bounded file/section inspections at immutable revisions, not whole-repository
security audits. Official provider documentation, linked beside the resulting
rules, controls platform behavior when a tool recipe or search index conflicts.

| Source at inspected revision | Mechanism adapted or reason for rejection |
|---|---|
| [Android skills](https://github.com/android/skills/tree/bac232fd02b0855df9275281a2a7a47643768719) | Current policy mapped to the actual artifact and form factor |
| [Gradle Play Publisher](https://github.com/Triple-T/gradle-play-publisher/tree/c7dfb4fd8a9043be9146d1d8062a048e1e3d80ec) | Existing variant/artifact/track ownership; automatic version and multi-artifact effects need explicit binding |
| [fastlane](https://github.com/fastlane/fastlane/tree/a3655d11b25065c43b80356dda22b3badb59c0a5) | Existing lane composition; production/completed defaults and write-bearing validation cannot imply authority |
| [EAS CLI](https://github.com/expo/eas-cli/tree/8ac9d5f101408a26cf54a27b5b9422444fd7717e) | Submission-job versus Play-state proof; first-upload documentation conflict retains the Console fallback |
| [RevenueCat Play Billing skills](https://github.com/RevenueCat/play-billing-skills/tree/85d29339424d09e20793d118208afe8d825950d8) | Conditional product/catalog and test-payment lifecycle; no RevenueCat service dependency |
| [Google Play CLI skills](https://github.com/PollyGlot/google-play-cli-skills/tree/2bbddaee52bde633ebfd123b1ae90542aa3219ad) | Exact-version promotion, generated artifacts and recovery surfaces; harmless-read and blind-retry assumptions rejected |
| [Callstack agent skills](https://github.com/callstackincubator/agent-skills/tree/2766baa46ca0fe7c16cc5ab4d0077ccec2e95fb9) | Native dependency and release-artifact compatibility checks, without importing framework implementation work |
| [Microsoft Store CLI](https://github.com/microsoft/msstore-cli/tree/901c6f3e515339c614fff6afa0454013727a12cd) and [Copilot skill](https://github.com/github/awesome-copilot/tree/7568a482ce2df38f8965ab5336a3220db796a4ba) | Bootstrap/lifecycle taxonomy; inspect implicit draft creation/deletion and paid-product limitations before use |
| [Chrome guidance](https://github.com/GoogleChrome/modern-web-guidance/tree/bfd8c8dded770f3ba07a518e28991a32df40f902) | Coherent reviewer/listing packet; blanket expedited-review claims rejected |
| [Browser extension publisher](https://github.com/aklinker1/publish-browser-extension/tree/8ce1e500903796f738636a9ea741e76dae7e8985) and [CWS CLI](https://github.com/VaughnBosu/cws-cli/tree/0fd7b1ddecfbc187529c9153ef128a6923b8e769) | Separate upload, publish and status; inherited rollout defaults require provider readback |
| [Social scheduling skills](https://github.com/social-media-skills/skills/tree/6e30eeb2f6736bda8683b6bbaa674af3641d7945) | Job lifecycle separate from each provider post; scheduler setup, campaign expansion and blanket approval rules rejected |
| [xurl](https://github.com/xdevplatform/xurl/tree/41259e8aef85f847145c383d02be6a40a2435466) | Exact app/user selector and media lifecycle; token output and unbounded processing waits rejected |
| [YouTube Data CLI](https://github.com/Bin-Huang/youtube-data-cli/tree/10a1b87277969588bab73d3ca4227e6b14593566) | Operation inventory only; credential-file defaults and replacement updates without field preservation rejected |
| [Cloudflare Wrangler skill](https://github.com/cloudflare/skills/tree/b052c32bab7dd493513260228a36c88294f343f1) | Project-local config, build-time environment and version/deployment distinction |
| [OpenAI deployment skills](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431) | Existing project/build route and staged intent; new-site production defaults, unclaimed deployment fallback and blind retries rejected |
| [AWS agent toolkit](https://github.com/aws/agent-toolkit-for-aws/tree/df5d2e847c021eb7332871ab8989d6f73dec887d) | Service-specific production flow and SAM development boundary; no toolkit/MCP or architecture dependency |
| [ECS deploy action](https://github.com/aws-actions/amazon-ecs-deploy-task-definition/tree/10a12db2b4741703f03060448e2c9f1f6fa9c140) | Immutable images, rendered definitions, scoped roles and stability observation; IAM-user setup recipes not copied |

Additional MCP and publishing wrappers were rejected where they introduced a
new hosted service, plaintext credential custody, broad retries or unsupported
provider assumptions. No candidate executable was run or imported. The final
guidance is newly written mechanism-level synthesis; upstream licenses and
trademarks remain with their owners. See the
[coverage map](../docs/CHANNEL-COVERAGE.md) for where each lifecycle is used.

## Validation and evidence boundary

Delivery contains provider runbooks and a local receipt helper. Its automated
tests cover the helper's receipt validation, hashing, event identity, recovery
records, and related local behavior. They do not exercise provider credentials,
uploads, review decisions, production deployment, public availability, or
consumer installation and playback.

The references provide dated official-source guidance. They are not provider
SDKs, certification, guarantees of approval, or proof that every channel has
been exercised end to end. Optional specialist tools and project-native release
systems remain responsible for their own execution and security contracts.

Every live delivery must record the strongest directly observed state and
its limits. A source-level check or historical observation must never become
a claim about current provider state or a successful user experience.
