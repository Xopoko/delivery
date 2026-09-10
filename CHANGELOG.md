# Changelog

Notable changes are recorded here. A version entry describes the source;
available release tags and assets are listed on GitHub separately.

## 0.3.3

- Correct Microsoft Store draft-replacement semantics and Chrome rollback
  checks for stored-data compatibility and pending submissions.
- Remove an unavailable Apple signing-skill dependency, clarify first IAP and
  subscription-group submission requirements, and correct a Google Play source.
- Verify protected web/AWS products through their intended access model and
  distinguish locally managed from remotely managed Cloudflare Tunnels.
- Update YouTube Shorts claim and thumbnail guidance; bind caption, thumbnail,
  and audio choices to the requested artifact and applicable requirements.
- Clarify recovery observations, pending review, and scheduling versus release.
- Reject ambiguous JSON, excessive nesting, and unrepresentable UTC timestamps
  in local receipts, with regression coverage for the reproduced failures.

## 0.3.2

- Use transparent destination artwork in the README for light and dark themes.

## 0.3.1

- Align destination artwork with platform colors: YouTube on red, AWS on
  yellow, black Apple on ivory, Google Play on periwinkle, and Windows on blue.
- Keep the compact plugin icon free of platform emblems.

## 0.3.0

- Prepare Delivery as a standalone package for Codex and Claude Code, with
  nine skills and bundled provider references.
- Make host capabilities, protected credential handling, and resource paths
  portable across installations.
- Add standalone package validation, a synthetic offline receipt demo, and
  contributor and security guidance.
- Document the distinction between receipt validation, provider state, and
  verification on the consumer surface.
