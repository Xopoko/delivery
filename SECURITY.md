# Security and privacy

Delivery contains agent instructions and an optional local receipt helper.
Instructions guide agent behavior; they do not enforce a security boundary.
The agent host, its tools, and your provider permissions determine what the
agent can access or change.

## Keep secrets outside the workflow record

Never place credentials, tokens, cookies, signing keys, reviewer access,
recovery material, signed URLs, or upload-session links in receipts, prompts,
issues, screenshots, or Git. Use the protected sign-in and credential mechanisms
provided by your host or the provider. Suspend capture while entering secrets.

Receipts are plaintext local JSON. The helper rejects several recognizable
secret formats, but cannot detect every secret or personal datum. It does not
encrypt receipts, manage credentials, or authorize provider actions. Store real
receipts in a private directory outside this repository and control access and
retention there.

The bundled Python tools make no network requests and include no telemetry.
Your agent host, provider tools, and services have their own data handling and
logging behavior. Keep private observations out of public reports even when a
tool considers their format valid.

## Review before use

Read the skill and shared contract that apply to your destination. Confirm the
artifact, target, audience, and intended effect before authorizing an external
transition. Mutable provider rules and current account state must be checked
at the time of delivery.

The automated checks cover the local package and receipt implementation. They
do not certify provider integrations, prevent unsafe use by an agent, or prove
that a live deployment is secure.

## Report a vulnerability

Use GitHub's [private vulnerability reporting](https://github.com/Xopoko/delivery/security/advisories/new)
when available. Include a minimal reproduction using fictional data, the
affected version or commit, expected behavior, and likely impact. Do not send
working secrets or private receipts.

If private reporting is unavailable, open a minimal issue requesting a private
reporting channel without exploit details or sensitive material. If a credential
has already been exposed, revoke or rotate it through its provider; removing
the text from an issue or Git does not revoke the credential.

Security fixes target the latest maintained version. Check the
[changelog](CHANGELOG.md) and validate an updated package before use.
