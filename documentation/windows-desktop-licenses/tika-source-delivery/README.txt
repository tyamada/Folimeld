Tika/Qt MIME-data corresponding-source supplement — DRAFT, NOT APPROVED

This directory is a prepared supplemental file set, not a built package,
not a published archive, and not the complete Qt/PySide/Folimeld source release.
No processing script, compiler, installer or app has been run.

Inputs and changes
- Original Tika MIME XML is pinned to commit c29724782854bb5a319f4a1940d0828a58ace3f9.
- The exact transformed XML, two original processing/update scripts,
  qt_attribution.json and REUSE.toml are retained from Qt 6.11.2.
- The static upstream-to-Qt diff records the actual retained XML differences.
- The original update script follows moving upstream history/date. Do not
  treat running it unchanged as a pinned historical reproduction recipe.
- Complete Qt source archive remains an external companion input:
  qt-everywhere-src-6.11.2.tar.xz
  SHA256 6dcfbca271d76a6502741a2c0dc6fc98ef7dd0b7b4cfd0abcebb285a86a26f33.
  See the full Qt build rules for generation/embedding beyond this subset.

Scope and notices
- Retain named PRONOM/TNA credit, OGL3.0 fallback/link, applicable Apache
  copyright/NOTICE and the MIME-specific file-4.26 BSD notice.
- Aggregate upstream licences/NOTICE and historical IPTC terms are under
  reference-only. Their presence does not mean all Java dependencies or
  Photo Metadata descriptions are included in Qt or this supplement.
- IPTC.java/Photoshop.java were inspected as scope evidence on the development
  PC but are not included here as Qt MIME source.
- Existing Qt/PySide/application licence and replacement requirements remain
  separate. This supplement alone is not final licence/source approval.

Verification and remaining work
Read SOURCE-SET.draft.json and verify each file's bytes/SHA256 before use.
The manifest excludes itself to avoid circular hashing. The manifest hash is
recorded in the development-PC verification record.
Integrate reviewed notices/source references into the final Desktop materials,
confirm any additional provider-specific attribution and material-specific
rights, and bind actual wheel/payload inputs after separately authorized steps.
Full transformation reproduction and binary embedding equivalence are untested.
No source ZIP or release has been created.
