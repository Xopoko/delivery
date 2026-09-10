# Install Delivery Skills

Delivery Skills provides instructions and provider guides for coding agents,
including Codex, Claude Code, Cursor, and other compatible hosts. Codex and
Claude Code have bundled plugin packages; other agents can read the skills
from a full checkout. Your environment supplies provider tools and account access.

## Host compatibility

The skills use Markdown instructions and relative resource paths. Codex is the
primary development and testing host; the intended audience includes other agents.

| Agent | How to use Delivery Skills | Verification so far |
| --- | --- | --- |
| Codex | Bundled plugin | Installation and skill discovery checked in a fresh runtime. |
| Claude Code | Bundled plugin | Manifest and installation command syntax validated; runtime and provider workflows not tested here. |
| Cursor | Full checkout under `.cursor/skills/delivery/` | Layout follows documented nested skill discovery; runtime not tested here. |
| Other compatible agents | Read the skills and bundled resources from a full checkout | Check discovery and resource access in the chosen host. |

## Requirements

- An agent that can read skill instructions and bundled files. The Codex and
  Claude Code installation routes use plugin support.
- Git access to this repository for marketplace installation.
- Python 3.11+ only for the optional receipt helper, demo, and package checks.

Use `python3` in the commands below if that is your Python 3.11+ executable.
The tools use the standard library. The skills can be used without Python.

The command syntax below was checked against Codex CLI 0.153.4 and Claude Code
2.1.231. This is command compatibility evidence, not a claim that every host
version or provider workflow has been tested. Check your installed CLI's
`--help` when using another version.

## Codex

```bash
codex plugin marketplace add Xopoko/delivery
codex plugin add delivery@delivery
codex plugin list --marketplace delivery
```

The repository registers the `delivery` marketplace; its plugin is also named
`delivery`. The default commands follow the repository's default branch. To
pin a reviewed revision, add `--ref` with that exact tag or commit to the first
command. A version in a manifest does not by itself establish a Git release tag.

For an existing local checkout, run from the repository root:

```bash
python scripts/validate_package.py
codex plugin marketplace add .
codex plugin add delivery@delivery
```

Choose either the Git source or the local source for this marketplace name.
Keep a registered local checkout in place while the host uses it.

## Claude Code

The CLI installs at user scope by default:

```bash
claude plugin marketplace add Xopoko/delivery
claude plugin install delivery@delivery
claude plugin list
```

Alternatively, inside Claude Code:

```text
/plugin marketplace add Xopoko/delivery
/plugin install delivery@delivery
/reload-plugins
```

For a local checkout, run from the repository root:

```bash
python scripts/validate_package.py
claude plugin marketplace add .
claude plugin install delivery@delivery
```

## Cursor

From the target project's root:

```bash
git clone https://github.com/Xopoko/delivery.git .cursor/skills/delivery
```

[Cursor documents recursive discovery of nested skills](https://cursor.com/docs/skills#nested-skill-directories).
The layout above applies that behavior to this package while keeping shared
resources in place. Restart Cursor, look for `/delivery`, and ask it to read
the bundled control contract before contacting a provider. This layout has not
been tested in a Cursor runtime here.

Keep the complete checkout intact. Importing only individual skill folders may
omit the shared `references/` and `scripts/` directories; check those resources
if you use a different import route.

## Other agents

Keep a full checkout in a location the agent can read, for example within its
workspace:

```bash
git clone https://github.com/Xopoko/delivery.git delivery-skills
```

Point the agent to `delivery-skills/skills/delivery/SKILL.md` and let it read the
linked channel skills and provider guides. Keep `skills/`, `references/`, and
`scripts/` together: the skill root's `../..` must still resolve to this package.
Copying or importing individual skill folders can break these shared links.

For an initial check, ask:

> Read delivery-skills/skills/delivery/SKILL.md and its bundled delivery control
> contract. Resolve package resources from the delivery-skills checkout. Explain
> how you would resume a timed-out upload. Do not contact or change a provider.

This uses explicit file context; automatic skill discovery depends on the host.
After the agent can read the resources, use the same task examples as in the
[README](../README.md#usage). For other hosts, check their current Agent Skills
support and resource-loading behavior before relying on automatic discovery.

## Verify discovery

Start a fresh agent session after installing or updating. For plugin installs,
check the host's plugin inventory for Delivery Skills. For a full checkout,
give the agent its skill path. Then ask:

> Confirm that Delivery Skills is available. List its skills, open its bundled
> delivery control contract, and explain how it handles a timed-out upload.
> This is an installation check; do not contact or change a provider.

The host should discover the router and channel skills listed in the
[README](../README.md#skill-map), and resolve the bundled contract. A package
validator passing proves the source structure; the host inventory and resource
read establish that the installed plugin is usable in that session.

Installing Delivery does not sign in, provision provider CLIs, register apps,
set up cloud resources, or authorize publication. Before an actual delivery,
the agent must discover the specific project and provider capabilities.

## Update

For a Git marketplace following its default branch, refresh the marketplace
and install the current plugin version:

```bash
codex plugin marketplace upgrade delivery
codex plugin add delivery@delivery
```

In Claude Code:

```bash
claude plugin marketplace update delivery
claude plugin update delivery@delivery
```

For a local source, update the checkout using your normal Git workflow,
validate it, and refresh the plugin in your host. Start a fresh session and
repeat discovery. Do not edit the host's installed cache directly.

## Remove

```bash
codex plugin remove delivery@delivery
```

Or:

```bash
claude plugin uninstall delivery@delivery
```

The marketplace can remain available without the plugin installed. Remove the
marketplace separately through your host if you no longer want it listed.
Your private receipts live in a location you chose and have their own retention
lifecycle; plugin removal is not receipt cleanup.
