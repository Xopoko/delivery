# Delivery source provenance

Observation date: 2026-08-24.

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
| `openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | Cloudflare deployment routing and user-surface verification; environment-specific escalation language not adopted |
| `cloudflare/skills` | `f96bff754e428838818017f75817f0f9428acd48` | Provider capability routing only; product catalog and command breadth not copied |
| `cloudflare/cloudflared` | `d1df7985bdf189c4caf34e290bafbf8f411e603b` | Active edge-connection readiness and ingress validation; mutable `latest` deployment rejected |
| `basecamp/kamal` | `eee0083b38661c3707c6b6052cc89e85038a096c` | Target/version deploy locks, health gates and immutable rollback; Kamal is not introduced unless project-native |
| `aws-actions/amazon-ecs-deploy-task-definition` | `2a913b360c33e87681f788667ec02c36a924e45b` | Unique image IDs, rendered task-definition revisions and bounded stability waits for existing GitHub/ECS paths |
| `aws/aws-cdk-cli` | `8f5a9c0c264a66614f0e82249e63c6ca11bd2f15` | Change-set preparation, actual-change diff, drift and rollback for existing CDK; production hotswap/express rejected |
| `aws-cloudformation/rain` | `90e8c6f55803775f23ff2c1ef70fd4e79574ae15` | Change summary and watch for existing CloudFormation; experimental forecast/content deployment is not authority |
| `aws/copilot-cli` | `a0dbe68908e55c4292e5838bd6cfbaea38364879` | Rejected for new adoption because support ended 2026-06-12; existing projects are legacy migration cases |

Other inspected agent-skill collections added no plan-changing mechanism after
the documented convergence point.

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
