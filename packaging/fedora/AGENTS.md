# Fedora COPR Packaging - Agent Context

## Purpose

Package build template for Fedora COPR. The CI workflow creates a source
archive and Cargo vendor archive, updates template values, builds a source RPM,
and submits it to COPR.

## Key Sources

- `packaging/fedora/README.md` — how COPR publishing works and local testing
  instructions.
- `.github/workflows/publish-copr.yml` — the workflow implementation.
- `packaging/fedora/siomon.spec` — RPM spec template.
- `PACKAGING.md` — one-time setup guide for secrets and COPR account
  configuration.
