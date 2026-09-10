# Local delivery receipts

The optional [`delivery_receipt.py`](../scripts/delivery_receipt.py) helper
records the small amount of state useful for resuming a delivery. It uses
Python 3.11+ and the standard library. It makes no network calls.

Use a private state directory outside the repository, or a location you have
already verified is ignored by Git. A receipt can contain sensitive business
context even when it contains no credentials.

## Commands

| Command | Purpose |
| --- | --- |
| `init` | Create a receipt bound to the artifact, delivery identity, and optional intent file. |
| `record` | Append a timestamped observation with an idempotent event ID. |
| `validate` | Validate the record and, when supplied, re-hash the bound input files. |
| `show` | Return a validated receipt. |

```bash
python scripts/delivery_receipt.py --help
python scripts/delivery_receipt.py init --help
python scripts/delivery_receipt.py record --help
```

Successful operations emit JSON and exit with status `0`. Validation failures
emit a JSON error and exit with status `2`. Treat stdout as potentially private:
`init` and `show` include the receipt, and `record` includes the event.

## Bind the release inputs

This example uses fictional values and relative example paths. Replace them
with your own nonsensitive identifiers and an existing private state location.
Run it from a private work directory, supplying the actual path to the helper.

```bash
python /path/to/delivery/scripts/delivery_receipt.py init --file private-state/video-7.json --delivery-id video-7 --provider youtube --provider-account-id example-channel --release-id video-7 --target-kind video --target-id planned-video-7 --channel private --effect stage --release-mode private --artifact video.mp4 --metadata-file intent.json
```

For `stage`, `submit`, `release`, and `verify`, initialization requires a
metadata file. Use a small nonsensitive intent manifest that captures material
version, audience, visibility, territory, declarations, and schedule facts that
are not already expressed by the fixed fields. The helper hashes its bytes; it
does not know whether its meaning is truthful or complete.

For web or cloud work, the artifact may be a nonsensitive deployment manifest
that binds the exact source or image digest, configuration and migration
revision, target resources, and recovery revision. Separate provider objects
should have separate receipts where their identity or lifecycle differs.

## Record an observation

After obtaining a real provider observation, record its nonsensitive facts:

```bash
python /path/to/delivery/scripts/delivery_receipt.py record --file private-state/video-7.json --event-id processing-1 --phase processing --status processing --provider-object-kind video --provider-object-id example-video-7 --next-action inspect-processing
```

Repeating the same event ID and content is idempotent. Reusing the ID with
different content is rejected. Typed provider-object identities stay stable
within a receipt. Observation timestamps determine the latest event; file
append order alone does not.

These checks protect record consistency. They do not authenticate the source
of an observation or validate that a provider transition really occurred.

## Re-check before an effect

```bash
python /path/to/delivery/scripts/delivery_receipt.py validate --file private-state/video-7.json --artifact video.mp4 --metadata-file intent.json
```

Validation with the artifact and any bound metadata re-checks names, sizes,
and SHA-256 hashes. Validation without the artifact checks only the receipt
structure and reports `complete: false`. A receipt that binds metadata also
requires that metadata file during validation.

`complete: true` means the requested local input checks completed. It does not
mean the delivery is complete, the provider state is current, or a write is
authorized. Re-read the provider before the next external effect.

## Privacy boundary

Store only stable nonsensitive identifiers, hashes, concise observed states,
and safe evidence references. Never store credentials, cookies, signing keys,
reviewer passwords, private contact data, raw provider responses, signed URLs,
or upload-session links.

The helper rejects several recognizable secret formats. This is a heuristic
guard, not a general data-loss prevention system, encryption layer, or promise
that every secret will be detected. Review inputs yourself and protect the
directory through your operating system. See [Security](../SECURITY.md).
