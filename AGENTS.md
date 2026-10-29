# Repository instructions

## Documentation filenames

- English documentation uses `<base>.md`; Japanese documentation uses `<base>_ja.md`, including Japanese-only documents.
- Keep `AGENTS.md` under its standard filename so repository instructions remain discoverable.
- When renaming documents, update incoming references, relative links, and language-switch links together.

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
