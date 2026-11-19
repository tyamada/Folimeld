# Sample PDFs

The language list offers all languages or an individual language/locale. The default follows the app language, or the system language if none is supplied; unsupported languages fall back to all languages. Choose Latest episode first (default) or From episode 1. The footer always identifies the copyright holder and the CC BY 4.0 license.

Use **File → Open a sample PDF…** or the empty-document prompt to choose one book after checking its episode, language/locale, title and download size. The PDF opens only after its byte count and SHA-256 are verified. The entire 51-book collection is never downloaded automatically. Failed downloads can be retried, and active downloads can be cancelled.

If catalogue retrieval or validation fails, the last valid catalogue is used, followed by the bundled catalogue. The bundled metadata is a snapshot of the public schema_version=1 manifest. An internet connection is required for the first download. Verified originals remain reusable after restarting and offline.

Storage is `samples-v1` under Qt AppLocalDataLocation for the active distribution profile. `originals` contains verified originals; `opened` contains a separate editing copy created each time a sample is opened. Save updates that working copy without changing the original. Use Save As to keep a document in your own folder. Previous copies are not automatically deleted. Existing unsaved documents retain the normal Save/Discard/Cancel prompt.

Author: **こまいろ日和 / Komairo Hiyori**. License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). [Author and distribution source](https://github.com/tyamada/manga-prompt-kit/releases/tag/manga-pdf-20261103-v1). Downloaded PDFs are unmodified; editing uses separate copies. When sharing modified or redistributed copies, include the source, author, license and a description of changes.

The current catalogue is retrieved from https://raw.githubusercontent.com/tyamada/manga-prompt-kit/main/releases/pdf-manifest.json . PDFs use the fixed Release URLs in `new_download_url`, never legacy or latest/download URLs. HTTPS, the designated GitHub repository and known Release asset redirect destinations are validated. Authentication is not required.
