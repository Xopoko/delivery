# Install Delivery

Delivery packages nine Agent Skills for Codex and Claude Code. Installing it
adds instructions and reference material to your agent. Provider tools and
account access are supplied separately by your environment.

## Requirements

- An agent host with plugin support: Codex or Claude Code.
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

Keep the entire repository intact. Copying only `skills/` omits the shared
references and optional helper. For another agent host, consult its current
Agent Skills support and verify relative resource resolution before use; this
repository does not claim a native installer for other hosts.

## Verify discovery

Start a fresh agent session after installing or updating. Check the host's
plugin inventory for Delivery and ask:

> Confirm that Delivery is available. List its nine skills, open its bundled
> delivery control contract, and explain how it handles a timed-out upload.
> This is an installation check; do not contact or change a provider.

The host should discover the router and eight channel skills listed in the
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
