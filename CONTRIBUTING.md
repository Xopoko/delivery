# Contributing to Delivery

Delivery welcomes focused improvements to delivery workflows, current official
references, receipt correctness, and documentation. Start with a concrete
problem: what could an agent incorrectly do or claim, and what evidence would
show that the change helps?

For a new provider, major behavior change, or dependency, open an issue first
so the scope can be discussed. Small corrections can go directly to a pull
request.

## Work locally

Use Python 3.11+ for the tools and checks; no third-party packages are required.

```bash
python scripts/validate_package.py
python -m unittest discover -s tests -v
python scripts/demo.py
```

Keep test fixtures fictional. Tests must not need an account, network access,
secret, installed provider CLI, or particular user's filesystem.

## Keep the package portable

Skills should resolve bundled resources relative to the installed package.
Do not add absolute workstation paths, organization-specific infrastructure,
personal account names, private service endpoints, or mandatory dependencies
on another private plugin.

Use current official sources for provider behavior and record the date when
a mutable requirement was checked. Explain what changes at the provider and
which observation verifies it. Treat a reference as guidance to check, not
proof that a provider tool is installed or authenticated.

## Preserve the delivery contract

Keep preparation, staging, submission, release, and consumer verification
distinct. Scope authority to the exact effect. After an ambiguous write,
reconcile provider state before retrying. Receipts must remain observations,
not approval grants or remote execution locks.

Run tests appropriate to a behavior change. For a documentation-only fix,
verify the affected links, commands, and package validation. Report the checks
you actually ran and any provider behavior you did not verify.

## Review and disclosure

Use the pull request template to describe the problem, resulting behavior,
evidence, and limitations. Remove private data from diffs, screenshots, logs,
filenames, and receipts before sharing. For a vulnerability or accidental
secret exposure, follow [Security](SECURITY.md) instead of posting sensitive
details in an issue.

Contributions are licensed under the repository's [MIT license](LICENSE).
