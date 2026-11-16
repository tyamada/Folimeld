# Desktop: versioned corresponding-source delivery plan (not approved)

[日本語](windows-desktop-sources_ja.md)

The numeric Desktop version, final source commit and publication location are not assigned. This is neither a published download nor final licence approval. uv development remains discontinued; this guide does not replace the Store source-delivery record.

## Bind the following for each version

- Application source: selected commit, AGPL text, Desktop spec/iss/entry points, version information, fixed runtime/tool/CRT/Inno ledgers and necessary generation/build instructions.
- Third-party source: the actual Qt/PySide, Python, Pillow, MuPDF and embedded component sources, changes/patches, necessary generation inputs/instructions and original notices. Parent-package links alone do not complete this set.
- Correspondence ledger: numeric Desktop version, commit, source/input sizes and SHA-256. After generation, bind the complete payload and setup as well.
- Published file list and SHA256SUMS: not created. Choose names and URLs after assigning the version and reviewing completed materials.

## Tika/Qt MIME-data integration

The [component notice](windows-desktop-licenses/TIKA-PRONOM-NOTICE.draft.txt) is integrated into the [Desktop final-notice draft](windows-desktop-licenses/THIRD-PARTY-NOTICES.draft.txt). It includes PRONOM/TNA/OGL credit, scoped Tika/ASF/IPTC explanations and the original Ian F. Darwin MIME-information BSD notice. It does not apply every third-party term to the whole application.

This guide links the [supplement instructions](windows-desktop-licenses/tika-source-delivery/README.txt) and [19-file manifest](windows-desktop-licenses/tika-source-delivery/SOURCE-SET.draft.json). They retain fixed upstream Tika XML, Qt6.11.2 transformed XML/scripts/attribution/REUSE, a diff, originals/references and the notice. This is not the complete Qt corresponding-source release.

Existing Qt source input:
`qt-everywhere-src-6.11.2.tar.xz`
SHA256: `6dcfbca271d76a6502741a2c0dc6fc98ef7dd0b7b4cfd0abcebb285a86a26f33`

Existing PySide/Shiboken source input:
`pyside-setup-everywhere-src-6.11.2.tar.xz`
SHA256: `cba47efbaad1bedd529725cbc14e21f156c7a19366f07b3edfbb076ffd7afdf8`

The [source ledger](windows-desktop-licenses/DEPENDENCY-SOURCES.draft.json) binds the notices, supplement manifest and fixed wheels, explicitly leaving the version and publication URL unassigned.

## Qt wheel correspondence and limits

Four fixed wheels were statically checked for hashes and version6.11.2. The three PySide configs declare59 modules; DLLs for the seven Desktop-allowed modules exist in the inputs. These are not final payload counts or effective feature flags. All27 distributed glue-source files agree with the source archive after newline normalization (zero raw-byte matches; differences are CRLF/LF). This does not prove the whole Qt DLLs are unchanged.

No SBOM/SPDX/CycloneDX-named files were found in these four wheels. No .patch/.diff-named files were found in the PySide source archive. Neither observation proves there were no additional upstream Qt changes. config build_date is self-recorded; PE6.11.2.0 values are version metadata.

## Before and after the initial build

Before onedir: review remaining wheel-specific Qt configuration/changes and source evidence, Pillow/MuPDF/CRT and other materials, version/signing policy and final notices/source index. Create reviewed-files.json only after completion; it does not exist now.
After onedir, before Inno: audit every actual payload file, packaged notice, version and source correspondence, then create the payload-review ledger. Do not require a nonexistent payload before the first onedir build.
Separate reproducibility research: upstream compiler/SDK/full generation environment, transformed-data regeneration and complete Qt DLL/wheel byte reproduction. Concrete missing changes/sources must not be deferred under that heading.

No build, commit, publication, test-PC update, WACK or Hosted API comparison was performed. No new billing or model request.

Static PE inspection of the seven allowed Qt DLLs plus qwindows/qjpeg (nine native files) found x64/version6.11.2.0 throughout, with no normal/delay Qt import outside the allowed set. Dynamic loading and actual collection remain unverified.
