# Repository instructions

## README translation synchronization

- `README.md` is the Japanese source of truth; `README_en.md` is its English translation.
- Whenever you modify `README.md`, update `README_en.md` in the same task without waiting for a separate user request. Include both files in the same commit when committing those changes.
- Translate all added or changed content and remove translations of deleted content. Keep section order, supported platforms, versions, download links, commands, feature descriptions, and limitations consistent.
- Preserve the language-switch links in both files. Keep paths and command arguments unchanged when translating; translate explanatory comments as appropriate.
- If you change shared factual content in `README_en.md`, update `README.md` as well. English-only wording corrections do not require a Japanese change.
- Before finishing, review both files for semantic consistency and check that their relative links resolve. These instructions govern agent edits; they do not install a background translation service for manual edits.

## Changelog translation synchronization

- `CHANGELOG.md` is the Japanese source of truth; `CHANGELOG_en.md` is its English translation.
- Whenever you modify `CHANGELOG.md`, update `CHANGELOG_en.md` in the same task without waiting for a separate user request. Include both files in the same commit when committing those changes.
- Translate all added or changed entries and remove translations of deleted entries. Keep version numbers, dates, section order, paths, commands, and factual content consistent.
- Preserve the language-switch links in both files. If you change shared factual content in `CHANGELOG_en.md`, update `CHANGELOG.md` as well. English-only wording corrections do not require a Japanese change.
- Before finishing, review both files for semantic consistency and check that their relative links resolve. These instructions govern agent edits; they do not install a background translation service for manual edits.
