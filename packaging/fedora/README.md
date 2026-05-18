# Fedora COPR Packaging

This directory contains the RPM spec template used to publish
[siomon](https://github.com/level1techs/siomon) to Fedora COPR.

## Files

- `siomon.spec` — RPM spec template. The CI workflow updates `Version`,
  `%global commit`, `%global shortcommit`, and `Release` before building an
  SRPM.

## How It Works

The GitHub Actions workflow (`.github/workflows/publish-copr.yml`) runs on an
Ubuntu runner and:

1. Resolves the requested tag to a full commit hash.
2. Queries COPR to decide the next RPM release number for the upstream version.
3. Creates a source archive from the tagged commit.
4. Vendors Cargo dependencies into a separate archive and writes Cargo config
   so COPR builds do not require registry access during `rpmbuild`.
5. Updates the spec template with the resolved version, commit, and release.
6. Builds a source RPM with `rpmbuild -bs`.
7. Uploads the SRPM to COPR with `copr-cli build`.

## Local Testing

To test the spec locally on Fedora:

```bash
sudo dnf install cargo rust rpmdevtools git
rpmdev-setuptree
git archive --format=tar.gz --prefix=siomon-0.2.3/ -o ~/rpmbuild/SOURCES/siomon-0.2.3.tar.gz v0.2.3
cargo vendor --locked --versioned-dirs ~/rpmbuild/SOURCES/vendor > /tmp/config.toml
tar -C ~/rpmbuild/SOURCES -czf ~/rpmbuild/SOURCES/siomon-0.2.3-vendor.tar.gz vendor
cp packaging/fedora/siomon.spec ~/rpmbuild/SPECS/
rpmbuild -bs ~/rpmbuild/SPECS/siomon.spec
```

See [PACKAGING.md](../../PACKAGING.md) for full setup and secrets
configuration.
