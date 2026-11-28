# Repository instructions

## Documentation filenames

- English documentation uses `<base>.md`; Japanese documentation uses `<base>_ja.md`, including Japanese-only documents.
- Keep `AGENTS.md` under its standard filename so repository instructions remain discoverable.
- When renaming documents, update incoming references, relative links, and language-switch links together.
- Store supplementary documentation, verification records, and README screenshots in `documentation/`; reserve `docs/` for a future GitHub Pages site.

## README translation synchronization

- `README_ja.md` is the Japanese source of truth; `README.md` is its English translation.
- Whenever you modify `README_ja.md`, update `README.md` in the same task without waiting for a separate user request. Include both files in the same commit when committing those changes.
- Translate all added or changed content and remove translations of deleted content. Keep section order, supported platforms, versions, download links, commands, feature descriptions, and limitations consistent.
- Preserve the language-switch links in both files. Keep paths and command arguments unchanged when translating; translate explanatory comments as appropriate.
- If you change shared factual content in `README.md`, update `README_ja.md` as well. English-only wording corrections do not require a Japanese change.
- Before finishing, review both files for semantic consistency and check that their relative links resolve. These instructions govern agent edits; they do not install a background translation service for manual edits.

## Changelog translation synchronization

- `CHANGELOG_ja.md` is the Japanese source of truth; `CHANGELOG.md` is its English translation.
- Whenever you modify `CHANGELOG_ja.md`, update `CHANGELOG.md` in the same task without waiting for a separate user request. Include both files in the same commit when committing those changes.
- Translate all added or changed entries and remove translations of deleted entries. Keep version numbers, dates, section order, paths, commands, and factual content consistent.
- Preserve the language-switch links in both files. If you change shared factual content in `CHANGELOG.md`, update `CHANGELOG_ja.md` as well. English-only wording corrections do not require a Japanese change.
- Before finishing, review both files for semantic consistency and check that their relative links resolve. These instructions govern agent edits; they do not install a background translation service for manual edits.

## Push, CI, and release announcements

- When pushing commits to GitHub, monitor the triggered GitHub Actions CI runs and resolve any CI errors before finishing the task.
- When publishing a package or release, confirm that the pushed release and its published packages are live and publicly verified, then post a release announcement to X (tyamada22 / `@tyamada22`).
- When a new Folimeld version is confirmed live on Microsoft Store, post an announcement from X `@tyamada22` with the verified version and the public Store listing URL. Confirm that Partner Center shows the matching submission under Store presence and that the public listing opens. Check for an existing announcement for the same Store version before posting, and record the post URL after verifying it. A GitHub corresponding-source release or certification approval alone does not trigger a Store announcement.

## Built MSIX package storage and retrieval

- Do not push built MSIX packages to the `Folimeld` GitHub repository.
- Save built MSIX packages to `../work/Folimeld/dist/` (`Downloads/source/work/Folimeld/dist/`).
- Obtain built MSIX packages stored under `Downloads/source/work/Folimeld/dist/` (cloned from `https://github.com/tyamada/work.git` into `Downloads/source/work`). Pull the latest changes in `Downloads/source/work` before copying or verifying MSIX packages.

## Microsoft Store corresponding source releases

- For every released Microsoft Store version, publish its corresponding source code on GitHub Releases under tag `windows-store-v<package_version>` (e.g., `windows-store-v1.0.2.0`).
- Attach the matching source ZIP, `SHA256SUMS.txt`, and `source-association.json` (recording the submitted x64/ARM64 MSIX hashes, executable hashes, and source archive hash). Do not attach built `.msix` binaries to GitHub Releases.
- Keep `make_latest: false` (or preserve the intended `latest` release) unless explicitly updating the repository's primary release, and verify public unauthenticated HTTPS downloads after publishing.
