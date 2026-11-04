# Linux package migration to GitHub Releases

[日本語](linux-release-migration_ja.md) | [English](linux-release-migration.md)

Reviewed: 2026-11-04. Planning and offline asset verification are complete. No upload, tag, publication, existing-file deletion or history rewrite has been performed.

## Distribution policy

- Windows EXE/MSIX and macOS app/PKG/DMG binaries stay private for local development and verification.
- Public distribution consists of Linux packages and their matching sources, checksums and build records.
- The four existing GitHub Releases cover v0.3.0 and earlier and had no attached assets when checked. Current README downloads point to `releases/ubuntu/`.

## Technical feasibility

Migration is technically possible. GitHub Releases accepts files below 2 GiB each ([official documentation](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)). All 17 current 0.3.3 assets meet that limit.

```bash
python -m tools.prepare_linux_release --version 0.3.3
```

This writes exact paths, names, sizes, SHA-256 hashes and roles to `build/linux-release-plan.json`. It checks four packages, their checksum list, four corresponding source ZIPs, four build records and four package/source association records. It also verifies source-file hashes inside the ZIPs. Windows/macOS binaries and `dist/` are excluded. Do not publish a wildcard such as `dist/*`.

## Proposed migration

1. Prepare a Release that copies the existing verified 0.3.3 assets unchanged. The proposed tag is `linux-v0.3.3`, titled “Linux packages 0.3.3 — existing artifacts”. Do not mix them with a rebuild of today's main.
2. The amd64 records identify base commit `ca33994f8ea7dada7996f8902d3ab703dfae88e5`, while arm64 identifies `9102573dc45b70393bed716dd5c9f9f7f9e5a35f`; both include uncommitted build changes. One tag cannot represent both sets of build inputs, so use the individual source ZIPs and records. Review the records before choosing the tag target; do not automatically substitute today's main. GitHub's automatic Source code ZIP must not replace the attached corresponding build-source snapshots.
3. Attach only the 17 manifest-listed assets to a draft. Link each package to its matching source and records in the release notes. Check that names are unique in the flat Release asset namespace.
4. Download the assets again and verify hashes and associations before publishing. Then update both READMEs together to fixed-tag URLs. A proposed URL is `https://github.com/tyamada/Folimeld/releases/download/linux-v0.3.3/folimeld_0.3.3_amd64.deb`; that asset URL has not been created yet ([official linking documentation](https://docs.github.com/en/repositories/releasing-projects-on-github/linking-to-releases)).
5. Retain `releases/ubuntu/` during migration so existing external URLs work. Any later deletion needs a separate impact review. Large files remain in Git history after removal from HEAD, so deletion alone does not remove their history from ordinary clones. History rewriting, which would affect development on the other PC, is outside this migration.
6. Publish subsequent Linux versions directly as Release assets instead of accumulating new package binaries in the repository.

## Open items in existing records

The original artifact records mark `dependency_sources` as “NOT INCLUDED”. Folimeld's own source ZIPs passed verification, but this does not establish completion of the dependency-source and notice review. Preserve the open items in the [distribution checklist](license-distribution_ja.md) and [0.3.2 audit](source-audit-0.3.2_ja.md); do not describe relocation as resolving them.

Version 0.3.2 lacks the same set of source association records. Keep it separately rather than applying 0.3.3 records retroactively. Linux installation and execution have not been retested in this review.
