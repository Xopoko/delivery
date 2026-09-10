<p align="center">
  <img src="assets/platforms.png" width="400" alt="Delivery destinations: Apple, Microsoft, Google Play, YouTube, and AWS">
</p>

<h1 align="center">Delivery</h1>

<p align="center">
  <strong>From a finished artifact to a verified release.</strong>
</p>

<p align="center">
  Agent skills for <strong>Codex</strong> and <strong>Claude Code</strong>
  &middot; <a href="LICENSE">MIT</a>
  &middot; <a href="docs/INSTALL.md">Install</a>
  &middot; <a href="docs/WALKTHROUGH.md">Try the demo</a>
</p>

The build is ready. The work ends when the intended audience can use it.

Delivery gives your agent a practical workflow for that last mile: bind the
exact artifact and destination, prepare the channel, carry out the authorized
transition, recover from uncertain responses, and verify the result where
users will see it.

It contains **nine skills**, provider references, and an optional Python
receipt helper. Your agent uses the project tools and provider access you
already have. Delivery itself ships no provider clients, credentials, browser
automation, background service, or hosted infrastructure.

## What changes in a delivery task

| Situation | Delivery's operating rule |
| --- | --- |
| Several builds or similarly named targets exist | Bind the artifact digest, provider account, target, and intended audience before writing. |
| An upload returns a timeout | Read the provider's state for the same object before considering a retry. |
| A store says “approved” | Preserve that state; separately verify release and installation when those are the goal. |
| A release crosses sessions | Resume from live provider state, with a minimal local receipt when useful. |
| A draft is ready for publication | Check the exact payload and destination against the user's authorization. |

The skills distinguish preparation, staging, submission, release, and user-visible
verification. A receipt can help remember what happened; the provider and the
actual consumer surface determine what happened.

## Quick start

### Codex

```bash
codex plugin marketplace add Xopoko/delivery
codex plugin add delivery@delivery
codex plugin list --marketplace delivery
```

### Claude Code

```bash
claude plugin marketplace add Xopoko/delivery
claude plugin install delivery@delivery
claude plugin list
```

Start a fresh session after installation. Keep the complete package together:
the skills use the bundled references. See [installation and updates](docs/INSTALL.md)
for local checkouts, removal, prerequisites, and verification boundaries.

Then ask your agent:

> Use Delivery to prepare the current app build for its existing store listing.
> Identify the exact build and listing, inspect the current provider state, and
> complete the readiness checks. Stop with a reviewable submission summary;
> do not submit it yet.

Or resume an uncertain operation:

> Use Delivery to resume the video upload that timed out. Find the matching
> object on the intended channel, inspect its processing and visibility state,
> and continue toward a private, playable upload. Reconcile the existing upload
> before trying another one.

Or verify a release:

> Use Delivery to verify the currently deployed revision of this website.
> Check the project deployment record, public hostname, TLS, active revision,
> and the main user journey. Report the evidence and any unverified part.

## Skill map

Use `delivery` for a broad request. It routes the work to the relevant channel.

| Skill | Destination | Focus |
| --- | --- | --- |
| [`delivery`](skills/delivery/SKILL.md) | All channels | Scope, identity, authority, evidence, and recovery |
| [`delivery-apple`](skills/delivery-apple/SKILL.md) | App Store, TestFlight, macOS | Signing, build processing, review, distribution, install proof |
| [`delivery-google-play`](skills/delivery-google-play/SKILL.md) | Google Play | App bundles, signing, testing tracks, review, rollout |
| [`delivery-microsoft-store`](skills/delivery-microsoft-store/SKILL.md) | Microsoft Store | MSIX and hosted EXE/MSI, certification, publication, lifecycle checks |
| [`delivery-chrome-web-store`](skills/delivery-chrome-web-store/SKILL.md) | Chrome Web Store | Package and privacy readiness, review, rollout, install proof |
| [`delivery-social`](skills/delivery-social/SKILL.md) | LinkedIn and X | Evidence-backed payloads, exact publication scope, canonical post verification |
| [`delivery-youtube`](skills/delivery-youtube/SKILL.md) | YouTube and Shorts | Private upload, processing, metadata, visibility, playback |
| [`delivery-web`](skills/delivery-web/SKILL.md) | Websites and APIs | Deployment revision, origin, DNS, TLS, traffic, recovery |
| [`delivery-aws`](skills/delivery-aws/SKILL.md) | Existing AWS services | Resource identity, deployment health, traffic, recovery, consumer path |

These are workflow skills, not bundled integrations. Available actions depend
on the agent host, the project's tools, provider permissions, and current
provider requirements. Platform references link to official documentation;
mutable requirements must be checked at delivery time.

## Try it without a provider account

With Python 3.11+ and a checkout of this repository:

```bash
python scripts/demo.py
```

The demo uses fictional data in a temporary directory and exercises the receipt
helper without network access. Follow the [walkthrough](docs/WALKTHROUGH.md)
to see what each check establishes and where live verification begins.

For work that spans sessions, [`delivery_receipt.py`](scripts/delivery_receipt.py)
can bind artifact and intent hashes, append idempotent observations, and check
for changed inputs. It stores no approval grant and makes no provider calls.
Keep real receipts in your own private state directory outside this repository.
See the [receipt guide](docs/RECEIPTS.md).

## Designed for explicit outcomes

Delivery keeps the final effect within the user's authorization. It prepares
reviewable work before requesting a missing decision, protects sign-in and
secret entry through the host's available mechanisms, and treats an ambiguous
write as a reason to reconcile state.

Provider approval, publication, search visibility, playback, and installation
are separate observations. The package checks and synthetic demo cannot prove
a live provider workflow or prevent an agent from disregarding instructions.
Read the [architecture](docs/ARCHITECTURE.md) and [security guidance](SECURITY.md)
for the execution and privacy boundaries.

## Develop and contribute

No third-party Python packages are required for the bundled tools.

```bash
python scripts/validate_package.py
python -m unittest discover -s tests -v
python scripts/demo.py
```

Small, evidenced improvements are welcome. See [Contributing](CONTRIBUTING.md),
the [changelog](CHANGELOG.md), and the [MIT license](LICENSE).

Platform names and marks identify delivery destinations and belong to their
respective owners. Delivery is independent and is not affiliated with or
endorsed by those platforms. The MIT license does not grant trademark rights.
