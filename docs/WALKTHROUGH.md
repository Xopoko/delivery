# Try the receipt workflow

This walkthrough is a small, offline demonstration of Delivery's local receipt
helper. It uses fictional identifiers and temporary files. No provider account,
network access, API key, package installation, or live publication is needed.

From the repository root, with Python 3.11+:

```bash
python scripts/demo.py
```

The command exits with status `0` when its checks pass. Read its output for
the observed results. Temporary demo files are cleaned up when it finishes.

```text
Delivery / synthetic recovery demo
  1. Bound artifact and intent to one private staging request.
  2. Recorded processing; no release or verification was inferred.
  3. Replayed observation: already_recorded.
  4. Revalidated original files: true.
  5. Changed artifact rejected: artifact does not match the bound name, size, and SHA-256.
No provider was contacted. Temporary files are removed on exit.
```

## The situation

Imagine preparing a release, recording the result of a provider operation, and
resuming later. Two questions matter: are these still the same release inputs,
and does the record contain an unambiguous observation of the same object?

The demo creates an artifact-bound receipt, records a synthetic processing
observation, repeats it without duplication, validates the bound files, and
shows that changing the artifact invalidates the binding. All provider states
are synthetic inputs, not observations of a real service.

Read [`scripts/demo.py`](../scripts/demo.py) for the complete scenario. To
inspect the full test suite:

```bash
python -m unittest discover -s tests -v
```

## Apply it to a real task

After installing the plugin, start with a bounded request:

> Use Delivery to prepare this release for the existing destination. Identify
> the exact artifact, material metadata, account, target, and requested audience.
> Inspect the current provider state. Complete the available readiness checks
> and show what is ready, what remains uncertain, and the next action.

For a short task, the agent may not need a receipt. For asynchronous review or
processing, use a private receipt as described in the [receipt guide](RECEIPTS.md).
Keep credentials and private provider responses out of it.

The next step is to observe the actual provider and verify the intended
consumer experience. The offline demo cannot stand in for either.
