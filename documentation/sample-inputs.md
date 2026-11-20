# Verification inputs using real PDFs

User-facing sample manga links point to the [central catalogue](https://tyamada.github.io/manga-prompt-kit/samples/en/). Do not duplicate individual PDFs into docs/sample or Pages.

## Explicit preparation

The fixed Release pdf-manifest.json is saved as tools/data/sample-inputs-v1.json and checked against its pinned SHA-256. Only the requested book is acquired and verified by byte count and SHA-256. The app's latest manifest, existing IDs and user caches are unchanged. Historical Filipino aliases such as ep1_tl resolve to ep1_fil.

```sh
python -m tools.sample_inputs --sample-id ep3_ja --cache-dir /absolute/external/sample-cache --download
python documentation/netbsd-verification/prepare_fixtures.py --cache-dir /absolute/external/sample-cache --output build/netbsd-verification
python documentation/openbsd-verification/verify_gui_results.py --cache-dir /absolute/external/sample-cache --results-dir build/openbsd-verification
```

On Windows, supply an absolute cache path outside the repository. Use --input-dir to supply an existing verified file by its original filename or SHA-256.pdf name. Without --download, no network access occurs; missing or corrupt inputs fail explicitly rather than silently skipping tests.

NetBSD forms and images use small generated fixtures. GUI comparisons against the real eight-page manga are separate integration checks. OpenBSD result verification needs saved real GUI outputs; successful preparation does not establish OpenBSD runtime acceptance.

The old documentation/netbsd-verification/fixtures.json and historical reports remain immutable evidence of their original runs, even where they name the old testdata path. Newly generated fixtures.json records the verified external input path.

## Publication and cleanup

Follow the [maintenance guide](https://github.com/tyamada/manga-prompt-kit/blob/main/docs/sample-download-maintenance.md). Folimeld currently has English and Japanese user-facing Pages, each linked to the matching catalogue. The central catalogue owns the language pages and regional anchors.

Old PDFs with digests different from the current 51-book set remain until their purpose and archival status are established. General regression PDFs, SEASIDE_LIVING, bundled JSON and user-downloaded PDFs are excluded from deletion. If a released app depends on an old URL, keep it available until a compatible app has been distributed.
